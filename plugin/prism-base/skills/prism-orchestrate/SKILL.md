---
name: prism-orchestrate
description: Drive the PRISM research program forward. Use when the user asks to "start prism", "resume prism", "advance prism", "run the next prism task", or issues /prism-next. Reads current_state.json, identifies the next eligible task per the spec DAG, enforces gates and human checkpoints, and dispatches the role-agent. Not for executing tasks directly.
---

# PRISM Orchestration Workflow

You are driving a long-running agentic research program. The spec is in `prism_research_plan_v1.0.md`. The state is in `working_dir/current_state.json` and `working_dir/phase_status.json`.

## Step 1 — Load state

Read these files in parallel:
- `working_dir/current_state.json`
- `working_dir/phase_status.json`
- `prism_research_plan_v1.0.md`

If any is missing, tell the user to run `/prism-init` first. Stop.

## Step 2 — Determine the next task

Walk the DAG from the spec's §8. The next task is the earliest-ordered task whose `depends_on:` list is fully satisfied by completed tasks in `phase_status.json`.

If the next task has a gate condition (§10 or explicit `gate: true`), check the gate:
- Phase 2/3/5 require `P1-T5` verdict ∈ {VALIDATED, PARTIAL}. If FALSIFIED, halt and prompt the user for a go/no-go override.
- Any mandatory checkpoint from §11 must have a matching entry in `working_dir/checkpoints/approved.yaml` — if not, pause and request user approval.

## Step 3 — Dispatch via Agent tool

Delegate to the correct subagent per the role map:
- data_fetcher → `prism-data-fetcher`
- parser → `prism-parser`
- theoretician → `prism-theoretician` (ALWAYS confirm human-in-the-loop before dispatch)
- computer → `prism-computer`
- validator → `prism-validator`
- critic → `prism-critic`
- reporter → `prism-reporter`
- librarian → `prism-librarian`

Pass the task's full spec block (inputs, outputs, success_criteria, failure_modes, estimated_tokens) as context.

## Step 4 — Enforce handoff contract

When the subagent returns, verify:
1. Every file listed in `outputs:` exists on disk.
2. Each output has the §9 YAML frontmatter (generated_by, generated_at, depends_on, spec_task_id).
3. For numerical outputs, the `method` column is non-empty.

If the contract fails, do not mark the task complete — surface the gap to the user.

## Step 5 — Update state

On successful completion:
- Update `current_state.json`: `last_completed_task`, `current_phase`, `current_task`, `tokens_used_cumulative`.
- Append to `phase_status.json`: `{task_id, verdict, completed_at, outputs: [paths]}`.
- Append one line to `working_dir/audit.log`: `<ISO_timestamp> | <task_id> | <agent> | <verdict> | <tokens> | <duration_s>`.

## Step 6 — Escalation checks

Before concluding the turn, scan for escalation triggers per spec §10:
- Any task exceeded 2× its token estimate
- Validator verdict was FALSIFIED
- Theoretician flagged a non-first-principles choice
- Data fetcher returned unexpected format 3× consecutively
- Framework inconsistency detected

If any trigger fires, summarize to the user and halt — do not auto-proceed to the next task.

## Output format

Print this status block at the end of every orchestration turn:

```
─── PRISM STATUS ───
Phase: <n> — <phase_name>
Last: <task_id> → <VERDICT>   (in <duration>, <tokens> tokens)
Next: <task_id> (<agent>)     gates: <ok|pending>
Checkpoints: <n_passed>/<n_required>
Budget: <used>/<total> tokens
Escalations: <none|list>
───────────────────
```
