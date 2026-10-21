# Execution: putting the pieces together (topic file: Days 30, 32, 33)

**Status: complete** (Day 30: the entry models; Day 32: models 1 and 2 on charts; Day 33:
models 3 and 4 on charts). Daily bias, take profits and stops come next (Days 34–38).
Lesson notes: `day30_execution_pt1.md`, `day32_execution_pt2.md`, `day33_execution_pt3.md`.
Code: `tradingbot/models_study.py` (all four models on the same setups).

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
| 1 | Sweep + break of structure | at the break: "this is an execution point" [Day 32, 05:02] | most risky |
| 2 | Sweep + break, poor reward-to-risk → order block | **on the touch**: "not on the break of structure ... we're executing when it comes into the order block"; stop above the highs [Day 32, 11:19; Day 30, 04:35] | middle |
| 3 | Sweep + break → fair value gap filled (even after missing the block) | **on confirmation**: "what are we waiting for? Some sort of reaction on a lower time frame", a break of structure inside the gap [Day 33, 09:41–10:05] | middle (≈ 2) |
| 4 | Sweep + break + gap or block filled + in the discount | as 2 or 3, inside the discount; best when equilibrium lines up with the gap [Day 33, 14:52–15:18] | safest; "foolproof" for beginners |

Gaps and equilibrium are "last chance entries" [Day 33, 19:14]. Setups against the daily bias are "short-lived" [Day 33, 23:27].

Choose which models you trade and write them in the execution plan [TJR Day 30, 06:51–07:16].

## How the bot's test harness maps onto them
- Model 1 ≈ the reversal path (`decide`): sweep within 10 candles + break, entry at the break's close.
- Model 2 as Day 32 executes it (on the touch, stop beyond the block) = the block trade in `orderblock_study.py` (a sweep is required there).
- The continuation path (`Continuation`, `zone="order_block"` / `"fvg"`) is the Days 16–24 variant: it waits for a lower-timeframe break inside the zone, an optional extra confirmation.
- Model 4 ≈ the continuation path with `in_discount=True` (H28).
- The continuation path doesn't yet require a sweep before the higher timeframe's break; TJR's models all start with one. To close when models 3 and 4 are tested (Day 33).

This is the "base strategy", not the whole of it: daily bias, stops and take profits come later [TJR Day 32, 02:23–04:30].

## Homework and the bot's results (models 1 and 2)
TJR: 10 examples of each, and look at what price does after [Day 32, 08:05, 12:04]. The bot's version (`orderblock_study.py`, run 2026-10-21) has 37–67 setups per chart on SPY and GLD, daily, 1-hour and 15-minute. Both models use the same stop (beyond the block) and the same target (the nearest liquidity).

| Chart | Model 1: avg R / median RR | Model 2: avg R per setup / median RR |
|---|---|---|
| SPY 1Day | −0.18 / 1.02 | −0.14 / 1.43 |
| SPY 1Hour | −0.05 / 1.18 | −0.07 / 1.51 |
| SPY 15Min | +0.03 / 1.25 | −0.04 / 1.57 |
| GLD 1Day | +0.12 / 1.59 | −0.05 / 1.90 |
| GLD 1Hour | +0.10 / 1.14 | 0.00 / 1.57 |
| GLD 15Min | +0.20 / 1.09 | +0.10 / 1.27 |

- Model 2 gives the better reward-to-risk on every chart, as TJR says.
- Its average result is lower on 5 of 6: it wins less often, by more than the better ratio pays for. That's against TJR's ladder (H29), so far.

## All four models on the same setups (Day 33 homework, `models_study.py`, 2026-10-21)
For each sweep + break on SPY and GLD (daily, 4-hour, 1-hour, 15-minute; 34–67 setups per chart), the bot entered each model's way. All four use the same stop (beyond the sweep) and target (the nearest liquidity). Full table: `day33_execution_pt3.md`.
- **Win rate:** model 4 (the "safest") has the lowest on 7 of 8 charts. Its deeper entries give the highest reward-to-risk on 7 of 8 (median 2.07–2.62).
- **Best average R per trade:** model 3 on 3 charts, model 1 on 2, model 4 on 2, model 2 on 1.
- **Model 3 (gap + reaction)** is positive on 6 of 8 charts; **model 2 (block on the touch)** on 2 of 8.
- **H29 (the ladder as win rate): not supported.** No model dominates. Without daily bias and TJR's exits these are base-strategy numbers only.

## Still open
1. Stops and targets per model (Days 37, 38); TJR's partials (H19).
2. Daily bias as a filter on all four models (Days 34–36).
3. The harness's continuation path doesn't require a sweep before the higher-timeframe break; `models_study.py` does.
