# PRISM Theory Validation — Agentic Research Plan v1.0

```yaml
spec_version: 1.0
title: PRISM 5D Logarithmic-Spiral Worldline — Empirical Validation Program
principal: Kip Madden
generated: 2026-04-16
framework_target: PRISM Estimate v7.0.4 compatible (17-agent, 14-MCP)
estimated_wall_time: 6-10 weeks (with human-in-the-loop checkpoints)
estimated_agent_tokens: 800K-1.5M across all phases
status: ready-to-execute
```

---

## 1. Mission

Determine whether the PRISM framework — which proposes that atomic structure is a 4D Cartesian projection of a 5D logarithmic-spiral worldline with α as the native rotation-scaling coupling — produces quantitatively correct predictions for (a) the hydrogen Lamb shift, (b) the proton radius discrepancy between electronic and muonic hydrogen, and (c) the running of α with energy scale, from a single geometric parameter without tuning.

## 2. Success Criteria

```yaml
must_have:
  - PRISM-derived s-state correction function produces Bethe-log values (2.98, 2.81, 2.77, 2.75, 2.74 for n=1..5) within 10% without fitting parameters to the data
  - Derivation is reproducible: another agent given the framework and the spec can re-derive the function
  - Final report clearly states whether PRISM is validated, falsified, or inconclusive at the achievable precision

should_have:
  - Same derived function predicts muonic hydrogen Lamb shift within experimental uncertainty
  - Cross-prediction for α(Q²) running agrees with LEP measurements
  - Public-release-quality code artifacts in version-controlled repo

nice_to_have:
  - Prediction for helium+ (hydrogenic Z=2) spectrum
  - Framework connection to proton radius puzzle (4% discrepancy explained)
  - Paper draft suitable for arXiv submission
```

## 3. Constraints

```yaml
hard:
  data_sources_allowed:
    - NIST Atomic Spectra Database (static Handbook tables)
    - NIST HDEL theoretical levels
    - CODATA 2022 fundamental constants
    - Published experimental papers (CREMA for muonic H, LEP for α running)
  data_sources_prohibited:
    - Any source requiring credentials
    - Non-peer-reviewed preprints as primary data (allowed as context only)
  compute_budget: single workstation-class machine, no GPU required
  copyright: no verbatim reproduction of copyrighted paper text beyond short quotes

soft:
  token_budget_per_phase: <200K input+output tokens
  human_checkpoint_frequency: after each phase; mandatory before publication
  parallelism: phase 1 tasks are mostly sequential; phases 2-4 can run concurrently after phase 1 completes
```

## 4. Assumptions (Challengeable)

These are the operating assumptions. Any agent may flag them for review:

```yaml
assumption_1:
  statement: PRISM's 5D framework, as currently specified by Kip Madden, is self-consistent enough to derive an explicit s-state correction function
  risk: framework may have implicit free parameters or require additional postulates
  check: Theoretician agent must flag any point in derivation where a choice is made without first-principles motivation

assumption_2:
  statement: The standard Bethe log is the correct target for comparison
  risk: PRISM might predict a different (but equally valid) decomposition of QED effects
  check: Validator must verify any alternative decomposition produces the same measured Lamb shift

assumption_3:
  statement: Reduced-mass and recoil effects factor cleanly from QED contributions
  risk: PRISM geometry may couple them non-trivially
  check: If PRISM derivation produces mass-coupled geometry, run v4 pipeline with PRISM-predicted baseline instead of Dirac+recoil

assumption_4:
  statement: 5-fold-symmetry / φ signature is testable at currently-achievable precision
  risk: may require data at precision not yet published
  check: Validator computes required precision for N-σ detection of φ-modulation before running
```

## 5. Agent Roles

Named using PRISM Estimate convention (RA codes optional for your internal tracking):

