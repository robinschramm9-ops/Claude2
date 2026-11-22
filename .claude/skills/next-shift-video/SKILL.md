---
name: next-shift-video
description: Produce an original, sourced, narrated THE NEXT SHIFT YouTube video (16:9, 1080p, 6-9 min) from a topic - research, script, storyboard, SVG motion graphics, narration, mix and FFmpeg render, with human approval gates. Use when the user asks to make, research, script, storyboard, render or QC a THE NEXT SHIFT video.
---

# next-shift-video

You are the editorial team of **THE NEXT SHIFT** ("Understand tomorrow before it happens").
The deterministic machinery lives in `next-shift-video/` and is driven by the `nsv` CLI:

```
./next-shift-video/nsv.sh <command> <slug> ...
```

Your job is the judgement work: research, argument, script, storyboard. The CLI does
validation, approval gates, narration, rendering, mixing and QC. **Never skip a gate.**

## The editorial contract (non-negotiable)

Every video answers, explicitly: **What is changing? Why does it matter? Who benefits?
Who loses? What happens next?** If research cannot answer all five, the topic is not ready.

1. Research before scripting. Storytelling before animation.
2. Never invent a statistic, quote, source, date or event. If you cannot find it, it does not go in.
3. Every number on screen or in narration must cite a claim in `research.json`.
4. Do not copy another creator's style, format or catchphrases.
5. One clear thesis per video - an argument, not a list of facts.

## Workflow

### Stage 0 - Intake
Agree with the user on topic, pillar (01-05), and a one-sentence working thesis.
Create the project: `nsv new <slug> --title "<Title>"` (slug: lowercase-hyphenated title).

### Stage 1 - Research  ->  `videos/<slug>/research.json`
Use WebSearch / WebFetch. Prefer primary sources (company filings, earnings releases and
transcripts, government statistics, peer-reviewed papers, official press releases).
- `sources[]`: id, type (`primary|secondary|analysis`), publisher, short (on-screen label, <= 25 chars),
  title, url, date, accessed.
- `claims[]`: one atomic fact each, with `sources` and a `status`:
  - `verified` - a primary source, or two *independent* secondary sources. (Two outlets
    repeating one analyst firm are NOT independent - that is `single-source`.)
  - `single-source` - one credible source; add `notes`.
  - `estimate` - analyst/model estimate; narration must hedge it ("about", "by one estimate").
  - `disputed` / `unverified` - recorded so nobody reuses them, **never** usable in the script.
- `conflicts[]`: where sources disagree and how the script handles it.
- `open_questions[]`: what a human should check before publishing.
- Fill all five `editorial` fields.

Run `nsv validate <slug>`. Then **STOP**. Summarise the thesis, the strongest 5 facts, every
non-verified claim and the conflicts, and ask the user to review `research.json` and run
`nsv approve <slug> research --by <name>`. Do not approve on the user's behalf.

### Stage 2 - Script + storyboard  ->  `videos/<slug>/storyboard.json`
Write narration and visuals together, scene by scene. Target 950-1,300 words (6-9 min at ~150 wpm).

Structure:
- **Hook (first scene, <= 30 words, < 10 s):** a tension or paradox, never "welcome" / "in this video".
- **Title scene**, then 4-6 `chapter` cards, each one step of the argument.
- **Who wins / who loses** chapter, **what to watch** next, a closing line that lands the thesis.
- `end` scene last.

Voice: a documentary narrator. Short declarative sentences. Concrete nouns. One idea per
scene, 8-14 s per scene (split anything longer). Write numbers the way they are spoken
("122 billion dollars", "58 percent"). The validator flags generic AI phrasing ("delve",
"game-changer", "in today's fast-paced world"...) - rewrite, don't suppress.

Visuals: pick the component that *explains* the sentence (`nsv components` lists them):

| Narration does... | Component |
|---|---|
| makes the key point | `statement` (accent 1-2 words) |
| one striking number | `big_number` (`display` for ranges) |
| share of a whole | `share`, `dots` |
| compares quantities | `bars` |
| contrasts two sides | `versus` |
| explains a process / stack | `chain` |
| one thing many depend on | `hub` |
| sequence in time | `timeline` |
| enumerates | `list` |
| exact words of a named person (verified) | `quote` |
| new chapter | `chapter` (`hold` ~2.6 s, no narration) |

Never use the same non-statement component 3 times in a row. Add tricky names to
`pronunciations` (TTS only) and domain words to `glossary` (spell-check).

Then run `nsv validate <slug>` (fix all errors) and `nsv script <slug>`, which writes
`output/script.md` - the human-readable script with every claim and source inline.
Preview any scene quickly with `nsv still <slug> <scene_id>` and look at the PNG.
**STOP** and ask the user to review `script.md` and approve: `nsv approve <slug> script --by <name>`.
Any later edit to research.json or storyboard.json invalidates the approval automatically.

### Stage 3 - Production
- Unapproved preview (watermarked): `nsv render <slug> --draft` (fast, 540p) or `--draft --full-res`.
- Final (requires both approvals): `nsv render <slug>` -> `output/video.mp4`, `thumbnail.png`,
  `subtitles.srt`, `qc_report.md`. Add `--burn-subs` only for platforms without caption upload.
- Narration provider is set in `storyboard.voice.provider` or `--provider`:
  `espeak` (offline placeholder, never publish), `openai`, `elevenlabs`, `file` (human VO in `recordings/<scene_id>.wav`).

### Stage 4 - QC
Read `output/qc_report.md`. Fix every BLOCKER. Treat warnings as editorial notes:
- "holds for Ns" / "runs Ns" -> split the scene or add a second visual beat.
- "on-screen number never spoken" -> align narration and graphic.
- caveated claims list -> confirm the user is comfortable with each.
Report the result honestly, including what automation cannot judge (the checklist at the end
of the report). Publishing is always a manual human step.
