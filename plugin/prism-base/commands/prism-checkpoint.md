---
description: Record a human checkpoint approval (or rejection) per spec §11. Five mandatory checkpoints gate the program; this command writes Kip's decision into working_dir/checkpoints/approved.yaml so the orchestrator can proceed.
argument-hint: "<checkpoint_id> <approve|reject> [note]"
---

# Record a PRISM human checkpoint decision

Parse `$ARGUMENTS`:
- `checkpoint_id` — one of: `cp1_framework`, `cp2_derivation`, `cp3_phase1_verdict`, `cp4_validation`, `cp5_paper_draft`
- `decision` — `approve` or `reject`
- `note` — optional free-text reason

## Steps

1. Verify the checkpoint id is one of the five mandatory checkpoints from spec §11.
2. Read `working_dir/checkpoints/approved.yaml` (create if absent).
3. Append the decision entry:
   ```yaml
   - checkpoint: <id>
     decision: <approve|reject>
     decided_by: Kip Madden
     decided_at: <ISO timestamp>
     note: <text or null>
     preceding_task: <last completed task from current_state.json>
   ```
4. If `reject`, halt the program: update `current_state.json` with `status: halted_at_checkpoint` and print the next steps (refine the rejected step, then re-submit for checkpoint).
5. If `approve`, report that the orchestrator is unblocked and suggest running `/prism-next`.

## The five checkpoints

| ID | Trigger | What Kip reviews |
|---|---|---|
| `cp1_framework` | After P1-T1 | Framework formalization before derivation begins |
| `cp2_derivation` | After P1-T3 | Each step of the s-state derivation |
| `cp3_phase1_verdict` | After P1-T5 | Go/no-go decision for phases 2-5 |
| `cp4_validation` | After all validation phases | Decision to proceed to publication |
| `cp5_paper_draft` | After P6-T2 | Final review before any external release |

## Guardrails

- Checkpoints are Kip's decisions, not agents'. If invoked by an agent or sub-agent, reject the call.
- Never silently skip a checkpoint. The orchestrator enforces the §11 list.
- `cp3_phase1_verdict` after a FALSIFIED verdict is a formal review question — record whether Kip is invoking the kill criterion (§14) or rescuing the framework.
