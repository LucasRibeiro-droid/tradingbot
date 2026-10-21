# Exits: take profits and stops (topic file: Days 37, 38)

**Status: complete.** Lesson notes: `day37_taking_profits.md`, `day38_stop_losses.md`.
Code: `tradingbot/exits.py` (take-profit ladder, partials); `models_study.py --exits` (test).
Position size (Day 39) is next.

## Take profits [TJR Day 37]
- At building blocks ("price magnets"), on the execution timeframe or one higher.
- **TP1** = the next higher-timeframe draw on liquidity in the trade's direction, minimum 1:1 "most of the time".
- Then the next building blocks: 3–4 take profits in all; partials (Day 36, 20:51); the rest to break even (Day 18 example).
- Not based on 1-minute confluences.

## Stops [TJR Day 38]
- Beyond the liquidity sweep, the invalidation point, whatever the entry.
- Plus room for the spread (0.5 points on the S&P, or the broker's spread).
- Exception, disliked: above a closer order block or gap when the sweep gives a terrible reward-to-risk.
- Never by fixed points or pips.
- De-risk on high-impact news and before bank holidays; don't trade US bank holidays.

## How the bot does it (`exits.py`, [Bot] choices)
- Three take profits:
  1. The first higher-timeframe liquidity pool at least 1R away.
  2. The next two levels beyond it, from liquidity pools on both timeframes and unfilled gap edges.
- Equal thirds; the stop moves to break even after TP1.
- A candle touching a target and the stop counts as the stop.
- No first target at 1R or more → no trade.
- Stop: the sweep's extreme (no spread buffer on bar data).

## Test: TJR's exits vs the bot's single target (H19, 2026-10-21)
Same setups, same entries (the four models of Days 30–33), same stop; only the exit differs. Average R per setup (missed entries = 0):

| Chart | M1 single → TJR | M2 | M3 | M4 |
|---|---|---|---|---|
| SPY 1Day | −0.18 → **−0.11** | −0.14 → **−0.08** | +0.03 → −0.08 | 0.00 → 0.00 |
| SPY 4Hour | −0.22 → **−0.05** | −0.16 → **−0.03** | −0.23 → **−0.07** | −0.08 → **0.00** |
| SPY 1Hour | −0.03 → **+0.18** | −0.05 → **+0.27** | +0.03 → **+0.04** | +0.11 → **+0.35** |
| SPY 15Min | 0.00 → **+0.35** | −0.07 → **+0.24** | −0.13 → −0.24 | −0.12 → **+0.08** |
| GLD 1Day | +0.05 → **+0.06** | −0.12 → **−0.08** | +0.04 → −0.01 | −0.13 → −0.17 |
| GLD 4Hour | +0.19 → 0.00 | +0.07 → +0.02 | +0.24 → **+0.27** | +0.16 → **+0.22** |
| GLD 1Hour | +0.09 → **+0.38** | 0.00 → **+0.20** | +0.19 → **+0.21** | −0.02 → −0.02 |
| GLD 15Min | +0.20 → **+0.32** | +0.10 → **+0.22** | +0.12 → **+0.14** | +0.11 → +0.08 |

- **Better on 23 of 32** (2 tied, 7 worse). Models 1 and 2: 7 of 8 charts each.
- **On the intraday charts** (1-hour and 15-minute), models 1 and 2 with TJR's exits are positive on all four: +0.18 to +0.38R per setup.
- Win rates fall (29–39% for models 1–2) while the first target's median reward-to-risk rises to 2.1–4.1. Fewer, bigger wins, as TJR trades.
- Part of the change: setups with no higher-timeframe target at 1R or more aren't taken (mainly on the daily charts, where the next timeframe up is weekly).
- **H19: supported.** The exit rules come from the lessons and weren't fitted to this data. The [Bot] choices (three targets, thirds, break even) were fixed before the run.
- **Caveat:** one run of 34–66 setups per chart, no costs or slippage.

## Now the default (config `v2-tjr-exits`, 2026-10-21)
`DecisionParams.exits = "tjr"` (3 take profits, first ≥1R at the next timeframe up's draw), `stop = "sweep"`. `models_study.py` uses TJR's exits by default (`--single-exit` for the old one).

**In the harness** (`decision_study.py`, same decisions, only the exit changed), total R:

| Chart pair | Reversal: single → TJR | Continuation: single → TJR |
|---|---|---|
| SPY 1Hour in 1Day | +2.6 → **+8.0** | −4.8 → **−0.1** |
| SPY 15Min in 4Hour | +4.2 → **+5.2** | −6.1 → **−1.3** |
| SPY 5Min in 1Hour | −5.2 → −13.0 | +0.2 → −0.8 |
| GLD 1Hour in 1Day | +0.3 → **+0.4** | +3.2 → **+3.4** |
| GLD 15Min in 4Hour | +4.0 → **+24.6** | +13.4 → **+45.6** |
| GLD 5Min in 1Hour | −1.5 → **+31.2** | −10.0 → **+8.9** |

- Better on 10 of 12; SPY 5-minute is the exception on both paths.
- The stop beyond the sweep gave **identical** trades to the old 10-candle stop: the sweep is always the extreme there.
