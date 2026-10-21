# Execution: putting the pieces together (topic file: Days 30, 32, 33)

**Status: incomplete.** Day 30 (the entry models) and Day 32 (models 1 and 2 on charts) are
learned; Day 33 (models 3 and 4 on charts) hasn't been received.
Lesson notes: `day30_execution_pt1.md`, `day32_execution_pt2.md`.

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
| 3 | Sweep + break → fair value gap filled (even after missing the block) | a reaction, or just the hit | middle (≈ 2) |
| 4 | Sweep + break + gap or block filled + in the discount | as 2 or 3, inside the discount | safest; "foolproof" for beginners |

Choose which models you trade and write them in the execution plan [TJR Day 30, 06:51–07:16].

## How the bot's test harness maps onto them
- Model 1 ≈ the reversal path (`decide`): sweep within 10 candles + break, entry at the break's close.
- Models 2/3 ≈ the continuation path (`Continuation`, `zone="order_block"` / `"fvg"`). The bot waits for a lower-timeframe break inside the zone, as in Days 16–24, rather than entering on the touch.
- Model 4 ≈ the continuation path with `in_discount=True` (H28).
- These paths don't yet require that the sweep and break come first: the continuation path uses the higher timeframe's trend, which a break of structure set, but doesn't check for a sweep before that break. That's a difference to close once Day 32 shows the models on charts.

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

## Open until Day 33
1. Model 3: does a gap entry also go on the touch? (Day 30: "a reaction, or just for it to get hit".)
2. Model 4 on charts.
3. Stops and targets per model (taught later: Days 37, 38).
4. The risk ladder (H29): models 3 and 4 still to test.
