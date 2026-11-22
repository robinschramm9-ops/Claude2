"""Frame compositor: background, camera, scene envelope, brand bug, source line, presenter (Pip)."""
from __future__ import annotations

import math
import wave

import numpy as np

from . import brand as B
from . import mascot
from .components import REGISTRY
from .fx import ease_in_out, group, text


def defs() -> str:
    """Built per frame from the active theme (themes change brand colours at runtime)."""
    return (f'<defs><radialGradient id="vig" cx="50%" cy="45%" r="75%">'
            f'<stop offset="0" stop-color="{"#151820" if B.THEME == "dark" else "#FFFFFF"}"/>'
            f'<stop offset="1" stop-color="{B.BG}"/></radialGradient>'
            f'<linearGradient id="fadeb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{B.BG}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{B.BG}" stop-opacity="0.85"/></linearGradient>'
            f'<radialGradient id="softshadow"><stop offset="0" stop-color="#6B6658" stop-opacity="0.20"/>'
            f'<stop offset="1" stop-color="#6B6658" stop-opacity="0"/></radialGradient>{mascot.DEFS}</defs>')


def background(T: float) -> str:
    """Global time T keeps the background drifting continuously across scene cuts."""
    if B.BG_BLOBS:   # white theme: warm paper with two large, slowly drifting soft circles
        return (f'<rect width="{B.W}" height="{B.H}" fill="{B.BG}"/>'
                f'<circle cx="{1500 + 40 * math.sin(T * 0.07):.1f}" cy="{260 + 30 * math.cos(T * 0.05):.1f}" r="520" fill="#FFFFFF" opacity="0.6"/>'
                f'<circle cx="{300 + 50 * math.cos(T * 0.06):.1f}" cy="{900 + 25 * math.sin(T * 0.08):.1f}" r="420" fill="#EFEDE6" opacity="0.7"/>')
    out = [f'<rect width="{B.W}" height="{B.H}" fill="url(#vig)"/>']
    step = 120
    off = (T * 5) % step
    lines = []
    for i in range(-1, B.W // step + 2):
        lines.append(f"M{i * step + off:.1f},0V{B.H}")
    for j in range(-1, B.H // step + 2):
        lines.append(f"M0,{j * step + off * 0.5:.1f}H{B.W}")
    out.append(f'<path d="{"".join(lines)}" stroke="{B.GRID}" stroke-width="1" opacity="0.55"/>')
    for k in range(9):
        px = (k * 263 + T * (6 + k)) % B.W
        py = (k * 157 + math.sin(T * 0.2 + k) * 40 + 120) % B.H
        out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{1.5 + (k % 3)}" fill="{B.ACCENT}" opacity="0.18"/>')
    out.append(f'<rect y="{B.H - 260}" width="{B.W}" height="260" fill="url(#fadeb)"/>')
    return "".join(out)


def chrome(chapter: str | None, sources: list[str], a: float) -> str:
    if B.THEME == "white":
        out = [f'<circle cx="76" cy="66" r="7" fill="{B.ACCENT_2}"/>', text(94, 73, B.CHANNEL, 22, B.INK_3, B.F_BOLD)]
        if chapter:
            out.append(text(B.W - 70, 73, chapter.lower(), 22, B.INK_3, B.F_REG, "end"))
    else:
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


# Narration loudness per scene (drives Pip's mouth). Cached per worker process.
_ENV: dict = {}


def _level(scene: dict, t: float) -> float:
    path = scene.get("vo_path")
    if not path or scene.get("vo_start") is None:
        return 0.0
    if path not in _ENV:
        try:
            with wave.open(path) as w:
                sr = w.getframerate()
                a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
            hop = sr // 30
            env = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2) + 1e-9) for i in range(0, len(a), hop)])
            _ENV[path] = (env / (env.max() or 1), 30)
        except (FileNotFoundError, wave.Error):
            _ENV[path] = (np.zeros(1), 30)
    env, fps = _ENV[path]
    i = int((t - (scene["vo_start"] - scene["start"])) * fps)
    return float(env[i]) if 0 <= i < len(env) else 0.0


def scene_svg(scene: dict, t: float, d: float, T: float) -> str:
    """Full 1920x1080 SVG for one frame. `scene` is a timeline entry."""
    fn = REGISTRY[scene["component"]]
    fade = B.SCENE_FADE
    env = min(1.0, t / fade if fade else 1, (d - t) / fade if fade else 1)
    env = ease_in_out(max(env, 0.0))
    push = 1.0 + B.CAMERA_PUSH * ease_in_out(t / d if d else 0)
    body = fn(scene.get("params", {}), t, d)
    content = group(body, opacity=env, scale=push, ty=(1 - env) * 12)
    pip = ""
    if scene.get("pip"):
        pip = group(mascot.draw(scene["pip"], t, d, _level(scene, t)), opacity=env)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{B.W}" height="{B.H}" '
            f'viewBox="0 0 {B.W} {B.H}">{defs()}{background(T)}{content}{pip}'
            f'{chrome(scene.get("chapter"), scene.get("source_labels", []), env)}</svg>')
