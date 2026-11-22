# Editorial review: "The Company Making Money From Every AI Revolution"

Reviewed version: current storyboard (39 scenes, 7.4 min, 955 words). Proposed changes are in
`review/proposed/`. **The current version is unchanged** and both versions pass validation.

Verdict: the structure works and the visuals are consistent. But the argument is **overstated in one
direction and outdated in one fact**. Both are fixable before narration.

---

## 1. Factual claims that need stronger evidence

Ranked by how badly a knowledgeable viewer could catch us out.

| # | Claim | Problem | Proposed fix |
|---|---|---|---|
| 1 | **92% of advanced capacity is in Taiwan** (s24) | Older SIA/BCG baseline. SIA/BCG's 2024 report says **69% (2022)**, projected **47% by 2032**. The single most quotable number in the video is out of date. | v2 uses 69% → 47% and shows the shift (s24, s25). Verify page 14 of the PDF. |
| 2 | **TSMC makes Google's and Amazon's AI chips** (s02, s06, s10, s16…) | It's the backbone of the thesis, yet the evidence is a 2023 article plus an inference. TSMC doesn't name customers, and AWS's 2025 Trainium3 launch names no foundry. It was marked *verified*; it isn't. | Downgraded to single-source in v2. Before publishing, find primary confirmation (Nvidia 10-K supplier section; company statements). If Google/AWS can't be confirmed, say "Nvidia and AMD" and "reportedly" for the rest. |
| 3 | **"More than 90% of CoWoS capacity"** (s17b) | Epoch AI measures CoWoS **and HBM** supply **by value**. Our sentence drops "by value", which makes it sound like a capacity share. | v2 adds "measured by value". |
| 4 | **"~70% foundry share"** (s08, s09, thumbnail) | Two news relays of one TrendForce release. Also, $122.5B ÷ $169.5B (TSMC ÷ top-10 total) = 72%, not 69.9%, so the denominator is something else. Check what. | Read TrendForce's own release before publishing. |
| 5 | **CEO "very nervous"** (s30b) | Taken from a Tom's Hardware headline, not the transcript. | Quote the transcript or soften to "has acknowledged concerns about an AI bubble". |
| 6 | **2026 capex $52–56B** (s30) | Single secondary source. The primary source (the earnings call) is already in our source list but wasn't checked. | Confirm in transcript S1. |
| 7 | **Qualitative facts without citations**: "doesn't compete with its customers" (s07), "active earthquake zone" (s25b), "Nvidia doesn't manufacture its chips" (s16) | All true and well known, but the validator only checks numbers, so these were never sourced. | Accept them as common knowledge, or add claims. **System gap:** the validator should also accept claim tags on non-numeric facts. I'd add that next. |

## 2. Weak reasoning in the TSMC/ASML argument

1. **"Gets paid no matter who wins" is half true, and the video never admits the other half.**
   TSMC is indifferent to *who* wins but fully exposed to *whether* the AI boom continues (a $52–56B
   capex bet). The current video hints at this in s30b and moves on. **v2 makes it the twist** (s30c:
   "TSMC doesn't need to know who wins. It needs the race to continue"). That makes the thesis more
   honest and more interesting.
2. **It never addresses the obvious objection: Nvidia makes more money.** Nvidia had $215.9B revenue and
   a 71% gross margin, against TSMC's $122.4B and 60%. The video calls Nvidia "the shovel seller", then
   implies TSMC is the better business without saying why. **v2 adds s15b**: Nvidia earns more, TSMC
   earns whoever wins. Conceding the counterpoint is what makes a documentary credible.
3. **The ASML chapter shows the chokepoint but not its consequence.** ASML is the deeper version of the
   thesis: it gets paid whichever foundry wins. One line could say so. ASML's pricing power and export
   controls are stronger material, and they're a candidate for its own video (#2 in the series).
4. **"Who controls" was implicit.** The channel's editorial question has three parts and the video only
   answered two out loud. v2 renames chapter 5 to "Who profits, who loses, who controls" and adds s29b.
5. **The Arizona section undercuts itself slightly.** "Diversifying the map doesn't diversify the dependence"
   is a strong line. But the 2032 projection (47%) shows the map *is* diversifying. v2 states both, and the
   argument holds because the factories are still TSMC's.

## 3. Repetitive or slow sections

From the rendered timeline (current version):

- **Statements are 13 of 39 scenes (~30% of runtime).** That's too much plain text on screen. v2 removes
  two weak ones (s10b and "Definitions vary") and adds two that carry the argument. It's still 13; the
  next pass should turn s07 and s20 into diagrams.
- **The thesis is stated three times in two minutes** (s01, s10b, plus the title). v2 merges s10/s10b.
- **TSMC isn't named until 0:34.** The mystery opening works, but s03's narration is padding. v2 shortens it
  by about 6 s. If retention data later shows an early drop, put the name in the hook.
- **Chapter 1 runs 110 s with four data scenes in a row** (s08 share → s09 bars → s11 big number → s12 bars).
  That's number fatigue. Option: move the platform split (s11–s12) after the Nvidia comparison, where
  "AI is now 58% of TSMC" lands harder. Not applied; it's your call.
- **The end sequence is a 19 s list (s31) right before the conclusion.** Lists at the end are where viewers
  leave. Consider cutting it to two items, or moving "what to watch" after the conclusion line.
- **Two hub diagrams with the same four spokes** (s02 "?" and s16 "TSMC"). This is a deliberate callback
  (question → answer) and I'd keep it, but only if the narration makes the payoff audible ("Remember the
  empty center?").

## 4. Charts that need better screen space

See `proposed/layout-before-after.png` (left = current, right = proposed). The patch is in
`proposed/layout.patch` and is **not applied** to the working code.

- **Bar charts with ≤4 bars** used only the top half of the frame. The proposed version centers them vertically, with bars ~45% thicker and labels and values ~30% larger.
- **Chain diagrams** (s06, s17, s22) were small boxes with 28px subtitles. The proposed boxes are ~35% larger, with 32px subtitles and balanced line breaks.
- Not yet fixed: the **`share` donut** leaves the right third of the frame empty when the label is short (s08). The **`dots`** grid is still small for 10 dots.

## 5. Transitions and sequences that need human eyes

Automation checked text bounds, sizes, timing and loudness. It can't judge these:

1. **All 39 cuts use the same fade.** Watch for monotony, especially s24 → s25 → s25b → s26 (four fades in 25 s).
2. **Reveal timing vs. narration.** Reveals are timed per scene, not per word. Check s02 and s16 (hub spokes should
   appear as each company is named), s09 (bars vs. "Samsung… SMIC…") and s31 (list items vs. "First… Second…").
3. **Counters** (s04, s15, s21, s26) count up over ~2 s. Make sure the number doesn't land after the narrator says it.
4. **All timing will change with the real voice.** Every duration comes from the placeholder voice. Rewatch
   the whole video after narration, not just the changed scenes.
5. **The draft watermark** sits over the bottom-center of every frame. It's intentional and disappears only in the approved final render.

## 6. What I'd do before narration (recommended order)

1. You: decide which v2 changes to accept (table in `README.md`).
2. Verify the caveated claims (`01-caveated-claims.md`). Items 1, 2 and 4 above are must-fix.
3. Apply the layout patch.
4. Approve research → approve script → narrate → full rewatch → final render.
