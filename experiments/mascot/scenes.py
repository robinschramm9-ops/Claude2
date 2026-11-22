"""Concept sheets, interaction scenes and short animations for the three mascot concepts.

    python3 scenes.py            # writes everything to out/
"""
from __future__ import annotations

import io
import math
import os
import subprocess
import sys

import cairosvg
from PIL import Image

from rig import ALL_DEFS, CONCEPTS, Lumen, Notch, Pip, Pose

OUT = os.path.join(os.path.dirname(__file__), "out")
W, H = 1920, 1080
F = "Inter"
FB = "Inter ExtraBold"
FS = "Inter SemiBold"

PROP_DEFS = (
    '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#11141B"/>'
    '<stop offset="0.62" stop-color="#1A1F2A"/><stop offset="1" stop-color="#0C0E13"/></linearGradient>'
    '<radialGradient id="spot" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#3D8BFF" stop-opacity="0.16"/>'
    '<stop offset="1" stop-color="#3D8BFF" stop-opacity="0"/></radialGradient>'
    '<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#232937"/>'
    '<stop offset="1" stop-color="#0E1016"/></linearGradient>'
    '<linearGradient id="glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1C2230" stop-opacity="0.96"/>'
    '<stop offset="1" stop-color="#121620" stop-opacity="0.96"/></linearGradient>'
    '<linearGradient id="bar-hi" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D4FF6E"/>'
    '<stop offset="1" stop-color="#7FB51A"/></linearGradient>'
    '<linearGradient id="bar-lo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5E6A80"/>'
    '<stop offset="1" stop-color="#394254"/></linearGradient>'
    '<radialGradient id="wafer-base" cx="0.4" cy="0.35" r="0.8"><stop offset="0" stop-color="#F7F9FC"/>'
    '<stop offset="0.5" stop-color="#B9C3D3"/><stop offset="1" stop-color="#6B778C"/></radialGradient>'
    '<linearGradient id="wafer-iri" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0" stop-color="#7CF5FF" stop-opacity="0.55"/><stop offset="0.3" stop-color="#C08BFF" stop-opacity="0.45"/>'
    '<stop offset="0.55" stop-color="#FFB86B" stop-opacity="0.35"/><stop offset="0.8" stop-color="#B6F23A" stop-opacity="0.45"/>'
    '<stop offset="1" stop-color="#3D8BFF" stop-opacity="0.5"/></linearGradient>'
    '<linearGradient id="mach-front" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9EDF3"/>'
    '<stop offset="1" stop-color="#A9B2C0"/></linearGradient>'
    '<linearGradient id="mach-side" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9099A8"/>'
    '<stop offset="1" stop-color="#5E6676"/></linearGradient>'
    '<linearGradient id="mach-top" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F6F8FB"/>'
    '<stop offset="1" stop-color="#C9D0DB"/></linearGradient>'
    '<radialGradient id="euv" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#F3E6FF"/>'
    '<stop offset="0.35" stop-color="#B477FF"/><stop offset="1" stop-color="#3A1670"/></radialGradient>'
    '<radialGradient id="glow-v" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#B477FF" stop-opacity="0.5"/>'
    '<stop offset="1" stop-color="#B477FF" stop-opacity="0"/></radialGradient>')


def svg(body, w=W, h=H):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {W} {H}">'
            f'<defs>{ALL_DEFS}{PROP_DEFS}</defs>{body}</svg>')


def png(s, path, w=W, h=H):
    cairosvg.svg2png(bytestring=s.encode(), write_to=path, output_width=w, output_height=h)


def T(x, y, s, size, fill="#F4F5F7", fam=F, anchor="start", op=1, ls=0):
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'opacity="{op}" letter-spacing="{ls}">{s}</text>')


