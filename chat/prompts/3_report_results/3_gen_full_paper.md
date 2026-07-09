# gen_full_paper — report_results

> Phase: `gen_paper_repo` · `gen_full_paper`
> Run: `run_-w6fuC_zXl2B` — Inequality Resilience
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_full_paper` (sdk_openhands_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 06:05:32 UTC

````
<workspace>
Your workspace: `/home/adrian/projects/ai-inventor/aii_data/users/admin/runs/run_-w6fuC_zXl2B/4_gen_paper_repo/_4_assemble_paper/paper/workspace`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/home/adrian/projects/ai-inventor/aii_data/users/admin/runs/run_-w6fuC_zXl2B/4_gen_paper_repo/_4_assemble_paper/paper/workspace/`:
GOOD: `/home/adrian/projects/ai-inventor/aii_data/users/admin/runs/run_-w6fuC_zXl2B/4_gen_paper_repo/_4_assemble_paper/paper/workspace/file.py`, `/home/adrian/projects/ai-inventor/aii_data/users/admin/runs/run_-w6fuC_zXl2B/4_gen_paper_repo/_4_assemble_paper/paper/workspace/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>

<task>
Create a publication-ready top-conference LaTeX paper with BibTeX from <paper_text> and <available_figures>, compile to PDF.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<paper_text>
title: >-
  Inequality, Political Equality, and Democratic Resilience: Evidence from Post-1990 Democratizers
abstract: >-
  Does inequality undermine democratic quality? Recent work establishes income inequality as a predictor of democratic backsliding,
  but the mechanisms remain unclear. This paper investigates whether education inequality amplifies the effect of income inequality
  on democratic erosion, and whether political equality mediates this relationship. Using a panel dataset of 1,187 country-year
  observations across 36 countries (1990-2023), including 11 post-1990 democratizers, I estimate panel models with entity
  and time fixed effects. Three findings emerge. First, the hypothesized interaction between income and education inequality
  is not statistically significant (coefficient = -0.00005, p = 0.837), failing to confirm the 'dual stratification' hypothesis.
  Second, within-country variation reveals that both income inequality (coefficient = -0.0014, p = 0.025) and education inequality
  (coefficient = -0.0192, p < 0.001) are negatively associated with democratic quality when countries serve as their own controls.
  Third, political equality (V-Dem v2pepwrsoc) strongly mediates the relationship between inequality and democratic quality
  (Sobel p < 0.001). The paper concludes that inequality undermines democracy by reducing political equality, but the specific
  interaction between income and education inequality lacks empirical support in this sample.
paper_text: |
  # Inequality, Political Equality, and Democratic Resilience: Evidence from Post-1990 Democratizers

  ## Abstract

  Does inequality undermine democratic quality? Recent work establishes income inequality as a predictor of democratic backsliding, but the mechanisms remain unclear. This paper investigates whether education inequality amplifies the effect of income inequality on democratic erosion, and whether political equality mediates this relationship. Using a panel dataset of 1,187 country-year observations across 36 countries (1990-2023), including 11 post-1990 democratizers, I estimate panel models with entity and time fixed effects. Three findings emerge. First, the hypothesized interaction between income and education inequality is not statistically significant, failing to confirm the "dual stratification" hypothesis. Second, within-country variation reveals that both income inequality (coefficient = -0.0014, p = 0.025) and education inequality (coefficient = -0.0192, p < 0.001) are negatively associated with democratic quality when countries serve as their own controls. Third, political equality (V-Dem v2pepwrsoc) strongly mediates the relationship between inequality and democratic quality (Sobel p < 0.001). The paper concludes that inequality undermines democracy by reducing political equality, but the specific interaction between income and education inequality lacks empirical support in this sample.

  **Keywords:** democratic backsliding, inequality, political equality, V-Dem, panel data, mediation analysis

  ## Introduction

  The relationship between economic inequality and democratic stability has re-emerged as a central concern in comparative political economy. Recent work by Haggard et al. [1] demonstrates that income inequality predicts democratic erosion in the twenty-first century, contributing to a growing literature on "democratic backsliding" [2]. However, two questions remain insufficiently answered: (1) Does education inequality independently affect democratic quality, and (2) Does political equality mediate the relationship between inequality and democratic backsliding?

  This paper investigates these questions using panel data from 36 countries between 1990 and 2023. The analysis yields three findings. First, contrary to the "dual stratification" hypothesis advanced in earlier work, the interaction between income inequality and education inequality is not statistically significant. The hypothesis that these inequalities jointly create a self-reinforcing elite capture equilibrium is not supported by the data. Second, within-country analysis reveals that both income and education inequality are negatively associated with democratic quality when exploiting within-country variation—a more credible source of identification than cross-country correlations. Third, political equality (measured by V-Dem's Political Equality Index) strongly mediates the relationship between inequality and democratic quality.

  [FIGURE:fig1]

  ### Research Question and Contributions

  This paper makes three contributions to comparative political economy:

  1. **Theoretical**: I clarify the mechanisms linking inequality to democratic erosion. Drawing on Acemoglu and Robinson's distinction between de facto and de jure power [3, 4], I argue that inequality reduces political equality, which in turn undermines democratic quality. The analysis provides the first systematic test of this mediation mechanism using V-Dem's Political Equality Index [5].

  2. **Empirical**: Using within-country variation (country fixed effects), I show that increases in inequality within countries are associated with declines in democratic quality. This within-country evidence is more credible for causal inference than cross-country correlations, which may be driven by time-invariant confounders such as colonial heritage or resource curses.

  3. **Null Result**: I report a null result on the interaction between income and education inequality. While the "dual stratification" hypothesis is theoretically plausible, it lacks empirical support in this sample. Honest reporting of null results is essential for cumulative knowledge production in comparative political economy.

  ### Roadmap

  The paper proceeds as follows. Section 2 reviews the theoretical framework and related literature. Section 3 describes the data and measurement strategy, with particular attention to reconciling discrepancies between the paper and the underlying data. Section 4 presents the empirical framework. Section 5 discusses the results, including the null interaction finding and the significant mediation effect. Section 6 concludes with implications for comparative political economy and democratic resilience.

  ## Theoretical Framework

  ### De Facto vs. De Jure Power

  Acemoglu and Robinson [3] distinguish between *de jure* political power (the power allocated by political institutions) and *de facto* political power (the power that arises from wealth, organization, education, or social networks). Democratic transitions often change de jure power without correspondingly changing de facto power. The result is a persistent gap between formal democratic institutions and actual political influence.

  The core theoretical claim of this paper is that inequality reduces de facto political power among disadvantaged groups, which in turn undermines democratic quality. This claim builds on three mechanisms:

  1. **Information and Participation Costs**: Education reduces the costs of political participation (time, effort, cognitive load). When education is unequally distributed, political participation becomes stratified by education level [6].

  2. **Coordination Capacity**: Education enhances the ability to coordinate collective action. Educated elites can more effectively organize to protect their interests, while the less educated face higher coordination costs [7].

  3. **Agenda-Setting Power**: Education increases preference sophistication, enabling educated groups to shape policy agendas. This agenda-setting power persists even under formal democracy [8].

  ### The Political Equality Mechanism

  The mechanism linking inequality to democratic backsliding operates through political equality—the extent to which political power is evenly distributed across socioeconomic groups. V-Dem's Political Equality Index (v2pepwrsoc) measures this concept directly, asking: "Is political power distributed according to social groups?" [5].

  The causal chain is:
  1. High inequality (income or education) → unequal de facto political power
  2. Unequal de facto power → low political equality (v2pepwrsoc)
  3. Low political equality → democratic backsliding (declining v2x_libdem)

  This paper tests whether political equality mediates the relationship between inequality and democratic backsliding.

  ### The Dual Stratification Hypothesis: A Null Result

  The "dual stratification" hypothesis advanced in earlier work proposes that income inequality and education inequality interact to create a self-reinforcing equilibrium of elite capture [9]. The logic is that income inequality enables elites to purchase education for their children, while education inequality enables elites to monopolize politically relevant skills. The interaction of both inequalities supposedly creates a "dual stratification" regime that resists democratic deepening.

  This paper reports a null result on this interaction hypothesis. The interaction term between income inequality and education inequality is not statistically significant in panel models with entity and time fixed effects (p = 0.837). While the theoretical logic of dual stratification is plausible, it lacks empirical support in this sample of 36 countries (1990-2023).

  ## Data and Measurement

  ### Data Sources and Sample

  The analysis uses a panel dataset covering 1990-2023, constructed from three primary sources:

  1. **V-Dem v.14 (2024)**: Provides Liberal Democracy Index (v2x_libdem) and Political Equality Index (v2pepwrsoc) [5].
  2. **World Bank World Development Indicators (WDI)**: Provides Gini coefficient (SI.POV.GINI) and education spending as % of GDP (SE.XPD.TOTL.GD.ZS).
  3. **Our World in Data (OWID)**: Provides tertiary enrollment rates as a proxy for education inequality.

  **Sample Size and Composition**: The initial merged dataset contains 1,291 country-year observations across 38 countries. After listwise deletion of missing values, the analytic sample includes 1,187 observations from 36 countries. The two dropped countries (due to excessive missing data) are not identified in the current analysis but likely include small countries with limited World Bank coverage.

  **Post-1990 Democratizers**: The sample includes 11 post-1990 democratizers: Benin, Bulgaria, Cape Verde, Estonia, Latvia, Mongolia, Namibia, Panama, Sao Tome and Principe, South Africa, and Suriname. This expanded sample addresses a key limitation of earlier work that included only 3-4 post-1990 democratizers.

  [FIGURE:fig2]

  ### Variable Construction

  **Dependent Variable**: V-Dem Liberal Democracy Index (v2x_libdem), ranging from 0 to 1, with higher values indicating higher democratic quality.

  **Key Independent Variables**:
  - Gini coefficient (0-100 scale), measuring income inequality
  - Education inequality index, constructed as the negative z-score of tertiary enrollment rates (higher values = more inequality). *Note: The Barro-Lee education Gini coefficient is the preferred measure [10], but is not available in the current OWID panels. Tertiary enrollment z-scores are used as a proxy, with the limitation that tertiary enrollment measures access not distribution.*
  - Interaction term: Gini × education inequality index

  **Mediating Variable**: V-Dem Political Equality Index (v2pepwrsoc), ranging from 0 (monopolized by one group) to 4 (equal power) [5].

  **Moderating Variable**: Government expenditure on education as % of GDP.

  **Control Variables**: Lagged dependent variable (v2x_libdem\_lag) to account for persistence in democratic quality.

  ### Missing Data

  The initial merged dataset (1,291 observations) has the following missing data rates:
  - Gini coefficient: 68 missing values (5.3% of 1,291)
  - Education spending: 34 missing values (2.6% of 1,291)
  - Tertiary enrollment: approximately 45% missing (limited country coverage in OWID)

  After listwise deletion, the analytic sample includes 1,187 observations (94.7% of 1,291). The high missing data rate for tertiary enrollment (used to construct the education inequality proxy) is a limitation. Readers should interpret results involving the education inequality index with caution.

  ### Descriptive Statistics

  Table 1 reports descriptive statistics for the full sample and by subgroup.

  **Table 1: Descriptive Statistics**

  | Variable | Full Sample | Post-1990 Democratizers | Other Countries |
  |----------|-------------|-------------------------|----------------|
  | v2x_libdem | 0.716 (0.142) | 0.622 (0.088) | 0.727 (0.143) |
  | v2pepwrsoc | 0.682 (0.149) | 0.555 (0.104) | 0.697 (0.146) |
  | Gini coefficient | 36.2 (9.87) | 44.1 (15.37) | 35.5 (8.88) |
  | Education spending (% GDP) | 5.26 (1.62) | 5.45 (1.91) | 5.24 (1.59) |
  | Tertiary enrollment (%) | 54.5 (27.71) | 38.0 (29.33) | 56.5 (26.86) |
  | Observations | 1,187 | 102 | 1,085 |

  *Note: Mean values with standard deviations in parentheses. Post-1990 democratizers include 11 countries (see text).*

  The table reveals that post-1990 democratizers have systematically lower democratic quality (0.622 vs. 0.727), lower political equality (0.555 vs. 0.697), and higher income inequality (Gini 44.1 vs. 35.5) compared to established democracies. These descriptive patterns are consistent with the hypothesis that inequality undermines democratic quality, but they do not establish causality.

  ### Correlation Analysis

  Figure 2 shows the correlation matrix for key variables. The Political Equality Index (v2pepwrsoc) is strongly correlated with liberal democracy (r = 0.936), confirming that political equality is a core component of democratic quality. Gini coefficient is negatively correlated with both political equality (r = -0.629) and liberal democracy (r = -0.452).

  [FIGURE:fig3]

  **Within-Country Correlations**: To address the reviewer's concern about cross-country correlations being driven by confounders, I compute within-country correlations by demeaning all variables by country (subtracting country means). The within-country correlation between Gini and v2x_libdem is -0.284 (compared to -0.452 in the cross-country analysis), indicating that within-country variation in inequality is also negatively associated with democratic quality, but the effect size is smaller.

  ## Empirical Framework

  ### Identification Strategy

  The panel structure with country fixed effects controls for time-invariant confounders such as colonial heritage, resource endowments, or historical state capacity. However, three identification challenges remain:

  1. **Reverse causality**: Democratic backsliding may cause increased inequality, not vice versa.
  2. **Time-varying confounders**: Economic crises, commodity price shocks, or geopolitical events may affect both inequality and democracy.
  3. **Measurement error**: The education inequality proxy (tertiary enrollment) is imperfect.

  Ideally, I would employ Arellano-Bond System GMM estimation [11] to address the lagged dependent variable bias and potential endogeneity of regressors. However, the System GMM estimator requires valid instruments and passes specification tests (AR(1), AR(2), Hansen J test). In practice, the linearmodels implementation of System GMM proved challenging to implement with the current data structure. As a fallback, I use Panel OLS with entity and time fixed effects, cluster-robust standard errors by country, and include the lagged dependent variable as a control [12].

  ### Specification

  The baseline specification is:

  $$v2x\_libdem_{it} = \alpha + \beta_1 v2x\_libdem_{it-1} + \beta_2 gini_{it} + \beta_3 edu\_ineq_{it} + \beta_4 (gini \times edu\_ineq)_{it} + \gamma X_{it} + \mu_i + \lambda_t + \epsilon_{it}$$

  where:
  - $v2x\_libdem_{it}$ is the liberal democracy index for country $i$ in year $t$
  - $gini_{it}$ is the Gini coefficient
  - $edu\_ineq_{it}$ is the education inequality index
  - $X_{it}$ is a vector of control variables (education spending)
  - $\mu_i$ are country fixed effects
  - $\lambda_t$ are year fixed effects

  Standard errors are clustered by country to account for serial correlation within countries.

  ### Mediation Analysis

  To test whether political equality mediates the relationship between inequality and democratic backsliding, I estimate:

  $$v2pepwrsoc_{it} = \alpha + \beta_1 gini_{it} + \beta_2 edu\_ineq_{it} + \beta_3 (gini \times edu\_ineq)_{it} + \gamma X_{it} + \mu_i + \lambda_t + \epsilon_{it}$$

  $$v2x\_libdem_{it} = \alpha + \beta_1 v2pepwrsoc_{it} + \beta_2 gini_{it} + \beta_3 edu\_ineq_{it} + \beta_4 (gini \times edu\_ineq)_{it} + \gamma X_{it} + \mu_i + \lambda_t + \epsilon_{it}$$

  If political equality mediates the relationship, the interaction term $\beta_4$ should be attenuated when v2pepwrsoc is included. I use the Sobel-Goodman test to assess the significance of the mediation effect [13].

  ## Results and Discussion

  ### Panel OLS Results

  Table 2 presents the Panel OLS estimates with entity and time fixed effects. Standard errors are clustered by country.

  **Table 2: Panel OLS Estimates of Democratic Quality**

  | Variable | Model 1: Main | Model 2: Interaction | Model 4: Triple |
  |----------|--------------|---------------------|----------------|
  | Democratic Quality$_{t-1}$ | 0.8566*** [0.0482] | 0.8559*** [0.0485] | 0.8561*** [0.0484] |
  | Gini Coefficient | -0.0005 [0.0004] | -0.0004 [0.0005] | -0.0004 [0.0006] |
  | Education Inequality Index |  | 0.0069 [0.0090] | 0.0063 [0.0088] |
  | Gini $\times$ Edu Inequality |  | -0.0000 [0.0002] | 0.0000 [0.0002] |
  | Gini $\times$ Edu Ineq $\times$ Edu Spend |  |  | -0.0000 [0.0000] |
  | Education Spending (\% GDP) | 0.0003 [0.0008] | 0.0006 [0.0008] | 0.0009 [0.0008] |
  | Observations | 1,187 | 1,187 | 1,187 |
  | R-squared | 0.800 | 0.801 | 0.801 |

  *Note: Panel OLS with entity and time fixed effects. Standard errors clustered by country in brackets. *** p<0.01, ** p<0.05, * p<0.10. Coefficients for country and year fixed effects not shown.*

  **Finding 1: Null Interaction Effect**. The interaction term (Gini $\times$ Education Inequality) in Model 2 is -0.00005 with a standard error of 0.0002, yielding p = 0.837. This is a null result: the data do not support the hypothesis that education inequality amplifies the effect of income inequality on democratic backsliding. The "dual stratification" hypothesis is not confirmed in this sample.

  **Finding 2: Lagged Dependent Variable**. The coefficient on the lagged dependent variable is approximately 0.856 in all models, indicating high persistence in democratic quality. This finding is consistent with the literature on democratic durability [14].

  **Finding 3: Main Effects Not Significant**. Neither income inequality (Gini) nor education inequality individually reaches statistical significance at conventional levels (p<0.05). This may seem surprising given the significant within-country effects reported below. The discrepancy likely reflects the inclusion of the lagged dependent variable, which absorbs much of the variation in democratic quality.

  ### Within-Country Analysis

  To further investigate the relationship between inequality and democratic quality, I estimate within-country effects by demeaning all variables by country. This approach eliminates between-country variation and estimates the relationship using only within-country variation over time.

  **Finding 4: Within-Country Effects**. When using within-country variation (country fixed effects), both income inequality and education inequality are negatively associated with democratic quality:
  - Gini coefficient (within): coefficient = -0.0014, p = 0.025
  - Education inequality index (within): coefficient = -0.0192, p < 0.001

  These within-country effects are statistically significant and substantively meaningful. A one standard deviation increase in the Gini coefficient within a country (9.87 points) is associated with a 0.014 decrease in v2x_libdem. While small in absolute terms, this effect is meaningful given the 0-1 scale of the democracy index.

  The within-country analysis provides more credible evidence for the inequality-democracy relationship because it eliminates time-invariant confounders. The null interaction effect, however, is robust: the interaction term remains insignificant in the within-country specification (p = 0.642).

  [FIGURE:fig4]

  ### Mediation Analysis

  **Finding 5: Political Equality Mediates**. The mediation analysis yields a highly significant result. Using the Sobel-Goodman test, I find that political equality (v2pepwrsoc) significantly mediates the relationship between the Gini-education inequality interaction and democratic quality (Sobel p < 0.001).

  The mediation paths are:
  - Path a (X → M): Gini × edu_ineq → v2pepwrsoc, coefficient = -0.0021, p < 0.001
  - Path b (M → Y): v2pepwrsoc → v2x_libdem, coefficient = 0.8887, p < 0.001
  - Total effect (X → Y): coefficient = -0.00198, p < 0.001

  The significant mediation effect indicates that political equality is a key mechanism linking inequality to democratic quality. When inequality is high, political equality declines, which in turn reduces democratic quality.

  ### Robustness Checks

  I conduct four robustness checks:

  1. **Alternative inequality measures**: Using SWIID instead of World Bank Gini yields qualitatively similar within-country effects, though the SWIID data are not available for all countries in the sample.

  2. **Alternative democracy measures**: Using Polity V and EIU democracy indices instead of V-Dem produces consistent within-country findings, though the mediation effect through political equality is specific to the V-Dem data.

  3. **Placebo tests**: Estimating the model on pre-1990 data (where the hypothesis should not hold) is not possible because the V-Dem data begin in 1990.

  4. **Alternative education inequality measures**: The Barro-Lee education Gini coefficient [10] is the preferred measure but is not available in the current OWID panels. The tertiary enrollment proxy is imperfect. Future work should use the Barro-Lee measure to validate the findings.

  ### Limitations

  Five limitations of the current analysis should be noted:

  1. **Null Interaction Finding**: The "dual stratification" hypothesis is not confirmed. The interaction between income and education inequality is not statistically significant. This null result may reflect low statistical power, measurement error in the education inequality proxy, or the possibility that the hypothesis is wrong.

  2. **Panel OLS Instead of System GMM**: The analysis uses Panel OLS with entity and time fixed effects, not System GMM as originally planned. The lagged dependent variable may introduce Nickell bias in dynamic panel models [15]. Future work should implement System GMM with valid instruments.

  3. **Education Inequality Measurement**: The proxy based on tertiary enrollment is imperfect. Directly using the Barro-Lee education Gini coefficient [10] would strengthen the analysis.

  4. **Missing Data**: The 45% missing data rate for tertiary enrollment limits the sample size and may introduce selection bias. Countries with missing tertiary enrollment data may differ systematically from countries with complete data.

  5. **Identification**: While within-country analysis eliminates time-invariant confounders, time-varying confounders (economic crises, commodity shocks) may still bias the estimates. Instrumental variable approaches or natural experiments would strengthen identification.

  ## Conclusion

  This paper investigated the relationship between inequality and democratic resilience using panel data from 36 countries (1990-2023). Three findings emerge.

  First, the "dual stratification" hypothesis—the proposition that income inequality and education inequality interact to accelerate democratic backsliding—is not supported by the data. The interaction term is not statistically significant in panel models with entity and time fixed effects. This null result is important: theoretical plausibility does not guarantee empirical support.

  Second, within-country analysis reveals that both income inequality and education inequality are negatively associated with democratic quality when exploiting within-country variation. These within-country effects are more credible for causal inference than cross-country correlations.

  Third, political equality (V-Dem v2pepwrsoc) strongly mediates the relationship between inequality and democratic quality. Inequality reduces political equality, which in turn undermines democratic quality. This mediation finding identifies a key mechanism linking inequality to democratic erosion.

  For comparative political economy, the paper's finding is that inequality undermines democracy by reducing political equality. Policies that reduce inequality—or that protect political equality even in the presence of inequality—may help sustain democratic quality. The null result on the interaction between income and education inequality suggests that these inequalities operate additively, not multiplicatively, in their effects on democratic backsliding.

  Future research should: (1) use improved education inequality measures from the Barro-Lee dataset; (2) employ System GMM or instrumental variable strategies to strengthen identification; (3) investigate whether the inequality-democracy relationship varies across different types of political institutions; and (4) examine the role of specific policies (campaign finance reform, voting rights expansion) in buffering the effect of inequality on political equality.

  ## References

  [1] Haggard, S., Kaufman, R. R., Kurtz, M. J., & Powell, A. R. (2024). Income inequality and the erosion of democracy in the twenty-first century. *Proceedings of the National Academy of Sciences*, 121(52), e2422543121.

  [2] Lührmann, A., & Lindberg, S. I. (2019). A third wave of autocratization is here: What is new about it? *Democratization*, 26(7), 1095-1113.

  [3] Acemoglu, D., & Robinson, J. A. (2008). Persistence of power, elites, and institutions. *American Economic Review*, 98(1), 267-293.

  [4] Acemoglu, D., & Robinson, J. A. (2006). *Economic origins of dictatorship and democracy*. Cambridge University Press.

  [5] Coppedge, M., Gerring, J., Altman, D., et al. (2011). Conceptualizing and measuring democracy: A new approach. *Perspectives on Politics*, 9(2), 247-267.

  [6] Brady, H. E., Verba, S., & Schlozman, K. L. (1995). Beyond SES: A resource model of political participation. *American Political Science Review*, 89(2), 271-294.

  [7] Olson, M. (1965). *The logic of collective action: Public goods and the theory of groups*. Harvard University Press.

  [8] Page, B. I., & Shapiro, R. Y. (1983). Effects of public opinion on policy. *American Political Science Review*, 77(1), 175-190.

  [9] Baliamoune-Lutz, M. (2018). Political elites, democracy and education. *Journal of Developing Areas*, 52(3).

  [10] Thomas, V., Wang, Y., & Fan, X. (2001). Measuring education inequality: Gini coefficients of education. *World Bank Economic Review*, 15(3), 395-415.

  [11] Roodman, D. (2009). How to do xtabond2: An introduction to difference and system GMM in Stata. *Stata Journal*, 9(1), 86-136.

  [12] Cameron, A. C., & Miller, D. L. (2015). A practitioner's guide to cluster-robust inference. *Journal of Human Resources*, 50(2), 317-372.

  [13] Sobel, M. E. (1982). Asymptotic confidence intervals for indirect effects in structural equation models. *Sociological Methodology*, 13, 290-312.

  [14] Przeworski, A. (2019). *Crises of democracy*. Cambridge University Press.

  [15] Nickell, S. (1981). Biases in dynamic models with fixed effects. *Econometrica*, 49(6), 1417-1426.

  ---

  **Data Availability**: The dataset constructed for this analysis is available at the AI Inventor system, with documentation in dataset_documentation.md \footnote{Code: \url{https://github.com/AMGrobelnik/ai-invention-27ddf1-inequality-political-equality-and-democr/tree/main/round-1/dataset-1}}.

  **Acknowledgments**: This research was conducted as part of the AI Inventor system, an automated research system for generating and testing novel hypotheses in comparative political economy.
summary: >-
  This paper investigates the relationship between inequality and democratic resilience using panel data from 36 countries
  (1990-2023). The analysis yields three findings: (1) the interaction between income and education inequality is not statistically
  significant, (2) within-country analysis shows both inequalities negatively affect democratic quality, and (3) political
  equality strongly mediates the inequality-democracy relationship. The paper contributes to comparative political economy
  by identifying political equality as a key mechanism and by honestly reporting a null result on the dual stratification
  hypothesis.
</paper_text>

<available_figures>
--- Item 1 ---
id: fig1
title: 'Conceptual Framework: Inequality, Political Equality, and Democratic Quality'
caption: >-
  Theoretical framework showing the hypothesized relationships. Inequality (income and education) reduces political equality,
  which in turn undermines democratic quality. The dual stratification hypothesis proposes that income and education inequality
  interact synergistically, but this interaction is not supported by the data.
image_gen_detailed_description: >-
  Conceptual diagram with boxes and arrows. Three main boxes: 'Inequality' (left), 'Political Equality' (middle), 'Democratic
  Quality' (right). Inequality box contains 'Income Inequality' and 'Education Inequality'. Arrow from Inequality to Political
  Equality labeled 'Negative effect'. Arrow from Political Equality to Democratic Quality labeled 'Positive effect'. Dashed
  arrow from Income Inequality to Education Inequality labeled 'Interaction (null result)'. Sans-serif font, white background,
  clean layout.
aspect_ratio: '21:9'
summary: >-
  Conceptual framework diagram showing the theoretical relationships between inequality, political equality, and democratic
  quality.
figure_path: figures/fig1_v0.jpg

--- Item 2 ---
id: fig2
title: Post-1990 Democratizers in Sample
caption: >-
  Geographic distribution of the 11 post-1990 democratizers in the expanded sample: Benin, Bulgaria, Cape Verde, Estonia,
  Latvia, Mongolia, Namibia, Panama, Sao Tome and Principe, South Africa, and Suriname.
image_gen_detailed_description: >-
  World map with 11 countries highlighted in red. Countries labeled: Benin (West Africa), Bulgaria (Eastern Europe), Cape
  Verde (Atlantic), Estonia (Northern Europe), Latvia (Northern Europe), Mongolia (East Asia), Namibia (Southern Africa),
  Panama (Central America), Sao Tome and Principe (Central Africa), South Africa (Southern Africa), Suriname (South America).
  Simple map, white background, sans-serif font.
aspect_ratio: '21:9'
summary: >-
  World map showing the geographic distribution of post-1990 democratizers in the sample.
figure_path: figures/fig2_v0.jpg

--- Item 3 ---
id: fig3
title: 'Correlation Matrix: Key Variables'
caption: >-
  Correlation matrix for key variables in the analysis. The Political Equality Index (v2pepwrsoc) is strongly correlated with
  liberal democracy (r = 0.936). Gini coefficient is negatively correlated with both political equality (r = -0.629) and liberal
  democracy (r = -0.452). Within-country correlations (in parentheses) are smaller but still negative.
image_gen_detailed_description: >-
  Heatmap correlation matrix. Rows and columns: 'v2x_libdem', 'v2pepwrsoc', 'Gini', 'Edu_Ineq', 'Edu_Spend'. Values: v2x_libdem
  vs v2pepwrsoc = 0.936, v2x_libdem vs Gini = -0.452 (-0.032 within), v2x_libdem vs Edu_Ineq = -0.521 (-0.071 within), v2pepwrsoc
  vs Gini = -0.629 (-0.033 within), v2pepwrsoc vs Edu_Ineq = -0.487 (-0.057 within), Gini vs Edu_Ineq = 0.214 (0.037 within).
  Color scale: dark blue = positive, dark red = negative. Sans-serif font, white background.
aspect_ratio: '21:9'
summary: >-
  Correlation matrix showing relationships between key variables, with both cross-country and within-country correlations.
figure_path: figures/fig3_v0.jpg

--- Item 4 ---
id: fig4
title: Within-Country Effects of Inequality on Democratic Quality
caption: >-
  Coefficient plot showing within-country effects of income inequality and education inequality on democratic quality (v2x_libdem).
  Both inequalities have negative and statistically significant effects. Estimates from panel models with entity and time
  fixed effects, using within-country variation.
image_gen_detailed_description: >-
  Coefficient plot (dot plot with confidence intervals). Y-axis: 'Income Inequality (Gini)' and 'Education Inequality Index'.
  X-axis: coefficient values from -0.025 to 0.005. Income Inequality coefficient = -0.0014 (95% CI: -0.0026 to -0.0002), Education
  Inequality coefficient = -0.0192 (95% CI: -0.027 to -0.011). Both confidence intervals do not include 0. Points are black
  dots, error bars are gray. Vertical dashed line at x=0. Sans-serif font, white background.
aspect_ratio: '21:9'
summary: >-
  Coefficient plot showing within-country effects of income and education inequality on democratic quality.
figure_path: figures/fig4_v0.jpg
</available_figures>

<figure_requirements>
CRITICAL: Include ALL figures from <available_figures>. No exceptions.

- Every figure MUST use \includegraphics{figures/filename.jpg}
- Do NOT skip, convert to tables, or describe without inserting
- Each needs: \begin{figure*|figure}[placement], \includegraphics, \caption, \label, \end{...} — pick env + placement by the figure's `aspect_ratio` field (see PLACEMENT below). Constrain every \includegraphics with `width=\linewidth,height=0.4\textheight,keepaspectratio` (single-column) or `width=\textwidth,height=0.45\textheight,keepaspectratio` (figure*). Use exactly these option keys — `max height=` is NOT valid LaTeX
- Use the `caption` field from each figure for \caption{...} — do NOT invent new captions
- Place figures where their [FIGURE:fig_id] markers appear in paper_text
- VERIFICATION: paper.tex MUST have exact same number of \includegraphics as <available_figures>
- Do NOT generate new figure images (no matplotlib, no PIL, no image generation). Use ONLY the pre-generated figures from <available_figures>. They were already created by a previous pipeline step.

PLACEMENT BY ASPECT RATIO (use the `aspect_ratio` field on each figure):
- `21:9` (architecture diagrams / hero figures): \begin{figure*}[!t] (full two-column width, top of page). The hero architecture diagram should appear EARLY in the paper — typically at the top of page 2. Marker placement in paper_text already determines this; preserve it.
- `16:9` (comparisons, multi-panel results): \begin{figure*}[!t] for full-width or \begin{figure}[!htbp] for single-column.
- `4:3` / `1:1` / `3:2` / `3:4` / `9:16`: \begin{figure}[!htbp] (single-column).
</figure_requirements>

<artifact_links>
The paper_text contains \footnote{Code: \url{...}} references linking to artifact source code
on GitHub. Include \usepackage{hyperref} and \usepackage{url}.
Preserve these exactly as-is — do not remove, rewrite, or convert them to plain text.
The URLs will not resolve yet (the repo is deployed after compilation) — do NOT try to verify or fix them.
</artifact_links>

<headings>
NEVER use inline math (``$...$``) inside ``\section{...}`` / ``\subsection{...}`` / ``\subsubsection{...}`` arguments — hyperref's bookmark builder errors out (``Token not allowed in a PDF string``) and the PDF outline breaks. If a section heading needs a math-looking term, use the text equivalent (``d star`` not ``$d^*$``, ``alpha-equivalent`` not ``$\alpha$-equivalent``) or wrap it in ``\texorpdfstring{$math$}{plain}``. Inline math inside body paragraphs is fine.
</headings>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-paper-to-latex, aii-semscholar-bib.
TODO 2. Review <paper_text> and <available_figures>. Copy all figure images into ./figures/ in your workspace. Count figures — MUST include every one. Plan placements per section. Build `./references.bib` via aii_semscholar_bib__fetch — collect DOIs/ArXiv IDs from <paper_text> and batch-fetch all BibTeX in one call. Do NOT fabricate entries.
TODO 3. Create `./paper.tex` per aii-paper-to-latex skill's setup, write ALL sections, insert ALL figures from <available_figures>, include `./references.bib` via \bibliography. Compile to PDF per skill's process. Fix errors.
TODO 4. CRITICAL VERIFICATION: Run `grep -c 'includegraphics' paper.tex`, confirm count equals figures in <available_figures>. If not, add missing figures. Verify `./paper.pdf` was created.
TODO 5. VISUAL REVIEW: Write Python script to convert EVERY page of paper.pdf to PNG at 150 DPI (use pdf2image or pymupdf). Then read ALL page screenshots — each page image costs ~1,600 tokens so a 15-page paper is only ~24K tokens. You MUST read every page. The ONLY exception is if all page images would not fit in your remaining context — in that case, read as many as fit and state which pages you are skipping and why. Check every page for layout issues, overlapping figures, cut-off text, bad spacing, formatting problems. Fix issues and recompile.
TODO 6. FINAL READ: Check page count (`pdfinfo paper.pdf` or pymupdf). Read entire paper.pdf — check for missing sections, unclear explanations, inconsistencies, typos. Fix and recompile. The ONLY exception is if all pages would not fit in your remaining context — in that case, read as many pages as fit and state which pages you are skipping and why.
</todos>

---

Output the result as JSON to: `/home/adrian/projects/ai-inventor/aii_data/users/admin/runs/run_-w6fuC_zXl2B/4_gen_paper_repo/_4_assemble_paper/paper/workspace/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "FullPaperExpectedFiles": {
      "description": "All expected output files from full paper generation.",
      "properties": {
        "paper_tex_path": {
          "description": "Path to LaTeX source file. Example: 'paper.tex'",
          "title": "Paper Tex Path",
          "type": "string"
        },
        "paper_pdf_path": {
          "description": "Path to compiled PDF. Example: 'paper.pdf'",
          "title": "Paper Pdf Path",
          "type": "string"
        },
        "references_bib_path": {
          "description": "Path to BibTeX bibliography file. Example: 'references.bib'",
          "title": "References Bib Path",
          "type": "string"
        },
        "figure_paths": {
          "description": "Paths to all figure image files. Example: ['figures/fig1_v0.jpg', 'figures/fig2_v0.jpg']",
          "items": {
            "type": "string"
          },
          "title": "Figure Paths",
          "type": "array"
        }
      },
      "required": [
        "paper_tex_path",
        "paper_pdf_path",
        "references_bib_path",
        "figure_paths"
      ],
      "title": "FullPaperExpectedFiles",
      "type": "object"
    }
  },
  "description": "Full paper \u2014 structured output from paper generation.",
  "properties": {
    "title": {
      "description": "Short descriptive title for this paper generation task (roughly 30-90 characters)",
      "maxLength": 90,
      "minLength": 30,
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "description": "Brief summary of the generated paper: sections written, figures included, compilation status",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/FullPaperExpectedFiles",
      "description": "All output files you created. Must include paper.tex, paper.pdf, references.bib, and paths to all figure files."
    }
  },
  "required": [
    "title",
    "summary",
    "out_expected_files"
  ],
  "title": "FullPaper",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `/home/adrian/projects/ai-inventor/aii_data/users/admin/runs/run_-w6fuC_zXl2B/4_gen_paper_repo/_4_assemble_paper/paper/workspace/.sdk_openhands_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-06-17 06:05:32 UTC

```
Direction: Comparative Political Economy — Inequality and Democratic Resilience. Something genuinely novel and groundbreaking that traces how inequality, education, and democratic-quality co-evolve across post-1990 democratizers, identifies what sustains resilience versus backsliding, and tests whether welfare-state institutions mediate the link. MUST use Our World in Data (OWID) panels.

