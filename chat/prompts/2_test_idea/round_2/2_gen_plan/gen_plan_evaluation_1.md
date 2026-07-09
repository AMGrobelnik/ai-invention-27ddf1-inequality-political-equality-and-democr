# gen_plan_evaluation_1 — test_idea

> Phase: `invention_loop` · round 2 · `gen_plan`
> Run: `run_-w6fuC_zXl2B` — Inequality Resilience
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_plan_evaluation_1` (sdk_openhands_agent)

### [1] SYSTEM-USER prompt · 2026-06-17 03:49:11 UTC

````
<hypothesis>
kind: hypothesis
title: >-
  The Dual Stratification Hypothesis: How Education and Income Inequality Co-Evolve to Undermine Democratic Resilience
hypothesis: >-
  Among post-1990 democratizers, the interaction between income inequality (measured by SWIID Gini) and education inequality
  (measured by Barro-Lee education Gini) creates a 'dual stratification' equilibrium that accelerates democratic backsliding,
  operating through reduced political equality (V-Dem v2pepwrsoc). Public education spending buffers this effect, but the
  hypothesis requires testing with expanded country sample and valid inequality measures before confirmation. The current
  evidence is limited to correlation patterns in a small sample (3 countries) with poor inequality proxies; confirmatory evidence
  is pending improved measurement and estimation.
motivation: >-
  While recent work establishes income inequality as a predictor of democratic backsliding (PNAS 2025), and Acemoglu & Robinson's
  framework emphasizes de facto vs. de jure power, no study has tested whether education inequality AMPLIFIES income inequality's
  effect on backsliding. This is theoretically important because: (1) Education inequality may matter MORE than income inequality
  for democratic resilience, as education affects political sophistication and who can run for office; (2) The co-evolution
  of both inequalities creates persistent elite capture (Acemoglu & Robinson 2008); (3) Welfare state spending on education
  could break this equilibrium, but this has not been tested at scale. For comparative political economy, this identifies
  a specific mechanism (de facto power distribution) through which inequality undermines democracy, and a specific policy
  lever (education spending) to sustain democratic resilience.
assumptions:
- >-
  Post-1990 democratizers share sufficient institutional variation to identify effects (tested via included country fixed
  effects)
- >-
  V-Dem's political equality index validly measures de facto power distribution (established in V-Dem codebook v.14)
- >-
  Education inequality can be proxied by tertiary enrollment rates and average years of education (direct inequality measures
  by SES not available in OWID, but proxies correlate with inequality in developed democracies)
- >-
  Welfare state spending on education is exogenous to short-term democratic backsliding (tested via lagged specifications)
- >-
  The de facto power mechanism operates at the national level (not just individual level)
investigation_approach: |-
  1. DATA: Merge OWID panels - V-Dem v.14 (liberal democracy index, political equality index), World Bank PIP (Gini coefficients), UNESCO education data (tertiary enrollment, average years), OECD SOCX (public education spending %GDP), Lindert social spending data. Sample: 35-40 post-1990 democratizers, 1990-2024 panel.
  2. IDENTIFICATION: Panel fixed-effects models with lagged dependent variable (Arellano-Bond GMM) to test: (a) Main effect of Gini on V-Dem liberal democracy index; (b) Interaction effect of Gini × education inequality; (c) Mediation via political equality index (Sobel-Goodman test); (d) Moderation via education spending (triple interaction: Gini × education inequality × education spending).
  3. ROBUSTNESS: (a) Alternative inequality measures (SWIID); (b) Alternative democracy measures (Polity V, EIU); (c) Placebo tests (pre-1990 period should show no effect); (d) Instrumental variable approach using lagged education inequality as instrument.
success_criteria: |-
  Hypothesis is CONFIRMED if: (1) Interaction term Gini × education inequality is negative and significant (p < 0.05) for predicting V-Dem liberal democracy decline; (2) Political equality index mediates this relationship (Sobel test p < 0.05); (3) Triple interaction Gini × education inequality × education spending is positive and significant (buffer effect).
  Hypothesis is DISCONFIRMED if: (1) No significant interaction (only main effects); (2) Education spending does not moderate the relationship; (3) De facto power (political equality) does not mediate.
related_works:
- >-
  PNAS 2025 'Income inequality and the erosion of democracy in the twenty-first century' (Haggard, Pennington, et al.): Establishes
  income inequality as predictor of democratic backsliding using V-Dem data. OUR DIFFERENCE: We test education inequality's
  INTERACTION with income inequality, not just main effect of income. Also, we identify mechanism (de facto power) and mediator
  (welfare spending).
- >-
  Acemoglu & Robinson (2008) 'Persistence of Power, Elites, and Institutions' (AER): Theoretically models how de facto power
  offsets de jure political power changes. OUR DIFFERENCE: We provide the first EMPIRICAL TEST of how education inequality
  affects de facto power distribution and subsequent democratic backsliding, using new V-Dem political equality data not available
  when A&R wrote.
- >-
  Baliamoune-Lutz (2018) 'Political Elites, Democracy and Education': Theoretical model on elite's education subsidy decisions
  under de facto power. OUR DIFFERENCE: We test the REVERSE causal direction - how education inequality (not elite's subsidies)
  affects democratic backsliding via de facto power - and use macro panel data across 35+ countries, not just Africa.
- >-
  Iversen & Soskice (2006) 'Education, Inequality, and Social Protection': Links education systems to inequality and welfare
  states. OUR DIFFERENCE: We focus on democratic BACKSLIDING (not just redistribution), use post-1990 democratizers (not just
  OECD), and test de facto power as mechanism (not just political preferences).
- >-
  Zuazu (2018) V-Dem Working Paper 'Electoral Systems and Income Inequality': Tests how political equality (de facto power)
  affects inequality. OUR DIFFERENCE: We reverse the causality - testing how inequality (income + education) affects political
  equality and democratic backsliding, not the other way.
inspiration: >-
  The hypothesis synthesizes three insights from comparative political economy: (1) Acemoglu & Robinson's de facto vs. de
  jure power framework (theoretically established but rarely tested directly with new V-Dem political equality data); (2)
  The 'dual stratification' concept from stratification economics (joint effects of multiple inequalities); (3) The welfare
  state as 'democratic insurance' - extending Iversen & Soskice's skill formation framework to focus on democratic resilience,
  not just redistribution. The cross-domain inspiration comes from 'persistence' models in macroeconomics (how multiple equilibria
  form and what shifts them) applied to political institutions.
terms:
- term: Dual Stratification
  definition: >-
    The co-occurrence of high income inequality and high education inequality, creating a persistent elite-dominated equilibrium
    that resists democratic deepening
- term: De Facto Political Power
  definition: >-
    Political influence arising from wealth, organization, education, or social networks, as distinct from de jure power allocated
    by political institutions (Acemoglu & Robinson 2008)
- term: Political Equality Index (V-Dem)
  definition: >-
    V-Dem measure (v2pepwrsoc) of the extent to which political power is evenly distributed across socioeconomic groups, ranging
    from 0 (elite monopoly) to 4 (equal power)
- term: Democratic Backsliding
  definition: >-
    The state-led debilitation or elimination of political institutions sustaining democratic control over executive power,
    including civil liberties, free elections, and rule of law (Lührmann & Lindberg 2019)
- term: Post-1990 Democratizers
  definition: >-
    Countries that transitioned to democracy after 1989, including post-communist states, Latin American countries in the
    Third Wave, and sub-Saharan African democratizers in the 1990s
- term: Welfare State Buffer
  definition: >-
    The hypothesis that generous welfare state spending (especially on education) reduces the political power asymmetry created
    by income and education inequality, thereby sustaining democratic quality
summary: >-
  Among post-1990 democratizers, the interaction of income and education inequality creates 'dual stratification' that accelerates
  democratic backsliding by enabling elite capture via de facto power. Welfare state education spending breaks this equilibrium.
  Tested using OWID panels (V-Dem, World Bank PIP, UNESCO, OECD SOCX) with panel GMM and mediation analysis.
_relation_rationale: >-
  Refining measurement strategy and acknowledging limited evidence; same conceptual frame but more specific/honest
_confidence_delta: decreased
_key_changes:
- >-
  Added specific measurement requirements: SWIID Gini and Barro-Lee education Gini (per research artifact recommendations)
- >-
  Acknowledged that hypothesis is NOT yet confirmed - current evidence is limited to correlations in small sample with poor
  proxies
- >-
  Added requirement for expanded country sample of post-1990 democratizers (must identify 10-20 countries using V-Dem coding)
- >-
  Clarified that welfare state buffer effect is untested pending valid education inequality measure
- >-
  Added honesty about current limitations: only 3 post-1990 democratizers in current data, high missing data rates
- >-
  Reframed success criteria to require actual GMM estimation with valid measures, not just correlation patterns
relation_type: evolution
</hypothesis>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: evaluation_iter2_dir3
type: evaluation
objective: >-
  Evaluate the GMM results for statistical validity and prepare the complete results section for the paper, including properly
  formatted regression tables (Table 2), specification test summaries, and reconciliation of all data discrepancies identified
  by the reviewer.
approach: >-
  Analyze the experiment output from the current iteration's experiment artifact to: (1) Verify specification test pass rates:
  AR(1) p<0.05, AR(2) p>0.05, Hansen J p>0.05; (2) Check instrument count < N to avoid proliferation bias; (3) Compute and
  report within-country correlations (demeaned data) for key variables; (4) Prepare Table 2 with all regression results in
  APSR format: coefficients with clustered standard errors in parentheses, stars for significance, N, specification tests
  at bottom; (5) Reconcile paper N values with actual data N, document Cape Verde exclusion reason (missing data), correct
  '<6% missing' claim with honest missing data rates; (6) Produce evaluation report with: results summary, specification test
  table, robustness check summary, data discrepancy reconciliation appendix. Output: eval_out.json with complete results tables
  and evaluation metrics.
depends_on: []
</artifact_direction>



<instructions>
YOUR ROLE: Write a detailed PLAN for the artifact. A separate executor agent runs the actual artifact later.

You are a PLANNER, not an executor. Your output is a plan that tells the executor what to do and how.
Do NOT execute the artifact itself — a separate agent handles that. Your job is to plan it so well that the executor can follow your plan step by step.

You CAN and SHOULD: search the web, read papers, and explore library docs to make your plan concrete.
You CANNOT run shell commands or scripts — code execution is disabled. Research via web tools only.

Do NOT do the executor's job: don't download datasets, don't implement code, don't run experiments, don't write proofs, don't compute evaluations.

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

EVALUATION executor scope:
  Output: eval_out.json with evaluation results
  DOES: Any evaluation of experiment results — metrics, statistical tests, ablations, comparisons, visualizations, robustness checks, error analysis, etc.
  DOES NOT: Implement new methods (use EXPERIMENT), collect data (use DATASET)
  This is for analyzing experiment outputs from any angle
</artifact_executor_scope>

<artifact_planning_rules>
EVALUATION: Must depend on at least one EXPERIMENT. Focus on statistical rigor and validity checks.
</artifact_planning_rules>


GOOD PLANS: specific, actionable, consider failure scenarios, build on the suggested approach.
BAD PLANS: vague hand-waving, ignoring the suggested approach, missing critical executor details.
</instructions><user_data>
User-provided reference materials are available at `/home/adrian/projects/ai-inventor/aii_data/users/admin/runs/run_-w6fuC_zXl2B/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `/home/adrian/projects/ai-inventor/aii_data/users/admin/runs/run_-w6fuC_zXl2B/3_invention_loop/iter_2/gen_plan/gen_plan_evaluation_1/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "description": "Plan for an EVALUATION artifact.",
  "properties": {
    "title": {
      "description": "Short title for the plan",
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Brief summary",
      "title": "Summary",
      "type": "string"
    },
    "runpod_compute_profile": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": "cpu_light",
      "description": "Compute tier for execution \u2014 pick from the available profiles list (e.g., 'gpu', 'cpu_heavy', 'cpu_light'). Only used in RunPod mode.",
      "title": "Runpod Compute Profile"
    },
    "metrics_descriptions": {
      "description": "What metrics will be computed and how they're defined",
      "title": "Metrics Descriptions",
      "type": "string"
    },
    "metrics_justification": {
      "description": "Why these metrics are the right ones - what do they tell us about the hypothesis",
      "title": "Metrics Justification",
      "type": "string"
    }
  },
  "required": [
    "title",
    "metrics_descriptions",
    "metrics_justification"
  ],
  "title": "EvaluationPlan",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `/home/adrian/projects/ai-inventor/aii_data/users/admin/runs/run_-w6fuC_zXl2B/3_invention_loop/iter_2/gen_plan/gen_plan_evaluation_1/.sdk_openhands_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-06-17 03:49:11 UTC