def stage(floor_y=860, spot=(960, 520), spot_r=760):
    vx = W / 2
    lines = "".join(f'<line x1="{vx + (i - 10) * 30}" y1="{floor_y}" x2="{vx + (i - 10) * 260}" y2="{H}"/>' for i in range(21))
    hl = "".join(f'<line x1="0" y1="{floor_y + d}" x2="{W}" y2="{floor_y + d}"/>' for d in (14, 34, 62, 100, 150, 214))
    return (f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
            f'<circle cx="{spot[0]}" cy="{spot[1]}" r="{spot_r}" fill="url(#spot)"/>'
            f'<rect y="{floor_y}" width="{W}" height="{H - floor_y}" fill="url(#floor)"/>'
            f'<g stroke="#2C3446" stroke-width="1.2" opacity="0.7">{lines}{hl}</g>'
            f'<rect y="{floor_y - 1}" width="{W}" height="2" fill="#3A4357" opacity="0.6"/>')


def brand_bug(label):
    return (f'<rect x="60" y="56" width="10" height="10" fill="#3D8BFF"/>' + T(80, 66, "THE NEXT SHIFT", 18, "#5C6270", FS, ls=4) +
            T(W - 60, 66, label, 18, "#5C6270", FS, "end", ls=4))


# Props -----------------------------------------------------------------------------------------
def chart_panel(x, y, w=760, h=520, grow=1.0, glow=False):
    """Bar chart on a glass panel. (x, y) = bottom-left corner. Data: TrendForce 4Q25 foundry revenue."""
    items = [("TSMC", 33.7, "$33.7B"), ("Samsung Foundry", 3.4, "$3.4B"), ("SMIC", 2.49, "$2.5B")]
    top = y - h
    o = [f'<rect x="{x + 10}" y="{top + 18}" width="{w}" height="{h}" rx="26" fill="#000" opacity="0.35"/>',
         f'<rect x="{x}" y="{top}" width="{w}" height="{h}" rx="26" fill="url(#glass)" stroke="#2E3649" stroke-width="2"/>',
         f'<rect x="{x + 26}" y="{top + 1}" width="{w - 52}" height="2" fill="#fff" opacity="0.12"/>']
    if glow:
        o.append(f'<circle cx="{x + w * 0.3}" cy="{top + h * 0.55}" r="{w * 0.55}" fill="url(#lumen-core-up)" opacity="0.18"/>')
    o.append(T(x + 44, top + 70, "Foundry revenue, 4Q 2025", 34, "#F4F5F7", FB))
    o.append(T(x + 44, top + 106, "TrendForce estimate", 22, "#8A92A3"))
    base = y - 70
    maxh = h - 230
    bw = (w - 88) / len(items) * 0.56
    for i, (lab, v, disp) in enumerate(items):
        bx = x + 44 + i * (w - 88) / len(items) + 10
        bh = max(2.0, maxh * v / 33.7 * grow)
        fill = "url(#bar-hi)" if i == 0 else "url(#bar-lo)"
        o.append(f'<rect x="{bx:.1f}" y="{base - bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="8" fill="{fill}"/>')
        if grow > 0.6:
            o.append(T(bx + bw / 2, base - bh - 18, disp, 34 if i == 0 else 28, "#F4F5F7", FB, "middle", min(1, (grow - 0.6) / 0.3)))
        o.append(T(bx + bw / 2, base + 40, lab, 22, "#AEB4C2", FS, "middle"))
    o.append(f'<line x1="{x + 40}" y1="{base}" x2="{x + w - 40}" y2="{base}" stroke="#3A4357" stroke-width="2"/>')
    return "".join(o)


