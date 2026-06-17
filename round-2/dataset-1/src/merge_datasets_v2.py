#!/usr/bin/env python3
"""
Dataset merger for Post-1990 Democratizers Inequality Panel.

Merges OWID datasets:
1. V-Dem v.14 (democracy indices)
2. World Bank PIP (income inequality Gini)
3. LIED (democratic transitions)
4. OECD SOCX (social expenditure)
5. Barro-Lee (education years)
6. World Bank EdStats (education expenditure)
"""

from loguru import logger
from pathlib import Path
import json
import sys
import pandas as pd
import numpy as np

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

# Paths to downloaded OWID datasets
OWID_TABLES_DIR = Path("/home/adrian/projects/ai-inventor/.claude/skills/aii-owid-datasets/temp/tables")
OUTPUT_DIR = Path("/home/adrian/projects/ai-inventor/aii_data/users/admin/runs/run_-w6fuC_zXl2B/3_invention_loop/iter_2/gen_art/gen_art_dataset_1")

@logger.catch(reraise=True)
def load_owid_dataset(table_name: str) -> pd.DataFrame:
    """Load full OWID dataset from saved JSON."""
    file_path = OWID_TABLES_DIR / f"full_{table_name}.json"
    logger.info(f"Loading {file_path}")
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Handle both list and dict formats
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict) and 'data' in data:
        df = pd.DataFrame(data['data'])
    else:
        raise ValueError(f"Unexpected JSON structure in {file_path}")
    
    logger.info(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    return df

@logger.catch(reraise=True)
def identify_post1990_democratizers(vdem_df: pd.DataFrame) -> list:
    """
    Identify post-1990 democratizers using V-Dem data.
    """
    logger.info("Identifying post-1990 democratizers...")
    
    # Filter V-Dem for best estimates only
    vdem_best = vdem_df[vdem_df['estimate'] == 'best'].copy()
    
    # Get liberal democracy index
    if 'libdem_vdem' in vdem_best.columns:
        vdem_best = vdem_best[['country', 'year', 'libdem_vdem']].copy()
    else:
        logger.warning("libdem_vdem not found in V-Dem data")
        return []
    
    # Filter for 1990+ and identify transitions
    vdem_best = vdem_best[vdem_best['year'] >= 1990].copy()
    
    democratizers = []
    for country in vdem_best['country'].unique():
        country_data = vdem_best[vdem_best['country'] == country].sort_values('year')
        
        # Check for transition from <0.5 to >=0.5
        transition_year = None
        for i in range(1, len(country_data)):
            prev_val = country_data.iloc[i-1]['libdem_vdem']
            curr_val = country_data.iloc[i]['libdem_vdem']
            
            if pd.notna(prev_val) and pd.notna(curr_val):
                if prev_val < 0.5 and curr_val >= 0.5:
                    transition_year = country_data.iloc[i]['year']
                    break
        
        if transition_year and 1990 <= transition_year <= 1995:
            democratizers.append({
                'country': country,
                'transition_year': int(transition_year)
            })
    
    # Remove invalid entries (continents, regions)
    invalid_countries = ['North America', 'South America', 'Europe', 'Asia', 'Africa', 'Oceania']
    democratizers = [d for d in democratizers if d['country'] not in invalid_countries]
    
    logger.info(f"Found {len(democratizers)} post-1990 democratizers: {[d['country'] for d in democratizers]}")
    return democratizers

@logger.catch(reraise=True)
def merge_datasets(vdem_df: pd.DataFrame, pip_df: pd.DataFrame, 
                  lied_df: pd.DataFrame, socx_df: pd.DataFrame,
                  barro_lee_df: pd.DataFrame, edstats_df: pd.DataFrame,
                  democratizers: list) -> pd.DataFrame:
    """Merge all datasets for the identified democratizer countries."""
    logger.info("Merging datasets...")
    
    # Get list of democratizer countries
    dem_countries = [d['country'] for d in democratizers]
    
    # Filter V-Dem for democratizers and best estimates
    vdem_best = vdem_df[(vdem_df['estimate'] == 'best') & 
                        (vdem_df['country'].isin(dem_countries))].copy()
    vdem_best = vdem_best[vdem_best['year'] >= 1990].copy()
    
    # Select relevant V-Dem columns
    vdem_cols = ['country', 'year']
    for col in ['libdem_vdem', 'delibdem_vdem', 'electdem_vdem', 'participdem_vdem',
                'civ_libs_vdem', 'corr_exec_vdem', 'v2x_libdem', 'v2pepwrsoc']:
        if col in vdem_best.columns:
            vdem_cols.append(col)
    
    vdem_subset = vdem_best[vdem_cols].copy()
    
    # Filter PIP for democratizers
    pip_subset = pip_df[pip_df['country'].isin(dem_countries)].copy()
    pip_subset = pip_subset[pip_subset['year'] >= 1990].copy()
    
    # Consolidate Gini coefficients from PIP
    gini_cols = [col for col in pip_subset.columns if 'spell' in col.lower()]
    
    def get_gini(row):
        for col in gini_cols:
            if pd.notna(row[col]):
                return row[col]
        return None
    
    pip_subset['gini_income'] = pip_subset.apply(get_gini, axis=1)
    pip_subset = pip_subset[['country', 'year', 'gini_income']].copy()
    
    # Filter LIED for democratizers
    lied_subset = lied_df[lied_df['country'].isin(dem_countries)].copy()
    lied_subset = lied_subset[lied_subset['year'] >= 1990].copy()
    
    # Select relevant LIED columns
    lied_cols = ['country', 'year', 'regime_lied', 'democratic_transition', 
                 'democracy_lied', 'is_full_democracy']
    lied_cols = [col for col in lied_cols if col in lied_subset.columns]
    lied_subset = lied_subset[lied_cols].copy()
    
    # Filter SOCX for democratizers
    socx_subset = socx_df[socx_df['country'].isin(dem_countries)].copy()
    socx_subset = socx_subset[socx_subset['year'] >= 1990].copy()
    
    # Get public social expenditure as %GDP
    if 'share_gdp' in socx_subset.columns:
        socx_subset = socx_subset[['country', 'year', 'share_gdp']].copy()
        socx_subset = socx_subset.rename(columns={'share_gdp': 'social_spending_gdp'})
    else:
        logger.warning("share_gdp not found in SOCX data")
        socx_subset = socx_subset[['country', 'year']].copy()
        socx_subset['social_spending_gdp'] = None
    
    # Filter Barro-Lee for democratizers (education years)
    barro_subset = barro_lee_df[barro_lee_df['country'].isin(dem_countries)].copy()
    barro_subset = barro_subset[barro_subset['year'] >= 1990].copy()
    
    # Get average years of education
    if 'mf_youth_and_adults__15_64_years__average_years_of_education' in barro_subset.columns:
        barro_subset = barro_subset[['country', 'year', 'mf_youth_and_adults__15_64_years__average_years_of_education']].copy()
        barro_subset = barro_subset.rename(columns={'mf_youth_and_adults__15_64_years__average_years_of_education': 'education_years'})
    else:
        logger.warning("Education years not found in Barro-Lee data")
        barro_subset = barro_subset[['country', 'year']].copy()
        barro_subset['education_years'] = None
    
    # Filter EdStats for democratizers (education expenditure)
    edstats_subset = edstats_df[edstats_df['country'].isin(dem_countries)].copy()
    edstats_subset = edstats_subset[edstats_subset['year'] >= 1990].copy()
    
    # Get government expenditure on education as %GDP
    if 'government_expenditure_on_education__total__pct_of_gdp' in edstats_subset.columns:
        edstats_subset = edstats_subset[['country', 'year', 'government_expenditure_on_education__total__pct_of_gdp']].copy()
        edstats_subset = edstats_subset.rename(columns={'government_expenditure_on_education__total__pct_of_gdp': 'education_spending_gdp'})
    else:
        logger.warning("Education expenditure not found in EdStats data")
        edstats_subset = edstats_subset[['country', 'year']].copy()
        edstats_subset['education_spending_gdp'] = None
    
    # Merge all datasets
    logger.info("Performing outer joins on country-year...")
    merged = vdem_subset
    
    for df, suffix in [(pip_subset, '_pip'), (lied_subset, '_lied'), 
                       (socx_subset, '_socx'), (barro_subset, '_barro'),
                       (edstats_subset, '_edstats')]:
        if not df.empty:
            merged = pd.merge(merged, df, on=['country', 'year'], how='outer', suffixes=('', suffix))
    
    # Add transition year info
    transition_map = {d['country']: d['transition_year'] for d in democratizers}
    merged['transition_year'] = merged['country'].map(transition_map)
    merged['post_transition'] = merged['year'] >= merged['transition_year']
    
    logger.info(f"Merged dataset: {len(merged)} rows, {len(merged.columns)} columns")
    return merged

@logger.catch(reraise=True)
def create_output_json(merged_df: pd.DataFrame, democratizers: list) -> dict:
    """Create standardized JSON output with metadata."""
    logger.info("Creating output JSON...")
    
    # Convert to records
    data_records = merged_df.to_dict('records')
    
    # Clean up NaN values for JSON serialization
    for record in data_records:
        for key, value in record.items():
            if pd.isna(value):
                record[key] = None
            elif isinstance(value, (np.integer, np.floating)):
                record[key] = float(value)
    
    # Create metadata
    metadata = {
        "n_countries": len(merged_df['country'].unique()),
        "n_years": len(merged_df['year'].unique()),
        "total_observations": len(merged_df),
        "variables": list(merged_df.columns),
        "sources": {
            "vdem": "V-Dem v.14 Country-Year Dataset",
            "pip": "World Bank Poverty and Inequality Platform (PIP)",
            "lied": "Lexical Index of Electoral Democracy (LIED)",
            "socx": "OECD Social Expenditure Database (SOCX)",
            "barro_lee": "Barro-Lee Education Dataset",
            "edstats": "World Bank Education Statistics (EdStats)"
        },
        "democratizers": democratizers,
        "year_range": {
            "start": int(merged_df['year'].min()) if not merged_df.empty else None,
            "end": int(merged_df['year'].max()) if not merged_df.empty else None
        }
    }
    
    # Create data dictionary
    data_dict = {
        "country": "Country name",
        "year": "Year of observation",
        "libdem_vdem": "V-Dem Liberal Democracy Index (0-1)",
        "gini_income": "Income inequality Gini coefficient (0-1)",
        "social_spending_gdp": "Public social expenditure as % of GDP",
        "education_years": "Average years of schooling (Barro-Lee)",
        "education_spending_gdp": "Government expenditure on education as % of GDP",
        "democratic_transition": "Binary flag for democratic transition year (LIED)",
        "transition_year": "Year of democratic transition",
        "post_transition": "Binary flag for post-transition period"
    }
    
    # Create documentation
    documentation = {
        "data_dict": data_dict,
        "missing_data": {
            col: int(merged_df[col].isnull().sum())
            for col in merged_df.columns
        },
        "computation_notes": (
            "Gini coefficients from World Bank PIP. Democracy indices from V-Dem v.14. "
            "Social expenditure from OECD SOCX. Democratic transitions identified using "
            "LIED and V-Dem liberal democracy index threshold (0.5). "
            "Education data from Barro-Lee and World Bank EdStats."
        )
    }
    
    output = {
        "metadata": metadata,
        "data": data_records,
        "documentation": documentation
    }
    
    return output

@logger.catch(reraise=True)
def main():
    logger.info("Starting dataset merger for post-1990 democratizers...")
    
    # Load datasets
    vdem_df = load_owid_dataset("garden_democracy_2024-03-07_vdem_vdem_multi_with_regions")
    pip_df = load_owid_dataset("garden_wb_2025-08-07_world_bank_pip_legacy_income_consumption_2021_gini")
    lied_df = load_owid_dataset("garden_democracy_2025-05-29_lexical_index_lexical_index")
    socx_df = load_owid_dataset("garden_oecd_2025-02-25_social_expenditure_social_expenditure")
    barro_lee_df = load_owid_dataset("garden_education_2023-07-17_education_barro_lee_projections_education_barro_lee_")
    edstats_df = load_owid_dataset("garden_wb_2024-11-04_edstats_edstats")
    
    # Identify post-1990 democratizers
    democratizers = identify_post1990_democratizers(vdem_df)
    
    if not democratizers:
        logger.error("No post-1990 democratizers found! Check V-Dem data.")
        return
    
    # Merge datasets
    merged_df = merge_datasets(vdem_df, pip_df, lied_df, socx_df, 
                               barro_lee_df, edstats_df, democratizers)
    
    if merged_df.empty:
        logger.error("Merged dataset is empty!")
        return
    
    # Create output JSON
    output = create_output_json(merged_df, democratizers)
    
    # Save output
    output_path = OUTPUT_DIR / "data_out.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    logger.info(f"Saved merged dataset to {output_path}")
    logger.info(f"Total observations: {len(merged_df)}")
    logger.info(f"Countries: {len(merged_df['country'].unique())}")
    
    # Create mini version (10%)
    mini_size = max(10, int(len(merged_df) * 0.1))
    mini_df = merged_df.sample(n=mini_size, random_state=42)
    mini_output = create_output_json(mini_df, democratizers)
    mini_path = OUTPUT_DIR / "data_out_mini.json"
    with open(mini_path, 'w') as f:
        json.dump(mini_output, f, indent=2)
    logger.info(f"Saved mini dataset to {mini_path}")
    
    # Print summary statistics
    logger.info("=== Summary Statistics ===")
    logger.info(f"Countries: {list(merged_df['country'].unique())}")
    if not merged_df.empty and 'year' in merged_df.columns:
        logger.info(f"Years: {merged_df['year'].min()} - {merged_df['year'].max()}")
    if not merged_df.empty and 'gini_income' in merged_df.columns:
        logger.info(f"Gini income (mean): {merged_df['gini_income'].mean():.3f}")
    if not merged_df.empty and 'libdem_vdem' in merged_df.columns:
        logger.info(f"Libdem V-Dem (mean): {merged_df['libdem_vdem'].mean():.3f}")

if __name__ == "__main__":
    main()
