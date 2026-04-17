---
description: Jump the PRISM orchestrator to a specific phase. Use to explicitly start or re-start a phase; normally /prism-next is sufficient.
argument-hint: "<phase_number>"
---

# Jump to PRISM Phase

Target phase: `$1` (integer, 1-6)

## Steps

1. Validate phase number is in [1, 6]. Reject otherwise.
2. Check phase prerequisites from spec:
   - Phase 2, 3, 5 require P1-T5 verdict ∈ {VALIDATED, PARTIAL}
   - Phase 4 requires P1-T5 to have returned any verdict (works even on FALSIFIED as a sanity check)
   - Phase 6 requires all of phases 1-5 to be at least attempted
3. If prerequisites fail, explain what's missing and exit.
4. If prerequisites pass:
   - Set `current_state.json → current_phase` to the target.
   - Set `current_state.json → current_task` to the first task in that phase per spec §8.
   - Log to `audit.log`: `<timestamp> | PHASE_JUMP | -> phase <n> | user: Kip Madden`.
5. Report the update and suggest `/prism-next` to dispatch.

## Guardrails

- Do not jump backward silently. If Kip asks to jump to an earlier phase (e.g., back to Phase 1 after failing validation), confirm: "Re-running Phase 1 will archive current derivations. Proceed?"
- Do not jump forward past a FALSIFIED verdict without an explicit kill-override. Surface the kill criterion from §14.
