"""Scene components. Each component is a pure function:

    component(params: dict, t: float, d: float) -> svg fragment

`t` is local scene time in seconds, `d` the scene duration. Components never
draw the background, camera, brand bug or source line - the compositor does.
Reveals are scheduled relative to `d` so a component adapts to narration length.

To add a component: write a function, decorate it with @component("name"),
and document its params in SCHEMAS (validate.py checks storyboards against it).
"""
from __future__ import annotations

import math

from . import brand as B
from .fx import (clamp, ease_in_out, ease_out, ease_out_back, esc, fit_size, fmt_num,
                 group, lerp, text, text_width, win, wrap)

REGISTRY = {}
SCHEMAS = {}  # name -> (required params, optional params)


def component(name, required=(), optional=()):
    def deco(fn):
        REGISTRY[name] = fn
        SCHEMAS[name] = (tuple(required), tuple(optional))
        return fn
    return deco


CX, CY = B.W / 2, B.H / 2


def soft_card(x, y, w, h, r, fill=None, opacity=1.0):
    """White-theme card: diffuse shadow, no outline."""
    fill = fill or B.BG_2
    return (f'<ellipse cx="{x + w / 2:.1f}" cy="{y + h + 10:.1f}" rx="{w * 0.5:.1f}" ry="{max(14, h * 0.12):.1f}" '
            f'fill="url(#softshadow)" opacity="{opacity:.2f}"/>'
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r:.1f}" fill="{fill}" opacity="{opacity:.3f}"/>')


def _reveal(t, d, i, n, start=0.25, span=0.55):
    """Stagger index i of n across [start, start+span] of the scene (fractions of d)."""
    if n <= 1:
        return win(t, start * d * 0.6, 0.6)
    step = span * d / n
    return ease_out(win(t, start * d * 0.4 + i * step, min(0.7, step * 1.5)))


def _kinetic_lines(lines, x, y0, size, lh, t, start, per_word, family, accent=(), anchor="middle",
                   color=None, accent_color=None):
    color, accent_color = color or B.INK, accent_color or B.ACCENT
    """Word-by-word rise-in typography. Returns (svg, end_time)."""
    out, k = [], 0
    accent_l = {a.lower().strip(".,!?:;") for a in accent}
    for li, line in enumerate(lines):
        words = line.split()
        lw = text_width(line, size, family)
        sp = text_width(" ", size, family)
        cx = x - lw / 2 if anchor == "middle" else x
        y = y0 + li * lh
        for w in words:
            p = ease_out(win(t, start + k * per_word, 0.45))
            ww = text_width(w, size, family)
            is_acc = w.lower().strip(".,!?:;\"'") in accent_l
            col = accent_color if is_acc else color
            out.append(text(cx, y + (1 - p) * size * 0.45, w, size, col, family, "start", p))
            if is_acc and p > 0.5:
                u = ease_out(win(t, start + k * per_word + 0.25, 0.5))
                out.append(f'<rect x="{cx:.1f}" y="{y + size * 0.2:.1f}" width="{ww * u:.1f}" '
                           f'height="{max(4, size * 0.07):.1f}" fill="{accent_color}"/>')
            cx += ww + sp
            k += 1
    return "".join(out), start + k * per_word


# ---------------------------------------------------------------------------
@component("chapter", required=("num", "title"))
def chapter(p, t, d):
    a = ease_out(win(t, 0.1, 0.6))
    line = ease_in_out(win(t, 0.2, 0.9))
    num = text(B.SAFE_X, CY - 70, f"{int(p['num']):02d}", 140, B.ACCENT, B.F_BOLD, opacity=a)
    bar = f'<rect x="{B.SAFE_X}" y="{CY - 30}" width="{600 * line:.1f}" height="{6 if B.SOFT else 3}" rx="3" fill="{B.ACCENT}"/>'
    size = fit_size(p["title"], 88, B.W - 2 * B.SAFE_X, B.F_BOLD)
    tl, _ = _kinetic_lines([p["title"]], B.SAFE_X, CY + 80, size, size * 1.1, t, 0.5, 0.12,
                           B.F_BOLD, anchor="start")
    return num + bar + tl


