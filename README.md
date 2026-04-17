# PRISM BASE

### A pre-registered research program for testing whether a five-dimensional logarithmic-spiral worldline hypothesis can reproduce the hydrogen spectrum

[![Phase](https://img.shields.io/badge/phase-1%20(Hydrogen%20Gate)-orange)](#research-program-structure)
[![Status](https://img.shields.io/badge/status-pre--verdict-yellow)](#current-status)
[![Framework](https://img.shields.io/badge/framework-Claude%20Code%20plugin-6b46c1)](#implementation-as-a-claude-code-plugin)
[![License](https://img.shields.io/badge/license-proprietary-lightgrey)](#license)

---

## Abstract

We introduce **PRISM** (Projected Reduction of an Intrinsic Spiral Manifold), a
geometric reinterpretation of non-relativistic quantum mechanics in which the
electron bound-state worldline is a five-dimensional logarithmic spiral whose
radial scaling rate coincides with the fine-structure constant α, and whose
compactification length in the fifth (spacelike) axis is fixed by a closure
condition to 2π/α. The four-dimensional wavefunction of standard quantum
mechanics is posited to emerge as the Jacobian-weighted projection of this
spiral onto the (1,3) Minkowski slice. The hypothesis is concretely
falsifiable: because no free parameters remain after the identification
k ≡ α, the framework must either reproduce the hydrogen Bethe logarithms of
Drake and Swainson (1990) to approximately three decimal places or be rejected.

This repository is the **research infrastructure** that conducts that test.
It is implemented as a Claude Code plugin containing a 17-role, 6-phase,
pre-registered research program with five human-in-the-loop checkpoints and
explicit, pre-committed kill criteria. The program has completed Phase 0
(qualitative confirmation, quantitative ~4.5× miss) and is active in Phase 1.

**Author.** Kip Madden, Cosapient (kipmadden@cosapient.com).
**Status at time of publication.** Pre-verdict. Awaiting cp1 framework
approval, after which Phase 1 (P1-T3 through P1-T5) will proceed.

---

## Plain-language summary

If you are not a physicist, here is what this repository is about.

There is a number in physics called the **fine-structure constant**, usually
written α. Its numerical value, roughly 1 divided by 137, governs how
strongly electrons interact with light and is woven into nearly every
calculation involving atoms. It appears in many places, but its *origin* is
unknown: physicists measure it, they do not derive it.

The PRISM hypothesis proposes that α has a geometric meaning. Imagine drawing
a **logarithmic spiral**, the shape of a nautilus shell, where every turn
widens at the same proportional rate. PRISM proposes that the electron's
trajectory, when viewed in a five-dimensional space (the usual four of
spacetime plus one "rolled-up" extra dimension), is literally such a spiral,
and that α is the *rate* at which it winds. What we observe as quantum
mechanics would then be the shadow of this spiral cast onto our lower-
dimensional world — much as a rotating coin throws a flat oscillating line on
a wall behind it.

The attractive feature of this idea is that it makes a very hard prediction
with **no adjustable knobs**. Once α is fixed (we know its value to twelve
decimal places), the framework either correctly predicts the fine-grained
energy levels of hydrogen — the simplest atom — or it is wrong. There is no
room to tune.

The hydrogen energy levels are known to extraordinary precision thanks to
decades of experimental and computational work. The specific numbers this
project must reproduce are called the **Bethe logarithms**, calculated to
better than one part in a million by Drake and Swainson (1990). If PRISM
cannot hit those numbers, PRISM is falsified.

This repository does not argue that PRISM is correct. It provides the
machinery to find out, and — importantly — it commits in advance to the
conditions under which the hypothesis will be abandoned. That machinery is an
*agentic* research program: AI subagents take on defined scientific roles
(theoretician, calculator, validator, critic) and the output of each step is
archived with its provenance, so the trail of reasoning is auditable by any
reader afterward, whether the outcome is positive or negative.

---

## 1. Current status

| phase | description                                          | status        |
|-------|------------------------------------------------------|---------------|
| 0     | Foundation — prototype derivations                   | complete      |
| 1     | Hydrogen gate — Bethe logarithm reproduction         | **active**    |
| 2     | Relativistic spectrum — Lamb shift, fine structure   | not started   |
| 3     | α running from low to high energy scale              | not started   |
| 4     | Symbolic regression cross-check (optional)           | not started   |
| 5     | External validation — muonic H, positronium, He⁺     | not started   |
| 6     | Report and manuscript preparation                    | not started   |

**Phase 0 outcome.** A sequence of four ansatz-driven prototype derivations
(`prism_hydrogen_v1.py` through `v4.py`) produced a qualitative confirmation
of the PRISM prediction that s-states (ℓ = 0) receive an additional
self-energy-like correction concentrated at small r, while states of nonzero
angular momentum do not. Quantitatively, the final (v4) prototype fell short
of the Drake–Swainson (1990) Bethe logarithms by a factor of approximately
4.5. The framework is therefore neither confirmed nor rejected at Phase 0; it
is rendered interesting and testable.

**Phase 1.** The P1-T1 task (framework formalization) raised seven open
theoretical questions, documented in `working_dir/kip_madden_prism_notes.md`
together with direct, postulate-level responses. The next milestone is
checkpoint cp1 (framework acceptance), followed by P1-T3 (symbolic derivation
of the Bethe logarithm) and the decisive gate at P1-T5 (numerical
comparison to Drake–Swainson 1990).

---

## 2. Theoretical overview

### 2.1 Postulate set

The framework is stated in six postulates:

- **P-1 (Geometry).** Spacetime is a direct product of (1,3) Minkowski space
  with one compactified spacelike axis χ of finite circumference L_χ. The
  signature is (+, −, −, −, −).
- **P-2 (Worldline form).** The bound-state electron worldline in the (x,y)
  plane of the 4D slice is a logarithmic spiral:
  r(θ) = r₀ · exp(k · θ).
- **P-3 (Geometric interpretation of α).** The spiral growth rate k is
  identified with the fine-structure constant at the electron rest-mass
  scale: k ≡ α(m_e).
- **P-4 (χ–θ coupling).** The compact coordinate winds linearly with the
  spiral angle modulo L_χ: χ(θ) = θ mod L_χ.
- **P-5 (Closure condition).** One revolution of the spiral corresponds to
  exactly one full traversal of the compact circle; combined with P-3 this
  yields L_χ = 2π / α. This is a derived consequence, not an independent
  postulate.
- **P-6 (Projection).** The observable 4D wavefunction is the projection of
  the 5D worldline weighted by the Jacobian
  J = k · r₀³ · exp(3kθ) · sin(φ_pol), where φ_pol is the polar angle in the
  embedding.

### 2.2 Derived consequences (not postulated)

- The enhancement of self-energy-like corrections for ℓ = 0 states follows
  from the interaction between the exp(3kθ) Jacobian factor and the
  non-vanishing amplitude of s-state wavefunctions at small r. States with
  ℓ ≥ 1 are suppressed at small r by the centrifugal barrier and therefore do
  not couple to this enhancement.
- Scale dependence of α (its "running") is predicted as a consequence of
  probing the spiral at different radii, not as a postulate.
- The Euler–Mascheroni constant γ is expected to appear in the regularization
  of the small-r integral, in a manner consistent with its appearance in the
  standard QED Bethe-log expression.

### 2.3 Explicit non-postulates

- **The golden ratio φ is not a postulate of PRISM.** Log-spirals in
  biological systems are often associated with φ because of five-fold
  symmetry; atomic orbitals are not five-fold symmetric, and the PRISM
  growth rate (k = α ≈ 7.3 × 10⁻³) is nowhere near log(φ) ≈ 0.481.
- **The s-state enhancement is not postulated.** If the P1-T3 derivation
  required it as an independent axiom, this would constitute a kill
  criterion.

### 2.4 Falsifiability

The identification k ≡ α leaves no free parameter in the prediction of
single-quantum-number observables. Concretely, the predicted Bethe
logarithm β(n,s) for n = 1..5 must reproduce the values of Drake and Swainson
(1990):

| n | β(n,s) Drake–Swainson (1990) |
|---|------------------------------|
| 1 | 2.984128556                  |
| 2 | 2.811769893                 |
| 3 | 2.767663612                  |
| 4 | 2.749811840                  |
| 5 | 2.740823727                  |

Target precision at the P1-T5 gate is on the order of 10⁻³ per value. Mixed-
sign deviations are automatically scored as FALSIFIED; consistent-sign
deviations of small magnitude may be scored PARTIAL pending critic review.

---

## 3. Research program structure

The program is specified in [prism_research_plan_v1.0.md](prism_research_plan_v1.0.md)
and implemented through seventeen named roles, of which nine are realized as
distinct AI subagents in [plugin/prism-base/agents/](plugin/prism-base/agents/):

| role            | responsibility                                            |
|-----------------|-----------------------------------------------------------|
| Orchestrator    | Task sequencing, gate enforcement, state transitions      |
| Theoretician    | Symbolic derivation, one logical step per session         |
| Computer        | Numerical evaluation, cross-checked                       |
| Validator       | Verdict generation against literature                     |
| Critic          | Structured red-team review; counter-hypothesis search     |
| Data Fetcher    | Retrieval of NIST, CREMA, PDG references                  |
| Parser          | Conversion of raw tabular inputs to canonical CSV         |
| Reporter        | Composition of `final_report.docx` and manuscript draft   |
| Librarian       | Enforcement of the handoff contract; artifact archival    |

### 3.1 Human-in-the-loop checkpoints

| id  | gate                                             | triggered after                      |
|-----|--------------------------------------------------|--------------------------------------|
| cp1 | Framework acceptance                             | `theoretical_foundation.md`          |
| cp2 | Derivation mid-course correction                 | mid P1-T3                            |
| cp3 | Phase 1 verdict approval                         | after P1-T5                          |
| cp4 | Cross-check validation complete                  | after Phases 2 and 3                 |
| cp5 | Manuscript approval                              | before Phase 6 release               |

### 3.2 Pre-committed kill criteria

The following conditions halt the program. They are fixed in the
specification and cannot be softened during execution:

- P1-T5 returns FALSIFIED with no rescue that preserves the postulate count;
- A proposed rescue requires more than one additional postulate;
- A required auxiliary measurement exceeds current experimental precision and
  is therefore untestable;
- Six months of calendar time elapse without a Phase 1 verdict.

When any of these conditions is detected, the responsible agent writes an
entry to [working_dir/escalations.md](working_dir/escalations.md) and exits without advancing state. The
orchestrator will not dispatch further tasks until a human renders a
`/prism-checkpoint <id> reject` decision or annotates the escalation file.

### 3.3 Handoff contract

Every artifact carries metadata. Text artifacts (`.md`, `.tex`, `.yaml`) use
inline YAML frontmatter; binary and tabular artifacts (`.csv`, `.json`,
`.pdf`) carry a sibling `.meta.yaml` sidecar. Required fields on every
artifact are:

- `generated_by` — the producing agent
- `generated_at` — ISO-8601 UTC timestamp
- `spec_task_id` — e.g. `P1-T3`
- `depends_on` — upstream artifact paths

Predictions CSVs must carry the canonical columns:
`system, n, l, j, quantity, predicted_value, uncertainty, method`.

[plugin/prism-base/scripts/verify_handoff.py](plugin/prism-base/scripts/verify_handoff.py)
walks the working directory and exits non-zero if any artifact is missing
frontmatter, missing a sidecar, or missing a required field. The orchestrator
runs this check before every phase advance.

---

## 4. Implementation as a Claude Code plugin

The orchestration layer is packaged as a Claude Code plugin
([plugin/prism-base/.claude-plugin/plugin.json](plugin/prism-base/.claude-plugin/plugin.json)).
Choice of Claude Code — rather than, for example, a standalone Python
pipeline — is motivated by three considerations:

1. Each role must be able to apply judgment to open-ended inputs (reading a
   partially-completed derivation, recognizing a postulate mismatch, framing
   a rescue hypothesis). These are not amenable to deterministic
   implementation.
2. The reasoning of each agent must be **inspectable** after the fact. Plugin
   subagents produce textual artifacts that can be read, critiqued, and
   cited.
3. The program benefits from heterogeneous model assignments: the
   Theoretician and Critic roles are assigned to Opus-class models; the
   Orchestrator, Computer, Validator, and Reporter to Sonnet-class; the
   Librarian and Data Fetcher to Haiku-class. See
   [plugin/prism-base/agents/](plugin/prism-base/agents/) for per-agent
   model bindings.

Non-agentic components (data retrieval, CSV parsing, BIC model competition,
formula evaluation, contract verification) are implemented as standalone
Python scripts under [plugin/prism-base/scripts/](plugin/prism-base/scripts/)
and invoked through `Bash`. They do not require MCP servers beyond the
filesystem.

---

## 5. Repository structure

```
1 PRISM BASE/                                       repo root
├── README.md                                       this file
├── prism_research_plan_v1.0.md                     authoritative program specification
├── prism_hydrogen_v3.py                            Phase 0 prototype (reference)
├── working_dir/                                    program state and artifacts
│   ├── current_state.json                          live orchestrator state
│   ├── phase_status.json                           phase and task progress
│   ├── audit.log                                   append-only agent dispatch log
│   ├── kip_madden_prism_notes.md                   PI framework notes
│   ├── derivations/                                symbolic derivations
│   │   ├── prism_formal_spec.md                    Theoretician's formal translation
│   │   └── prism_coordinate_diagram.svg
│   ├── knowledge_base/                             literature reference values
│   ├── predictions/ deliverables/ figures/ ...     task outputs by phase
│   └── checkpoints/                                human-in-the-loop decisions
└── plugin/                                         Claude Code plugin wrapper
    ├── prism-base-0.1.0.plugin                     packaged bundle
    └── prism-base/                                 plugin source
        ├── .claude-plugin/plugin.json              Claude Code manifest
        ├── agents/                                 9 subagents (per research program role)
        ├── skills/                                 8 procedures invoked by the agents
        ├── commands/                               6 slash commands (prism-init, -next, ...)
        ├── scripts/                                Python helpers (non-agentic)
        │   ├── fetch_nist.py                       NIST/CREMA retrieval with caching
        │   ├── parse_nist_html.py                  HTML to canonical CSV
        │   ├── bic_rank.py                         Bayesian information criterion ranking
        │   ├── evaluate_derived_formula.py         SymPy formula to predictions CSV
        │   ├── validate_vs_literature.py           Verdict engine
        │   ├── verify_handoff.py                   Handoff-contract enforcement
        │   └── run_pysr.py                         Optional PySR symbolic regression
        └── templates/                              Seed files copied on /prism-init
            ├── current_state.json
            ├── phase_status.json
            ├── source_urls.yaml
            ├── operator_basis_config.yaml
            ├── handoff_contract_template.yaml
            └── knowledge_base/
                ├── literature_values.yaml          Drake-Swainson, CREMA, CODATA 2022
                └── README.md
```

---

## 6. Reproducing the program

### 6.1 Installation

Place this repository at a Claude Code plugins path:

```
~/.claude/plugins/prism-base/               (macOS, Linux)
%USERPROFILE%\.claude\plugins\prism-base\   (Windows)
```

Launch Claude Code pointed at the plugin directory:

```
claude --plugin-dir ~/.claude/plugins/prism-base
```

Python dependencies for the helper scripts:

```
pip install pyyaml sympy scipy mpmath pandas numpy python-docx --break-system-packages
```

Optional, for the Phase 4 symbolic-regression cross-check:

```
pip install pysr --break-system-packages
# Requires Julia >= 1.9 on PATH, or PySR will install it on first use.
```

If Julia is not available, Phase 4 exits cleanly with status 77 (skipped)
and the program continues. P4-T1 is optional; P1-T5 is the decisive gate.

### 6.2 Bootstrapping the working directory

From a fresh program root (a directory outside of synchronised cloud
storage is recommended on Windows, since filter-driver overhead on
OneDrive can slow agent workflows by a factor of five to ten):

```
/prism-init       Bootstrap working_dir from templates
/prism-status     Verify state is consistent
```

### 6.3 Operating rhythm

The program is designed to execute one task per session:

```
/prism-status                         Check current phase and next eligible task
/prism-next                           Dispatch the next task
...                                   Task runs; artifact lands in working_dir/
/prism-checkpoint cp<n> approve       Only at human-in-the-loop gates
```

The orchestrator selects the appropriate subagent based on
`phase_status.json` and the research plan specification.

---

## 7. Theoretical background documents

Three documents, in order of increasing formality, accompany this repository:

1. **[prism_research_plan_v1.0.md](prism_research_plan_v1.0.md)** (program
   root) — the authoritative specification of the research program. Defines
   all seventeen roles, each task, each artifact contract, and the kill
   criteria.
2. **[working_dir/kip_madden_prism_notes.md](working_dir/kip_madden_prism_notes.md)**
   — principal-investigator framework notes. First-person exposition of the
   core intuitions, the history of prior iterations (v1 through v4), and
   direct responses to the seven open questions raised by the Theoretician at
   P1-T1.
3. **[working_dir/derivations/prism_formal_spec.md](working_dir/derivations/prism_formal_spec.md)**
   — the Theoretician's formal translation of the postulate set into symbolic
   form, including the 5D→4D coordinate transformation and the Jacobian
   derivation.

Readers interested in **what PRISM predicts** should begin with (2).
Readers interested in **how it is being tested** should begin with (1).

---

## 8. Key references

- Drake, G. W. F., and Swainson, R. A. (1990). Bethe logarithms for hydrogenic
  atoms. *Physical Review A* 41 (3), 1243–1246.
- Lundeen, S. R., and Pipkin, F. M. (1981). Measurement of the Lamb shift in
  hydrogen, n = 2. *Physical Review Letters* 46 (4), 232–235.
- Pohl, R. et al. [CREMA collaboration] (2010). The size of the proton.
  *Nature* 466, 213–216.
- Tiesinga, E., Mohr, P. J., Newell, D. B., and Taylor, B. N. (2024). CODATA
  recommended values of the fundamental physical constants: 2022. *Reviews of
  Modern Physics* 96, 025002.
- Bethe, H. A., and Salpeter, E. E. (1957). *Quantum Mechanics of One- and
  Two-Electron Atoms*. Springer-Verlag.

Full attribution of literature values is maintained in
[plugin/prism-base/templates/knowledge_base/literature_values.yaml](plugin/prism-base/templates/knowledge_base/literature_values.yaml).

---

## 9. Citation

```
Madden, K. (2026). PRISM BASE: A pre-registered research program for testing
the 5D logarithmic-spiral hypothesis on the hydrogen spectrum. Cosapient
Technical Report. [verdict forthcoming]
```

A BibTeX entry will be provided upon resolution of Phase 1.

---

## 10. License

Proprietary. The orchestration infrastructure, agent specifications, and
helper scripts are authored by Kip Madden (Cosapient) and distributed under
a proprietary license pending the outcome of Phase 1. Inquiries, including
academic collaboration and reproduction requests, may be directed to
kipmadden@cosapient.com.

The underlying PRISM theory and the Phase 0 prototype code
(`prism_hydrogen_v1.py` through `v4.py`) are authored separately and are not
covered by the plugin's license.

---

## 11. Acknowledgments

The orchestration design benefits from the Claude Code plugin architecture
provided by Anthropic. Role assignments by model tier (Opus for Theoretician
and Critic, Sonnet for Orchestrator / Computer / Validator / Reporter, Haiku
for Librarian and Data Fetcher) follow the guidance in the Claude Code
documentation and are specified per-agent in
[plugin/prism-base/agents/](plugin/prism-base/agents/).

Hydrogen-spectrum reference data follow the National Institute of Standards
and Technology Atomic Spectra Database, the *Handbook of Basic Atomic
Spectroscopic Data* (NIST), and the CODATA 2022 adjustment. Drake and
Swainson (1990) remains the definitive source for hydrogenic Bethe logarithms
at the precision relevant to this work.

---

*This README will be updated at each checkpoint. A FALSIFIED verdict at
cp3 will result in publication of the artifact trail as a negative result.*
