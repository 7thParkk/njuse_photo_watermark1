from __future__ import annotations

from typing import Tuple

from PIL import Image, ImageDraw, ImageFont


def load_font(font_path: str | None, font_size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        if font_path:
            return ImageFont.truetype(font_path, font_size)
    except Exception:
        pass
    # Fallback to default PIL font (bitmap). Not ideal for CJK, but ensures progress.
    try:
        return ImageFont.load_default()
    except Exception:
        return ImageFont.load_default()


def measure_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> Tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    return width, height


def compute_position(
    image_size: Tuple[int, int],
    text_size: Tuple[int, int],
    position: str,
    margin: int,
) -> Tuple[int, int]:
    img_w, img_h = image_size
    txt_w, txt_h = text_size
    pos = position.lower()

    if pos == "top-left":
        return margin, margin
    if pos == "top-right":
        return max(margin, img_w - txt_w - margin), margin
    if pos == "center":
        return (img_w - txt_w) // 2, (img_h - txt_h) // 2
    if pos == "bottom-left":
        return margin, max(margin, img_h - txt_h - margin)
    # default bottom-right
    return max(margin, img_w - txt_w - margin), max(margin, img_h - txt_h - margin)


def draw_watermark(
    image: Image.Image,
    text: str,
    color: str,
    font_path: str | None,
    font_size: int,
    position: str,
    margin: int,
) -> Image.Image:
    # Work on a copy, ensure RGBA for alpha-safe drawing
    if image.mode not in ("RGB", "RGBA"):
        base = image.convert("RGBA")
    else:
        base = image.copy()

    font = load_font(font_path, font_size)
    draw = ImageDraw.Draw(base)
    text_w, text_h = measure_text(draw, text, font)
    x, y = compute_position(base.size, (text_w, text_h), position, margin)

    # Optional subtle shadow for readability
    shadow_offset = 1
    try:
        draw.text((x + shadow_offset, y + shadow_offset), text, fill="#00000080", font=font)
    except Exception:
        # Some modes may not accept alpha in hex; fallback to opaque black shadow
        draw.text((x + shadow_offset, y + shadow_offset), text, fill="#000000", font=font)

    draw.text((x, y), text, fill=color, font=font)
    return base


