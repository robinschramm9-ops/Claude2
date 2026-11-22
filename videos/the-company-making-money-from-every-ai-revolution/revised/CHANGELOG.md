# Change log: revised version vs. original working version

The **original working version** (`../storyboard.json`, `../research.json`, `../output/*`) is **unchanged**.
The earlier proposal (`../review/proposed/`) is also unchanged, kept for reference.
The revised version lives entirely in `revised/`. Nothing is approved, narrated or published.

**Original:** 39 scenes, 955 words, 13 static text scenes.  
**Revised:** 42 scenes, 1054 words (~7.0 min), 10 static text scenes, 2 on-screen primary-source quotes.

## Your decisions, as applied

| # | Your instruction | Applied as |
|---|---|---|
| 1 | Taiwan 69%, explained; 47% only as projection | s24 names the measure, year and source; s25 says 'forecast' / 'projection, not a result' |
| 2 | No unverified Google/Amazon claim; the thesis must survive without it | Claim removed everywhere. Replaced by AMD's and Nvidia's own 10-K statements and the Blackwell wafer. See `evidence.md` |
| 3 | Nvidia vs TSMC counterargument, different supply-chain positions, no guarantee | s15b, s15c, s16; 'advantage, not a guarantee'; counter-examples in s29c |
| 4 | Audit every market-share figure | `market-share-audit.md`; full-year relay figures replaced with TrendForce's primary 4Q25 data |
| 5 | Pacing: remove repetition, fewer static scenes, restructure the end list | 13 → 10 statements; thesis repetition removed; list 4 → 3 items |
| 5b | Chart redesign as a separate patch | **Not applied.** Still `review/proposed/layout.patch`, unmerged |
| 6 | Blind voice comparison, no paid service | `blind-test/` (free voices only; see its README for why ElevenLabs and OpenAI are missing) |

## Scene by scene

