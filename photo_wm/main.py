from __future__ import annotations

import logging
from typing import Optional, Tuple

from PIL import Image

from .scanner import collect_files
from .exif_reader import get_date_text_for_image
from .watermark import draw_watermark
from .io_utils import ensure_output_dir, get_output_path


logger = logging.getLogger(__name__)


def run(
    *,
    path: str,
    font_size: int,
    color: str,
    position: str,
    margin: int,
    date_format: str,
    font_path: Optional[str],
    recursive: bool,
    fallback_filetime: bool,
    suffix: str,
    overwrite: bool,
    ext: Optional[str],
    quality: int,
    dry_run: bool,
) -> None:
    files = collect_files(path, recursive)
    if not files:
        logger.warning("No image files found to process.")
        return

    output_dir = ensure_output_dir(path)
    logger.info("Output directory: %s", output_dir)

    total = len(files)
    success = 0
    skipped = 0

    for fp in files:
        date_text = get_date_text_for_image(fp, date_format, use_file_time_fallback=fallback_filetime)
        if not date_text:
            logger.warning("Skip (no date): %s", fp)
            skipped += 1
            continue

        out_path = get_output_path(fp, output_dir, suffix=suffix, ext=ext, overwrite=overwrite)
        logger.debug("%s -> %s | text=%s", fp, out_path, date_text)

        if dry_run:
            success += 1
            continue

        try:
            with Image.open(fp) as im:
                result = draw_watermark(
                    image=im,
                    text=date_text,
                    color=color,
                    font_path=font_path,
                    font_size=font_size,
                    position=position,
                    margin=margin,
                )
                save_kwargs = {}
                if ext:
                    fmt = ext.lower().lstrip(".")
                    save_kwargs["format"] = fmt.upper()
                if (ext or im.format) in ("JPEG", "JPG", "WEBP", "webp", "jpeg", "jpg"):
                    save_kwargs["quality"] = quality
                result.save(out_path, **save_kwargs)
            success += 1
        except Exception as e:
            logger.error("Failed: %s (%s)", fp, e)
            skipped += 1

    logger.info("Processed: %s | Success: %s | Skipped: %s", total, success, skipped)


