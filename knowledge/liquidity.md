# Liquidity: the bot's model (Days 8, 10 and 12 together)

TJR calls liquidity "probably the largest topic and the most important topic of my strategy"
and splits it into three lessons that only make sense together:

| Lesson | Question | Notes |
|---|---|---|
| Day 8, Part 1 | **Why** does price move? | `day08_liquidity_pt1.md` |
| Day 10, Part 2 | **Where** does liquidity sit? | `day10_liquidity_pt2.md` |
| Day 12, Part 3 | **How** do you trade it? | `day12_liquidity_pt3.md` |

This file is the combined model the bot follows. Code: `tradingbot/liquidity.py`.

## 1. Why: price moves to fill orders (Day 8)

- **Liquidity is resting orders:** stop losses and limit or stop orders waiting at a price (Day 8, 02:20).
- Banks and institutions have orders too large to fill against a few traders. They need many people trading the other way, so they push price to where those orders rest (Day 8, 03:52–06:31).
- Once their orders are filled, price turns. "The market is unable to actually move in the direction that it wants to without taking out liquidity" (Day 10, 11:18).
- Without liquidity being taken, the market is "chippy choppy" and can't change direction (Day 12, 03:09).

## 2. Where: beyond prominent highs and lows (Days 10 and 12)

- **Above a high:** buy stops from breakout buyers, and stop losses from traders shorting below it (Day 10, 02:49–05:21).
- **Below a low:** sell stops from breakdown sellers, and stop losses from traders buying above it (Day 10, 05:36–07:14).
- **Prominent highs and lows matter most** (Day 12, 03:36–05:56): the start of a big trend, a double top, a high or low that caused a break of structure. In TJR's charts they held for weeks or months (S&P 2022 highs and lows, GBPUSD's 2020 low). "Prominent" is relative to the timeframe.
- It happens on every timeframe, from monthly to 1-minute (Day 10, 07:42; Day 12, 16:48).
- **Bot rule:** a *pool* is liquidity above a high (`buy_side`) or below a low (`sell_side`) that is higher (lower) than `pool_strength` (5) candles on each side and hasn't been traded through since. `scan()` reports, for each candle, the pools it took and the pools still waiting. On a chart: `python -m tradingbot.chart SYMBOL --timeframe TF` (green lines, dashed while untaken).

## 3. How: sweep, confirmation, then target the other side (Days 8 and 12)

1. **Price takes a pool** (a sweep). This alone is not a trade: "it doesn't mean when this high gets hit we press sell ... you would lose way more than you win" (Day 12, 06:21–06:38). **Locked:** `LOCKED.liquidity_alone_is_entry = False`.
2. **Confirmation that orders were filled:** a break of structure the other way (Day 6's rule: a candle close past the most recent high or low), plus other confluences. "Price doesn't react, perfect, no trade" (Day 12, 07:20).
3. **Entry:** TJR enters on the pullback after the break, into an imbalance (fair value gap) or an order block (Day 12, 10:54–11:20, 14:30, 15:14; frame at 15:25 shows the shaded imbalance on gold 5-minute). Those are Days 14–24; until then the bot enters at the close of the break candle.
4. **Stop:** beyond the sweep, where the idea is proven wrong. The bot uses the most extreme price of the last `sweep_lookback` (10) candles. Stop placement is taught properly on Day 38.
5. **Target: the liquidity on the other side.** "Liquidity [is] a magnet for price" (Day 12, 05:56). The banks that sold at the high must buy back at the lows, where other traders' orders let them exit (Day 12, 08:20–10:22). The bot targets the nearest untaken pool beyond the entry. No pool there, no trade.

`sweep_then_shift()` recognizes steps 1–2; `plan()` builds steps 3–5; `simulate()` follows the plan exactly, candle by candle: +reward/risk if the target is hit first, −1R if the stop is, and a candle that touches both counts as the stop.

**Not a strategy by itself.** "This is not a strategy, it's a piece that we can plug in to a strategy" (Day 12, 01:41). "Not every single high and low will be used as liquidity to fill orders, and that's why we wait for a confluence" (Day 12, 19:25).

## What the bot found (2026-10-20)

`python -m tradingbot.liquidity_study SYMBOL --htf TF --ltf TF --days N`. Every break of
structure got the same plan, so the only difference between groups is TJR's condition:
was liquidity taken on the other side just before the break?

**Baseline (pool_strength 5), average R per trade:**

| Chart | After liquidity | Without | Median reward/risk (after vs without) |
|---|---|---|---|
| SPY 1-hour in daily | +0.06 (n=161) | +0.04 (n=223) | 1.25 vs 0.82 |
| GLD 1-hour in daily | +0.09 (n=147) | −0.00 (n=219) | 1.45 vs 1.04 |
| SPY daily in weekly | −0.12 (n=59) | −0.04 (n=61) | 1.04 vs 0.74 |
| GLD daily in weekly | +0.08 (n=53) | +0.00 (n=101) | 1.73 vs 0.88 |
| SPY 5-min in daily | −0.09 (n=121) | +0.01 (n=183) | 1.20 vs 0.90 |
| GLD 5-min in daily | +0.04 (n=121) | +0.09 (n=205) | 1.33 vs 1.25 |

- **The model is about break-even as it stands.** After-liquidity beat without on 3 of 6 charts, and every average is within ±0.12R.
- **After-liquidity trades do get better reward to risk** (higher median on all 6 charts), because the sweep sets a clear stop and the other side's liquidity sits further away. They win less often for the same reason.
- **With the higher timeframe**, the after-liquidity trades were positive on the daily and hourly charts (GLD daily +0.47R n=11, SPY daily +0.07R n=13, SPY 1-hour +0.07R n=35) and negative on the 5-minute charts. The samples are too small to trust.
- **H14 rejected:** more prominent pools (strength 10 or 20) made after-liquidity trades worse on 7 of 8 charts. The baseline stays at 5.

What's missing is what TJR says is missing: the entry. Entering at the break's close
instead of on the pullback into a fair value gap or order block gives a worse price and a
wider stop. Days 14–24 will supply that, and the same study will measure the difference.
