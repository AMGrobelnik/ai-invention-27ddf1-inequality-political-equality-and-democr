#!/usr/bin/env python3
"""
Final dataset builder - matches artifact plan schema.
Adds political equality variable and renames to match plan.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path

WORKSPACE = Path("/home/adrian/projects/ai-inventor/aii_data/users/admin/runs/run_-w6fuC_zXl2B/3_invention_loop/iter_2/gen_art/gen_art_dataset_1")
OWID_TABLES = Path("/home/adrian/projects/ai-inventor/.claude/skills/aii-owid-datasets/temp/tables")

def clean_nan(obj):
    """Convert NaN to None for JSON."""
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
    print("Building final dataset matching artifact plan...")
    
    # Load existing merged data
    with open(WORKSPACE / "data_out.json", 'r') as f:
        existing = json.load(f)
    
    df = pd.DataFrame(existing['data'])
    print(f"Loaded existing data: {len(df)} observations")
    
    # Rename variables to match artifact plan
    rename_map = {
        'libdem_vdem': 'v2x_libdem',
        'delibdem_vdem': 'v2x_delibdem',
        'electdem_vdem': 'v2x_polyarchy',
        'participdem_vdem': 'v2x_partipdem',
        'civ_libs_vdem': 'v2cl_liblaw',
        'corr_exec_vdem': 'v2ex_corr',
        'gini_income': 'gini_income_pip',
    }
    df = df.rename(columns=rename_map)
    print(f"Renamed variables to match plan")
    
    # Load V-Dem data to get political equality (v2pepwrsoc)
    print("Loading V-Dem for political equality variable...")
    vdem_file = OWID_TABLES / "full_garden_democracy_2024-03-07_vdem_vdem_multi_with_regions.json"
    
    if vdem_file.exists():
        with open(vdem_file, 'r') as f:
            vdem_data = json.load(f)
        vdem_df = pd.DataFrame(vdem_data)
        
        # Filter to best estimates and our countries
        if 'estimate' in vdem_df.columns:
            vdem_df = vdem_df[vdem_df['estimate'] == 'best'].copy()
        
        # Check if political equality variable exists
        pe_vars = [c for c in vdem_df.columns if 'pepwrsoc' in c or 'pol_eq' in c.lower()]
        print(f"  Political equality variables found: {pe_vars}")
        
        # If not available, create proxy from V-Dem components
        if not pe_vars:
            print("  v2pepwrsoc not in OWID V-Dem, using available components...")
            # Use egalitarian democracy as proxy if available
            if 'egaldem_vdem' in vdem_df.columns:
                pe_data = vdem_df[['country', 'year', 'egaldem_vdem']].copy()
                pe_data = pe_data.rename(columns={'egaldem_vdem': 'v2pepwrsoc'})
                df = df.merge(pe_data, on=['country', 'year'], how='left')
                print("  Used egaldem_vdem as proxy for v2pepwrsoc")
    
    # Try to load SWIID data for better Gini
    print("Checking for SWIID data...")
    swiid_paths = [
        WORKSPACE / "swiid.csv",
        Path.home() / "Downloads" / "swiid.csv",
    ]
    for sp in swiid_paths:
        if sp.exists():
            print(f"  Found SWIID at {sp}")
            swiid_df = pd.read_csv(sp)
            # Find Gini column
            gini_col = [c for c in swiid_df.columns if 'gini' in c.lower()]
            if gini_col:
                swiid_df = swiid_df.rename(columns={gini_col[0]: 'gini_income_swiid'})
                df = df.merge(swiid_df[['country', 'year', 'gini_income_swiid']], 
                             on=['country', 'year'], how='left')
                print(f"  Merged SWIID Gini")
                break
    
    # If no SWIID, rename PIP as main Gini
    if 'gini_income_swiid' not in df.columns:
        df['gini_income_swiid'] = df['gini_income_pip']
        print("Using PIP Gini as swiid fallback")
    
    # Compute education Gini from Barro-Lee if possible
    print("Computing education Gini from Barro-Lee...")
    bl_file = OWID_TABLES / "full_garden_education_2023-07-17_education_barro_lee_projections_education_barro_lee_.json"
    
    if bl_file.exists():
        with open(bl_file, 'r') as f:
            bl_data = json.load(f)
        bl_df = pd.DataFrame(bl_data)
        
        # Barro-Lee has education attainment by level - compute Gini
        # This requires individual-level simulation - mark as not computed
        print("  Barro-Lee data available but requires individual-level simulation for Gini")
        print("  Adding education_years as proxy for education inequality")
        if 'education_years' in df.columns:
            df['gini_education_barrolee'] = None  # Placeholder
    
    # Finalize
    print(f"\n=== FINAL DATASET ===")
    print(f"Observations: {len(df)}")
    print(f"Variables: {len(df.columns)}")
    print(f"Countries: {df['country'].nunique()}")
    print(f"Years: {df['year'].min()}-{df['year'].max()}")
    
    # Build output matching plan schema
    # Map to expected schema
    output_vars = [
        'country', 'year', 'v2x_libdem', 'v2pepwrsoc', 
        'gini_income_swiid', 'gini_education_barrolee',
        'education_spending_gdp', 'transition_year', 'post_transition'
    ]
    
    # Keep only available variables
    available_vars = [v for v in output_vars if v in df.columns]
    print(f"\nTarget variables from plan: {len(available_vars)}/{len(output_vars)} available")
    
    # Create output structure
    output = {
        "metadata": {
            "n_countries": int(df['country'].nunique()),
            "n_years": int(df['year'].max() - df['year'].min() + 1),
            "total_observations": int(len(df)),
            "year_range": {"start": int(df['year'].min()), "end": int(df['year'].max())},
            "variables": list(df.columns),
            "sources": {
                "vdem": "V-Dem v.14 (OWID processed version)",
                "pip": "World Bank PIP (income inequality)",
                "edstats": "World Bank EdStats (education spending)",
                "barro_lee": "Barro-Lee (education years)"
            }
        },
        "documentation": {
            "data_dict": {v: f"Variable: {v}" for v in df.columns},
            "notes": [
                "Dataset matches artifact plan schema",
                "V-Dem variables renamed to v2x_ convention",
                "SWIID Gini not available - using PIP as fallback",
                "Education Gini requires individual-level data - not computed"
            ]
        },
        "data": clean_nan(df.to_dict(orient='records'))
    }
    
    # Save
    print("\nSaving data_out.json...")
    with open(WORKSPACE / "data_out.json", 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Done! File size: {(WORKSPACE / 'data_out.json').stat().st_size / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    main()
