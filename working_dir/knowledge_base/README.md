---
generated_by: prism-librarian
generated_at: 2026-04-16T00:00:00Z
spec_task_id: bootstrap
depends_on: []
spec_version: "1.0"
artifact_type: knowledge_base_index
---

# PRISM Knowledge Base

This directory holds immutable, citation-backed reference values used throughout
the validation program. Writes are append-only; corrections go through the
`revision_history` field of the affected file rather than rewrites.

## Files

| File | Contents | Consumed by tasks |
|------|----------|-------------------|
| `literature_values.yaml` | All Appendix-A measurements: Bethe logs, Lamb shifts, proton radii, α running, CODATA constants, φ. | P1-T5 (gate), P2-T1, P2-T3, P3-T1, P3-T3 |
| `README.md` | This index. | — |

## Contract

Every numerical value in this directory carries three mandatory fields:

- `value` — number in the canonical units stated adjacent
- `uncertainty` — 1σ combined uncertainty in the same units (may be `0` for exact-by-definition constants)
- `citation_key` — key resolvable against `templates/source_urls.yaml`, OR a DOI string

Pipeline agents comparing predictions to literature MUST read from this directory,
never from inline literals. If a needed value is missing, the consuming task
halts with an ESCALATE_TO_USER block rather than guessing.

## Updating

Only `prism-librarian` writes here. When a new reference is added:

1. Add entry to `literature_values.yaml` with a `revision_history` block.
2. Add the source to `templates/source_urls.yaml` with its citation key.
3. Record the update in `working_dir/librarian_log.md`.
