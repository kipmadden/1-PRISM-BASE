---
name: prism-derive-s-state
description: Guide the human-in-the-loop derivation of the PRISM s-state correction function from 5D geometry. Implements P1-T3, the critical-path task. Always produces one derivation step at a time for user review. Use when the user says "continue the s-state derivation", "do the next derivation step", "P1-T3", or the orchestrator dispatches P1-T3 to prism-theoretician.
---

# PRISM s-State Correction Derivation — P1-T3

**This is the most important single task in the entire research program.** If the derivation produces Bethe-log values within 10% of +2.98, +2.81, +2.77, +2.75, +2.74 for n=1..5 without any fitting to the data, PRISM is validated. If not, PRISM is falsified at this precision.

## Non-negotiable rules

1. **One step per turn.** Propose exactly one derivation step, get user ACCEPT/REJECT/REVISE, then (and only then) append to the `.tex` file.
2. **No comparison to literature during derivation.** The validator (P1-T5) does that. Premature comparison breaks the "without tuning" claim.
3. **No implicit choices.** Any place the derivation picks a constant, sign, branch, or normalization must be flagged `[[CHOICE: <description>]]` and escalated.
4. **No new postulates.** If the derivation needs one, halt. That's an assumption-escalation per spec §4.

## Workflow (repeat until done)

### Step N: propose

Read `working_dir/derivations/P1-T3_s_state_correction.tex` so far. Identify the next unresolved goal from the outline. Compose a LaTeX snippet (≤15 lines inline math) with an English justification tied to either:
- A prior line of this derivation (cite line number)
- A postulate in `prism_formal_spec.md` (cite postulate id)
- A standard QM/QFT theorem (cite source)

Write the proposal to chat, not yet to disk:

```
### Proposed step N
**Goal:** <one sentence>
**Justification:** <one or two sentences, cite sources>

$$
<LaTeX snippet>
$$

**Output:** <what this step produces for the next step to consume>
```

### Step N: review

Ask the user: `ACCEPT / REJECT / REVISE?`

- **ACCEPT** → append the step to `.tex`, update the symbolic form in `.json`, continue to step N+1.
- **REJECT** → record the rejection in `derivation_log.md` with the user's reason, do not append, re-plan.
- **REVISE: <user edit>** → apply the edit, re-present for confirmation before appending.

### Step N: persist

On ACCEPT:
1. Append the snippet to `working_dir/derivations/P1-T3_s_state_correction.tex`.
2. Update `working_dir/derivations/P1-T3_s_state_correction.json` with:
   ```json
   {"step": N, "symbolic_form": "<sympy-parseable>", "variables": {...}, "postulates_used": [...]}
   ```
3. Append one line to `working_dir/derivations/derivation_log.md`.

## Success criteria (from spec §8, P1-T3)

The completed derivation must deliver all three:
1. Integral expression for the s-state self-energy analog in the native spiral basis.
2. Integral is finite and well-defined (no renormalization handwaves).
3. Explicit function of `n` with no free parameters beyond α.

When all three are met, the derivation is complete. Hand off to P1-T4 (prism-computer) for numerical evaluation.

## Failure modes (from spec §8, P1-T3)

- **integral_diverges**: PRISM needs an explicit regularization scheme. Escalate to user.
- **expression_requires_tuning**: PRISM is not parameter-free at current specification. Document plainly and continue — but flag in the phase-1 verdict.

Both are legitimate outcomes. Do not paper over either.

## Outputs required at task completion

- `working_dir/derivations/P1-T3_s_state_correction.tex`
- `working_dir/derivations/P1-T3_s_state_correction.json`
- `working_dir/derivations/derivation_log.md` (appended)
- `working_dir/derivations/P1-T3_s_state_correction.tex.meta.yaml` per handoff contract

Estimated: 80K-150K tokens, 2-3 weeks wall time including user review cycles.
