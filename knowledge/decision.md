# How the bot decides (test harness)

The methodology itself is reconstructed in `methodology.md`. This file describes the bot's
**test harness** (`tradingbot/decision.py`): one decision process that reads the indicators
learned so far, so their contribution can be measured. It is not TJR's strategy and is not
for live trading; several steps are [Bot] placeholders until the lessons that teach them.
At every candle close it reads its indicators and decides buy, sell or nothing, listing
the reasons each indicator gave.

## Indicators it reads today

| Indicator | Lessons | What it contributes | Notes |
|---|---|---|---|
| Candles | Day 2 | What a single closed candle says (strong close, rejection, weakness, indecision). Not used in decisions yet. | `day02_candlesticks.md` |
| Trend and higher-timeframe bias | Day 4 | Which direction is allowed at all. | `day04_trends.md` |
| Break of structure | Day 6 | The trigger: a candle closes past the most recent high or low. | `day06_break_of_structure.md` |
| Liquidity | Days 8, 10, 12 | Evidence that orders were just filled on the other side (a sweep), and where price is drawn to next (the target). | `liquidity.md` |
| Fair value gaps | Days 14, 16, 18 | where retracements go; entry area with a reaction or lower-timeframe break. Detection ready (`fvg.py`); not in the harness until Day 18 teaches how to trade them | `fair_value_gaps.md` |
| Order blocks | Days 20, 22, 24 | to come | |
| Equilibrium | Days 26, 28 | to come | |
| Daily bias | Days 34, 35, 36 | to come | |

Rules from the discipline lessons apply on top: follow the plan exactly (Day 3), never
against the higher timeframe (Day 4), closes only (Days 2 and 6), focus on two instruments
(Day 4).

## The harness today

1. **Trigger:** a break of structure [TJR Day 6].
2. **Direction allowed:** only with the higher timeframe's trend [TJR Day 4, locked].
3. **Confluence:** every indicator in `DecisionParams.confluences` must agree. Today that's `liquidity_swept`: liquidity on the other side was taken shortly before [TJR Days 8, 12]; "shortly" = within 10 candles [Bot].
4. **Entry:** the trigger candle's close [Bot]. TJR enters on the retracement into a fair value gap or order block, triggered by a break of structure on a **lower** timeframe [TJR Day 12, 10:54; Day 14, 04:28]. The harness is single-timeframe for the trigger until those lessons are learned.
5. **Stop:** beyond the most extreme price of the last 10 candles [Bot]; stops are taught on Day 38.
6. **Target:** the draw on liquidity, the nearest untaken pool in the trade's direction [TJR Day 12]. None, no trade.

## How it improves

`python -m tradingbot.decision_study SYMBOL --htf TF --ltf TF` runs the decision process
over history, follows every decision exactly, and repeats it with one indicator added or
removed. The difference is that indicator's contribution (H12 in `journal/hypotheses.md`).
New indicators join the same process as lessons are learned; the bot never runs separate
strategies side by side.
