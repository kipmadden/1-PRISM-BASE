---
description: Dispatch the next eligible PRISM task. Invokes the prism-orchestrator subagent, which reads state, checks gates/checkpoints, and routes to the correct role-agent.
argument-hint: "[--dry-run]"
---

# Dispatch Next PRISM Task

Invoke the `prism-orchestrator` subagent via the Agent tool.

Pass this context to it:
- Current working directory is the user's project root.
- State files live in `./working_dir/`.
- Spec is `./prism_research_plan_v1.0.md`.
- If `$ARGUMENTS` contains `--dry-run`, the orchestrator should identify the next task and print the dispatch plan but NOT actually call the role-agent.

## Pre-dispatch checks

Before invoking the orchestrator, verify:
1. `working_dir/current_state.json` exists (else prompt `/prism-init`).
2. `working_dir/phase_status.json` exists.
3. No unresolved escalations in `working_dir/escalations.md`.

If any check fails, report to the user and stop — do not invoke the orchestrator.

## After the orchestrator returns

Print the updated status block (same format as `/prism-status`). If the orchestrator halted at a gate or checkpoint, surface the pending approval clearly with the exact text of the question needing answer.