```
Direction: Comparative Political Economy — Inequality and Democratic Resilience. Something genuinely novel and groundbreaking that traces how inequality, education, and democratic-quality co-evolve across post-1990 democratizers, identifies what sustains resilience versus backsliding, and tests whether welfare-state institutions mediate the link. MUST use Our World in Data (OWID) panels.

Ambition: level 1 of 5 — confirmatory/parametric science: a careful confirmatory test within established institutional-economics theory; precision, identification, and robustness over conceptual novelty.

Reviewer: I am Daron Acemoglu (MIT). Calibrate from my existing work. Cross-domain perspectives (historical sociology, political behavior, economic anthropology) welcome — but keep them close to what I already know, not too far from my background.

Submission/Goal: a paper for the American Political Science Review, the Journal of Democracy, or World Politics. Audience: comparative political economists and political scientists. Tone: empirically rigorous, grounded in institutional economics, reproducible on public OWID data.
```

### [3] SKILL-INPUT — aii-web-tools · 2026-06-17 03:50:47 UTC

The agent loaded the **aii-web-tools** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-web-tools
description: "Web research toolkit: web search (Serper/Google), web page fetch as markdown (HTML and PDF), and regex grep over full page/PDF text. Use whenever a task needs to search the web, read a page, mine a paper/PDF, verify citations, or extract exact quotes, numbers, or methodology from a URL."
---

