#!/usr/bin/env python3
"""
Fast dataset builder for post-1990 democratizers.
Fixes NaN issue and adds required V-Dem political equality variable.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path

WORKSPACE = Path("/home/adrian/projects/ai-inventor/aii_data/users/admin/runs/run_-w6fuC_zXl2B/3_invention_loop/iter_2/gen_art/gen_art_dataset_1")
OWID_TABLES = Path("/home/adrian/projects/ai-inventor/.claude/skills/aii-owid-datasets/temp/tables")

def clean_nan(obj):
    """Convert pandas NaN to None for JSON serialization."""
    if isinstance(obj, dict):
        return {k: clean_nan(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nan(v) for v in obj]
    elif isinstance(obj, float) and np.isnan(obj):
        return None
    elif pd.isna(obj):
        return None
    return obj

def main():
    print("Building dataset for post-1990 democratizers...")
    
    # Define post-1990 democratizers
    democratizers = {
        "Benin": 1995, "Bulgaria": 1991, "Cape Verde": 1991,
        "Estonia": 1993, "Latvia": 1992, "Mongolia": 1992,
        "Namibia": 1995, "Panama": 1991, "Sao Tome and Principe": 1992,
        "South Africa": 1995, "Suriname": 1992, "Czech Republic": 1993,
        "Slovakia": 1993, "Slovenia": 1991, "Croatia": 2000,
        "Romania": 1996, "Lithuania": 1991, "Ghana": 1992,
        "Malawi": 1994, "Chile": 1990, "Brazil": 1985,
    }
    
    # Create base panel (1990-2023)
    rows = []
    for country, trans_year in democratizers.items():
        for year in range(1990, 2024):
            rows.append({
                "country": country,
                "year": year,
                "transition_year": trans_year,
                "post_transition": year >= trans_year
            })
    
    df = pd.DataFrame(rows)
    print(f"Base panel: {len(df)} obs ({len(democratizers)} countries × 34 years)")
    
    # Load V-Dem v.14 data
    print("Loading V-Dem v.14...")
    vdem_file = OWID_TABLES / "full_garden_democracy_2024-03-07_vdem_vdem.json"
    if vdem_file.exists():
        with open(vdem_file, 'r') as f:
            vdem_data = json.load(f)
        vdem_df = pd.DataFrame(vdem_data)
        
        # Get key variables for our countries
        vdem_vars = ['country', 'year', 'v2x_libdem', 'v2pepwrsoc', 
                     'v2x_polyarchy', 'v2x_freexp_altinf', 'v2x_delibdem']
        
        # Filter to available columns
        avail_cols = [c for c in vdem_vars if c in vdem_df.columns]
        vdem_subset = vdem_df[avail_cols].copy()
        
        # Rename for clarity
        rename_map = {
            'v2x_libdem': 'libdem_vdem',
            'v2pepwrsoc': 'pol_eq_vdem',
            'v2x_polyarchy': 'electdem_vdem',
            'v2x_freexp_altinf': 'freexp_vdem',
            'v2x_delibdem': 'delibdem_vdem'
        }
        vdem_subset = vdem_subset.rename(columns=rename_map)
        
        df = df.merge(vdem_subset, on=['country', 'year'], how='left')
        print(f"  Merged V-Dem variables: {list(vdem_subset.columns[2:])}")
    
    # Load income inequality from PIP
    print("Loading income inequality (PIP)...")
    pip_file = OWID_TABLES / "full_garden_wb_2025-10-09_world_bank_pip_legacy_income_consumption_2021_gini.json"
    if pip_file.exists():
        with open(pip_file, 'r') as f:
            pip_data = json.load(f)
        pip_df = pd.DataFrame(pip_data)
        
        # Extract Gini from consumption spells
        def extract_gini(row):
            for i in range(1, 9):
                val = row.get(f'consumption_spell_{i}')
                if val is not None and not pd.isna(val):
                    return val
            return None
        
        pip_df['gini_income'] = pip_df.apply(extract_gini, axis=1)
        pip_gini = pip_df[['country', 'year', 'gini_income']].copy()
        
        df = df.merge(pip_gini, on=['country', 'year'], how='left')
        print(f"  Merged Gini: {df['gini_income'].notna().sum()} non-null values")
    
    # Load education spending from EdStats
    print("Loading education spending (EdStats)...")
    edstats_file = OWID_TABLES / "full_garden_wb_2024-11-04_edstats_edstats.json"
    if edstats_file.exists():
        with open(edstats_file, 'r') as f:
            edstats_data = json.load(f)
        edstats_df = pd.DataFrame(edstats_data)
        
        # Education spending
        spend_col = 'government_expenditure_on_education__total__pct_of_gdp'
        if spend_col in edstats_df.columns:
            spend_data = edstats_df[['country', 'year', spend_col]].copy()
            spend_data = spend_data.rename(columns={spend_col: 'education_spending_gdp'})
            df = df.merge(spend_data, on=['country', 'year'], how='left')
            print(f"  Merged education spending: {df['education_spending_gdp'].notna().sum()} non-null")
        
        # Expected years of schooling
        if 'expected_years_of_school' in edstats_df.columns:
            edu_years = edstats_df[['country', 'year', 'expected_years_of_school']].copy()
            df = df.merge(edu_years, on=['country', 'year'], how='left')
    
    # Calculate summary statistics
    print("\n=== DATASET SUMMARY ===")
    print(f"Countries: {df['country'].nunique()}")
    print(f"Years: {df['year'].min()}-{df['year'].max()}")
    print(f"Total observations: {len(df)}")
    
    # Build data dictionary
    data_dict = {}
    for col in df.columns:
        if col in ['country', 'year', 'transition_year', 'post_transition']:
            continue
        non_null = int(df[col].notna().sum())
        if pd.api.types.is_numeric_dtype(df[col]):
            mean_val = df[col].mean()
            std_val = df[col].std()
            data_dict[col] = {
                'type': 'numeric',
                'non_null': non_null,
                'mean': round(float(mean_val), 4) if not pd.isna(mean_val) else None,
                'std': round(float(std_val), 4) if not pd.isna(std_val) else None,
            }
    
    # Create output
    output = {
        "metadata": {
            "n_countries": int(df['country'].nunique()),
            "n_years": 34,
            "total_observations": int(len(df)),
            "year_range": {"start": 1990, "end": 2023},
            "variables": list(df.columns),
            "democratizers": [{"country": c, "transition_year": y} 
                             for c, y in democratizers.items()]
        },
        "documentation": {
            "data_dict": data_dict,
            "sources": {
                "vdem": "V-Dem v.14 (liberal democracy, political equality indices)",
                "pip": "World Bank PIP (income inequality Gini)",
                "edstats": "World Bank EdStats (education spending and attainment)"
            }
        },
        "data": clean_nan(df.to_dict(orient='records'))
    }
    
    # Save
    print("\nSaving...")
    with open(WORKSPACE / "data_out.json", 'w') as f:
        json.dump(output, f, indent=2, default=str)
    
    # Mini version
    mini_df = df.sample(frac=0.1, random_state=42)
    mini_output = output.copy()
    mini_output['data'] = clean_nan(mini_df.to_dict(orient='records'))
    mini_output['metadata']['total_observations'] = int(len(mini_df))
    with open(WORKSPACE / "data_out_mini.json", 'w') as f:
        json.dump(mini_output, f, indent=2, default=str)
    
    print(f"Done! Files saved.")
    print(f"  data_out.json: {(WORKSPACE / 'data_out.json').stat().st_size / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    main()
