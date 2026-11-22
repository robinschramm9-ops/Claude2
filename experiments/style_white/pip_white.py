"""Pip sequences in the white / round / natural style, voiced by the ElevenLabs voice 'Claude'.

Reuses the timing, audio and camera machinery of ../mascot/pip_dynamic.py; only the look changes.

    PIP_EL_VOICE=<voice_id> python3 pip_white.py [chart|wafer|machine ...]
"""
from __future__ import annotations

import math
import os
import subprocess
import sys

import cairosvg
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("PIP_TTS", "elevenlabs")
os.environ.setdefault("PIP_EL_VOICE", "GwaSlBgu1okDU38ZSzyb")   # "Claude" (user's generated voice)
os.environ.setdefault("PIP_TAG", "_white")
sys.path.insert(0, os.path.join(HERE, "..", "mascot"))
sys.path.insert(0, HERE)
import pip_dynamic as PD                                       # noqa: E402
from frames import (BG, DEFS, FONT, GREEN, GREEN_D, INK, MUTED, SAND, STONE, SoftPip,  # noqa: E402
                    soft_box)
from rig import Pose                                           # noqa: E402

PD.OUT = os.path.join(HERE, "out", "anim")
W, H, FPS = 1920, 1080, 30
ease, ease_out, back_out, talk = PD.ease, PD.ease_out, PD.back_out, PD.talk


def T(x, y, s, size, fill=INK, weight="bold", anchor="middle", op=1.0):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-weight="{weight}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" opacity="{op:.2f}">{s}</text>')


def slam(txt, x, y, size, dt, color=INK, hold=99.0, weight="bold"):
    """Soft pop-in: scales from 140% with a gentle overshoot; fades out after `hold`."""
    if dt < 0 or dt > hold + 0.3:
        return ""
    sc = 1 + 0.4 * (1 - ease_out(dt / 0.18))
    op = min(1.0, dt / 0.07) * (1 - ease((dt - hold) / 0.3))
    return (f'<g transform="translate({x} {y}) scale({sc:.3f}) translate({-x} {-y})">'
            + T(x, y, txt, size, color, weight, "middle", op) + "</g>")


def pulse(t, at):
    d = t - at
    if not 0 <= d < 0.6:
        return ""
    return f'<circle cx="{W / 2}" cy="{H / 2}" r="{600 + d * 900:.0f}" fill="{GREEN}" opacity="{0.10 * (1 - d / 0.6):.3f}"/>'


def page_bg():
    return (f'<rect x="-400" y="-400" width="{W + 800}" height="{H + 800}" fill="{BG}"/>'
            f'<circle cx="1500" cy="260" r="520" fill="#FFFFFF" opacity="0.6"/>'
            f'<circle cx="300" cy="900" r="420" fill="#EFEDE6" opacity="0.7"/>')


def chrome(label, note):
    return (f'<circle cx="76" cy="66" r="7" fill="{GREEN}"/>' + T(94, 73, "the next shift", 22, MUTED, "bold", "start") +
            T(W - 70, 73, label, 22, MUTED, "normal", "end") + T(140, 1020, note, 22, MUTED, "normal", "start"))


def doc(world, cam, t, over, label, note):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>{DEFS}</defs>'
            f'<rect width="{W}" height="{H}" fill="{BG}"/>{cam(t, page_bg() + world)}{over}{chrome(label, note)}</svg>')


def bubble(cx, base, v, rmax, g, fill, label, ring=False, text_inside=False):
    r = rmax * (v / 70.4) ** 0.5 * max(0.0, back_out(g, 1.4))
    if r <= 0.5:
        return ""
    cy = base - rmax * (v / 70.4) ** 0.5
    o = [f'<circle cx="{cx}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}"/>']
    if ring:
        o.append(f'<circle cx="{cx}" cy="{cy:.1f}" r="{r + 14:.1f}" fill="none" stroke="{GREEN_D}" stroke-width="5" opacity="0.8"/>')
    k = min(1.0, max(0.0, (g - 0.6) / 0.3))
    if text_inside:
        o.append(T(cx, cy + 18, f"{v:.1f}%", 56, "#FFFFFF", "bold", "middle", k))
    else:
        o.append(T(cx, cy - r - 22, f"{v:.1f}%", 34, INK, "bold", "middle", k))
    o.append(T(cx, base + 52, label, 26, MUTED, "bold", "middle", k))
    return "".join(o)