| Scene | Status | Change |
|---|---|---|
| `s01` | changed | Hook no longer promises a guaranteed outcome: 'positioned to profit, almost no matter who wins'. |
| `s02` | changed | Hub with Google/Amazon spokes (unverified) → Nvidia vs AMD, the two rivals whose own 10-Ks name TSMC. |
| `s03` | changed | Shorter: TSMC is named sooner. |
| `s04` | changed | Same number, now sourced to TSMC's own SEC filing (US$122.42B, +35.9%). |
| `s05` | changed | Chapter 'The toll booth' → 'One factory, many rivals' (no guaranteed-payment metaphor). |
| `s06` | changed | Designers are now 'Nvidia, AMD' only; the 'almost always TSMC' generalization is removed. |
| `s06b` | NEW | NEW: AMD 10-K quote on screen (primary evidence). |
| `s06c` | NEW | NEW: Nvidia 10-K quote naming TSMC *and Samsung*, plus the Blackwell wafer. |
| `s07` | changed | Static statement → two-column contrast explaining the foundry model. |
| `s08` | changed | 69.9% full-year (news relay) → 70.4% for 4Q25 from TrendForce's own release, plus Samsung 7.1%. |
| `s09` | changed | Share bars → revenue bars (like-for-like, same source and quarter). |
| `s10` | changed | Merges old s10 + s10b; hedged ('still likely to land'). |
| `s11` | changed | Sourced to TSMC slide 8; adds +48% growth; drops the unsourced '51% in 2024'. |
| `s12` | changed | Sourced to TSMC slide 8. |
| `s13` | unchanged |  |
| `s14` | unchanged |  |
| `s15` | changed | Unchanged meaning; tighter narration. |
| `s15b` | NEW | NEW: gross-margin comparison with all three caveats on screen (one-off charge, fiscal year, accounting basis). |
| `s15c` | NEW | NEW: explains the two companies' supply-chain positions ('part of what Nvidia spends, TSMC earns'). |
| `s16` | changed | Hub of TSMC customers (Google/Amazon unverified) → the core argument plus 'an advantage, not a guarantee'. |
| `s17` | changed | Processor sub-label no longer asserts 'made by TSMC' for all designers. |
| `s17b` | changed | 'More than 90%' → 'around 90%' (Epoch's CoWoS table sums to 89.6%). |
| `s18` | changed | Now attributed to Epoch AI's bottleneck conclusion, not asserted. |
| `s19` | unchanged |  |
| `s20` | unchanged |  |
| `s21` | changed | No longer implies TSMC uses High-NA machines. |
| `s22` | changed | Designers: 'Nvidia, AMD'; 'manufacturers, led by TSMC'. |
| `s23` | changed | Chapter 'The single point of failure' → 'Concentrated risk' (less absolute). |
| `s24` | changed | 92% → 69%, explicitly 'wafer capacity for advanced logic below 10 nm, 2022, SIA/BCG 2024'. |
| `s25` | changed | 'Definitions vary' filler → the 2032 forecast (47%), labeled a projection twice. |
| `s25b` | changed | 'Huge' → 'large'; follows the forecast. |
| `s26` | unchanged |  |
| `s26b` | changed | Absorbs old s27 (fewer static text scenes). |
| `s28` | changed | Chapter title is now the channel question. |
| `s29` | changed | 'Collect a toll on nearly every chip' → 'positioned to profit'; rivals compete for ~30% (derived from 70.4%). |
| `s29c` | NEW | NEW: counter-example. Samsung's $16.5B Tesla AI6 contract, plus Nvidia's own 10-K naming Samsung. |
| `s29b` | NEW | NEW: answers 'who controls' explicitly. |
| `s30` | changed | Capex now verified from TSMC's own release. |
| `s31` | changed | End list 4 → 3 items, shorter, placed before the closing argument. |
| `s30c` | NEW | NEW: the honest limit of the thesis (TSMC needs the race to continue). |
| `s32b` | changed | Tightened closing line; 'for now'. |
| `s33` | unchanged |  |
| `s10b` | **removed** | Removed: repeated the thesis a third time. |
| `s27` | **removed** | Merged into s26b. |
| `s30b` | **removed** | Removed: CEO 'very nervous' couldn't be verified from the transcript. |
| `s32` | **removed** | Removed: filler before the conclusion. |

## Research changes (`revised/research.json`)

- **+9 sources read directly:** TSMC 4Q25 presentation and release (SEC 6-K), AMD 10-K, Nvidia 10-K, Nvidia blog, TrendForce release, Epoch AI, plus TechCrunch and Bloomberg (Tesla–Samsung). Also SIA/BCG 2024, read in the PDF.
- **Upgraded to primary-verified:** revenue, HPC/platform split, TSMC gross margin, Nvidia gross margin (with its $4.5B charge), 2026 capex.
- **New claims:** `c_amd_tsmc`, `c_nvda_tsmc`, `c_blackwell`, `c_share_q4`, `c_samsung_q4`, `c_rev_q4`, `c_cowos_bottleneck`, `c_tesla_samsung`.
- **Retired (kept in the file, marked disputed/unverified, unusable):** `c_customers`, `c_share`, `c_samsung`, `c_smic`, `c_taiwan` (92%), `c_nervous`, `c_us265`.
- **Still open** (`open_questions`): ASML sole supplier; TSMC $165B/Arizona (TSMC's site blocks automated reading); Samsung's own Tesla filing; a current TSMC source for CoWoS.

## Pipeline change (affects all versions)

- `nsv/validate.py`: 'forecast', 'projection', 'projects', 'projected', 'expects' and 'likely' now count as hedging words. A forecast labeled as one was being wrongly rejected. The original version still validates identically.

## Open editorial decision

- **Title.** 'The Company Making Money From **Every** AI Revolution' over-claims by the standard you set in point 4. Options: *'The AI Company Hiding in Plain Sight'*, *'Who Really Profits From the AI Chip Race?'*, or keep it. Your call; not changed.
- **Repetitive layout.** The two-column contrast is now used 5 times. Accepted for content review only; the visual redesign you've asked for should replace it.
