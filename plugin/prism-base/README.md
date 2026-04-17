# prism-base

**PRISM Theory Validation Program — agentic orchestration for Claude Code.**

This plugin implements the `prism_research_plan_v1.0` specification: a 17-agent-role-addressable, 6-phase research program to test whether a 5D logarithmic-spiral worldline hypothesis reproduces the hydrogen spectrum to the precision of Drake & Swainson 1990 Bethe logarithms. It provides the orchestration layer (9 subagents, 8 skills, 6 slash commands, 7 helper scripts) plus seeded templates for working-directory state, knowledge base, and handoff contracts.

Phase 0 (Foundation) is **already complete** from prior work: `prism_hydrogen_v1–v4.py` confirmed the qualitative PRISM prediction (s-states feel extra coupling) but failed quantitatively (wrong sign, ~4.5× off). Phase 1 is the critical-path gate. P1-T5 is the live/die decision for the whole program.

---

## What's in the box

```
prism-base/
├── .claude-plugin/plugin.json          # manifest
├── agents/                             # 9 subagents (one per role in spec §5)
│   ├── prism-orchestrator.md           #   sequences phases, enforces gates
│   ├── prism-data-fetcher.md           #   NIST / CREMA / PDG retrieval
│   ├── prism-parser.md                 #   raw HTML/CGI → structured CSV
│   ├── prism-theoretician.md           #   (opus) symbolic derivation, one step/turn
│   ├── prism-computer.md               #   numerical evaluation with cross-checks
│   ├── prism-validator.md              #   VALIDATED / PARTIAL / FALSIFIED verdicts
│   ├── prism-critic.md                 #   red-team alternatives and null tests
│   ├── prism-reporter.md               #   final_report.docx / paper_draft.tex
│   └── prism-librarian.md              #   (haiku) immutable literature store
├── skills/                             # 8 procedures the agents invoke
│   ├── prism-orchestrate/              #   the top-level state machine
│   ├── prism-handoff-contract/         #   YAML frontmatter / sidecar enforcement
│   ├── prism-derive-s-state/           #   P1-T3 critical path (opus)
│   ├── prism-fetch-nist/               #   proxy-safe NIST URLs + retry policy
│   ├── prism-bic-rank/                 #   BIC model competition
│   ├── prism-validate-verdict/         #   mandatory 4-section verdict template
│   ├── prism-pysr-regression/          #   Julia/PySR driver (P4-T1, skippable)
│   └── prism-red-team/                 #   structured counter-hypothesis review
├── commands/                           # 6 slash commands
│   ├── prism-init.md                   #   /prism-init     bootstrap working_dir
│   ├── prism-status.md                 #   /prism-status   read-only status block
│   ├── prism-next.md                   #   /prism-next     dispatch next task
│   ├── prism-checkpoint.md             #   /prism-checkpoint cp1..cp5 decisions
│   ├── prism-phase.md                  #   /prism-phase N  jump with prerequisites
│   └── prism-report.md                 #   /prism-report   interim status .docx
├── scripts/                            # pure-Python helpers (no Julia required
│   ├── fetch_nist.py                   #   except run_pysr.py)
│   ├── parse_nist_html.py
│   ├── bic_rank.py
│   ├── evaluate_derived_formula.py
│   ├── validate_vs_literature.py
│   ├── verify_handoff.py
│   └── run_pysr.py
└── templates/                          # copied to working_dir/ on /prism-init
    ├── current_state.json
    ├── phase_status.json
    ├── source_urls.yaml
    ├── operator_basis_config.yaml
    ├── handoff_contract_template.yaml
    └── knowledge_base/
        ├── literature_values.yaml       # Bethe logs, Lamb shifts, α running
        └── README.md
```

---

## Install (Claude Code)

1. Copy this folder — or the `.plugin` archive — into your Claude Code plugins location. For a user-scoped install that's `~/.claude/plugins/prism-base/`.
2. Restart Claude Code (or reload plugins).
3. `cd` into the directory you want to use as the PRISM program root — this is where `working_dir/` will be created.
4. Run `/prism-init`. This copies the templates into `working_dir/` and sets `initialized_at` in `current_state.json`.
5. Verify with `/prism-status`.

Python dependencies the helper scripts expect:

```
pip install pyyaml sympy scipy mpmath pandas numpy python-docx --break-system-packages
```

Optional for Phase 4 (symbolic regression):

```
pip install pysr --break-system-packages
# PySR will install Julia on first use, OR have Julia >= 1.9 on PATH already.
```

---

## How to run the program

The expected operating rhythm is one task per session, with the orchestrator driving:

```
/prism-status          # see where we are
/prism-next            # dispatch the eligible task; orchestrator picks the agent
# ... task runs ...
# review artifact under working_dir/, optionally give feedback
/prism-checkpoint cp1 approve   # at human-in-the-loop checkpoints only
```

The five human-in-the-loop checkpoints (spec §11) are:

| id  | gate                                             | when |
|-----|--------------------------------------------------|------|
| cp1 | Framework acceptance                             | after `theoretical_foundation.md` |
| cp2 | Derivation mid-course correction                 | inside P1-T3 |
| cp3 | Phase 1 verdict approval                         | after P1-T5 |
| cp4 | Cross-check validation complete                  | after Phases 2 & 3 |
| cp5 | Paper-draft approval                             | before Phase 6 release |

Kill criteria (spec §14) are enforced in `prism-orchestrate/SKILL.md` and will halt the program automatically if:

- P1-T5 returns FALSIFIED with no rescue, OR
- A rescue move would require introducing >1 new postulate, OR
- A required measurement exceeds current experimental precision, OR
- 6 months of wall time pass without Phase 1 verdict.

---

## MCP assumption

This plugin assumes you have **filesystem MCP only**. All data fetching goes through `scripts/fetch_nist.py` (Python `requests` via Bash), not `web_fetch`/`web_search`. Endpoints known to be blocked by sandbox proxies (NIST ASD CGI, HDEL CGI) are flagged `proxy_safe: false` in `source_urls.yaml`; the data fetcher falls back to the static Handbook tables which remain reliable.

If you later add MCPs for ArXiv, GitHub, or a Python executor, the orchestrator does not need changes — the data fetcher and parser agents will transparently use them.

---

## Handoff contract

Every artifact the pipeline produces carries metadata (see `templates/handoff_contract_template.yaml`). Text artifacts (`.md`, `.tex`, `.yaml`) use inline YAML frontmatter; binary/tabular artifacts (`.csv`, `.json`, `.pdf`) carry a `.meta.yaml` sidecar. `scripts/verify_handoff.py` enforces this; the orchestrator runs it before every phase advance.

Required fields on every artifact:
`generated_by`, `generated_at`, `spec_task_id`, `depends_on`.

Predictions CSVs MUST carry columns:
`system, n, l, j, quantity, predicted_value, uncertainty, method`.

---

## Kill switch & escalation

When an agent encounters a situation that meets spec §14 kill criteria, it writes an escalation entry to `working_dir/escalations.md` and exits without advancing the state. The orchestrator will refuse `/prism-next` until you resolve it — either with a `/prism-checkpoint <id> reject` (program halts) or by editing the escalation file to note a resolution.

---

## Authorship

Principal: Kip Madden (kipmadden@cosapient.com).
Plugin license: Proprietary. PRISM theory and Phase 0 code authored separately.
Source spec: `prism_research_plan_v1.0.md`.
