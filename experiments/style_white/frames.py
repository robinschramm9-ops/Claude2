"""Style frames: 'white, simple, extremely round, natural'.

Rules: warm white backgrounds · no straight hard edges, every shape is a circle or a pill ·
soft diffuse shadows instead of outlines · one natural green accent · rounded type (Quicksand).
"""
from __future__ import annotations

import os
import sys

import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "mascot"))
from rig import COMMON_DEFS, Pip, Pose, _arm, _brow, _eye, _legs, _mouth, _wrap  # noqa: E402

W, H = 1920, 1080
OUT = os.path.join(HERE, "out")
BG, CARD, INK, MUTED = "#F7F6F2", "#FFFFFF", "#2E2F2C", "#9A978F"
GREEN, GREEN_D, SAND, STONE, LAV = "#9CCB5A", "#7FAF3E", "#E9DFCC", "#DAD6CD", "#CBC3E3"
FONT = "Quicksand"

DEFS = COMMON_DEFS + Pip.defs + (
    f'<radialGradient id="soft"><stop offset="0" stop-color="#6B6658" stop-opacity="0.22"/>'
    f'<stop offset="1" stop-color="#6B6658" stop-opacity="0"/></radialGradient>'
    f'<radialGradient id="glowg"><stop offset="0" stop-color="{GREEN}" stop-opacity="0.22"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></radialGradient>'
    f'<linearGradient id="spip" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#B4DB78"/><stop offset="1" stop-color="#8DBF4C"/></linearGradient>'
    f'<linearGradient id="appliance" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#ECE9E2"/></linearGradient>'
    f'<radialGradient id="window" cx="0.42" cy="0.38" r="0.7"><stop offset="0" stop-color="#F1EDFB"/><stop offset="1" stop-color="{LAV}"/></radialGradient>'
    f'<radialGradient id="waferg" cx="0.38" cy="0.32" r="0.8"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.6" stop-color="#E9EEF3"/>'
    f'<stop offset="1" stop-color="#D3DAE2"/></radialGradient>')


def T(x, y, s, size, fill=INK, weight="normal", anchor="start", fam=FONT, op=1):
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-weight="{weight}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" opacity="{op}">{s}</text>')


def soft_box(x, y, w, h, r, fill=CARD, depth=18):
    """Rounded card floating on a soft, diffuse shadow (stacked translucent layers; no hard edge)."""
    layers = "".join(f'<rect x="{x - i * 1.5}" y="{y + depth * 0.35 + i}" width="{w + i * 3}" height="{h + i}" rx="{r + i}" '
                     f'fill="#5C5647" opacity="0.012"/>' for i in range(depth))
    return layers + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"/>'


def ground(x, y, w):
    return f'<ellipse cx="{x}" cy="{y}" rx="{w / 2}" ry="{w * 0.07}" fill="url(#soft)"/>'


def page(body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>{DEFS}</defs>'
            f'<rect width="{W}" height="{H}" fill="{BG}"/>'
            f'<circle cx="1500" cy="260" r="520" fill="#FFFFFF" opacity="0.6"/><circle cx="300" cy="900" r="420" fill="#EFEDE6" opacity="0.7"/>'
            f'{body}'
            f'<circle cx="76" cy="66" r="7" fill="{GREEN}"/>' + T(94, 73, "the next shift", 22, MUTED, "bold") +
            T(W - 70, 73, label, 22, MUTED, "normal", "end") + "</svg>")


