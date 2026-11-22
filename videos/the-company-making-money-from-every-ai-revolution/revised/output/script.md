# The Company Making Money From Every AI Revolution

*1054 words, approx. 7.0 min at 150 wpm*
**Central question:** If nobody knows which AI company will win, who gets paid regardless?

**Thesis:** TSMC is positioned to profit from the growth of AI chips largely regardless of which designer wins: the two leading merchant AI-chip designers, Nvidia and AMD, both document their reliance on it; it earns about 70% of foundry revenue; and high-performance computing is now 58% of its revenue. This is an advantage, not a guarantee: Nvidia also uses Samsung, Tesla chose Samsung, and TSMC is exposed to whether AI spending keeps growing.

| | |
|---|---|
| What Changes | AI spending is shifting value and bargaining power toward the very few companies that can physically manufacture leading-edge chips: above all TSMC, and beneath it ASML. |
| Why It Matters | Whichever lab or chip designer wins the AI race, its product runs on silicon that is mostly made by one company, largely on one island. That concentration shapes prices, supply, and geopolitical risk for everyone. |
| Who Benefits | TSMC (paid on nearly every advanced AI chip regardless of the designer), ASML (sole commercial supplier of EUV tools), and customers with priority access to scarce capacity. |
| Who Loses | Rival foundries competing for a shrinking remainder of the market; chip designers who must queue for manufacturing and packaging capacity; anyone exposed to a disruption in Taiwan. |
| What Next | Record capital spending is a bet that AI demand holds; packaging is the tightest bottleneck; production is spreading to Arizona but still under TSMC; rivals are trying to close the gap. |

---

### s01 - `statement`
> Everyone in the AI race is trying to pick the winner. One company is positioned to profit almost no matter which chip designer comes out on top.
*Visual:* {"text": "Positioned to profit, almost no matter who wins.", "accent": ["profit,"]}

