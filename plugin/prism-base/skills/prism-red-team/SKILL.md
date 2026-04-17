---
name: prism-red-team
description: Red-team pass on PRISM findings — alternative explanations, confound checks, null-test proposals. Implements P6-T1. Used by prism-critic at the end of the validation phases, before the reporter drafts the paper. Can be invoked mid-program if the validator flags a 5σ anomaly.
---

# PRISM Red-Team Pass — P6-T1

## Operating principle

If you can't find three alternative explanations for a positive finding, you haven't looked hard enough. The job is to find ways PRISM might be wrong, so a reviewer doesn't.

## Workflow

1. Read every `validation/phase*_verdict.md`, every `derivations/*.tex`, and the original `prism_research_plan_v1.0.md`.
2. For each VALIDATED or PARTIAL verdict, write an entry in `counter_hypotheses.md` answering:
   - Does standard QED (properly applied) predict the same number?
   - Is the apparent agreement sensitive to unit choice or sign convention?
   - Could a dimensionally-different ansatz produce the same prediction from 4D math?
   - Has a similar "without tuning" claim appeared in the literature and been retracted? (e.g., the original Nambu formula for μ-mass)
3. For each FALSIFIED verdict, write an entry in `failure_analysis.md` answering:
   - Is the failure pattern consistent across all failed cases?
   - What minimal modification would fix it? Is that modification epicyclic?
   - Does the failure rule out the whole framework or just one parameterization?
4. Propose null tests in `null_test_suggestions.md` — concrete experiments that distinguish PRISM from each top alternative. Each gets: observable, required precision, predicted difference (sigma), feasibility today.

## Required counter-hypotheses (must address, at minimum)

- **Standard QED recovery**: Does a careful Bethe-log derivation in standard QED produce the same numerical prediction? If yes, PRISM is empirically indistinguishable at this precision — VALIDATED but not DIFFERENTIATED.
- **Reduced-mass systematic**: v3 had this exact failure mode. Verify the current phase's reduced-mass handling is explicit and correct.
- **Kaluza-Klein revival**: Could any 5D compactification with appropriate radius reproduce this? If yes, PRISM's claim of specific rotation-scaling structure is not distinguishing from generic 5D.
- **Number-coincidence**: α ≈ 1/137 is suggestive but not unique. Run: do other near-α ratios produce similar fits?
- **Fit artifact despite "no fitting" claim**: Re-read the derivation path — did any step implicitly choose a constant in a way that makes the result post-hoc adjustable?

## Output format

```markdown
---
generated_by: prism-critic
generated_at: <timestamp>
spec_task_id: P6-T1
depends_on: [<verdict SHAs>, <derivation SHAs>]
---

# PRISM Red-Team Report

## Counter-Hypothesis 1: <name>
**Severity:** <LOW | MEDIUM | HIGH>
**Claim:** <the alternative explanation>
**Evidence for:** <what supports it>
**Evidence against:** <what argues it does not apply here>
**Distinguishing test:** <observable + precision + predicted difference>
**Verdict:** <plausible | implausible | inconclusive>

## Counter-Hypothesis 2: ...

## Null-Test Suggestions
1. <test name> — <observable> at <precision> would distinguish PRISM from <alternative> by <sigma>σ.
...

## Recommendation to Reporter
<what to include in the final paper's discussion/limitations section>
```

## Honest tone

"Extra dimensions sound weird" is not a counter-hypothesis. "Kaluza-Klein with compactification radius R_KK produces the same running-α at this precision and has lower postulate cost" is.

Cite sources. Every alternative needs ≥1 peer-reviewed reference.