```yaml
orchestrator:
  responsibility: sequence phases, manage state, enforce checkpoints, escalate blockers
  inputs: this spec, current_state.json
  outputs: phase_status.json, escalation_queue.md
  tools_required: [state_manager, escalation_router]

data_fetcher:
  responsibility: pull raw data from external sources with retry/cache/validate
  inputs: source_urls.yaml, cache_policy.json
  outputs: raw_data/*.html, raw_data/*.csv, fetch_audit.log
  tools_required: [web_search, web_fetch, disk_cache]
  mcp_servers: [filesystem]

parser:
  responsibility: transform raw data into structured, typed records
  inputs: raw_data/*
  outputs: structured_data/*.csv, structured_data/*.json, data_schema.yaml
  tools_required: [regex_engine, html_parser, csv_writer]
  mcp_servers: [filesystem]

theoretician:
  responsibility: derive mathematical expressions from PRISM first principles
  inputs: prism_framework.md, derivation_targets.yaml
  outputs: derivations/*.tex, derivation_log.md
  tools_required: [symbolic_math (sympy), latex_renderer]
  human_in_the_loop: REQUIRED — every derivation step reviewed before acceptance
  mcp_servers: [filesystem, sympy-mcp if available]

computer:
  responsibility: evaluate derived expressions numerically, run fits, generate predictions
  inputs: derivations/*.json, structured_data/*.csv
  outputs: predictions/*.csv, fit_results/*.json, diagnostics/*.png
  tools_required: [python (numpy, scipy, matplotlib), pysr (optional)]
  mcp_servers: [filesystem, code_execution]

validator:
  responsibility: cross-check predictions against literature, flag inconsistencies, compute confidence intervals
  inputs: predictions/*.csv, literature_values.yaml
  outputs: validation_report.md, anomaly_log.md
  tools_required: [statistical_tests, literature_lookup]
  mcp_servers: [filesystem, web_search]

critic:
  responsibility: red-team findings, propose alternative explanations, search for confounds
  inputs: validation_report.md, current_hypotheses.md
  outputs: counter_hypotheses.md, null_test_suggestions.md
  tools_required: [literature_search, reasoning_chain]

reporter:
  responsibility: synthesize all outputs into human-readable deliverables
  inputs: all phase outputs
  outputs: final_report.docx, executive_summary.md, figures/*
  tools_required: [docx_generator, matplotlib, pandoc]
  mcp_servers: [filesystem]

librarian:
  responsibility: maintain immutable knowledge base of literature values, prior art, established facts
  inputs: this spec's citations, validator lookups
  outputs: knowledge_base/*.yaml
  tools_required: [knowledge_store, citation_formatter]
  mcp_servers: [filesystem]
```

## 6. Tool / MCP Server Manifest

```yaml
required_mcp_servers:
  - filesystem: read/write all artifacts in working directory
  - web_search: general literature lookup
  - web_fetch: direct URL retrieval (NIST static pages, published papers)
  - code_execution: Python runtime for analysis pipeline

recommended_mcp_servers:
  - sympy_mcp: symbolic derivation support (if available in your inventory)
  - arxiv_mcp: structured paper retrieval
  - zotero_mcp: citation management

optional:
  - github_mcp: version control of artifacts
  - notion_mcp: human-facing progress dashboard
```

---

## 7. Phase Structure

### Phase 0 — Foundation (PREREQUISITE, ALREADY DONE)

Status: **complete**. Artifacts `prism_hydrogen_v4.py` and `prism_research_summary.docx` exist. Agents may reuse but must not re-derive.

### Phase 1 — First-Principles Derivation (CRITICAL PATH)

The pivotal phase. If the derivation produces Bethe-log values matching literature, PRISM is validated. If not, PRISM is falsified at this precision. Everything else in the plan is downstream of phase 1.

### Phase 2 — Muonic Hydrogen Cross-Check (UNIQUE CLAIM)

The test no other theory explains naturally. Can run in parallel with phase 3 after phase 1 completes.

### Phase 3 — α(Q²) Running Cross-Check (INDEPENDENT VALIDATION)

Second slice of the same geometry at completely different energy scale. Can run in parallel with phase 2.