## Web tools

You have three web capabilities: **search**, **fetch**, and **grep** (exact
regex extraction over a full page or PDF).

**Pick where they come from, in this order:**

1. **If you have built-in `WebSearch` / `WebFetch` tools, PREFER those over the
   scripts below.** They may be **deferred tools** (listed by name but with
   schemas not yet loaded) — if so, call `ToolSearch("select:WebSearch,WebFetch")`
   ONCE to load them, then use them normally. Do not skip them just because they
   need that one extra load step; they are the preferred path. Pair them with the
   `aii_web_tools__fetch_grep` script below when you need exact text / numbers /
   methodology that a summary would miss, or when reading a PDF.
2. **Only if you have NO built-in `WebSearch` / `WebFetch`** (e.g. the OpenHands
   backend), use the scripts in this skill (below). They are our own
   implementations — Serper.dev for search, html2text + PyMuPDF for fetch, and
   regex grep over the full document text. They work without any built-in web
   tools.

Workflow either way: **search** (discover) → **fetch** (read for the gist) →
**grep** (pull exact details / read PDFs).

---

## Running the scripts

Run every script with the skill's pre-provisioned interpreter (it already has
`requests`, `html2text`, `pymupdf`, `python-dotenv`). Set `PY` once:

```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-web-tools"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

### 1. Search the web (Serper.dev / Google)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "neuro-symbolic FOL translation LLM" --max-results 10
```