def wafer(cx, cy, r, tilt=0.0, die=True):
    """Silicon wafer with die grid and iridescent sheen. tilt squashes it into perspective (0..0.7)."""
    ry = r * (1 - tilt)
    cid = f"wclip{int(cx)}{int(cy)}{int(r)}"
    grid = []
    step = r / 7.2
    if die:
        for gx in range(-8, 9):
            for gy in range(-8, 9):
                x0, y0 = gx * step, gy * step
                if math.hypot(x0 + step / 2, y0 + step / 2) < r * 0.9:
                    grid.append(f'<rect x="{x0 + 2:.1f}" y="{y0 + 2:.1f}" width="{step - 4:.1f}" height="{step - 4:.1f}" rx="2"/>')
    return (f'<defs><clipPath id="{cid}"><ellipse cx="0" cy="0" rx="{r}" ry="{r}"/></clipPath></defs>'
            f'<g transform="translate({cx} {cy}) scale(1 {1 - tilt:.3f})">'
            f'<ellipse cx="6" cy="14" rx="{r}" ry="{r}" fill="#000" opacity="0.3"/>'
            f'<circle r="{r}" fill="url(#wafer-base)" stroke="#5A6478" stroke-width="3"/>'
            f'<g clip-path="url(#{cid})"><g fill="#3A4A6A" fill-opacity="0.22" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="1">{"".join(grid)}</g>'
            f'<rect x="{-r}" y="{-r}" width="{2 * r}" height="{2 * r}" fill="url(#wafer-iri)"/>'
            f'<ellipse cx="{-r * 0.35}" cy="{-r * 0.45}" rx="{r * 0.5}" ry="{r * 0.18}" fill="#fff" opacity="0.35" transform="rotate(-30 {-r * 0.35} {-r * 0.45})"/></g>'
            f'<circle cx="0" cy="{r - 2}" r="{r * 0.045}" fill="#11141B"/></g>')


def machine(x, y, w=1100, h=640, glow=1.0):
    """Stylised EUV lithography system (illustration). (x, y) = front-bottom-left corner."""
    dx, dy = w * 0.16, -h * 0.13
    fx0, fy0 = x, y - h
    o = [f'<ellipse cx="{x + w * 0.55}" cy="{y + 8}" rx="{w * 0.62}" ry="38" fill="url(#shadow)" opacity="0.55"/>',
         f'<path d="M{fx0},{fy0} l{dx},{dy} h{w} l{-dx},{-dy} Z" fill="url(#mach-top)"/>',
         f'<path d="M{x + w},{fy0} l{dx},{dy} v{h} l{-dx},{-dy} Z" fill="url(#mach-side)"/>',
         f'<rect x="{x}" y="{fy0}" width="{w}" height="{h}" fill="url(#mach-front)"/>']
    for i in range(1, 4):  # module seams
        sx = x + w * i / 4
        o.append(f'<line x1="{sx}" y1="{fy0}" x2="{sx}" y2="{y}" stroke="#8D96A6" stroke-width="2"/>')
    o.append(f'<line x1="{x}" y1="{fy0 + h * 0.18}" x2="{x + w}" y2="{fy0 + h * 0.18}" stroke="#8D96A6" stroke-width="2"/>')
    for m in range(4):  # vents
        vx = x + w * m / 4 + 30
        for r in range(6):
            o.append(f'<rect x="{vx}" y="{fy0 + h * 0.24 + r * 18}" width="{w / 4 - 60}" height="7" rx="3" fill="#9AA3B2"/>')
    # viewport with EUV-violet glow
    cxv, cyv, rv = x + w * 0.62, fy0 + h * 0.6, h * 0.17
    o.append(f'<circle cx="{cxv}" cy="{cyv}" r="{rv * 2.6}" fill="url(#glow-v)" opacity="{0.9 * glow:.2f}"/>')
    o.append(f'<circle cx="{cxv}" cy="{cyv}" r="{rv + 14}" fill="#6B7383"/><circle cx="{cxv}" cy="{cyv}" r="{rv}" fill="url(#euv)" opacity="{0.4 + 0.6 * glow:.2f}"/>')
    o.append(f'<circle cx="{cxv}" cy="{cyv}" r="{rv + 14}" fill="none" stroke="#D5DAE3" stroke-width="3"/>')
    # control panel with status lights
    px, py = x + w * 0.12, fy0 + h * 0.56
    o.append(f'<rect x="{px}" y="{py}" width="{w * 0.2}" height="{h * 0.26}" rx="10" fill="#1E2430"/>')
    for i, c in enumerate(("#B6F23A", "#B6F23A", "#3D8BFF", "#FFC83D")):
        o.append(f'<circle cx="{px + 30 + i * 34}" cy="{py + 30}" r="8" fill="{c}"/>')
    o.append(f'<rect x="{px + 22}" y="{py + 56}" width="{w * 0.2 - 44}" height="{h * 0.11}" rx="6" fill="#2D6BD3" opacity="0.6"/>')
    # pipes & cable trays on top
    for i in range(5):
        tx = x + w * 0.1 + i * w * 0.17
        o.append(f'<path d="M{tx},{fy0 + 4} q{dx * 0.3},{dy - 50} {dx * 0.6},{dy - 10}" fill="none" stroke="#7C8596" stroke-width="16" stroke-linecap="round"/>')
    o.append(f'<rect x="{x}" y="{y - 22}" width="{w}" height="22" fill="#7B8494"/>')
    o.append(f'<rect x="{x + 16}" y="{fy0 + h * 0.06}" width="220" height="40" rx="6" fill="#1E2430"/>' +
             T(x + 30, fy0 + h * 0.06 + 28, "EUV LITHOGRAPHY", 18, "#C9CEDB", FS, ls=2))
    return "".join(o)


