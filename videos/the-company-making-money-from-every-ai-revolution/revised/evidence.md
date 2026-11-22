# Evidence file: does the thesis stand without the uncertain customer claims?

**Revised thesis.** TSMC is *positioned* to profit from the growth of AI chips largely regardless of which
designer wins. It's an advantage, **not a guarantee**.

The thesis no longer uses Google's or Amazon's chips as evidence. Every pillar below comes from a primary
document I read directly, quoted verbatim.

## Pillar 1: The two leading merchant AI-chip rivals both document their reliance on TSMC

> "We rely on Taiwan Semiconductor Manufacturing Company Limited (TSMC) for the production of all wafers for
> microprocessor and GPU products at 7 nanometer (nm) or smaller nodes…"
> **AMD, Form 10-K, fiscal year ended 27 Dec 2025** ([SEC](https://www.sec.gov/Archives/edgar/data/0000002488/000000248826000018/amd-20251227.htm))

> "We utilize a fabless and contracting manufacturing strategy…"
> "We utilize foundries, such as Taiwan Semiconductor Manufacturing Company Limited, or TSMC, and Samsung
> Electronics Co., Ltd., or Samsung, to produce our semiconductor wafers."
> **NVIDIA, Form 10-K, fiscal year ended 25 Jan 2026** ([SEC](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm))

> "…visited TSMC's semiconductor manufacturing facility in Phoenix to celebrate the first NVIDIA Blackwell
> wafer produced on U.S. soil, representing that Blackwell has reached volume production."
> **NVIDIA blog, Oct 2025** ([link](https://blogs.nvidia.com/blog/tsmc-blackwell-manufacturing/))

**What this proves:** if AMD gains share from Nvidia in AI GPUs, or the reverse, the advanced wafers are
very likely made by TSMC either way.
**What it doesn't prove:** that *every* AI chip is made by TSMC. Nvidia names Samsung too.

## Pillar 2: AI-driven computing is now most of TSMC's business, and growing fastest

TSMC 4Q25 presentation, **slide 8 "2025 Revenue by Platform"** (filed with the SEC): HPC **58%**, Smartphone 29%,
IoT 5%, Automotive 5%, DCE 1%, Others 2%. HPC growth **+48%** YoY.
Slide 11 "2025 Financial Highlights": net revenue **US$122.42B (+35.9%)**, gross margin **59.9%** (2024: 56.1%).
([SEC filing](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25presentatione.htm))

Caveat: HPC isn't only AI. It includes server and PC processors.

## Pillar 3: TSMC's position in foundry is far ahead of the next competitor

> "…lifted quarterly revenue 2% QoQ to $33.7 billion, which allowed TSMC to maintain its leading position with a
> 70.4% market share. Samsung Foundry (excluding System LSI)… increased its market share from 6.8% to 7.1%…"
> **TrendForce, 12 Mar 2026** ([link](https://www.trendforce.com/presscenter/news/20260312-12965.html)). An analyst estimate for one quarter.

## Pillar 4: The bottleneck sits in TSMC's part of the chain

> "We find that the four largest AI chip designers — NVIDIA, Google, AMD, and Amazon — collectively consumed over
> 90% of global CoWoS packaging capacity and HBM supply by value in 2025… This asymmetry suggests that scaling AI
> chip production in 2025 was primarily bottlenecked by CoWoS and HBM manufacturing."
> **Epoch AI** ([link](https://epoch.ai/data-insights/ai-chip-supply-chain-constraints)). The CoWoS table alone sums to 89.6%, so the script says "around 90%".

Note: this is Epoch's estimate of who *used* the capacity. It's presented as an attributed estimate, and the
revised script doesn't claim TSMC manufactures Google's or Amazon's chips.

## Pillar 5: TSMC is betting on continued growth

> "The management further expects the 2026 capital budget to be between US$52 billion and US$56 billion."
> **TSMC 4Q25 earnings release**, filed with the SEC ([link](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm))

## Counter-evidence, stated in the video

1. **Nvidia names Samsung as a foundry** alongside TSMC (10-K, above). Scenes s06c and s29c.
2. **Tesla chose Samsung:** a ~$16.5B contract (July 2025) to make Tesla's AI6 chip in Texas. Reported by [TechCrunch](https://techcrunch.com/2025/07/28/tesla-signs-16-5b-deal-with-samsung-to-make-ai-chips) and [Bloomberg](https://www.bloomberg.com/news/articles/2025-07-28/samsung-bags-16-5-billion-deal-in-big-win-for-chipmaking-arm); Samsung's own filing not read. Scene s29c.
3. **Nvidia earns more per dollar:** 71.1% vs 59.9% gross margin. Scene s15b.
4. **TSMC depends on AI demand continuing:** the record capex is a bet. Scenes s30 and s30c.

## Verdict on the stress test

Delete every Google and Amazon reference and the argument still stands. It now rests on the two companies'
own SEC filings, TSMC's SEC filings, and one attributed analyst estimate per supporting point.
**The weakest remaining links:**
- **ASML as the sole EUV supplier** (single secondary source; asml.com isn't reachable from here).
- **TSMC's $165B US plan and Arizona timeline** (TSMC's site blocks automated reading).

Both are listed in `research.json → open_questions` for you to check in a browser.

## Removed because they couldn't be verified
- **"TSMC makes Google's TPUs and Amazon's Trainium":** no primary confirmation.
- **TSMC CEO "very nervous":** the transcript is behind a bot check, and the wording only came from a headline.