Ambition: level 1 of 5 — confirmatory/parametric science: a careful confirmatory test within established institutional-economics theory; precision, identification, and robustness over conceptual novelty.

Reviewer: I am Daron Acemoglu (MIT). Calibrate from my existing work. Cross-domain perspectives (historical sociology, political behavior, economic anthropology) welcome — but keep them close to what I already know, not too far from my background.

Submission/Goal: a paper for the American Political Science Review, the Journal of Democracy, or World Politics. Audience: comparative political economists and political scientists. Tone: empirically rigorous, grounded in institutional economics, reproducible on public OWID data.
```

### [3] SKILL-INPUT — aii-paper-to-latex · 2026-06-17 06:05:45 UTC

The agent loaded the **aii-paper-to-latex** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-paper-to-latex
description: LaTeX paper assembly and compilation. Covers document setup, figure inclusion from pre-generated JPEGs, compilation process, and output files. Use when assembling a paper from pre-written text and pre-generated figures into a compiled PDF.
---

## LaTeX Paper Assembly

Assembles a research paper from paper text, pre-generated figure JPEGs, and bibliography into a compiled PDF.

### Document Setup

```latex
\documentclass[11pt,letterpaper]{article}
\usepackage{graphicx, geometry, amsmath, hyperref, natbib, booktabs, xcolor, listings}
\geometry{margin=1in}
\hypersetup{colorlinks=true, linkcolor=black, citecolor=black, urlcolor=black}
```

### Figure Inclusion

CRITICAL: Include ALL figures. Every figure MUST appear in the paper.

```latex
\begin{figure}[!htbp]
  \centering
  \includegraphics[width=0.92\textwidth,keepaspectratio]{figures/filename.jpg}
  \caption{Descriptive caption.}
  \label{fig:label}
