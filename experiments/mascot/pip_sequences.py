"""PIP animation tests: three short narrated sequences from the revised TSMC script.

Voice: Kokoro (open-source, Apache-2.0), calm male voice, slowed slightly for a serious read.
Pip's mouth is driven by the narration's loudness; story beats are keyed to sentence starts.

    python3 pip_sequences.py [chart|wafer|machine ...]
"""
from __future__ import annotations

import math
import os
import re
import subprocess
import sys
import wave

import cairosvg
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "next-shift-video"))
from rig import Pip, Pose                                     # noqa: E402
from scenes import T, brand_bug, machine, stage, svg, wafer   # noqa: E402

OUT = os.path.join(HERE, "out", "pip")
FPS, W, H = 30, 1920, 1080
VOICE, SPEED = os.environ.get("PIP_VOICE", "am_michael"), 0.9
MODELS = "/tmp/claude-0/models"
PRON = {"TSMC": "T S M C", "ASML": "A S M L", "TrendForce": "Trend Force", "AMD": "A M D", "High-NA": "High N A"}

SEQUENCES = {
    "chart": ["The research firm TrendForce estimates that TSMC took 70.4 percent of global foundry revenue in the last quarter of 2025.",
              "Samsung's foundry business, in second place, took 7.1 percent.",
              "That isn't a lead. It's a different league."],
    "wafer": ["Follow a single AI chip.",
              "Companies like Nvidia and AMD design it. But a design is only a blueprint.",
              "Someone has to turn it into billions of transistors, on a disc of silicon like this one."],
    "machine": ["But even TSMC depends on someone.",
                "Only one company in the world sells the machines that print the most advanced chips: ASML, in the Netherlands.",
                "Its most advanced model reportedly costs around 380 to 400 million dollars. Each."],
}


# Audio ------------------------------------------------------------------------------------------
def speak(name):
    from kokoro_onnx import Kokoro
    k = Kokoro(f"{MODELS}/kokoro-v1.0.int8.onnx", f"{MODELS}/voices-v1.0.bin")
    sr, gap, lead = 24000, 0.45, 0.6
    parts, starts, t = [np.zeros(int(lead * sr), np.float32)], [], lead
    for s in SEQUENCES[name]:
        txt = s
        for a, b in PRON.items():
            txt = re.sub(rf"\b{re.escape(a)}\b", b, txt)
        audio, sr = k.create(txt, voice=VOICE, speed=SPEED, lang="en-us")
        audio = np.asarray(audio, np.float32)
        starts.append((t, t + len(audio) / sr))
        parts += [audio, np.zeros(int(gap * sr), np.float32)]
        t += len(audio) / sr + gap
    parts.append(np.zeros(int(0.8 * sr), np.float32))
    voice = np.concatenate(parts)
    return voice, sr, starts


def envelope(voice, sr, n_frames):
    hop = sr / FPS
    env = np.array([np.sqrt(np.mean(voice[int(i * hop):int((i + 1) * hop)] ** 2) + 1e-9) for i in range(n_frames)])
    env = np.convolve(env, np.ones(3) / 3, mode="same")
    return env / (env.max() or 1)


def mix(name, voice, sr, dur):
    from nsv.audio import score, SR as MSR
    vpath = os.path.join(OUT, f"{name}_voice.wav")
    with wave.open(vpath, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(voice, -1, 1) * 32767).astype(np.int16).tobytes())
    mus = score(dur, seed=11, bpm=70)
    mpath = os.path.join(OUT, f"{name}_music.wav")
    with wave.open(mpath, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(MSR)
        w.writeframes((np.clip(mus, -1, 1) * 32767).astype(np.int16).tobytes())
    out = os.path.join(OUT, f"{name}_mix.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", vpath, "-i", mpath, "-filter_complex",
                    "[0]aresample=48000,pan=stereo|c0=c0|c1=c0,asplit=2[v][sc];"
                    "[1]volume=-17dB[m];[m][sc]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=400[md];"
                    "[v][md]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-2:LRA=11", "-ar", "48000", out], check=True)
    return out


# Animation helpers ---------------------------------------------------------------------------------
def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def talk_mouth(a, rest="flat"):
    return "open" if a > 0.55 else "o" if a > 0.22 else rest


def camera(content, zoom=1.0, cx=W / 2, cy=H / 2):
    return f'<g transform="translate({cx} {cy}) scale({zoom:.4f}) translate({-cx} {-cy})">{content}</g>'


def caption(text):
    return T(80, 1030, text, 20, "#5C6270")


