"""Editorial validation: sourcing, structure, style. Errors block, warnings inform."""
from __future__ import annotations

import re

from .components import SCHEMAS

CLAIM_STATUSES = {"verified", "single-source", "estimate", "disputed", "unverified"}
USABLE = {"verified", "single-source", "estimate"}
SOURCE_TYPES = {"primary", "secondary", "analysis"}
EDITORIAL_KEYS = ("what_changes", "why_it_matters", "who_benefits", "who_loses", "what_next")
WPM = 150

# Phrases that make a script sound like a generic AI assistant.
BANNED = ["in today's fast-paced world", "delve", "game-changer", "game changer", "revolutionize",
          "unlock the power", "it's important to note", "in conclusion", "landscape of", "tapestry",
          "buckle up", "let's dive", "dive into", "without further ado", "ever-evolving", "navigate the",
          "harness the power", "cutting-edge", "seamless", "a testament to", "smash that like"]
HEDGES = ("estimate", "about", "roughly", "around", "nearly", "almost", "analysts", "reportedly",
          "some", "could", "may", "up to", "more than", "over", "at least", "by one", "according")

NUM_RE = re.compile(r"(?<![\w.])(\$?\d[\d,.]*\s*(%|percent|billion|million|trillion|nanometers?|nm)?)", re.I)
YEAR_RE = re.compile(r"^(19|20)\d\d$")


def _numbers(s: str):
    out = []
    for m in NUM_RE.finditer(s or ""):
        tok = m.group(1).strip()
        bare = tok.replace("$", "").replace(",", "")
        if YEAR_RE.match(bare) or re.fullmatch(r"0?\d", bare):  # years and 0-9 ordinals
            continue
        out.append(tok)
    return out


def _texts(obj):
    """All human-visible strings inside component params."""
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k not in ("color", "highlight", "decimals", "flow", "size"):
                yield from _texts(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _texts(v)
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        yield str(obj)


def validate_research(r: dict):
    errors, warns = [], []
    for k in ("topic", "central_question"):
        if not str(r.get(k, "")).strip():
            errors.append(f"research.{k} is empty")
    ed = r.get("editorial", {})
    for k in EDITORIAL_KEYS:
        if not str(ed.get(k, "")).strip():
            errors.append(f"research.editorial.{k} is empty - every video must answer it")
    srcs = {}
    for s in r.get("sources", []):
        sid = s.get("id")
        if not sid or sid in srcs:
            errors.append(f"source id missing/duplicate: {sid}")
        srcs[sid] = s
        for k in ("title", "publisher", "url", "accessed"):
            if not s.get(k):
                errors.append(f"source {sid}: missing {k}")
        if s.get("type") not in SOURCE_TYPES:
            errors.append(f"source {sid}: type must be one of {sorted(SOURCE_TYPES)}")
    if not srcs:
        errors.append("research has no sources")
    claims = {}
    for c in r.get("claims", []):
        cid = c.get("id")
        if not cid or cid in claims:
            errors.append(f"claim id missing/duplicate: {cid}")
        claims[cid] = c
        if c.get("status") not in CLAIM_STATUSES:
            errors.append(f"claim {cid}: status must be one of {sorted(CLAIM_STATUSES)}")
        if not c.get("sources"):
            errors.append(f"claim {cid}: no sources")
        for sid in c.get("sources", []):
            if sid not in srcs:
                errors.append(f"claim {cid}: unknown source {sid}")
        if c.get("status") == "verified":
            types = {srcs.get(s, {}).get("type") for s in c.get("sources", [])}
            if len(c.get("sources", [])) < 2 and "primary" not in types:
                errors.append(f"claim {cid}: 'verified' needs a primary source or two independent sources")
        if c.get("status") in ("single-source", "estimate", "disputed") and not c.get("notes"):
            warns.append(f"claim {cid}: status '{c.get('status')}' should carry a note explaining the caveat")
    return errors, warns, srcs, claims


def validate_storyboard(sb: dict, research: dict):
    errors, warns, srcs, claims = validate_research(research)
    scenes = sb.get("scenes", [])
    if not scenes:
        errors.append("storyboard has no scenes")
    ids, words = set(), 0
    comps = []
    for i, sc in enumerate(scenes):
        sid = sc.get("id") or f"#{i}"
        if sid in ids:
            errors.append(f"{sid}: duplicate scene id")
        ids.add(sid)
        comp = sc.get("component")
        if comp not in SCHEMAS:
            errors.append(f"{sid}: unknown component '{comp}'")
            continue
        comps.append(comp)
        req, opt = SCHEMAS[comp]
        params = sc.get("params", {})
        for k in req:
            if k not in params:
                errors.append(f"{sid}: component '{comp}' requires param '{k}'")
        for k in params:
            if k not in req + opt:
                warns.append(f"{sid}: param '{k}' is not used by '{comp}'")
        narr = sc.get("narration", "")
        if not narr.strip() and not sc.get("hold"):
            errors.append(f"{sid}: needs narration or a 'hold' duration")
        words += len(narr.split())
        used = sc.get("claims", [])
        for cid in used:
            c = claims.get(cid)
            if not c:
                errors.append(f"{sid}: unknown claim {cid}")
            elif c.get("status") not in USABLE:
                errors.append(f"{sid}: claim {cid} is '{c.get('status')}' and cannot be stated as fact")
            elif c.get("status") == "estimate" and not any(h in narr.lower() for h in HEDGES):
                errors.append(f"{sid}: claim {cid} is an estimate - narration must hedge it "
                              f"(e.g. 'about', 'analysts estimate')")
        nums = _numbers(narr) + [n for s in _texts(params) for n in _numbers(s)]
        if nums and not used:
            errors.append(f"{sid}: states numbers {nums[:4]} but cites no claim")
        low = narr.lower()
        for b in BANNED:
            if b in low:
                warns.append(f"{sid}: generic phrasing '{b}'")
    # structure --------------------------------------------------------------
    if scenes:
        first = scenes[0].get("narration", "")
        if len(first.split()) > 32:
            warns.append("hook: first scene runs past ~10 s of speech; tighten the opening")
        if any(w in first.lower() for w in ("welcome", "in this video", "hey guys", "subscribe")):
            errors.append("hook: first line is channel chatter, not a hook")
    mins = words / WPM
    if not 6 <= mins <= 9.5:
        warns.append(f"estimated runtime {mins:.1f} min is outside the 6-9 min target")
    for i in range(len(comps) - 2):
        if comps[i] == comps[i + 1] == comps[i + 2] and comps[i] != "statement":
            warns.append(f"repetition: '{comps[i]}' used 3x in a row at scenes {i + 1}-{i + 3}")
    if comps:
        top = max(set(comps), key=comps.count)
        if comps.count(top) / len(comps) > 0.4:
            warns.append(f"variety: '{top}' is {comps.count(top)}/{len(comps)} scenes")
    stats = {"scenes": len(scenes), "words": words, "est_minutes": round(mins, 1),
             "claims_used": len({c for s in scenes for c in s.get("claims", [])})}
    return errors, warns, stats
