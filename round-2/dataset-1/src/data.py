#!/usr/bin/env python3
"""
Data standardization script for gen_art_dataset_1.
Transforms data_out.json to expected schema format with datasets/examples structure.
"""

import json
import pandas as pd
from pathlib import Path

WORKSPACE = Path("/home/adrian/projects/ai-inventor/aii_data/users/admin/runs/run_-w6fuC_zXl2B/3_invention_loop/iter_2/gen_art/gen_art_dataset_1")

def main():
    print("Standardizing dataset to expected schema...")
    
    # Load current data
    with open(WORKSPACE / "data_out.json", 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data['data'])
    print(f"Loaded {len(df)} observations")
    
    # Define input features (X) and output/target (y)
    # Input: inequality, education, social spending, transition dummies
    feature_cols = [
        'gini_income_swiid',
        'gini_education_barrolee', 
        'education_spending_gdp',
        'post_transition',
        'transition_year'
    ]
    
    # Output: democratic quality (V-Dem liberal democracy index)
    target_col = 'v2x_libdem'
    
    # Create examples list
    examples = []
    for idx, row in df.iterrows():
        # Skip rows with missing target
        if row[target_col] is None:
            continue
        
        # Build input features dict (only non-null features)
        input_features = {}
        for col in feature_cols:
            if col in row and row[col] is not None:
                input_features[col] = row[col]
        
        # If no features available, skip
        if not input_features:
            continue
        
        example = {
            "input": json.dumps(input_features),
            "output": str(row[target_col]),
            "metadata_fold": idx % 5,  # 5-fold assignment
            "metadata_feature_names": list(input_features.keys()),
            "metadata_task_type": "regression",
            "metadata_row_index": int(idx),
            "metadata_country": row['country'],
            "metadata_year": int(row['year']),
        }
        examples.append(example)
    
    print(f"Created {len(examples)} examples")
    
    # Group by dataset name
    output = {
        "datasets": [
            {
                "dataset": "post1990_democratizers_inequality",
                "examples": examples
            }
        ]
    }
    
    # Save standardized output
    output_file = WORKSPACE / "full_data_out.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Saved to {output_file}")
    print(f"File size: {output_file.stat().st_size / 1024 / 1024:.2f} MB")
    print(f"Examples: {len(examples)}")
    print(f"Features: {len(examples[0]['metadata_feature_names']) if examples else 0}")
    
    # Create mini version (10%)
    import random
    random.seed(42)
    mini_examples = random.sample(examples, int(len(examples) * 0.1))
    mini_output = {
        "datasets": [
            {
                "dataset": "post1990_democratizers_inequality",
                "examples": mini_examples
            }
        ]
    }
    with open(WORKSPACE / "mini_data_out.json", 'w') as f:
        json.dump(mini_output, f, indent=2)
    print(f"Mini version: {len(mini_examples)} examples")
    
    print("\nDone!")

if __name__ == "__main__":
    main()