# Poses & personality -------------------------------------------------------------------------------
POSES = {
    "idle": Pose(arm_l=12, arm_r=14, mouth="smile"),
    "hello": Pose(arm_r=165, bend_r=-0.3, mouth="grin", brow="raised"),
    "point": Pose(arm_r=95, hand_r="point", look=(0.8, -0.2), mouth="smile", lean=4),
    "surprised": Pose(arm_l=150, arm_r=150, bend_l=0.1, bend_r=0.1, mouth="open", brow="raised", squash=-0.1),
    "thinking": Pose(arm_r=160, bend_r=0.75, look=(-0.4, -0.6), brow="skeptical", mouth="flat"),
    "walk": Pose(walk=0.9, arm_l=-30, arm_r=35, lean=6, mouth="smile", look=(0.6, 0)),
}
EXPRESSIONS = {
    "curious": dict(brow="raised", mouth="o", look=(0.5, -0.3)),
    "delighted": dict(brow="raised", mouth="grin", blink=0.0),
    "skeptical": dict(brow="skeptical", mouth="smirk", look=(0.6, 0.2)),
    "shocked": dict(brow="raised", mouth="open", squash=-0.05),
    "worried": dict(brow="worried", mouth="worried", look=(-0.2, 0.4)),
}
PERSONA = {
    "NOTCH": ("A silicon wafer come to life", "Curious young engineer. Takes things apart to see how they work. Gets genuinely excited by how stuff is made.",
              "Silver-blue wafer body with iridescent die grid · lime gloves and sneakers · signature: the wafer notch"),
    "PIP": ("The cheeky market sleuth", "Named after the smallest move in a price. Scrutinizes every number through his monocle. Unimpressed by hype, delighted by a good data point.",
            "Lime teardrop whose tip curls like a rising chart line · gold monocle, bow tie and shoes"),
    "LUMEN": ("The lantern that shines a light on hidden things", "Calm, slightly mysterious guide. Leads viewers into the dark corners of the supply chain. His core glows with the mood of the data.",
              "Indigo glass lantern body · ring handle (signature silhouette) · core light: lime = growth, coral = risk, blue = neutral, gold = idea"),
}


def char_png(C, pose, size=600, scale=1.25):
    """Character alone on a transparent canvas (used for the silhouette test)."""
    p = pose.but(x=size / 2, y=size * 0.86, s=scale)
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
         f'<defs>{ALL_DEFS}{PROP_DEFS}</defs>{C.draw(p)}</svg>')
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode()))).convert("RGBA")


