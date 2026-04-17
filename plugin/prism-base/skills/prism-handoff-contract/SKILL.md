---
name: prism-handoff-contract
description: Write or verify the PRISM handoff contract — the YAML frontmatter that every pipeline artifact carries so downstream tasks can consume outputs without re-parsing prose. Use when any PRISM agent is writing a derivation, prediction CSV, validation report, figure, or raw data file.
---

# PRISM Handoff Contract (spec §9)

Every artifact in the PRISM working directory carries a YAML frontmatter block or sidecar so downstream tasks have a machine-readable provenance trail.

## For `.md`, `.tex`, and text files

Frontmatter is inline at the top of the file:

```yaml
---
generated_by: <agent_id>          # e.g., prism-computer
generated_at: <ISO timestamp>      # e.g., 2026-04-17T09:14:32Z
depends_on:                        # list of input file SHA256 hashes
  - <sha256>
  - <sha256>
spec_task_id: <P#-T#>              # e.g., P1-T4
---
```

## For `.csv`, `.json`, and binary files

Frontmatter goes in a sidecar file named `<filename>.meta.yaml`. Example: `predictions/phase1.csv` has `predictions/phase1.csv.meta.yaml` next to it.

The sidecar carries the same four required fields plus any type-specific additions:

```yaml
generated_by: <agent_id>
generated_at: <ISO timestamp>
depends_on: [<sha256>, ...]
spec_task_id: <P#-T#>

# For CSVs, add schema
columns:
  - {name: <str>, type: <str>, unit: <str>, description: <str>}
record_count: <int>

# For predictions, add
columns_required: [system, n, l, j, quantity, predicted_value, uncertainty, method]
```

## Required file-type conventions (from spec §9)

- **data_files**: `.csv` with explicit header row; schema in adjacent `.yaml`.
- **derivations**: `.tex` for human reading; `.json` with sympy-parseable formula for machine consumption. Both for every derivation task.
- **predictions**: `.csv` with columns `[system, n, l, j, quantity, predicted_value, uncertainty, method]`.
- **validation_reports**: `.md` with required sections `[summary, comparison_table, verdict, recommendations]`.
- **figures**: `.png` for inline review, `.pdf` for publication. Both for every figure.

## Verification

Before any task is marked complete, every declared output file must:
1. Exist on disk.
2. Have either inline frontmatter (text types) or a `.meta.yaml` sidecar (binary/csv types).
3. Have all four required fields populated (no null/TODO).
4. For predictions CSVs, have all seven required columns.

If verification fails, the task stays `in_progress` and the orchestrator surfaces the gap.

## Helper script

`scripts/verify_handoff.py <path>` — walks a directory, checks every artifact has valid frontmatter, reports missing or malformed entries. Exit code non-zero on any failure.
