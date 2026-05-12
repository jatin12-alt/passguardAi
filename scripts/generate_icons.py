"""
Generates PNG app icons for PassguardAI PWA (192 + 512, maskable-safe padding).
Requires Pillow. Run from repo root: python scripts/generate_icons.py
"""
from __future__ import annotations

import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "icons")


def find_bold_font() -> str | None:
    windir = os.environ.get("WINDIR", r"C:\Windows")
    candidates = [
        os.path.join(windir, "Fonts", "segoeuib.ttf"),
        os.path.join(windir, "Fonts", "arialbd.ttf"),
        os.path.join(windir, "Fonts", "calibrib.ttf"),
    ]
    for p in candidates:
        if os.path.isfile(p):
            return p
    return None


def draw_icon(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (7, 6, 15, 255))
    d = ImageDraw.Draw(img)
    pad = int(size * 0.08)
    cx, cy = size // 2, int(size * 0.46)
    # Shield
    top = pad + int(size * 0.06)
    left = pad
    right = size - pad
    bottom = size - pad - int(size * 0.06)
    midx = cx
    shield = [
        (midx, top),
        (right, top + int(size * 0.14)),
        (right, int(cy + size * 0.22)),
        (midx, bottom),
        (left, int(cy + size * 0.22)),
        (left, top + int(size * 0.14)),
    ]
    d.polygon(shield, fill=(26, 23, 48, 255), outline=(124, 251, 247, 255), width=max(2, size // 96))
    # Accent wedge
    wedge = [(midx, top + size // 12), (midx + size // 6, cy + size // 10), (midx - size // 6, cy + size // 10)]
    d.polygon(wedge, fill=(196, 181, 253, 200))

    font_path = find_bold_font()
    pg_size = int(size * 0.26)
    ai_size = int(size * 0.055)
    try:
        f_pg = ImageFont.truetype(font_path, pg_size) if font_path else ImageFont.load_default()
        f_ai = ImageFont.truetype(font_path, ai_size) if font_path else ImageFont.load_default()
    except OSError:
        f_pg = f_ai = ImageFont.load_default()

    d.text((cx, cy + int(size * 0.06)), "PG", fill=(124, 251, 247, 255), font=f_pg, anchor="mm")
    d.text((cx, cy + int(size * 0.16)), "AI", fill=(144, 136, 184, 255), font=f_ai, anchor="mm")
    return img


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for name, sz in (("icon-192.png", 192), ("icon-512.png", 512)):
        path = os.path.join(OUT, name)
        draw_icon(sz).save(path, "PNG")
        print("Wrote", path)


if __name__ == "__main__":
    sys.exit(main() or 0)
