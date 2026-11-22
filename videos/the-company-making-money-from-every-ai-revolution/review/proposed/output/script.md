# The Company Making Money From Every AI Revolution

*1068 words, approx. 7.1 min at 150 wpm*
**Central question:** If nobody knows which AI company will win, who gets paid regardless?

**Thesis:** TSMC does not need to know who wins the AI race - it manufactures for almost every contender, and beneath it ASML supplies the machines. Nvidia earns more today; TSMC earns more reliably. Its real exposure is not WHO wins, but WHETHER the race continues.

| | |
|---|---|
| What Changes | AI spending is shifting value and bargaining power toward the very few companies that can physically manufacture leading-edge chips: above all TSMC, and beneath it ASML. |
| Why It Matters | Whichever lab or chip designer wins the AI race, its product runs on silicon that is mostly made by one company, largely on one island. That concentration shapes prices, supply, and geopolitical risk for everyone. |
| Who Benefits | TSMC (paid on nearly every advanced AI chip regardless of the designer), ASML (sole commercial supplier of EUV tools), and customers with priority access to scarce capacity. |
| Who Loses | Rival foundries competing for a shrinking remainder of the market; chip designers who must queue for manufacturing and packaging capacity; anyone exposed to a disruption in Taiwan. |
| What Next | Record capital spending is a bet that AI demand holds; packaging is the tightest bottleneck; production is spreading to Arizona but still under TSMC; rivals are trying to close the gap. |

---

### s01 - `statement`
> Every company in the AI race is trying to beat the others. But there is one company that gets paid no matter who wins.
*Visual:* {"text": "One company gets paid no matter who wins.", "accent": ["paid"]}

### s02 - `hub`
> Nvidia. Google. Amazon. AMD. They compete fiercely to build the chips that power artificial intelligence. Yet the most advanced of those chips are manufactured by the same company.
*Visual:* {"center": "?", "spokes": ["Nvidia", "Google", "Amazon", "AMD"], "flow": true}
- **[c_customers]** _single-source_ - TSMC manufactures the leading AI accelerators, including Nvidia's GPUs, Google's TPUs, Amazon's Trainium and AMD's Instinct chips. (AnandTech, Epoch AI)

### s03 - `title`
> Its name isn't printed on the chips, and most people have never heard of it. But the entire AI industry depends on it.
*Visual:* {"kicker": "The Money Behind Technology", "title": "The Company Making Money From Every AI Revolution", "accent": ["Every"]}

### s04 - `big_number`
> It's called TSMC, the Taiwan Semiconductor Manufacturing Company. In 2025, it took in about 122 billion dollars in revenue, up 36 percent in a single year.
*Visual:* {"value": 122.4, "prefix": "$", "suffix": "B", "decimals": 1, "label": "TSMC revenue in 2025", "sub": "Up 36% in a single year", "color": "accent"}
- **[c_rev]** _verified_ - TSMC's 2025 net revenue was about US$122.4 billion, up about 36% year on year (NT$3,809.05 billion). (TSMC, Manufacturing Dive)

### s05 - `chapter`
*Visual:* {"num": 1, "title": "The toll booth"}