@component("title", required=("title",), optional=("kicker", "accent"))
def title(p, t, d):
    out = []
    if p.get("kicker"):
        a = ease_out(win(t, 0.1, 0.6))
        out.append(text(CX, CY - 170, p["kicker"].upper(), 30, B.ACCENT, B.F_SEMI, "middle", a, spacing=6))
    lines = wrap(p["title"], 104, B.W - 2 * B.SAFE_X - 100, B.F_BOLD, balance=True)
    y0 = CY - (len(lines) - 1) * 60 + 20
    tl, _ = _kinetic_lines(lines, CX, y0, 104, 120, t, 0.35, 0.11, B.F_BOLD, p.get("accent", []))
    out.append(tl)
    return "".join(out)


@component("statement", required=("text",), optional=("accent", "sub", "size"))
def statement(p, t, d):
    size = int(p.get("size", 76))
    lines = wrap(p["text"], size, B.W - 2 * B.SAFE_X - 80, B.F_BOLD, balance=True)
    lh = size * 1.18
    y0 = CY - (len(lines) - 1) * lh / 2 + size * 0.3 - (40 if p.get("sub") else 0)
    nwords = len(p["text"].split())
    per = min(0.22, max(0.06, d * 0.45 / max(nwords, 1)))
    tl, end = _kinetic_lines(lines, CX, y0, size, lh, t, 0.25, per, B.F_BOLD, p.get("accent", []))
    out = [tl]
    if p.get("sub"):
        a = ease_out(win(t, end + 0.2, 0.6))
        sy = y0 + (len(lines) - 1) * lh + 95
        for i, sl in enumerate(wrap(p["sub"], 36, 1300, B.F_REG, balance=True)):
            out.append(text(CX, sy + i * 48, sl, 36, B.INK_2, B.F_REG, "middle", a))
    return "".join(out)


@component("big_number", required=("value", "label"),
           optional=("prefix", "suffix", "decimals", "sub", "color", "from", "display"))
def big_number(p, t, d):
    """Counts up to `value`. Use `display` for ranges/text that must not count (e.g. "$52-56B")."""
    dec = int(p.get("decimals", 0))
    v0 = float(p.get("from", 0))
    prog = ease_out(win(t, 0.3, min(2.2, d * 0.45)))
    v = lerp(v0, float(p["value"]), prog)
    final = p.get("display") or f'{p.get("prefix", "")}{fmt_num(float(p["value"]), dec)}{p.get("suffix", "")}'
    s = final if p.get("display") else f'{p.get("prefix", "")}{fmt_num(v, dec)}{p.get("suffix", "")}'
    size = fit_size(final, 240, B.W - 2 * B.SAFE_X, B.F_BOLD)
    col = p.get("color", B.INK)
    col = {"accent": B.ACCENT, "lime": B.ACCENT_2, "warn": B.WARN}.get(col, col)
    a = ease_out(win(t, 0.15, 0.5))
    out = [text(CX, CY + 40, s, size, col, B.F_BOLD, "middle", a)]
    la = ease_out(win(t, 0.8, 0.6))
    out.append(text(CX, CY + 140, p["label"], 44, B.INK, B.F_SEMI, "middle", la))
    lw = text_width(p["label"], 44, B.F_SEMI)
    u = ease_in_out(win(t, 1.0, 0.8))
    out.append(f'<rect x="{CX - lw / 2:.1f}" y="{CY + 165}" width="{lw * u:.1f}" height="{6 if B.SOFT else 4}" rx="3" fill="{B.ACCENT}"/>')
    if p.get("sub"):
        sa = ease_out(win(t, 1.4, 0.6))
        for i, sl in enumerate(wrap(p["sub"], 34, 1300)):
            out.append(text(CX, CY + 235 + i * 46, sl, 34, B.INK_2, B.F_REG, "middle", sa))
    return "".join(out)


