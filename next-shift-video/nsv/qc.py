"""Automated quality control. Produces output/qc_report.md. BLOCKERS fail the build."""
from __future__ import annotations

import json
import re
import subprocess

from . import brand as B
from .components import REGISTRY
from .fx import text_width
from .validate import validate_storyboard

TEXT_RE = re.compile(r'<text x="([\d.-]+)" y="([\d.-]+)" font-family="([^"]+)" font-size="([\d.]+)"[^>]*'
                     r'text-anchor="(\w+)"[^>]*>([^<]*)</text>')
STOP = {"ai", "gpu", "gpus", "cpu", "cpus", "tpu", "tpus", "apps", "app", "fab", "fabs", "chatbot", "chatbots",
        "startup", "startups", "smartphone", "smartphones", "online", "dataset", "datasets", "algorithm",
        "algorithms", "automation", "robotics", "blockchain", "crypto", "fintech", "subscription"}


def _text_bounds(tl):
    issues = []
    for sc in tl:
        t = max(0.0, sc["dur"] - B.SCENE_FADE - 0.05)
        svg = REGISTRY[sc["component"]](sc["params"], t, sc["dur"])
        for m in TEXT_RE.finditer(svg):
            x, y, fam, size, anchor, s = m.groups()
            x, y, size = float(x), float(y), float(size)
            s = s.replace("&amp;", "&").replace("&quot;", '"')
            w = text_width(s, int(size), fam)
            left = x - w / 2 if anchor == "middle" else x - w if anchor == "end" else x
            right = left + w
            if size < B.MIN_TEXT_PX:
                issues.append(("BLOCKER", sc["id"], f"text '{s[:30]}' is {size:.0f}px (< {B.MIN_TEXT_PX}px minimum)"))
            if left < 60 or right > B.W - 60 or y < 60 or y > B.H - 70:
                issues.append(("BLOCKER", sc["id"], f"text '{s[:30]}' leaves the safe frame "
                                                    f"(x {left:.0f}-{right:.0f}, y {y:.0f})"))
    return issues


def _spelling(sb):
    try:
        from spellchecker import SpellChecker
    except ImportError:
        return [("WARN", "-", "pyspellchecker not installed; spelling not checked")]
    sp = SpellChecker()
    gloss = {w.lower() for w in sb.get("glossary", [])} | STOP
    issues, names = [], set()
    for sc in sb["scenes"]:
        blobs = [sc.get("narration", "")] + list(_strings(sc.get("params", {})))
        for blob in blobs:
            for w in re.findall(r"[A-Za-z][A-Za-z'\u2019\-]{2,}", blob):
                w = w.replace("\u2019", "'")
                lw = re.sub(r"'s$", "", w.lower().strip("'-"))
                if lw in gloss or w.isupper() or re.sub(r"'s$", "", w).isupper():
                    continue
                if not sp.unknown([lw]):          # whole word known (incl. contractions)
                    continue
                parts = [p for p in re.split(r"-", lw) if len(p) > 2 and "'" not in p]
                unknown = sp.unknown(parts) if parts else set()
                if not unknown:
                    continue
                if w[0].isupper():
                    names.add(w)
                else:
                    issues.append(("WARN", sc["id"], f"possible misspelling: '{w}' "
                                                     f"(suggest: {sp.correction(lw)})"))
    if names:
        issues.append(("INFO", "-", "check proper nouns: " + ", ".join(sorted(names))))
    return issues


def _strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k != "color":
                yield from _strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from _strings(v)


def _visual_numbers(params):
    for k in ("value",):
        if k in params:
            yield params[k]
    for it in params.get("items", []) if isinstance(params.get("items"), list) else []:
        if isinstance(it, dict) and "value" in it:
            yield it["value"]


def _sync(tl, cues):
    issues = []
    for sc in tl:
        narr = sc["narration"].replace(",", "")
        for v in _visual_numbers(sc["params"]):
            try:
                leads = {str(int(float(v))), str(round(float(v)))}
            except (TypeError, ValueError):
                continue
            if min(map(len, leads)) >= 2 and not any(re.search(rf"\b{l}\b", narr) for l in leads):
                issues.append(("WARN", sc["id"], f"on-screen number {v} is never spoken - viewers may be confused"))
        if sc["dur"] > 20:
            issues.append(("WARN", sc["id"], f"scene runs {sc['dur']:.0f}s - split it, it will feel static"))
        elif sc["component"] in ("statement", "quote", "big_number") and sc["dur"] > 14:
            issues.append(("WARN", sc["id"], f"{sc['component']} holds for {sc['dur']:.0f}s - consider a second beat"))
    for a, b in zip(cues, cues[1:]):
        if b["start"] < a["end"] - 0.01:
            issues.append(("BLOCKER", "-", f"subtitles overlap at {a['start']:.1f}s"))
    for c in cues:
        d = c["end"] - c["start"]
        cps = len(c["text"]) / d if d > 0 else 99
        if cps > 21:
            issues.append(("WARN", "-", f"subtitle at {c['start']:.1f}s reads at {cps:.0f} chars/s (>21)"))
    return issues


