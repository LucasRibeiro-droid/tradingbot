# How the bot decides

The bot has **one** decision process (`tradingbot/decision.py`). The lessons don't each
teach a strategy; they each teach a way of reading the chart, an **indicator**. At every
candle close the bot reads all of its indicators and decides: buy, sell, or do nothing.
Every decision lists the reasons each indicator gave.

## Indicators it reads today

| Indicator | Lessons | What it contributes | Notes |
|---|---|---|---|
| Candles | Day 2 | What a single closed candle says (strong close, rejection, weakness, indecision). Not used in decisions yet. | `day02_candlesticks.md` |
| Trend and higher-timeframe bias | Day 4 | Which direction is allowed at all. | `day04_trends.md` |
| Break of structure | Day 6 | The trigger: a candle closes past the most recent high or low. | `day06_break_of_structure.md` |
| Liquidity | Days 8, 10, 12 | Evidence that orders were just filled on the other side (a sweep), and where price is drawn to next (the target). | `liquidity.md` |
| Fair value gaps | Days 14, 16, 18 | to come: where to enter on the pullback | |
| Order blocks | Days 20, 22, 24 | to come | |
| Equilibrium | Days 26, 28 | to come | |
| Daily bias | Days 34, 35, 36 | to come | |

Rules from the discipline lessons apply on top: follow the plan exactly (Day 3), never
against the higher timeframe (Day 4), closes only (Days 2 and 6), focus on two instruments
(Day 4).

## The decision today

1. **Trigger:** a break of structure (Day 6).
2. **Direction allowed:** only with the higher timeframe's trend (Day 4, locked).
3. **Confluence:** every indicator in `DecisionParams.confluences` must agree. Today that's `liquidity_swept`: liquidity on the other side was taken in the last 10 candles.
4. **Entry:** the trigger candle's close. TJR enters on the pullback into a fair value gap or order block (Day 12, 10:54). That comes when those indicators are learned.
5. **Stop:** beyond the most extreme price of the last 10 candles.
6. **Target:** the draw on liquidity, the nearest untaken pool in the trade's direction. None, no trade.

## How it improves

`python -m tradingbot.decision_study SYMBOL --htf TF --ltf TF` runs the decision process
over history, follows every decision exactly, and repeats it with one indicator added or
removed. The difference is that indicator's contribution (H12 in `journal/hypotheses.md`).
New indicators join the same process as lessons are learned; the bot never runs separate
strategies side by side.
