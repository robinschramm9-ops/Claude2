# Narration: OpenAI TTS vs ElevenLabs

**Nothing has been purchased, and no API key has been used for synthesis.** Both providers are
already implemented in `nsv`. The proposed storyboard has a settings block for each. You pick one,
and nothing else changes.

Target voice: credible, confident male documentary narrator. Natural, intelligent, measured. No YouTube-presenter energy.

## Side by side

| | **OpenAI** (`gpt-4o-mini-tts`) | **ElevenLabs** (`eleven_multilingual_v2`) |
|---|---|---|
| **Voice quality** | Good and clear. Delivery is steered by a written instruction ("calm, authoritative documentary narrator…"), which fits our brief well. Slightly more synthetic on long passages. | Best-in-class naturalness for long-form narration. Better at emphasis on numbers and natural pauses. |
| **Voice choice** | A fixed set of built-in voices (e.g. `onyx`, deep male). **Every OpenAI user has the same voices.** | Large voice library, plus cloning your own voice (Creator plan). Popular library voices are heavily used on YouTube; audition less common ones. |
| **Cost for this video** | Published rate: $0.60 / 1M text tokens + $12 / 1M audio tokens, **about 1.5¢ per minute of audio**. One full pass ≈ **$0.10–0.15**. Ten full re-takes cost under $2. | Subscription. **Starter ~$5–6/mo** (≈30k credits, includes a commercial license). **Creator $22/mo** (≈100k+ credits, voice cloning). ≈1 credit per character, though sources disagree. One full pass ≈ **5,500 credits**. |
| **Cost for 8 videos** | A few dollars in total, pay-as-you-go. | ≈ 45k credits for a single pass of each video; realistically 2–3× that with auditions and re-takes → **Creator plan**, about **$22/mo** for 2–3 months. The free plan does **not** allow commercial use. |
| **Subtitle timing** | No timestamps, so subtitles fall back to proportional timing per scene (small drift). | **Word-accurate subtitles.** Built: the pipeline uses ElevenLabs' character timestamps. |
| **Continuity across scenes** | Each scene is generated independently. | Built: each request includes the neighbouring scenes' text, so intonation flows across cuts. |
| **Setup still needed** | (1) Add `api.openai.com` to the "Claude2" environment's allowed hosts. (2) An OpenAI API key with billing enabled, saved as a network secret. | (1) Host already allowed. (2) **The saved key is rejected by ElevenLabs** (`invalid_api_key`) and must be replaced with a fresh one. (3) Choose a `voice_id` by audition. |
| **Disclosure** | OpenAI's terms require telling listeners the voice is AI-generated. Put "Narration: AI-generated voice" in the description. | No equivalent rule found in this research. Disclose anyway. |
| **Risk to check** | Some of OpenAI's localized model pages mark `gpt-4o-mini-tts` as scheduled for retirement. Confirm the current model name before buying credits. | Plan credit allowances changed in 2026, and sources disagree. Check the live pricing page. |

**YouTube:** its help center requires the "altered or synthetic content" disclosure for realistic
synthetic media, and says disclosure does not affect monetization. Tick it at upload. That's the honest
choice, and it costs nothing.

## Recommendation

**ElevenLabs, Creator plan, for the launch period.** For a channel whose whole bet is "premium and credible",
the voice is about half of the perceived quality, and word-accurate subtitles are already built for it.
OpenAI is the right choice only if you want to keep costs near zero while you test the format.

Cheaper way to decide: run a **blind A/B test** on scenes s01, s15b and s30c (~700 characters). That costs a few
cents on OpenAI plus a Starter month on ElevenLabs. Listen without knowing which is which, then commit.

## The voice brief (used for auditions and for OpenAI's style instruction)

> Calm, authoritative documentary narrator. Measured pace (~150 words per minute), low warm register.
> Confident, never salesy. Clear emphasis on numbers and the key word of each sentence. Short natural
> pauses at full stops. Sounds like an intelligent person explaining something important, not a presenter
> selling something.

Audition criteria, in order: (1) credibility on numbers ("122 billion dollars"); (2) no up-talk or forced
excitement; (3) holds attention over 60 s; (4) not a voice you recognize from other channels.
