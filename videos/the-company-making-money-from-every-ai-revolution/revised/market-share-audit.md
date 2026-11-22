# Market-share audit: every share figure in the revised version

Rule applied: a share figure is used only if we can say **what it measures, for which year, whether it's
actual, estimated or projected, where it comes from, and whether any comparison is like-for-like**.
Phrases like "controls the chip market" are banned. Each figure below is described exactly as its source defines it.

| # | Figure (scene) | Exactly what it measures | Period | Type | Original source (read directly?) | Like-for-like? |
|---|---|---|---|---|---|---|
| 1 | **TSMC 70.4%** (s08, thumbnail "70%") | TSMC's share of **global foundry revenue** (revenue from making chips for other companies) | **4Q 2025** (one quarter) | **Estimate** (analyst) | TrendForce press release, 12 Mar 2026 (**yes**) | Measured against *total* foundry revenue, not just the top 10: TSMC's $33.7B is ~73% of the top-10 sum, so the denominator is larger. A single quarter, so it can swing, e.g. iPhone launches lifted 4Q25. |
| 2 | **Samsung Foundry 7.1%** (s08) | Samsung's **foundry business, excluding System LSI** (its own chip-design unit), as a share of foundry revenue | 4Q 2025 | Estimate | TrendForce (**yes**) | Same source, period and denominator as #1: **like-for-like**. |
| 3 | **Revenue: TSMC $33.7B / Samsung Foundry ~$3.4B / SMIC ~$2.49B** (s09) | Quarterly foundry revenue in US$ | 4Q 2025 | Estimate (TSMC's own reported 4Q25 revenue, $33.73B, matches) | TrendForce (**yes**); TSMC release (**yes**) | Same source and quarter: **like-for-like**. Replaces the old full-year *share* bars (69.9 / 7.2 / 5.3), which came only from news relays. |
| 4 | **"Roughly 30% of foundry revenue TSMC doesn't take"** (s29) | 100% − 70.4% | 4Q 2025 | Derived from an estimate | From #1 | Same basis as #1. Narration says "roughly". |
| 5 | **HPC 58% of TSMC revenue; +48% YoY** (s11, s12) | Share of **TSMC's own** 2025 revenue from its "HPC" platform. HPC includes AI accelerators **and** server/PC processors. | 2025 (calendar) | **Actual** (company-reported) | TSMC 4Q25 presentation, slide 8, filed with the SEC (**yes**) | Internal split of one company's revenue. Never presented as "AI = 58%". |
| 6 | **Smartphone 29%, everything else 13%** (s12) | Same split: smartphone; IoT 5 + automotive 5 + DCE 1 + others 2 | 2025 | Actual | TSMC slide 8 (**yes**) | Same basis as #5. |
| 7 | **~90% of CoWoS capacity** (s17b) | Share of **global CoWoS advanced-packaging capacity** used by Nvidia (60.3), Google (13.5), AMD (8.4) and Amazon (7.4); sum 89.6% | 2025 | **Estimate** (model, with confidence intervals) | Epoch AI (**yes**) | Says "around 90%". The old "more than 90%" mixed this with HBM-by-value and was wrong for CoWoS alone. |
| 8 | **Taiwan 69% / South Korea 31%** (s24) | Share of **global wafer fabrication capacity for logic chips below 10 nm**: fabs ≥5k wafer starts/month, ≥8-inch, R&D fabs excluded | **2022** | Actual capacity, as **estimated by BCG** from US Commerce Dept and SEMI data | SIA/BCG 2024, Exhibit 6, p.14 (**yes**, see caveat) | Capacity (wafer starts), **not** production value or market share. Caveat: the chart's colour legend is lost in text extraction; the country assignment is confirmed by the report's own text and two news reports. |
| 9 | **Taiwan 47% by 2032** (s25) | Same measure as #8 | **2032** | **Forecast**, based on fab projects announced since 2020 | SIA/BCG 2024 (**yes**) | Same basis as #8. The narration calls it "a projection, not a result" and the screen says "forecast". |

## Removed share figures

| Figure | Why it was removed |
|---|---|
| TSMC **69.9%**, Samsung **7.2%**, SMIC **5.3%** (full-year 2025) | Only in news relays (Focus Taiwan, Taipei Times). TrendForce's own release doesn't contain them. Replaced by #1–3. |
| Taiwan **92%** of advanced capacity | Older SIA/BCG baseline. Replaced by #8. |
| "Over 90% of CoWoS **and HBM** by value" | Different measure from CoWoS capacity alone. Replaced by #7. |

## Non-share comparisons checked for like-for-like

| Comparison | Issue | How the script handles it |
|---|---|---|
| Nvidia gross margin **71.1%** vs TSMC **59.9%** (s15b) | Different fiscal years (Nvidia's ends 25 Jan 2026; TSMC's is calendar 2025, so ~11 months overlap) and different accounting (US GAAP vs Taiwan IFRS). Nvidia's includes a one-off $4.5B charge. | All three caveats are on screen. Framed as "different positions, different economics", not as a precise ranking. |
| Nvidia revenue $215.9B vs TSMC $122.4B | Not shown side by side any more. Part of Nvidia's costs *is* TSMC's revenue, so comparing them directly misleads. | s15c explains the supply-chain positions instead. |