@component("bars", required=("items",), optional=("title", "highlight", "prefix", "suffix", "decimals", "max"))
def bars(p, t, d):
    items = p["items"]
    n = len(items)
    out = []
    top = B.SAFE_Y + 60
    if p.get("title"):
        out.append(text(B.SAFE_X, top + 40, p["title"], 52, B.INK, B.F_BOLD, opacity=ease_out(win(t, 0.1, 0.5))))
        top += 110
    vmax = float(p.get("max") or max(float(i["value"]) for i in items))
    label_w = 430
    bar_x = B.SAFE_X + label_w
    bar_wmax = B.W - B.SAFE_X - bar_x - 230
    gap = min(130, (B.H - B.SAFE_Y - top - 40) / max(n, 1))
    bh = min(64, gap * 0.55)
    hi = p.get("highlight")
    dec = int(p.get("decimals", 0))
    for i, it in enumerate(items):
        r = _reveal(t, d, i, n, 0.2, 0.5)
        y = top + 40 + i * gap
        col = B.ACCENT if (hi is None or hi == i) else B.INK_3
        if hi == i:
            col = B.ACCENT_2
        lsize = fit_size(it["label"], 38, label_w - 30, B.F_SEMI)
        out.append(text(bar_x - 30, y + bh * 0.68, it["label"], lsize,
                        B.INK if (hi is None or hi == i) else B.INK_2, B.F_SEMI, "end", r))
        w = bar_wmax * float(it["value"]) / vmax * ease_out(win(t, 0.25 * d * 0.4 + i * 0.5 * d / n + 0.1, 1.1))
        out.append(f'<rect x="{bar_x}" y="{y:.1f}" width="{max(w, 0):.1f}" height="{bh:.1f}" rx="{bh / 2 if B.SOFT else 4:.1f}" '
                   f'fill="{col}" opacity="{r:.3f}"/>')
        val = it.get("display") or f'{p.get("prefix", "")}{fmt_num(float(it["value"]), dec)}{p.get("suffix", "")}'
        out.append(text(bar_x + w + 20, y + bh * 0.68, val, 38, B.INK, B.F_BOLD, opacity=r))
    return "".join(out)


@component("share", required=("value", "label"), optional=("title", "sub"))
def share(p, t, d):
    v = float(p["value"])
    prog = ease_in_out(win(t, 0.3, min(2.0, d * 0.4)))
    r, cx, cy = 230, B.SAFE_X + 330, CY + 20
    circ = 2 * math.pi * r
    arc = circ * v / 100 * prog
    out = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{B.GRID}" stroke-width="44"/>',
           f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{B.ACCENT}" stroke-width="44" stroke-linecap="{"round" if B.SOFT else "butt"}" '
           f'stroke-dasharray="{arc:.1f} {circ:.1f}" transform="rotate(-90 {cx} {cy})"/>',
           text(cx, cy + 40, f"{v * prog:.0f}%", 120, B.INK, B.F_BOLD, "middle")]
    x = cx + r + 140
    a = ease_out(win(t, 0.6, 0.6))
    y = cy - 60
    if p.get("title"):
        out.append(text(x, y - 70, p["title"].upper(), 30, B.ACCENT, B.F_SEMI, opacity=a, spacing=5))
    for i, ln in enumerate(wrap(p["label"], 60, B.W - x - B.SAFE_X, B.F_BOLD)):
        out.append(text(x, y + i * 72, ln, 60, B.INK, B.F_BOLD, opacity=a))
        last = y + i * 72
    if p.get("sub"):
        sa = ease_out(win(t, 1.2, 0.6))
        for i, ln in enumerate(wrap(p["sub"], 34, B.W - x - B.SAFE_X)):
            out.append(text(x, last + 80 + i * 46, ln, 34, B.INK_2, B.F_REG, opacity=sa))
    return "".join(out)


@component("versus", required=("left", "right"), optional=("verdict", "title"))
def versus(p, t, d):
    out = []
    if p.get("title"):
        out.append(text(CX, B.SAFE_Y + 80, p["title"], 48, B.INK, B.F_BOLD, "middle", ease_out(win(t, 0.1, 0.5))))
    line = ease_in_out(win(t, 0.2, 0.8))
    out.append(f'<rect x="{CX - 1}" y="{CY - 260 * line:.1f}" width="2" height="{520 * line:.1f}" fill="{B.INK_3}"/>')
    for side, key, delay in ((-1, "left", 0.4), (1, "right", 0.4 + d * 0.25)):
        s = p[key]
        a = ease_out(win(t, delay, 0.6))
        x = CX + side * 420
        col = {"accent": B.ACCENT, "lime": B.ACCENT_2, "warn": B.WARN}.get(s.get("color", ""), B.INK)
        out.append(text(x, CY - 120, s["label"].upper(), 32, B.INK_2, B.F_SEMI, "middle", a, spacing=4))
        vs = fit_size(s["value"], 130, 760, B.F_BOLD)
        out.append(text(x, CY + 40 + (1 - a) * 30, s["value"], vs, col, B.F_BOLD, "middle", a))
        if s.get("note"):
            for i, ln in enumerate(wrap(s["note"], 32, 700)):
                out.append(text(x, CY + 130 + i * 44, ln, 32, B.INK_2, B.F_REG, "middle", a))
    if p.get("verdict"):
        va = ease_out(win(t, d * 0.65, 0.6))
        out.append(text(CX, B.H - B.SAFE_Y - 30, p["verdict"], 42, B.ACCENT_2, B.F_BOLD, "middle", va))
    return "".join(out)


