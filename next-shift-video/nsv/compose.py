"""Frame compositor: background, camera, scene envelope, brand bug, source line."""
from __future__ import annotations

import math

from . import brand as B
from .components import REGISTRY
from .fx import ease_in_out, esc, group, text

_DEFS = (f'<defs><radialGradient id="vig" cx="50%" cy="45%" r="75%">'
         f'<stop offset="0" stop-color="#151820"/><stop offset="1" stop-color="{B.BG}"/></radialGradient>'
         f'<linearGradient id="fadeb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{B.BG}" stop-opacity="0"/>'
         f'<stop offset="1" stop-color="{B.BG}" stop-opacity="0.85"/></linearGradient></defs>')


def background(T: float) -> str:
    """Global time T keeps the grid drifting continuously across scene cuts."""
    out = [f'<rect width="{B.W}" height="{B.H}" fill="url(#vig)"/>']
    step = 120
    off = (T * 5) % step
    lines = []
    for i in range(-1, B.W // step + 2):
        x = i * step + off
        lines.append(f"M{x:.1f},0V{B.H}")
    for j in range(-1, B.H // step + 2):
        y = j * step + off * 0.5
        lines.append(f"M0,{y:.1f}H{B.W}")
    out.append(f'<path d="{"".join(lines)}" stroke="{B.GRID}" stroke-width="1" opacity="0.55"/>')
    # a few slow drifting particles
    for k in range(9):
        px = (k * 263 + T * (6 + k)) % B.W
        py = (k * 157 + math.sin(T * 0.2 + k) * 40 + 120) % B.H
        out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{1.5 + (k % 3)}" fill="{B.ACCENT}" opacity="0.18"/>')
    out.append(f'<rect y="{B.H - 260}" width="{B.W}" height="260" fill="url(#fadeb)"/>')
    return "".join(out)


def chrome(chapter: str | None, sources: list[str], a: float) -> str:
    out = [f'<rect x="{B.SAFE_X - 100}" y="60" width="10" height="10" fill="{B.ACCENT}"/>',
           text(B.SAFE_X - 80, 71, B.CHANNEL, 18, B.INK_3, B.F_SEMI, spacing=4)]
    if chapter:
        out.append(text(B.W - B.SAFE_X + 100, 71, chapter.upper(), 18, B.INK_3, B.F_SEMI, "end", spacing=4))
    if sources:
        s = "Source: " + "; ".join(sources)
        if len(s) > 120:
            s = s[:117] + "..."
        out.append(text(B.SAFE_X - 100, B.H - 50, s, 20, B.INK_3, B.F_REG, opacity=a))
    return "".join(out)


def scene_svg(scene: dict, t: float, d: float, T: float) -> str:
    """Full 1920x1080 SVG for one frame. `scene` is a timeline entry."""
    fn = REGISTRY[scene["component"]]
    fade = B.SCENE_FADE
    env = min(1.0, t / fade if fade else 1, (d - t) / fade if fade else 1)
    env = ease_in_out(max(env, 0.0))
    push = 1.0 + B.CAMERA_PUSH * ease_in_out(t / d if d else 0)
    body = fn(scene.get("params", {}), t, d)
    content = group(body, opacity=env, scale=push, ty=(1 - env) * 12)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{B.W}" height="{B.H}" '
            f'viewBox="0 0 {B.W} {B.H}">{_DEFS}{background(T)}{content}'
            f'{chrome(scene.get("chapter"), scene.get("source_labels", []), env)}</svg>')
