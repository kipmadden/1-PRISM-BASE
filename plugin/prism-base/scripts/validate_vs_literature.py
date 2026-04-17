#!/usr/bin/env python3
"""
validate_vs_literature.py — render a VALIDATED/PARTIAL/FALSIFIED verdict for a
predictions file against `knowledge_base/literature_values.yaml`.

Thresholds (spec §10):
    VALIDATED  — max |frac_dev| < 0.10  AND  consistent sign  AND  σ_dev < 5
    PARTIAL    — 0.10 ≤ max |frac_dev| < 0.50  AND  sign-consistent  AND  σ_dev < 10
    FALSIFIED  — max |frac_dev| ≥ 0.50  OR  sign flip on more than one row  OR  σ_dev ≥ 10
    NULL_RESULT — zero overlapping rows OR prediction values are all NaN

Sign-flip handling:
    - A *consistent* sign flip on EVERY row is logged and passed through to the
      verdict (common in geometric theories where a convention differs). Caller
      can apply `--allow-consistent-sign-flip` to accept it as equivalent up to
      sign.
    - A MIXED-sign pattern (some flipped, some not) is always FALSIFIED regardless
      of magnitude.

Output: a markdown report at --out plus a JSON summary at --out.json
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import pathlib
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("PyYAML required: pip install pyyaml --break-system-packages\n")
    sys.exit(4)


def read_predictions(path: pathlib.Path) -> list[dict]:
    with path.open() as f:
        return list(csv.DictReader(f))


def resolve_literature(kb: dict, quantity: str, system: str, n: int | None) -> tuple[float | None, float | None, str | None]:
    """
    Map (quantity, system, n) tuple to a literature value in the knowledge base.
    Returns (value, uncertainty, citation_key) or (None, None, None) if not found.
    """
    if quantity == "bethe_log" and system.startswith("H_") and n is not None:
        try:
            entry = kb["bethe_log_values"]["values"][f"n_{n}"]
            return entry["value"], entry["uncertainty"], kb["bethe_log_values"]["citation_key"]
        except KeyError:
            return None, None, None
    if quantity == "lamb_shift_2s_2p" and system == "H_2s":
        e = kb["hydrogen_lamb_shift"]["energy"]
        return e["value"], e["uncertainty"], kb["hydrogen_lamb_shift"]["citation_key"]
    if quantity == "lamb_shift_2s_2p" and system == "muH_2s":
        e = kb["muonic_hydrogen_lamb_shift"]["energy"]
        return e["value"], e["uncertainty"], kb["muonic_hydrogen_lamb_shift"]["citation_key"]
    return None, None, None


def verdict_band(max_frac: float, max_sigma: float, sign_status: str) -> str:
    if sign_status == "mixed":
        return "FALSIFIED"
    if max_frac < 0.10 and max_sigma < 5:
        return "VALIDATED"
    if max_frac < 0.50 and max_sigma < 10:
        return "PARTIAL"
    return "FALSIFIED"


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate PRISM predictions vs. literature values")
    ap.add_argument("--predictions", required=True)
    ap.add_argument("--knowledge-base", required=True, help="path to literature_values.yaml")
    ap.add_argument("--out", required=True, help="output markdown report path")
    ap.add_argument("--allow-consistent-sign-flip", action="store_true")
    ap.add_argument("--spec-task-id", default="unknown")
    args = ap.parse_args()

    preds = read_predictions(pathlib.Path(args.predictions))
    with pathlib.Path(args.knowledge_base).open() as f:
        kb = yaml.safe_load(f)

    comparison_rows: list[dict] = []
    signs: list[int] = []

    for p in preds:
        q = p.get("quantity", "")
        system = p.get("system", "")
        try:
            n = int(p["n"]) if p.get("n") else None
        except (ValueError, TypeError):
            n = None
        lit_val, lit_sigma, citation = resolve_literature(kb, q, system, n)
        if lit_val is None:
            continue
        try:
            pred_val = float(p["predicted_value"])
        except (ValueError, TypeError):
            continue
        if math.isnan(pred_val):
            continue

        residual = pred_val - lit_val
        frac_dev = abs(residual) / abs(lit_val) if lit_val else float("inf")
        sigma_dev = abs(residual) / lit_sigma if lit_sigma else None
        sign = 1 if (pred_val * lit_val) >= 0 else -1
        signs.append(sign)

        comparison_rows.append({
            "quantity": q,
            "system": system,
            "n": n,
            "predicted": pred_val,
            "literature": lit_val,
            "residual": residual,
            "frac_dev": frac_dev,
            "sigma_dev": sigma_dev,
            "sign_match": sign == 1,
            "citation_key": citation,
        })

    if not comparison_rows:
        verdict = "NULL_RESULT"
        max_frac = None
        max_sigma = None
        sign_status = "n/a"
    else:
        if all(s == 1 for s in signs):
            sign_status = "consistent"
        elif all(s == -1 for s in signs):
            sign_status = "consistent_flip"
        else:
            sign_status = "mixed"

        max_frac = max(r["frac_dev"] for r in comparison_rows)
        max_sigma = max((r["sigma_dev"] or 0) for r in comparison_rows)

        if sign_status == "consistent_flip" and not args.allow_consistent_sign_flip:
            verdict = "FALSIFIED"
        else:
            verdict = verdict_band(max_frac, max_sigma, sign_status)

    # ── Markdown report ────────────────────────────────────────────────────
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as f:
        f.write("---\n")
        f.write(f"generated_by: prism-validator\n")
        f.write(f"generated_at: {dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n")
        f.write(f"spec_task_id: {args.spec_task_id}\n")
        f.write(f"depends_on:\n  - {args.predictions}\n  - {args.knowledge_base}\n")
        f.write(f"artifact_type: validation\n")
        f.write("validation_metadata:\n")
        f.write(f"  verdict: {verdict}\n")
        f.write(f"  max_fractional_deviation: {max_frac}\n")
        f.write(f"  sigma_deviation: {max_sigma}\n")
        f.write(f"  escalation_triggered: {str(max_sigma is not None and max_sigma >= 5).lower()}\n")
        f.write("---\n\n")
        f.write("# PRISM Validation Report\n\n")
        f.write("## Summary\n\n")
        f.write(f"- Predictions: `{args.predictions}`\n")
        f.write(f"- Knowledge base: `{args.knowledge_base}`\n")
        f.write(f"- Rows compared: **{len(comparison_rows)}**\n")
        f.write(f"- Sign status: **{sign_status}**\n")
        f.write(f"- Worst fractional deviation: **{max_frac}**\n")
        f.write(f"- Worst σ deviation: **{max_sigma}**\n\n")
        f.write("## Comparison Table\n\n")
        f.write("| quantity | system | n | predicted | literature | frac_dev | σ_dev | sign_match | citation |\n")
        f.write("|---|---|---|---|---|---|---|---|---|\n")
        for r in comparison_rows:
            f.write(f"| {r['quantity']} | {r['system']} | {r['n']} | {r['predicted']:.6g} | "
                    f"{r['literature']:.6g} | {r['frac_dev']:.3e} | "
                    f"{(r['sigma_dev'] or 0):.2f} | {r['sign_match']} | {r['citation_key']} |\n")
        f.write(f"\n## Verdict: **{verdict}**\n\n")
        f.write("## Recommendations\n\n")
        if verdict == "VALIDATED":
            f.write("- Proceed to next task per orchestrator state.\n")
        elif verdict == "PARTIAL":
            f.write("- Pattern qualitatively correct but quantitatively off. Investigate:\n")
            f.write("  1. Missing higher-order QED term in the ansatz.\n")
            f.write("  2. Unit conversion (cm⁻¹ ↔ eV) or reduced-mass factor.\n")
            f.write("  3. Sign convention in the PRISM integrand.\n")
        elif verdict == "FALSIFIED":
            f.write("- Disagreement exceeds kill thresholds. Invoke escalation per spec §14.\n")
            f.write("- Consider whether a rescue move requires a new postulate — if yes, HALT.\n")
        else:
            f.write("- No literature overlap found. Check that prediction rows use canonical quantity/system keys.\n")

    # ── JSON summary ───────────────────────────────────────────────────────
    json_path = out.with_suffix(out.suffix + ".json")
    with json_path.open("w") as f:
        json.dump({
            "verdict": verdict,
            "max_fractional_deviation": max_frac,
            "max_sigma_deviation": max_sigma,
            "sign_status": sign_status,
            "rows_compared": len(comparison_rows),
            "rows": comparison_rows,
        }, f, indent=2, default=str)

    sys.stderr.write(f"[validate_vs_literature] verdict={verdict}  rows={len(comparison_rows)}\n")
    print(json.dumps({"verdict": verdict, "report": str(out)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
