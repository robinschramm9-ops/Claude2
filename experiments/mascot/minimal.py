"""Round 2: restrained, minimal-face mascot concepts (calibration board only).

Design rules for this round (lessons from round 1, which read as childish):
  - no mouth, no blush, no sparkly cartoon pupils, no costume props
  - matte materials (ceramic, brushed metal, dark glass), one lime accent at most
  - personality from posture, head tilt and a single minimal "eye" element
  - silhouette derived from the subject matter (semiconductors, instruments)
"""
from __future__ import annotations

import math
import os

import cairosvg

W, H = 1920, 1080
OUT = os.path.join(os.path.dirname(__file__), "out")
LIME = "#B6F23A"

DEFS = (
    '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0F1116"/><stop offset="1" stop-color="#090A0D"/></linearGradient>'
    '<radialGradient id="pool" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.07"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>'
    '<radialGradient id="shadow"><stop offset="0" stop-color="#000" stop-opacity="0.85"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
    '<linearGradient id="ceramic" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4A505C"/><stop offset="0.45" stop-color="#363B45"/><stop offset="1" stop-color="#1E2128"/></linearGradient>'
    '<linearGradient id="visor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05060A"/><stop offset="1" stop-color="#14171E"/></linearGradient>'
    '<linearGradient id="silver" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8A93A2"/><stop offset="0.3" stop-color="#E4E8EE"/>'
    '<stop offset="0.62" stop-color="#A9B1BE"/><stop offset="1" stop-color="#5D6573"/></linearGradient>'
    '<linearGradient id="graphite" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3A3F49"/><stop offset="0.5" stop-color="#5A616E"/><stop offset="1" stop-color="#2A2E36"/></linearGradient>'
    '<radialGradient id="lens" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#2A3446"/><stop offset="1" stop-color="#05070B"/></radialGradient>'
)


def T(x, y, s, size, fill="#E9EBEF", fam="Inter", anchor="start", ls=0, op=1):
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'letter-spacing="{ls}" opacity="{op}">{s}</text>')


def limb(pts, w=7, color="#5A616E"):
    """Segmented, slightly mechanical limb with joint discs (reads 'precise', not 'noodle')."""
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    joints = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{w * 0.62:.1f}" fill="#2A2E36" stroke="{color}" stroke-width="1.5"/>' for x, y in pts[1:-1])
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>{joints}'


def arm(sx, sy, a1, a2, l1=42, l2=40, w=7, color="#5A616E", tip="#8A919D"):
    """Two-segment arm: a1 = upper-arm angle, a2 = forearm angle (degrees; 0 = down, 90 = forward)."""
    ex, ey = sx + l1 * math.sin(math.radians(a1)), sy + l1 * math.cos(math.radians(a1))
    hx, hy = ex + l2 * math.sin(math.radians(a2)), ey + l2 * math.cos(math.radians(a2))
    return limb([(sx, sy), (ex, ey), (hx, hy)], w, color) + f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{w * 0.95:.1f}" fill="{tip}"/>'


def legs(hip_y, spread, w=9, color="#4A505C", foot="#2A2E36", stride=0.0):
    o = []
    for s in (-1, 1):
        fx = s * spread + stride * s * 10
        o.append(limb([(s * spread * 0.8, hip_y), (s * spread * 0.9 + 3, hip_y / 2), (fx, -6)], w, color))
        o.append(f'<rect x="{fx - 14:.1f}" y="-10" width="30" height="10" rx="4" fill="{foot}"/>')
    return "".join(o)


def place(x, y, s, body, tilt=0, facing=1):
    return (f'<ellipse cx="{x}" cy="{y + 2}" rx="{80 * s}" ry="{12 * s}" fill="url(#shadow)" opacity="0.7"/>'
            f'<g transform="translate({x} {y}) rotate({tilt * facing}) scale({s * facing} {s})">{body}</g>')


# ------------------------------------------------------------------------------------------------
# A. VISOR: a matte ceramic capsule. Its only feature is a dark visor with one lime light-line.
#    The line IS the expression: long = attentive, short = focused, arc = approving, split = doubt.
def visor(pose="neutral", a=(15, 10), b=(10, 5)):
    line = {"neutral": "M-30,-162 H30", "focus": "M-12,-162 H12", "approve": "M-30,-166 Q0,-152 30,-166",
            "doubt": "M-30,-162 H-8 M8,-160 H30"}[pose]
    return (legs(-40, 22) + arm(-58, -150, -a[0], -a[1], color="#4A505C") +
            '<rect x="-62" y="-232" width="124" height="196" rx="56" fill="url(#ceramic)"/>'
            '<rect x="-62" y="-232" width="124" height="196" rx="56" fill="none" stroke="#5E6572" stroke-width="1.5"/>'
            '<rect x="-48" y="-182" width="96" height="40" rx="20" fill="url(#visor)"/>'
            f'<path d="{line}" fill="none" stroke="{LIME}" stroke-width="5" stroke-linecap="round"/>'
            f'<path d="{line}" fill="none" stroke="{LIME}" stroke-width="14" stroke-linecap="round" opacity="0.15"/>'
            '<path d="M-44,-212 Q-52,-150 -46,-70" fill="none" stroke="#fff" stroke-width="3" opacity="0.07"/>' +
            arm(58, -150, a[0] if False else b[0], b[1]))