@component("timeline", required=("events",), optional=("title",))
def timeline(p, t, d):
    ev = p["events"]
    n = len(ev)
    out = []
    if p.get("title"):
        out.append(text(B.SAFE_X, B.SAFE_Y + 90, p["title"], 52, B.INK, B.F_BOLD, opacity=ease_out(win(t, 0.1, 0.5))))
    x0, x1, y = B.SAFE_X + 40, B.W - B.SAFE_X - 40, CY + 40
    lp = ease_in_out(win(t, 0.3, d * 0.7))
    out.append(f'<rect x="{x0}" y="{y - 1}" width="{(x1 - x0) * lp:.1f}" height="3" fill="{B.INK_3}"/>')
    step = (x1 - x0) / max(n - 1, 1) if n > 1 else 0
    for i, e in enumerate(ev):
        x = x0 + i * step if n > 1 else CX
        frac = (x - x0) / (x1 - x0) if n > 1 else 0
        a = ease_out_back(win(t, 0.3 + frac * d * 0.7, 0.5))
        if a <= 0:
            continue
        last = i == n - 1
        col = B.ACCENT_2 if last else B.ACCENT
        out.append(f'<circle cx="{x:.1f}" cy="{y}" r="{14 * a:.1f}" fill="{col}"/>')
        up = i % 2 == 0
        ty = y - 60 if up else y + 95
        out.append(text(x, ty, str(e["year"]), 46, col, B.F_BOLD, "middle", clamp(a)))
        lines = wrap(e["label"], 30, max(min(step * 0.9, 520), 240) if n > 1 else 600, balance=True)
        lw = max(text_width(ln, 30) for ln in lines)
        lx = clamp(x, B.SAFE_X - 60 + lw / 2, B.W - B.SAFE_X + 60 - lw / 2)  # keep labels in frame
        for j, ln in enumerate(lines if up else lines):
            yy = (ty - 60 - (len(lines) - 1 - j) * 40) if up else (ty + 50 + j * 40)
            out.append(text(lx, yy, ln, 30, B.INK_2, B.F_REG, "middle", clamp(a)))
    return "".join(out)


@component("chain", required=("nodes",), optional=("title", "highlight", "caption"))
def chain(p, t, d):
    nodes = p["nodes"]
    n = len(nodes)
    hi = p.get("highlight")
    out = []
    if p.get("title"):
        out.append(text(CX, B.SAFE_Y + 100, p["title"], 50, B.INK, B.F_BOLD, "middle", ease_out(win(t, 0.1, 0.5))))
    bw, bh = min(300, (B.W - 2 * B.SAFE_X - (n - 1) * 70) / n), 170
    total = n * bw + (n - 1) * 70
    x0, y = CX - total / 2, CY - bh / 2 + 20
    for i, nd in enumerate(nodes):
        a = _reveal(t, d, i, n, 0.15, 0.5)
        x = x0 + i * (bw + 70)
        is_hi = hi == i
        stroke = B.ACCENT_2 if is_hi else B.ACCENT
        if B.SOFT:
            out.append(soft_card(x, y + (1 - a) * 30, bw, bh, min(bh / 2, B.CARD_RADIUS),
                                 "#EEF6E2" if is_hi else None, a))
        elif is_hi and a > 0.9:  # glow ring
            g = 0.5 + 0.5 * math.sin(t * 3)
            out.append(f'<rect x="{x - 10}" y="{y - 10}" width="{bw + 20}" height="{bh + 20}" rx="18" fill="none" '
                       f'stroke="{B.ACCENT_2}" stroke-width="2" opacity="{0.25 + 0.35 * g:.2f}"/>')
        if not B.SOFT:
            out.append(f'<rect x="{x:.1f}" y="{y + (1 - a) * 30:.1f}" width="{bw:.1f}" height="{bh}" rx="12" '
                       f'fill="{B.BG_2}" stroke="{stroke}" stroke-width="{3 if is_hi else 2}" opacity="{a:.3f}"/>')
        ls = fit_size(nd["label"], 40, bw - 30, B.F_BOLD)
        out.append(text(x + bw / 2, y + 78 + (1 - a) * 30, nd["label"], ls, B.INK, B.F_BOLD, "middle", a))
        if nd.get("sub"):
            for j, ln in enumerate(wrap(nd["sub"], 28, bw - 30)[:2]):
                out.append(text(x + bw / 2, y + 120 + j * 34 + (1 - a) * 30, ln, 28, B.INK_2, B.F_REG, "middle", a))
        if i < n - 1:
            ap = _reveal(t, d, i + 0.6, n, 0.15, 0.5)
            ax0, ax1 = x + bw + 10, x + bw + 60
            out.append(f'<line x1="{ax0:.1f}" y1="{y + bh / 2:.1f}" x2="{lerp(ax0, ax1, ap):.1f}" y2="{y + bh / 2:.1f}" '
                       f'stroke="{B.INK_3}" stroke-width="3"/>')
            if ap > 0.95:
                out.append(f'<path d="M{ax1 - 12:.1f},{y + bh / 2 - 9:.1f} L{ax1:.1f},{y + bh / 2:.1f} '
                           f'L{ax1 - 12:.1f},{y + bh / 2 + 9:.1f}" fill="none" stroke="{B.INK_3}" stroke-width="3"/>')
    if p.get("caption"):
        out.append(text(CX, y + bh + 130, p["caption"], 38, B.INK_2, B.F_REG, "middle", ease_out(win(t, d * 0.7, 0.6))))
    return "".join(out)


