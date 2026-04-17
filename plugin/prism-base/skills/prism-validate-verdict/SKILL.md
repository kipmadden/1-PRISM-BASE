---
name: prism-validate-verdict
description: Render a phase verdict (VALIDATED / PARTIAL / FALSIFIED) by comparing PRISM predictions against literature values. Used by prism-validator at every gate task (P1-T5, P2-T3, P3-T3, P4-T2, P5-T5). Writes verdict markdown, residuals CSV, and comparison plot.
---

# PRISM Phase Verdict Rendering

You are a gatekeeper. Your verdict decides whether the research program proceeds, refines, or halts. Report what the data says, not what the framework hopes it says.

## Verdict criteria

These are the default bands. Per-task success_criteria in the spec may tighten them.

| Verdict | Threshold |
|---|---|
| **VALIDATED** | All predictions within 10% of literature, consistent sign, within any stated uncertainty envelope |
| **PARTIAL** | All within 50%, correct qualitative pattern, but numerical match incomplete |
| **FALSIFIED** | Any off by >50%, wrong sign anywhere, or missed qualitative pattern |

## Workflow

1. Load the predictions CSV (from prism-computer) and the corresponding literature YAML (from prism-librarian).
2. Join by key columns (system + n + l + j). Every prediction row must have a literature match or be flagged as extrapolation.
3. Compute per-row: `predicted, uncertainty_pred, measured, uncertainty_meas, abs_error, rel_error_pct, sigma`.
4. Run `scripts/validate_vs_literature.py --pred <csv> --lit <yaml> --out <dir>`.
5. Render the verdict markdown using the mandatory four-section template below.

## Mandatory verdict template

```markdown
---
generated_by: prism-validator
generated_at: <timestamp>
spec_task_id: <P#-T#>
depends_on: [<sha256(predictions)>, <sha256(literature)>]
---

# Phase <n> Verdict — <date>

## Summary

<one paragraph. Lead with the verdict. No hedging. E.g.:
"Phase 1 PRISM s-state correction is VALIDATED: predicted Bethe-log analogs for n=1..5
agree with literature (Drake & Swainson 1990) to within 4% across all five levels, with
no tuning. The derivation is parameter-free beyond α.">

## Comparison Table

| n | Predicted | ± | Measured | ± | |err| | rel %. | σ |
|---|---|---|---|---|---|---|---|
| 1 | ... | ... | ... | ... | ... | ... | ... |
| ... |

## Verdict

**<VALIDATED | PARTIAL | FALSIFIED>** — <one-sentence tied to success_criteria>

## Recommendations

- <Action item for orchestrator: proceed to phase N / halt / escalate>
- <Flag for critic: anomaly needing red-team review>
- <Note for reporter: caveat to include in final paper>
```

## Sign-convention handling

Some PRISM derivations may produce the opposite overall sign from standard QED by convention (e.g., binding energy counted positive vs negative). If ALL five predictions have a consistent sign flip, document the convention and pass. If signs are MIXED across n, that is not a convention difference — that's a failure. Report FALSIFIED.

## Escalation triggers (spec §10)

Flag for immediate user escalation if:
- Any residual exceeds 5σ
- sigma column is computable for >50% of rows and the median sigma > 3
- Predictions fall outside the literature's stated range by 10× or more

## Outputs

1. `working_dir/validation/<phase>_verdict.md` — the verdict document.
2. `working_dir/validation/<phase>_residuals.csv` — per-row residuals for the critic.
3. `working_dir/figures/<phase>_comparison.png` + `.pdf` — predicted-vs-measured scatter with 1:1 line and residual subplot.
4. Update `working_dir/phase_status.json` with the verdict.