### Phase 4 — Symbolic Regression Confirmation (SANITY CHECK)

Data-driven search for the same functional form derived analytically. If the data-discovered form matches the derived form, high confidence.

### Phase 5 — Extended Dataset (ROBUSTNESS)

Deuterium, He⁺, higher-n hydrogen, full NIST HDEL up to n=200. Establishes generality.

### Phase 6 — Synthesis and Publication (DELIVERABLE)

Draft paper, figures, code release, peer review prep.

---

## 8. Task Specifications

### Phase 1: First-Principles Derivation

#### Task 1.1 — Formalize PRISM framework for computation

```yaml
task_id: P1-T1
agent: theoretician
human_in_the_loop: REQUIRED
inputs:
  - kip_madden_prism_notes.md (source material from Kip's prior work)
  - prism_framework_v7.0.4_draft.md
outputs:
  - prism_formal_spec.md (explicit postulates, notation, coordinate definitions)
  - prism_coordinate_diagram.svg
tools: [markdown_editor, svg_generator]
success_criteria:
  - Every variable has a type, range, and physical interpretation
  - Every postulate is stated without reference to "intuitively" or "obviously"
  - Coordinate transformations between 5D native and 4D Cartesian are explicit functions
failure_modes:
  - framework_ambiguous: escalate to Kip for clarification of specific postulate
  - framework_inconsistent: halt phase, issue anomaly report
estimated_tokens: 20K-40K
estimated_wall_time: 2-4 days (dominated by human review cycles)
```

#### Task 1.2 — Derive orbital wavefunction in 5D spiral basis

```yaml
task_id: P1-T2
agent: theoretician
human_in_the_loop: REQUIRED
depends_on: [P1-T1]
inputs:
  - prism_formal_spec.md
outputs:
  - derivations/5d_wavefunction.tex
  - derivations/4d_projection.tex
  - derivations/angular_momentum_mapping.tex
tools: [sympy, latex_renderer]
success_criteria:
  - 5D wavefunction ψ(n, ℓ, j, χ, r) explicitly written where χ is the 5th-dim coordinate
  - 4D projection recovers standard hydrogen wavefunction in appropriate limit
  - Angular momentum quantization emerges from compactification topology (not postulated)
failure_modes:
  - projection_does_not_reduce: framework is inconsistent with known QM — halt
  - quantization_requires_postulate: note as additional free parameter; continue but flag
estimated_tokens: 60K-120K
estimated_wall_time: 1-2 weeks
```

#### Task 1.3 — Derive s-state-specific correction (THE CENTRAL CALCULATION)

```yaml
task_id: P1-T3
agent: theoretician
human_in_the_loop: REQUIRED
depends_on: [P1-T2]
inputs:
  - derivations/5d_wavefunction.tex
outputs:
  - derivations/s_state_correction.tex
  - derivations/s_state_correction_formula.json
tools: [sympy, numerical_integration]
success_criteria:
  - Derive integral expression for s-state self-energy analog in native spiral basis
  - Integral is finite and well-defined (no renormalization handwaves)
  - Expression is explicit function of n with no free parameters beyond α
failure_modes:
  - integral_diverges: PRISM needs explicit regularization scheme — escalate
  - expression_requires_tuning: PRISM is not parameter-free at current specification — document and continue
estimated_tokens: 80K-150K
estimated_wall_time: 2-3 weeks
critical_path: TRUE
```

#### Task 1.4 — Numerically evaluate derived expression for n=1..5

```yaml
task_id: P1-T4
agent: computer
depends_on: [P1-T3]
inputs:
  - derivations/s_state_correction_formula.json
outputs:
  - predictions/prism_bethe_log_analog.csv
  - predictions/numerical_method_log.md
tools: [scipy.integrate, mpmath for high-precision]
success_criteria:
  - Values computed to 6 significant figures with documented error estimate
  - Numerical method (quadrature choice, convergence test) is documented
  - Cross-check using two independent methods agrees to 4+ sig figs
failure_modes:
  - integral_not_converging: increase precision, try alternative representation
  - values_diverge: return to P1-T3 for regularization
estimated_tokens: 10K-20K
estimated_wall_time: 1-2 days
```