@component("hub", required=("center", "spokes"), optional=("title", "flow"))
def hub(p, t, d):
    sp = p["spokes"]
    n = len(sp)
    cx, cy, R = CX, CY + 30, 340
    out = []
    if p.get("title"):
        out.append(text(CX, B.SAFE_Y + 40, p["title"], 46, B.INK, B.F_BOLD, "middle", ease_out(win(t, 0.1, 0.5))))
    ca = ease_out_back(win(t, 0.2, 0.7))
    for i, s in enumerate(sp):
        ang = -math.pi / 2 + 2 * math.pi * i / n
        x, y = cx + R * math.cos(ang) * 1.45, cy + R * math.sin(ang)
        a = _reveal(t, d, i, n, 0.2, 0.45)
        if a <= 0:
            continue
        lx = lerp(cx, x, a)
        ly = lerp(cy, y, a)
        out.append(f'<line x1="{cx}" y1="{cy}" x2="{lx:.1f}" y2="{ly:.1f}" stroke="{B.INK_3}" stroke-width="2" opacity="{a:.2f}"/>')
        if p.get("flow", True) and a >= 1:  # money/data pulses flowing into the hub
            ph = ((t * 0.45 + i / n) % 1.0)
            px, py = lerp(x, cx, ph), lerp(y, cy, ph)
            out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="{B.ACCENT_2}" opacity="{0.9 * (1 - ph * 0.5):.2f}"/>')
        w = text_width(s, 32, B.F_SEMI) + 48
        if B.SOFT:
            out.append(soft_card(lx - w / 2, ly - 32, w, 64, 32, None, a))
        else:
            out.append(f'<rect x="{lx - w / 2:.1f}" y="{ly - 32:.1f}" width="{w:.1f}" height="64" rx="32" '
                       f'fill="{B.BG_2}" stroke="{B.ACCENT}" stroke-width="2" opacity="{a:.2f}"/>')
        out.append(text(lx, ly + 11, s, 32, B.INK, B.F_SEMI, "middle", a))
    cr = 120 * ca
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{max(cr, 0):.1f}" fill="{B.ACCENT}"/>')
    if ca > 0.5:
        cs = fit_size(p["center"], 46, 220, B.F_BOLD)
        out.append(text(cx, cy + cs * 0.36, p["center"], cs, B.BG, B.F_BOLD, "middle", clamp(ca)))
    return "".join(out)


