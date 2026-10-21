# Equilibrium (topic file: Days 26, 28)

**Status: complete** (Day 26: what it is; Day 28: on the chart; there is no part 3).
Lesson notes: `day26_equilibrium_pt1.md`, `day28_equilibrium_pt2.md`.
Code: `tradingbot/equilibrium.py` (measurement, read-only); `decision.Continuation(in_discount=True)` (test).

## What it is [TJR]
- The **50% level** of a swing [Day 26, 06:32; Day 28, 01:27].
  - **Uptrend:** measure low → high. Below 50% is the **discount**, where smart money buys; above it is the premium [Day 28, 01:27–02:24].
  - **Downtrend:** measure high → low. Smart money shorts from the upper half, "when price gets on sale" [Day 28, 02:43–03:07].
- TJR's word "discount" means a good price for the trade, in either direction [Inferred from Day 26, 07:06 and Day 28, 02:06–02:14 with "on sale"].
- **Tool:** a Gann box or Fibonacci showing only 0, 0.5 and 1, drawn wick to wick [TJR Day 28, 03:57–05:12; wicks inferred from frames].

## Which swing [TJR Day 28, with frames]
- "Whenever you see price make a new high in an uptrend, drag it from the low up to the high" [18:23]. A downtrend mirrors it.
- If 50% isn't reached, keep the low and drag the high to each new high [08:20–08:26].
- Once a dip reaches 50% and price makes a new high, measure again from that dip's low [09:01–09:16].
- After a break of structure, start from the extreme the move came from [08:13–08:20 + frame 08:30; Inferred].

## What it's for [TJR]
- The third **retracement tool**, after order blocks and fair value gaps [Day 26, 09:05–10:12].
- **A gauge, not an entry:** inside the discount, find a gap, an order block or a break of structure [Day 26, 08:21–08:48; Day 28, 03:07–03:46].
- Equilibrium + a break of structure alone is "not much confirmation" [Day 28, 07:20].
- **Best combinations:** a fair value gap inside the discount [Day 26, 09:49; Day 28, 11:21]; an order block "combined with the confirmation of it being in equilibrium" [Day 28, 03:30–03:43].
- **Every timeframe**, from monthly (gold) to 5-minute. The higher-timeframe equilibrium sets the area; scale down for the break [Day 28, 07:39, 13:25–13:59, 15:17–16:31].
- It's why traders use the 50% and 61.8% Fibonacci levels [Day 28, 07:46–08:02].

## How the bot measures it (`equilibrium.ranges`)
At each candle: the swing being measured (direction, low, high).
- It starts at a break of structure, from the extreme since the previous break.
- The end is dragged with each new extreme.
- After a retracement reaches 50% and a new extreme forms, it restarts from that retracement's extreme.
- Wick to wick.
- `Range.depth(price)`: how deep a retracement reaches, 0.5 = equilibrium, ≥ 0.5 = the discount side for the trade [Bot].

## Test: does reaching the discount improve the fair value gap continuation? (H28, 2026-10-21)
The same continuation path (higher-timeframe gap, retrace, lower-timeframe break), with one added condition: the retracement must reach the higher timeframe's discount (depth ≥ 0.5).

| Chart | Without: n, win, avg R | In discount: n, win, avg R |
|---|---|---|
| SPY 1Hour in 1Day (730d) | 33, 52%, −0.15 | 24, 50%, **−0.10** |
| SPY 15Min in 4Hour (700d) | 118, 55%, −0.05 | 82, 63%, **+0.07** |
| SPY 5Min in 1Hour (150d) | 63, 60%, +0.00 | 49, 63%, **+0.01** |
| GLD 1Hour in 1Day (730d) | 41, 68%, +0.08 | 32, 75%, **+0.14** |
| GLD 15Min in 4Hour (700d) | 134, 54%, +0.10 | 95, 51%, −0.05 |
| GLD 5Min in 1Hour (150d) | 83, 40%, −0.12 | 56, 39%, −0.20 |

- **Average R:** better on 4 of 6 charts; win rate higher on 4 of 6.
- **Reward-to-risk drops** (median 0.16–0.30 vs 0.22–0.57): a deeper pullback gives a wider stop, while the target (the nearest liquidity) doesn't move.
- **Verdict:** leaning supported, not conclusive. Not promoted.
- It makes the bot's lack of TJR's exits (H19) more costly: he targets far liquidity and takes partials along the way.
