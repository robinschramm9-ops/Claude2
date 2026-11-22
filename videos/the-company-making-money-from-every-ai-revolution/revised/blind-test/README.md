# Blind voice test

**How to listen:** play `Sample_A.mp3` to `Sample_E.mp3`, ideally on headphones and then on a phone speaker.
Each sample reads the same three revised scenes: the **hook** (s01), the **numbers scene** (s15b, gross margins)
and the **closing line** (s32b). All five are normalized to the same loudness (−16 LUFS), so volume can't
bias you. Rank them **before** opening `zz_KEY_open_after_listening.md`.

Judge on: (1) credibility on numbers; (2) measured, not salesy; (3) would you listen for 7 minutes?; (4) does it
sound like a voice from other channels?

## What's in the test, and what isn't

| Option | In this test? | Why |
|---|---|---|
| Free, open-source voices (Apache-2.0, run locally at no cost) | **Yes**, several voices | No account, payment or key needed |
| The current placeholder voice | **Yes**, as a reference | So you can hear the baseline |
| **ElevenLabs** | **No** | The saved API key is rejected (`invalid_api_key`). ElevenLabs' **free** plan would be enough for this test (~2,000 characters of its 10,000 monthly), with no subscription needed, but it requires a valid key. |
| **OpenAI** | **No** | No free tier: any use is billed. You asked for no paid usage yet. |

To add ElevenLabs to the same blind set: create a **free** ElevenLabs account and API key, and save it in the
"Claude2" environment's network secrets for `api.elevenlabs.io`. I'll then audition 3–4 male narrators on the same
three scenes, at the same loudness, under new letters. No subscription is needed for that.

## Commercial-use terms (read from the providers' own pages, 22 Nov 2026)

**ElevenLabs**, Terms of Service ([elevenlabs.io/terms-of-use](https://elevenlabs.io/terms-of-use)):
> "if you access or use our Services free of charge (such a user, a "Free User"), you may only use the Services
> for non-commercial purposes; (ii) if you access or use our Services through a paid subscription plan (such a
> user, a "Paid User"), you may use the Services for commercial purposes…"

So the **free plan is fine for this test but not for a monetized channel**. The pricing page lists the commercial
license from **Starter** upwards.

**OpenAI**, Service Terms ([openai.com/policies/service-terms](https://openai.com/policies/service-terms/)), "Prompt-to-Voice" section:
> "Customer must clearly disclose that generated speech is AI-generated, must not intentionally remove or alter
> OpenAI-provided indicators of AI origin…"

(This clause is in the Prompt-to-Voice section. Assume the same disclosure for standard voices; that's the safe reading.)

**Kokoro (free, open-source)**: weights licensed **Apache-2.0** ([LICENSE](https://raw.githubusercontent.com/hexgrad/kokoro/main/LICENSE));
the README says *"With Apache-licensed weights, Kokoro can be deployed anywhere from production environments to
personal projects."* Commercial use is permitted. The runtime library (`kokoro-onnx`) is MIT.

**YouTube**: tick the "altered or synthetic content" disclosure at upload whichever provider you choose.
YouTube says disclosure doesn't affect monetization ([help page](https://support.google.com/youtube/answer/14328491)).

## Total expected cost (8 videos)

Assumptions: ~6,000 characters per video per full take; ~3 takes per video including auditions and fixes →
~18,000 characters per video, **~145,000 characters for 8 videos**.

| Option | Price (from the provider's page) | Expected total for 8 videos |
|---|---|---|
| ElevenLabs **Creator** | $22/mo, 121,000 credits/mo; 1 credit = 1 character on Multilingual v2; **$11 first month** | ~2 months → **$33** ($11 + $22). Black Friday annual offer: $99 for the first year, ends 1 Dec. |
| ElevenLabs **Starter** | $6/mo, 30,000 credits; commercial license included | Too small: ~1.5 videos/month. ~5 months → **~$30**, but it slows production |
| **OpenAI** gpt-4o-mini-tts | ≈ $0.015 per minute of audio *(from OpenAI's developer docs via search; the pricing page didn't render for me)* | ~7 min × 3 takes × 8 ≈ 170 min → **≈ $2.50–$5** |
| **Kokoro** (free) | $0 | **$0**, but not yet wired into `nsv` (about an hour of work) and no word-level timestamps |

Nothing has been purchased, and no paid API has been called.