def concept_sheet(C, idx):
    name = C.name
    title, persona, look = PERSONA[name]
    o = [stage(floor_y=640, spot=(960, 460), spot_r=900), brand_bug(f"MASCOT CONCEPT {idx} OF 3")]
    o.append(T(80, 150, name, 76, "#F4F5F7", FB, ls=6))
    o.append(T(80, 196, title, 30, "#B6F23A", FS))
    o.append(T(1180, 120, "PERSONALITY", 18, "#5C6270", FS, ls=3))
    for i, line in enumerate(_wrap(persona, 52)):
        o.append(T(1180, 152 + i * 32, line, 24, "#C9CEDB"))
    o.append(T(1180, 282, "DESIGN", 18, "#5C6270", FS, ls=3))
    for i, line in enumerate(_wrap(look, 52)):
        o.append(T(1180, 314 + i * 32, line, 24, "#C9CEDB"))
    for i, (pn, pose) in enumerate(POSES.items()):
        x = 160 + i * 262
        o.append(C.draw(pose.but(x=x, y=640, s=1.12)))
        o.append(T(x, 690, pn.upper(), 18, "#8A92A3", FS, "middle", ls=3))
    # close-up expressions: heads cropped in circles
    o.append(T(80, 770, "CLOSE-UP EXPRESSIONS", 18, "#5C6270", FS, ls=3))
    head_y = {"NOTCH": 118, "PIP": 140, "LUMEN": 140}[name]
    for i, (en, kw) in enumerate(EXPRESSIONS.items()):
        cx, cy = 180 + i * 210, 900
        cid = f"hc{i}"
        o.append(f'<defs><clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="88"/></clipPath></defs>'
                 f'<circle cx="{cx}" cy="{cy}" r="88" fill="#232937"/>'
                 f'<g clip-path="url(#{cid})">{C.draw(Pose(x=cx - 10, y=cy + head_y * 1.55, s=1.55, **kw))}</g>'
                 f'<circle cx="{cx}" cy="{cy}" r="88" fill="none" stroke="#3A4357" stroke-width="2"/>')
        o.append(T(cx, cy + 122, en.upper(), 18, "#8A92A3", FS, "middle", ls=3))
    o.append(T(1180, 770, "SILHOUETTE TEST (does it read at thumbnail size?)", 18, "#5C6270", FS, ls=3))
    path = os.path.join(OUT, f"sheet_{name.lower()}.png")
    png(svg("".join(o)), path)
    # silhouette test, composited with PIL from the alpha channel
    base = Image.open(path).convert("RGBA")
    ch = char_png(C, POSES["point"])
    alpha = ch.split()[3]
    for k, sz in enumerate((190, 96, 48, 28)):
        sil = Image.new("RGBA", ch.size, (244, 245, 247, 255))
        sil.putalpha(alpha)
        sil = sil.resize((sz, sz), Image.LANCZOS)
        base.alpha_composite(sil, (1190 + sum((190, 96, 48, 28)[:k]) + k * 40, 1010 - sz))
    base.convert("RGB").save(path)
    return path


def _wrap(s, n):
    words, lines, cur = s.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    return lines + [cur]


# Interaction scenes --------------------------------------------------------------------------------
def scene_chart(C, t=1.0):
    name = C.name
    o = [stage(), brand_bug("CHAPTER 1 · ONE FACTORY, MANY RIVALS")]
    if name == "NOTCH":    # hauls the chart up out of the floor, delighted
        o.append(chart_panel(820, 860 - 40 * (1 - t), grow=t))
        o.append(C.draw(Pose(x=700, y=860, s=1.5, arm_l=150, arm_r=128, bend_l=0.05, bend_r=0.1, hand_l="grip", hand_r="grip",
                             lean=-8, squash=-0.06, brow="raised", mouth="grin", look=(0.9, -0.5))))
    elif name == "PIP":    # leans on the panel, taps the TSMC bar, raises an eyebrow
        o.append(chart_panel(560, 860, grow=t))
        o.append(C.draw(Pose(x=470, y=860, s=1.5, arm_l=40, arm_r=118, hand_r="point", lean=10, brow="skeptical",
                             mouth="smirk", look=(1, -0.4))))
    else:                  # lights the chart up from below with his core
        o.append(chart_panel(820, 860, grow=t, glow=True))
        o.append(C.draw(Pose(x=640, y=860, s=1.5, arm_l=20, arm_r=110, hand_r="point", mood="up", brow="raised",
                             mouth="smile", look=(1, -0.6), extra={"ring_sway": 8})))
    o.append(T(80, 1030, "Data: TrendForce, 4Q 2025 (estimate). Illustration.", 20, "#5C6270"))
    return svg("".join(o))


