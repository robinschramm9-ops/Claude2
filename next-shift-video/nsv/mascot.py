"""Pip: THE NEXT SHIFT's presenter. One master design + a Pose = every appearance (consistency by construction).

Placed on a scene with a storyboard key:  "pip": {"pose": "talk", "x": 1720, "y": 1000, "s": 0.8, "facing": -1}
Poses: idle, talk, point, hello, skeptical, surprised, think. The mouth follows the scene's narration audio.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, replace

GREEN, GREEN_D = "#9CCB5A", "#7FAF3E"

DEFS = ('<radialGradient id="shadow"><stop offset="0" stop-color="#000" stop-opacity="0.9"/>'
        '<stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="pipsoft"><stop offset="0" stop-color="#6B6658" stop-opacity="0.22"/>'
        '<stop offset="1" stop-color="#6B6658" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="spip" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#B4DB78"/>'
        '<stop offset="1" stop-color="#8DBF4C"/></linearGradient>')


def _ground(x, y, w):
    return f'<ellipse cx="{x}" cy="{y}" rx="{w / 2}" ry="{w * 0.07}" fill="url(#pipsoft)"/>'


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
        mdy, mrot = p.extra.get("monocle_drop", (0, 0))
        o.append(f'<g transform="translate(0 {mdy:.1f}) rotate({mrot:.1f} 28 -134)">'
                 '<circle cx="28" cy="-134" r="22" fill="none" stroke="#C9A84E" stroke-width="3.5"/></g>'
                 f'<path d="M48,-124 Q{60 + mdy * 0.1:.1f},{-92 + mdy * 0.5:.1f} 46,-66" fill="none" stroke="#C9A84E" stroke-width="2" stroke-linecap="round"/>')
        o.append(_brow(-10, -160, 20, p.brow, -1, "#4E6B2A", 5))
        o.append(_brow(28, -166, 22, p.brow, 1, "#4E6B2A", 5))
        o.append(_mouth(10, -100, 26, p.mouth, "#4E6B2A", "#6E3B3B"))
        front, _ = _arm(52, -96, p.arm_r, 60, p.bend_r, 9, GREEN_D, p.hand_r, "#F3F8E8", 11)
        o.append(front)
        return _ground(p.x, p.y, 150 * p.s) + _wrap(p, "".join(o))




PRESETS = {
    "idle": dict(arm_l=12, arm_r=14, mouth="smile"),
    "talk": dict(arm_l=14, arm_r=40, mouth="smile", look=(-0.2, 0)),
    "point": dict(arm_r=95, hand_r="point", look=(1, -0.2), mouth="smile", lean=6),
    "hello": dict(arm_r=165, bend_r=-0.3, mouth="grin", brow="raised"),
    "skeptical": dict(arm_r=150, bend_r=0.7, arm_l=150, bend_l=0.7, brow="skeptical", mouth="smirk"),
    "surprised": dict(arm_l=150, arm_r=150, bend_l=0.1, bend_r=0.1, mouth="open", brow="raised", squash=-0.08),
    "think": dict(arm_r=160, bend_r=0.75, look=(-0.4, -0.6), brow="skeptical", mouth="flat"),
}


def draw(spec: dict, t: float, d: float, level: float = 0.0) -> str:
    """Pip for one frame. t = scene time, d = scene duration, level = narration loudness 0..1."""
    preset = dict(PRESETS.get(spec.get("pose", "idle"), PRESETS["idle"]))
    enter = min(1.0, t / 0.35)
    hop = -40 * math.sin(math.pi * enter) if enter < 1 else 0          # small hop on entry
    breathe = 0.012 * math.sin(t * 2.4)
    if spec.get("pose") == "talk":
        preset["arm_r"] = 40 + 14 * math.sin(t * 3.1)                  # talking gesture
    rest = preset.get("mouth", "smile")
    mouth = "open" if level > 0.5 else "o" if level > 0.2 else rest
    blink = 1.0 if (t % 3.7) < 0.12 else 0.0
    p = Pose(x=spec.get("x", 1720), y=spec.get("y", 1000) + hop, s=spec.get("s", 0.8),
             facing=spec.get("facing", -1), **{k: v for k, v in preset.items() if k != "mouth"})
    p = p.but(mouth=mouth, blink=blink, squash=p.squash + breathe)
    return SoftPip.draw(p)
