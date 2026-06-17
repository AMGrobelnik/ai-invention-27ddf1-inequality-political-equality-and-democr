#!/usr/bin/env python3
"""Mediation analysis with bootstrap CIs."""
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

# Load dataset
workspace = Path("/home/adrian/projects/ai-inventor/aii_data/users/admin/runs/run_-w6fuC_zXl2B/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1")
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
logger.info(f"Loaded dataset: {len(df)} rows")

# Run mediation analysis
required = ['v2x_libdem', 'gini', 'edu_ineq_index', 'gini_x_edu_ineq', 'v2pepwrsoc']
if all(v in df.columns for v in required):
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
        
        # Save mediation results
        with open(workspace / 'mediation_results.json', 'w') as f:
            json.dump(mediation_results, f, indent=2)
        logger.info("Saved mediation_results.json")
else:
    logger.warning("Missing variables for mediation analysis")
