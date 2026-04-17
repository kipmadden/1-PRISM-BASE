---
name: prism-pysr-regression
description: Run the symbolic regression sanity check (P4-T1). Feeds cleaned v4-pipeline residuals into PySR with a PRISM-restricted operator basis, produces the top-10 discovered expressions and a Pareto frontier. Used only if Julia is installed on the host — otherwise the task is skipped, not substituted.
---

# PySR Symbolic Regression — P4-T1

The Kepler move: let the data reveal the functional form rather than forcing an ansatz. If PySR's top expression is algebraically equivalent to the theoretician's derived form (P1-T3), that's independent corroboration.

## Preconditions

1. **Julia must be installed** — `julia --version` must succeed.
2. **PySR must be installed** — `python -c "import pysr"` must succeed.
3. **Operator basis** — `working_dir/operator_basis_config.yaml` must exist and declare:
   ```yaml
   allowed_operators: [+, -, *, /, log, sin, cos, exp]
   allowed_constants: [1, α, π, φ, n, ℓ, j]
   max_expression_complexity: 20
   ```

If any precondition fails, skip this task — do not substitute a weaker regression tool.

## Input data

- `working_dir/predictions/v4_pipeline_residuals.csv` — residuals from phase-0 v4 output after subtracting dirac_recoil baseline. Columns: `n, l, j, residual, uncertainty`.

## Workflow

1. Run `scripts/run_pysr.py --data <csv> --config <yaml> --iterations 40 --out <dir>`.
2. PySR writes its Pareto frontier (complexity vs loss) and a table of candidate expressions.
3. Extract the top 10 by loss and complexity to `working_dir/pysr_fits/top_10_expressions.csv`.
4. Render the Pareto frontier to `working_dir/pysr_fits/pareto_frontier.png` + `.pdf`.

## Success criteria (from spec §8, P4-T1)

- 40+ iterations completed
- Top expression has R² > 0.99 on training data
- At least one expression in the top-10 uses ≤10 operators (readable form)

## Handoff to validator

P4-T2 compares the discovered top expression against the theoretician's derived form. The validator should flag HIGH_CONFIDENCE if they are algebraically equivalent (up to rearrangement). If different, the critic agent red-teams the discrepancy.

## Output contract

- `working_dir/pysr_fits/top_10_expressions.csv` with the standard handoff sidecar
- Columns: `rank, expression, complexity, loss, r_squared, operator_count`
- `working_dir/pysr_fits/pysr_run_log.md` — the full PySR run log for audit