def scene_wafer(C):
    name = C.name
    o = [stage(spot=(960, 420)), brand_bug("HOW A CHIP IS MADE")]
    if name == "NOTCH":    # holds up a wafer far bigger than himself: "meet the family"
        o.append(wafer(960, 452, 205, tilt=0.12))
        o.append(C.draw(Pose(x=960, y=860, s=1.45, arm_l=172, arm_r=172, bend_l=-0.05, bend_r=0.05, hand_l="grip", hand_r="grip",
                             squash=-0.08, brow="raised", mouth="grin", look=(0, -1))))
        o.append(T(1220, 300, "300 mm", 40, "#B6F23A", FB) + T(1220, 336, "silicon wafer", 24, "#AEB4C2"))
    elif name == "PIP":    # inspects the die grid through the monocle, nose almost on it
        o.append(wafer(1120, 520, 300, tilt=0.0))
        o.append(C.draw(Pose(x=720, y=860, s=1.6, arm_l=60, arm_r=82, hand_r="grip", lean=14, brow="skeptical",
                             mouth="o", look=(1, -0.2))))
        o.append(T(1120, 900, "Hundreds of chips per wafer", 30, "#F4F5F7", FS, "middle"))
    else:                  # shines his light on the wafer; the die grid appears where the light falls
        o.append(f'<circle cx="1120" cy="470" r="420" fill="url(#lumen-core-idea)" opacity="0.22"/>')
        o.append(wafer(1120, 470, 280, tilt=0.38))
        o.append(C.draw(Pose(x=640, y=860, s=1.55, arm_l=150, arm_r=120, hand_r="open", mood="idea", brow="raised",
                             mouth="o", look=(1, -0.5), extra={"ring_sway": -6})))
    o.append(T(80, 1030, "Illustration.", 20, "#5C6270"))
    return svg("".join(o))


def scene_machine(C):
    name = C.name
    o = [stage(floor_y=900, spot=(1100, 500), spot_r=900), brand_bug("CHAPTER 3 · THE MACHINE BEHIND THE MACHINE")]
    o.append(machine(560, 900, w=1100, h=640, glow=1.0 if name != "LUMEN" else 1.4))
    if name == "NOTCH":    # tiny, looking all the way up in awe, pointing
        o.append(C.draw(Pose(x=330, y=900, s=0.95, arm_r=150, hand_r="point", look=(0.6, -1), brow="raised", mouth="o", lean=-10)))
    elif name == "PIP":    # leans casually on the machine, counting the price on his fingers
        o.append(C.draw(Pose(x=470, y=900, s=0.95, facing=1, arm_r=120, bend_r=0.4, arm_l=20, lean=12, brow="skeptical",
                             mouth="smirk", look=(-0.6, -0.2))))
        o.append(f'<rect x="200" y="560" width="330" height="96" rx="20" fill="#F4F5F7"/>'
                 f'<path d="M420,656 l30,34 l6,-34 Z" fill="#F4F5F7"/>' +
                 T(365, 602, "Reportedly", 24, "#1B1F27", FS, "middle") + T(365, 638, "$380–400M each.", 28, "#1B1F27", FB, "middle"))
    else:                  # steps into the violet light of the viewport
        o.append(C.draw(Pose(x=1180, y=900, s=0.95, facing=-1, arm_r=130, hand_r="point", look=(-0.2, -1), mood="idea",
                             brow="raised", mouth="o")))
    o.append(T(80, 1030, "Stylised illustration of an EUV lithography system (ASML). Not to scale.", 20, "#5C6270"))
    return svg("".join(o))


