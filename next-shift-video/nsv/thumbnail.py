"""1280x720 thumbnail in the channel style: one huge idea, one accent, no clutter."""
from __future__ import annotations

from . import brand as B
from .compose import background, defs
from .fx import esc, fit_size, text, text_width, wrap


def render_thumbnail(project, path):
    import cairosvg
    sb = project.storyboard
    th = sb.get("thumbnail", {})
    headline = th.get("headline", sb.get("title", "")).upper()
    accent = {w.upper() for w in th.get("accent", [])}
    kicker = th.get("kicker", "")
    big = th.get("big")  # optional huge right-hand number/word
    out = [background(3.0)]
    bs = fit_size(big, 380, 620, B.F_BOLD) if big else 0
    big_left = B.W - 120 - (text_width(big, bs, B.F_BOLD) if big else 0)
    maxw = (big_left - 130 - 90) if big else B.W - 300
    size = 170
    lines = wrap(headline, size, maxw, B.F_BOLD, balance=True)
    while (len(lines) > 3 or any(text_width(l, size, B.F_BOLD) > maxw for l in lines)) and size > 70:
        size -= 6
        lines = wrap(headline, size, maxw, B.F_BOLD, balance=True)
    lh = size * 1.02
    y0 = B.H / 2 - (len(lines) - 1) * lh / 2 + size * 0.35
    for i, ln in enumerate(lines):
        x = 130
        for w in ln.split():
            col = B.ACCENT_2 if w.strip(".,?!") in accent else B.INK
            out.append(text(x, y0 + i * lh, w, size, col, B.F_BOLD))
            x += text_width(w + " ", size, B.F_BOLD)
    out.append(f'<rect x="130" y="{y0 - size - 30:.0f}" width="140" height="14" fill="{B.ACCENT}"/>')
    if kicker:
        out.append(text(300, y0 - size - 16, kicker.upper(), 40, B.INK_2, B.F_SEMI, spacing=6))
    if big:
        out.append(text(B.W - 120, B.H / 2 + bs * 0.35, big, bs, B.ACCENT, B.F_BOLD, "end"))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{B.W}" height="{B.H}" viewBox="0 0 {B.W} {B.H}">'
           f'{defs()}{"".join(out)}</svg>')
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(path), output_width=1280, output_height=720)
    return path