# Softened Pip: same character, rounded tip, flatter matte colour, no bow tie ------------------------
class SoftPip:
    @staticmethod
    def draw(p: Pose):
        body = ("M0,-30 C-62,-30 -78,-78 -74,-120 C-70,-166 -42,-198 -10,-220 "
                "C2,-229 20,-238 31,-229 C41,-220 33,-206 24,-202 "
                "C48,-176 72,-150 72,-112 C70,-66 52,-30 0,-30 Z")
        o = [_legs(p, -38, 18, 36, 10, GREEN_D, "#EEF5E2", 16)]
        back, _ = _arm(-56, -96, -p.arm_l, 58, -p.bend_l, 9, GREEN_D, p.hand_l, "#F3F8E8", 11)
        o.append(back)
        o.append(f'<path d="{body}" fill="url(#spip)"/>')
        o.append('<ellipse cx="-34" cy="-150" rx="12" ry="26" fill="#fff" opacity="0.25" transform="rotate(24 -34 -150)"/>')
        o.append(_eye(-10, -132, 14, 17, p, "#2E2F2C", None, "#8DBF4C"))
        o.append(_eye(28, -134, 16, 19, p, "#2E2F2C", None, "#8DBF4C"))
        o.append('<circle cx="28" cy="-134" r="22" fill="none" stroke="#C9A84E" stroke-width="3.5"/>'
                 '<path d="M48,-124 Q60,-92 46,-66" fill="none" stroke="#C9A84E" stroke-width="2" stroke-linecap="round"/>')
        o.append(_brow(-10, -160, 20, p.brow, -1, "#4E6B2A", 5))
        o.append(_brow(28, -166, 22, p.brow, 1, "#4E6B2A", 5))
        o.append(_mouth(10, -100, 26, p.mouth, "#4E6B2A", "#6E3B3B"))
        front, _ = _arm(52, -96, p.arm_r, 60, p.bend_r, 9, GREEN_D, p.hand_r, "#F3F8E8", 11)
        o.append(front)
        return ground(p.x, p.y, 150 * p.s) + _wrap(p, "".join(o))


# Frames -------------------------------------------------------------------------------------------------
def frame_chart(P):
    o = [soft_box(760, 230, 900, 640, 56)]
    o.append(T(830, 330, "Share of global foundry revenue", 40, INK, "bold"))
    o.append(T(830, 378, "4Q 2025 · TrendForce estimate", 26, MUTED))
    items = [("TSMC", 70.4, GREEN), ("Samsung", 7.1, SAND), ("All others", 22.5, STONE)]
    # bubble AREA is proportional to share (radius ~ sqrt), so round shapes never distort the data
    rmax = 170
    cxs = [1000, 1290, 1480]
    for i, (lab, v, c) in enumerate(items):
        r = rmax * (v / 70.4) ** 0.5
        cy = 760 - r
        o.append(f'<circle cx="{cxs[i]}" cy="{cy:.1f}" r="{r:.1f}" fill="{c}"/>')
        if i == 0:
            o.append(T(cxs[i], cy + 18, f"{v:.1f}%", 56, "#FFFFFF", "bold", "middle"))
        else:
            o.append(T(cxs[i], cy - r - 22, f"{v:.1f}%", 34, INK, "bold", "middle"))
        o.append(T(cxs[i], 812, lab, 26, MUTED, "bold", "middle"))
    o.append(T(830, 850, "Circle area = share", 20, MUTED))
    o.append(P.draw(Pose(x=470, y=860, s=1.7, arm_r=112, hand_r="point", look=(1, -0.3), brow="skeptical", mouth="smirk", lean=6)))
    o.append(T(140, 1010, "Data: TrendForce, 4Q 2025 (estimate)", 22, MUTED))
    return page("".join(o), "one factory, many rivals")


def frame_wafer(P):
    cx, cy, r = 1180, 470, 300
    o = [f'<circle cx="{cx}" cy="{cy}" r="{r + 120}" fill="url(#glowg)"/>',
         f'<ellipse cx="{cx + 10}" cy="{cy + r + 70}" rx="{r * 0.8}" ry="30" fill="url(#soft)"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#waferg)"/>']
    step = 58
    for gx in range(-5, 5):
        for gy in range(-5, 5):
            x0, y0 = cx + gx * step + 6, cy + gy * step + 6
            if ((x0 + 23 - cx) ** 2 + (y0 + 23 - cy) ** 2) ** 0.5 < r - 40:
                o.append(f'<rect x="{x0}" y="{y0}" width="46" height="46" rx="16" fill="#DCE3EA"/>')
    o.append(f'<rect x="{cx - 2 * step + 6}" y="{cy - step + 6}" width="46" height="46" rx="16" fill="{GREEN}"/>')
    o.append(T(cx, cy + r + 150, "Every AI chip starts as one of these squares.", 34, INK, "bold", "middle"))
    o.append(P.draw(Pose(x=640, y=860, s=1.7, arm_r=95, hand_r="point", lean=12, look=(1, -0.2), brow="raised", mouth="o")))
    return page("".join(o), "how a chip is made")


