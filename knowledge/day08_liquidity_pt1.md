# Day 8 — Liquidity, Part 1: what it is and why price moves

Source: TJR Boot Camp, Day 8: Liquidity Pt 1 (https://www.youtube.com/watch?v=Lxnu7InGhGE, 11:42).
Transcript by Gemini (`sources/day08_liquidity_pt1.md`); video checked by the bot from an
uploaded copy. TJR says "not much that's going to be put on the chart today, mainly just
going to be me talking", and the video confirms it: one static gold weekly chart
(XAUUSD 1W, FOREXCOM) with no drawings for all 11:41, so the transcript carries the lesson.
Gemini's screen log checked out against the real frame: its open/high/low (1946.59 /
1974.82 / 1932.14) match exactly, and its "16 Oct '23" is the date label TradingView shows
under the mouse cursor hovering in empty space to the right of the last candle.
Code: `tradingbot/liquidity.py`, `took_high`/`took_low` in `tradingbot/trend.py`.

"Probably the largest topic and the most important topic of my strategy." Part 1 is only
the *why*. Where liquidity sits is Part 2 (Day 10); how to trade it is Part 3 (Day 12).

## What the lesson teaches

### 1. Liquidity is resting orders (02:20–03:18)
- Stop orders (taking people out of trades) and limit orders (buy limits, sell limits) waiting at a price.
- When price reaches that point it activates them: people enter and exit, a pool of money changes hands.
- **Bot rule:** `TrendState.took_high` / `took_low` mark a candle that traded past the most recent high or low, by wick or close; it took the orders resting there. (Day 6's `sweep_*` events are the subset that took them without closing past.)

### 2. Why price goes there: the market movers need it (03:41–06:31)
- Every buy needs a seller. Banks and institutions have orders far too large to fill against a few traders.
- To fill them, they push price into liquidity, where many people are exiting or entering the other way. Once filled, they move the market where they want.

### 3. The sequence TJR trades (06:31–09:36)
- Price reaches liquidity → liquidity is taken → **confirmation: a break of structure the other way**, meaning "the orders have been filled" and the trend has changed → trade in the new direction.
- That's what makes trades hit take profit, "not 'oh it bounced off a floor'". TJR rejects support and resistance as guessing (01:19–01:41, 07:41).
- **Bot rule:** `liquidity.sweep_then_shift()` recognizes the sequence: a break of structure up with liquidity below taken in the last `sweep_lookback` (10) candles, or the mirror case. It's not an entry yet; execution comes in Day 12.

### 4. No shift, no trade (08:19–08:59)
- "If we don't see a shift in direction, if we don't see anything, perfect. Hands off." Price reaching liquidity is never by itself a reason to buy or sell.
- **Bot rule (locked):** `LOCKED.liquidity_alone_is_entry = False`.

### 5. Catch tops and bottoms (09:58–10:44)
- You can't enter at the exact moment the banks do; you wait for the confirmation. But the entry still lands near the top or bottom of the move: "pretty much every single one of my trades, it's not already in a trend. It's at the top or the bottom of a trend."

### Homework (11:03)
- Watch the video three or four times until the concept is fully understood. For the bot: this file.

## First study (baseline v0-day08, 2026-10-20)

Question: is a break of structure more reliable when liquidity on the other side was taken just before it?

**It couldn't be answered yet.** About 99% of breaks on every chart already came right after liquidity was taken (for example 399 of 402 on SPY 1-hour), leaving 1–7 breaks per chart to compare against. With Day 6's two-candle rule, nearly every small wiggle is a high or low, so "the most recent low got taken" is almost always true before a break.

What the bot takes from this: its current notion of liquidity, "any most-recent two-candle high or low", is far too broad. TJR doesn't treat every tiny low as a pool of resting orders; Day 10 teaches where liquidity actually sits. Queued as H13.
