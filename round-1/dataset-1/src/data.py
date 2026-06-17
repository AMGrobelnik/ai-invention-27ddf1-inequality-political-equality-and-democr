#!/usr/bin/env python3
"""Data preparation script for Dual Stratification Dataset.

This script transforms the panel dataset into the required format with
examples grouped by dataset, each having input/output fields.

Usage:
    uv run data.py  # Generates full_data_out.json, data_out.json, etc.
"""

import json
import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent


def transform_to_examples_format(df: pd.DataFrame) -> list:
    """Transform panel data to examples format.
    
    Each country-year observation becomes an example with:
    - input: JSON string of feature values
    - output: v2x_libdem value (democracy index)
    - metadata fields for country, year, etc.
    """
    examples = []
    
    # Features to include in input
    feature_cols = [
        "gini", "education_spending_gdp", "tertiary_enrollment",
        "v2pepwrsoc", "edu_ineq_index"
    ]
    
    for _, row in df.iterrows():
        # Create input dict (exclude metadata)
        input_dict = {col: row[col] for col in feature_cols if col in row and pd.notna(row[col])}
        
        # Create example
        example = {
            "input": json.dumps(input_dict, default=str),
            "output": str(row["v2x_libdem"]) if pd.notna(row["v2x_libdem"]) else "",
            "metadata_country": row["country"],
            "metadata_year": int(row["year"]),
            "metadata_post_1990_democratizer": bool(row["post_1990_democratizer"]) if "post_1990_democratizer" in row else False,
            "metadata_task_type": "regression",
            "metadata_feature_names": list(input_dict.keys())
        }
        examples.append(example)
    
    return examples


def main():
    """Load, transform, and save the dataset in required format."""
    
    # Load the main dataset
    with open(OUTPUT_DIR / "data_out.json", "r") as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    
    print(f"Dataset loaded: {len(df)} rows, {df['country'].nunique()} countries")
    print(f"Years: {df['year'].min()}-{df['year'].max()}")
    
    # Transform to examples format
    print("\nTransforming to examples format...")
    examples = transform_to_examples_format(df)
    print(f"Created {len(examples)} examples")
    
    # Create the grouped output structure
    output = {
        "datasets": [
            {
                "dataset": "dual_stratification_panel",
                "examples": examples
            }
        ]
    }
    
    # Save full_data_out.json
    with open(OUTPUT_DIR / "full_data_out.json", "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"✓ Saved full_data_out.json")
    
    # Also update data_out.json to use same format
    with open(OUTPUT_DIR / "data_out.json", "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"✓ Updated data_out.json")
    
    # Create mini version (3 examples)
    mini_output = {
        "datasets": [
            {
                "dataset": "dual_stratification_panel",
                "examples": examples[:3]
            }
        ]
    }
    with open(OUTPUT_DIR / "data_out_mini.json", "w") as f:
        json.dump(mini_output, f, indent=2, default=str)
    print(f"✓ Saved data_out_mini.json")
    
    # Create preview version (truncated)
    preview_examples = []
    for ex in examples[:3]:
        preview_ex = {k: (v[:50] if isinstance(v, str) and len(v) > 50 else v) for k, v in ex.items()}
        preview_examples.append(preview_ex)
    
    preview_output = {
        "datasets": [
            {
                "dataset": "dual_stratification_panel",
                "examples": preview_examples
            }
        ]
    }
    with open(OUTPUT_DIR / "data_out_preview.json", "w") as f:
        json.dump(preview_output, f, indent=2, default=str)
    print(f"✓ Saved data_out_preview.json")
    
    print(f"\n✓ All output files generated successfully!")


if __name__ == "__main__":
    main()