#### Task 1.5 — Compare PRISM prediction to measured Bethe log

```yaml
task_id: P1-T5
agent: validator
depends_on: [P1-T4]
inputs:
  - predictions/prism_bethe_log_analog.csv
  - knowledge_base/bethe_log_literature.yaml (Drake & Swainson 1990)
outputs:
  - validation/phase1_verdict.md
  - validation/residual_comparison.csv
  - figures/phase1_comparison.png
tools: [statistical_tests, matplotlib]
success_criteria:
  - Comparison table with predicted vs measured for n=1..5
  - Relative error computed
  - Explicit verdict: VALIDATED (within 10%) / PARTIAL (within 50%) / FALSIFIED (off by >50% or wrong sign)
failure_modes: none — this is a reporting task
estimated_tokens: 5K-10K
estimated_wall_time: 4-8 hours
gate: TRUE
gate_condition: if verdict == FALSIFIED, halt all downstream phases pending Kip review
```

### Phase 2: Muonic Hydrogen Cross-Check

#### Task 2.1 — Fetch CREMA collaboration muonic hydrogen data

```yaml
task_id: P2-T1
agent: data_fetcher
depends_on: [P1-T5 == VALIDATED or PARTIAL]
inputs:
  - source: Pohl et al. Nature 466, 213 (2010) and follow-ups
  - source: Antognini et al. Science 339, 417 (2013)
outputs:
  - raw_data/muonic_h_lamb_shift.csv
  - raw_data/muonic_h_citations.bib
tools: [web_fetch, arxiv_mcp, pdf_extractor]
success_criteria:
  - Primary CREMA measurements of μH(2S-2P) transitions obtained
  - Uncertainties documented
  - Citation metadata preserved
estimated_tokens: 30K-50K
estimated_wall_time: 1-2 days
```

#### Task 2.2 — Apply PRISM-derived function to muonic system

```yaml
task_id: P2-T2
agent: computer
depends_on: [P1-T3, P2-T1]
inputs:
  - derivations/s_state_correction_formula.json
  - muon mass, muonic Bohr radius constants
outputs:
  - predictions/muonic_h_lamb_shift.csv
  - predictions/proton_radius_prediction.json
tools: [python]
success_criteria:
  - Predicted muonic Lamb shift computed
  - Predicted proton radius from muonic probe computed
  - If PRISM derivation couples to reduced mass via compactification depth, record coupling
estimated_tokens: 10K-20K
```

#### Task 2.3 — Validate against measured muonic Lamb shift and proton radius puzzle

```yaml
task_id: P2-T3
agent: validator
depends_on: [P2-T2]
inputs:
  - predictions/muonic_h_lamb_shift.csv
  - raw_data/muonic_h_lamb_shift.csv
  - knowledge_base/proton_radius_puzzle.yaml
outputs:
  - validation/phase2_verdict.md
  - figures/muonic_vs_electronic_proton_radius.png
success_criteria:
  - Comparison of predicted vs measured muonic Lamb shift with σ-difference
  - Explicit check: does PRISM predict the 4% electronic/muonic proton radius discrepancy?
  - Verdict: VALIDATED / PARTIAL / FALSIFIED
failure_modes: none — reporting task
estimated_tokens: 10K
gate: TRUE
```

### Phase 3: α(Q²) Running Cross-Check

#### Task 3.1 — Fetch α running data

```yaml
task_id: P3-T1
agent: data_fetcher
depends_on: [P1-T5]
inputs:
  - source: Jegerlehner compilation (α_had(M_Z²))
  - source: PDG review on electroweak fits
outputs:
  - raw_data/alpha_running.csv
  - raw_data/alpha_running_citations.bib
success_criteria:
  - α values at multiple Q² scales from low energy to M_Z
  - Systematic uncertainties documented
estimated_tokens: 30K
```

