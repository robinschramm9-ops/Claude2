# Review package: "The Company Making Money From Every AI Revolution"

**Status: awaiting your review. Nothing is approved, and nothing is published.**
`nsv status` shows `research: missing`, `script: missing`. The final render is blocked until you approve.

## What's here

| File | What it is |
|---|---|
| `../output/script.md` | **Current version** script: every scene, narration, visual, claim and source |
| `../output/draft.mp4` | Current version, 1080p, placeholder robot voice, watermarked (not in git: 29 MB, can be regenerated) |
| `../output/thumbnail.png` | Current thumbnail |
| `../output/qc_report.md` | Full QC report for the draft (PASS, 0 blockers, 5 warnings) |
| `../research.json` | Current research: 14 sources, 19 claims (18 cited, 1 deliberately unused) |
| `01-caveated-claims.md` | The 8 caveated claims plus 2 I found during review, each with sources and what to verify |
| `02-editorial-review.md` | Weak evidence, weak reasoning, slow sections, chart layout, transitions to check by eye |
| `03-narration-options.md` | OpenAI vs ElevenLabs: cost, quality, setup, keys, recommendation |
| `proposed/` | **Proposed version**, kept separate: `research.json` (19 sources, 23 claims), `storyboard.json` (41 scenes, ~7.1 min), `output/script.md`, `output/thumbnail.png`, `new-scenes.png` |
| `proposed/layout.patch` + `layout-before-after.png` | Chart layout fix. **Not applied** to the working code |

## Proposed changes (pick per item)

| | Scene | Change | Decision |
|---|---|---|---|
| R1 | `s03` | Shorter: TSMC is named ~6 s earlier. | ☐ accept ☐ reject |
| R2 | `s10` | Merged with s10b (the thesis was stated three times in the first 2 minutes). | ☐ accept ☐ reject |
| R3 | `s15b` | NEW: concedes Nvidia earns more, which makes the TSMC argument sharper and more honest. | ☐ accept ☐ reject |
| R4 | `s17b` | Adds 'measured by value', as the source does. | ☐ accept ☐ reject |
| R5 | `s21` | Removes the implication that TSMC uses High-NA (not confirmed in the research). | ☐ accept ☐ reject |
| R6 | `s24` | 92% (older baseline) replaced by 69% (2022, SIA/BCG 2024). | ☐ accept ☐ reject |
| R7 | `s25` | 'Definitions vary' filler replaced by the 2032 projection, so the shift is shown, not just asserted. | ☐ accept ☐ reject |
| R8 | `s28` | Chapter title is now the channel's editorial question. | ☐ accept ☐ reject |
| R9 | `s29b` | NEW: answers 'who controls' explicitly. | ☐ accept ☐ reject |
| R10 | `s30c` | NEW: the honest limit of the thesis (TSMC is exposed to the size of the boom). | ☐ accept ☐ reject |
| R12 | research | `c_customers` downgraded verified → single-source; `c_taiwan` (92%) marked disputed; +5 sources, +4 claims (69%/47% Taiwan, TSMC & Nvidia gross margins) | ☐ accept ☐ reject |
| R13 | thumbnail | "The AI toll booth" (3 words) instead of "The company behind the AI boom" | ☐ accept ☐ reject |
| R14 | code | Layout patch: centered, larger bar charts and chain diagrams | ☐ accept ☐ reject |

## When you're ready (you run these, not me)

```bash
./next-shift-video/nsv.sh approve the-company-making-money-from-every-ai-revolution research --by <your name>
./next-shift-video/nsv.sh approve the-company-making-money-from-every-ai-revolution script   --by <your name>
```
If you accept some of the proposed changes, I'll merge them into the main files first. Approve **after**
that: any edit after approval invalidates it automatically.