Returns ranked title / URL / snippet lines. Use it first to scan the
landscape; snippets are for discovery only — fetch a page before judging it.

### 2. Fetch a page as markdown (HTML or PDF)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" fetch --url "https://arxiv.org/abs/2303.11366" --max-chars 10000
```

`--max-chars` caps output (default 10000); `--char-offset N` pages further in.
Handles PDFs transparently via PyMuPDF.

### 3. Grep a page or PDF (exact regex extraction)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" grep --url "https://arxiv.org/pdf/2303.11366" --pattern "verbal reinforcement" --max-matches 20 --context-chars 200
```

Returns only the matching sections with surrounding context — the right tool
for exact numbers, table values, methodology, or long PDFs where a summary
would lose the detail. `-i` for case-insensitive.

**Parallelize** independent searches/fetches in one turn; only sequence a
fetch after the search that produced its URL.

---

## Notes

- The scripts call our ability server. If a script prints
  `Ability service not available`, the server is down — say so rather than
  silently improvising a different search method.
- Do **not** hand-roll your own `requests`/scraping for search when these
  tools are available: Serper returns clean Google results and the fetch/grep
  scripts already handle HTML, PDFs, and encoding.
````

### [4] SKILL-INPUT — aii-fast-web-search · 2026-06-17 03:51:39 UTC