#### Task 3.2 — Derive α running from PRISM geometry

```yaml
task_id: P3-T2
agent: theoretician
human_in_the_loop: REQUIRED
depends_on: [P1-T1]
outputs:
  - derivations/alpha_running_from_geometry.tex
  - predictions/alpha_q2_prism.csv
success_criteria:
  - Derivation uses same compactification parameter as phase 1 (no new parameters)
  - Functional form for α(Q²) from geometry
failure_modes:
  - requires_new_parameter: PRISM doesn't unify these two observations — document and continue
estimated_tokens: 60K-100K
```

#### Task 3.3 — Validate α running prediction

```yaml
task_id: P3-T3
agent: validator
depends_on: [P3-T1, P3-T2]
outputs:
  - validation/phase3_verdict.md
  - figures/alpha_running_prism_vs_data.png
gate: TRUE
```

### Phase 4: Symbolic Regression Sanity Check

#### Task 4.1 — Configure PySR with PRISM operator basis

```yaml
task_id: P4-T1
agent: computer
depends_on: [P1-T5]
inputs:
  - v4_pipeline_residuals.csv (from prism_hydrogen_v4.py output)
  - operator_basis_config.yaml:
      allowed_operators: [+, -, *, /, log, sin, cos, exp]
      allowed_constants: [1, α, π, φ, n, ℓ, j]
      max_expression_complexity: 20
outputs:
  - pysr_fits/top_10_expressions.csv
  - pysr_fits/pareto_frontier.png
tools: [pysr (requires Julia)]
success_criteria:
  - 40+ iterations completed
  - Top expression has R² > 0.99 on training data
estimated_tokens: 15K
estimated_wall_time: 4-8 hours (mostly compute)
```

#### Task 4.2 — Compare discovered vs derived form

```yaml
task_id: P4-T2
agent: validator
depends_on: [P4-T1, P1-T3]
outputs:
  - validation/phase4_verdict.md
success_criteria:
  - Algebraic comparison of PySR top expression to derived expression
  - If equivalent (up to algebraic rearrangement), HIGH CONFIDENCE flag
  - If different, flag for critic review
estimated_tokens: 10K
```

### Phase 5: Extended Dataset

#### Task 5.1 — Fetch deuterium spectrum

```yaml
task_id: P5-T1
agent: data_fetcher
inputs:
  - source: NIST Handbook Deuterium table
outputs:
  - raw_data/deuterium_levels.csv
```

#### Task 5.2 — Fetch NIST HDEL high-n data

```yaml
task_id: P5-T2
agent: data_fetcher
inputs:
  - source: physics.nist.gov/hdel
outputs:
  - raw_data/hdel_hydrogen_n1_to_200.csv
note: HDEL CGI endpoint may require proxy workaround per sandbox experience
```

#### Task 5.3 — Fetch He⁺ (Z=2 hydrogenic) spectrum

```yaml
task_id: P5-T3
agent: data_fetcher
outputs:
  - raw_data/he_plus_levels.csv
```

#### Task 5.4 — Apply PRISM derived function across extended datasets

```yaml
task_id: P5-T4
agent: computer
depends_on: [P1-T3, P5-T1, P5-T2, P5-T3]
outputs:
  - predictions/extended_dataset_predictions.csv
  - figures/predictions_vs_measurements_all_systems.png
success_criteria:
  - Same functional form applied to all systems with only Z and mass varying
  - No system-specific tuning
```

#### Task 5.5 — Validate extended predictions

```yaml
task_id: P5-T5
agent: validator
depends_on: [P5-T4]
outputs:
  - validation/phase5_verdict.md
  - validation/robustness_summary.md
gate: TRUE
```

### Phase 6: Synthesis and Publication

#### Task 6.1 — Critic red-team pass

```yaml
task_id: P6-T1
agent: critic
depends_on: [all previous phases]
inputs:
  - all validation reports
  - all derivations
outputs:
  - red_team_report.md (alternative explanations, possible confounds, statistical concerns)
  - recommended_null_tests.md
tools: [literature_search, reasoning_chain]
success_criteria:
  - At least 3 alternative explanations considered
  - At least 2 specific falsification experiments suggested
estimated_tokens: 40K
```

