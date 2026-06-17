#!/usr/bin/env python3
"""Complete evaluation script for dual stratification hypothesis."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from loguru import logger
import sys
import warnings

warnings.filterwarnings('ignore')
logger.remove()
logger.add(sys.stdout, level="INFO", format="{message}")

workspace = Path("/home/adrian/projects/ai-inventor/aii_data/users/admin/runs/run_-w6fuC_zXl2B/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1")

# Load experiment output
experiment_path = workspace.parent / "gen_art_experiment_1" / "method_out.json"
with open(experiment_path, 'r') as f:
    exp_data = json.load(f)

models = exp_data.get('models', {})
hypothesis = exp_data.get('hypothesis_test_results', {})

logger.info(f"Loaded {len(models)} models")

# Load dataset for mediation analysis
dataset_path = Path("/home/adrian/projects/ai-inventor/aii_data/users/admin/runs/run_-w6fuC_zXl2B/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/data_out.json")
with open(dataset_path, 'r') as f:
    data = json.load(f)

examples = data['datasets'][0]['examples']
rows = []
for ex in examples:
    try:
        input_dict = json.loads(ex['input'])
        output_val = float(ex['output'])
        row = {
            'country': ex.get('metadata_country', 'Unknown'),
            'year': int(ex.get('metadata_year', 0)),
            'v2x_libdem': output_val,
            **input_dict
        }
        rows.append(row)
    except:
        continue

df = pd.DataFrame(rows)
df['gini_x_edu_ineq'] = df['gini'] * df['edu_ineq_index']
logger.info(f"Loaded dataset: {len(df)} rows")

# Run mediation analysis
logger.info("Running mediation analysis with bootstrap CIs...")
required = ['v2x_libdem', 'gini', 'edu_ineq_index', 'gini_x_edu_ineq', 'v2pepwrsoc']
analysis_df = df[required].dropna()

if len(analysis_df) >= 50:
    # Model c: total effect
    X_c = sm.add_constant(analysis_df[['gini', 'edu_ineq_index', 'gini_x_edu_ineq']])
    model_c = sm.OLS(analysis_df['v2x_libdem'], X_c).fit()
    
    # Model a: mediator ~ treatment
    model_a = sm.OLS(analysis_df['v2pepwrsoc'], X_c).fit()
    
    # Model b and c': outcome ~ treatment + mediator
    X_b = sm.add_constant(analysis_df[['gini', 'edu_ineq_index', 'gini_x_edu_ineq', 'v2pepwrsoc']])
    model_b = sm.OLS(analysis_df['v2x_libdem'], X_b).fit()
    
    a = model_a.params.get('gini_x_edu_ineq', 0)
    b = model_b.params.get('v2pepwrsoc', 0)
    c = model_c.params.get('gini_x_edu_ineq', 0)
    c_prime = model_b.params.get('gini_x_edu_ineq', 0)
    
    se_a = model_a.bse.get('gini_x_edu_ineq', 0)
    se_b = model_b.bse.get('v2pepwrsoc', 0)
    
    indirect_effect = a * b
    sobel_se = np.sqrt(a**2 * se_b**2 + b**2 * se_a**2 + se_a**2 * se_b**2)
    sobel_z = indirect_effect / sobel_se if sobel_se > 0 else 0
    sobel_p = 2 * (1 - stats.norm.cdf(abs(sobel_z)))
    
    proportion_mediated = indirect_effect / c if c != 0 else 0
    
    # Bootstrap CI
    bootstrap_effects = []
    for _ in range(1000):
        idx = np.random.choice(len(analysis_df), size=len(analysis_df), replace=True)
        boot_df = analysis_df.iloc[idx]
        
        try:
            boot_a = sm.OLS(boot_df['v2pepwrsoc'], sm.add_constant(boot_df[['gini', 'edu_ineq_index', 'gini_x_edu_ineq']])).fit()
            boot_b = sm.OLS(boot_df['v2x_libdem'], sm.add_constant(boot_df[['gini', 'edu_ineq_index', 'gini_x_edu_ineq', 'v2pepwrsoc']])).fit()
            a_boot = boot_a.params.get('gini_x_edu_ineq', 0)
            b_boot = boot_b.params.get('v2pepwrsoc', 0)
            bootstrap_effects.append(a_boot * b_boot)
        except:
            continue
    
    if len(bootstrap_effects) > 10:
        ci_lower = float(np.percentile(bootstrap_effects, 2.5))
        ci_upper = float(np.percentile(bootstrap_effects, 97.5))
    else:
        ci_lower = float(indirect_effect - 1.96 * sobel_se)
        ci_upper = float(indirect_effect + 1.96 * sobel_se)
    
    mediation_results = {
        'sobel_z': float(sobel_z),
        'sobel_p': float(sobel_p),
        'indirect_effect': float(indirect_effect),
        'direct_effect': float(c_prime),
        'total_effect': float(c),
        'proportion_mediated': float(proportion_mediated),
        'bootstrap_CI': [ci_lower, ci_upper]
    }
    
    logger.info(f"Mediation: Sobel z={sobel_z:.3f}, p={sobel_p:.3f}")
    logger.info(f"Bootstrap CI: [{ci_lower:.3f}, {ci_upper:.3f}]")
else:
    mediation_results = {'error': 'Insufficient data'}

# Save mediation results
with open(workspace / 'mediation_results.json', 'w') as f:
    json.dump(mediation_results, f, indent=2, default=str)
logger.info("Saved mediation_results.json")

# Generate APSR Table 2
logger.info("Generating APSR Table 2...")
var_order = ['gini', 'edu_ineq_index', 'gini_edu_interaction', 'gini_x_edu_ineq',
          'education_spending_gdp', 'gini_x_edu_ineq_x_edu_spend',
          'tertiary_enrollment', 'v2x_libdem_lag']

var_labels = {
    'gini': 'Gini coefficient',
    'edu_ineq_index': 'Education inequality',
    'gini_edu_interaction': 'Gini x Edu ineq',
    'gini_x_edu_ineq': 'Gini x Edu ineq',
    'education_spending_gdp': 'Education spending (% GDP)',
    'gini_x_edu_ineq_x_edu_spend': 'Triple interaction',
    'tertiary_enrollment': 'Tertiary enrollment',
    'v2x_libdem_lag': 'Democratic quality (lag)'
}

def get_stars(pval):
    if pval is None or np.isnan(pval):
        return ''
    if pval < 0.01:
        return '***'
    elif pval < 0.05:
        return '**'
    elif pval < 0.10:
        return '*'
    return ''

lines = []
lines.append("=" * 90)
lines.append("Table 2: Panel Regression Estimates of Dual Stratification on Democratic Quality")
lines.append("=" * 90)
lines.append("")

header = "{0:<35}".format('Variable')
for i, m in enumerate(models.keys(), 1):
    header += " Model {0}{1:<20}".format(i, '')
lines.append(header)
lines.append("-" * 90)

for var in var_order:
    row = "{0:<35}".format(var_labels.get(var, var))
    for model_name, model_data in models.items():
        coef = model_data['coefficients'].get(var, np.nan)
        se = model_data.get('std_errors', {}).get(var, np.nan)
        pval = model_data.get('pvalues', {}).get(var, np.nan)
        
        if not np.isnan(coef):
            stars = get_stars(pval)
            row += " {0:.3f}{1}   ".format(coef, stars)
            row += "({0:.3f})    ".format(se)
        else:
            row += "{0:<25}".format('')
    lines.append(row)

lines.append("-" * 90)

for i, (model_name, model_data) in enumerate(models.items(), 1):
    lines.append("Model {0}: N={1}, Countries={2}".format(i, model_data['n_obs'], model_data['n_groups']))

lines.append("")
lines.append("Note: Panel OLS with country fixed effects; standard errors clustered by country.")
lines.append("*** p<0.01, ** p<0.05, * p<0.10.")
lines.append("=" * 90)

text_table = "\n".join(lines)
with open(workspace / 'table2_apsr.txt', 'w') as f:
    f.write(text_table)
logger.info("Saved Table 2 to table2_apsr.txt")

# Update eval_out.json with all results
logger.info("Updating eval_out.json...")
with open(workspace / 'eval_out.json', 'r') as f:
    eval_output = json.load(f)

# Add missing components
with open(workspace / 'correlations.json', 'r') as f:
    correlations = json.load(f)
eval_output['within_country_correlations'] = correlations

with open(workspace / 'missing_data_report.json', 'r') as f:
    missing_data = json.load(f)
eval_output['data_discrepancy_report'] = missing_data

eval_output['mediation_results'] = mediation_results
eval_output['table2_apsr_text'] = text_table

# Add LaTeX table
latex_lines = []
latex_lines.append("\\begin{table}[htbp]")
latex_lines.append("\\centering")
latex_lines.append("\\caption{Panel Regression Estimates of Dual Stratification}")
latex_lines.append("\\label{tab:results}")
latex_lines.append("\\begin{tabular}{l" + "c" * len(models) + "}")
latex_lines.append("\\hline")
latex_lines.append("\\hline")
latex_lines.append("Variable " + " & ".join([f"Model {i}" for i in range(1, len(models)+1)]) + " \\\\")
latex_lines.append("\\hline")

for var in var_order:
    row = f"{var_labels.get(var, var)} "
    for model_name, model_data in models.items():
        coef = model_data['coefficients'].get(var, np.nan)
        if not np.isnan(coef):
            se = model_data.get('std_errors', {}).get(var, 0)
            row += " & {0:.3f} \\  ({1:.3f}) ".format(coef, se)
        else:
            row += " & & "
    latex_lines.append(row.rstrip(" & ") + " \\\\")

latex_lines.append("\\hline")
latex_lines.append("\\end{tabular}")
latex_lines.append("\\end{table}")

latex_table = "\n".join(latex_lines)
eval_output['table2_apsr_latex'] = latex_table

with open(workspace / 'table2_apsr.tex', 'w') as f:
    f.write(latex_table)
logger.info("Saved LaTeX table to table2_apsr.tex")

# Update metrics_agg
eval_output['metrics_agg']['sobel_z'] = mediation_results.get('sobel_z', 0.0)
eval_output['metrics_agg']['sobel_p'] = mediation_results.get('sobel_p', 1.0)
eval_output['metrics_agg']['proportion_mediated'] = mediation_results.get('proportion_mediated', 0.0)

# Save final eval_out.json
with open(workspace / 'eval_out.json', 'w') as f:
    json.dump(eval_output, f, indent=2, default=str)

logger.info("Updated eval_out.json with all results")
logger.info("Evaluation completed successfully!")
