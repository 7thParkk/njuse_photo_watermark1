from __future__ import annotations

import os
from typing import Optional, Tuple


def ensure_output_dir(input_path: str) -> str:
    if os.path.isfile(input_path):
        parent = os.path.dirname(input_path)
        base_dir = os.path.basename(parent)
        out_dir = os.path.join(parent, f"{base_dir}_watermark")
    else:
        parent = input_path
        base_dir = os.path.basename(os.path.normpath(input_path))
        out_dir = os.path.join(parent, f"{base_dir}_watermark")

    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def get_output_path(
    input_file: str,
    output_dir: str,
    suffix: str = "",
    ext: Optional[str] = None,
    overwrite: bool = False,
) -> str:
    name, original_ext = os.path.splitext(os.path.basename(input_file))
    out_ext = (ext or original_ext.lstrip(".")).lower()
    if not out_ext.startswith("."):
        out_ext = "." + out_ext

    candidate = os.path.join(output_dir, f"{name}{suffix}{out_ext}")
    if overwrite or not os.path.exists(candidate):
        return candidate

    # Incremental naming: name (1).ext
    index = 1
    while True:
        cand = os.path.join(output_dir, f"{name}{suffix} ({index}){out_ext}")
        if not os.path.exists(cand):
            return cand
        index += 1