# Animation ------------------------------------------------------------------------------------------------
def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def anim_frame(C, t):
    """6-second beat: walk in → stop → haul the chart up → bars grow → reaction → look at camera."""
    name = C.name
    o = [stage(), brand_bug("ANIMATION TEST")]
    walk_end, x_end = 2.0, 700 if name != "PIP" else 470
    if t < walk_end:
        x = -150 + (x_end + 150) * ease(t / walk_end * 1.05)
        p = Pose(x=x, y=860, s=1.5, walk=t * 9, arm_l=-30 * math.sin(t * 9), arm_r=30 * math.sin(t * 9) + 10,
                 lean=6, mouth="smile", look=(0.7, 0), squash=0.03 * abs(math.sin(t * 9)))
    else:
        p = Pose(x=x_end, y=860, s=1.5)
    rise = ease((t - 2.3) / 0.9)
    grow = ease((t - 3.1) / 1.0)
    px = 820 if name != "PIP" else 560
    if t >= 2.0:
        o.append(chart_panel(px, 860 + 560 * (1 - rise), grow=grow, glow=(name == "LUMEN" and grow > 0)))
    if t >= walk_end:
        settle = math.exp(-(t - walk_end) * 6) * math.sin((t - walk_end) * 18) * 0.08
        if t < 2.3:
            p = p.but(squash=settle, mouth="smile", look=(0.9, 0))
        elif t < 4.2:
            if name == "PIP":
                p = p.but(arm_r=110 * rise + 10, hand_r="point", lean=10 * rise, look=(1, -0.3), brow="skeptical", mouth="flat")
            elif name == "LUMEN":
                p = p.but(arm_r=110 * rise + 10, hand_r="point", mood="up" if grow > 0.2 else "neutral", look=(1, -0.5),
                          brow="raised", mouth="smile", extra={"ring_sway": 6 * math.sin(t * 5)})
            else:
                p = p.but(arm_l=150 * rise, arm_r=128 * rise, hand_l="grip", hand_r="grip", lean=-8 * rise,
                          look=(0.9, -0.5), brow="raised", mouth="smile")
        else:  # reaction to the TSMC bar, then a look to camera
            r = (t - 4.2)
            pop = math.exp(-r * 5) * math.sin(r * 16) * 0.12
            if name == "PIP":
                p = p.but(arm_r=118, hand_r="point", lean=10, squash=pop, brow="skeptical",
                          mouth="smirk", look=(1, -0.4) if r < 0.9 else (-0.4, 0.1), blink=1.0 if 1.3 < r < 1.42 else 0)
            elif name == "LUMEN":
                p = p.but(arm_r=110, hand_r="point", mood="up", squash=pop, brow="raised", mouth="o" if r < 0.9 else "smile",
                          look=(1, -0.5) if r < 0.9 else (-0.3, 0.1), extra={"ring_sway": 10 * math.exp(-r * 2) * math.sin(r * 9)})
            else:
                p = p.but(arm_l=150, arm_r=150, squash=-0.1 + pop, brow="raised", mouth="open" if r < 0.9 else "grin",
                          look=(0.9, -0.5) if r < 0.9 else (-0.3, 0.1), blink=1.0 if 1.4 < r < 1.52 else 0)
    o.append(C.draw(p))
    return svg("".join(o))


def render_anim(C, fps=24, secs=6.0, w=960, h=540):
    path = os.path.join(OUT, f"anim_{C.name.lower()}.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "png", "-i", "-",
                           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", path], stdin=subprocess.PIPE)
    for f in range(int(fps * secs)):
        ff.stdin.write(cairosvg.svg2png(bytestring=anim_frame(C, f / fps).encode(), output_width=w, output_height=h))
    ff.stdin.close()
    ff.wait()
    return path


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:] or ["sheets", "scenes", "anims"]
    for i, C in enumerate(CONCEPTS, 1):
        n = C.name.lower()
        if "sheets" in only:
            print(concept_sheet(C, i))
        if "scenes" in only:
            for k, fn in (("chart", scene_chart), ("wafer", scene_wafer), ("machine", scene_machine)):
                pth = os.path.join(OUT, f"scene_{k}_{n}.png")
                png(fn(C), pth)
                print(pth)
        if "anims" in only:
            print(render_anim(C))