def frame_machine(P):
    x, y, w, h = 760, 220, 960, 640
    o = [f'<ellipse cx="{x + w / 2}" cy="{y + h + 26}" rx="{w * 0.55}" ry="44" fill="url(#soft)"/>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="140" fill="url(#appliance)"/>',
         f'<rect x="{x + 70}" y="{y + 70}" width="{w - 140}" height="70" rx="35" fill="#F2EFE9"/>',
         f'<circle cx="{x + w * 0.62}" cy="{y + h * 0.58}" r="150" fill="#EFEBE3"/>',
         f'<circle cx="{x + w * 0.62}" cy="{y + h * 0.58}" r="118" fill="url(#window)"/>',
         f'<circle cx="{x + w * 0.58}" cy="{y + h * 0.53}" r="26" fill="#fff" opacity="0.7"/>',
         f'<rect x="{x + 110}" y="{y + h * 0.48}" width="210" height="150" rx="40" fill="#F2EFE9"/>']
    for i, c in enumerate((GREEN, GREEN, SAND)):
        o.append(f'<circle cx="{x + 160 + i * 55}" cy="{y + h * 0.48 + 55}" r="14" fill="{c}"/>')
    o.append(f'<rect x="{x + 150}" y="{y + h * 0.48 + 92}" width="130" height="22" rx="11" fill="{STONE}"/>')
    o.append(f'<rect x="{x + 140}" y="{y + h - 12}" width="120" height="36" rx="18" fill="{STONE}"/>'
             f'<rect x="{x + w - 260}" y="{y + h - 12}" width="120" height="36" rx="18" fill="{STONE}"/>')
    o.append(soft_box(170, 300, 400, 150, 75))
    o.append(T(370, 362, "reportedly", 26, MUTED, "bold", "middle") + T(370, 414, "$380–400M each", 42, INK, "bold", "middle"))
    o.append(P.draw(Pose(x=520, y=860, s=1.05, arm_r=150, hand_r="point", look=(0.6, -1), brow="raised", mouth="o", lean=-8)))
    o.append(T(140, 1010, "Stylised illustration of an ASML EUV lithography system. Price: press reports.", 22, MUTED))
    return page("".join(o), "the machine behind the machine")


def pip_compare():
    o = [T(W / 2, 170, "Pip in the new style", 54, INK, "bold", "middle"),
         T(W / 2, 222, "Left: original. Right: softened (rounded tip, matte colour, no bow tie).", 28, MUTED, "normal", "middle")]
    o.append(Pip.draw(Pose(x=660, y=860, s=2.3, arm_r=40, look=(0.3, 0), mouth="smirk", brow="skeptical")))
    o.append(SoftPip.draw(Pose(x=1260, y=860, s=2.3, arm_r=40, look=(0.3, 0), mouth="smirk", brow="skeptical")))
    o.append(T(660, 960, "original", 28, MUTED, "bold", "middle") + T(1260, 960, "softened", 28, GREEN_D, "bold", "middle"))
    return page("".join(o), "mascot")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, svg in (("1_chart", frame_chart(SoftPip)), ("2_wafer", frame_wafer(SoftPip)),
                      ("3_machine", frame_machine(SoftPip)), ("4_pip_compare", pip_compare())):
        p = os.path.join(OUT, f"{name}.png")
        cairosvg.svg2png(bytestring=svg.encode(), write_to=p)
        print(p)
