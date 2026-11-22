# Caveated claims: what you must check before approving

These claims are **not** fully verified. The QC report lists the 8 used in the current version.
This review adds 2 more that I found during it (marked **NEW**). Nothing here is invented: every source link
comes from the research file. Where a link is to a news relay rather than the original, the check says so.

## `c_share` (single-source), used in s08, s09, s29

**Claim:** TSMC held 69.9% of global foundry revenue in 2025 (TrendForce), up from 64.4% in 2024.

- S4: Focus Taiwan (CNA), reporting TrendForce, [TSMC nets nearly 70% of 2025 foundry market](https://focustaiwan.tw/business/202603130009) (secondary, 2026-03-13)
- S13: Taipei Times / LTN, reporting TrendForce, [TSMC nets nearly 70% of 2025 foundry market](https://news.ltn.com.tw/news/focus/breakingnews/5369655) (secondary, 2026-03-14)

**Caveat on file:** Both outlets relay one analyst firm (TrendForce). Attribute it on screen and in narration.

**What to verify:** Open TrendForce's own press release (not the news relays). Confirm 69.9% and what the denominator is (global foundry revenue vs top-10 total: $122.5B / $169.5B would be 72%, not 69.9%).

## `c_samsung` (single-source), used in s09

**Claim:** Samsung was second with 7.2% of 2025 foundry revenue (TrendForce).

- S4: Focus Taiwan (CNA), reporting TrendForce, [TSMC nets nearly 70% of 2025 foundry market](https://focustaiwan.tw/business/202603130009) (secondary, 2026-03-13)

**Caveat on file:** TrendForce estimate.

**What to verify:** Same TrendForce release: confirm 7.2% and that it covers Samsung's foundry business only.

## `c_smic` (single-source), used in s09

**Claim:** SMIC was third with about 5.3% of 2025 foundry revenue (TrendForce).

- S4: Focus Taiwan (CNA), reporting TrendForce, [TSMC nets nearly 70% of 2025 foundry market](https://focustaiwan.tw/business/202603130009) (secondary, 2026-03-13)

**Caveat on file:** TrendForce estimate.

**What to verify:** Same TrendForce release: confirm about 5.3%.

## `c_asml_sole` (single-source), used in s20, s22

**Claim:** ASML is the only company that sells commercial EUV lithography systems.

- S9: CNBC, [Exclusive look at the making of High-NA, ASML's new $400 million chipmaking colossus](https://www.nbcwashington.com/news/business/money-report/exclusive-look-at-the-making-of-high-na-asmls-new-400-million-chipmaking-colossus/3919541/) (secondary, 2025)

**Caveat on file:** Widely reported; confirm against ASML's annual report before publishing.

**What to verify:** ASML annual report or 20-F: find the statement that ASML is the sole supplier of EUV lithography systems.

## `c_highna` (estimate), used in s21

**Claim:** ASML's High-NA EUV tool costs roughly $380-400 million per machine according to press reports.

- S8: Tom's Hardware (citing Reuters), [ASML's High-NA chipmaking tool will cost $380 million](https://www.tomshardware.com/tech-industry/manufacturing/asmls-high-na-chipmaking-tool-will-cost-dollar380-million-the-company-already-has-orders-for-10-to-20-machines-and-is-ramping-up-production) (secondary, 2024-02)
- S9: CNBC, [Exclusive look at the making of High-NA, ASML's new $400 million chipmaking colossus](https://www.nbcwashington.com/news/business/money-report/exclusive-look-at-the-making-of-high-na-asmls-new-400-million-chipmaking-colossus/3919541/) (secondary, 2025)

**Caveat on file:** No official list price; $380M (Reuters, 2024) vs ~$400M (CNBC, 2025).

**What to verify:** No list price exists. Keep the range and the word 'reportedly'. Optionally find a 2026 report on High-NA pricing.

## `c_cowos` (estimate), used in s17b, s29

**Claim:** Nvidia, Google, AMD and Amazon together consumed over 90% of global CoWoS packaging capacity (by value) in 2025, while using about 12% of advanced logic die production.

- S10: Epoch AI, [AI chip supply chain constraints](https://epoch.ai/data-insights/ai-chip-supply-chain-constraints) (analysis, 2026)

**Caveat on file:** Epoch AI estimate. Must be hedged in narration.

**What to verify:** Read Epoch AI's page. The 90% figure covers CoWoS capacity AND HBM supply, measured by value. The current narration drops 'by value'; the proposed version restores it.

## `c_capex26` (single-source), used in s30

**Claim:** TSMC guided 2026 capital spending of US$52-56 billion.

- S7: Tom's Hardware, [TSMC 'very nervous' about AI bubble concerns despite another record-setting quarter; will invest $52-56 billion in capex](https://www.tomshardware.com/tech-industry/semiconductors/tsmc-very-nervous-about-ai-bubble-concerns-despite-another-record-setting-quarter-but-assured-of-demand-ceo-says-careless-investment-would-be-a-disaster-for-tsmc-for-sure-company-will-invest-usd52-usd56-billion-in-capex) (secondary, 2026-01)

**Caveat on file:** Verify against the 4Q25 transcript (S1) before publishing.

**What to verify:** Read TSMC's 4Q25 earnings call transcript (S1) and confirm the US$52-56B 2026 capital budget guidance in TSMC's own words.

## `c_nervous` (single-source), used in s30b

**Claim:** TSMC's CEO said he was 'very nervous' about AI bubble concerns while saying demand is real.

- S7: Tom's Hardware, [TSMC 'very nervous' about AI bubble concerns despite another record-setting quarter; will invest $52-56 billion in capex](https://www.tomshardware.com/tech-industry/semiconductors/tsmc-very-nervous-about-ai-bubble-concerns-despite-another-record-setting-quarter-but-assured-of-demand-ceo-says-careless-investment-would-be-a-disaster-for-tsmc-for-sure-company-will-invest-usd52-usd56-billion-in-capex) (secondary, 2026-01)

**Caveat on file:** Paraphrase via Tom's Hardware; find the exact transcript wording before quoting directly.

**What to verify:** Find the CEO's exact words in the S1 transcript. If he didn't say 'very nervous' about demand, rewrite the line. The current wording relies on a Tom's Hardware headline.

## NEW: `c_customers` (verified in current version), used in s02, s06, s10, s10b, s16, s17b, s22

**Claim:** TSMC manufactures the leading AI accelerators, including Nvidia's GPUs, Google's TPUs, Amazon's Trainium and AMD's Instinct chips.

- S11: AnandTech, [TSMC: Short Supply of HPC GPUs to Persist for 1.5 Years](https://www.anandtech.com/show/20045)
- S10: Epoch AI, [AI chip supply chain constraints](https://epoch.ai/data-insights/ai-chip-supply-chain-constraints)

**Problem:** Marked *verified* in the current version, but that's overstated. TSMC doesn't disclose customers, and AWS's Dec 2025 Trainium3 launch (S19) confirms 3nm but names no foundry. Check: Nvidia's latest 10-K supplier section; AMD, Google and AWS statements that name TSMC. The proposed version downgrades it to single-source.

## NEW: `c_taiwan` (verified in current version), used in s24

**Claim:** In the SIA/BCG study, 92% of global leading-edge (below 10nm) logic capacity was located in Taiwan (the remaining 8% in South Korea).

- S12: Semiconductor Industry Association / BCG, [Strengthening the Global Semiconductor Supply Chain in an Uncertain Era](https://www.semiconductors.org/strengthening-the-global-semiconductor-supply-chain-in-an-uncertain-era/)

**Problem:** The 92% figure is an older SIA/BCG baseline. SIA/BCG's 2024 report gives **69% for 2022**, projected to fall to **47% by 2032**. The two studies may define 'sub-10nm' differently. Check page 14 of the 2024 PDF (S15). The proposed version replaces 92% with 69% and the projection.

## Also unresolved

- **S2** is a third-party mirror of TSMC's release. Replace it with the official release (S18, pr.tsmc.com) once the full-year tables are checked.
- **c_us265** (TSMC's reported $265B Arizona total) is marked unverified and deliberately left out of both versions.