# B. APERTURE: a precision instrument. Lens head on a slim neck; the iris aperture is the eye:
#    wide = curious/surprised, narrow = scrutinising. Head tilt carries the attitude (lamp-like).
def aperture(open_=0.55, tilt=0, look=0.0, a=(15, 10), b=(10, 5)):
    r_out, r_in = 44, 16 + 24 * open_
    blades = []
    for i in range(6):
        t0 = math.radians(i * 60 + 15)
        t1 = math.radians(i * 60 + 75)
        blades.append(f'M{r_in * math.cos(t0) + look * 6:.1f},{r_in * math.sin(t0):.1f} L{r_out * math.cos(t1):.1f},{r_out * math.sin(t1):.1f}')
    head = (f'<g transform="translate(0 -212) rotate({tilt})">'
            f'<circle r="{r_out + 12}" fill="url(#silver)"/><circle r="{r_out + 12}" fill="none" stroke="#3A3F49" stroke-width="2"/>'
            f'<circle r="{r_out}" fill="#15181F"/>'
            f'<circle cx="{look * 6:.1f}" r="{r_in:.1f}" fill="url(#lens)"/>'
            f'<path d="{" ".join(blades)}" stroke="#3A404B" stroke-width="2"/>'
            f'<circle cx="{look * 6 - r_in * 0.35:.1f}" cy="{-r_in * 0.35:.1f}" r="{max(2, r_in * 0.18):.1f}" fill="{LIME}" opacity="0.8"/>'
            f'<rect x="-6" y="{-r_out - 22}" width="12" height="10" rx="3" fill="#5A616E"/></g>')
    return (legs(-40, 26, color="#3A3F49") + arm(-30, -116, -a[0], -a[1], color="#3A3F49") +
            '<rect x="-42" y="-130" width="84" height="94" rx="18" fill="url(#graphite)"/>'
            '<rect x="-42" y="-82" width="84" height="6" fill="#B6F23A" opacity="0.85"/>'
            '<rect x="-7" y="-160" width="14" height="34" rx="5" fill="url(#silver)"/>' + head +
            arm(30, -116, b[0], b[1], color="#5A616E"))


# C. INGOT: a monocrystalline silicon ingot, the raw material of every chip. Brushed-silver
#    cylinder with the boule's conical crown. Two narrow eye slits, nothing else.
def ingot(eyes=1.0, look=0.0, a=(15, 10), b=(10, 5)):
    eh = 22 * eyes
    return (legs(-40, 22, color="#5D6573", foot="#3A3F49") + arm(-60, -140, -a[0], -a[1], color="#5D6573") +
            '<path d="M-60,-186 L-60,-50 Q0,-30 60,-50 L60,-186 Z" fill="url(#silver)"/>'
            '<path d="M-60,-186 Q-58,-214 -30,-224 Q0,-232 30,-224 Q58,-214 60,-186 Q0,-170 -60,-186 Z" fill="url(#silver)"/>'
            '<ellipse cx="0" cy="-228" rx="16" ry="5" fill="#8A93A2"/>'
            '<path d="M-60,-186 Q0,-170 60,-186" fill="none" stroke="#5D6573" stroke-width="2"/>'
            '<path d="M-60,-92 Q0,-74 60,-92" fill="none" stroke="#B6F23A" stroke-width="5"/>'
            '<path d="M-36,-188 L-36,-60" stroke="#fff" stroke-width="5" opacity="0.25"/>'
            f'<rect x="{-20 + look * 7:.1f}" y="{-160 - eh / 2:.1f}" width="9" height="{eh:.1f}" rx="4.5" fill="#0E1015"/>'
            f'<rect x="{12 + look * 7:.1f}" y="{-160 - eh / 2:.1f}" width="9" height="{eh:.1f}" rx="4.5" fill="#0E1015"/>' +
            arm(60, -140, b[0], b[1], color="#8A93A2"))


