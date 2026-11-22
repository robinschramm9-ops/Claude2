# next-shift-video

The production system for **THE NEXT SHIFT** – *Understand tomorrow before it happens.*

You give it a topic and approve the research and the script. It produces a narrated, subtitled
1920×1080 video in the channel's motion-graphics style, plus a thumbnail and a QC report.

```
IDEA → RESEARCH ──[human gate]──► SCRIPT + STORYBOARD ──[human gate]──► NARRATION → TIMELINE
     → SVG SCENES → FRAMES → FFMPEG → MIX (score, SFX, ducking, −14 LUFS) → SUBTITLES → QC → video.mp4
```

## Architecture: who does what

| Layer | Done by | Where |
|---|---|---|
| Research, argument, script, storyboard | **Claude Code**, following the skill | `.claude/skills/next-shift-video/SKILL.md` |
| Sourcing rules, approval gates, hook/style/number checks | `nsv validate`, `nsv approve` | `nsv/validate.py`, `nsv/project.py` |
| Narration (pluggable TTS) | `nsv voice` | `nsv/audio.py` |
| Timing, subtitles | derived from real narration lengths | `nsv/timeline.py` |
| Graphics | 14 parametric SVG components + compositor | `nsv/components.py`, `nsv/compose.py` |
| Rendering | cairosvg → PNG → FFmpeg (x264), parallel chunks | `nsv/render.py` |
| Score + SFX | synthesized from scratch (no licensing questions) | `nsv/audio.py` |
| QC | text bounds, min size, spelling, subtitle reading speed, static scenes, number/narration sync, loudness, true peak, codec/duration | `nsv/qc.py` |
| Brand | every color, font, margin and timing constant | `nsv/brand.py` |

Why it's split this way: the editorial work needs judgement and live web research, which Claude
Code already does (no extra API key). Everything after the script is deterministic, so it's plain
Python you can test and rerun for free.

## Setup

Requirements: Python 3.10+, FFmpeg, the **Inter** font family, and optionally `espeak-ng` for offline placeholder narration.

```bash
pip install -r next-shift-video/requirements.txt
# Debian/Ubuntu:  sudo apt-get install ffmpeg fonts-inter espeak-ng
# macOS:          brew install ffmpeg espeak-ng && brew install --cask font-inter
```

## Producing a video

In Claude Code, ask: *"Make a THE NEXT SHIFT video on <topic>"*. The skill walks through the stages.
By hand:

```bash
N=./next-shift-video/nsv.sh
$N new why-data-is-worth-more-than-oil --title "Why Data Is Becoming More Valuable Than Oil"
# research -> videos/<slug>/research.json
$N validate <slug>
$N approve  <slug> research --by robin
# script/storyboard -> videos/<slug>/storyboard.json
$N validate <slug>
$N script   <slug>                 # -> output/script.md, review it
$N still    <slug> s04             # PNG preview of one scene in a few seconds
$N render   <slug> --draft         # watermarked 540p preview, no approval needed (~2 min)
$N approve  <slug> script --by robin
$N render   <slug>                 # final 1080p30 -> output/video.mp4 (+ thumbnail, srt, QC)
```

Outputs land in `videos/<slug>/output/`: `video.mp4`, `thumbnail.png` (1280×720), `subtitles.srt`
(upload it to YouTube as captions), `qc_report.md` and `script.md`.

### Approval gates
`nsv approve` records a fingerprint of the approved files. If anyone edits `research.json` or
`storyboard.json` afterwards, the approval becomes `stale` and the final render refuses to run.
Unapproved renders are always stamped **DRAFT — NOT APPROVED**, so they can't be published by accident.

### Sourcing rules the validator enforces
- Every number in narration or on screen must cite a claim (years and single digits excepted).
- A claim is `verified` only with a primary source or two independent ones.
- `estimate` claims must be hedged in the narration ("about", "by one estimate", ...).
- `unverified` and `disputed` claims can be stored, but can't be used.
- All five editorial questions must be answered. The hook can't be channel chatter.

## Narration providers

Set `storyboard.voice.provider`, or pass `--provider`. Clips are cached per scene, so you only
pay again for scenes whose text changed.

| Provider | Quality | Cost | Setup |
|---|---|---|---|
| `espeak` | Robotic. **Placeholder only, never publish.** | free, offline | `espeak-ng` |
| `openai` | Good, steerable ("documentary narrator" style prompt built in), male voice `onyx` | pay-per-use, typically well under $1 per video; check current pricing | `OPENAI_API_KEY` |
| `elevenlabs` | Best for a documentary male voice | subscription; check current plans | `ELEVENLABS_API_KEY` + `voice.voice_id` |
| `file` | Your own voice (strongest brand asset long term) | your time | put `recordings/<scene_id>.wav` in the project |

Example `voice` blocks:
```json
{"provider": "openai", "voice": "onyx", "model": "gpt-4o-mini-tts"}
{"provider": "elevenlabs", "voice_id": "<from your voice library>", "stability": 0.55}
```
> In the Claude Code cloud sandbox, the API hosts (`api.openai.com`, `api.elevenlabs.io`) have to be
> allowed in the environment's network settings and the key added as a secret. Locally, an env var is enough.

Free local alternatives worth testing on your own machine: Piper and Kokoro TTS. Generate the
WAVs, then use the `file` provider.

## Music
`nsv/audio.py` synthesizes an original, restrained score (minor pads, sub pulse, shimmer) and
whoosh SFX, ducks the music under speech, and normalizes to −14 LUFS with a −2 dBTP target.
To use a licensed track instead, set `"audio": {"music_file": "music/track.wav"}` in the storyboard.
Keep the license with the project.

## Extending

- **New visual component**: add a function in `nsv/components.py` with `@component("name", required=..., optional=...)`.
  It gets `(params, t, d)` and returns an SVG fragment. Schedule reveals relative to `d`.
  Validation and QC pick it up automatically.
- **Change the look**: edit `nsv/brand.py` (palette, fonts, margins, fade/camera timings). Every video follows.
- **New QC rule**: add to `nsv/qc.py`. Return `("BLOCKER"|"WARN"|"INFO", scene_id, message)`.
- **New TTS provider**: add a function to `PROVIDERS` in `nsv/audio.py`.

## Performance
About 75 ms per 1080p frame per core. A 7.5-minute video (~13,000 frames) renders in about 6–7 minutes
on 4 cores. Frames that haven't changed are reused.

## Known limits (honest list)
- **Subtitle and visual sync is proportional within each scene**, not word-accurate. Next step: use
  ElevenLabs' timestamp endpoint or forced alignment for word-level cues.
- **No maps yet.** Maps need licensed or public-domain geodata (e.g. Natural Earth). Planned as a `map` component.
- **No 9:16 Shorts yet.** Components are written for 16:9. Planned: a `brand.VERTICAL` layout plus a cut-down storyboard.
- **QC can't judge quality**: whether the hook works, whether the argument is right, whether the voice sounds
  natural. The report ends with a human checklist for exactly that.
- **Text-bounds QC** checks each scene's final state, not every intermediate animation frame.