def _probe(path, total):
    issues = []
    r = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return [("BLOCKER", "-", f"ffprobe cannot read {path}")], {}
    info = json.loads(r.stdout)
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    dur = float(info["format"]["duration"])
    if not v or v["codec_name"] != "h264" or v.get("pix_fmt") != "yuv420p":
        issues.append(("BLOCKER", "-", "video stream must be h264/yuv420p"))
    if v and (v["width"], v["height"]) not in ((1920, 1080), (960, 540)):
        issues.append(("BLOCKER", "-", f"resolution {v['width']}x{v['height']}"))
    if not a or a["codec_name"] != "aac":
        issues.append(("BLOCKER", "-", "missing AAC audio stream"))
    if abs(dur - total) > 0.6:
        issues.append(("BLOCKER", "-", f"duration {dur:.1f}s != timeline {total:.1f}s"))
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-map", "0:a",
                        "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    summ = r.stderr[r.stderr.rfind("Summary:"):]
    li = re.search(r"I:\s+(-?[\d.]+) LUFS", summ)
    tp = re.search(r"Peak:\s+(-?[\d.]+) dBFS", summ)
    lufs = float(li.group(1)) if li else None
    peak = float(tp.group(1)) if tp else None
    if lufs is None or not -15.5 <= lufs <= -12.5:
        issues.append(("BLOCKER", "-", f"integrated loudness {lufs} LUFS (target -14 +/-1.5)"))
    if peak is not None and peak > -1.0:
        issues.append(("BLOCKER", "-", f"true peak {peak} dBFS (> -1)"))
    return issues, {"duration_s": round(dur, 2), "lufs": lufs, "true_peak_dbfs": peak,
                    "video": f"{v['codec_name']} {v['width']}x{v['height']} {v.get('r_frame_rate')}" if v else None}


def run_qc(project, tl, total, cues, video_path=None):
    sb, research = project.storyboard, project.research
    errors, warns, stats = validate_storyboard(sb, research)
    issues = [("BLOCKER", "-", e) for e in errors] + [("WARN", "-", w) for w in warns]
    issues += _text_bounds(tl)
    issues += _spelling(sb)
    issues += _sync(tl, cues)
    media = {}
    if video_path:
        mi, media = _probe(video_path, total)
        issues += mi
    claims = {c["id"]: c for c in research.get("claims", [])}
    caveats = [f"{cid} ({claims[cid]['status']}): {claims[cid].get('notes', '')}"
               for cid in sorted({c for s in sb["scenes"] for c in s.get("claims", [])})
               if cid in claims and claims[cid]["status"] != "verified"]
    blockers = [i for i in issues if i[0] == "BLOCKER"]
    lines = [f"# QC report: {sb.get('title')}", "",
             f"**Result: {'FAIL' if blockers else 'PASS'}** | {len(blockers)} blockers, "
             f"{sum(1 for i in issues if i[0] == 'WARN')} warnings", "",
             f"- Runtime: {total / 60:.1f} min ({total:.1f}s), {stats['scenes']} scenes, {stats['words']} words",
             f"- Claims cited: {stats['claims_used']}"]
    for k, v in media.items():
        lines.append(f"- {k}: {v}")
    lines += ["", "## Issues", ""]
    lines += [f"- **{lvl}** `{sid}` {msg}" for lvl, sid, msg in issues] or ["- none"]
    lines += ["", "## Claims used with caveats (human must be comfortable with these)", ""]
    lines += [f"- {c}" for c in caveats] or ["- none"]
    lines += ["", "## Human review checklist (automation cannot judge these)", "",
              "- [ ] Does the hook make you want to keep watching?",
              "- [ ] Is there a clear argument, not just a list of facts?",
              "- [ ] Would a domain expert find anything misleading?",
              "- [ ] Does the narration sound natural at every scene boundary?",
              "- [ ] Thumbnail + title: honest, and would you click?"]
    rep = project.out / "qc_report.md"
    rep.write_text("\n".join(lines) + "\n")
    return blockers, issues, rep
