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
                   "source_labels": labels})
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


def subtitles(project, tl) -> tuple[str, list]:
    cues = []
    for sc in tl:
        if not sc["vo_start"]:
            continue
        chunks = _chunks(sc["narration"])
        total = sum(len(c) for c in chunks) or 1
        t = sc["vo_start"]
        for c in chunks:
            d = sc["vo_dur"] * len(c) / total
            cues.append({"start": t, "end": t + d - 0.04, "text": _lines(c)})
            t += d
    srt = "\n".join(f"{i + 1}\n{_ts(c['start'])} --> {_ts(c['end'])}\n{c['text']}\n" for i, c in enumerate(cues))
    path = project.out / "subtitles.srt"
    path.write_text(srt)
    return str(path), cues