# Minimal props in the same restrained language -------------------------------------------------
def chart_card(x, y, w=430, h=300):
    bars = [(1.0, LIME), (0.1, "#4A505C"), (0.074, "#4A505C")]
    o = [f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" rx="14" fill="#14171E" stroke="#2A2F39" stroke-width="1.5"/>',
         T(x + 28, y - h + 46, "Foundry revenue, 4Q 2025", 22, "#E9EBEF", "Inter SemiBold"),
         T(x + 28, y - h + 72, "TrendForce estimate", 15, "#7D8492")]
    base, mh = y - 46, h - 150
    step = (w - 60) / 3
    for i, (v, c) in enumerate(bars):
        bx = x + 30 + i * step + (step - 64) / 2
        o.append(f'<rect x="{bx}" y="{base - mh * v:.1f}" width="64" height="{mh * v:.1f}" fill="{c}"/>')
        o.append(T(bx + 32, base + 26, ("TSMC", "Samsung", "SMIC")[i], 15, "#9AA1AE", "Inter", "middle"))
    o.append(T(x + 30 + (step - 64) / 2 + 32 + 50, base - mh + 22, "$33.7B", 20, "#E9EBEF", "Inter SemiBold", "start"))
    return "".join(o)


def wafer(cx, cy, r):
    grid = "".join(f'<line x1="{cx + d}" y1="{cy - r}" x2="{cx + d}" y2="{cy + r}"/><line x1="{cx - r}" y1="{cy + d}" x2="{cx + r}" y2="{cy + d}"/>'
                   for d in range(-r, r, max(8, r // 7)))
    cid = f"w{cx}{cy}"
    return (f'<defs><clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath></defs>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#silver)"/>'
            f'<g clip-path="url(#{cid})" stroke="#3A3F49" stroke-width="1" opacity="0.6">{grid}</g>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#5D6573" stroke-width="2"/>')


def board():
    o = [f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
         f'<rect x="60" y="56" width="10" height="10" fill="#3D8BFF"/>' + T(80, 66, "THE NEXT SHIFT", 18, "#5C6270", "Inter SemiBold", ls=4) +
         T(W - 60, 66, "MASCOT ROUND 2 · CALIBRATION SKETCH", 18, "#5C6270", "Inter SemiBold", "end", ls=4)]
    cols = [("VISOR", "A matte ceramic capsule. One lime light-line is its whole face.", "line = expression"),
            ("APERTURE", "A precision instrument. The lens iris is its eye; the head tilt is its attitude.", "iris = expression"),
            ("INGOT", "A silicon ingot, the raw material of every chip. Two eye slits, nothing else.", "posture = expression")]
    for i, (name, idea, rule) in enumerate(cols):
        cx = 320 + i * 640
        o.append(f'<circle cx="{cx}" cy="640" r="330" fill="url(#pool)"/>')
        o.append(f'<line x1="{cx - 290}" y1="760" x2="{cx + 290}" y2="760" stroke="#22262E" stroke-width="2"/>')
        o.append(T(cx - 290, 150, name, 44, "#F4F5F7", "Inter ExtraBold", ls=6))
        lines, cur = [], ""
        for wd in idea.split():
            if len(cur) + len(wd) + 1 > 58:
                lines.append(cur)
                cur = wd
            else:
                cur = (cur + " " + wd).strip()
        for k, ln in enumerate(lines + [cur]):
            o.append(T(cx - 290, 188 + k * 26, ln, 19, "#9AA1AE"))
        o.append(T(cx - 290, 246, rule.upper(), 14, LIME, "Inter SemiBold", ls=3))
    # hero poses: presenting the chart
    o.append(chart_card(320 - 40, 760, 300, 250))
    o.append(place(170, 760, 1.05, visor("approve", a=(20, 10), b=(95, 70)), tilt=3))
    o.append(chart_card(960 - 20, 760, 300, 250))
    o.append(place(830, 760, 1.05, aperture(0.25, tilt=18, look=1, a=(15, 5), b=(100, 120)), tilt=4))
    o.append(wafer(1720, 560, 110))
    o.append(place(1530, 760, 1.05, ingot(0.6, look=1, a=(10, 0), b=(110, 150)), tilt=6))
    # secondary poses (small): expression range
    small = [(visor("neutral"), visor("focus"), visor("doubt")),
             (aperture(0.9, tilt=-6), aperture(0.15, tilt=10, look=1), aperture(0.55, tilt=-16, look=-1)),
             (ingot(1.0), ingot(0.25, look=1), ingot(1.25, look=-1, a=(160, 170), b=(160, 170)))]
    labels = [("attentive", "focused", "doubtful"), ("surprised", "scrutinising", "curious"), ("neutral", "sceptical", "amazed")]
    for i in range(3):
        for k in range(3):
            x = 320 + i * 640 - 200 + k * 200
            o.append(place(x, 990, 0.5, small[i][k]))
            o.append(T(x, 1030, labels[i][k].upper(), 13, "#7D8492", "Inter SemiBold", "middle", ls=2))
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>{DEFS}</defs>'
         f'{"".join(o)}</svg>')
    path = os.path.join(OUT, "round2_calibration.png")
    cairosvg.svg2png(bytestring=s.encode(), write_to=path)
    return path


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(board())
