# QC report: The Company Making Money From Every AI Revolution

**Result: PASS** | 0 blockers, 9 warnings

- Runtime: 8.1 min (485.4s), 42 scenes, 1054 words
- Claims cited: 24
- duration_s: 485.44
- lufs: -14.0
- true_peak_dbfs: -1.5
- video: h264 1920x1080 30/1

## Issues

- **INFO** `-` check proper nouns: High-perf
- **WARN** `s06c` quote holds for 16s - consider a second beat
- **WARN** `s11` big_number holds for 15s - consider a second beat
- **WARN** `s12` on-screen number 58 is never spoken - viewers may be confused
- **WARN** `s18` statement holds for 16s - consider a second beat
- **WARN** `s20` statement holds for 16s - consider a second beat
- **WARN** `s24` scene runs 21s - split it, it will feel static
- **WARN** `s29c` big_number holds for 18s - consider a second beat
- **WARN** `-` subtitle at 198.8s reads at 22 chars/s (>21)
- **WARN** `-` subtitle at 383.2s reads at 24 chars/s (>21)

## Claims used with caveats (human must be comfortable with these)

- c_asml_sole (single-source): Widely reported; confirm against ASML's annual report before publishing.
- c_cowos (estimate): Read directly. CoWoS shares sum to 89.6%: say 'around 90%', NOT 'more than 90%' (that phrasing refers to CoWoS and HBM by value).
- c_cowos_bottleneck (estimate): Analysis/conclusion, attribute to Epoch AI.
- c_cowos_def (single-source): CoWoS combines logic dies and HBM (Epoch AI, P7). That it is TSMC's technology rests on S11 (TSMC chairman, 2023: 'our CoWoS capacity').
- c_highna (estimate): No official list price; $380M (Reuters, 2024) vs ~$400M (CNBC, 2025).
- c_rev_q4 (estimate): TSMC's own figure for 4Q25 is US$33.73B (P2), which matches.
- c_samsung_q4 (estimate): TrendForce analyst estimate, quarterly. 'Samsung Foundry (excluding System LSI)' is Samsung's foundry business only, not all Samsung chipmaking.
- c_share_q4 (estimate): Analyst estimate, quarterly. Measured against total foundry revenue (TSMC's $33.7B is ~73% of the top-10 sum, so the denominator is larger than the top 10).
- c_taiwan32 (estimate): Forecast based on fab projects announced since 2020. Must be called a forecast/projection.
- c_tesla_samsung (single-source): Both outlets report Samsung's regulatory disclosure plus Musk's confirmation; the filing itself wasn't read.

## Human review checklist (automation cannot judge these)

- [ ] Does the hook make you want to keep watching?
- [ ] Is there a clear argument, not just a list of facts?
- [ ] Would a domain expert find anything misleading?
- [ ] Does the narration sound natural at every scene boundary?
- [ ] Thumbnail + title: honest, and would you click?
