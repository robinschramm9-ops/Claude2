"""nsv - THE NEXT SHIFT video production CLI.

    nsv new <slug> --title "..."         scaffold a project in videos/<slug>/
    nsv components                       list visual components and their params
    nsv validate <slug>                  editorial + sourcing checks
    nsv script <slug>                    export script.md for human review
    nsv approve <slug> research|script --by NAME
    nsv status <slug>
    nsv still <slug> <scene_id> [--at 0.8]   PNG preview of one scene (fast iteration)
    nsv voice <slug> [--provider espeak|openai|elevenlabs|file] [--force]
    nsv render <slug> [--draft [--full-res]] [--provider ...] [--burn-subs]
    nsv thumbnail <slug>
    nsv qc <slug>
"""
from __future__ import annotations

import argparse
import json
import sys

from . import project as P


def _p(slug):
    return P.Project(slug)


def cmd_new(a):
    d = P.new_project(a.slug, a.title)
    print(f"created {d}\nnext: research -> fill research.json, then nsv validate {a.slug}")


def cmd_components(a):
    from .components import SCHEMAS
    for k, (req, opt) in sorted(SCHEMAS.items()):
        print(f"{k:12s} required: {', '.join(req) or '-':32s} optional: {', '.join(opt) or '-'}")


def _report(errors, warns):
    for e in errors:
        print(f"  ERROR  {e}")
    for w in warns:
        print(f"  warn   {w}")


def cmd_validate(a):
    from .validate import validate_research, validate_storyboard
    pr = _p(a.slug)
    e, w, _, _ = validate_research(pr.research)
    print("research.json:", "OK" if not e else f"{len(e)} errors")
    _report(e, w)
    if pr.path("storyboard.json").exists():
        e2, w2, st = validate_storyboard(pr.storyboard, pr.research)
        e2 = [x for x in e2 if x not in e]
        w2 = [x for x in w2 if x not in w]
        print("storyboard.json:", "OK" if not e2 else f"{len(e2)} errors", json.dumps(st))
        _report(e2, w2)
        e += e2
    sys.exit(1 if e else 0)


def cmd_script(a):
    pr = _p(a.slug)
    sb, r = pr.storyboard, pr.research
    claims = {c["id"]: c for c in r["claims"]}
    srcs = {s["id"]: s for s in r["sources"]}
    ed = r["editorial"]
    L = [f"# {sb['title']}", "", f"**Central question:** {r['central_question']}", "",
         f"**Thesis:** {sb.get('thesis', '')}", "", "| | |", "|---|---|"]
    L += [f"| {k.replace('_', ' ').title()} | {v} |" for k, v in ed.items()]
    L += ["", "---", ""]
    for sc in sb["scenes"]:
        L.append(f"### {sc['id']} - `{sc['component']}`")
        if sc.get("narration"):
            L.append(f"> {sc['narration']}")
        L.append(f"*Visual:* {sc.get('visual_note') or json.dumps(sc.get('params', {}))[:220]}")
        for cid in sc.get("claims", []):
            c = claims.get(cid, {})
            L.append(f"- **[{cid}]** _{c.get('status')}_ - {c.get('text')} "
                     f"({', '.join(srcs.get(s, {}).get('publisher', s) for s in c.get('sources', []))})")
        L.append("")
    L += ["---", "", "## Sources", ""]
    L += [f"- **{s['id']}** {s['publisher']}: [{s['title']}]({s['url']}) ({s['type']}, accessed {s['accessed']})"
          for s in r["sources"]]
    words = sum(len(s.get("narration", "").split()) for s in sb["scenes"])
    L.insert(2, f"*{words} words, approx. {words / 150:.1f} min at 150 wpm*")
    out = pr.out / "script.md"
    out.write_text("\n".join(L) + "\n")
    print(out)


def cmd_approve(a):
    from .validate import validate_research, validate_storyboard
    pr = _p(a.slug)
    if a.gate == "research":
        e = validate_research(pr.research)[0]
    else:
        e = validate_storyboard(pr.storyboard, pr.research)[0]
    if e:
        _report(e, [])
        sys.exit(f"cannot approve {a.gate}: fix the errors above first")
    pr.approve(a.gate, a.by)
    print(f"{a.gate} approved by {a.by} (fingerprint {pr.fingerprint(a.gate)}). "
          f"Editing the underlying files will invalidate this approval.")


def cmd_status(a):
    pr = _p(a.slug)
    for g in P.GATES:
        print(f"{g:9s} {pr.gate_status(g)}")
    for f in ("draft.mp4", "video.mp4", "thumbnail.png", "subtitles.srt", "qc_report.md", "script.md"):
        p = pr.out / f
        print(f"{f:14s} {'yes' if p.exists() else '-'}")