# ---------------------------------------------------------------------------------------------------- chart
def chart(t, a, s):
    rise = ease_out((t - s[1]) / 0.4)
    dy = 700 * (1 - rise)
    w = []
    if t > s[1]:
        w.append(f'<g transform="translate(0 {dy:.1f})">' + soft_box(760, 230, 900, 640, 56) +
                 T(830, 316, "Share of global foundry revenue", 40, INK, "bold", "start") +
                 T(830, 364, "4Q 2025 · TrendForce estimate", 26, MUTED, "normal", "start") +
                 bubble(1000, 760, 70.4, 170, (t - s[1] - 0.4) / 0.5, GREEN, "TSMC", ring=s[3] <= t < s[4], text_inside=True) +
                 bubble(1290, 760, 7.1, 170, (t - s[1] - 0.6) / 0.5, SAND, "Samsung", ring=s[4] <= t < s[6]) +
                 bubble(1480, 760, 22.5, 170, (t - s[1] - 0.8) / 0.5, STONE, "All others") +
                 T(830, 852, "Circle area = share", 20, MUTED, "normal", "start") + "</g>")
    hop = ease_out((t - 0.1) / 0.35)
    jump = -110 * math.sin(math.pi * min(1, max(0, (t - 0.1) / 0.35)))
    p = Pose(x=-200 + 670 * hop, y=860 + jump, s=1.7, arm_r=60, look=(0.2, 0), mouth=talk(a))
    if t < s[1]:
        p = p.but(arm_r=150 if t > 0.45 else 60, hand_r="point", look=(0.3, -0.8), brow="raised", squash=-0.08 if t < 0.5 else 0)
    elif t < s[3]:
        p = p.but(arm_r=40 + 10 * math.sin(t * 6), look=(0.1, 0))
    elif t < s[4]:
        p = p.but(arm_r=112, hand_r="point", look=(1, -0.3), brow="raised", mouth=talk(a, "grin"), lean=6)
    elif t < s[6]:
        p = p.but(arm_r=100, hand_r="point", look=(1, 0.2), brow="skeptical", lean=12, mouth=talk(a, "flat"))
    else:
        p = p.but(arm_r=150, bend_r=0.7, arm_l=150, bend_l=0.7, look=(0, 0), brow="skeptical", mouth=talk(a, "smirk"),
                  squash=math.exp(-max(0, t - s[7]) * 6) * math.sin(max(0, t - s[7]) * 20) * 0.06)
    w.append(SoftPip.draw(p))
    cam = PD.Shots([(0, 1.35, 760, 520), (s[1], 1.0, 960, 540), (s[3], 1.4, 1000, 560), (s[4], 1.6, 1300, 640),
                    (s[6], 1.55, 470, 640), (s[7], 1.0, 960, 540)], shakes=[(s[0], 8), (s[3], 10), (s[7], 12)])
    over = (slam("70¢", W / 2 + 140, 640, 300, t - s[0], GREEN_D, hold=s[1] - s[0] - 0.1) +
            slam("TSMC", 470, 330, 150, t - s[3], GREEN_D, hold=s[4] - s[3] - 0.1) +
            slam("7¢", W / 2 + 280, 330, 120, t - s[5], INK, hold=s[6] - s[5]) +
            slam("A different league.", W / 2, 200, 110, t - s[7], GREEN_D) + pulse(t, s[7]))
    return doc("".join(w), cam, t, over, "one factory, many rivals", "Data: TrendForce, 4Q 2025 foundry revenue share (estimate)")


# ---------------------------------------------------------------------------------------------------- wafer
def wafer_round(cx, cy, r, lit=0):
    o = [f'<circle cx="{cx}" cy="{cy}" r="{r + 110}" fill="url(#glowg)"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#waferg)"/>']
    step = r / 5.2
    k = 0
    for gx in range(-5, 5):
        for gy in range(-5, 5):
            x0, y0 = cx + gx * step + step * 0.1, cy + gy * step + step * 0.1
            sz = step * 0.8
            if ((x0 + sz / 2 - cx) ** 2 + (y0 + sz / 2 - cy) ** 2) ** 0.5 < r - step * 0.7:
                fill = GREEN if k < lit else "#DCE3EA"
                o.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{sz:.1f}" height="{sz:.1f}" rx="{sz * 0.34:.1f}" fill="{fill}"/>')
                k += 1
    return "".join(o)


