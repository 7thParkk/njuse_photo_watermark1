from __future__ import annotations

import datetime as _dt
import os
from typing import Optional

import exifread


EXIF_CANDIDATE_TAGS = (
    "EXIF DateTimeOriginal",
    "EXIF CreateDate",
    "Image DateTime",
)


def _parse_exif_datetime(value: str) -> Optional[_dt.datetime]:
    # Common EXIF format: YYYY:MM:DD HH:MM:SS
    try:
        return _dt.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception:
        return None


def read_capture_datetime(image_path: str) -> Optional[_dt.datetime]:
    """Read capture datetime from EXIF. Return None if not found."""
    try:
        with open(image_path, "rb") as f:
            tags = exifread.process_file(f, details=False, stop_tag="EXIF DateTimeOriginal")
    except Exception:
        return None

    for key in EXIF_CANDIDATE_TAGS:
        v = tags.get(key)
        if not v:
            continue
        parsed = _parse_exif_datetime(str(v))
        if parsed:
            return parsed
    return None


def format_date(dt: _dt.datetime, fmt: str) -> str:
    # Map custom tokens to strftime
    mapping = {
        "YYYY": dt.strftime("%Y"),
        "MM": dt.strftime("%m"),
        "DD": dt.strftime("%d"),
    }
    out = fmt
    for k, v in mapping.items():
        out = out.replace(k, v)
    return out


def get_date_text_for_image(
    image_path: str,
    date_format: str,
    use_file_time_fallback: bool = True,
) -> Optional[str]:
    dt = read_capture_datetime(image_path)
    if dt is None and use_file_time_fallback:
        try:
            stat = os.stat(image_path)
            # Use creation time where available; st_mtime as fallback
            timestamp = getattr(stat, "st_ctime", stat.st_mtime)
            dt = _dt.datetime.fromtimestamp(timestamp)
        except Exception:
            dt = None

    if dt is None:
        return None
    # Only keep date component
    dt = _dt.datetime(dt.year, dt.month, dt.day)
    return format_date(dt, date_format)