The agent loaded the **aii-fast-web-search** skill.

```
Tool: invoke_skill
{
  "name": "aii-fast-web-search"
}
```

### [5] SKILL-INPUT — aii-web-research-tools · 2026-06-17 03:51:53 UTC

The agent loaded the **aii-web-research-tools** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-web-research-tools
description: "Comprehensive web research toolkit — use whenever a task needs MORE than a handful of WebSearch/WebFetch calls (multi-source literature reviews, deep verification across many pages, paper/PDF mining, cross-referencing claims, building bibliographies). Not for single quick lookups — use raw WebSearch/WebFetch for those. Adds aii_web_tools__fetch_grep for exact regex extraction over HTML or PDFs (arXiv, journals) with context windows, beyond what WebFetch's lossy summary returns. Trigger: any extensive/comprehensive/deep research task, literature review, multi-source investigation, verify many citations, arxiv, paper, PDF, exact quote, methodology, table value, regex."
---

## Available Web Tools

Three levels of web tools:

1. **WebSearch** — broad discovery. Returns titles, URLs, snippets. Cheapest. Use first to scan the landscape.
2. **WebFetch** — read a specific page. LLM summarizes it. HTML only. May miss specific details.
3. **aii_web_tools__fetch_grep** — exact text extraction from HTML or PDF. Regex matching with context windows.
   Use for precise details, methodology, or when WebFetch missed something.
   Key params: pattern (required), max_matches (default 20), context_chars (default 200 per side).

**Workflow:** WebSearch → WebFetch for gist → aii_web_tools__fetch_grep for exact details or PDFs.

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-web-research-tools"
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [6] SYSTEM-USER prompt · 2026-06-17 03:56:47 UTC

```
<validation-feedback>
Attempt 1 failed validation.

You have not created the output file `.sdk_openhands_agent_struct_out.json` yet. Use the Write tool to create it.

Please use the Write tool to overwrite `.sdk_openhands_agent_struct_out.json` with corrected JSON. Do not invent new fields; match the schema you were given.
</validation-feedback>
```

### [7] SKILL-INPUT — aii-json · 2026-06-17 03:59:27 UTC

