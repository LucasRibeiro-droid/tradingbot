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
several lessons also get one combined file (`liquidity.md`, `fair_value_gaps.md`, `order_blocks.md`).
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
| 19 | How to Read News Data | not yet studied | — |
| 20 | Order Blocks | learned (concept); topic file `order_blocks.md` | — |
| 21 | How to Take a Win | not yet studied | — |
| 22 | Order Blocks pt.2 | learned; detection built, homework study run | `tradingbot/orderblocks.py`, `tradingbot/orderblock_study.py` |
| 23 | Check In | not yet studied | — |
| 24 | Order Blocks Pt 3 | learned (via captions + Gemini screen log); **order blocks complete**; order-block continuation path added to the harness | `tradingbot/decision.py` |
| 25 | Over Confidence | not yet studied | — |
| 26 | Equilibrium | learned (concept); topic file `equilibrium.md` | — |
| 27 | Fear | not yet studied | — |
| 28 | Equilibrium pt.2 | learned; **equilibrium complete**; measurement built, tested as a continuation filter | `tradingbot/equilibrium.py`, `tradingbot/decision.py` |
| 29 | Trading Plan | not yet studied | — |
| 30 | Execution | learned (entry models, no charts); topic file `execution.md` | — |
| 31 | Hard Work | not yet studied | — |
| 32 | Execution pt.2 | learned (models 1 and 2 on charts); homework matches `orderblock_study.py` | `tradingbot/orderblock_study.py` |
| 33 | Execution pt.3 | learned; **execution complete**; all four entry models compared on the same setups | `tradingbot/models_study.py` |
| 34 | Daily Bias | learned (part 1); topic file `daily_bias.md`; first test of the bias on the entry models | `tradingbot/models_study.py --bias` |
| 35 | Daily Bias pt. 2 | learned (live, with charts); H31 weakened, H32 tested | `tradingbot/models_study.py --bias` |
| 36–55 | … | not yet studied | — |

## How the bot learns

1. **Rules from lessons** go into code. Rules TJR states as absolutes go in `config.LOCKED`, and the bot never tunes them.
2. **Numbers the bot must choose** (how small a "small body" is, how long a "long wick" is) go in `config.py` as a versioned baseline.
3. **Studies** measure every read against the base rate of the same chart and save the results in `journal/studies/`.
4. **Hypotheses** (`journal/hypotheses.md`) propose changing one variable at a time. A change becomes the new baseline only if it beats the old one on data it was not fitted on.
