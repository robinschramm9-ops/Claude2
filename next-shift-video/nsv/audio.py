"""Narration (pluggable TTS), original procedural score, SFX and the final mix.

All music and SFX are synthesised here from scratch, so there is no licensing
question. Swap in licensed tracks later via storyboard.audio.music_file.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import urllib.request
import wave

import numpy as np

SR = 48000


# Utilities -------------------------------------------------------------------
def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError(f"{cmd[0]} failed: {r.stderr[-1500:]}")
    return r


def to_wav(src, dst):
    """Normalise any audio to 48 kHz mono 16-bit wav, trimming leading/trailing silence."""
    run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-af",
         "silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
         "silenceremove=start_periods=1:start_threshold=-50dB,areverse",
         "-ar", str(SR), "-ac", "1", "-sample_fmt", "s16", str(dst)])


def read_wav(p) -> np.ndarray:
    with wave.open(str(p)) as w:
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        if w.getnchannels() == 2:
            data = data.reshape(-1, 2).mean(axis=1)
        if w.getframerate() != SR:
            raise ValueError(f"{p}: expected {SR} Hz")
    return data


def write_wav(p, data: np.ndarray, channels=1):
    data = np.clip(data, -1, 1)
    with wave.open(str(p), "wb") as w:
        w.setnchannels(channels)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((data * 32767).astype(np.int16).tobytes())


# TTS providers -----------------------------------------------------------------
DOC_STYLE = ("Calm, authoritative documentary narrator. Measured pace, low warm register, "
             "clear emphasis on numbers, short natural pauses at full stops. Never salesy.")


def tts_espeak(text, out, voice):
    if not shutil.which("espeak-ng"):
        raise RuntimeError("espeak-ng not installed (apt-get install espeak-ng)")
    raw = str(out) + ".raw.wav"
    run(["espeak-ng", "-v", voice.get("voice", "en-us+m3"), "-s", str(voice.get("wpm", 150)),
         "-p", str(voice.get("pitch", 38)), "-w", raw, text])
    to_wav(raw, out)
    os.remove(raw)


def _http(url, body, headers):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def tts_openai(text, out, voice):
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    audio = _http("https://api.openai.com/v1/audio/speech",
                  {"model": voice.get("model", "gpt-4o-mini-tts"), "voice": voice.get("voice", "onyx"),
                   "input": text, "instructions": voice.get("style", DOC_STYLE), "response_format": "wav"},
                  {"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    raw = str(out) + ".raw.wav"
    open(raw, "wb").write(audio)
    to_wav(raw, out)
    os.remove(raw)


def tts_elevenlabs(text, out, voice):
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise RuntimeError("ELEVENLABS_API_KEY is not set")
    vid = voice.get("voice_id")
    if not vid:
        raise RuntimeError("voice.voice_id is required for ElevenLabs (pick one in your voice library)")
    audio = _http(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128",
                  {"text": text, "model_id": voice.get("model", "eleven_multilingual_v2"),
                   "voice_settings": {"stability": voice.get("stability", 0.55),
                                      "similarity_boost": voice.get("similarity", 0.75),
                                      "style": voice.get("style_exaggeration", 0.15)}},
                  {"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    raw = str(out) + ".raw.mp3"
    open(raw, "wb").write(audio)
    to_wav(raw, out)
    os.remove(raw)


def tts_file(text, out, voice):
    """Human-recorded narration: put build/vo/<scene_id>.wav (any format) in voice.dir."""
    raise RuntimeError("provider 'file' is resolved in synthesize()")


PROVIDERS = {"espeak": tts_espeak, "openai": tts_openai, "elevenlabs": tts_elevenlabs}


def speakable(text, pron: dict):
    """Apply pronunciation fixes for TTS only; subtitles keep the original text."""
    for k, v in pron.items():
        text = re.sub(rf"\b{re.escape(k)}\b", v, text)
    return text


def synthesize(project, provider: str | None = None, force=False):
    """Create one wav per scene; cached by (provider, voice, text). Returns {scene_id: seconds}."""
    sb = project.storyboard
    voice = dict(sb.get("voice", {}))
    provider = provider or voice.get("provider", "espeak")
    pron = sb.get("pronunciations", {})
    vo = project.build / "vo"
    vo.mkdir(exist_ok=True)
    durs = {}
    for sc in sb["scenes"]:
        text = sc.get("narration", "").strip()
        if not text:
            continue
        out = vo / f"{sc['id']}.wav"
        if provider == "file":
            src = next((p for p in (project.dir / "recordings").glob(f"{sc['id']}.*")), None)
            if not src:
                raise SystemExit(f"provider=file: missing recordings/{sc['id']}.*")
            to_wav(src, out)
        else:
            key = hashlib.sha256(json.dumps([provider, voice, speakable(text, pron)]).encode()).hexdigest()[:12]
            stamp = vo / f"{sc['id']}.key"
            if force or not out.exists() or not stamp.exists() or stamp.read_text() != key:
                PROVIDERS[provider](speakable(text, pron), out, voice)
                stamp.write_text(key)
        durs[sc["id"]] = len(read_wav(out)) / SR
    return durs, provider


# Score ---------------------------------------------------------------------------
def _note(n):  # MIDI -> Hz
    return 440.0 * 2 ** ((n - 69) / 12)


def score(duration: float, seed: int = 7, bpm: float = 76) -> np.ndarray:
    """Restrained cinematic bed: evolving minor pads, sub pulse, soft high shimmer. Stereo."""
    rng = np.random.default_rng(seed)
    n = int(duration * SR)
    t = np.arange(n) / SR
    L = np.zeros(n, np.float32)
    Rr = np.zeros(n, np.float32)
    prog = [[50, 57, 62, 65], [46, 53, 58, 62], [41, 53, 57, 60], [48, 55, 60, 64]]  # Dm Bb F C
    bar = 4 * 60 / bpm
    chord_len = bar * 2
    xf = 2.5
    k = 0
    start = 0.0
    while start < duration:
        ch = prog[k % len(prog)]
        a, b = max(0, int((start - xf) * SR)), min(n, int((start + chord_len + xf) * SR))
        tt = t[a:b] - (start - xf)
        seg_len = (b - a) / SR
        env = np.minimum(1, np.minimum(tt / xf, (seg_len - tt) / xf)).clip(0, 1) ** 1.5
        for i, m in enumerate(ch):
            f = _note(m)
            det = 1 + (rng.random() - 0.5) * 0.004
            wave_ = (np.sin(2 * np.pi * f * det * tt) + 0.35 * np.sin(2 * np.pi * 2 * f * tt + i)
                     + 0.12 * np.sin(2 * np.pi * 3 * f * tt))
            amp = 0.045 * (0.8 if i == 0 else 1)
            pan = 0.5 + (i - 1.5) * 0.18
            L[a:b] += (wave_ * env * amp * (1 - pan)).astype(np.float32)
            Rr[a:b] += (wave_ * env * amp * pan).astype(np.float32)
        start += chord_len
        k += 1
    # sub pulse on every beat (felt, not heard)
    beat = 60 / bpm
    bt = (t % beat)
    root = np.array([_note(prog[int(x // chord_len) % 4][0] - 12) for x in t[::SR // 10]])
    root = np.repeat(root, SR // 10)[:n]
    sub = np.sin(2 * np.pi * root * t) * np.exp(-bt * 5) * 0.09
    # slow shimmer
    shim = (np.sin(2 * np.pi * _note(81) * t) * (0.5 + 0.5 * np.sin(2 * np.pi * t / 11))) * 0.006
    L += sub + shim
    Rr += sub + shim * 0.8
    fade = np.minimum(1, np.minimum(t / 3, (duration - t) / 4)).clip(0, 1)
    return np.stack([L * fade, Rr * fade], axis=1)


def whoosh(length=0.7, seed=0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = int(length * SR)
    noise = rng.standard_normal(n).astype(np.float32)
    # crude moving-average low-pass whose cutoff sweeps up then down
    out = np.zeros(n, np.float32)
    acc = 0.0
    for i in range(0, n, 64):
        x = i / n
        alpha = 0.02 + 0.25 * np.sin(np.pi * x)
        blk = noise[i:i + 64]
        res = np.empty_like(blk)
        for j, v in enumerate(blk):
            acc += alpha * (v - acc)
            res[j] = acc
        out[i:i + 64] = res
    env = np.sin(np.pi * np.linspace(0, 1, n)) ** 2
    return out * env * 0.35


# Mix ----------------------------------------------------------------------------------
def _measure(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af",
                        "loudnorm=I=-14:TP=-2:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    js = r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1]
    return json.loads(js)


def mix(project, timeline, total, music_db=-20.0, duck_db=-9.0):
    """Lay narration on the timeline, duck the score under speech, add transition SFX,
    then two-pass EBU R128 normalise to -14 LUFS / -2 dBTP target (QC limit -1) (YouTube's reference)."""
    n = int(total * SR) + SR
    voice = np.zeros(n, np.float32)
    sfx = np.zeros(n, np.float32)
    vo = project.build / "vo"
    sw = whoosh()
    for i, sc in enumerate(timeline):
        if sc.get("vo_start") is not None:
            clip = read_wav(vo / f"{sc['id']}.wav")
            a = int(sc["vo_start"] * SR)
            voice[a:a + len(clip)] += clip[: n - a]
        if sc["component"] in ("chapter", "title") or i == 0:
            a = max(0, int((sc["start"] - 0.25) * SR))
            seg = sw[: n - a]
            sfx[a:a + len(seg)] += seg
    sbm = project.storyboard.get("audio", {})
    if sbm.get("music_file"):
        mf = project.dir / sbm["music_file"]
        tmp = project.build / "music_in.wav"
        run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", str(mf), "-t", f"{n / SR:.2f}",
             "-ar", str(SR), "-ac", "2", str(tmp)])
        with wave.open(str(tmp)) as w:
            mus = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, 2) / 32768
    else:
        mus = score(n / SR, seed=int(sbm.get("seed", 7)))
    mus = mus[:n]
    if len(mus) < n:
        mus = np.pad(mus, ((0, n - len(mus)), (0, 0)))
    # sidechain-style ducking from the speech envelope (smoothed, 150 ms attack/release)
    win_ = int(0.15 * SR)
    env = np.convolve(np.abs(voice), np.ones(win_) / win_, mode="same")
    speaking = np.clip(env / 0.02, 0, 1)
    gain = 10 ** ((music_db + duck_db * speaking) / 20)
    out = mus * gain[:, None]
    out += (voice * 0.9)[:, None]
    out += (sfx * 10 ** (-14 / 20))[:, None] * np.array([1.0, 0.85])
    raw = project.build / "mix_raw.wav"
    write_wav(raw, out.reshape(-1), channels=2)
    m = _measure(raw)
    final = project.build / "mix.wav"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-af",
         f"loudnorm=I=-14:TP=-2:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
         f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true",
         "-ar", str(SR), str(final)])
    return final
