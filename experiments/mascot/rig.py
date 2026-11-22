"""THE NEXT SHIFT mascot experiment: one parametric rig, three original characters.

Consistency strategy: every image of a character is generated from ONE master design function
plus a Pose. Proportions, colours and features can't drift between shots, because nothing is
redrawn by hand or by an image generator. New poses = new Pose values, never new drawings.

Coordinates: local space, origin at the ground point between the feet, +x = the direction the
character faces, y down (SVG). Height ~200 units at scale 1.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, replace

INK = "#1B1F27"


@dataclass
class Pose:
    x: float = 0                # ground position in the scene
    y: float = 0
    s: float = 1.0              # scale
    facing: int = 1             # 1 = right, -1 = left
    lean: float = 0             # degrees, + leans forward
    squash: float = 0           # -0.2 (stretch) .. 0.2 (squash)
    arm_l: float = 15           # degrees: 0 down, 90 forward, 180 up (back arm)
    arm_r: float = 15           # front arm
    bend_l: float = 0.25        # elbow curvature
    bend_r: float = 0.25
    hand_l: str = "open"        # open | point | grip
    hand_r: str = "open"
    look: tuple = (0.0, 0.0)    # pupil offset, -1..1
    blink: float = 0.0          # 0 open .. 1 closed
    brow: str = "neutral"       # neutral | raised | skeptical | frown | worried
    mouth: str = "smile"        # smile | grin | open | o | smirk | flat | worried
    walk: float | None = None   # walk-cycle phase in radians, None = standing
    mood: str = "neutral"       # Lumen core light: neutral | up | down | idea
    extra: dict = field(default_factory=dict)

    def but(self, **kw):
        return replace(self, **kw)


def soft_shadow(x, y, w, h=None, o=0.45):
    h = h or w * 0.22
    return (f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{w / 2:.1f}" ry="{h / 2:.1f}" '
            f'fill="url(#shadow)" opacity="{o}"/>')


COMMON_DEFS = ('<radialGradient id="shadow"><stop offset="0" stop-color="#000" stop-opacity="0.9"/>'
               '<stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>')


# ---------------------------------------------------------------------------------------------
# Shared parts: arms, hands, legs, eyes, brows, mouths (so all three feel like one family of
# craft, while silhouettes and colours differ completely)
def _arm(sx, sy, ang, length, bend, width, color, hand, hand_color, hand_r):
    a = math.radians(ang)
    hx, hy = sx + length * math.sin(a), sy + length * math.cos(a)
    mx, my = (sx + hx) / 2, (sy + hy) / 2
    nx, ny = -(hy - sy), (hx - sx)                      # perpendicular -> elbow curve
    n = math.hypot(nx, ny) or 1
    cx, cy = mx + nx / n * length * bend, my + ny / n * length * bend
    out = [f'<path d="M{sx:.1f},{sy:.1f} Q{cx:.1f},{cy:.1f} {hx:.1f},{hy:.1f}" fill="none" '
           f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>']
    if hand == "point":
        dx, dy = math.sin(a), math.cos(a)
        out.append(f'<line x1="{hx:.1f}" y1="{hy:.1f}" x2="{hx + dx * hand_r * 2.1:.1f}" y2="{hy + dy * hand_r * 2.1:.1f}" '
                   f'stroke="{hand_color}" stroke-width="{hand_r * 0.75:.1f}" stroke-linecap="round"/>')
    r = hand_r * (1.1 if hand == "grip" else 1)
    out.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{r:.1f}" fill="{hand_color}"/>')
    out.append(f'<circle cx="{hx - r * 0.3:.1f}" cy="{hy - r * 0.35:.1f}" r="{r * 0.35:.1f}" fill="#fff" opacity="0.35"/>')
    return "".join(out), (hx, hy)


def _legs(p: Pose, hip_y, spread, length, width, color, shoe_color, shoe_w):
    out = []
    for side, ph in ((-1, 0.0), (1, math.pi)):
        if p.walk is None:
            fx, lift = side * spread * 1.15, 0
        else:
            fx = side * spread * 0.6 + math.sin(p.walk + ph) * spread * 1.6
            lift = max(0.0, math.cos(p.walk + ph)) * length * 0.28
        hx = side * spread
        fy = -lift
        out.append(f'<path d="M{hx:.1f},{hip_y:.1f} Q{(hx + fx) / 2 + 4:.1f},{(hip_y + fy) / 2:.1f} {fx:.1f},{fy - 4:.1f}" '
                   f'fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>')
        out.append(f'<ellipse cx="{fx + shoe_w * 0.28:.1f}" cy="{fy - 3:.1f}" rx="{shoe_w:.1f}" ry="{shoe_w * 0.52:.1f}" fill="{shoe_color}"/>')
        out.append(f'<ellipse cx="{fx + shoe_w * 0.1:.1f}" cy="{fy - 6:.1f}" rx="{shoe_w * 0.55:.1f}" ry="{shoe_w * 0.2:.1f}" fill="#fff" opacity="0.28"/>')
    return "".join(out)


def _eye(cx, cy, rx, ry, p: Pose, pupil, iris=None, lid_color=None):
    out = [f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="#FBFCFE"/>']
    if p.blink < 0.95:
        px, py = cx + p.look[0] * rx * 0.45, cy + p.look[1] * ry * 0.4
        pr = min(rx, ry) * 0.58
        if iris:
            out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{pr * 1.25:.1f}" fill="{iris}"/>')
        out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{pr:.1f}" fill="{pupil}"/>')
        out.append(f'<circle cx="{px - pr * 0.38:.1f}" cy="{py - pr * 0.42:.1f}" r="{pr * 0.34:.1f}" fill="#fff"/>')
        out.append(f'<circle cx="{px + pr * 0.35:.1f}" cy="{py + pr * 0.35:.1f}" r="{pr * 0.14:.1f}" fill="#fff" opacity="0.8"/>')
    if p.blink > 0.02 and lid_color:  # eyelid closes from the top
        h = ry * 2 * min(1, p.blink)
        out.append(f'<path d="M{cx - rx - 1:.1f},{cy - ry - 1:.1f} h{rx * 2 + 2:.1f} v{h:.1f} '
                   f'Q{cx:.1f},{cy - ry + h + ry * 0.35:.1f} {cx - rx - 1:.1f},{cy - ry + h:.1f} Z" fill="{lid_color}"/>')
    return "".join(out)


def _brow(cx, cy, w, kind, side, color, thick):
    tilt = {"neutral": 0, "raised": -0.12, "skeptical": (-0.35 if side > 0 else 0.15),
            "frown": 0.32 * side, "worried": -0.32 * side}.get(kind, 0)
    lift = {"raised": -9, "skeptical": (-10 if side > 0 else 2), "worried": -4}.get(kind, 0)
    x1, x2 = cx - w / 2, cx + w / 2
    y1 = cy + lift - tilt * w / 2 * side
    y2 = cy + lift + tilt * w / 2 * side
    return (f'<path d="M{x1:.1f},{y1:.1f} Q{cx:.1f},{min(y1, y2) - 5:.1f} {x2:.1f},{y2:.1f}" fill="none" '
            f'stroke="{color}" stroke-width="{thick}" stroke-linecap="round"/>')


def _mouth(cx, cy, w, kind, color, inner="#5A1E2B"):
    h = w * 0.5
    if kind == "smile":
        return f'<path d="M{cx - w / 2:.1f},{cy:.1f} Q{cx:.1f},{cy + h:.1f} {cx + w / 2:.1f},{cy:.1f}" fill="none" stroke="{color}" stroke-width="{w * 0.16:.1f}" stroke-linecap="round"/>'
    if kind == "grin":
        return (f'<path d="M{cx - w / 2:.1f},{cy:.1f} Q{cx:.1f},{cy + h * 1.6:.1f} {cx + w / 2:.1f},{cy:.1f} Z" fill="{inner}"/>'
                f'<path d="M{cx - w / 2 + 3:.1f},{cy + 1:.1f} Q{cx:.1f},{cy + h * 0.5:.1f} {cx + w / 2 - 3:.1f},{cy + 1:.1f}" fill="#fff" opacity="0.9"/>')
    if kind == "open":
        return (f'<ellipse cx="{cx:.1f}" cy="{cy + h * 0.45:.1f}" rx="{w * 0.36:.1f}" ry="{h * 0.62:.1f}" fill="{inner}"/>'
                f'<ellipse cx="{cx:.1f}" cy="{cy + h * 0.8:.1f}" rx="{w * 0.2:.1f}" ry="{h * 0.2:.1f}" fill="#E06A7A"/>')
    if kind == "o":
        return f'<ellipse cx="{cx:.1f}" cy="{cy + h * 0.3:.1f}" rx="{w * 0.17:.1f}" ry="{h * 0.3:.1f}" fill="{inner}"/>'
    if kind == "smirk":
        return f'<path d="M{cx - w / 2.5:.1f},{cy + 2:.1f} Q{cx + w * 0.05:.1f},{cy + h * 0.35:.1f} {cx + w / 2:.1f},{cy - h * 0.3:.1f}" fill="none" stroke="{color}" stroke-width="{w * 0.16:.1f}" stroke-linecap="round"/>'
    if kind == "worried":
        return f'<path d="M{cx - w / 2.4:.1f},{cy + h * 0.3:.1f} Q{cx:.1f},{cy - h * 0.25:.1f} {cx + w / 2.4:.1f},{cy + h * 0.3:.1f}" fill="none" stroke="{color}" stroke-width="{w * 0.15:.1f}" stroke-linecap="round"/>'
    return f'<line x1="{cx - w / 3:.1f}" y1="{cy:.1f}" x2="{cx + w / 3:.1f}" y2="{cy:.1f}" stroke="{color}" stroke-width="{w * 0.15:.1f}" stroke-linecap="round"/>'


def _wrap(p: Pose, body):
    """Place the local drawing in the scene: position, scale, facing, lean, squash."""
    sx = p.s * p.facing * (1 + p.squash)
    sy = p.s * (1 - p.squash)
    return (f'<g transform="translate({p.x:.1f} {p.y:.1f}) rotate({p.lean * p.facing:.2f}) '
            f'scale({sx:.4f} {sy:.4f})">{body}</g>')


# =============================================================================================
# Concept A: NOTCH. A silicon wafer come to life. Circle with the wafer's orientation notch
# as its signature "cowlick". Curious engineer energy. Silver-blue body, lime gloves and shoes.
class Notch:
    name = "NOTCH"
    defs = ('<radialGradient id="notch-body" cx="0.36" cy="0.3" r="0.85">'
            '<stop offset="0" stop-color="#F4F8FF"/><stop offset="0.35" stop-color="#C3D2EA"/>'
            '<stop offset="0.75" stop-color="#7D96BF"/><stop offset="1" stop-color="#3E557F"/></radialGradient>'
            '<linearGradient id="notch-iri" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#7CF5FF" stop-opacity="0.35"/><stop offset="0.35" stop-color="#B6F23A" stop-opacity="0.18"/>'
            '<stop offset="0.6" stop-color="#C08BFF" stop-opacity="0.3"/><stop offset="1" stop-color="#3D8BFF" stop-opacity="0.25"/></linearGradient>'
            '<clipPath id="notch-clip"><circle cx="0" cy="-118" r="78"/></clipPath>')
    R, CY = 82, -118

    @classmethod
    def body_path(cls):
        R, cy = cls.R, cls.CY
        a0, half, nr = math.radians(-58), math.radians(15), 24
        p1 = (R * math.cos(a0 - half), cy + R * math.sin(a0 - half))
        p2 = (R * math.cos(a0 + half), cy + R * math.sin(a0 + half))
        return (f'M{p2[0]:.2f},{p2[1]:.2f} A{R},{R} 0 1 1 {p1[0]:.2f},{p1[1]:.2f} '
                f'A{nr},{nr} 0 0 0 {p2[0]:.2f},{p2[1]:.2f} Z')

    @classmethod
    def draw(cls, p: Pose):
        cy, R = cls.CY, cls.R
        o = [_legs(p, -42, 20, 40, 9, "#8FA3C7", "#B6F23A", 17)]
        back, _ = _arm(-R * 0.6, cy + 28, -p.arm_l, 64, -p.bend_l, 8, "#6F82A6", p.hand_l, "#B6F23A", 11)
        o.append(back)
        o.append(f'<path d="{cls.body_path()}" fill="url(#notch-body)" stroke="#2B3E5C" stroke-width="3"/>')
        grid = "".join(f'<line x1="{x}" y1="{cy - R}" x2="{x}" y2="{cy + R}"/>' for x in range(-78, 80, 13)) + \
               "".join(f'<line x1="{-R}" y1="{y}" x2="{R}" y2="{y}"/>' for y in range(int(cy - 78), int(cy + 80), 13))
        o.append(f'<g clip-path="url(#notch-clip)"><rect x="-90" y="{cy - 90}" width="180" height="180" fill="url(#notch-iri)"/>'
                 f'<g stroke="#ffffff" stroke-opacity="0.26" stroke-width="1.2">{grid}</g></g>')
        o.append(f'<ellipse cx="-30" cy="{cy - 44}" rx="26" ry="12" fill="#fff" opacity="0.5" transform="rotate(-28 -30 {cy - 44})"/>')
        # face
        ex = 20
        o.append(_eye(-ex + 10, cy - 8, 15, 19, p, "#14233D", "#2F6FD8", "#9BB3D6"))
        o.append(_eye(ex + 14, cy - 8, 15, 19, p, "#14233D", "#2F6FD8", "#9BB3D6"))
        o.append(_brow(-ex + 10, cy - 36, 22, p.brow, -1, "#22324D", 5))
        o.append(_brow(ex + 14, cy - 36, 22, p.brow, 1, "#22324D", 5))
        o.append(_mouth(14, cy + 26, 26, p.mouth, "#22324D"))
        o.append('<ellipse cx="-10" cy="-96" rx="9" ry="5" fill="#FF8FA3" opacity="0.28"/>'
                 '<ellipse cx="44" cy="-96" rx="9" ry="5" fill="#FF8FA3" opacity="0.28"/>')
        front, _ = _arm(R * 0.62, cy + 30, p.arm_r, 66, p.bend_r, 8, "#8FA3C7", p.hand_r, "#B6F23A", 11)
        o.append(front)
        return soft_shadow(p.x, p.y, 150 * p.s) + _wrap(p, "".join(o))


# =============================================================================================
# Concept B: PIP. A cheeky market creature (a "pip" is the smallest move in a price).
# Teardrop body whose tip curls back like a rising chart line. Lime body, charcoal limbs,
# a gold monocle for scrutinizing numbers.
class Pip:
    name = "PIP"
    defs = ('<radialGradient id="pip-body" cx="0.35" cy="0.38" r="0.8">'
            '<stop offset="0" stop-color="#F0FFB8"/><stop offset="0.3" stop-color="#C9FA55"/>'
            '<stop offset="0.75" stop-color="#8CC51F"/><stop offset="1" stop-color="#4E7A0C"/></radialGradient>'
            '<radialGradient id="pip-belly" cx="0.5" cy="0.4" r="0.6"><stop offset="0" stop-color="#FAFFE0" stop-opacity="0.85"/>'
            '<stop offset="1" stop-color="#FAFFE0" stop-opacity="0"/></radialGradient>')

    @staticmethod
    def body_path():
        return ("M0,-30 C-62,-30 -78,-78 -74,-120 C-70,-168 -36,-206 4,-236 "
                "C10,-241 22,-248 30,-246 C40,-244 34,-232 26,-228 "
                "C50,-200 74,-160 72,-112 C70,-66 52,-30 0,-30 Z")

    @classmethod
    def draw(cls, p: Pose):
        o = [_legs(p, -38, 18, 36, 9, "#7DB21A", "#E7C65A", 16)]
        back, _ = _arm(-56, -96, -p.arm_l, 58, -p.bend_l, 8, "#6A9A14", p.hand_l, "#EAFBB8", 10)
        o.append(back)
        o.append(f'<path d="{cls.body_path()}" fill="url(#pip-body)" stroke="#3E6108" stroke-width="3"/>')
        o.append('<ellipse cx="2" cy="-74" rx="38" ry="32" fill="url(#pip-belly)"/>')
        o.append('<ellipse cx="-30" cy="-160" rx="16" ry="30" fill="#fff" opacity="0.32" transform="rotate(24 -30 -160)"/>')
        o.append(_eye(-10, -132, 14, 17, p, "#14200A", None, "#8CC51F"))
        o.append(_eye(28, -134, 16, 19, p, "#14200A", None, "#8CC51F"))
        # monocle on the front eye
        mdy, mrot = p.extra.get("monocle_drop", (0, 0))   # gag: the monocle falls off
        o.append(f'<g transform="translate(0 {mdy:.1f}) rotate({mrot:.1f} 28 -134)">'
                 '<circle cx="28" cy="-134" r="22" fill="#FFF7D6" fill-opacity="0.12" stroke="#E7C65A" stroke-width="4"/>'
                 '<path d="M14,-150 A20,20 0 0 1 36,-154" fill="none" stroke="#fff" stroke-width="3" opacity="0.7"/></g>'
                 f'<path d="M48,-124 Q{62 + mdy * 0.1:.1f},{-90 + mdy * 0.5:.1f} 46,-62" fill="none" stroke="#E7C65A" stroke-width="2" stroke-dasharray="3 3"/>')
        o.append(_brow(-10, -160, 20, p.brow, -1, "#2B3D0A", 5))
        o.append(_brow(28, -166, 22, p.brow, 1, "#2B3D0A", 5))
        o.append(_mouth(10, -100, 26, p.mouth, "#2B3D0A"))
        # bow tie
        o.append('<path d="M-6,-62 L-26,-72 L-26,-50 Z M6,-62 L26,-72 L26,-50 Z" fill="#1E2430"/>'
                 '<circle cx="0" cy="-61" r="6" fill="#2E3646"/>')
        front, _ = _arm(52, -96, p.arm_r, 60, p.bend_r, 8, "#8CC51F", p.hand_r, "#F4FFD0", 10)
        o.append(front)
        return soft_shadow(p.x, p.y, 140 * p.s) + _wrap(p, "".join(o))


# =============================================================================================
# Concept C: LUMEN. A small lantern-keeper who "shines a light" on hidden things. Rounded
# glass capsule with a ring handle on top (signature silhouette) and a glowing core whose
# colour is the mood of the data: lime = growth, coral = risk, blue = neutral, gold = idea.
class Lumen:
    name = "LUMEN"
    CORE = {"neutral": ("#9CD2FF", "#3D8BFF"), "up": ("#E4FF9A", "#B6F23A"),
            "down": ("#FFC2B8", "#FF5A4E"), "idea": ("#FFF1B0", "#FFC83D")}
    defs = ('<linearGradient id="lumen-glass" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#6E62E0"/><stop offset="0.45" stop-color="#3A2F9E"/>'
            '<stop offset="1" stop-color="#17124F"/></linearGradient>'
            '<linearGradient id="lumen-metal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9ECF5"/>'
            '<stop offset="1" stop-color="#7E8597"/></linearGradient>' +
            "".join(f'<radialGradient id="lumen-core-{k}"><stop offset="0" stop-color="#fff"/>'
                    f'<stop offset="0.35" stop-color="{a}"/><stop offset="0.7" stop-color="{b}" stop-opacity="0.55"/>'
                    f'<stop offset="1" stop-color="{b}" stop-opacity="0"/></radialGradient>'
                    for k, (a, b) in {"neutral": ("#9CD2FF", "#3D8BFF"), "up": ("#E4FF9A", "#B6F23A"),
                                      "down": ("#FFC2B8", "#FF5A4E"), "idea": ("#FFF1B0", "#FFC83D")}.items()))

    @classmethod
    def draw(cls, p: Pose):
        o = [_legs(p, -40, 20, 36, 9, "#9AA0B8", "#C9CEDB", 16)]
        back, _ = _arm(-52, -110, -p.arm_l, 60, -p.bend_l, 8, "#7C829A", p.hand_l, "#C9CEDB", 10)
        o.append(back)
        sway = p.extra.get("ring_sway", 0)
        o.append(f'<g transform="rotate({sway:.1f} 0 -196)"><path d="M-22,-196 C-26,-246 26,-246 22,-196" fill="none" '
                 f'stroke="url(#lumen-metal)" stroke-width="9" stroke-linecap="round"/></g>')
        o.append('<rect x="-44" y="-206" width="88" height="16" rx="8" fill="url(#lumen-metal)"/>')
        o.append('<rect x="-62" y="-196" width="124" height="160" rx="54" fill="url(#lumen-glass)" stroke="#1A1450" stroke-width="3"/>')
        o.append(f'<circle cx="0" cy="-84" r="58" fill="url(#lumen-core-{p.mood})" opacity="0.95"/>')
        o.append('<rect x="-48" y="-44" width="96" height="14" rx="7" fill="url(#lumen-metal)"/>')
        o.append('<path d="M-46,-170 Q-50,-120 -42,-80" fill="none" stroke="#fff" stroke-width="6" opacity="0.25" stroke-linecap="round"/>')
        o.append(_eye(-14, -150, 13, 15, p, "#120E35", "#5B4FD6", "#3A2F9E"))
        o.append(_eye(24, -150, 13, 15, p, "#120E35", "#5B4FD6", "#3A2F9E"))
        o.append(_brow(-14, -174, 18, p.brow, -1, "#C9CEDB", 4.5))
        o.append(_brow(24, -174, 18, p.brow, 1, "#C9CEDB", 4.5))
        o.append(_mouth(6, -126, 20, p.mouth, "#E8EAF2", "#0E0B2E"))
        front, _ = _arm(54, -110, p.arm_r, 62, p.bend_r, 8, "#9AA0B8", p.hand_r, "#C9CEDB", 10)
        o.append(front)
        glow = f'<circle cx="{p.x:.1f}" cy="{p.y - 84 * p.s:.1f}" r="{150 * p.s:.1f}" fill="url(#lumen-core-{p.mood})" opacity="0.18"/>'
        return glow + soft_shadow(p.x, p.y, 140 * p.s) + _wrap(p, "".join(o))


CONCEPTS = [Notch, Pip, Lumen]
ALL_DEFS = COMMON_DEFS + "".join(c.defs for c in CONCEPTS)
