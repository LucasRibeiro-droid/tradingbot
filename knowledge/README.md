# Knowledge base

What the bot knows, one TJR Boot Camp lesson at a time
(playlist: https://www.youtube.com/playlist?list=PLKE_22Jx497twaT62Qv9DAiagynP4dAYV).

**The lessons teach indicators, not strategies.** Each one is a way of reading the chart
(candles, trend, break of structure, liquidity, ...). The bot reads all of them through
**one** decision process, described in `decision.md`. The terms are defined in `glossary.md`.

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
| 13–55 | … | not yet studied | — |

## How the bot learns

1. **Rules from lessons** go into code. Rules TJR states as absolutes go in `config.LOCKED`, and the bot never tunes them.
2. **Numbers the bot must choose** (how small a "small body" is, how long a "long wick" is) go in `config.py` as a versioned baseline.
3. **Studies** measure every read against the base rate of the same chart and save the results in `journal/studies/`.
4. **Hypotheses** (`journal/hypotheses.md`) propose changing one variable at a time. A change becomes the new baseline only if it beats the old one on data it was not fitted on.