def _voice_and_timeline(pr, provider=None, force=False):
    from . import audio, timeline
    durs, prov = audio.synthesize(pr, provider, force)
    tl, total = timeline.build(pr, durs)
    print(f"narration via {prov}: {len(durs)} clips, runtime {total / 60:.2f} min")
    return tl, total, prov


def cmd_voice(a):
    _voice_and_timeline(_p(a.slug), a.provider, a.force)


def cmd_still(a):
    from . import render, timeline
    pr = _p(a.slug)
    tlp = pr.build / "timeline.json"
    if tlp.exists():
        tl = json.loads(tlp.read_text())
    else:  # estimate durations from word counts when no narration exists yet
        tl, _ = timeline.build(pr, {s["id"]: len(s.get("narration", "").split()) / 2.5
                                    for s in pr.storyboard["scenes"] if s.get("narration")})
    sc = next((s for s in tl if s["id"] == a.scene), None)
    if not sc:
        sys.exit(f"no scene {a.scene}")
    out = pr.build / f"still_{a.scene}.png"
    render.still(tl, sc["start"] + sc["dur"] * a.at, out)
    print(out)


def cmd_thumbnail(a):
    from .thumbnail import render_thumbnail
    pr = _p(a.slug)
    print(render_thumbnail(pr, pr.out / "thumbnail.png"))


def cmd_render(a):
    from . import audio, qc, render, timeline
    from .thumbnail import render_thumbnail
    pr = _p(a.slug)
    if not a.draft:
        pr.require_gates()
    tl, total, prov = _voice_and_timeline(pr, a.provider)
    if prov == "espeak" and not a.draft:
        print("WARNING: espeak is a robotic placeholder voice. Do not publish this narration.")
    srt, cues = timeline.subtitles(pr, tl)
    mixp = audio.mix(pr, tl, total)
    vid = render.render_video(pr, tl, total, mixp, draft=a.draft, workers=a.workers,
                              burn_subs=srt if a.burn_subs else None, full_res=a.full_res)
    render_thumbnail(pr, pr.out / "thumbnail.png")
    blockers, issues, rep = qc.run_qc(pr, tl, total, cues, vid)
    print(f"QC: {'FAIL' if blockers else 'PASS'} ({len(blockers)} blockers) -> {rep}")
    for b in blockers:
        print("  BLOCKER", b[1], b[2])
    sys.exit(1 if blockers else 0)


def cmd_qc(a):
    from . import qc, timeline
    pr = _p(a.slug)
    tl = json.loads((pr.build / "timeline.json").read_text())
    total = tl[-1]["start"] + tl[-1]["dur"]
    _, cues = timeline.subtitles(pr, tl)
    vid = pr.out / "video.mp4"
    if not vid.exists():
        vid = pr.out / "draft.mp4"
    blockers, issues, rep = qc.run_qc(pr, tl, total, cues, vid if vid.exists() else None)
    print(rep.read_text())
    sys.exit(1 if blockers else 0)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="nsv", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("new"); s.add_argument("slug"); s.add_argument("--title", required=True); s.set_defaults(f=cmd_new)
    s = sub.add_parser("components"); s.set_defaults(f=cmd_components)
    for name, fn in (("validate", cmd_validate), ("script", cmd_script), ("status", cmd_status),
                     ("thumbnail", cmd_thumbnail), ("qc", cmd_qc)):
        s = sub.add_parser(name); s.add_argument("slug"); s.set_defaults(f=fn)
    s = sub.add_parser("approve"); s.add_argument("slug"); s.add_argument("gate", choices=P.GATES)
    s.add_argument("--by", required=True); s.set_defaults(f=cmd_approve)
    s = sub.add_parser("still"); s.add_argument("slug"); s.add_argument("scene")
    s.add_argument("--at", type=float, default=0.8); s.set_defaults(f=cmd_still)
    provs = ["espeak", "openai", "elevenlabs", "file"]
    s = sub.add_parser("voice"); s.add_argument("slug"); s.add_argument("--provider", choices=provs)
    s.add_argument("--force", action="store_true"); s.set_defaults(f=cmd_voice)
    s = sub.add_parser("render"); s.add_argument("slug"); s.add_argument("--draft", action="store_true")
    s.add_argument("--provider", choices=provs); s.add_argument("--workers", type=int)
    s.add_argument("--burn-subs", action="store_true")
    s.add_argument("--full-res", action="store_true", help="draft at 1080p/30fps (still watermarked)")
    s.set_defaults(f=cmd_render)
    a = ap.parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()
