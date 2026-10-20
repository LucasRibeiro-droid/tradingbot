# Knowledge base

What the bot knows, one TJR Boot Camp lesson at a time
(playlist: https://www.youtube.com/playlist?list=PLKE_22Jx497twaT62Qv9DAiagynP4dAYV).

**The lessons are modules of one course, not separate strategies.** Start here:

- `LEARNING_PROTOCOL.md`: how every lesson is processed (the owner's instructions).
- `methodology.md`: the cumulative knowledge base: the one methodology reconstructed so far, every rule tagged [TJR] / [Inferred] / [Bot], with open questions and contradictions.
- `course_map.md`: all 56 videos, what each teaches, how it connects, what's still missing.
- `glossary.md`: every term learned.
- `decision.md`: the bot's test harness that combines the indicators learned so far.

Each lesson file says what was taught (with video timestamps), which rule or code it
became, and what the bot's own study of it found on real charts. Topics taught over
several lessons also get one combined file (e.g. `liquidity.md` for Days 8, 10 and 12).
`sources/` holds transcripts: written by Gemini (`scripts/gemini_watch.py`) for YouTube links,
or offline by Whisper (`scripts/transcribe_local.py`) for uploaded videos with audio.

| Day | Lesson | Status | Code |
|---|---|---|---|
| 1 | Take Action | not yet studied | — |
| 2 | Candlesticks | learned, first study run | `tradingbot/candles.py`, `tradingbot/study.py` |
| 3 | Discipline | learned | `tradingbot/discipline.py` |
| 4 | Trends | learned, first study and forecast run | `tradingbot/trend.py`, `tradingbot/trend_study.py`, `tradingbot/forecast.py` |
| 5 | Goal Setting | not yet studied | — |
| 6 | Break of Structure | learned, first study run; revised Day 4's swings | `tradingbot/trend.py`, `tradingbot/chart.py` |
| 7 | Individuality | learned (via Gemini), first study run | `tradingbot/session_study.py` |
| 8 | Liquidity Pt 1 | learned; indicator in `liquidity.md` | `tradingbot/liquidity.py` |
| 9 | Check In | not yet studied | — |
| 10 | Liquidity Pt 2 | learned; indicator in `liquidity.md` | `tradingbot/liquidity.py`, `tradingbot/chart.py` |
| 11 | How to take a Loss | not yet studied | — |
| 12 | Liquidity Pt 3 | learned; indicator in `liquidity.md`, used by the decision process | `tradingbot/liquidity.py`, `tradingbot/decision.py` |
| 13 | Risk Management | not yet studied | — |
| 14 | Fair Value Gaps Pt 1 | learned (concept) | — |
| 15 | Identifying problems | not yet studied | — |
| 16 | FVG Pt. 2 | learned; detection built, homework study run; topic file `fair_value_gaps.md` | `tradingbot/fvg.py`, `tradingbot/fvg_study.py` |
| 17 | Patience | not yet studied | — |
| 18 | FVG Pt. 3 | learned; fair value gaps complete; continuation path in the harness | `tradingbot/decision.py` |
| 19–55 | … | not yet studied | — |

## How the bot learns

1. **Rules from lessons** go into code. Rules TJR states as absolutes go in `config.LOCKED`, and the bot never tunes them.
2. **Numbers the bot must choose** (how small a "small body" is, how long a "long wick" is) go in `config.py` as a versioned baseline.
3. **Studies** measure every read against the base rate of the same chart and save the results in `journal/studies/`.
4. **Hypotheses** (`journal/hypotheses.md`) propose changing one variable at a time. A change becomes the new baseline only if it beats the old one on data it was not fitted on.