### s06 - `chain`
> To understand why, follow a single AI chip. Companies like Nvidia design it. But a design is only a blueprint. Someone has to turn it into billions of transistors on a slice of silicon. For the most advanced AI chips, that someone is almost always TSMC.
*Visual:* {"title": "The life of an AI chip", "nodes": [{"label": "Design", "sub": "Nvidia, Google, AMD"}, {"label": "Manufacture", "sub": "TSMC"}, {"label": "Package", "sub": "Advanced packaging"}, {"label": "Deploy", "sub": "Dat
- **[c_customers]** _single-source_ - TSMC manufactures the leading AI accelerators, including Nvidia's GPUs, Google's TPUs, Amazon's Trainium and AMD's Instinct chips. (AnandTech, Epoch AI)

### s07 - `statement`
> This business model is the source of its power. TSMC is a foundry. It doesn't sell chips under its own name, and it doesn't compete with its customers. It makes chips for everyone else.
*Visual:* {"text": "It doesn't sell chips. It makes them for everyone else.", "accent": ["everyone"]}

### s08 - `share`
> And everyone else is almost everyone. According to the research firm TrendForce, TSMC earned close to 70 percent of all foundry revenue in the world in 2025.
*Visual:* {"value": 70, "title": "Global foundry revenue, 2025", "label": "went to TSMC", "sub": "TrendForce estimate: 69.9%"}
- **[c_share]** _single-source_ - TSMC held 69.9% of global foundry revenue in 2025 (TrendForce), up from 64.4% in 2024. (Focus Taiwan (CNA), reporting TrendForce, Taipei Times / LTN, reporting TrendForce)

### s09 - `bars`
> Its nearest rival, Samsung, had about 7 percent. China's SMIC, about 5. That isn't a lead. It's a different league. Numbers two and three combined don't reach a fifth of TSMC's share.
*Visual:* {"title": "Foundry market share, 2025", "items": [{"label": "TSMC", "value": 69.9, "display": "69.9%"}, {"label": "Samsung", "value": 7.2, "display": "7.2%"}, {"label": "SMIC", "value": 5.3, "display": "5.3%"}], "highlig
- **[c_share]** _single-source_ - TSMC held 69.9% of global foundry revenue in 2025 (TrendForce), up from 64.4% in 2024. (Focus Taiwan (CNA), reporting TrendForce, Taipei Times / LTN, reporting TrendForce)
- **[c_samsung]** _single-source_ - Samsung was second with 7.2% of 2025 foundry revenue (TrendForce). (Focus Taiwan (CNA), reporting TrendForce)
- **[c_smic]** _single-source_ - SMIC was third with about 5.3% of 2025 foundry revenue (TrendForce). (Focus Taiwan (CNA), reporting TrendForce)

### s10 - `statement`
> Nvidia might lose ground to Google's custom chips. Amazon might build its own. A startup might design something better. In almost every one of those scenarios, the order still lands at TSMC.
*Visual:* {"text": "Whoever wins, the chips still have to be made.", "accent": ["made."]}
- **[c_customers]** _single-source_ - TSMC manufactures the leading AI accelerators, including Nvidia's GPUs, Google's TPUs, Amazon's Trainium and AMD's Instinct chips. (AnandTech, Epoch AI)

### s11 - `big_number`
> You can see the shift in TSMC's own numbers. In 2025, high-performance computing, the category that includes AI accelerators, made up 58 percent of its revenue.
*Visual:* {"value": 58, "suffix": "%", "label": "of TSMC revenue: high-performance computing", "sub": "Includes AI accelerators, server and PC processors", "color": "accent"}
- **[c_hpc]** _verified_ - High-performance computing was 58% of TSMC's 2025 revenue, up from 51% in 2024. (TSMC, TSMC)

### s12 - `bars`
> That's up from 51 percent a year earlier. Smartphones, the business that built the modern TSMC, fell to 29 percent. Everything else, from cars to connected devices, adds up to about 13 percent.
*Visual:* {"title": "TSMC revenue by platform, 2025", "items": [{"label": "High-perf. computing", "value": 58, "display": "58%"}, {"label": "Smartphones", "value": 29, "display": "29%"}, {"label": "Everything else", "value": 13, "
- **[c_hpc]** _verified_ - High-performance computing was 58% of TSMC's 2025 revenue, up from 51% in 2024. (TSMC, TSMC)
- **[c_phone]** _verified_ - Smartphone was 29% of TSMC's 2025 revenue, down from 35% in 2024. (TSMC)
- **[c_other]** _verified_ - All other platforms (IoT, automotive, consumer, other) together were about 13% of 2025 revenue. (TSMC)

### s13 - `chapter`
*Visual:* {"num": 2, "title": "Selling shovels"}

### s14 - `statement`
> There's an old saying about gold rushes. The surest way to get rich isn't digging for gold. It's selling the shovels.
*Visual:* {"text": "In a gold rush, sell shovels.", "accent": ["shovels."]}

### s15 - `big_number`
> Nvidia is often called the shovel seller of AI, and it has been spectacularly successful. For its fiscal year 2026, Nvidia reported nearly 216 billion dollars in revenue.
*Visual:* {"value": 215.9, "prefix": "$", "suffix": "B", "decimals": 1, "label": "Nvidia revenue, fiscal 2026", "sub": "Data center alone: $193.7B", "color": "lime"}
- **[c_nvda]** _verified_ - Nvidia reported fiscal 2026 revenue of $215.9 billion (up 65%); data center revenue was $193.7 billion. (NVIDIA)

### s15b - `versus`
> To be fair, Nvidia is the bigger winner right now. It kept about 71 percent of its revenue as gross profit, against about 60 percent at TSMC. But Nvidia has to keep winning to keep those margins. If a rival's chip takes over, TSMC very likely manufactures that one too.
*Visual:* {"title": "Gross margin", "left": {"label": "Nvidia, fiscal 2026", "value": "71%", "note": "Higher margin, but it has to keep winning", "color": "lime"}, "right": {"label": "TSMC, 2025", "value": "60%", "note": "Lower ma
- **[c_nvda_gm]** _verified_ - Nvidia's fiscal 2026 GAAP gross margin was 71.1%. (NVIDIA)
- **[c_gm]** _verified_ - TSMC's 2025 gross margin was 59.9%, up from 56.1% in 2024. (TSMC)
- **[c_customers]** _single-source_ - TSMC manufactures the leading AI accelerators, including Nvidia's GPUs, Google's TPUs, Amazon's Trainium and AMD's Instinct chips. (AnandTech, Epoch AI)

### s16 - `hub`
> But Nvidia designs its chips. It doesn't manufacture them. TSMC does. So it is with Google's custom AI chips, Amazon's Trainium, and AMD's accelerators. The shovel sellers all buy from the same shovel factory.
*Visual:* {"title": "Who manufactures the shovels?", "center": "TSMC", "spokes": ["Nvidia", "Google", "Amazon", "AMD"]}
- **[c_customers]** _single-source_ - TSMC manufactures the leading AI accelerators, including Nvidia's GPUs, Google's TPUs, Amazon's Trainium and AMD's Instinct chips. (AnandTech, Epoch AI)

### s17 - `chain`
> And the dependence goes beyond the silicon itself. Modern AI chips need an advanced packaging step called CoWoS, which places the processor right next to high-speed memory.
*Visual:* {"title": "Advanced packaging", "nodes": [{"label": "Processor", "sub": "Made by TSMC"}, {"label": "+ Memory", "sub": "High-bandwidth"}, {"label": "CoWoS", "sub": "Packaged together"}], "highlight": 2}
- **[c_cowos_def]** _verified_ - CoWoS is TSMC's advanced packaging technology that integrates AI processors with high-bandwidth memory; it is a key capacity constraint for AI chips. (Epoch AI, AnandTech)

### s17b - `dots`
> By one estimate from the research group Epoch AI, just four companies accounted for more than 90 percent of the world's CoWoS packaging capacity in 2025, measured by value.
*Visual:* {"total": 10, "highlight": 9, "label": "90%+ of advanced AI packaging capacity", "sub": "Nvidia, Google, AMD and Amazon, by value, 2025 (Epoch AI estimate)"}
- **[c_cowos]** _estimate_ - Nvidia, Google, AMD and Amazon together consumed over 90% of global CoWoS packaging capacity (by value) in 2025, while using about 12% of advanced logic die production. (Epoch AI)
- **[c_customers]** _single-source_ - TSMC manufactures the leading AI accelerators, including Nvidia's GPUs, Google's TPUs, Amazon's Trainium and AMD's Instinct chips. (AnandTech, Epoch AI)

### s18 - `statement`
> That packaging capacity is one of the tightest bottlenecks in the industry. Which means TSMC doesn't just make the chips. In practice, it helps decide how many of them the world can have.
*Visual:* {"text": "TSMC doesn't just make the chips. It helps decide how many exist.", "accent": ["how", "many"]}
- **[c_cowos_def]** _verified_ - CoWoS is TSMC's advanced packaging technology that integrates AI processors with high-bandwidth memory; it is a key capacity constraint for AI chips. (Epoch AI, AnandTech)

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
> So the real structure of the AI economy looks like this. At the top, the AI products everyone talks about. Below them, the chip designers. Below them, TSMC. And underneath it all, machines from a single Dutch company.
*Visual:* {"title": "The AI stack, from the bottom up", "nodes": [{"label": "ASML", "sub": "Lithography machines"}, {"label": "TSMC", "sub": "Manufacturing"}, {"label": "Designers", "sub": "Nvidia, Google, AMD"}, {"label": "AI pro
- **[c_asml_sole]** _single-source_ - ASML is the only company that sells commercial EUV lithography systems. (CNBC)
- **[c_customers]** _single-source_ - TSMC manufactures the leading AI accelerators, including Nvidia's GPUs, Google's TPUs, Amazon's Trainium and AMD's Instinct chips. (AnandTech, Epoch AI)

### s23 - `chapter`
*Visual:* {"num": 4, "title": "The single point of failure"}

### s24 - `share`
> Now for the part that keeps governments awake at night. According to a 2024 report from the Semiconductor Industry Association and Boston Consulting Group, 69 percent of the world's most advanced chipmaking capacity was in Taiwan in 2022. Nearly all the rest was in South Korea.
*Visual:* {"value": 69, "title": "Leading-edge capacity (below 10nm), 2022", "label": "was located in Taiwan", "sub": "Nearly all the rest: South Korea. SIA & BCG, 2024."}
- **[c_taiwan22]** _single-source_ - In 2022, Taiwan had 69% of global sub-10nm manufacturing capacity and South Korea 31% (SIA/BCG 2024). (Semiconductor Industry Association / BCG, The Register, South China Morning Post)

### s25 - `versus`
> The same report projects Taiwan's share falling to 47 percent by 2032, as new factories open in the United States. Less concentrated. But still the center of gravity.
*Visual:* {"title": "Taiwan's share of leading-edge capacity", "left": {"label": "2022", "value": "69%", "color": "accent"}, "right": {"label": "2032, projected", "value": "47%", "note": "as US capacity grows", "color": "lime"}, "
- **[c_taiwan22]** _single-source_ - In 2022, Taiwan had 69% of global sub-10nm manufacturing capacity and South Korea 31% (SIA/BCG 2024). (Semiconductor Industry Association / BCG, The Register, South China Morning Post)
- **[c_taiwan32]** _single-source_ - SIA/BCG project Taiwan's share of sub-10nm capacity to fall to 47% by 2032, with the US rising to 28%. (Semiconductor Industry Association / BCG, The Register)

### s25b - `statement`
> Even so, a huge part of the AI economy rests on factories on one island, in an active earthquake zone, at the center of one of the world's most sensitive geopolitical disputes.
*Visual:* {"text": "A huge part of the AI economy rests on one island.", "accent": ["one", "island."]}

### s26 - `big_number`
> Which is why the map is starting to change. In March 2025, TSMC said it expects its total investment in the United States to reach 165 billion dollars.
*Visual:* {"value": 165, "prefix": "$", "suffix": "B", "label": "TSMC's planned total US investment", "color": "accent"}
- **[c_us]** _verified_ - In March 2025 TSMC said its total US investment is expected to reach US$165 billion, including three more fabs, two advanced packaging facilities and an R&D center in Arizona. (TSMC)

### s26b - `timeline`
> Its first Arizona factory entered volume production in late 2024. The new plan adds more factories, two advanced packaging plants and a research center.
*Visual:* {"title": "TSMC in Arizona", "events": [{"year": 2024, "label": "First fab in volume production"}, {"year": 2025, "label": "US plan raised to $165B"}, {"year": "Next", "label": "More fabs, packaging plants, R&D center"}]
- **[c_az1]** _verified_ - TSMC's first Arizona fab entered volume production in the fourth quarter of 2024. (TSMC)
- **[c_us]** _verified_ - In March 2025 TSMC said its total US investment is expected to reach US$165 billion, including three more fabs, two advanced packaging facilities and an R&D center in Arizona. (TSMC)

### s27 - `statement`
> But notice who is building those factories. It's still TSMC. Moving production closer to customers reduces one risk. It doesn't change who the industry depends on.
*Visual:* {"text": "Diversifying the map doesn't diversify the dependence.", "accent": ["dependence."]}

### s28 - `chapter`
*Visual:* {"num": 5, "title": "Who profits, who loses, who controls"}

### s29 - `versus`
> So who benefits? TSMC and ASML collect something like a toll on nearly every advanced AI chip, no matter whose design wins. Who loses? Rival manufacturers fighting over what's left of the market, and every chip designer that has to wait in line for capacity.
*Visual:* {"left": {"label": "Benefits", "value": "TSMC + ASML", "note": "Paid on nearly every advanced chip, whoever designs it", "color": "lime"}, "right": {"label": "Under pressure", "value": "Everyone else", "note": "Rival fou
- **[c_share]** _single-source_ - TSMC held 69.9% of global foundry revenue in 2025 (TrendForce), up from 64.4% in 2024. (Focus Taiwan (CNA), reporting TrendForce, Taipei Times / LTN, reporting TrendForce)
- **[c_cowos]** _estimate_ - Nvidia, Google, AMD and Amazon together consumed over 90% of global CoWoS packaging capacity (by value) in 2025, while using about 12% of advanced logic die production. (Epoch AI)

### s29b - `statement`
> And who controls the future of AI? Not only the companies with the smartest models. Also the few that control the bottlenecks underneath them: the machines, the factories, and the packaging lines.
*Visual:* {"text": "Control sits at the bottlenecks.", "accent": ["bottlenecks."], "sub": "Machines. Factories. Packaging lines."}

### s30 - `big_number`
> And TSMC is betting big that this lasts. It plans to spend between 52 and 56 billion dollars on capacity in 2026.
*Visual:* {"value": 56, "display": "$52\u201356B", "label": "TSMC planned capital spending, 2026", "sub": "A record bet that AI demand holds", "color": "lime"}
- **[c_capex26]** _single-source_ - TSMC guided 2026 capital spending of US$52-56 billion. (Tom's Hardware)

### s30b - `statement`
> Its chief executive has reportedly admitted to being very nervous about whether AI demand will hold.
*Visual:* {"text": "Even its CEO is reportedly nervous about whether demand will hold.", "accent": ["nervous"]}
- **[c_nervous]** _single-source_ - TSMC's CEO said he was 'very nervous' about AI bubble concerns while saying demand is real. (Tom's Hardware)

### s30c - `statement`
> That is the real risk in this business. TSMC doesn't need to know who wins the AI race. But it does need the race to keep going.
*Visual:* {"text": "TSMC doesn't need to know who wins. It needs the race to continue.", "accent": ["continue."]}

### s31 - `list`
> So here is what to watch. First, whether AI demand justifies record spending on new factories. Second, whether packaging capacity keeps up. Third, whether factories outside Taiwan can match its output. And fourth, whether any rival can close the gap.
*Visual:* {"title": "What to watch next", "items": ["Does AI demand justify record factory spending?", "Can packaging capacity keep up?", "Can fabs outside Taiwan match its output?", "Can any rival close the gap?"]}

### s32 - `statement`
> The AI race will produce winners and losers among the companies we talk about every day.
*Visual:* {"text": "The AI race will have winners and losers.", "accent": ["winners", "losers."]}

### s32b - `statement`
> But the most dependable money may not go to whoever builds the smartest model. It may go to whoever owns the bottleneck. Right now, that's a company most people have never heard of.
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