#### Task 6.2 — Draft paper

```yaml
task_id: P6-T2
agent: reporter
human_in_the_loop: REQUIRED
depends_on: [P6-T1]
inputs: all artifacts
outputs:
  - paper_draft.tex
  - paper_draft.pdf
  - figures/publication_quality/*.pdf
tools: [latex, matplotlib]
success_criteria:
  - ~4000-6000 words
  - Abstract, intro, framework section, derivation section, results, discussion, conclusion
  - All figures at 300 DPI
  - Bibliography in arXiv-compatible format
estimated_tokens: 80K-150K
```

#### Task 6.3 — Reproducibility package

```yaml
task_id: P6-T3
agent: reporter
depends_on: [P6-T2]
outputs:
  - github_ready/
      - code/ (all pipeline scripts)
      - data/ (all fetched data with provenance)
      - derivations/ (all .tex and .json)
      - README.md (reproduce-from-scratch instructions)
      - LICENSE
      - CITATION.cff
success_criteria:
  - Fresh clone + single command reproduces all results
estimated_tokens: 15K
```

---

## 9. Handoff Contracts

Each task produces deliverables in specific file formats so downstream tasks don't need to re-parse prose:

```yaml
data_files: .csv with explicit header row; schema in adjacent .yaml
derivations: .tex for human reading; .json with extracted formulas for machine consumption
predictions: .csv with columns [system, n, l, j, quantity, predicted_value, uncertainty, method]
validation_reports: .md with required sections [summary, comparison_table, verdict, recommendations]
figures: .png for inline review, .pdf for publication
```

Every file includes a YAML frontmatter block with:
```yaml
generated_by: <agent_id>
generated_at: <ISO timestamp>
depends_on: [<list of input file hashes>]
spec_task_id: <P#-T#>
```

## 10. Escalation Rules

```yaml
automatic_escalation_to_human:
  - any_derivation_step_makes_non_first_principles_choice
  - predicted_value_differs_from_measured_by_>5_sigma_without_known_cause
  - framework_inconsistency_detected
  - data_source_returns_unexpected_format_3_times_in_a_row
  - token_budget_for_phase_exceeded_2x

pause_and_report (no escalation, but logged):
  - retry_with_backoff_succeeds_after_1-2_attempts
  - literature_value_has_known_superseding_revision
  - alternative_derivation_path_available

auto_proceed:
  - routine_data_fetch_and_parse
  - numerical_evaluation_of_validated_formulas
  - fit_convergence_within_tolerance
```

## 11. Human Checkpoints (Mandatory)

```yaml
checkpoint_1: after P1-T1 (framework formalization) — Kip approves before derivation begins
checkpoint_2: after P1-T3 (s-state derivation) — Kip reviews each step of the derivation
checkpoint_3: after P1-T5 (phase 1 verdict) — go/no-go decision for phases 2-5
checkpoint_4: after all validation phases — decision to proceed to publication
checkpoint_5: after P6-T2 (paper draft) — final review before any external release
```

## 12. Deliverables (Final)

```yaml
primary:
  - final_report.docx (executive summary + results)
  - paper_draft.pdf (publication-ready)
  - github_ready/ (full reproducibility package)

secondary:
  - all phase verdict reports (.md)
  - all derivations (.tex + .json)
  - all figures (.png + .pdf)
  - red_team_report.md
  - raw_data_audit.log

archive:
  - conversation transcripts from human checkpoints
  - decision log for each gate
  - token usage summary
```

## 13. Honest Limitations of This Plan

Tasks an agentic system **cannot fully automate** in this program:

1. **Theoretical derivations (P1-T2, P1-T3, P3-T2)**: Original theoretical physics work. An AI can propose, compute, and critique derivations but cannot substitute for human mathematical creativity at the current state of the art. Human-in-the-loop is non-negotiable here.

