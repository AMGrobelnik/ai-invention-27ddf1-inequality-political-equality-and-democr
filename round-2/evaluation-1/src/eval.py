#!/usr/bin/env python3
"""
Evaluation Script: Panel OLS Results Validation for Dual Stratification Hypothesis

Evaluates the experiment output (Panel OLS with entity/time effects) and produces
a properly formatted eval_out.json with complete evaluation metrics.

Adapted from the original GMM-focused plan to handle the actual Panel OLS output.
"""

from loguru import logger
from pathlib import Path
import json
import sys
import numpy as np
from scipy import stats
import warnings
from typing import Dict, List, Any, Optional, Tuple

warnings.filterwarnings('ignore')

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")


def load_experiment_output() -> Optional[Dict[str, Any]]:
    """Load method_out.json from experiment artifact."""
    # Try iter_2 first
    exp_path = Path("/home/adrian/projects/ai-inventor/aii_data/users/admin/runs/run_-w6fuC_zXl2B/3_invention_loop/iter_2/gen_art/gen_art_experiment_1/method_out.json")
    
    if not exp_path.exists():
        # Fallback to iter_1
        exp_path = Path("/home/adrian/projects/ai-inventor/aii_data/users/admin/runs/run_-w6fuC_zXl2B/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method_out.json")
    
    if not exp_path.exists():
        logger.error("Experiment output not found in either iter_2 or iter_1")
        return None
    
    logger.info(f"Loading experiment output from {exp_path}")
    with open(exp_path, 'r') as f:
        data = json.load(f)
    
    return data


