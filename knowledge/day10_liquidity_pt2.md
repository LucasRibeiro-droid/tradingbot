# Day 10 — Liquidity, Part 2: where it sits

Source: TJR Boot Camp, Day 10: Liquidity Pt. 2 (https://www.youtube.com/watch?v=rdz6vnXb8wE, 16:31).
Studied from the uploaded video (with audio). Transcript made offline with Whisper
(`scripts/transcribe_local.py`), in `sources/day10_liquidity_pt2.md`; charts checked from frames.
Code: `tradingbot/liquidity.py` (`find_pools`, `pools_and_takes`, `sweep_then_shift`).
Chart: `tradingbot/chart.py` now draws pools.

**See `liquidity.md` for the combined model (Days 8, 10, 12).**

**This lesson revises Day 8's code.** Day 8 counted every two-candle high or low as
liquidity, so ~99% of breaks of structure "came after liquidity". Day 10 shows that
liquidity rests beyond clear highs and lows that have held for a while.

## What the lesson teaches

### 1. Who is on the other side of the banks (01:54–05:36)
- In an uptrend, retail traders see higher highs and higher lows and expect the trend to continue. When a high is pushed above, two groups have orders resting just above it:
  - **buy stops** from traders buying the breakout
  - **stop losses** from traders shorting inside the range, whose idea is invalidated above the high
- When the high is taken, both are filled: "they literally liquidated all of those people". That is the liquidity banks use to fill large orders and send price the other way, "usually to the downside".
- TJR drew this on a blank gold 4-hour chart (frame at 05:15: a high with a line above it).

### 2. The mirror case below lows (05:36–07:14)
- In a downtrend, **sell stops** (shorting the breakdown) and **stop losses of longs** rest below lows. When a low is taken, the move down fills orders and price turns.
- Using liquidity is how TJR catches "the top of a downtrend or the bottom of an uptrend": getting in "at the beginning of a trend".
- He previews that the move that does the liquidating is essentially an **order block** (Days 20–24).

### 3. On the chart: "sweep, fall" and "sweep, rally" on every timeframe (07:14–13:26)
The levels TJR marks are clear highs and lows that held for a while, not small wiggles:
- **Gold 4-hour** (frame at 07:30): a mid-April high marked with a line; weeks later price pushes above it and collapses.
- **S&P 500 daily** (frame at 08:05): a 2022 high at ~4310 taken months later, then a big sell-off.
- **GBPUSD monthly** (frame at 08:55): the 2020 low at ~1.14 swept in 2022, a "massive liquidity sweep", then a reversal.
- **GBPUSD 1-hour, Asian session** (frame at 10:15): break of structure down, lows taken, rally, break of structure up.
- **Gold 15-minute** (frame at 11:10): a low taken, then a rally.
- **S&P 500 monthly** (frame at 13:12): the June 2022 low (~3636) swept in October 2022, then a break of structure up on the weekly and a rally. At recording time the monthly candle was pushing into the 2022 high (~4310): "we got some liquidity".
- "The market is unable to actually move in the direction that it wants to without taking out liquidity to fill the orders" (11:18).

**Bot rule:** a **pool** is resting liquidity above a high (`buy_side`) or below a low (`sell_side`) that is higher (lower) than `pool_strength` (5) candles on each side and has not been traded through since. `pools_and_takes()` marks the candle that first trades past it (wick or close) as taking it; after that the pool is gone. `sweep_then_shift()` now needs a pool taken in the last `sweep_lookback` (10) candles before a break of structure the other way.

### 4. Not enough on its own (13:45–14:22)
- "It's not just liquidity. You need to know a lot more than just liquidity and break of structure to be able to form an actual bias and take an actual high probability trade." Execution is Day 12.
- Liquidity is introduced first "because it's the hardest one to grasp, but it's the most useful one to understand."

### 5. Homework (11:50–12:32, 14:33)
- On three timeframes, find five liquidity sweeps each, on whatever instrument you trade.
- **Bot version:** `python -m tradingbot.chart SYMBOL --timeframe TF` now draws every pool, from the high or low that forms it to the candle that takes it (dashed while still untaken). First charts on three timeframes are in `journal/charts/`: SPY daily, GLD 1-hour, SPY 15-minute.

## First study (baseline v0-day10, 2026-10-20)

H13 rerun: is a break of structure better after a pool on the other side was taken in the
previous 10 candles? With Day 10's pools about 40% of breaks qualify, so both groups are
large enough to compare (26–122 breaks each).

- **Breaks up:** after liquidity beat without it on 3 of 6 charts. Clearest: SPY 1-hour +6.4% vs −3.5%, SPY daily +7.1% vs −8.4%, GLD 5-minute +11.7% vs −5.4% (edge over each chart's base rate, 5 candles ahead).
- **Breaks down:** after liquidity beat without it on only 2 of 6.

What the bot takes from this: on its own, "liquidity then break" is not yet better than
a break alone over the next 5 candles. That matches TJR's own warning that liquidity and
break of structure aren't enough by themselves. Two things are still missing: the rest
of the strategy (fair value gaps, order blocks, bias), and a fairer test. TJR's trades are
judged by whether they reach their target before their stop, not by where price is 5
candles later, and that needs Day 12's execution rules.
