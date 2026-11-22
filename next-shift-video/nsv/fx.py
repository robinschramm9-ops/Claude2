"""Low-level helpers: easing, timing windows, SVG escaping, text measurement."""
from __future__ import annotations

import functools
import math
import os
from xml.sax.saxutils import escape

from . import brand


# Easing ------------------------------------------------------------------
def clamp(x, lo=0.0, hi=1.0):
    return lo if x < lo else hi if x > hi else x


def ease_out(x):  # cubic
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_in_out(x):
    x = clamp(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def ease_out_back(x, s=1.4):
    x = clamp(x)
    return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


def win(t, start, dur):
    """Progress 0..1 of an animation that starts at `start` and lasts `dur` seconds."""
    if dur <= 0:
        return 1.0 if t >= start else 0.0
    return clamp((t - start) / dur)


def lerp(a, b, p):
    return a + (b - a) * p


# SVG -----------------------------------------------------------------------
def esc(s) -> str:
    return escape(str(s), {'"': "&quot;"})


def text(x, y, s, size, fill=brand.INK, family=brand.F_REG, anchor="start",
         opacity=1.0, spacing=0, extra=""):
    if opacity <= 0.001:
        return ""
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" opacity="{opacity:.3f}"{ls} {extra}>'
            f'{esc(s)}</text>')


def group(content, opacity=1.0, tx=0.0, ty=0.0, scale=1.0, cx=None, cy=None):
    if opacity <= 0.001 or not content:
        return ""
    tf = []
    if tx or ty:
        tf.append(f"translate({tx:.2f} {ty:.2f})")
    if scale != 1.0:
        cx = brand.W / 2 if cx is None else cx
        cy = brand.H / 2 if cy is None else cy
        tf.append(f"translate({cx:.2f} {cy:.2f}) scale({scale:.4f}) translate({-cx:.2f} {-cy:.2f})")
    t = f' transform="{" ".join(tf)}"' if tf else ""
    o = f' opacity="{opacity:.3f}"' if opacity < 0.999 else ""
    return f"<g{t}{o}>{content}</g>"


def fmt_num(v: float, decimals: int = 0) -> str:
    if decimals == 0:
        return f"{int(round(v)):,}"
    return f"{v:,.{decimals}f}"


# Text measurement ------------------------------------------------------------
@functools.lru_cache(maxsize=None)
def _font_path(family: str):
    fname = brand.FONT_FILES.get(family)
    if not fname:
        return None
    for d in brand.FONT_DIRS:
        p = os.path.join(os.path.expanduser(d), fname)
        if os.path.exists(p):
            return p
    return None


@functools.lru_cache(maxsize=None)
def _pil_font(family: str, size: int):
    from PIL import ImageFont
    p = _font_path(family)
    if p:
        return ImageFont.truetype(p, size)
    return None


def text_width(s: str, size: int, family: str = brand.F_REG, spacing: float = 0) -> float:
    f = _pil_font(family, int(size))
    if f is None:  # rough fallback if Inter is missing
        w = 0.56 * size * len(s)
    else:
        w = f.getlength(s)
    return w + spacing * max(len(s) - 1, 0)


def wrap(s: str, size: int, max_w: float, family: str = brand.F_REG, balance: bool = False) -> list[str]:
    """Greedy word wrap. balance=True evens out line lengths (no orphaned last word)."""
    lines = _greedy(s, size, max_w, family)
    if balance and len(lines) > 1:
        lo, hi = max_w * 0.3, max_w
        for _ in range(14):  # narrowest width that keeps the same number of lines
            mid = (lo + hi) / 2
            if len(_greedy(s, size, mid, family)) > len(lines):
                lo = mid
            else:
                hi = mid
        lines = _greedy(s, size, hi, family)
    return lines


def _greedy(s, size, max_w, family):
    words, lines, cur = s.split(), [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if cur and text_width(cand, size, family) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = cand
    if cur:
        lines.append(cur)
    return lines


def fit_size(s: str, size: int, max_w: float, family: str, min_size: int = brand.MIN_TEXT_PX) -> int:
    """Shrink a single-line string until it fits max_w (never below min_size)."""
    while size > min_size and text_width(s, size, family) > max_w:
        size -= 2
    return size


def sin01(t, period):
    return 0.5 + 0.5 * math.sin(2 * math.pi * t / period)
