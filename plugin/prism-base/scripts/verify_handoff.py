#!/usr/bin/env python3
"""
verify_handoff.py — prism-librarian's contract verifier.

Walks a directory, finds every artifact (any file that isn't an index or hidden),
and checks for either:

    (A) inline YAML frontmatter at the top (delimited by --- lines), OR
    (B) a sibling <filename>.meta.yaml sidecar.

Required fields (enforced):
    generated_by, generated_at, spec_task_id, depends_on

Exits:
    0 — all artifacts pass
    1 — at least one artifact missing contract; report printed to stdout
    2 — invoked on nonexistent directory

Use from the orchestrator before each phase advance.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("PyYAML required: pip install pyyaml --break-system-packages\n")
    sys.exit(4)


REQUIRED_FIELDS = ("generated_by", "generated_at", "spec_task_id", "depends_on")
TEXT_EXTS = {".md", ".tex", ".py", ".yaml", ".yml"}
SIDECAR_EXTS = {".csv", ".json", ".pdf", ".png", ".h5", ".parquet", ".bin", ".html"}
SKIP_NAMES = {"README.md", "MEMORY.md"}
SKIP_SUFFIXES = (".meta.yaml",)


def extract_frontmatter(path: pathlib.Path) -> dict | None:
    try:
        head = path.read_text(errors="replace").splitlines()[:80]
    except Exception:
        return None
    if not head or head[0].strip() != "---":
        return None
    try:
        end = next(i for i in range(1, len(head)) if head[i].strip() == "---")
    except StopIteration:
        return None
    try:
        return yaml.safe_load("\n".join(head[1:end])) or {}
    except Exception:
        return None


def read_sidecar(path: pathlib.Path) -> dict | None:
    sidecar = path.with_suffix(path.suffix + ".meta.yaml")
    if not sidecar.exists():
        return None
    try:
        with sidecar.open() as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return None


def check_file(path: pathlib.Path) -> tuple[bool, list[str]]:
    errors: list[str] = []
    meta = None
    if path.suffix.lower() in TEXT_EXTS:
        meta = extract_frontmatter(path)
        if meta is None:
            meta = read_sidecar(path)  # still allow sidecar for text files
        if meta is None:
            errors.append("missing frontmatter AND sidecar")
            return False, errors
    elif path.suffix.lower() in SIDECAR_EXTS:
        meta = read_sidecar(path)
        if meta is None:
            errors.append("missing .meta.yaml sidecar")
            return False, errors
    else:
        return True, []  # unknown type, skip

    for field in REQUIRED_FIELDS:
        if field not in meta:
            errors.append(f"missing required field: {field}")
    return len(errors) == 0, errors


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify PRISM handoff contract across a directory")
    ap.add_argument("--root", required=True)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    root = pathlib.Path(args.root)
    if not root.exists():
        sys.stderr.write(f"No such directory: {root}\n")
        return 2

    failures: list[tuple[pathlib.Path, list[str]]] = []
    total = 0

    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.name.startswith(".") or p.name in SKIP_NAMES:
            continue
        if any(p.name.endswith(sfx) for sfx in SKIP_SUFFIXES):
            continue
        total += 1
        ok, errs = check_file(p)
        if not ok:
            failures.append((p, errs))

    if not args.quiet:
        print(f"Scanned: {total} artifacts under {root}")
        print(f"Failures: {len(failures)}")
        for p, errs in failures:
            print(f"  {p}")
            for e in errs:
                print(f"    - {e}")

    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
