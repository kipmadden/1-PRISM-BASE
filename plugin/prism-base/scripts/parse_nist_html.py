#!/usr/bin/env python3
"""
parse_nist_html.py — NIST Handbook static-HTML table parser.

Targets the hydrogen/deuterium pages under /PhysRefData/Handbook/Tables/ which
carry pipe-delimited text inside <pre> blocks. Produces a tidy CSV with
canonical columns and an accompanying .meta.yaml sidecar.

Usage
-----
    python parse_nist_html.py --in raw_data/nist_handbook_hydrogen_table5.html \
                              --out structured_data/hydrogen_levels.csv \
                              --spec-task-id P1-T2

Output columns
--------------
    n, l, j, term, energy_cm_inverse, energy_eV, uncertainty_eV, source

Conversion
----------
    1 cm^-1 = 1.23984198433... × 10^-4 eV (CODATA 2022, hc in eV·cm units)
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import pathlib
import re
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("PyYAML required: pip install pyyaml --break-system-packages\n")
    sys.exit(4)

# CODATA 2022: hc = 1.986 445 857e-25 J·m -> in eV·cm = 1.239841984e-4
CM_INVERSE_TO_EV = 1.239841984332e-4

PRE_BLOCK_RE = re.compile(r"<pre[^>]*>(.*?)</pre>", re.DOTALL | re.IGNORECASE)
TAG_STRIP_RE = re.compile(r"<[^>]+>")
# Term symbols like 2S1/2, 2P3/2, etc.
TERM_RE = re.compile(r"(\d+)([A-Z])(\d+)/(\d+)")


def strip_html(s: str) -> str:
    return TAG_STRIP_RE.sub("", s)


def sha256_path(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_term(term: str) -> tuple[int | None, int | None, float | None]:
    """Parse '2S1/2' -> (n=2, l=0, j=0.5).  Returns (None, None, None) on failure."""
    m = TERM_RE.search(term.strip())
    if not m:
        return None, None, None
    n = int(m.group(1))
    letter = m.group(2)
    l_map = {"S": 0, "P": 1, "D": 2, "F": 3, "G": 4, "H": 5}
    l = l_map.get(letter)
    num, den = int(m.group(3)), int(m.group(4))
    j = num / den if den else None
    return n, l, j


def parse_lines(pre_text: str) -> list[dict]:
    rows: list[dict] = []
    for raw_line in pre_text.splitlines():
        line = raw_line.strip()
        if not line or "|" not in line:
            continue
        # Skip header/separator rows
        if set(line) <= {"|", "-", " ", "="}:
            continue
        parts = [p.strip() for p in line.split("|")]
        # Heuristic: NIST table 5 rows have >= 3 non-empty fields with a term-looking token.
        term_tok = next((p for p in parts if TERM_RE.search(p)), None)
        if not term_tok:
            continue
        # Try to pull energy as the last numeric field.
        energy_cm = None
        uncertainty_eV = None
        for p in reversed(parts):
            try:
                energy_cm = float(p.replace(",", ""))
                break
            except ValueError:
                continue
        if energy_cm is None:
            continue
        n, l, j = parse_term(term_tok)
        rows.append({
            "n": n,
            "l": l,
            "j": j,
            "term": term_tok,
            "energy_cm_inverse": energy_cm,
            "energy_eV": energy_cm * CM_INVERSE_TO_EV,
            "uncertainty_eV": uncertainty_eV,
            "source": "nist_handbook_mk00a",
        })
    return rows


def write_sidecar(csv_path: pathlib.Path, input_path: pathlib.Path, spec_task_id: str, nrows: int) -> None:
    meta = {
        "generated_by": "prism-parser",
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "spec_task_id": spec_task_id,
        "depends_on": [str(input_path)],
        "spec_version": "1.0",
        "artifact_type": "structured_data",
        "content_sha256": sha256_path(csv_path),
        "provenance": {
            "source_citation_key": "nist_handbook_mk00a",
            "source_url": None,
            "fetch_timestamp": None,
            "upstream_chain": [f"raw -> {input_path.name}", f"{spec_task_id} -> {csv_path.name}"],
        },
        "prediction_metadata": {
            "units": {"energy": "eV", "energy_alt": "cm^-1"},
            "n_range": None,
        },
        "notes": {"nrows": nrows, "parser": "pipe-delimited <pre> block"},
    }
    sidecar = csv_path.with_suffix(csv_path.suffix + ".meta.yaml")
    with sidecar.open("w") as f:
        yaml.safe_dump(meta, f, sort_keys=False)


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse NIST Handbook hydrogen table HTML -> CSV")
    parser.add_argument("--in", dest="infile", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--spec-task-id", default="unknown")
    args = parser.parse_args()

    in_path = pathlib.Path(args.infile)
    out_path = pathlib.Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    html = in_path.read_text(errors="replace")
    blocks = PRE_BLOCK_RE.findall(html)
    if not blocks:
        sys.stderr.write("No <pre> blocks found — page layout may have changed.\n")
        return 2

    all_rows: list[dict] = []
    for block in blocks:
        all_rows.extend(parse_lines(strip_html(block)))

    if not all_rows:
        sys.stderr.write("<pre> blocks parsed but no rows recognized. Inspect input.\n")
        return 3

    with out_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["n", "l", "j", "term", "energy_cm_inverse", "energy_eV", "uncertainty_eV", "source"])
        writer.writeheader()
        for r in all_rows:
            writer.writerow(r)

    write_sidecar(out_path, in_path, args.spec_task_id, len(all_rows))
    sys.stderr.write(f"[parse_nist_html] wrote {len(all_rows)} rows -> {out_path}\n")
    print(str(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