\end{figure}
```

Rules:
- ALWAYS use `[!htbp]` float placement (NOT `[t]` or `[h]` alone)
- ALWAYS constrain with `width` and `keepaspectratio` to prevent page takeover
- Every figure needs `\caption`, `\label`, and a `\ref` in the text
- Do NOT convert figures to tables or describe them without inserting the image
- Do NOT skip any figures

### Compilation Process

Run each command separately (do NOT chain with `&&` — pdflatex often exits non-zero on warnings, which would skip bibtex and leave citations as `??`):

```bash
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex
```

All four commands are required. Skipping bibtex causes `??` in all citations.
Fix any errors between runs. Verify `./paper.pdf` was created.

### Output Files

- `./paper.tex` — LaTeX source
- `./references.bib` — bibliography file
- `./paper.pdf` — compiled PDF
- `./figures/*.jpg` — all figure images (pre-generated, copied into workspace)
````

### [4] SKILL-INPUT — aii-semscholar-bib · 2026-06-17 06:05:45 UTC

The agent loaded the **aii-semscholar-bib** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-semscholar-bib
description: Build bibliographies using Semantic Scholar. Batch-fetch BibTeX for papers by DOI, ArXiv ID, or title. Use when writing papers, generating reference lists, or building .bib files.
---

## Tool: `aii_semscholar_bib__fetch`

Batch-fetch BibTeX entries from Semantic Scholar. Pass all references in a single call — the tool handles batching internally.

### How it works

1. **DOI/ArXiv refs** → batched into POST /paper/batch calls (up to 500 per API call, auto-chunked)
2. **Title-only refs** → individual GET /paper/search/match (1s delay between)
3. **Post-process** → fix entry type, fix citation key (AuthorYYYY), inject DOI

The ability server runs a single worker (`max_threads: 1`). Multiple concurrent tool calls are queued — each runs independently (no cross-request aggregation). Batching happens within each request.

### Input format

```json
{
  "references": [
    {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
    {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
    {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
  ]
}
```

Each reference object can have:
- `doi` — DOI string (ArXiv DOIs like `10.48550/arXiv.XXXX.XXXXX` auto-convert to ArXiv IDs)
- `arxiv` — ArXiv ID (e.g. `"2305.14325"`)
- `title` — Paper title (used for search/match when no DOI/ArXiv)
- `author` — First author last name (for cleaner citation key)
- `year` — Publication year (int, for citation key)

At least one of `doi`, `arxiv`, or `title` is required per reference.

### Output format

```json
{
  "success": true,
  "bib_text": "@inproceedings{Vaswani2017, ...}\n\n@article{Wei2022, ...}",
  "total": 3,
  "found": 3,
  "failed_count": 0,
  "entries": [{"citation_key": "Vaswani2017", "bibtex": "...", "title": "...", "doi": "...", "arxiv": ""}],
  "failed": []
}
```

### Workflow

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Call `aii_semscholar_bib__fetch` with the full list in **one call**
3. Save `bib_text` from the response to your `references.bib` file
4. Check `failed` — for any missed papers, follow the **fallback procedure** below

### Fallback for failed references (MANDATORY)

NEVER fabricate BibTeX. For each failed reference:
1. **WebSearch** for `"Title" author year` (try `site:arxiv.org` too)
2. **WebFetch** the paper page → extract title, authors, year, venue, DOI/ArXiv ID
3. If DOI/ArXiv found → retry `aii_semscholar_bib__fetch` with it
4. Last resort: write BibTeX by hand using **only verified info from the actual paper page**

---

### CLI (for manual use / debugging)

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-semscholar-bib" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_semscholar_bib__fetch.py --refs '[
  {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
  {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
  {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
]'
```

`--json, -j` — output raw JSON instead of .bib text

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [5] SYSTEM-USER prompt · 2026-06-17 06:13:55 UTC

```
<validation-feedback>
Attempt 1 failed validation.

Schema validation found 1 problem — fix ALL of them at once:
  - at `title`: 'Inequality, Political Equality, and Democratic Resilience: Evidence from Post-1990 Democratizers - LaTeX Paper Generation' is too long (at most 90 characters, got 121)
Every required field must be present and every field type must match the schema.

Please use the Write tool to overwrite `.sdk_openhands_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```
