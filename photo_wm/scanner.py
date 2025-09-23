from __future__ import annotations

import os
from typing import Iterable, List


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".tiff", ".tif"}


def is_image_file(path: str) -> bool:
    _, ext = os.path.splitext(path)
    return ext.lower() in SUPPORTED_EXTENSIONS


def collect_files(input_path: str, recursive: bool) -> List[str]:
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Path does not exist: {input_path}")

    if os.path.isfile(input_path):
        return [input_path] if is_image_file(input_path) else []

    collected: List[str] = []
    if recursive:
        for root, _, files in os.walk(input_path):
            for name in files:
                full = os.path.join(root, name)
                if is_image_file(full):
                    collected.append(full)
    else:
        for name in os.listdir(input_path):
            full = os.path.join(input_path, name)
            if os.path.isfile(full) and is_image_file(full):
                collected.append(full)

    collected.sort()
    return collected