@component("list", required=("items",), optional=("title",))
def listing(p, t, d):
    items = p["items"]
    n = len(items)
    out = []
    y = B.SAFE_Y + 100
    if p.get("title"):
        out.append(text(B.SAFE_X, y, p["title"], 56, B.INK, B.F_BOLD, opacity=ease_out(win(t, 0.1, 0.5))))
        y += 110
    gap = min(150, (B.H - B.SAFE_Y - y) / max(n, 1))
    for i, it in enumerate(items):
        a = _reveal(t, d, i, n, 0.15, 0.6)
        yy = y + 40 + i * gap
        out.append(text(B.SAFE_X + (1 - a) * -40, yy, f"{i + 1:02d}", 48, B.ACCENT, B.F_BOLD, opacity=a))
        for j, ln in enumerate(wrap(it, 46, B.W - 2 * B.SAFE_X - 140, B.F_SEMI)[:2]):
            out.append(text(B.SAFE_X + 130 + (1 - a) * -40, yy + j * 54, ln, 46, B.INK, B.F_SEMI, opacity=a))
    return "".join(out)


@component("quote", required=("text", "who"), optional=("role",))
def quote(p, t, d):
    lines = wrap(p["text"], 60, 1350, B.F_MED, balance=True)
    y0 = CY - (len(lines) - 1) * 40 - 30
    out = [text(CX - 720, y0 - 40, "“", 220, B.ACCENT, B.F_BOLD, opacity=ease_out(win(t, 0.1, 0.5)))]
    tl, end = _kinetic_lines(lines, CX, y0 + 20, 60, 80, t, 0.3, min(0.12, d * 0.4 / max(len(p["text"].split()), 1)),
                             B.F_MED)
    out.append(tl)
    a = ease_out(win(t, end + 0.2, 0.6))
    yy = y0 + len(lines) * 80 + 60
    out.append(text(CX, yy, "— " + p["who"], 38, B.INK, B.F_SEMI, "middle", a))
    if p.get("role"):
        out.append(text(CX, yy + 50, p["role"], 30, B.INK_2, B.F_REG, "middle", a))
    return "".join(out)


@component("dots", required=("total", "highlight", "label"), optional=("sub",))
def dots(p, t, d):
    total, hl = int(p["total"]), int(p["highlight"])
    cols = 10 if total > 10 else 5
    rows = math.ceil(total / cols)
    s = 58 if total > 20 else 120
    x0 = B.SAFE_X + 60
    y0 = CY - rows * s / 2 + 20
    out = []
    for i in range(total):
        r, c = divmod(i, cols)
        a = ease_out(win(t, 0.2 + i * min(0.04, d * 0.3 / total), 0.3))
        on = i < hl and t > 0.2 + total * min(0.04, d * 0.3 / total) + 0.3 + i * 0.03
        col = B.ACCENT if on else B.GRID
        out.append(f'<circle cx="{x0 + c * s:.1f}" cy="{y0 + r * s:.1f}" r="{(20 if s < 100 else 44) * a:.1f}" fill="{col}"/>')
    x = x0 + cols * s + 40
    la = ease_out(win(t, d * 0.35, 0.6))
    for i, ln in enumerate(wrap(p["label"], 64, B.W - x - B.SAFE_X, B.F_BOLD)):
        out.append(text(x, CY - 40 + i * 76, ln, 64, B.INK, B.F_BOLD, opacity=la))
    if p.get("sub"):
        for i, ln in enumerate(wrap(p["sub"], 34, B.W - x - B.SAFE_X)):
            out.append(text(x, CY + 130 + i * 46, ln, 34, B.INK_2, B.F_REG, opacity=ease_out(win(t, d * 0.5, 0.6))))
    return "".join(out)


@component("end", optional=("next",))
def end(p, t, d):
    a = ease_out(win(t, 0.2, 0.8))
    out = [text(CX, CY - 40, B.CHANNEL, 110, B.INK, B.F_BOLD, "middle", a, spacing=8),
           f'<rect x="{CX - 300 * a:.1f}" y="{CY + 5}" width="{600 * a:.1f}" height="4" fill="{B.ACCENT}"/>',
           text(CX, CY + 80, B.TAGLINE, 40, B.INK_2, B.F_LIGHT, "middle", ease_out(win(t, 0.8, 0.8)))]
    if p.get("next"):
        out.append(text(CX, CY + 220, "NEXT: " + p["next"], 34, B.ACCENT_2, B.F_SEMI, "middle",
                        ease_out(win(t, 1.4, 0.8)), spacing=2))
    return "".join(out)


def names():
    return sorted(REGISTRY)
