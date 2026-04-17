"""
Atomic JSON writer for PRISM working-directory state files.

INTEGRATION NOTE
----------------
No Python process currently writes phase_status.json or current_state.json
directly — those files are written by Claude agent tool calls (Write/Edit).
The truncation bug in phase_status.json (commit 3cb619b) was caused by an
interrupted agent write, not a Python crash.

Integration points when a Python orchestrator is added:
  - Any script that updates working_dir/phase_status.json
  - Any script that updates working_dir/current_state.json
  - Any future script that updates working_dir/checkpoints/approved.yaml
    (YAML variant: serialize with PyYAML then pass the string to write_atomic)

Usage:
    from working_dir.utils.atomic_write import write_json_atomic
    write_json_atomic("working_dir/phase_status.json", data_dict)
"""

import json
import os


def write_json_atomic(path: str, data: object, indent: int = 2) -> None:
    """Write *data* as JSON to *path* atomically.

    Writes to a .tmp sibling, fsyncs, then uses os.replace() so the target
    file is never left in a partially-written state if the process is
    interrupted.  os.replace() is atomic on POSIX and as close as Windows
    allows (it is atomic with respect to other processes reading the file).
    """
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def write_text_atomic(path: str, text: str) -> None:
    """Write *text* to *path* atomically (for YAML or other text formats)."""
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)
