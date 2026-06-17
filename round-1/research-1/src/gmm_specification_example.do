/* Stata code example for xtabond2 with interaction terms
   Dual Stratification Hypothesis: Interaction of income and education inequality
   on democratic backsliding (post-1990 democratizers)
*/

version 12.6
clear all
set more off

// Install required packages if not already installed
// ssc install xtabond2, replace
// ssc install abar, replace

// Load data (example - replace with actual OWID panel data)
// use "owid_panel_post1990_democratizers.dta", clear

// Describe the model:
// Dependent variable: democratic_backsliding (0/1 or continuous measure)
// Key independent variables: 
//   - income_ineq (SWIID gini)
//   - educ_ineq (education gini from Barro-Lee)
//   - interaction: income_ineq * educ_ineq
// Control variables: [add based on literature]

// Generate interaction term
gen income_educ_interaction = income_ineq * educ_ineq

// Label variables
label variable democratic_backsliding "Democratic backsliding (V-Dem index)"
label variable income_ineq "Income inequality (SWIID gini)"
label variable educ_ineq "Education inequality (education gini)"
label variable income_educ_interaction "Interaction: income × education inequality"
label variable lag_democratic_backsliding "Lagged democratic backsliding"

// SPECIFICATION 1: Difference GMM
// Treat all RHS variables as endogenous (appropriate if they are potentially endogenous)
xtabond2 democratic_backsliding L.democratic_backsliding income_ineq educ_ineq income_educ_interaction, ///
    gmm(L.democratic_backsliding income_ineq educ_ineq income_educ_interaction, laglimits(2 .)) ///
    iv(, equation(level)) ///
    collapse ///
    small ///
    twostep

// Post-estimation tests for Difference GMM
abar, lags(2) // AR(1) and AR(2) tests
estat serial // Alternative for serial correlation test
estat overid // Hansen J test

// SPECIFICATION 2: System GMM (recommended)
// More efficient, uses additional moment conditions
xtabond2 democratic_backsliding L.democratic_backsliding income_ineq educ_ineq income_educ_interaction, ///
    gmm(L.democratic_backsliding income_ineq educ_ineq income_educ_interaction, laglimits(2 .)) ///
    iv(, equation(level)) ///
    collapse ///
    small ///
    twostep ///
    system

// Post-estimation tests for System GMM
abar, lags(2) // AR(1) and AR(2) tests
estat overid // Hansen J test for validity of overidentifying restrictions

// SPECIFICATION 3: With additional control variables
// [Add control variables based on literature and data availability]
// xtabond2 democratic_backsliding L.democratic_backsliding income_ineq educ_ineq income_educ_interaction ///
//     gdp_per_capita trade_openness resource_rents ethnic_fractionalization, ///
//     gmm(L.democratic_backsliding income_ineq educ_ineq income_educ_interaction gdp_per_capita, laglimits(2 .)) ///
//     iv(trade_openness resource_rents ethnic_fractionalization, equation(level)) ///
//     collapse small twostep system

// Interpretation of tests:
// 1. AR(1) test: Should reject null (p < 0.05) - indicates first-differenced errors are serially correlated
// 2. AR(2) test: Should NOT reject null (p > 0.05) - indicates no second-order serial correlation
// 3. Hansen J test: Should NOT reject null (p > 0.05) - validates instrument validity
// 4. Monitor instrument count: Should be < number of countries (N)

// ROBUSNTESS CHECKS:
// 1. Vary lag limits for GMM instruments
// 2. Try one-step vs. two-step estimation
// 3. Check if interaction term remains significant with different specifications
// 4. Compare difference GMM vs. system GMM results

// Save estimates
estimates store system_gmm_interaction

// Export results to LaTeX or CSV
// esttab system_gmm_interaction using "results_gmm.tex", replace b(%9.3f) se(%9.3f) star(* 0.10 ** 0.05 *** 0.01)

/*
KEY SPECIFICATION NOTES:

1. INTERACTION TERM TREATMENT:
   - If component variables (income_ineq, educ_ineq) are endogenous, 
     the interaction term should also be treated as endogenous
   - Use GMM-style instruments for all endogenous variables including interaction

2. INSTRUMENT LAG LIMITS:
   - laglimits(2 .) means use lags 2 and higher as instruments
   - This avoids using too recent lags which may be correlated with errors
   - Adjust based on T (time periods) - need sufficient time series length

3. COLLAPSE OPTION:
   - Limits instrument proliferation by collapsing GMM instruments
   - Critical when N is small relative to T

4. SYSTEM VS. DIFFERENCE GMM:
   - System GMM is more efficient (uses level equation with additional assumptions)
   - Difference GMM is more robust (weaker assumptions)
   - Recommend starting with difference GMM, then try system GMM

5. TIME-VARYING VS. TIME-INVARIANT VARIABLES:
   - Time-invariant variables (e.g., colonial heritage) cannot be included in difference GMM
   - Use system GMM to include time-invariant variables in level equation
   - Or use group mean differencing for time-invariant variables

6. MISSING DATA:
   - GMM handles unbalanced panels but gaps reduce effective sample
   - Consider interpolation for key variables if gaps are small
*/

// Example of handling time-invariant variable in interaction:
// If one component of interaction is time-invariant (e.g., legal_origin),
// cannot include directly in difference GMM
// Options:
//   a) Use system GMM (includes level equation)
//   b) Use group mean differencing to create time-varying proxy
//   c) Include as country-specific effect in Bayesian framework