def pill(x, y, label, dt, gone=-1.0):
    if dt < 0:
        return ""
    k = back_out(dt / 0.3)
    if gone >= 0:
        k *= 1 - ease_out(gone / 0.2)
        if k <= 0.01:
            return ""
    return (f'<g transform="translate({x} {y}) scale({k:.3f})">' + soft_box(-150, -55, 300, 110, 55) +
            T(0, 16, label, 44, INK, "bold", "middle") + "</g>")


def wafer(t, a, s):
    spin = ease_out((t - 0.15) / 0.6)
    wx, wy, r = 1180, 470, 300
    lit = int(max(0, (t - s[1]) / 0.05)) if t > s[1] else 0
    w = []
    if t > 0.15:
        w.append(f'<ellipse cx="{wx + 10}" cy="{wy + r + 70}" rx="{r * 0.8 * spin:.1f}" ry="30" fill="url(#soft)"/>')
        w.append(f'<g transform="translate({wx} {wy}) scale({0.1 + 0.9 * spin:.3f}) rotate({(1 - spin) * -200:.1f}) translate({-wx} {-wy})">'
                 + wafer_round(wx, wy, r, min(lit, 9)) + "</g>")
    hop = ease_out((t - 0.05) / 0.3)
    jump = -90 * math.sin(math.pi * min(1, max(0, t / 0.3)))
    p = Pose(x=-180 + 820 * hop, y=860 + jump, s=1.7, mouth=talk(a), arm_r=95, hand_r="point", look=(1, -0.2), lean=8)
    if s[2] <= t < s[3]:
        which = 0 if t < s[2] + 0.55 else 1
        p = p.but(arm_r=110 if which else 150, arm_l=150 if which == 0 else 20, hand_l="point",
                  look=((-1, -0.6) if which == 0 else (1, -0.6)), brow="raised", lean=0)
    elif s[3] <= t < s[4]:
        p = p.but(arm_r=30, look=(0, 0), brow="skeptical", mouth=talk(a, "flat"), lean=0)
    elif t >= s[4]:
        p = p.but(arm_r=170, arm_l=170, hand_r="open", look=(0, -0.3), brow="raised", mouth=talk(a, "grin"), lean=0,
                  squash=-0.1 * math.exp(-(t - s[4]) * 5))
    w.append(SoftPip.draw(p))
    cam = PD.Shots([(0, 1.0, 960, 540), (s[1], 1.7, 1180, 480), (s[2], 1.0, 960, 540), (s[3], 1.45, 700, 640),
                    (s[4], 1.0, 960, 540)], shakes=[(s[4], 12)])
    over = (pill(560, 220, "NVIDIA", t - s[2], gone=t - s[4]) + pill(1360, 220, "AMD", t - s[2] - 0.55, gone=t - s[4]) +
            slam("?", 960, 520, 240, t - s[3], GREEN_D, hold=s[4] - s[3] - 0.05) +
            slam("TSMC", W / 2, 230, 200, t - s[4], INK) +
            slam("Each square = one chip", 1180, 900, 42, t - s[1] - 0.2, INK, hold=s[2] - s[1] - 0.3) + pulse(t, s[4]))
    return doc("".join(w), cam, t, over, "how a chip is made",
               "Sources: AMD 10-K (FY2025); NVIDIA Blackwell wafer at TSMC Arizona (Oct 2025). Illustration.")


# -------------------------------------------------------------------------------------------------- machine
def appliance(x, y, w, h, glow):
    o = [f'<ellipse cx="{x + w / 2}" cy="{y + h + 26}" rx="{w * 0.55}" ry="44" fill="url(#soft)"/>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="140" fill="url(#appliance)"/>',
         f'<rect x="{x + 70}" y="{y + 70}" width="{w - 140}" height="70" rx="35" fill="#F2EFE9"/>',
         f'<circle cx="{x + w * 0.62}" cy="{y + h * 0.58}" r="{150 + 10 * glow:.1f}" fill="#E9E4F4" opacity="0.7"/>',
         f'<circle cx="{x + w * 0.62}" cy="{y + h * 0.58}" r="150" fill="#EFEBE3"/>',
         f'<circle cx="{x + w * 0.62}" cy="{y + h * 0.58}" r="118" fill="url(#window)"/>',
         f'<circle cx="{x + w * 0.58}" cy="{y + h * 0.53}" r="26" fill="#fff" opacity="0.7"/>',
         f'<rect x="{x + 110}" y="{y + h * 0.48}" width="210" height="150" rx="40" fill="#F2EFE9"/>',
         f'<rect x="{x + 150}" y="{y + h * 0.48 + 92}" width="130" height="22" rx="11" fill="{STONE}"/>',
         f'<rect x="{x + 140}" y="{y + h - 12}" width="120" height="36" rx="18" fill="{STONE}"/>',
         f'<rect x="{x + w - 260}" y="{y + h - 12}" width="120" height="36" rx="18" fill="{STONE}"/>']
    for i, c in enumerate((GREEN, GREEN, SAND)):
        o.append(f'<circle cx="{x + 160 + i * 55}" cy="{y + h * 0.48 + 55}" r="14" fill="{c}"/>')
    return "".join(o)


