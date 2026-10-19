# Day 6 — Break of Structure

Source: TJR Boot Camp, Day 6: Break of Structure (https://www.youtube.com/watch?v=PmhuPbY8ZHo, 30:30).
Studied from the full video plus the captions.
Code: `tradingbot/trend.py` (`swings`, `trend_series`). Chart check: `tradingbot/chart.py`.
Study: `tradingbot/trend_study.py` (groups 4 and 5).

**This lesson revises Day 4.** The Day 4 code found swings as turning points with 2
candles on each side. Day 6 defines highs and lows exactly, and says a trend changes
only when a candle closes past the *most recent* one. The trend code now follows Day 6;
the old method is kept as `swing_method="pivot"` for comparison.

## What the lesson teaches

### 1. What a high and a low are (01:56–06:12)
- **High:** a move up, then a move down. One up candle followed by one down candle is enough.
- **Low:** a move down, then a move up.
- The level is the most extreme wick of the two candles. The high is whichever of the two has the higher wick, even if it's the down candle (04:20).
- Highs and lows don't have to look pretty. TJR zooms into the 4-hour chart (frame at 06:05) to show the real low sits under a different candle than it seems on the daily.
- A high isn't a high until the next candle closes down: "this candle forming is not a high" (21:14).
- **Bot rule:** `swing_method="two_candle"` (default). A swing is known once its second candle closes.

### 2. Break of structure: a close, never a wick (07:37–13:25)
- Up: a candle **body closes above** the most recent high. Down: a body closes below the most recent low.
- Gold daily (frames at 12:40, 13:15): a later wick pokes above the high at 1984.31, "technically a higher high", but no candle closes above it, and price falls. "It is not a break of structure unless the candle closes above a high or below a low. Write that down."
- **Bot rule (locked):** `LOCKED.bos_requires_close`. `trend_series` marks `bos_up` and `bos_down` on the closing candle only. A wick past the level without a close is marked `sweep_high` or `sweep_low` (a fake).

### 3. Only the most recent high and low count (08:54, 18:00–19:00, 27:16–28:34)
- Once a newer low forms, the older lows stop mattering, even if they're lower.
- **Bot rule:** `trend_series` keeps only the most recent high and low.

### 4. TJR's checklist, typed out on screen (14:02–18:00, frame at 17:50)
1. Identify the trend: uptrend or downtrend.
2. In an uptrend, watch the lows.
3. In a downtrend, watch the highs.
4. Break of structure down (uptrend into downtrend): a close below the most recent low.
5. Break of structure up (downtrend into uptrend): a close above the most recent high.
- **Bot rule:** exactly this, in `trend_series`. Before the first break, the bot watches both sides.

### 5. Consolidation: highs and lows with no break (19:42–20:20)
- Gold daily (frame at 20:00): high, low, high, low, and nothing closes past them. "Market had no clue where it wanted to go." A terrible week to trade.
- **Bot rule:** no break means no direction change; Day 4's consolidation flag still applies.

### 6. A break isn't forever; higher timeframes decide (22:13–23:18)
- A break down on the daily while the weekly is bullish is "just a retracement" (GBPUSD).
- **Bot rule:** combines with Day 4's higher-timeframe bias. The study measures breaks with versus against the higher timeframe.

### 7. Fakes: wicks that trap traders (23:18–26:20)
- GBPUSD weekly (frames at 23:50, 25:40): wicks below the most recent low that never close below it. Mid-week one candle was a full red candle, "ninety percent of retailers were short", and it closed back up. Price kept going higher "because the trend never was broken".
- "This looks like a liquidity sweep." These are the subject of Day 8.
- Even a real break is never certain: "even when we know for certain we don't actually know", so never trade one that isn't even confirmed (24:36).

### 8. Homework (29:15–30:30)
- Find 10 real breaks of structure and 10 fakes (a wick past a high or low that someone might mistake for a break).
- **Bot version:**
  - `python -m tradingbot.chart SYMBOL --timeframe 1Day` draws every high, low, break and fake on a chart, so you can check the bot's eye against TJR's. The first ones are in `journal/charts/`.
  - The study counts hundreds of each and measures what happened next.

## First study results (baseline v0-day06, 2026-10-19)

Same charts as Day 4. Horizon: 5 candles. "Edge" is hit rate minus the base rate of the same chart.

1. **A break down against a higher-timeframe uptrend was the weakest signal.** It did worse than the base rate in 4 of 5 charts: SPY daily −13.7% (n=49), GLD daily −9.3% (n=43). That backs TJR's "just a retracement".
2. **Breaks up against a higher-timeframe downtrend did not fail.** They beat the base rate in all 5 charts (+1.0% to +8.9%). So the rule held on the down side and not on the up side. One likely reason: SPY and GLD both drifted up over these years. That's a hypothesis to test (H9).
3. **Fakes on their own had no consistent edge.** A sweep of a low followed by a rise beat the base rate in 3 of 5 charts; a sweep of a high followed by a fall in 2 of 5. TJR says these are liquidity sweeps, taught next in Day 8, so they're expected to need that context.
4. **Two-candle swings vs the old pivot swings:** with-versus-against-the-higher-timeframe results were similar (6 of 10 vs 7 of 10 comparisons favored "with"). The two-candle rule is the lesson's definition, so it's the baseline regardless.
