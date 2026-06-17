#!/usr/bin/env python3
"""
Fix and rebuild the merged dataset for post-1990 democratizers.
Corrects issues: year range (cap at 2023), adds proper documentation,
improves variable selection.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path

# Paths
WORKSPACE = Path("/home/adrian/projects/ai-inventor/aii_data/users/admin/runs/run_-w6fuC_zXl2B/3_invention_loop/iter_2/gen_art/gen_art_dataset_1")
OWID_TABLES = Path("/home/adrian/projects/ai-inventor/.claude/skills/aii-owid-datasets/temp/tables")

def load_json(path):
    """Load JSON file."""
    with open(path, 'r') as f:
        return json.load(f)

def save_json(data, path):
    """Save data to JSON file."""
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, default=str)

def main():
    print("Starting dataset fix for post-1990 democratizers...")
    
    # Load existing merged data
    existing_file = WORKSPACE / "data_out.json"
    if existing_file.exists():
        print(f"Loading existing data from {existing_file}...")
        with open(existing_file, 'r') as f:
            existing_data = json.load(f)
        existing_df = pd.DataFrame(existing_data['data'])
        print(f"  Loaded {len(existing_df)} observations")
    else:
        print("No existing data found, building from scratch...")
        existing_df = None
    
    # Define post-1990 democratizers with transition years
    democratizers = {
        "Benin": 1995,
        "Bulgaria": 1991,
        "Cape Verde": 1991,
        "Estonia": 1993,
        "Latvia": 1992,
        "Mongolia": 1992,
        "Namibia": 1995,
        "Panama": 1991,
        "Sao Tome and Principe": 1992,
        "South Africa": 1995,
        "Suriname": 1992,
        "Czech Republic": 1993,
        "Slovakia": 1993,
        "Slovenia": 1991,
        "Croatia": 2000,
        "Romania": 1996,
        "Lithuania": 1991,
        "Ghana": 1992,
        "Malawi": 1994,
        "Chile": 1990,
        "Brazil": 1985,
    }
    
    # Create base panel
    print("Creating base panel...")
    rows = []
    for country, trans_year in democratizers.items():
        for year in range(1990, 2024):  # Cap at 2023
            rows.append({
                "country": country,
                "year": year,
                "transition_year": trans_year,
                "post_transition": year >= trans_year
            })
    
    df = pd.DataFrame(rows)
    print(f"  Base panel: {len(df)} observations ({len(democratizers)} countries × 34 years)")
    
    # Load and merge V-Dem data (from existing if available)
    if existing_df is not None and 'libdem_vdem' in existing_df.columns:
        print("Merging V-Dem variables from existing data...")
        vdem_cols = [c for c in existing_df.columns if 'vdem' in c]
        vdem_data = existing_df[['country', 'year'] + vdem_cols].copy()
        df = df.merge(vdem_data, on=['country', 'year'], how='left')
        print(f"  Merged {len(vdem_cols)} V-Dem variables")
    
    # Load and merge income inequality from PIP
    print("Loading World Bank PIP income inequality data...")
    pip_file = OWID_TABLES / "full_garden_wb_2025-10-09_world_bank_pip_legacy_income_consumption_2021_gini.json"
    if pip_file.exists():
        pip_data = load_json(pip_file)
        pip_df = pd.DataFrame(pip_data)
        
        # Extract Gini from consumption_spell columns (take first non-null)
        def extract_gini(row):
            for i in range(1, 9):
                val = row.get(f'consumption_spell_{i}')
                if val is not None and not pd.isna(val):
                    return val
            return None
        
        pip_df['gini_income_pip'] = pip_df.apply(extract_gini, axis=1)
        pip_gini = pip_df[['country', 'year', 'gini_income_pip']].copy()
        
        df = df.merge(pip_gini, on=['country', 'year'], how='left')
        print(f"  Merged PIP Gini coefficients")
        print(f"  Non-null Gini values: {df['gini_income_pip'].notna().sum()}")
    
    # Load and merge education spending from EdStats
    print("Loading World Bank EdStats education data...")
    edstats_file = OWID_TABLES / "full_garden_wb_2024-11-04_edstats_edstats.json"
    if edstats_file.exists():
        edstats_data = load_json(edstats_file)
        edstats_df = pd.DataFrame(edstats_data)
        
        # Get education spending variable
        if 'government_expenditure_on_education__total__pct_of_gdp' in edstats_df.columns:
            edu_spend = edstats_df[['country', 'year', 'government_expenditure_on_education__total__pct_of_gdp']].copy()
            edu_spend = edu_spend.rename(columns={'government_expenditure_on_education__total__pct_of_gdp': 'education_spending_gdp'})
            df = df.merge(edu_spend, on=['country', 'year'], how='left')
            print(f"  Merged education spending (% GDP)")
            print(f"  Non-null values: {df['education_spending_gdp'].notna().sum()}")
        
        # Get expected years of schooling (proxy for education quantity)
        if 'expected_years_of_school' in edstats_df.columns:
            edu_years = edstats_df[['country', 'year', 'expected_years_of_school']].copy()
            df = df.merge(edu_years, on=['country', 'year'], how='left')
            print(f"  Merged expected years of schooling")
    
    # Try to load SWIID data if available (check common locations)
    print("Checking for SWIID data...")
    swiid_paths = [
        WORKSPACE / "swiid.csv",
        WORKSPACE / "data" / "swiid.csv",
        Path.home() / "Downloads" / "swiid.csv",
    ]
    swiid_found = False
    for sp in swiid_paths:
        if sp.exists():
            print(f"  Found SWIID data at {sp}")
            swiid_df = pd.read_csv(sp)
            # Try to identify Gini column
            gini_col = [c for c in swiid_df.columns if 'gini' in c.lower()]
            if gini_col:
                swiid_df = swiid_df.rename(columns={gini_col[0]: 'gini_income_swiid'})
                df = df.merge(swiid_df[['country', 'year', 'gini_income_swiid']], 
                             on=['country', 'year'], how='left')
                print(f"  Merged SWIID Gini coefficients")
                swiid_found = True
            break
    
    if not swiid_found:
        print("  SWIID data not found, using PIP Gini as primary")
        df['gini_income'] = df['gini_income_pip']
    
    # Calculate summary statistics
    print("\n=== DATASET SUMMARY ===")
    print(f"Countries: {df['country'].nunique()}")
    print(f"Years: {df['year'].min()} - {df['year'].max()}")
    print(f"Total observations: {len(df)}")
    
    # Document variables
    data_dict = {}
    for col in df.columns:
        if col in ['country', 'year', 'transition_year']:
            continue
        non_null = df[col].notna().sum()
        if df[col].dtype in ['float64', 'int64']:
            mean_val = df[col].mean()
            std_val = df[col].std()
            data_dict[col] = {
                'type': 'numeric',
                'non_null': int(non_null),
                'mean': round(float(mean_val), 4) if not pd.isna(mean_val) else None,
                'std': round(float(std_val), 4) if not pd.isna(std_val) else None,
            }
        else:
            data_dict[col] = {
                'type': 'other',
                'non_null': int(non_null),
            }
    
    # Create output structure
    output = {
        "metadata": {
            "n_countries": int(df['country'].nunique()),
            "n_years": int(df['year'].max() - df['year'].min() + 1),
            "total_observations": int(len(df)),
            "year_range": {
                "start": int(df['year'].min()),
                "end": int(df['year'].max())
            },
            "variables": list(df.columns),
            "democratizers": [{"country": c, "transition_year": y} 
                             for c, y in democratizers.items()]
        },
        "documentation": {
            "data_dict": data_dict,
            "sources": {
                "vdem": "V-Dem v.14 Country-Year Dataset (liberal democracy indices)",
                "pip": "World Bank Poverty and Inequality Platform (PIP) - income inequality Gini",
                "edstats": "World Bank Education Statistics (EdStats) - education spending and attainment",
                "swiid": "Standardized World Income Inequality Database (SWIID) - if available"
            },
            "notes": [
                "Dataset covers post-1990 democratizer countries",
                "Year range capped at 2023",
                "Income inequality from World Bank PIP (consumption-based Gini)",
                "Education spending as % of GDP from World Bank EdStats",
                "V-Dem variables: v2x_libdem (liberal democracy), v2pepwrsoc (political equality)"
            ]
        },
        "data": df.to_dict(orient='records')
    }
    
    # Save output
    print("\nSaving output files...")
    save_json(output, WORKSPACE / "data_out.json")
    
    # Create mini version (10% of observations)
    mini_df = df.sample(frac=0.1, random_state=42)
    mini_output = output.copy()
    mini_output['data'] = mini_df.to_dict(orient='records')
    mini_output['metadata']['total_observations'] = int(len(mini_df))
    save_json(mini_output, WORKSPACE / "data_out_mini.json")
    
    # Create preview version (first 10 rows)
    preview_df = df.head(10)
    preview_output = output.copy()
    preview_output['data'] = preview_df.to_dict(orient='records')
    preview_output['metadata']['total_observations'] = int(len(preview_df))
    save_json(preview_output, WORKSPACE / "data_out_preview.json")
    
    print(f"\nOutput files saved:")
    print(f"  data_out.json: { (WORKSPACE / 'data_out.json').stat().st_size / 1024 / 1024:.2f} MB")
    print(f"  data_out_mini.json: { (WORKSPACE / 'data_out_mini.json').stat().st_size / 1024 / 1024:.2f} MB")
    print(f"  data_out_preview.json: { (WORKSPACE / 'data_out_preview.json').stat().st_size / 1024:.2f} KB")
    
    print("\nDone!")

if __name__ == "__main__":
    main()
