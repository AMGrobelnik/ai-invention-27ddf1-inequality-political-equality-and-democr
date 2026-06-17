# Dual Stratification Dataset: Post-1990 Democratizers Panel (1990-2024)

## Dataset Overview

This dataset combines V-Dem democratic indicators, World Bank income inequality data, and education indicators to test the dual stratification hypothesis in post-1990 democratizers.

## Data Sources

1. **V-Dem (Varieties of Democracy) v.14** - Liberal Democracy Index (v2x_libdem) and Political Equality Index (v2pepwrsoc)
   - Source: Our World in Data - garden/democracy/2024-03-07/vdem/vdem_multi_with_regions
   - URL: https://v-dem.net/

2. **World Bank Gini Coefficient** - Income inequality measured by Gini index (0-100 scale)
   - Source: World Development Indicators (WDI) - indicator SI.POV.GINI
   - URL: https://data.worldbank.org/indicator/SI.POV.GINI

3. **World Bank Education Spending** - Government expenditure on education as % of GDP
   - Source: WDI - indicator SE.XPD.TOTL.GD.ZS
   - URL: https://data.worldbank.org/indicator/SE.XPD.TOTL.GD.ZS

4. **Education Enrollment Rates** - Tertiary enrollment rates (% gross)
   - Source: Our World in Data - garden/education/2023-07-17/education_lee_lee
   - URL: https://ourworldindata.org/education

## Dataset Statistics

**Observations**: 1291
**Countries**: 38
**Years**: 1990 - 2023
**Complete cases**: 1223 (94.7%)

## Variables

| Variable | Description | Source | Range/Values |
|----------|-------------|--------|--------------|
| country | Country name | V-Dem | String |
| year | Year | V-Dem | 1990-2023 |
| v2x_libdem | Liberal Democracy Index | V-Dem | 0-1 (continuous) |
| v2pepwrsoc | Political Equality Index | V-Dem | 0-4 (continuous) |
| gini | Gini coefficient | World Bank | 0-100 (continuous) |
| education_spending_gdp | Education spending (% GDP) | World Bank | % (continuous) |
| tertiary_enrollment | Tertiary enrollment rate (%) | OWID | % (continuous) |
| edu_ineq_index | Education inequality index (proxy) | Computed | Z-score (continuous) |
| post_1990_democratizer | Flag for post-1990 democratizers | Computed | Boolean |

## Data Quality

### Missing Data

| Variable | Missing | % Missing |
|----------|---------|-----------|
| gini | 68 | 5.3% |
| education_spending_gdp | 34 | 2.6% |
| tertiary_enrollment | 0 | 0% |

## Post-1990 Democratizers

The following countries were identified as true post-1990 democratizers (v2x_libdem transitioned from <0.5 to >=0.5 during 1990-1995):

1. Bulgaria
2. Cape Verde
3. Latvia
4. Namibia

**Note**: The dataset includes 38 countries total. The 4 true democratizers can be compared with the full sample using the `post_1990_democratizer` flag.

## Usage

### Loading the Data

```python
import json
import pandas as pd

# Load full dataset
with open('data_out.json', 'r') as f:
    data = json.load(f)
df = pd.DataFrame(data)

# Load complete cases only
with open('data_out_complete.json', 'r') as f:
    complete_data = json.load(f)
df_complete = pd.DataFrame(complete_data)
```

## Files

- `data_out.json` - Full dataset (1291 records)
- `data_out_complete.json` - Complete cases only (1223 records)
- `data_out_mini.json` - 3 sample records (for testing)
- `data_out_preview.json` - 3 truncated records (for logging)
- `dataset_report.json` - Data quality report

## Citation

If using this dataset, please cite:

- V-Dem Project (2024). Varieties of Democracy (V-Dem) Dataset v.14. https://v-dem.net/
- World Bank (2024). World Development Indicators. https://data.worldbank.org/
- Our World in Data (2024). Education dataset. https://ourworldindata.org/education

## Version

Created: 2024-06-17
Version: 1.0
Contact: AI Inventor System
