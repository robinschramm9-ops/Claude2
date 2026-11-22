"""Turn storyboard + narration durations into an exact timeline and SRT subtitles."""
from __future__ import annotations

import json
import re

from . import brand as B

LEAD_IN = 0.3          # silence before narration starts in each scene
MAX_CHARS = 42         # per subtitle line
MAX_LINES = 2


def build(project, durations: dict) -> tuple[list, float]:
    sb = project.storyboard
    research = project.research
    srcs = {s["id"]: s for s in research.get("sources", [])}
    claims = {c["id"]: c for c in research.get("claims", [])}
    t = 0.0
    tl = []
    chapter = None
    for sc in sb["scenes"]:
        if sc["component"] == "chapter":
            chapter = sc["params"]["title"]
        vd = durations.get(sc["id"], 0.0)
        d = max(float(sc.get("hold", 0)), (LEAD_IN + vd + B.SCENE_PAD) if vd else 0, float(sc.get("min", 0)))
        if d <= 0:
            d = 3.0
        labels = []
        for cid in sc.get("claims", []):
            for sid in claims.get(cid, {}).get("sources", []):
                lab = srcs.get(sid, {}).get("short") or srcs.get(sid, {}).get("publisher")
                if lab and lab not in labels:
                    labels.append(lab)
        tl.append({"id": sc["id"], "component": sc["component"], "params": sc.get("params", {}),
                   "start": round(t, 3), "dur": round(d, 3),
                   "vo_start": round(t + LEAD_IN, 3) if vd else None, "vo_dur": round(vd, 3),
                   "narration": sc.get("narration", ""), "chapter": chapter if sc["component"] != "chapter" else None,
                   "source_labels": labels, "pip": sc.get("pip"),
                   "vo_path": str(project.build / "vo" / f"{sc['id']}.wav") if vd else None})
        t += d
    (project.build / "timeline.json").write_text(json.dumps(tl, indent=1))
    return tl, round(t, 3)


def _chunks(text: str):
    """Split narration into subtitle-sized cues on sentence/clause boundaries."""
    parts = re.split(r"(?<=[.!?;:])\s+|(?<=,)\s+(?=\S{3,})", text.strip())
    cues = []
    for part in parts:
        words, cur = part.split(), ""
        for w in words:
            cand = (cur + " " + w).strip()
            if len(cand) > MAX_CHARS * MAX_LINES:
                cues.append(cur)
                cur = w
            else:
                cur = cand
        if cur:
            cues.append(cur)
    merged = []
    for c in cues:  # merge tiny fragments into their predecessor if it fits
        if merged and len(c) < 18 and len(merged[-1]) + len(c) + 1 <= MAX_CHARS * MAX_LINES:
            merged[-1] += " " + c
        else:
            merged.append(c)
    return merged


def _lines(cue: str):
    if len(cue) <= MAX_CHARS:
        return cue
    words = cue.split()
    best, bi = None, 1
    for i in range(1, len(words)):  # balanced two-line split
        a, b = " ".join(words[:i]), " ".join(words[i:])
        if len(a) <= MAX_CHARS and len(b) <= MAX_CHARS:
            score = abs(len(a) - len(b))
            if best is None or score < best:
                best, bi = score, i
    return " ".join(words[:bi]) + "\n" + " ".join(words[bi:])


def _ts(s):
    ms = int(round(s * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    sec, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"


def _aligned_times(project, sc, chunks):
    """Use TTS character timestamps (ElevenLabs) for exact cue timing, if available."""
    ap = project.build / "vo" / f"{sc['id']}.align.json"
    if not ap.exists():
        return None
    al = json.loads(ap.read_text())
    orig, n_sp = sc["narration"], len(al["starts"])
    if n_sp < 2:
        return None
    # map original-char index -> spoken-text index (pronunciation fixes change lengths slightly)
    scale = (n_sp - 1) / max(len(orig) - 1, 1)
    out, cur = [], 0
    for c in chunks:
        i0 = orig.find(c.split()[0], cur)
        i0 = cur if i0 < 0 else i0
        i1 = min(len(orig) - 1, i0 + len(c) - 1)
        cur = i1 + 1
        out.append((al["starts"][round(i0 * scale)], al["ends"][round(i1 * scale)]))
    return out


def subtitles(project, tl) -> tuple[str, list]:
    cues = []
    for sc in tl:
        if not sc["vo_start"]:
            continue
        chunks = _chunks(sc["narration"])
        timed = _aligned_times(project, sc, chunks)
        if timed is None:  # proportional fallback
            total = sum(len(c) for c in chunks) or 1
            t, timed = 0.0, []
            for c in chunks:
                d = sc["vo_dur"] * len(c) / total
                timed.append((t, t + d - 0.04))
                t += d
        for c, (a, b) in zip(chunks, timed):
            cues.append({"start": sc["vo_start"] + a, "end": sc["vo_start"] + b, "text": _lines(c)})
    for a, b in zip(cues, cues[1:]):  # close tiny gaps (no flicker), never overlap
        if b["start"] - a["end"] < 0.6:
            a["end"] = b["start"] - 0.04
        a["end"] = max(a["end"], a["start"] + 0.5)
    srt = "\n".join(f"{i + 1}\n{_ts(c['start'])} --> {_ts(c['end'])}\n{c['text']}\n" for i, c in enumerate(cues))
    path = project.out / "subtitles.srt"
    path.write_text(srt)
    return str(path), cues
