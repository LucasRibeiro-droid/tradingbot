# Execution: putting the pieces together (topic file: Days 30, 32, 33)

**Status: incomplete.** Day 30 (the entry models, no charts) is learned; Day 32 (examples
of each model) and Day 33 haven't been received.
Lesson notes: `day30_execution_pt1.md`.

## The building blocks and what they say [TJR Day 30, 01:05–02:46]
| Block | Says | Topic file |
|---|---|---|
| Liquidity sweep | orders *may* have been filled (unconfirmed) | `liquidity.md` |
| Break of structure | orders *were* filled; the market structure shifted | `day06_break_of_structure.md` |
| Order block | the range where the orders were filled | `order_blocks.md` |
| Fair value gap | a range with no opposing liquidity | `fair_value_gaps.md` |
| Equilibrium | the discounted price between the high and the low | `equilibrium.md` |

## The four entry models [TJR Day 30, 03:12–06:45]
| # | Model | Entry | Risk (TJR) |
|---|---|---|---|
| 1 | Sweep + break of structure | on the break: "the top of the move" | most risky |
| 2 | Sweep + break, poor reward-to-risk → order block | "enter at the order block, stops above the highs" | middle |
| 3 | Sweep + break → fair value gap filled (even after missing the block) | a reaction, or just the hit | middle (≈ 2) |
| 4 | Sweep + break + gap or block filled + in the discount | as 2 or 3, inside the discount | safest; "foolproof" for beginners |

Choose which models you trade and write them in the execution plan [TJR Day 30, 06:51–07:16].

## How the bot's test harness maps onto them
- Model 1 ≈ the reversal path (`decide`): sweep within 10 candles + break, entry at the break's close.
- Models 2/3 ≈ the continuation path (`Continuation`, `zone="order_block"` / `"fvg"`). The bot waits for a lower-timeframe break inside the zone, as in Days 16–24, rather than entering on the touch.
- Model 4 ≈ the continuation path with `in_discount=True` (H28).
- These paths don't yet require that the sweep and break come first: the continuation path uses the higher timeframe's trend, which a break of structure set, but doesn't check for a sweep before that break. That's a difference to close once Day 32 shows the models on charts.

## Open until Days 32, 33
1. Touch or confirmation at the zone for models 2 and 3.
2. Where model 1 enters (the break's close?).
3. Stops and targets for each model (stops "above the highs" for model 2).
4. Does TJR's risk ladder hold in the data? (H29)
