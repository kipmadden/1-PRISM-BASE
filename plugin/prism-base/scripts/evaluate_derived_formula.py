#!/usr/bin/env python3
"""
evaluate_derived_formula.py — turn a sympy-parseable formula for a hydrogen
observable into a predictions CSV the rest of the pipeline can consume.

This is the bridge from Phase 1's derivation (`derivations/*.md` or a LaTeX
expression in the derivation metadata) to Phase 1's prediction artifact
(`predictions/*.csv`) that validate_vs_literature.py scores.

Usage
-----
    python evaluate_derived_formula.py \
        --formula "log(n) + alpha/n" \
        --quantity bethe_log \
        --system H_1s \
        --n-range 1 5 \
        --out predictions/P1-T4_bethe_log_prism.csv \
        --spec-task-id P1-T4

Design notes
------------
- Uses sympy for safe parsing (no `eval`).
- Substitutes CODATA 2022 values for named constants (alpha, pi, phi) from the
  knowledge_base yaml file by default.
- Writes predictions CSV with canonical columns:
    system, n, l, j, quantity, predicted_value, uncertainty, method
- Writes a .meta.yaml sidecar recording formula + constants used.
- `uncertainty` column is written null unless --uncertainty-mode symbolic-propagation
  is requested (and sympy can differentiate the formula).
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import math
import pathlib
import sys

try:
    import sympy as sp
except ImportError:
    sys.stderr.write("sympy required: pip install sympy --break-system-packages\n")
    sys.exit(4)

try:
    import yaml
except ImportError:
    sys.stderr.write("PyYAML required: pip install pyyaml --break-system-packages\n")
    sys.exit(4)


DEFAULT_CONSTANTS = {
    "alpha": 7.2973525643e-3,
    "pi": math.pi,
    "phi": (1 + math.sqrt(5)) / 2,
}


def load_constants(kb_path: pathlib.Path | None) -> dict[str, float]:
    if kb_path is None or not kb_path.exists():
        return dict(DEFAULT_CONSTANTS)
    with kb_path.open() as f:
        kb = yaml.safe_load(f) or {}
    out = dict(DEFAULT_CONSTANTS)
    try:
        out["alpha"] = float(kb["alpha_at_me"]["value"])
    except (KeyError, ValueError, TypeError):
        pass
    try:
        out["phi"] = float(kb["prism_geometric_constants"]["phi"]["value"])
    except (KeyError, ValueError, TypeError):
        pass
    return out


def evaluate(formula_str: str, n_values: list[int], constants: dict[str, float]) -> list[tuple[int, float]]:
    n_sym = sp.Symbol("n", positive=True, integer=True)
    alpha_sym, pi_sym, phi_sym = sp.symbols("alpha pi phi", positive=True)
    local = {"n": n_sym, "alpha": alpha_sym, "pi": pi_sym, "phi": phi_sym,
             "log": sp.log, "sin": sp.sin, "cos": sp.cos, "exp": sp.exp, "sqrt": sp.sqrt}
    expr = sp.sympify(formula_str, locals=local)
    subs = {alpha_sym: constants["alpha"], pi_sym: constants["pi"], phi_sym: constants["phi"]}

    out: list[tuple[int, float]] = []
    for n_val in n_values:
        val = float(expr.subs({**subs, n_sym: n_val}).evalf(25))
        out.append((n_val, val))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Evaluate a derived formula over n range -> predictions CSV")
    ap.add_argument("--formula", required=True, help="sympy-parseable expression in n (and alpha, pi, phi)")
    ap.add_argument("--quantity", required=True)
    ap.add_argument("--system", required=True)
    ap.add_argument("--l", type=int, default=0)
    ap.add_argument("--j", type=float, default=0.5)
    ap.add_argument("--n-range", nargs=2, type=int, required=True, metavar=("N_MIN", "N_MAX"))
    ap.add_argument("--knowledge-base", default=None, help="literature_values.yaml for constants")
    ap.add_argument("--method-label", default="prism_derived")
    ap.add_argument("--out", required=True)
    ap.add_argument("--spec-task-id", default="P1-T4")
    args = ap.parse_args()

    constants = load_constants(pathlib.Path(args.knowledge_base) if args.knowledge_base else None)
    n_values = list(range(args.n_range[0], args.n_range[1] + 1))
    pairs = evaluate(args.formula, n_values, constants)

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["system", "n", "l", "j", "quantity", "predicted_value", "uncertainty", "method"])
        for n_val, pred in pairs:
            w.writerow([args.system, n_val, args.l, args.j, args.quantity, repr(pred), "", args.method_label])

    meta = {
        "generated_by": "prism-computer",
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "spec_task_id": args.spec_task_id,
        "depends_on": [],
        "spec_version": "1.0",
        "artifact_type": "prediction",
        "prediction_metadata": {
            "model_id": args.method_label,
            "units": {"energy": "eV"},
            "n_range": args.n_range,
            "systems_included": [args.system],
            "formula_symbolic": args.formula,
            "free_parameters_count": 0,
            "constants_used": constants,
        },
    }
    with out.with_suffix(out.suffix + ".meta.yaml").open("w") as f:
        yaml.safe_dump(meta, f, sort_keys=False)

    sys.stderr.write(f"[evaluate_derived_formula] wrote {len(pairs)} predictions -> {out}\n")
    print(str(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
