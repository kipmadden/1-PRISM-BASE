---
description: Print the current PRISM program status — phase, last completed task, next eligible task, gate status, checkpoint status, token budget.
---

# PRISM Program Status

Read `working_dir/current_state.json` and `working_dir/phase_status.json`. If either is missing, report that `/prism-init` must be run first.

Render this block:

```
─── PRISM STATUS ───
Program: PRISM Theory Validation v1.0
Current phase: <n> — <phase_name>
Last completed: <task_id> → <VERDICT> (at <timestamp>)
Next eligible: <task_id> (<agent>, est. <tokens>)
Gates: <PASSED | PENDING: <gate_name>>
Checkpoints: <n_approved>/<n_required> approved
  Pending: <list>
Tokens used: <used> / <budget> (<pct>%)
Wall time elapsed: <days> (of 6-10 week estimate)
Escalations open: <count>
  <list if any>

Phase verdict table:
  Phase 1 (critical path): <PENDING | VALIDATED | PARTIAL | FALSIFIED>
  Phase 2 (muonic H):       <...>
  Phase 3 (α running):       <...>
  Phase 4 (symbolic regr.): <...>
  Phase 5 (extended data):  <...>
  Phase 6 (synthesis):      <...>
─────────────────────
```

Do not dispatch anything. Read-only report.

If the user asks follow-ups like "what blocks P2?" or "why is P1-T3 still pending?", answer from the state files without dispatching.