def share_panel(x, y, grow, w=760, h=520, hi=None):
    """Foundry revenue share, 4Q25 (TrendForce estimate). 'All others' = 100 - 70.4 - 7.1."""
    items = [("TSMC", 70.4), ("Samsung Foundry", 7.1), ("All others", 22.5)]
    top = y - h
    o = [f'<rect x="{x + 12}" y="{top + 18}" width="{w}" height="{h}" rx="22" fill="#000" opacity="0.35"/>',
         f'<rect x="{x}" y="{top}" width="{w}" height="{h}" rx="22" fill="url(#glass)" stroke="#2E3649" stroke-width="2"/>',
         T(x + 44, top + 66, "Share of global foundry revenue", 32, "#F4F5F7", "Inter ExtraBold"),
         T(x + 44, top + 100, "4Q 2025 · TrendForce estimate", 22, "#8A92A3")]
    base, maxh = y - 72, h - 270
    col = (w - 88) / 3
    for i, (lab, v) in enumerate(items):
        g = ease((grow - i * 0.15) / 0.7)
        bx, bw = x + 44 + i * col + col * 0.18, col * 0.64
        bh = max(2.0, maxh * v / 70.4 * g)
        fill = "url(#bar-hi)" if i == 0 else "url(#bar-lo)"
        stroke = ' stroke="#F4F5F7" stroke-width="3"' if hi == i else ""
        o.append(f'<rect x="{bx:.1f}" y="{base - bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="8" fill="{fill}"{stroke}/>')
        if g > 0.5:
            o.append(T(bx + bw / 2, base - bh - 16, f"{v:.1f}%", 40 if i == 0 else 30, "#F4F5F7", "Inter ExtraBold", "middle", min(1, (g - 0.5) * 3)))
        o.append(T(bx + bw / 2, base + 40, lab, 22, "#AEB4C2", "Inter SemiBold", "middle"))
    o.append(f'<line x1="{x + 40}" y1="{base}" x2="{x + w - 40}" y2="{base}" stroke="#3A4357" stroke-width="2"/>')
    return "".join(o)


def walking(t, t0, t1, x0, x1):
    p = ease((t - t0) / (t1 - t0))
    moving = t0 <= t < t1
    return x0 + (x1 - x0) * p, moving


# Sequences ------------------------------------------------------------------------------------------------
def frame_chart(t, a, st):
    s1, s2, s3 = st[0][0], st[1][0], st[2][0]
    x, moving = walking(t, 0.0, 2.0, -160, 430)
    base = Pose(x=x, y=860, s=1.55)
    if moving:
        p = base.but(walk=t * 8.5, arm_l=-28 * math.sin(t * 8.5), arm_r=28 * math.sin(t * 8.5) + 10, lean=5, mouth="flat", look=(0.6, 0))
    elif t < s2:  # presenting to camera while the panel rises
        p = base.but(arm_r=40 + 12 * math.sin(t * 2.2) if t < s1 + 1.2 else 125, hand_r="open" if t < s1 + 1.2 else "point",
                     arm_l=15, look=(0.1, 0) if t < s1 + 1.2 else (1, -0.3), brow="neutral", mouth=talk_mouth(a), lean=0)
    elif t < s3:  # turns to the Samsung bar, unimpressed
        p = base.but(arm_r=105, hand_r="point", look=(1, 0.1), brow="skeptical", mouth=talk_mouth(a, "flat"), lean=6)
    else:         # back to camera: the verdict
        k = ease((t - s3) / 0.4)
        p = base.but(arm_r=60 - 30 * k, arm_l=15, look=(0.8 - 0.8 * k, -0.1), brow="skeptical" if t > s3 + 1.2 else "raised",
                     mouth=talk_mouth(a, "smirk"), blink=1.0 if s3 + 2.0 < t < s3 + 2.12 else 0)
    rise = ease((t - (s1 + 0.6)) / 1.0)
    grow = max(0.0, (t - (s1 + 1.4)) / 1.6)
    zoom = 1.0 + 0.03 * ease(t / 12)
    hi = 1 if s2 <= t < s3 else (0 if t >= s3 else None)
    world = stage() + (share_panel(700, 860 + 600 * (1 - rise), grow, hi=hi) if t > s1 else "") + Pip.draw(p)
    return svg(camera(world, zoom) + brand_bug("CHAPTER 1 · ONE FACTORY, MANY RIVALS") +
               caption("Data: TrendForce, 4Q 2025 (estimate). 'All others' = 100% minus TSMC and Samsung."))