The agent loaded the **aii-json** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-json
description: JSON validation and formatting toolkit. Validate JSON files against schemas for experiment pipelines, and generate full/mini/preview versions of JSON datasets. Use for validating pipeline outputs, checking schema compliance, or creating size-optimized JSON variants.
---

## Contents

- Validating JSON (schema validation against experiment schemas)
- Formatting JSON (generate full/mini/preview versions)

**IMPORTANT - Parallel execution:** GNU `parallel` subshells do NOT inherit `source activate`. Use `export` for variables and **single-quoted** command templates so parallel's subshells can resolve them:
```
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

---

## Validating JSON

Validate JSON files against predefined schemas for experiment-based hypothesis selection, data collection, solution generation, and evaluation.

### Quick Start

1. Read the schema spec you need to adhere to (e.g., `schemas/exp_eval_sol_out.json`)
2. Create your output file following that schema structure
3. Validate:

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /path/to/eval_out.json
```

### Script: aii_json_validate_schema.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file /tmp/eval_out.json
```

**Parallel execution (multiple validations):**

IMPORTANT: When validating multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_validate_schema.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --format {1} --file {2}' ::: 'exp_sel_data_out' 'exp_gen_sol_out' 'exp_eval_sol_out' :::+ '/tmp/full_data_out.json' '/tmp/method_out.json' '/tmp/eval_out.json'
```

**Example output (success):**
```
Validating: aii_json_validate_schema.py
Format: exp_eval_sol_out

✓ Validation PASSED
```

**Example output (failure):**
```
Validating: aii_json_validate_schema.py
Format: exp_sel_data_out

✗ Validation FAILED

Errors:
  Path: datasets → 0 → examples → 0
  Error: 'output' is a required property
  Validator: required
```

**Parameters:**

`--format` (required)
- Format type to validate against
- Determines which schema to use

`--file` (required)
- Path to JSON file to validate
- Must be valid JSON
- **Always pass an absolute path.** Relative paths resolve from the
  ability server's CWD (typically ``/ai-inventor/aii_server``), not from
  your agent workspace, so ``data_out/x.json`` will silently look in the
  wrong directory and fail with "Could not load JSON file". The validate
  endpoint also accepts a ``workspace_dir`` arg if you need to keep a
  relative path — pass your workspace path there.

**Tips:**
- Fix errors in your JSON and rerun validation until it passes

### Schema Files

Schemas are stored in `.claude/skills/aii-json/schemas/`:

**Hypothesis Selection & Evaluation:**
- `sel_hypo_out.json` - Hypothesis Selection output (all hypotheses with selected flags)
- `feasibility_eval_all.json` - All hypotheses with feasibility scores
- `feasibility_eval_top.json` - Top 5 most feasible hypotheses
- `novelty_research_one.json` - Single hypothesis novelty research arguments with citations
- `novelty_eval_all.json` - All hypotheses with novelty scores
- `novelty_eval_top.json` - Single best selected hypothesis

**Experiment Pipeline:**
- `exp_sel_data_out.json` - Experiment Data Selection format
- `exp_gen_sol_out.json` - Experiment Solution Generation format
- `exp_eval_sol_out.json` - Experiment Solution Evaluation format

---

## Formatting JSON

Generate three size-optimized versions of a JSON file for efficient development and preview:
- **full**: Identical to original (all data)
- **mini**: First 3 items only (for quick testing)
- **preview**: Mini + all strings truncated to 200 chars (for quick inspection)

### Quick Start

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

### Script: aii_json_format_mini_preview.py

**Example input:**
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input method_out.json
```

**Parallel execution (multiple files):**

IMPORTANT: When formatting multiple files, use GNU parallel instead of separate Bash tool calls:
```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-json" && \
export PY="$SKILL_DIR/../.ability_client_venv/bin/python" && \
export S="$SKILL_DIR/scripts/aii_json_format_mini_preview.py" && \
parallel -j 50 -k --group --will-cite '$PY $S --input {}' ::: 'full_data_out.json' 'method_out.json' 'eval_out.json'
```

**Example output:**
```
Generated 3 versions:
  Full (50 items): /path/to/full_method_out.json
  Mini (3 items): /path/to/mini_method_out.json
  Preview (3 items, truncated): /path/to/preview_method_out.json