def evaluate_models(experiment_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate Panel OLS models from experiment output.
    
    For Panel OLS, we check:
    - Coefficient signs and significance
    - R-squared (reasonable values)
    - N > parameters (sufficient degrees of freedom)
    - F-tests for joint significance (implicit in p-values)
    """
    models = experiment_data.get('metadata', {}).get('models', {})
    
    if not models:
        logger.warning("No models found in experiment output")
        return {}
    
    results = {
        'specification_tests': {},
        'model_summaries': {}
    }
    
    for model_name, model_data in models.items():
        if model_name == 'Model 3_mediation':
            continue  # Handle mediation separately
        
        logger.info(f"Evaluating {model_name}")
        
        # Extract model info
        coefs = model_data.get('coefficients', {})
        ses = model_data.get('std_errors', {})
        pvals = model_data.get('pvalues', {})
        n_obs = model_data.get('n_obs', 0)
        n_groups = model_data.get('n_groups', 0)
        r_squared = model_data.get('r_squared', 0)
        
        # Calculate t-statistics
        t_stats = {}
        for var in coefs:
            if var in ses and ses[var] != 0:
                t_stats[var] = coefs[var] / ses[var]
        
        # Specification checks for Panel OLS
        checks = {
            'r_squared': r_squared,
            'r_squared_reasonable': 0.0 <= r_squared <= 0.95,
            'n_obs': n_obs,
            'n_params': len(coefs),
            'n_obs_sufficient': n_obs > 3 * len(coefs),
            'n_groups': n_groups,
            'entity_effects': n_groups > 1
        }
        
        # Check key hypothesis-related variables
        if 'gini_edu_interaction' in pvals:
            checks['interaction_sig'] = pvals['gini_edu_interaction'] < 0.05
            checks['interaction_negative'] = coefs.get('gini_edu_interaction', 0) < 0
        
        if 'triple_interaction' in pvals:
            checks['triple_sig'] = pvals['triple_interaction'] < 0.05
            checks['triple_positive'] = coefs.get('triple_interaction', 0) > 0
        
        results['specification_tests'][model_name] = checks
        results['model_summaries'][model_name] = {
            'coefficients': coefs,
            'std_errors': ses,
            't_statistics': t_stats,
            'p_values': pvals,
            'n_obs': n_obs,
            'n_groups': n_groups,
            'r_squared': r_squared
        }
    
    return results


def generate_apsr_table(models_eval: Dict[str, Any]) -> Tuple[str, str]:
    """
    Generate APSR-formatted regression table.
    
    Returns: (latex_table, text_table)
    """
    
    def significance_stars(pval):
        if pval < 0.01:
            return "***"
        elif pval < 0.05:
            return "**"
        elif pval < 0.10:
            return "*"
        return ""
    
    variables = [
        'v2x_libdem_lag',
        'gini',
        'edu_ineq_index',
        'gini_edu_interaction',
        'triple_interaction',
        'education_spending_gdp'
    ]
    
    var_labels = {
        'v2x_libdem_lag': 'Democratic Quality$_{t-1}$',
        'gini': 'Gini Coefficient',
        'edu_ineq_index': 'Education Inequality Index',
        'gini_edu_interaction': 'Gini $\\times$ Edu Inequality',
        'triple_interaction': 'Gini $\\times$ Edu Ineq $\\times$ Edu Spend',
        'education_spending_gdp': 'Education Spending (\\% GDP)'
    }
    
    model_names = ['Model 1', 'Model 2', 'Model 4']
    
    # LaTeX table
    latex_lines = []
    latex_lines.append("\\begin{table}[htbp]")
    latex_lines.append("\\centering")
    latex_lines.append("\\caption{Panel OLS Estimates of Democratic Quality}")
    latex_lines.append("\\label{tab:dual_stratification}")
    latex_lines.append("\\begin{tabular}{lccc}")
    latex_lines.append("\\hline")
    latex_lines.append(" & (1) & (2) & (3) \\\\")
    latex_lines.append(" & Main & Interaction & Triple \\\\")
    latex_lines.append("\\hline")
    
    for var in variables:
        row = f"{var_labels.get(var, var)} "
        for model_name in model_names:
            if model_name in models_eval['model_summaries']:
                summary = models_eval['model_summaries'][model_name]
                if var in summary['coefficients']:
                    coef = summary['coefficients'][var]
                    se = summary['std_errors'][var]
                    pval = summary['p_values'][var]
                    stars = significance_stars(pval)
                    
                    row += f" & {coef:.4f}{stars} \\\\ [{se:.4f}] "
                else:
                    row += " & "
            else:
                row += " & "
        row += "\\\\"
        latex_lines.append(row)
    
    latex_lines.append("\\hline")
    latex_lines.append("\\hline")
    
    # Add N and R-squared
    for i, model_name in enumerate(model_names):
        if i == 0:
            line = "Observations "
        else:
            line = ""
        
        if model_name in models_eval['model_summaries']:
            summary = models_eval['model_summaries'][model_name]
            line += f" & {summary['n_obs']} "
        else:
            line += " & "
        
        if i == len(model_names) - 1:
            line += "\\\\"
        latex_lines.append(line)
    
    for i, model_name in enumerate(model_names):
        if i == 0:
            line = "R-squared "
        else:
            line = ""
        
        if model_name in models_eval['model_summaries']:
            summary = models_eval['model_summaries'][model_name]
            line += f" & {summary['r_squared']:.3f} "
        else:
            line += " & "
        
        if i == len(model_names) - 1:
            line += "\\\\"
        latex_lines.append(line)
    
    latex_lines.append("\\hline")
    latex_lines.append("\\multicolumn{4}{p{\\linewidth}}{\\footnotesize Panel OLS estimates with entity and time fixed effects; standard errors clustered by country in brackets. *** p$<$0.01, ** p$<$0.05, * p$<$0.10.}")
    latex_lines.append("\\end{tabular}")
    latex_lines.append("\\end{table}")
    
    latex_table = "\n".join(latex_lines)
    
    # Text table
    text_lines = []
    text_lines.append("=" * 90)
    text_lines.append("Table 2: Panel OLS Estimates of Democratic Quality")
    text_lines.append("=" * 90)
    header = f"{'Variable':<35}"
    for m in model_names:
        header += f" {m:<18}"
    text_lines.append(header)
    text_lines.append("-" * 90)
    
    for var in variables:
        row = f"{var_labels.get(var, var):<35}"
        for model_name in model_names:
            if model_name in models_eval['model_summaries']:
                summary = models_eval['model_summaries'][model_name]
                if var in summary['coefficients']:
                    coef = summary['coefficients'][var]
                    se = summary['std_errors'][var]
                    pval = summary['p_values'][var]
                    stars = significance_stars(pval)
                    row += f" {coef:.4f}{stars}".ljust(20)
                else:
                    row += " " * 18
            else:
                row += " " * 18
        text_lines.append(row)
        # Add SE on next line
        row2 = f"{'':<35}"
        for model_name in model_names:
            if model_name in models_eval['model_summaries']:
                summary = models_eval['model_summaries'][model_name]
                if var in summary['std_errors']:
                    se = summary['std_errors'][var]
                    row2 += f" [{se:.4f}]".ljust(20)
                else:
                    row2 += " " * 18
            else:
                row2 += " " * 18
        text_lines.append(row2)
    
    text_lines.append("-" * 90)
    obs_line = f"{'Observations':<35}"
    for model_name in model_names:
        if model_name in models_eval['model_summaries']:
            n = models_eval['model_summaries'][model_name]['n_obs']
            obs_line += f" {n} ".ljust(20)
        else:
            obs_line += " " * 18
    text_lines.append(obs_line)
    
    text_lines.append("")
    text_lines.append("Note: Panel OLS with entity and time fixed effects.")
    text_lines.append("      Standard errors clustered by country in brackets.")
    text_lines.append("      *** p<0.01, ** p<0.05, * p<0.10")
    text_lines.append("=" * 90)
    
    text_table = "\n".join(text_lines)
    
    return latex_table, text_table


def evaluate_hypothesis(experiment_data: Dict[str, Any], models_eval: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate whether the dual stratification hypothesis is confirmed.
    
    Criteria:
    1. Gini × education inequality interaction is negative and significant (p < 0.05)
    2. Political equality (v2pepwrsoc) mediates the relationship (Sobel test p < 0.05)
    3. Triple interaction (Gini × edu ineq × edu spend) is positive and significant
    """
    
    criterion1_met = False
    criterion2_met = False
    criterion3_met = False
    
    reasoning_points = []
    
    # Criterion 1: Interaction term in Model 2
    if 'Model 2' in models_eval['model_summaries']:
        summary = models_eval['model_summaries']['Model 2']
        if 'gini_edu_interaction' in summary['coefficients']:
            coef = summary['coefficients']['gini_edu_interaction']
            pval = summary['p_values']['gini_edu_interaction']
            
            if coef < 0 and pval < 0.05:
                criterion1_met = True
                reasoning_points.append(f"Criterion 1 MET: Interaction coef = {coef:.4f}, p = {pval:.3f}")
            else:
                reasoning_points.append(f"Criterion 1 NOT MET: Interaction coef = {coef:.4f}, p = {pval:.3f} (need negative, p<0.05)")
    
    # Criterion 2: Mediation
    models = experiment_data.get('metadata', {}).get('models', {})
    if 'Model 3_mediation' in models:
        mediation = models['Model 3_mediation']
        paths = mediation.get('paths', [])
        
        indirect_path = [p for p in paths if p.get('path') == 'Indirect']
        if indirect_path:
            indirect_pval = indirect_path[0].get('pval', 1)
            
            if indirect_pval < 0.05:
                criterion2_met = True
                reasoning_points.append(f"Criterion 2 MET: Indirect effect p = {indirect_pval:.3f}")
            else:
                reasoning_points.append(f"Criterion 2 NOT MET: Indirect effect p = {indirect_pval:.3f}")
    
    # Criterion 3: Triple interaction in Model 4
    if 'Model 4' in models_eval['model_summaries']:
        summary = models_eval['model_summaries']['Model 4']
        if 'triple_interaction' in summary['coefficients']:
            coef = summary['coefficients']['triple_interaction']
            pval = summary['p_values']['triple_interaction']
            
            if coef > 0 and pval < 0.05:
                criterion3_met = True
                reasoning_points.append(f"Criterion 3 MET: Triple interaction coef = {coef:.6f}, p = {pval:.3f}")
            else:
                reasoning_points.append(f"Criterion 3 NOT MET: Triple interaction coef = {coef:.6f}, p = {pval:.3f}")
    
    confirmed = criterion1_met and criterion2_met and criterion3_met
    
    reasoning = "\n".join(reasoning_points)
    if confirmed:
        reasoning += "\n\nOVERALL: All criteria met. Hypothesis CONFIRMED."
    else:
        failed = []
        if not criterion1_met:
            failed.append("Criterion 1 (interaction)")
        if not criterion2_met:
            failed.append("Criterion 2 (mediation)")
        if not criterion3_met:
            failed.append("Criterion 3 (triple interaction)")
        reasoning += f"\n\nOVERALL: Hypothesis NOT CONFIRMED. Failed: {', '.join(failed)}."
    
    return {
        'confirmed': confirmed,
        'criterion1_met': criterion1_met,
        'criterion2_met': criterion2_met,
        'criterion3_met': criterion3_met,
        'reasoning': reasoning
    }


def create_output(experiment_data: Dict[str, Any], models_eval: Dict[str, Any], 
                  latex_table: str, text_table: str, hypothesis_eval: Dict[str, Any]) -> Dict[str, Any]:
    """Create the final output dictionary."""
    
    output = {
        'evaluation_metadata': {
            'evaluator': 'gen_art_evaluation_1',
            'timestamp': str(Path(__file__).stat().st_mtime),
            'experiment_output_loaded': True
        },
        'specification_tests': models_eval.get('specification_tests', {}),
        'table2_apsr_latex': latex_table,
        'table2_apsr_text': text_table,
        'hypothesis_evaluation': hypothesis_eval,
        'experiment_summary': {
            'method': experiment_data.get('metadata', {}).get('method', 'Unknown'),
            'n_countries': experiment_data.get('metadata', {}).get('n_countries', 0),
            'n_obs_total': experiment_data.get('metadata', {}).get('n_obs', 0),
            'years': experiment_data.get('metadata', {}).get('years', 'Unknown')
        }
    }
    
    # Add model summaries
    output['model_summaries'] = models_eval.get('model_summaries', {})
    
    # Add mediation results if available
    models = experiment_data.get('metadata', {}).get('models', {})
    if 'Model 3_mediation' in models:
        output['mediation_results'] = models['Model 3_mediation']
    
    # Add data discrepancy info (from previous analysis)
    output['data_discrepancy_report'] = {
        'note': 'Panel OLS used; no GMM instrument checks needed',
        'missing_data_available': True
    }
    
    return output


@logger.catch(reraise=True)
def main():
    """Main evaluation function."""
    
    logger.info("Starting evaluation of Dual Stratification Hypothesis experiment")
    
    # Load experiment output
    experiment_data = load_experiment_output()
    
    if experiment_data is None:
        logger.error("Cannot proceed without experiment output")
        output = {
            'evaluation_metadata': {
                'evaluator': 'gen_art_evaluation_1',
                'timestamp': 'unknown',
                'experiment_output_loaded': False,
                'error': 'Experiment output not found'
            }
        }
        with open('eval_out.json', 'w') as f:
            json.dump(output, f, indent=2)
        return
    
    # Evaluate models
    logger.info("Evaluating models")
    models_eval = evaluate_models(experiment_data)
    
    # Generate tables
    logger.info("Generating APSR tables")
    latex_table, text_table = generate_apsr_table(models_eval)
    
    # Save tables
    Path('table2_apsr.tex').write_text(latex_table)
    Path('table2_apsr.txt').write_text(text_table)
    logger.info("Tables saved")
    
    # Evaluate hypothesis
    logger.info("Evaluating hypothesis")
    hypothesis_eval = evaluate_hypothesis(experiment_data, models_eval)
    
    # Create output
    output = create_output(experiment_data, models_eval, latex_table, text_table, hypothesis_eval)
    
    # Save output
    output_path = Path('eval_out.json')
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    logger.info(f"Evaluation complete. Output saved to {output_path}")
    
    # Print summary
    print("\n" + "="*60)
    print("EVALUATION SUMMARY")
    print("="*60)
    print(f"Method: {output['experiment_summary']['method']}")
    print(f"N countries: {output['experiment_summary']['n_countries']}")
    print(f"N observations: {output['experiment_summary']['n_obs_total']}")
    print("-" * 60)
    print(f"Hypothesis Confirmed: {hypothesis_eval['confirmed']}")
    print(f"  Criterion 1 (Interaction negative/significant): {hypothesis_eval['criterion1_met']}")
    print(f"  Criterion 2 (Mediation significant): {hypothesis_eval['criterion2_met']}")
    print(f"  Criterion 3 (Triple interaction positive/significant): {hypothesis_eval['criterion3_met']}")
    print("="*60)
    print("\nReasoning:")
    print(hypothesis_eval['reasoning'])


if __name__ == "__main__":
    main()
