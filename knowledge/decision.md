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
| Fair value gaps | Days 14, 16, 18 | The continuation path: a higher-timeframe gap in the trend's direction, price retraces in, lower-timeframe break of structure | `fair_value_gaps.md` |
| Order blocks | Days 20, 22, 24 | An alternative zone for the continuation path (`Continuation(zone="order_block")`), compared with fair value gaps (H24); not yet the baseline. | `order_blocks.md` |
| Equilibrium | Days 26, 28 | Measured (`equilibrium.py`); an optional condition on the continuation path: the retracement must reach the higher timeframe's discount (H28), not the baseline yet. | `equilibrium.md` |
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

## The continuation path (Days 14–24)

`decision.Continuation`, run alongside the reversal path:
1. A fair value gap on the **higher** timeframe, in that timeframe's trend direction [TJR Day 16].
2. Price retraces into it [TJR]; a gap price pushes past is dropped [TJR Day 18]; "pushed past" = a close beyond the far side [Bot].
3. Trigger: a break of structure on the **lower** timeframe in the trend's direction [TJR Days 14, 16, 18].
4. Only from 9:30 New York on [TJR Day 18: after the market open].
5. Stop beyond the retracement's extreme [TJR Day 18 example]; target the nearest untaken liquidity [TJR Day 12]. One target, no partials, no break-even yet [Bot simplification].
6. The zone can be a fair value gap (baseline) or an order block, TJR's first choice [TJR Day 20, 06:57; Day 24, 11:53]. Same steps otherwise, so the two can be compared (H24).

## How the paths map onto TJR's entry models (Day 30)

Model 1 (sweep + break) ≈ the reversal path; models 2/3 (order block / gap) ≈ the continuation path with `zone="order_block"` / `"fvg"`; model 4 (+ discount) ≈ `in_discount=True`. Differences and open points: `execution.md`.

## How it improves

`python -m tradingbot.decision_study SYMBOL --htf TF --ltf TF` runs the decision process
over history, follows every decision exactly, and repeats it with one indicator added or
removed. The difference is that indicator's contribution (H12 in `journal/hypotheses.md`).
New indicators join the same process as lessons are learned; the bot never runs separate
strategies side by side.
