# Liquidity (indicator)

Taught across three lessons that build on each other: Day 8 (why), Day 10 (where),
Day 12 (how to read it). Lesson notes: `day08_liquidity_pt1.md`, `day10_liquidity_pt2.md`,
`day12_liquidity_pt3.md`. Code: `tradingbot/liquidity.py`.

**Liquidity is not a strategy.** It's one indicator the bot reads, alongside candles,
trend and break of structure, to decide when to buy or sell. TJR: "It's a piece that we
can plug in to a strategy" (Day 12, 01:41). How the bot combines it with the other
indicators is in `decision.md`.

## What it measures

**Liquidity** is resting orders: stop losses and limit or stop orders waiting at a price
(Day 8, 02:20). Banks need it to fill their large orders, so price is pushed into it, and
once those orders are filled price can turn (Day 8, 03:52–06:31). Without liquidity being
taken, the market is "chippy choppy" (Day 12, 03:09).

It rests at predictable places (Day 10, 02:49–07:14):
- **Above highs (buy-side liquidity):** buy stops of breakout buyers, and stop losses of traders shorting below the high.
- **Below lows (sell-side liquidity):** sell stops of breakdown sellers, and stop losses of traders buying above the low.

**Prominent** highs and lows hold the most (Day 12, 03:36–05:56): the start of a big trend,
a double top, a high or low that caused a break of structure. It happens on every timeframe.

## How the bot reads it

| Reading | Function | Meaning |
|---|---|---|
| **Pools** | `scan` | Every high (low) higher (lower) than `pool_strength` (5) candles on each side that price hasn't traded through since. On a chart: green lines, dashed while untaken. |
| **Liquidity taken** | `scan` | The candle that first trades past a pool, by wick or close, takes it. The pool is gone after that. |
| **Liquidity swept** (just taken) | `swept_before` | A pool on one side was taken in the last `sweep_lookback` (10) candles. |
| **Draw on liquidity** | `draw` | The nearest untaken pool in a direction: where price is likely headed next. |

## What it tells the decision

- **A sweep is evidence for a reversal the other way.** Banks filled their orders there, so price is likely to turn. It is only evidence. "It doesn't mean when this high gets hit we press sell ... you would lose way more than you win" (Day 12, 06:21). It needs confirmation from another indicator: a break of structure the other way (Day 8, 07:04; Day 12, 06:38). **Locked:** `LOCKED.liquidity_alone_is_entry = False`.
- **No reaction, no trade.** If liquidity is taken and nothing confirms it, do nothing (Day 8, 08:38; Day 12, 07:20).
- **The draw on liquidity sets the target.** "Liquidity [is] a magnet for price" (Day 12, 05:56). After a sweep of highs and a break down, price is drawn to the lows on the other side, where the banks exit (Day 12, 08:20–10:22).
- **Not every high or low gets used.** That's why the other indicators have to agree: "that's why we wait for a confluence" (Day 12, 19:25).

## What the bot measured (2026-10-20)

The decision process (`decision.md`), with and without liquidity as a required
confluence, judged by target before stop. Average R per decision:

| Chart | With liquidity | Without |
|---|---|---|
| SPY 1-hour in daily | +0.07 (n=35) | −0.02 (n=110) |
| GLD 1-hour in daily | +0.01 (n=29) | −0.01 (n=104) |
| SPY daily in weekly | +0.07 (n=13) | −0.18 (n=32) |
| GLD daily in weekly | +0.47 (n=11) | +0.33 (n=49) |
| SPY 5-min in daily | −0.09 (n=46) | −0.07 (n=101) |
| GLD 5-min in daily | −0.19 (n=51) | −0.20 (n=127) |

Adding liquidity improved the decisions on 4 of 6 charts, was about even on 1 and worse
on 1. It cuts the number of decisions by about two-thirds. The samples are small, so it
stays a required confluence for now and gets retested as more indicators arrive.

Settings tested: `pool_strength` 10 and 20 (more prominent pools) made results worse on
7 of 8 charts (H14, rejected; stays 5).
