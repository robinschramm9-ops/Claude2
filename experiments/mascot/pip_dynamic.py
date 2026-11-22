"""PIP v2: fast, punchy sequences. Short phrases, quick camera changes, kinetic type, sound design.

Every visual beat is keyed to the start of a narration phrase (each phrase is synthesized
separately, so its start time is known exactly).

    python3 pip_dynamic.py [chart|wafer|machine ...]
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
from rig import Pip, Pose                                     # noqa: E402
from scenes import T, brand_bug, machine, stage, svg, wafer   # noqa: E402

OUT = os.path.join(HERE, "out", "pip_v2")
FPS, W, H, SR = 30, 1920, 1080, 48000
VOICE, SPEED = os.environ.get("PIP_VOICE", "am_michael"), 1.12
MODELS = "/tmp/claude-0/models"
LIME, INK = "#B6F23A", "#F4F5F7"
PRON = {"TSMC": "T S M C", "ASML": "A S M L", "AMD": "A M D", "EUV": "E U V", "Nvidia": "en vidia"}

SEQ = {
    "chart": ["Seventy cents.", "Of every dollar the world spent on contract chipmaking at the end of 2025,",
              "went to one company.", "TSMC.", "Samsung, in second place?", "Seven cents.",
              "That's not a lead.", "That's a different league."],
    "wafer": ["Every AI chip starts like this.", "A disc of pure silicon.", "Nvidia and AMD design the chips.",
              "But the factory that builds their most advanced ones?", "TSMC."],
    "machine": ["But TSMC depends on this.", "An EUV lithography machine.", "Only one company on Earth sells them.",
                "ASML.", "The price?", "Reportedly, 380 to 400 million dollars.", "Each."],
}


# ---------------------------------------------------------------------------------------- audio
TTS = os.environ.get("PIP_TTS", "kokoro")
EL_VOICE = os.environ.get("PIP_EL_VOICE", "nPczCjzI2devNBz1zQrb")
TAG = os.environ.get("PIP_TAG", "")


def speak_elevenlabs(name):
    """ElevenLabs, phrase by phrase, each request given its neighbours for natural continuity."""
    import json, urllib.error, urllib.request
    sr, phrases = 24000, SEQ[name]
    parts, starts, t = [np.zeros(int(0.25 * sr), np.float32)], [], 0.25
    for i, ph in enumerate(phrases):
        body = {"text": ph, "model_id": "eleven_multilingual_v2",
                "previous_text": " ".join(phrases[:i])[-400:], "next_text": " ".join(phrases[i + 1:])[:400],
                "voice_settings": {"stability": 0.38, "similarity_boost": 0.8, "style": 0.35, "use_speaker_boost": True, "speed": 1.08}}
        req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{EL_VOICE}?output_format=mp3_44100_128",
                                     data=json.dumps(body).encode(), method="POST",
                                     headers={"xi-api-key": os.environ.get("ELEVENLABS_API_KEY", "proxy-injected"),
                                              "Content-Type": "application/json", "Accept": "audio/mpeg"})
        for attempt in range(6):            # free plan allows few concurrent requests: back off on 429
            try:
                mp3 = urllib.request.urlopen(req, timeout=120).read()
                break
            except urllib.error.HTTPError as e:
                if e.code != 429 or attempt == 5:
                    raise
                import time; time.sleep(2 * 2 ** attempt)
        pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", "pipe:0", "-f", "f32le", "-ac", "1", "-ar", str(sr), "pipe:1"],
                             input=mp3, capture_output=True, check=True).stdout
        a = np.frombuffer(pcm, np.float32).copy()
        nz = np.where(np.abs(a) > 0.01)[0]
        a = a[max(0, nz[0] - 600): nz[-1] + 1200] if len(nz) else a
        starts.append(t)
        gap = 0.28 if ph.endswith((".", "?")) else 0.05
        parts += [a, np.zeros(int(gap * sr), np.float32)]
        t += len(a) / sr + gap
    parts.append(np.zeros(int(1.0 * sr), np.float32))
    return np.concatenate(parts), sr, starts


def speak(name):
    if TTS == "elevenlabs":
        return speak_elevenlabs(name)
    from kokoro_onnx import Kokoro
    k = Kokoro(f"{MODELS}/kokoro-v1.0.int8.onnx", f"{MODELS}/voices-v1.0.bin")
    parts, starts, t, sr = [np.zeros(int(0.25 * 24000), np.float32)], [], 0.25, 24000
    for ph in SEQ[name]:
        txt = ph
        for a, b in PRON.items():
            txt = re.sub(rf"\b{re.escape(a)}\b", b, txt)
        a, sr = k.create(txt, voice=VOICE, speed=SPEED, lang="en-us")
        a = np.asarray(a, np.float32)
        nz = np.where(np.abs(a) > 0.01)[0]              # trim Kokoro's own leading/trailing silence
        a = a[max(0, nz[0] - 600): nz[-1] + 1200] if len(nz) else a
        starts.append(t)
        gap = 0.32 if ph.endswith((".", "?")) else 0.06
        parts += [a, np.zeros(int(gap * sr), np.float32)]
        t += len(a) / sr + gap
    parts.append(np.zeros(int(1.0 * sr), np.float32))
    return np.concatenate(parts), sr, starts


def _env(n, attack, decay):
    t = np.arange(n) / SR
    return np.minimum(1, t / attack) * np.exp(-t / decay)


def sfx_impact():
    n = int(0.5 * SR); t = np.arange(n) / SR
    f = 70 * np.exp(-t * 6) + 38
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.002, 0.16)
    click = np.random.default_rng(1).standard_normal(n) * _env(n, 0.0005, 0.012) * 0.5
    return (body + click) * 0.9


def sfx_whoosh(length=0.45):
    n = int(length * SR)
    noise = np.random.default_rng(2).standard_normal(n)
    out = np.convolve(noise, np.ones(18) / 18, mode="same") - np.convolve(noise, np.ones(90) / 90, mode="same")
    return out * np.sin(np.pi * np.linspace(0, 1, n)) ** 2 * 1.4


def sfx_tick():
    n = int(0.05 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 2400 * t) * _env(n, 0.0005, 0.01) * 0.5


def sfx_ding():
    n = int(1.0 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1318 * t) + 0.5 * np.sin(2 * np.pi * 2637 * t)) * _env(n, 0.002, 0.3) * 0.45


SFX = {"impact": sfx_impact, "whoosh": sfx_whoosh, "tick": sfx_tick, "ding": sfx_ding}


def beat_bed(dur, bpm=112):
    """Driving minimal bed: kick on every beat, soft hats on off-beats, low pulse bass."""
    n = int(dur * SR); out = np.zeros(n)
    beat = 60 / bpm
    k = sfx_impact() * 0.55
    hat = np.random.default_rng(3).standard_normal(int(0.03 * SR)) * _env(int(0.03 * SR), 0.0005, 0.006) * 0.12
    t = np.arange(n) / SR
    for i in range(int(dur / beat) + 1):
        a = int(i * beat * SR)
        out[a:a + len(k)] += k[: n - a]
        h = int((i + 0.5) * beat * SR)
        out[h:h + len(hat)] += hat[: max(0, n - h)]
    bass = np.sin(2 * np.pi * 55 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * t / beat - np.pi / 2)) * 0.08
    fade = np.minimum(1, np.minimum(t / 0.3, (dur - t) / 0.8)).clip(0, 1)
    return (out + bass) * fade


def mix(name, voice, sr, dur, events):
    vpath = os.path.join(OUT, f"{name}{TAG}_voice.wav")
    with wave.open(vpath, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(voice, -1, 1) * 32767).astype(np.int16).tobytes())
    fx = np.zeros(int(dur * SR) + SR)
    for t0, kind in events:
        s = SFX[kind](); a = int(t0 * SR)
        fx[a:a + len(s)] += s[: len(fx) - a]
    bed = beat_bed(dur)
    mpath = os.path.join(OUT, f"{name}{TAG}_fx.wav")
    music = np.zeros_like(fx); music[:len(bed)] = bed
    stereo = np.stack([music * 0.5 + fx * 0.6, music * 0.5 + fx * 0.6], 1)
    with wave.open(mpath, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(stereo, -1, 1) * 32767).astype(np.int16).reshape(-1).tobytes())
    out = os.path.join(OUT, f"{name}{TAG}_mix.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", vpath, "-i", mpath, "-filter_complex",
                    "[0]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=1.4,asplit=2[v][sc];"
                    "[1]volume=-6dB[m];[m][sc]sidechaincompress=threshold=0.03:ratio=5:attack=10:release=250[md];"
                    "[v][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9", "-ar", "48000", out], check=True)
    return out


# ------------------------------------------------------------------------------------ motion helpers
def ease(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)


def ease_out(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3


def back_out(x, s=1.8):
    x = max(0.0, min(1.0, x)); return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


class Shots:
    """Camera keyframes (time, zoom, cx, cy); fast 0.3 s eased moves between them, plus impact shake."""
    def __init__(self, keys, shakes=()):
        self.keys, self.shakes = sorted(keys), shakes

    def __call__(self, t, content):
        prev = self.keys[0]; cur = self.keys[0]
        for k in self.keys:
            if k[0] <= t:
                prev, cur = cur, k
        p = ease_out((t - cur[0]) / 0.3) if cur is not prev else 1
        z, cx, cy = (prev[i] + (cur[i] - prev[i]) * p for i in (1, 2, 3))
        sx = sy = 0.0
        for st, amp in self.shakes:
            d = t - st
            if 0 <= d < 0.35:
                e = amp * math.exp(-d * 12)
                sx += e * math.sin(d * 90); sy += e * math.cos(d * 70)
        return (f'<g transform="translate({W / 2 + sx:.1f} {H / 2 + sy:.1f}) scale({z:.4f}) translate({-cx:.1f} {-cy:.1f})">'
                f'{content}</g>')


def slam(txt, x, y, size, dt, color=INK, anchor="middle", hold=99.0, fam="Inter ExtraBold"):
    """Kinetic word: drops in from 160% scale in 0.16 s, holds, fades."""
    if dt < 0 or dt > hold + 0.25:
        return ""
    sc = 1 + 0.6 * (1 - ease_out(dt / 0.16))
    op = min(1.0, dt / 0.06) * (1 - ease((dt - hold) / 0.25))
    return (f'<g transform="translate({x} {y}) scale({sc:.3f}) translate({-x} {-y})" opacity="{op:.2f}">'
            f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" fill="#0B0C0F" stroke="#0B0C0F" '
            f'stroke-width="{max(6, size * 0.09):.0f}" stroke-linejoin="round" text-anchor="{anchor}" letter-spacing="-2" opacity="0.92">{txt}</text>'
            f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" fill="{color}" text-anchor="{anchor}" '
            f'letter-spacing="-2">{txt}</text></g>')


def talk(a, rest="smirk"):
    return "open" if a > 0.5 else "o" if a > 0.2 else rest


def flash(t, at, strength=0.18):
    d = t - at
    return f'<rect width="{W}" height="{H}" fill="#fff" opacity="{strength * math.exp(-d * 9):.3f}"/>' if 0 <= d < 0.5 else ""


def panel_bars(x, y, w, h, grow, hi=None):
    items = [("TSMC", 70.4), ("Samsung", 7.1), ("All others", 22.5)]
    o = [f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" rx="22" fill="url(#glass)" stroke="#2E3649" stroke-width="2"/>',
         T(x + 40, y - h + 60, "Share of global foundry revenue", 30, INK, "Inter ExtraBold"),
         T(x + 40, y - h + 92, "4Q 2025 · TrendForce estimate", 20, "#8A92A3")]
    base, maxh, col = y - 64, h - 250, (w - 80) / 3
    for i, (lab, v) in enumerate(items):
        g = back_out((grow - i * 0.12) / 0.45, 1.2)
        bx, bw = x + 40 + i * col + col * 0.18, col * 0.64
        bh = max(2.0, maxh * v / 70.4 * max(0, g))
        fill = "url(#bar-hi)" if i == 0 else "url(#bar-lo)"
        st = ' stroke="#F4F5F7" stroke-width="4"' if hi == i else ""
        o.append(f'<rect x="{bx:.1f}" y="{base - bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="8" fill="{fill}"{st}/>')
        o.append(T(bx + bw / 2, base - bh - 14, f"{v:.1f}%", 36 if i == 0 else 28, INK, "Inter ExtraBold", "middle", min(1, max(0, g))))
        o.append(T(bx + bw / 2, base + 36, lab, 22, "#AEB4C2", "Inter SemiBold", "middle"))
    return "".join(o)


def card(x, y, label, dt, color="#1C2230", gone=None):
    if dt < 0:
        return ""
    k = back_out(dt / 0.3)
    if gone is not None and gone >= 0:
        k *= 1 - ease_out(gone / 0.2)
        if k <= 0.01:
            return ""
    return (f'<g transform="translate({x} {y}) scale({k:.3f})"><rect x="-150" y="-60" width="300" height="120" rx="18" fill="{color}" '
            f'stroke="#3A4357" stroke-width="2"/>' + T(0, 16, label, 46, INK, "Inter ExtraBold", "middle") + "</g>")


# ----------------------------------------------------------------------------------------- sequences
def chart(t, a, s):
    # s = phrase start times
    world = [stage()]
    grow = (t - s[1] - 0.4) / 1.0
    rise = ease_out((t - s[1]) / 0.35)
    if t > s[1]:
        world.append(panel_bars(760, 860 + 700 * (1 - rise), 780, 540, grow, hi=0 if s[3] <= t < s[4] else (1 if s[4] <= t < s[6] else None)))
    # Pip: hop-in on phrase 0, then snappy poses
    hop = ease_out((t - 0.1) / 0.35)
    jump = -120 * math.sin(math.pi * min(1, max(0, (t - 0.1) / 0.35)))
    p = Pose(x=-200 + 620 * hop, y=860 + jump, s=1.6, arm_r=60, look=(0.2, 0), mouth=talk(a))
    if t < s[1]:
        p = p.but(arm_r=150 if t > 0.45 else 60, hand_r="point", look=(0.3, -0.8), brow="raised", squash=-0.08 if t < 0.5 else 0)
    elif t < s[3]:
        p = p.but(arm_r=40 + 10 * math.sin(t * 6), look=(0.1, 0), brow="neutral")
    elif t < s[4]:
        p = p.but(arm_r=120, hand_r="point", look=(1, -0.4), brow="raised", mouth=talk(a, "grin"), lean=8)
    elif t < s[6]:
        p = p.but(arm_r=100, hand_r="point", look=(1, 0.3), brow="skeptical", lean=14, mouth=talk(a, "flat"))
    else:
        p = p.but(arm_r=150, bend_r=0.7, arm_l=150, bend_l=0.7, look=(0, 0), brow="skeptical", mouth=talk(a, "smirk"),
                  squash=math.exp(-max(0, t - s[7]) * 6) * math.sin(max(0, t - s[7]) * 20) * 0.06)
    world.append(Pip.draw(p))
    cam = Shots([(0, 1.35, 760, 520), (s[1], 1.0, 960, 540), (s[3], 1.45, 960, 520), (s[4], 1.6, 1130, 700),
                 (s[6], 1.55, 430, 640), (s[7], 1.0, 960, 540)], shakes=[(0.1, 0), (s[0], 14), (s[3], 18), (s[7], 22)])
    over = [slam("70¢", W / 2 + 120, 620, 300, t - s[0], LIME, hold=s[1] - s[0] - 0.1),
            slam("TSMC", 470, 330, 150, t - s[3], LIME, hold=s[4] - s[3] - 0.1),
            slam("7¢", W / 2 + 260, 330, 120, t - s[5], INK, hold=s[6] - s[5]),
            slam("A DIFFERENT LEAGUE.", W / 2, 230, 120, t - s[7], LIME)]
    return _bg_svg(cam(t, "".join(world)) + "".join(over) + flash(t, s[7]) + brand_bug("THE NEXT SHIFT · TEST") +
               T(80, 1030, "Data: TrendForce, 4Q 2025 foundry revenue share (estimate).", 20, "#5C6270"))


def wafer_seq(t, a, s):
    world = [stage(spot=(960, 460))]
    spin = ease_out((t - 0.15) / 0.6)
    r = 30 + 250 * spin
    wx, wy = 1150, 470
    world.append(f'<g transform="rotate({(1 - spin) * -280:.1f} {wx} {wy})">{wafer(wx, wy, int(r), tilt=0.05)}</g>' if t > 0.15 else "")
    sweep = (t - s[1]) / 0.9
    if 0 < sweep < 1.2:   # light sweep across the die grid
        sx = wx - 260 + 520 * sweep
        world.append(f'<rect x="{sx - 40:.1f}" y="{wy - 260}" width="80" height="520" fill="{LIME}" opacity="0.18" transform="rotate(18 {sx:.1f} {wy})"/>')
    hop = ease_out((t - 0.05) / 0.3)
    jump = -90 * math.sin(math.pi * min(1, max(0, t / 0.3)))
    p = Pose(x=-180 + 920 * hop, y=860 + jump, s=1.6, mouth=talk(a), arm_r=120, hand_r="grip", look=(1, -0.3))
    if s[2] <= t < s[3]:
        which = 0 if t < s[2] + 0.55 else 1
        p = p.but(arm_r=110 if which else 150, arm_l=150 if which == 0 else 20, hand_r="point", hand_l="point",
                  look=((-1, -0.6) if which == 0 else (1, -0.6)), brow="raised")
    elif s[3] <= t < s[4]:
        p = p.but(arm_r=30, look=(0, 0), brow="skeptical", mouth=talk(a, "flat"))
    elif t >= s[4]:
        p = p.but(arm_r=170, arm_l=170, look=(0, -0.3), brow="raised", mouth=talk(a, "grin"),
                  squash=-0.1 * math.exp(-(t - s[4]) * 5))
    world.append(Pip.draw(p))
    cam = Shots([(0, 1.0, 960, 540), (s[1], 1.9, 1150, 470), (s[2], 1.0, 960, 540), (s[3], 1.5, 760, 640),
                 (s[4], 1.0, 960, 540)], shakes=[(s[1], 6), (s[4], 22)])
    over = [card(560, 230, "NVIDIA", t - s[2], gone=t - s[4]), card(1360, 230, "AMD", t - s[2] - 0.55, gone=t - s[4]),
            slam("?", 1380, 470, 260, t - s[3], LIME, hold=s[4] - s[3] - 0.05),
            slam("TSMC", W / 2, 300, 220, t - s[4], LIME),
            slam("Each square = one chip", 1150, 860, 40, t - s[1] - 0.2, INK, hold=s[2] - s[1] - 0.3, fam="Inter SemiBold")]
    return _bg_svg(cam(t, "".join(world)) + "".join(over) + flash(t, s[4]) + brand_bug("THE NEXT SHIFT · TEST") +
               T(80, 1030, "Sources: AMD 10-K (FY2025); NVIDIA Blackwell wafer at TSMC Arizona (Oct 2025). Illustration.", 20, "#5C6270"))


def machine_seq(t, a, s):
    world = [stage(floor_y=900, spot=(1100, 500), spot_r=900),
             machine(560, 900, w=1100, h=640, glow=0.7 + 0.3 * math.sin(t * 6) ** 2)]
    p = Pose(x=380, y=900, s=1.0, mouth=talk(a), arm_r=145, hand_r="point", look=(0.7, -1), brow="raised", lean=-8)
    if s[4] <= t < s[5]:
        p = p.but(arm_r=30, look=(-0.3, 0), brow="skeptical", mouth=talk(a, "flat"), lean=0)
    elif t >= s[5]:
        r = t - s[5]
        drop = min(1.0, max(0.0, (r - 0.9) / 0.35))
        p = p.but(arm_r=40, arm_l=30, look=(0, -0.1), brow="raised", mouth=talk(a, "open"), lean=0,
                  squash=-0.1 * math.exp(-max(0, r - 0.9) * 5),
                  extra={"monocle_drop": (drop ** 2 * 160, drop * 70)})
    world.append(Pip.draw(p))
    cam = Shots([(0, 2.6, 400, 790), (s[0] + 0.7, 1.9, 900, 420), (s[1], 1.0, 960, 540), (s[2], 1.25, 1110, 600),
                 (s[4], 2.4, 400, 780), (s[5], 1.6, 520, 700), (s[6], 2.6, 405, 770)],
                 shakes=[(s[1], 10), (s[3], 18), (s[5] + 0.9, 8), (s[6], 20)])
    price_dt = t - s[5]
    price = ""
    if price_dt >= 0:
        v = 380 * ease_out(price_dt / 0.7)
        price = slam(f"${v:,.0f}–400M" if price_dt > 0.7 else f"${v:,.0f}M", W / 2, 300, 150, price_dt, LIME, hold=s[6] - s[5] + 2)
    over = [slam("1", W / 2, 520, 420, t - s[2], LIME, hold=s[3] - s[2] - 0.05),
            slam("ASML", W / 2, 300, 200, t - s[3], INK, hold=s[4] - s[3] - 0.05),
            price, slam("EACH.", 1440, 600, 140, t - s[6], INK),
            slam("reportedly", W / 2, 180, 40, price_dt, "#AEB4C2", hold=s[6] - s[5] + 2, fam="Inter SemiBold")]
    return _bg_svg(cam(t, "".join(world)) + "".join(over) + flash(t, s[3]) + brand_bug("THE NEXT SHIFT · TEST") +
               T(80, 1030, "Stylised illustration of an ASML EUV system. Price: press reports; no official list price.", 20, "#5C6270"))


def _bg_svg(body):
    return svg(f'<rect x="-50" y="-50" width="{W + 100}" height="{H + 100}" fill="#0C0E13"/>' + body)


FRAMES = {"chart": chart, "wafer": wafer_seq, "machine": machine_seq}
EVENTS = {  # (phrase index, offset, sfx)
    "chart": [(0, 0.0, "impact"), (1, 0.0, "whoosh"), (3, 0.0, "impact"), (4, 0.0, "whoosh"), (5, 0.0, "tick"),
              (6, 0.0, "whoosh"), (7, 0.0, "impact")],
    "wafer": [(0, 0.1, "whoosh"), (1, 0.0, "whoosh"), (2, 0.0, "tick"), (2, 0.55, "tick"), (3, 0.0, "whoosh"), (4, 0.0, "impact")],
    "machine": [(0, 0.6, "whoosh"), (1, 0.0, "whoosh"), (2, 0.0, "impact"), (3, 0.0, "impact"), (4, 0.0, "whoosh"),
                (5, 0.7, "ding"), (6, 0.0, "impact")],
}


def render(name):
    os.makedirs(OUT, exist_ok=True)
    voice, sr, starts = speak(name)
    dur = len(voice) / sr
    n = int(dur * FPS)
    hop = sr / FPS
    env = np.array([np.sqrt(np.mean(voice[int(i * hop):int((i + 1) * hop)] ** 2) + 1e-9) for i in range(n)])
    env = env / (env.max() or 1)
    events = [(starts[i] + off, kind) for i, off, kind in EVENTS[name]]
    audio = mix(name, voice, sr, dur, events)
    silent = os.path.join(OUT, f"{name}{TAG}_silent.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
                           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "veryfast", silent], stdin=subprocess.PIPE)
    for f in range(n):
        ff.stdin.write(cairosvg.svg2png(bytestring=FRAMES[name](f / FPS, float(env[f]), starts).encode(),
                                        output_width=W, output_height=H))
    ff.stdin.close(); ff.wait()
    out = os.path.join(OUT, f"pip_v2_{name}{TAG}.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", audio, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    os.remove(silent)
    return out, round(dur, 1), [round(x, 2) for x in starts]


if __name__ == "__main__":
    for nm in sys.argv[1:] or list(FRAMES):
        print(render(nm))
