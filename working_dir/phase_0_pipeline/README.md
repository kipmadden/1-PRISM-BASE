---
generated_by: prism-orchestrator
generated_at: 2026-04-17T00:00:00Z
spec_task_id: bootstrap
depends_on: []
spec_version: "1.0"
artifact_type: phase_index
---

# Phase 0 — Foundation pipeline

Phase 0 is **PRE_COMPLETE** per spec. Artifacts placed here on bootstrap:

| File | Status | Notes |
|------|--------|-------|
| `prism_hydrogen_v3.py` | Present | Latest available pipeline in user project root. Spec referenced `v4`; only `v3` exists at bootstrap time. |
| `prism_hydrogen_v4.py` | **MISSING** | Mentioned by spec as the artifact validating the qualitative PRISM prediction (s-states feel extra coupling). If v4 was produced separately, place it here for reference. |

## Phase 0 finding (per phase_status.json)

> Qualitative PRISM prediction confirmed (s-states feel extra coupling). Quantitative
> ansatz failed (wrong sign, ~4.5x off Bethe log). Pipeline runs end-to-end on live
> NIST data.

This is the launch state for Phase 1 — the first-principles derivation must produce
a closed-form s-state correction whose absolute values match Drake & Swainson (1990).
