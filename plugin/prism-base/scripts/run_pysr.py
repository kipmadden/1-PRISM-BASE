#!/usr/bin/env python3
"""
run_pysr.py — P4-T1 symbolic regression driver (Phase 4).

Precondition checks, then runs PySR on the hydrogen residual data with the
operator basis in templates/operator_basis_config.yaml. Produces:

    pysr_fits/<run_id>/pareto.csv       (rank, complexity, loss, expr)
    pysr_fits/<run_id>/pareto.csv.meta.yaml
    pysr_fits/<run_id>/flagged.md       (PRISM-signature matches)
    pysr_fits/<run_id>/run.log

IMPORTANT
---------
Per spec §5.E, if Julia or PySR is missing, this script EXITS 77 (skipped) and
does NOT substitute a weaker fitter. Phase 4 is optional — P1-T5 is the gate,
not P4-T1 — so a skip is safe. The orchestrator will record the skip reason.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import shutil
import subprocess
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("PyYAML required: pip install pyyaml --break-system-packages\n")
    sys.exit(4)


EXIT_SKIPPED_MISSING_PRECONDITION = 77


def has_command(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def julia_version_ok(min_major: int = 1, min_minor: int = 9) -> bool:
    if not has_command("julia"):
        return False
    try:
        out = subprocess.run(["julia", "--version"], capture_output=True, text=True, timeout=15)
        m = re.search(r"julia version (\d+)\.(\d+)", out.stdout)
        if not m:
            return False
        maj, minr = int(m.group(1)), int(m.group(2))
        return (maj, minr) >= (min_major, min_minor)
    except Exception:
        return False


def pysr_importable() -> bool:
    try:
        import pysr  # noqa: F401
        return True
    except Exception:
        return False


def match_signatures(expr_str: str, signatures: list[str]) -> list[str]:
    """Return list of signatures that appear as substrings of the sympy-style expression."""
    hits: list[str] = []
    for sig in signatures:
        # naive substring check; PySR emits fairly canonical forms like 'log(n)' already
        if sig.replace(" ", "") in expr_str.replace(" ", ""):
            hits.append(sig)
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description="PRISM PySR symbolic regression driver")
    ap.add_argument("--data", required=True, help="CSV with columns n, residual (and optional weight)")
    ap.add_argument("--config", required=True, help="operator_basis_config.yaml")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--run-id", default=dt.datetime.now(dt.timezone.utc).strftime("run_%Y%m%dT%H%M%SZ"))
    ap.add_argument("--spec-task-id", default="P4-T1")
    args = ap.parse_args()

    # ── Preconditions ──────────────────────────────────────────────────────
    if not julia_version_ok():
        sys.stderr.write("[run_pysr] SKIP: Julia >= 1.9 not found on PATH.\n")
        return EXIT_SKIPPED_MISSING_PRECONDITION
    if not pysr_importable():
        sys.stderr.write("[run_pysr] SKIP: pysr Python package not importable.\n")
        return EXIT_SKIPPED_MISSING_PRECONDITION

    import numpy as np
    import pandas as pd
    from pysr import PySRRegressor

    with open(args.config) as f:
        cfg = yaml.safe_load(f)
    signatures = cfg.get("prism_signatures", [])
    allowed_ops = set(cfg.get("allowed_operators", ["+", "-", "*", "/", "log", "sin", "cos", "exp"]))
    binary_ops = [op for op in ("+", "-", "*", "/") if op in allowed_ops]
    unary_ops = [op for op in ("log", "sin", "cos", "exp") if op in allowed_ops]
    max_complexity = int(cfg.get("max_expression_complexity", 20))
    iterations = int(cfg.get("iterations", 40))
    population_size = int(cfg.get("population_size", 50))

    # ── Load data ──────────────────────────────────────────────────────────
    df = pd.read_csv(args.data)
    if "n" not in df.columns or "residual" not in df.columns:
        sys.stderr.write("[run_pysr] data must have columns: n, residual (optional: weight)\n")
        return 5
    X = df[["n"]].to_numpy()
    y = df["residual"].to_numpy()
    weights = df["weight"].to_numpy() if "weight" in df.columns else None

    # ── Run ────────────────────────────────────────────────────────────────
    out_dir = pathlib.Path(args.out_dir) / args.run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    model = PySRRegressor(
        niterations=iterations,
        populations=population_size,
        binary_operators=binary_ops,
        unary_operators=unary_ops,
        maxsize=max_complexity,
        progress=False,
        verbosity=1,
        equation_file=str(out_dir / "equations.csv"),
    )
    model.fit(X, y, weights=weights)

    frontier = model.equations_
    # Write Pareto frontier CSV
    pareto_path = out_dir / "pareto.csv"
    frontier.to_csv(pareto_path, index=False)

    # Flagged signatures
    flagged = []
    for _, row in frontier.iterrows():
        expr = str(row.get("equation", ""))
        hits = match_signatures(expr, signatures)
        if hits:
            flagged.append({"complexity": row.get("complexity"), "loss": row.get("loss"), "equation": expr, "signatures": hits})

    with (out_dir / "flagged.md").open("w") as f:
        f.write("---\n")
        f.write(f"generated_by: prism-computer\n")
        f.write(f"generated_at: {dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n")
        f.write(f"spec_task_id: {args.spec_task_id}\n")
        f.write(f"depends_on:\n  - {args.data}\n  - {args.config}\n")
        f.write(f"artifact_type: fit_result\n---\n\n")
        f.write(f"# PySR Flagged Expressions\n\n")
        if not flagged:
            f.write("_No PRISM signatures matched in the Pareto frontier._\n")
        else:
            for h in flagged:
                f.write(f"- **complexity={h['complexity']}, loss={h['loss']:.4g}**\n")
                f.write(f"  - expr: `{h['equation']}`\n")
                f.write(f"  - matched: {h['signatures']}\n")

    # Sidecar for pareto.csv
    meta = {
        "generated_by": "prism-computer",
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "spec_task_id": args.spec_task_id,
        "depends_on": [args.data, args.config],
        "spec_version": "1.0",
        "artifact_type": "fit_result",
        "fit_metadata": {
            "fitter": "pysr",
            "iterations": iterations,
            "population_size": population_size,
            "max_complexity": max_complexity,
            "allowed_operators": list(allowed_ops),
            "n_flagged_signatures": len(flagged),
        },
    }
    with pareto_path.with_suffix(".csv.meta.yaml").open("w") as f:
        yaml.safe_dump(meta, f, sort_keys=False)

    print(json.dumps({"pareto": str(pareto_path), "flagged_count": len(flagged), "run_id": args.run_id}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
