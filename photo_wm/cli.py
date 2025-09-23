from __future__ import annotations

import os
import sys
import logging
from typing import Optional

import typer

from .main import run


app = typer.Typer(add_completion=False, help="Add EXIF date watermark to photos.")


@app.command()
def apply(
    path: str = typer.Argument(..., help="Path to an image file or a directory"),
    font_size: int = typer.Option(32, "--font-size", "-s", help="Font size in points"),
    color: str = typer.Option("#FFFFFF", "--color", "-c", help="Text color (hex or name)"),
    position: str = typer.Option(
        "bottom-right",
        "--position",
        "-p",
        help="Watermark position: top-left|top-right|center|bottom-left|bottom-right",
    ),
    margin: int = typer.Option(16, "--margin", "-m", help="Margin in pixels"),
    date_format: str = typer.Option("YYYY-MM-DD", "--date-format", "-f", help="Date format"),
    font_path: Optional[str] = typer.Option(None, "--font-path", help="Path to a .ttf/.ttc font"),
    recursive: bool = typer.Option(False, "--recursive", "-r", help="Recurse into subdirectories"),
    fallback_filetime: bool = typer.Option(True, "--fallback-filetime/--no-fallback-filetime", help="Use file time when EXIF missing"),
    suffix: str = typer.Option("", "--suffix", help="Output filename suffix"),
    overwrite: bool = typer.Option(False, "--overwrite", help="Overwrite existing outputs"),
    ext: Optional[str] = typer.Option(None, "--ext", help="Output format: jpg|png|webp|tiff"),
    quality: int = typer.Option(90, "--quality", help="Output quality for JPEG/WEBP"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without writing files"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose logging"),
):
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="[%(levelname)s] %(message)s",
    )
    try:
        run(
            path=path,
            font_size=font_size,
            color=color,
            position=position,
            margin=margin,
            date_format=date_format,
            font_path=font_path,
            recursive=recursive,
            fallback_filetime=fallback_filetime,
            suffix=suffix,
            overwrite=overwrite,
            ext=ext,
            quality=quality,
            dry_run=dry_run,
        )
    except Exception as exc:
        logging.getLogger(__name__).error(str(exc))
        raise typer.Exit(code=1)


def main():
    app()