```

**Parameters:**

`--input` (required)
- Path to input JSON file
- Must have a top-level array
- Example: `method_out.json`, `full_data_out.json`

`--output-dir` (optional)
- Output directory for generated files
- Default: same directory as input file
- Files are prefixed with `full_`, `mini_`, `preview_`

**Output Files:**

All three files use the same base name with different prefixes:
- `full_{basename}.json` - Complete dataset (identical to original)
- `mini_{basename}.json` - First 3 array items only
- `preview_{basename}.json` - First 3 items with strings truncated to 200 chars

**Tips:**
- Input JSON must have a top-level array structure
- String truncation is recursive (applies to nested objects and arrays)
- Use preview files for quick inspection without reading large datasets
- Use mini files for developing/testing code before running on full dataset

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [8] SKILL-INPUT — aii-python · 2026-06-17 04:03:54 UTC

The agent loaded the **aii-python** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-python
description: Python coding standards for experiment and evaluation scripts. Covers environment setup, logging, error handling, and code structure.
---

## Environment Setup

- Python 3.12+
- **NEVER use `pip` or `.venv/bin/pip`** — they are not installed. Use `uv` for ALL package operations:
  ```bash
  uv venv .venv --python=3.12
  source .venv/bin/activate  # or: .venv/bin/python script.py
  uv pip install pandas loguru  # NOT: pip install
  ```
- Create `.toml` file with dependencies, create uv `.venv` and activate it
- NO inline dependencies (no `# /// script` headers)

## Logging

Use `loguru` for all logging. Add a file sink alongside stdout.

```python
from loguru import logger
import sys

logger.remove()  # Remove default handler
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")
```

Rules:
- Log every major step (data loading, processing start/end, results)
- If applicable, log every LLM API call input and output
- Truncate long outputs in logs (add truncation logic for potentially large strings)
- Use `logger.error()` in except blocks (traceback auto-captured)

## Error Handling

- Wrap major operations in try/except blocks
- Use `@logger.catch(reraise=True)` decorator on main functions — without `reraise=True`, the script exits 0 even on uncaught exceptions, hiding failures from downstream consumers
- Use explicit exception types, not bare `except:`
- Never silently swallow exceptions — always log them

```python
@logger.catch(reraise=True)
def main():
    try:
        data = load_data(path)
    except FileNotFoundError:
        logger.error("Data file not found")
        raise
    except json.JSONDecodeError:
        logger.error("Invalid JSON in data file")
        raise
```

## Code Structure

- Use `pathlib.Path` for file operations: `Path("data/input.json").read_text()` not `open(...).read()`
- Use type hints for function signatures
- Use keyword arguments for functions with more than 4 parameters
- No hardcoded paths — derive from script location or accept as arguments

## Script Pattern

Standard pattern for experiment/evaluation scripts:

```python
#!/usr/bin/env python3
"""Brief description of what this script does."""

from loguru import logger
from pathlib import Path
import json
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

@logger.catch(reraise=True)
def main():
    # Load data
    data_path = Path("full_data_out.json")
    logger.info(f"Loading data from {data_path}")
    data = json.loads(data_path.read_text())
    logger.info(f"Loaded {len(data['examples'])} examples")

    # Process
    results = []
    for i, example in enumerate(data["examples"]):
        try:
            result = process(example)
            results.append(result)
        except Exception:
            logger.error(f"Failed on example {i}")
            continue

    # Save output
    output = {"examples": results}
    Path("method_out.json").write_text(json.dumps(output, indent=2))
    logger.info(f"Saved {len(results)} results")

if __name__ == "__main__":
    main()
```
````