2. **Framework consistency judgment**: If the derivation appears to require a new postulate, the agent cannot decide whether that's acceptable — this is a framework-evolution decision only Kip can make.

3. **Scientific peer review simulation**: The critic agent can red-team, but cannot replicate domain-expert review. External physicist review is recommended before any public release.

Tasks an agentic system **can fully automate**:
- All data fetching, parsing, validation
- Numerical evaluation of established formulas
- Statistical fitting and model comparison
- Figure generation and report writing
- Literature lookup and citation formatting
- Symbolic regression (with human review of outputs)

## 14. Kill Criteria

This research program should be formally terminated (not just paused) if:

```yaml
- P1-T5 returns FALSIFIED and Kip determines framework cannot be rescued without becoming unfalsifiable
- More than 2 separate assumptions (Section 4) require escalation to "new postulate" status (framework becomes untestable)
- Required data is demonstrated to not exist at needed precision and cannot be obtained
- Six months elapse with no phase 1 completion
```

Termination is a legitimate outcome and documents a publishable negative result.

---

## Appendix A: Priors — Key Literature Values

```yaml
bethe_log_values:
  n_1: 2.984128556
  n_2: 2.811769893
  n_3: 2.767663612
  n_4: 2.749811840
  n_5: 2.740823727
  source: Drake & Swainson, Phys. Rev. A 41, 1243 (1990)

hydrogen_lamb_shift:
  value_mhz: 1057.845
  uncertainty_mhz: 0.009
  source: Lundeen & Pipkin, Phys. Rev. Lett. 46, 232 (1981)

muonic_hydrogen_lamb_shift:
  value_mev: 0.2065
  source: Antognini et al., Science 339, 417 (2013)

proton_radius_electronic:
  value_fm: 0.8775
  uncertainty_fm: 0.0051
  source: CODATA 2018

proton_radius_muonic:
  value_fm: 0.84087
  uncertainty_fm: 0.00039
  source: CREMA 2013

alpha_at_me:
  value: 0.0072973525643
  source: CODATA 2022

alpha_at_mz:
  value: 0.007816
  uncertainty: 0.000005
  source: Jegerlehner 2019
```

## Appendix B: Starting State (Already Complete)

```yaml
existing_artifacts:
  - prism_hydrogen_v1.py: baseline pipeline with hand-curated data
  - prism_hydrogen_v2.py: fine-structure + BIC model selection
  - prism_hydrogen_v3.py: live NIST fetch, Lamb shift 99.96% literature
  - prism_hydrogen_v4.py: reduced-mass corrected, clean QED extraction
  - prism_research_summary.docx: human-readable summary
  - kip_madden_prism_framework_notes: in Kip's possession, to be supplied to P1-T1

v4_current_findings:
  qualitative_prediction_status: CONFIRMED (s-states feel extra coupling, pattern scales correctly)
  quantitative_ansatz_status: FAILED (fit coefficient wrong sign and ~4.5x off from Bethe log)
  phi_modulation_status: MARGINAL (2.7σ, neither confirmed nor ruled out)
  net_interpretation: Framework geometric intuition is right; guess at functional form was wrong
```

## Appendix C: Spec Self-Test

Before dispatching to agents, the orchestrator should verify this spec passes:

```yaml
self_test_questions:
  - Can the mission be evaluated objectively? YES (success_criteria is binary)
  - Can each task run with only its declared inputs? TO BE VERIFIED per task
  - Is every agent role bounded? YES (explicit responsibilities)
  - Is every tool dependency explicit? YES (tool manifest in section 6)
  - Are escalation paths defined for every failure mode? YES (section 10)
  - Is there a kill criterion? YES (section 14)
  - Is human-in-the-loop explicit where needed? YES (marked per task)
  - Are deliverables concrete? YES (section 12)
```

---

*End of spec. Version-controlled as `prism_research_plan_v1.0.md`. Orchestrator starts at Phase 1, Task 1.1 upon Kip's checkpoint approval.*
