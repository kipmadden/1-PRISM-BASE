---
description: Compile the current PRISM research state into a human-readable status report. Reads all verdicts, derivations, and predictions; produces a Word document summary at working_dir/deliverables/status_report_<date>.docx.
---

# Compile PRISM Status Report

Invoke the `prism-reporter` subagent with context:
- This is an **interim** status report, not the final paper draft (which requires P6-T2 and cp5_paper_draft).
- Scope: summarize current state across all phases, whether pending, in progress, or verdict-complete.
- Audience: Kip (principal) and any internal reviewer.
- Format: Word document using the docx skill.
- Length target: 4-8 pages.

## Required sections

1. **Executive Summary** — one paragraph. Verdict count, current phase, headline result.
2. **Phase-by-phase status** — for each phase, a callout with status (PENDING / IN PROGRESS / COMPLETE) and verdict if complete.
3. **Critical path** — where is P1-T5? What did it return?
4. **Open escalations** — anything from `working_dir/escalations.md` still unresolved.
5. **Deliverables to date** — listed artifacts with paths.
6. **Next actions** — ranked by value, drawn from the spec's §8 remainder.
7. **Honest caveats** — which success criteria are met, which are not, which are open questions.

## Guardrails

- This is not the paper draft. Do not present results as publication-ready unless Phase 6 is complete and cp5 is approved.
- Use the docx skill to produce a styled document with the convention established in `prism_basis_research_summary_v1.docx` (indigo headings, callouts, tables).
- Name the file `status_report_<YYYY-MM-DD>.docx` and place in `working_dir/deliverables/`.
- After writing, print the file path so the user can open it directly.