def frame_wafer(t, a, st):
    s1, s2, s3 = st[0][0], st[1][0], st[2][0]
    base = Pose(x=760, y=860, s=1.6)
    # the wafer is lowered from above on sentence 3, Pip catches it and inspects it
    drop = ease((t - s3) / 1.1)
    wy = -300 + (560 + 300) * drop
    if t < s2:
        p = base.but(arm_r=35 + 10 * math.sin(t * 2), look=(0, 0), mouth=talk_mouth(a), brow="neutral")
    elif t < s3:
        p = base.but(arm_r=150, bend_r=0.2, arm_l=15, look=(0.3, -0.6), mouth=talk_mouth(a), brow="raised")
    elif t < s3 + 1.1:
        p = base.but(arm_r=165, arm_l=160, hand_r="grip", hand_l="grip", look=(0.4, -1), mouth="o", brow="raised", squash=-0.04)
    else:  # leans in, monocle to the die grid
        k = ease((t - s3 - 1.1) / 0.8)
        p = base.but(x=760 - 60 * k, arm_r=70 + 30 * k, hand_r="grip", arm_l=40, lean=14 * k, look=(1, -0.2),
                     brow="skeptical", mouth=talk_mouth(a, "flat"))
    zoom = 1.0 + 0.22 * ease((t - (s3 + 1.4)) / 2.5)   # slow push-in to the die grid
    world = stage(spot=(1000, 480)) + (wafer(1150, wy, 250, tilt=0.06) if t > s3 - 0.1 else "") + Pip.draw(p)
    if t > s3 + 2.2:
        o = min(1, (t - s3 - 2.2) / 0.6)
        world += T(1150, 880, "Each square: one chip", 30, "#F4F5F7", "Inter SemiBold", "middle", o)
    return svg(camera(world, zoom, cx=1120, cy=560) + brand_bug("HOW A CHIP IS MADE") + caption("Illustration."))


def frame_machine(t, a, st):
    s1, s2, s3 = st[0][0], st[1][0], st[2][0]
    x, moving = walking(t, 0.2, 3.0, -120, 380)
    base = Pose(x=x, y=900, s=1.0)
    if moving:
        p = base.but(walk=t * 9, arm_l=-28 * math.sin(t * 9), arm_r=28 * math.sin(t * 9), lean=5, look=(0.8, -0.3), mouth=talk_mouth(a))
    elif t < s3:  # looks up at the machine
        p = base.but(arm_r=145, hand_r="point", look=(0.7, -1), brow="raised", mouth=talk_mouth(a, "o"), lean=-8)
    else:         # the price: double take, then a sceptical look to camera
        r = t - s3
        p = base.but(arm_r=40, look=(0.7, -1) if r < 1.0 else (-0.2, 0), brow="raised" if r < 1.6 else "skeptical",
                     mouth=talk_mouth(a, "flat"), squash=math.exp(-max(0, r - 1.0) * 5) * math.sin(max(0, r - 1.0) * 14) * 0.08,
                     blink=1.0 if 1.0 < r < 1.1 else 0)
    zoom = 1.25 - 0.25 * ease((t - 0.5) / 4.5)           # pull out: reveal the scale of the machine
    world = stage(floor_y=900, spot=(1100, 500), spot_r=900) + machine(560, 900, w=1100, h=640, glow=0.6 + 0.4 * math.sin(t * 1.5) ** 2) + Pip.draw(p)
    if t > s3 + 0.4:
        k = ease((t - s3 - 0.4) / 0.5)
        bx = 200
        world += (f'<g opacity="{k:.2f}" transform="translate(0 {20 * (1 - k):.1f})">'
                  f'<rect x="{bx}" y="560" width="350" height="104" rx="18" fill="#F4F5F7"/>'
                  f'<path d="M{bx + 230},664 l26,30 l8,-30 Z" fill="#F4F5F7"/>' +
                  T(bx + 175, 602, "Reportedly", 24, "#1B1F27", "Inter SemiBold", "middle") +
                  T(bx + 175, 642, "$380–400M each", 32, "#1B1F27", "Inter ExtraBold", "middle") + "</g>")
    return svg(camera(world, zoom, cx=700, cy=700) + brand_bug("CHAPTER 3 · THE MACHINE BEHIND THE MACHINE") +
               caption("Stylised illustration of an ASML EUV lithography system. Price: press reports, no official list price."))


FRAMES = {"chart": frame_chart, "wafer": frame_wafer, "machine": frame_machine}


def render(name):
    os.makedirs(OUT, exist_ok=True)
    voice, sr, starts = speak(name)
    dur = len(voice) / sr
    n = int(dur * FPS)
    env = envelope(voice, sr, n)
    audio = mix(name, voice, sr, dur)
    silent = os.path.join(OUT, f"{name}_silent.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
                           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "veryfast", silent], stdin=subprocess.PIPE)
    for f in range(n):
        ff.stdin.write(cairosvg.svg2png(bytestring=FRAMES[name](f / FPS, float(env[f]), starts).encode(),
                                        output_width=W, output_height=H))
    ff.stdin.close()
    ff.wait()
    out = os.path.join(OUT, f"pip_{name}.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", audio, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    os.remove(silent)
    return out, round(dur, 1)


if __name__ == "__main__":
    for nm in sys.argv[1:] or list(FRAMES):
        print(render(nm))