### s02 - `versus`
> Nvidia and AMD are fierce rivals in AI chips. Yet their own annual reports name the same manufacturer for their most advanced chips.
*Visual:* {"title": "Rivals in AI chips", "left": {"label": "Nvidia", "value": "Blackwell", "note": "Flagship AI GPU", "color": "lime"}, "right": {"label": "AMD", "value": "Instinct", "note": "AI accelerators", "color": "accent"},
- **[c_nvda_tsmc]** _verified_ - Nvidia is fabless and uses foundries such as TSMC and Samsung to produce its semiconductor wafers. (NVIDIA (Form 10-K, fiscal 2026))
- **[c_amd_tsmc]** _verified_ - AMD relies on TSMC for the production of all wafers for its microprocessor and GPU products at 7 nm or smaller nodes. (AMD (Form 10-K, fiscal 2025))
- **[c_blackwell]** _verified_ - In October 2025, Nvidia and TSMC celebrated the first Nvidia Blackwell wafer produced in the US, at TSMC's Phoenix facility. (NVIDIA (corporate blog))

### s03 - `title`
> Its name isn't printed on the chips, and most people have never heard of it. But the AI industry depends on it.
*Visual:* {"kicker": "The Money Behind Technology", "title": "The Company Making Money From Every AI Revolution", "accent": ["Every"]}

### s04 - `big_number`
> It's called TSMC, the Taiwan Semiconductor Manufacturing Company. In 2025, its revenue reached about 122 billion dollars, up 36 percent in a single year.
*Visual:* {"value": 122.4, "prefix": "$", "suffix": "B", "decimals": 1, "label": "TSMC revenue in 2025", "sub": "Up 35.9% in a single year", "color": "accent"}
- **[c_rev]** _verified_ - TSMC's 2025 net revenue was US$122.42 billion, up 35.9% year on year. (TSMC (Form 6-K, EX-99.2, filed with the SEC), Manufacturing Dive)

### s05 - `chapter`
*Visual:* {"num": 1, "title": "One factory, many rivals"}

### s06 - `chain`
> Follow a single AI chip. Companies like Nvidia and AMD design it. But a design is only a blueprint. Someone has to turn it into billions of transistors on silicon.
*Visual:* {"title": "The life of an AI chip", "nodes": [{"label": "Design", "sub": "Nvidia, AMD"}, {"label": "Manufacture", "sub": "Foundry"}, {"label": "Package", "sub": "Advanced packaging"}, {"label": "Deploy", "sub": "Data cen
- **[c_nvda_tsmc]** _verified_ - Nvidia is fabless and uses foundries such as TSMC and Samsung to produce its semiconductor wafers. (NVIDIA (Form 10-K, fiscal 2026))
- **[c_amd_tsmc]** _verified_ - AMD relies on TSMC for the production of all wafers for its microprocessor and GPU products at 7 nm or smaller nodes. (AMD (Form 10-K, fiscal 2025))

### s06b - `quote`
> AMD's annual report puts it plainly. We rely on TSMC for the production of all wafers for microprocessor and GPU products at 7 nanometer or smaller nodes.
*Visual:* {"text": "We rely on [TSMC] for the production of all wafers for microprocessor and GPU products at 7 nanometer (nm) or smaller nodes.", "who": "AMD", "role": "Annual report (Form 10-K), fiscal 2025"}
- **[c_amd_tsmc]** _verified_ - AMD relies on TSMC for the production of all wafers for its microprocessor and GPU products at 7 nm or smaller nodes. (AMD (Form 10-K, fiscal 2025))

### s06c - `quote`
> Nvidia's annual report names two manufacturers: TSMC and Samsung. And when Nvidia celebrated the first Blackwell wafer produced in the United States, in October 2025, it came out of TSMC's factory in Arizona.
*Visual:* {"text": "We utilize foundries, such as [TSMC] and Samsung, to produce our semiconductor wafers.", "who": "NVIDIA", "role": "Annual report (Form 10-K), fiscal 2026"}
- **[c_nvda_tsmc]** _verified_ - Nvidia is fabless and uses foundries such as TSMC and Samsung to produce its semiconductor wafers. (NVIDIA (Form 10-K, fiscal 2026))
- **[c_blackwell]** _verified_ - In October 2025, Nvidia and TSMC celebrated the first Nvidia Blackwell wafer produced in the US, at TSMC's Phoenix facility. (NVIDIA (corporate blog))

### s07 - `versus`
> That's the foundry model. TSMC doesn't sell AI chips under its own name. It manufactures chips that other companies design, and it competes for their orders, not for their customers.
*Visual:* {"title": "Two different businesses", "left": {"label": "Chip designers", "value": "Design", "note": "Sell chips under their own name", "color": "lime"}, "right": {"label": "Foundry", "value": "Manufacture", "note": "Mak

### s08 - `share`
> By that measure, the gap is enormous. The research firm TrendForce estimates TSMC took 70.4 percent of global foundry revenue in the last quarter of 2025. Samsung's foundry business, in second place, took 7.1 percent.
*Visual:* {"value": 70, "title": "Global foundry revenue, 4Q 2025", "label": "went to TSMC", "sub": "TrendForce estimate: 70.4%. Samsung Foundry: 7.1%."}
- **[c_share_q4]** _estimate_ - TrendForce estimates TSMC held a 70.4% share of global foundry revenue in 4Q25. (TrendForce (own press release))
- **[c_samsung_q4]** _estimate_ - TrendForce estimates Samsung Foundry (excluding System LSI) held 7.1% of foundry revenue in 4Q25, up from 6.8%. (TrendForce (own press release))

### s09 - `bars`
> In dollars, that quarter: about 33.7 billion for TSMC. About 3.4 billion for Samsung's foundry business. About 2.5 billion for China's SMIC.
*Visual:* {"title": "Foundry revenue, 4Q 2025 (TrendForce)", "items": [{"label": "TSMC", "value": 33.7, "display": "$33.7B"}, {"label": "Samsung Foundry", "value": 3.4, "display": "$3.4B"}, {"label": "SMIC", "value": 2.49, "displa
- **[c_rev_q4]** _estimate_ - 4Q25 foundry revenue per TrendForce: TSMC $33.7B; Samsung Foundry nearly $3.4B; SMIC almost $2.49B. (TrendForce (own press release))

### s10 - `statement`
> That matters for the AI race. If AMD takes ground from Nvidia, the orders for those chips are still likely to land at the same factory.
*Visual:* {"text": "Whichever rival gains, the order likely goes to the same factory.", "accent": ["same"]}
- **[c_amd_tsmc]** _verified_ - AMD relies on TSMC for the production of all wafers for its microprocessor and GPU products at 7 nm or smaller nodes. (AMD (Form 10-K, fiscal 2025))
- **[c_nvda_tsmc]** _verified_ - Nvidia is fabless and uses foundries such as TSMC and Samsung to produce its semiconductor wafers. (NVIDIA (Form 10-K, fiscal 2026))

### s11 - `big_number`
> You can see this in TSMC's own numbers. In 2025, high-performance computing, the category that includes AI accelerators, made up 58 percent of its revenue, and grew 48 percent in a year.
*Visual:* {"value": 58, "suffix": "%", "label": "of TSMC revenue: high-performance computing", "sub": "+48% in 2025. Includes AI accelerators, server and PC processors", "color": "accent"}
- **[c_hpc]** _verified_ - High-performance computing (HPC) was 58% of TSMC's 2025 revenue; HPC revenue grew 48% year on year. (TSMC (Form 6-K, EX-99.2, filed with the SEC))

### s12 - `bars`
> Smartphones, the business that built the modern TSMC, were 29 percent. Everything else, from cars to connected devices, about 13 percent.
*Visual:* {"title": "TSMC revenue by platform, 2025", "items": [{"label": "High-perf. computing", "value": 58, "display": "58%"}, {"label": "Smartphones", "value": 29, "display": "29%"}, {"label": "Everything else", "value": 13, "
- **[c_hpc]** _verified_ - High-performance computing (HPC) was 58% of TSMC's 2025 revenue; HPC revenue grew 48% year on year. (TSMC (Form 6-K, EX-99.2, filed with the SEC))
- **[c_phone]** _verified_ - Smartphone was 29% of TSMC's 2025 revenue. (TSMC (Form 6-K, EX-99.2, filed with the SEC))
- **[c_other]** _verified_ - IoT 5%, automotive 5%, DCE 1% and others 2% made up the remaining 13% of 2025 revenue. (TSMC (Form 6-K, EX-99.2, filed with the SEC))

### s13 - `chapter`
*Visual:* {"num": 2, "title": "Selling shovels"}

### s14 - `statement`
> There's an old saying about gold rushes. The surest way to get rich isn't digging for gold. It's selling the shovels.
*Visual:* {"text": "In a gold rush, sell shovels.", "accent": ["shovels."]}

### s15 - `big_number`
> Nvidia is often called the shovel seller of AI, and it has been spectacularly successful: nearly 216 billion dollars in revenue in its fiscal year 2026.
*Visual:* {"value": 215.9, "prefix": "$", "suffix": "B", "decimals": 1, "label": "Nvidia revenue, fiscal 2026", "sub": "Data center alone: $193.7B", "color": "lime"}
- **[c_nvda]** _verified_ - Nvidia reported fiscal 2026 revenue of $215.9 billion (up 65%); data center revenue was $193.7 billion. (NVIDIA, NVIDIA (Form 10-K, fiscal 2026))

### s15b - `versus`
> And Nvidia keeps more of each dollar. Its gross margin was 71 percent, even after a one-off charge of 4.5 billion dollars. TSMC's was 60 percent.
*Visual:* {"title": "Gross margin", "left": {"label": "Nvidia, fiscal 2026", "value": "71.1%", "note": "Includes a $4.5B one-off charge", "color": "lime"}, "right": {"label": "TSMC, 2025", "value": "59.9%", "note": "Calendar year,
- **[c_nvda_gm]** _verified_ - Nvidia's fiscal 2026 gross margin was 71.1% (fiscal 2025: 75.0%), including a $4.5 billion charge for H20 excess inventory and purchase obligations. (NVIDIA (Form 10-K, fiscal 2026))
- **[c_gm]** _verified_ - TSMC's 2025 gross margin was 59.9% (2024: 56.1%). (TSMC (Form 6-K, EX-99.2, filed with the SEC))

### s15c - `chain`
> That's because they sit at different points in the chain. Nvidia designs and sells complete chips and systems. TSMC is paid to manufacture them. Part of what Nvidia spends, TSMC earns.
*Visual:* {"title": "Where each company is paid", "nodes": [{"label": "TSMC", "sub": "Paid to manufacture"}, {"label": "Nvidia", "sub": "Designs, sells chips and systems"}, {"label": "Data centers", "sub": "Buy the systems"}], "hi
- **[c_nvda_tsmc]** _verified_ - Nvidia is fabless and uses foundries such as TSMC and Samsung to produce its semiconductor wafers. (NVIDIA (Form 10-K, fiscal 2026))
- **[c_blackwell]** _verified_ - In October 2025, Nvidia and TSMC celebrated the first Nvidia Blackwell wafer produced in the US, at TSMC's Phoenix facility. (NVIDIA (corporate blog))

### s16 - `statement`
> Nvidia has to keep winning to keep those margins. TSMC benefits as long as demand for advanced chips keeps growing, whoever designs them. That's an advantage. It isn't a guarantee.
*Visual:* {"text": "Nvidia needs to keep winning. TSMC needs the market to keep growing.", "accent": ["winning.", "growing."]}

### s17 - `chain`
> The dependence goes beyond the silicon. Modern AI chips need an advanced packaging step called CoWoS, which places the processor right next to high-speed memory.
*Visual:* {"title": "Advanced packaging", "nodes": [{"label": "Processor", "sub": "Leading-edge logic"}, {"label": "+ Memory", "sub": "High-bandwidth"}, {"label": "CoWoS", "sub": "Packaged together"}], "highlight": 2}
- **[c_cowos_def]** _single-source_ - CoWoS is TSMC's advanced packaging technology that integrates AI processors with high-bandwidth memory; it is a key capacity constraint for AI chips. (Epoch AI, AnandTech)

### s17b - `dots`
> By one estimate from the research group Epoch AI, the four largest AI chip designers used around 90 percent of the world's CoWoS capacity in 2025.
*Visual:* {"total": 10, "highlight": 9, "label": "~90% of global CoWoS capacity", "sub": "used by Nvidia, Google, AMD and Amazon in 2025 (Epoch AI estimate)"}
- **[c_cowos]** _estimate_ - Epoch AI estimates the four largest AI chip designers (Nvidia, Google, AMD, Amazon) used around 90% of global CoWoS packaging capacity in 2025 (Nvidia 60.3%, Google 13.5%, AMD 8.4%, Amazon 7.4%). (Epoch AI)

### s18 - `statement`
> Epoch AI concludes that in 2025, AI chip production was held back mainly by packaging and memory, not by chip design. Whoever controls that capacity has real influence over how many AI chips get made.
*Visual:* {"text": "In 2025, the bottleneck was packaging, not design.", "accent": ["packaging,"], "sub": "Epoch AI: CoWoS and HBM limited AI chip output"}
- **[c_cowos_bottleneck]** _estimate_ - Epoch AI concludes that scaling AI chip production in 2025 was primarily bottlenecked by CoWoS and HBM manufacturing, not logic dies. (Epoch AI)

### s19 - `chapter`
*Visual:* {"num": 3, "title": "The machine behind the machine"}

### s20 - `statement`
> But even TSMC depends on someone. To print the tiniest features on a chip, it uses extreme ultraviolet lithography. And only one company in the world sells those machines: ASML, in the Netherlands.
*Visual:* {"text": "Only one company sells the machines that print the most advanced chips.", "accent": ["one"], "sub": "ASML, Veldhoven, the Netherlands"}
- **[c_asml_sole]** _single-source_ - ASML is the only company that sells commercial EUV lithography systems. (CNBC)

### s21 - `big_number`
> ASML's most advanced model, called High-NA EUV, reportedly costs around 380 to 400 million dollars. For a single machine.
*Visual:* {"value": 380, "prefix": "$", "suffix": "M+", "label": "Reported price of one High-NA EUV machine (ASML)", "sub": "Press reports range from $380M to $400M", "color": "accent"}
- **[c_highna]** _estimate_ - ASML's High-NA EUV tool costs roughly $380-400 million per machine according to press reports. (Tom's Hardware (citing Reuters), CNBC)

### s22 - `chain`
> So the structure looks like this. At the top, the AI products everyone talks about. Below them, the chip designers. Below them, the manufacturers, led by TSMC. And underneath, lithography machines from a single Dutch company.
*Visual:* {"title": "The AI stack, from the bottom up", "nodes": [{"label": "ASML", "sub": "Lithography machines"}, {"label": "TSMC", "sub": "Manufacturing"}, {"label": "Designers", "sub": "Nvidia, AMD"}, {"label": "AI products", 
- **[c_asml_sole]** _single-source_ - ASML is the only company that sells commercial EUV lithography systems. (CNBC)
- **[c_amd_tsmc]** _verified_ - AMD relies on TSMC for the production of all wafers for its microprocessor and GPU products at 7 nm or smaller nodes. (AMD (Form 10-K, fiscal 2025))
- **[c_share_q4]** _estimate_ - TrendForce estimates TSMC held a 70.4% share of global foundry revenue in 4Q25. (TrendForce (own press release))

### s23 - `chapter`
*Visual:* {"num": 4, "title": "Concentrated risk"}

### s24 - `share`
> Now the part that worries governments. A 2024 report by the Semiconductor Industry Association and Boston Consulting Group found that in 2022, 69 percent of the world's wafer capacity for the most advanced logic chips, below 10 nanometers, was in Taiwan. The rest was in South Korea.
*Visual:* {"value": 69, "title": "Advanced logic (<10nm) wafer capacity, 2022", "label": "was located in Taiwan", "sub": "South Korea: 31%. SIA & BCG, 2024 report."}
- **[c_taiwan22]** _verified_ - In 2022, 69% of global wafer fabrication capacity for logic chips below 10 nm was in Taiwan and 31% in South Korea (SIA/BCG, 2024). (Semiconductor Industry Association / BCG, The Register, South China Morning Post)

### s25 - `versus`
> The same report forecasts Taiwan's share falling to 47 percent by 2032, if the factories announced since 2020 are built. That's a projection, not a result.
*Visual:* {"title": "Taiwan's share of advanced logic capacity", "left": {"label": "2022", "value": "69%", "color": "accent"}, "right": {"label": "2032, forecast", "value": "47%", "note": "if announced fabs are built", "color": "l
- **[c_taiwan22]** _verified_ - In 2022, 69% of global wafer fabrication capacity for logic chips below 10 nm was in Taiwan and 31% in South Korea (SIA/BCG, 2024). (Semiconductor Industry Association / BCG, The Register, South China Morning Post)
- **[c_taiwan32]** _estimate_ - SIA/BCG forecast Taiwan's share of <10 nm logic wafer capacity at 47% in 2032 (US ~28%). (Semiconductor Industry Association / BCG, The Register)

### s25b - `statement`
> Even so, a large part of the AI economy rests on factories on one island, in an active earthquake zone, at the center of one of the world's most sensitive geopolitical disputes.
*Visual:* {"text": "A large part of the AI economy rests on one island.", "accent": ["one", "island."]}

### s26 - `big_number`
> Which is why the map is starting to change. In March 2025, TSMC said it expects its total investment in the United States to reach 165 billion dollars.
*Visual:* {"value": 165, "prefix": "$", "suffix": "B", "label": "TSMC's planned total US investment", "color": "accent"}
- **[c_us]** _verified_ - In March 2025 TSMC said its total US investment is expected to reach US$165 billion, including three more fabs, two advanced packaging facilities and an R&D center in Arizona. (TSMC)

### s26b - `timeline`
> Its first Arizona factory entered volume production in late 2024. But notice who is building these factories: TSMC itself. Moving production closer to customers reduces one risk. It doesn't change who the industry depends on.
*Visual:* {"title": "TSMC in Arizona", "events": [{"year": 2024, "label": "First fab in volume production"}, {"year": 2025, "label": "US plan raised to $165B"}, {"year": "Next", "label": "More fabs, packaging plants, R&D center"}]
- **[c_az1]** _verified_ - TSMC's first Arizona fab entered volume production in the fourth quarter of 2024. (TSMC)
- **[c_us]** _verified_ - In March 2025 TSMC said its total US investment is expected to reach US$165 billion, including three more fabs, two advanced packaging facilities and an R&D center in Arizona. (TSMC)

### s28 - `chapter`
*Visual:* {"num": 5, "title": "Who profits, who loses, who controls"}

### s29 - `versus`
> So who profits? TSMC and ASML are positioned to profit from AI chip demand, whichever designer wins. Who's under pressure? Rival foundries, competing for the roughly 30 percent of foundry revenue TSMC doesn't take.
*Visual:* {"left": {"label": "Positioned to profit", "value": "TSMC + ASML", "note": "Whichever chip designer wins", "color": "lime"}, "right": {"label": "Under pressure", "value": "Rival foundries", "note": "Competing for ~30% of
- **[c_share_q4]** _estimate_ - TrendForce estimates TSMC held a 70.4% share of global foundry revenue in 4Q25. (TrendForce (own press release))
- **[c_asml_sole]** _single-source_ - ASML is the only company that sells commercial EUV lithography systems. (CNBC)

### s29c - `big_number`
> But TSMC doesn't win every order. In July 2025, Samsung signed a contract worth about 16.5 billion dollars to make Tesla's next AI chip. And Nvidia's own annual report lists Samsung as a foundry, alongside TSMC.
*Visual:* {"value": 16.5, "prefix": "$", "suffix": "B", "decimals": 1, "label": "Samsung's contract to make Tesla's AI6 chip", "sub": "Signed July 2025, Samsung's Texas fab", "color": "warn"}
- **[c_tesla_samsung]** _single-source_ - In July 2025 Samsung signed a contract worth about $16.5 billion to manufacture Tesla's AI6 chip at its Texas fab. (TechCrunch, Bloomberg)
- **[c_nvda_tsmc]** _verified_ - Nvidia is fabless and uses foundries such as TSMC and Samsung to produce its semiconductor wafers. (NVIDIA (Form 10-K, fiscal 2026))

### s29b - `statement`
> And who controls the future of AI? Not only the companies with the smartest models. Also the few that control the bottlenecks underneath them: the machines, the factories, and the packaging lines.
*Visual:* {"text": "Control sits at the bottlenecks.", "accent": ["bottlenecks."], "sub": "Machines. Factories. Packaging lines."}

### s30 - `big_number`
> And TSMC is betting heavily that demand keeps growing. It expects to spend 52 to 56 billion dollars on capital investment in 2026.
*Visual:* {"value": 56, "display": "$52\u201356B", "label": "TSMC 2026 capital budget (guidance)", "sub": "A record bet that AI demand holds", "color": "lime"}
- **[c_capex26]** _verified_ - TSMC expects its 2026 capital budget to be between US$52 billion and US$56 billion. (TSMC (Form 6-K, EX-99.1, filed with the SEC))

### s31 - `list`
> Three things will decide how this plays out. Whether AI demand justifies that spending. Whether packaging capacity keeps up. And whether rivals like Samsung win more of the most advanced orders.
*Visual:* {"title": "What to watch", "items": ["Does AI demand justify the spending?", "Can packaging capacity keep up?", "Can rivals win advanced orders?"]}

### s30c - `statement`
> That's the real risk in this business. TSMC doesn't need to know who wins the AI race. But it does need the race to keep going.
*Visual:* {"text": "TSMC doesn't need to know who wins. It needs the race to continue.", "accent": ["continue."]}

### s32b - `statement`
> The most dependable money in AI may not go to whoever builds the smartest model. It may go to whoever owns the bottleneck. For now, that's a company most people have never heard of.
*Visual:* {"text": "The most dependable money goes to whoever owns the bottleneck.", "accent": ["bottleneck."]}

### s33 - `end`
> This is THE NEXT SHIFT. Understand tomorrow before it happens.
*Visual:* {"next": "Who controls the future of AI?"}

---

## Sources

- **S1** TSMC: [TSMC 4Q25 Earnings Conference Transcript](https://investor.tsmc.com/japanese/encrypt/files/encrypt_file/reports/2026-01/51d09df96cd89ac19d65af39032b038dc2896a24/TSMC%204Q25%20Transcript.pdf) (primary, accessed 2026-11-22)
- **S2** TSMC: [TSMC 4Q25 earnings release (mirror copy)](https://basic.10jqka.com.cn/ajax/usaph/pubDetail/72c4a5f2626ccedf_pdf) (primary, accessed 2026-11-22)
- **S3** Manufacturing Dive: [TSMC Q4 and full-year 2025 earnings](https://www.manufacturingdive.com/news/tsmc-q4-full-year-2025-earnings-ai-taiwan/809775) (secondary, accessed 2026-11-22)
- **S4** Focus Taiwan (CNA), reporting TrendForce: [TSMC nets nearly 70% of 2025 foundry market](https://focustaiwan.tw/business/202603130009) (secondary, accessed 2026-11-22)
- **S5** NVIDIA: [NVIDIA Announces Financial Results for Fourth Quarter and Fiscal 2026](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/default.aspx) (primary, accessed 2026-11-22)
- **S6** TSMC: [TSMC Intends to Expand Its Investment in the United States to US$165 Billion to Power the Future of AI](https://pr.tsmc.com/english/news/3210) (primary, accessed 2026-11-22)
- **S7** Tom's Hardware: [TSMC 'very nervous' about AI bubble concerns despite another record-setting quarter; will invest $52-56 billion in capex](https://www.tomshardware.com/tech-industry/semiconductors/tsmc-very-nervous-about-ai-bubble-concerns-despite-another-record-setting-quarter-but-assured-of-demand-ceo-says-careless-investment-would-be-a-disaster-for-tsmc-for-sure-company-will-invest-usd52-usd56-billion-in-capex) (secondary, accessed 2026-11-22)
- **S8** Tom's Hardware (citing Reuters): [ASML's High-NA chipmaking tool will cost $380 million](https://www.tomshardware.com/tech-industry/manufacturing/asmls-high-na-chipmaking-tool-will-cost-dollar380-million-the-company-already-has-orders-for-10-to-20-machines-and-is-ramping-up-production) (secondary, accessed 2026-11-22)
- **S9** CNBC: [Exclusive look at the making of High-NA, ASML's new $400 million chipmaking colossus](https://www.nbcwashington.com/news/business/money-report/exclusive-look-at-the-making-of-high-na-asmls-new-400-million-chipmaking-colossus/3919541/) (secondary, accessed 2026-11-22)
- **S10** Epoch AI: [AI chip supply chain constraints](https://epoch.ai/data-insights/ai-chip-supply-chain-constraints) (analysis, accessed 2026-11-22)
- **S11** AnandTech: [TSMC: Short Supply of HPC GPUs to Persist for 1.5 Years](https://www.anandtech.com/show/20045) (secondary, accessed 2026-11-22)
- **S12** Semiconductor Industry Association / BCG: [Strengthening the Global Semiconductor Supply Chain in an Uncertain Era](https://www.semiconductors.org/strengthening-the-global-semiconductor-supply-chain-in-an-uncertain-era/) (primary, accessed 2026-11-22)
- **S13** Taipei Times / LTN, reporting TrendForce: [TSMC nets nearly 70% of 2025 foundry market](https://news.ltn.com.tw/news/focus/breakingnews/5369655) (secondary, accessed 2026-11-22)
- **S14** South China Morning Post: [TSMC pledges extra US$100 billion Arizona fab expansion](https://www.scmp.com/tech/tech-war/article/3360809/tsmc-pledges-extra-us100-billion-arizona-fab-expansion-amid-soaring-ai-chip-demand) (secondary, accessed 2026-11-22)
- **S15** Semiconductor Industry Association / BCG: [Emerging Resilience in the Semiconductor Supply Chain](https://www.semiconductors.org/wp-content/uploads/2024/05/Report_Emerging-Resilience-in-the-Semiconductor-Supply-Chain.pdf) (primary, accessed 2026-11-22)
- **S16** The Register: [US to triple chip manufacturing capacity by 2032, SIA report](https://www.theregister.com/2024/05/08/us_china_sia/) (secondary, accessed 2026-11-22)
- **S17** South China Morning Post: [Tech war: US to dwarf China in advanced chip-making capacity by 2032, report finds](https://www.scmp.com/tech/tech-war/article/3262220/tech-war-us-dwarf-china-advanced-chip-making-capacity-2032-report-finds) (secondary, accessed 2026-11-22)
- **S18** TSMC: [TSMC Reports Fourth Quarter EPS of NT$19.50](https://pr.tsmc.com/english/news/3281) (primary, accessed 2026-11-22)
- **S19** Amazon Web Services: [Announcing Amazon EC2 Trn3 UltraServers](https://aws.amazon.com/about-aws/whats-new/2025/12/amazon-ec2-trn3-ultraservers) (primary, accessed 2026-11-22)
- **P1** TSMC (Form 6-K, EX-99.2, filed with the SEC): [2025 Fourth Quarter Earnings Conference presentation](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25presentatione.htm) (primary, accessed 2026-11-22)
- **P2** TSMC (Form 6-K, EX-99.1, filed with the SEC): [TSMC 4Q25 earnings release with guidance](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000008/a4q25e_withguidancexfinal.htm) (primary, accessed 2026-11-22)
- **P3** AMD (Form 10-K, fiscal 2025): [AMD Annual Report on Form 10-K for the fiscal year ended December 27, 2025](https://www.sec.gov/Archives/edgar/data/0000002488/000000248826000018/amd-20251227.htm) (primary, accessed 2026-11-22)
- **P4** NVIDIA (Form 10-K, fiscal 2026): [NVIDIA Annual Report on Form 10-K for the fiscal year ended January 25, 2026](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm) (primary, accessed 2026-11-22)
- **P5** NVIDIA (corporate blog): [NVIDIA and TSMC Celebrate First NVIDIA Blackwell Wafer Produced in the US](https://blogs.nvidia.com/blog/tsmc-blackwell-manufacturing/) (primary, accessed 2026-11-22)
- **P6** TrendForce (own press release): [AI Demand Drives 4Q25 Global Top 10 Foundries Revenue Up 2.6% QoQ](https://www.trendforce.com/presscenter/news/20260312-12965.html) (analysis, accessed 2026-11-22)
- **P7** Epoch AI: [Advanced packaging and HBM, not logic dies, were the bottlenecks on AI chip production in 2025](https://epoch.ai/data-insights/ai-chip-supply-chain-constraints) (analysis, accessed 2026-11-22)
- **S20** TechCrunch: [Tesla signs $16.5B deal with Samsung to make AI chips](https://techcrunch.com/2025/07/28/tesla-signs-16-5b-deal-with-samsung-to-make-ai-chips) (secondary, accessed 2026-11-22)
- **S21** Bloomberg: [Samsung to Make Tesla AI Chips in Multiyear Texas Deal](https://www.bloomberg.com/news/articles/2025-07-28/samsung-bags-16-5-billion-deal-in-big-win-for-chipmaking-arm) (secondary, accessed 2026-11-22)
