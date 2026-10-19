# Day 4 — Trends

Source: TJR Boot Camp, Day 4: Trends (https://www.youtube.com/watch?v=viuGHEuv0nw, 28:44).
Studied from the full video plus the captions.
Code: `tradingbot/trend.py`. Thresholds: `TrendParams` in `tradingbot/config.py`.
Homework: `tradingbot/forecast.py`. Study: `tradingbot/trend_study.py`.

## What the lesson teaches

### 1. Why the trend matters: momentum (01:01–01:36)
- Markets move on momentum. Once price trends, odds are it continues, like a ball pushed on a flat surface.
- The trend tells you which direction to place trades in.

### 2. Reading a trend (02:13–03:32, drawn on screen)
- **Uptrend:** higher highs and higher lows. Each push goes past the last high, and each pullback holds above the last low.
- **Downtrend:** lower highs and lower lows.
- It continues until it breaks. On gold's weekly chart (frame at 04:50, swings circled), TJR walks through high, higher high and higher low pairs until a close below the last higher low makes a lower low; then "it's probably going to flip its direction".
- **Bot rule:** `swings()` finds turning points that are higher (lower) than `swing_strength` candles on each side. A swing only counts once the candles that confirm it have closed. `trend_series()` starts a trend from two higher highs and higher lows (or lower highs and lower lows). It flips only when a candle **closes** beyond the last swing on the other side; that close is the structure break. Day 6 covers break of structure in depth.

### 3. Pullbacks vary, the push past the high doesn't (06:37–07:10)
- Retracements can be small or deep, and you can't know which. What repeats is the extension past the last high.
- So don't trade retracements; ride the momentum.

### 4. Higher timeframes hold higher power (07:41–10:53)
- Over one weekly uptrend there can be thousands of 15-minute trend changes. Getting caught up in those is where people go wrong.
- If the 4-hour, daily or weekly says down and the 15-minute says up, **wait for the 15-minute to turn down**, then trade down. The lower timeframe is only for an optimized entry.
- TJR's own biggest struggle and his losing weeks came from trading small timeframes against the higher-timeframe bias (09:15, 21:49).
- TJR's style: a liquidity sweep on the 30-minute plus a break of structure on the 5-minute, while the 4-hour and daily say the same direction (10:22).
- For intraday trading, at minimum know where price wants to go **for the day** (17:23).
- **Bot rule (locked):** `LOCKED.trade_against_htf_trend = False`. `bias(htf, ltf)` returns the higher timeframe's direction and is `ready` only once the lower timeframe trends the same way. `state_at()` only uses higher-timeframe candles that had already closed.

### 5. Consolidation: the third way markets move (12:32–13:51)
- Price moves up, down, or sideways. Gold's 5-minute chart (frame at 12:50, boxed) made a higher high and a higher low, but stayed "static, stagnant" until it broke the floor, shifted structure and started making lower highs and lower lows.
- A small higher high and higher low inside a range isn't a trend.
- **Bot rule:** a candle is `consolidating` when price over the last `consolidation_lookback` candles went less than `consolidation_max_efficiency` (30%) of its high-to-low range. While consolidating, `tradeable_direction` is none and the bot makes no call.

### 6. Simplify with a line chart (18:00–20:34, 28:04)
- Gold weekly, 15-minute and 30-minute shown as a line of closes (frames at 18:25, 19:40, 20:55). Without candle colors, direction is easy to see: in a downtrend the moves up are always smaller than the moves down.
- **Bot setting:** `swing_source = "close"` finds swings from closes only, like a line chart. The default is `"wick"`; which one works better is a hypothesis to test (H6).

### 7. Focus on one or two instruments (27:04)
- "What makes you think you can understand multiple asset classes if you're already losing on 10 of them?"
- **Bot rule (locked):** `LOCKED.max_instruments = 2`. Watchlist: SPY (for TJR's S&P 500) and GLD (for gold).

### 8. Homework: predict the week, the next days, today (23:39–27:04)
- Write down where price wants to go this week, then the next couple of days, then today. Direction only; no stop loss, no position. It's fine if price goes against you briefly first.
- **Bot version:** `python -m tradingbot.forecast make` writes the calls for the watchlist to `journal/forecasts/DATE.json`: the week from the weekly trend, the next days and today from the daily trend, each noting whether the lower timeframe agrees yet. `python -m tradingbot.forecast grade` grades each call once its horizon has passed.
- **First forecast, 2026-10-19:** SPY: no call; the weekly chart is consolidating. GLD (at 379.94): down for the week, the next days and today, with the lower timeframe agreeing.

## First study results (baseline v0-day04, 2026-10-19)

`python -m tradingbot.trend_study SYMBOL --htf TF --ltf TF --days N`. Horizon: 5 candles.
"Edge" is hit rate minus the base rate on the same chart.

Charts: SPY and GLD 1-hour inside daily (2 years), SPY and GLD daily inside weekly (6 years), SPY 5-minute inside daily (60 days).

1. **Trend direction alone has no edge at 5 candles.** Edges ranged from −5.1% to +1.7% across all ten up/down groups. On SPY daily, price rises 60% of 5-day windows anyway, so "trend up" adds nothing beyond that.
2. **With the higher timeframe beat against it in 7 of 10 comparisons**, in line with TJR's rule, but the gaps were mostly small. The clearest: GLD daily, up-trend against the weekly −12.5% vs with it +2.3%; SPY 5-minute, up-trend against the daily −8.5% vs with it +2.6%.
3. **Day 2 candle reads that agree with the higher timeframe beat those that oppose it in 6 of 10 comparisons.** That's barely better than chance, so H4 stays open.

What the bot takes from this:
- This matches TJR's own framing: the trend is "the overall umbrella" that picks the direction, not the entry (05:39, 11:58). Entries come from break of structure, liquidity and the rest of the strategy in later lessons.
- The way the bot measures trend may not yet match how TJR sees it. His swings on the weekly chart are much bigger than 2-candle turning points, and his claim is about the next push going past the last high, not about the next 5 candles. Both are queued as one-variable tests (H5, H7).
