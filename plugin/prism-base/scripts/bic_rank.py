#!/usr/bin/env python3
"""
bic_rank.py — Rank candidate models against hydrogen spectrum data by BIC.

BIC = n·ln(RSS/n) + k·ln(n)
    where n = number of data points, k = number of free parameters,
    RSS = sum of squared residuals (weighted by per-row uncertainty if available)

Interpretation bands (Kass & Raftery 1995):
    ΔBIC < 2      — not worth more than a bare mention
    2 ≤ ΔBIC < 6  — positive evidence against higher-BIC model
    6 ≤ ΔBIC < 10 — strong evidence
    ΔBIC ≥ 10     — decisive

Input
-----
A predictions CSV per model with columns:
    system, n, l, j, quantity, predicted_value, uncertainty, method

A measurements CSV (or merged file) with the same rows and a measured_value column.

Output
------
A BIC ranking table (JSON + CSV) with a .meta.yaml sidecar.

Hazard notes
------------
- The `rydberg_null` model will often win on BIC for small-n subsets because it
  fits the gross structure near-exactly with 1 parameter. FLAG when this happens —
  it indicates the spectrum slice is not QED-sensitive and a different quantity
  (Bethe log, Lamb shift, 2S-1S) must be chosen as the discriminator.
- The reduced-mass correction can masquerade as physics. Ensure every model is
  evaluated WITH reduced mass applied consistently before ranking.
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


def read_csv(path: pathlib.Path) -> list[dict]:
    with path.open() as f:
        return list(csv.DictReader(f))


def bic(rss: float, n: int, k: int) -> float:
    if n <= 0:
        return float("inf")
    return n * math.log(rss / n) + k * math.log(n)


def aic(rss: float, n: int, k: int) -> float:
    if n <= 0:
        return float("inf")
    return n * math.log(rss / n) + 2 * k


def compute_rss(predictions: list[dict], measurements: dict[str, float], uncertainties: dict[str, float]) -> tuple[float, int]:
    rss = 0.0
    count = 0
    for p in predictions:
        key = (p.get("system"), p.get("n"), p.get("l"), p.get("j"), p.get("quantity"))
        key_str = "|".join(str(x) for x in key)
        if key_str not in measurements:
            continue
        try:
            pred = float(p["predicted_value"])
            meas = measurements[key_str]
        except (ValueError, TypeError):
            continue
        sigma = uncertainties.get(key_str)
        resid = pred - meas
        if sigma and sigma > 0:
            rss += (resid / sigma) ** 2
        else:
            rss += resid ** 2
        count += 1
    return rss, count


def load_measurements(path: pathlib.Path) -> tuple[dict[str, float], dict[str, float]]:
    rows = read_csv(path)
    measurements = {}
    uncertainties = {}
    for r in rows:
        key = "|".join(str(r.get(c, "")) for c in ("system", "n", "l", "j", "quantity"))
        try:
            measurements[key] = float(r.get("measured_value") or r.get("energy_eV") or r["predicted_value"])
        except (KeyError, ValueError, TypeError):
            continue
        try:
            uncertainties[key] = float(r.get("uncertainty") or r.get("uncertainty_eV") or 0)
        except (ValueError, TypeError):
            pass
    return measurements, uncertainties


def main() -> int:
    parser = argparse.ArgumentParser(description="BIC model ranking for PRISM")
    parser.add_argument("--measurements", required=True, help="CSV with measured_value column")
    parser.add_argument("--model", action="append", required=True,
                        help="model_id=path/to/predictions.csv:k (repeatable)")
    parser.add_argument("--out", required=True, help="output JSON path")
    parser.add_argument("--spec-task-id", default="unknown")
    args = parser.parse_args()

    meas_path = pathlib.Path(args.measurements)
    measurements, uncertainties = load_measurements(meas_path)
    if not measurements:
        sys.stderr.write("No measurements parsed — check CSV columns.\n")
        return 2

    results = []
    for spec in args.model:
        try:
            model_part, k_str = spec.rsplit(":", 1)
            model_id, pred_path_str = model_part.split("=", 1)
            k = int(k_str)
        except ValueError:
            sys.stderr.write(f"Invalid --model spec (use model_id=path:k): {spec}\n")
            return 5
        preds = read_csv(pathlib.Path(pred_path_str))
        rss, n = compute_rss(preds, measurements, uncertainties)
        if n == 0:
            sys.stderr.write(f"No overlapping rows for model {model_id}; skipping.\n")
            continue
        b = bic(rss, n, k)
        a = aic(rss, n, k)
        results.append({
            "model_id": model_id,
            "predictions_path": pred_path_str,
            "n_free_parameters": k,
            "n_data_points": n,
            "rss": rss,
            "bic": b,
            "aic": a,
        })

    if not results:
        sys.stderr.write("No models scored.\n")
        return 3

    best_bic = min(r["bic"] for r in results)
    for r in results:
        r["delta_bic"] = r["bic"] - best_bic
        if r["delta_bic"] < 2:
            band = "indistinguishable"
        elif r["delta_bic"] < 6:
            band = "positive_evidence"
        elif r["delta_bic"] < 10:
            band = "strong_evidence"
        else:
            band = "decisive"
        r["evidence_band"] = band
    results.sort(key=lambda r: r["bic"])

    out_path = pathlib.Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as f:
        json.dump({"ranking": results, "best_bic": best_bic}, f, indent=2)

    # Sidecar
    meta = {
        "generated_by": "prism-computer",
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "spec_task_id": args.spec_task_id,
        "depends_on": [str(meas_path)] + [m.split("=", 1)[1].rsplit(":", 1)[0] for m in args.model],
        "spec_version": "1.0",
        "artifact_type": "fit_result",
        "fit_metadata": {
            "fitter": "analytic_bic",
            "n_models_scored": len(results),
            "best_model_id": results[0]["model_id"],
            "best_bic": best_bic,
        },
    }
    with out_path.with_suffix(".json.meta.yaml").open("w") as f:
        yaml.safe_dump(meta, f, sort_keys=False)

    # Warning: rydberg_null winning on small-n Balmer slice is an artifact, not physics.
    top = results[0]
    if top["model_id"] == "rydberg_null" and top["n_data_points"] <= 6:
        sys.stderr.write(
            "[bic_rank] WARN: rydberg_null is top-ranked on a small-n slice. "
            "This is almost certainly a degeneracy artifact, not evidence the "
            "null model is physically preferred. Choose a more QED-sensitive "
            "quantity (Bethe log, 2S-1S, Lamb shift) before drawing a verdict.\n"
        )

    print(json.dumps({"best": results[0]["model_id"], "best_bic": best_bic, "ranking_path": str(out_path)}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