def machine(t, a, s):
    w = [appliance(760, 220, 960, 640, math.sin(t * 5) ** 2)]
    p = Pose(x=520, y=860, s=1.05, mouth=talk(a), arm_r=150, hand_r="point", look=(0.6, -1), brow="raised", lean=-8)
    if s[4] <= t < s[5]:
        p = p.but(arm_r=30, look=(-0.3, 0), brow="skeptical", mouth=talk(a, "flat"), lean=0)
    elif t >= s[5]:
        r = t - s[5]
        drop = min(1.0, max(0.0, (r - 0.9) / 0.35))
        p = p.but(arm_r=40, arm_l=30, look=(0, -0.1), brow="raised", mouth=talk(a, "open"), lean=0,
                  squash=-0.1 * math.exp(-max(0, r - 0.9) * 5), extra={"monocle_drop": (drop ** 2 * 165, drop * 70)})
    w.append(SoftPip.draw(p))
    cam = PD.Shots([(0, 2.4, 520, 760), (s[0] + 0.7, 1.7, 1100, 420), (s[1], 1.0, 960, 540), (s[2], 1.2, 1150, 560),
                    (s[4], 2.3, 520, 740), (s[5], 1.5, 640, 660), (s[6], 2.4, 525, 740)],
                   shakes=[(s[3], 10), (s[6], 12)])
    pd = t - s[5]
    price = ""
    if pd >= 0:
        v = 380 * ease_out(pd / 0.7)
        price = slam(f"${v:,.0f}–400M" if pd > 0.7 else f"${v:,.0f}M", W / 2, 300, 140, pd, GREEN_D, hold=s[6] - s[5] + 2)
    over = (slam("1", W / 2, 560, 400, t - s[2], GREEN_D, hold=s[3] - s[2] - 0.05) +
            slam("ASML", W / 2, 300, 190, t - s[3], INK, hold=s[4] - s[3] - 0.05) + price +
            slam("reportedly", W / 2, 180, 40, pd, MUTED, hold=s[6] - s[5] + 2) +
            slam("each.", 1460, 620, 130, t - s[6], INK) + pulse(t, s[3]))
    return doc("".join(w), cam, t, over, "the machine behind the machine",
               "Stylised illustration of an ASML EUV system. Price: press reports; no official list price.")


FRAMES = {"chart": chart, "wafer": wafer, "machine": machine}


def render(name):
    os.makedirs(PD.OUT, exist_ok=True)
    voice, sr, starts = PD.speak(name)
    dur = len(voice) / sr
    n = int(dur * FPS)
    hop = sr / FPS
    env = np.array([np.sqrt(np.mean(voice[int(i * hop):int((i + 1) * hop)] ** 2) + 1e-9) for i in range(n)])
    env = env / (env.max() or 1)
    events = [(starts[i] + off, kind) for i, off, kind in PD.EVENTS[name]]
    audio = PD.mix(name, voice, sr, dur, events)
    silent = os.path.join(PD.OUT, f"{name}_silent.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
                           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "veryfast", silent], stdin=subprocess.PIPE)
    for f in range(n):
        ff.stdin.write(cairosvg.svg2png(bytestring=FRAMES[name](f / FPS, float(env[f]), starts).encode(),
                                        output_width=W, output_height=H))
    ff.stdin.close(); ff.wait()
    out = os.path.join(PD.OUT, f"pip_white_{name}.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", audio, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    os.remove(silent)
    return out, round(dur, 1)


if __name__ == "__main__":
    for nm in sys.argv[1:] or list(FRAMES):
        print(render(nm))
