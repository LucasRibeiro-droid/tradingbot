# Day 2 — Candlesticks

Source: TJR Boot Camp, Day 2: Candlesticks (https://www.youtube.com/watch?v=bEkbNGUzQME, 23:17).
Studied from the full video plus the captions. Timestamps below point into the video.
Code: `tradingbot/candles.py`. Thresholds: `CandleParams` in `tradingbot/config.py`.

## What the lesson teaches

### 1. A candle is a span of time (03:05–04:25)
- The timeframe (1m, 5m, 1D, 1W …) is how long one candle takes to close. On the 5-minute chart, one candle is five minutes of price movement.
- One higher-timeframe candle summarizes what the lower timeframe did. TJR can often guess the 1-minute structure from one or two 5-minute candles.
- **Bot rule:** every candle carries its timeframe; a read always says which timeframe it came from.

### 2. Anatomy (04:25–06:42)
Shown on screen as two hand-drawn candles labeled `open` and `close`.
- **Bullish candle:** opens at the bottom of the body, closes at the top.
- **Bearish candle:** opens at the top of the body, closes at the bottom.
- **Wicks** show where price went during the candle but did not close: the top of the upper wick is the highest price, the bottom of the lower wick is the lowest.
- On TJR's chart, up candles are blue and down candles are black. Colors don't matter to the bot; it uses open vs close.
- **Bot rule:** `Candle.body`, `upper_wick`, `lower_wick`, `direction`, `close_location`.

### 3. Only single-candle patterns (07:31–09:52)
- TJR rejects patterns of three or more candles ("mountain tops", W's, head and shoulders) and everything outside one row of the cheat sheet he shows.
- The row he keeps: **doji, long-legged doji, cross doji, inverted cross doji, dragonfly doji, gravestone doji, hammer, hanging man, inverted hammer.**
- He keeps them because they show where price was rejected and where it wasn't.
- **Bot rule (locked):** `LOCKED.max_pattern_candles = 2`. `shape()` only names candles from that row, plus `strong_close` and `regular`. A hammer shape after a rise is named hanging man, and an inverted hammer after a rise is named shooting star, so the study can tell them apart.

### 4. Weakness: a close that couldn't hold (09:52–10:40)
- Example on the S&P 5-minute chart (frame at 10:05: a bullish candle with a fat upper wick, marked in pink): price opened, pushed far up, then closed much lower. Still bullish, but "not strong enough to close" up there, and it was probably taking liquidity above.
- **Bot read:** `kind="weakness"`. A bullish close with an upper wick at least as long as the body leans bearish, and the mirror image for bearish candles. Dojis are excluded.

### 5. Dojis: indecision and fading momentum (10:40–13:22)
- A doji is a small body, usually with long wicks. It shows indecision, sometimes with a lean.
- After a big sell-off, a doji with a long lower wick but no full-bodied close lower means bearish momentum is fading. In the example, price then consolidated.
- A long upper wick that fails to close above a level, followed by a drop, is the mirror case.
- **Bot read:** `kind="indecision"`. A doji after a move leans weakly against that move (strength 0.25).

### 6. Never trade a candle on its own (13:22–15:01)
- Gold daily (frame at 14:30): a bullish doji with strong rejection to the downside, but price is in a downtrend that keeps breaking structure lower, and it kept falling.
- "This is only one confluence." A candle read must never override the trend (Days 4 and 6).
- **Bot rule (locked):** `LOCKED.candle_read_is_entry_signal = False`. Reads are inputs for later lessons, not entries.

### 7. Strong close (15:01–15:37)
- Gold daily (frame at 15:20, circled): a full bearish body with small wicks, so price closed and continued down.
- **Bot read:** `kind="strong_close"`. Body ≥ 70% of the range and a closing-side wick ≤ 10%; leans in the candle's direction.

### 8. Rejection: wicks don't lie (15:37–20:30)
- GBPJPY weekly (frames at 16:00 and 17:30): an Oct 2022 candle opens, sells off hard, then rallies back and closes near its high. Massive lower wick, tiny upper wick, "closed almost as bullish as it could have". Price then rallied and took out the highs.
- GBPUSD weekly (frames at 19:40 and 21:10): a long lower wick, then a full bullish close, then a rally that takes the highs. Two candles read together count as confluence.
- **Bot read:** `kind="rejection"`. A wick ≥ 50% of the range with the close in the opposite third. It's stronger if it also closes in that direction with almost no opposite wick.

### 9. Only closed candles count (16:22–17:46)
- "We can only make bias and decision on candles that have formed, not candles that are forming." Mid-candle, the GBPJPY week looked like a big red candle; it closed as a strong bullish rejection.
- **Bot rule (locked):** `LOCKED.closed_candles_only = True`. `read()` raises `FormingCandleError` on an open candle, and `data.fetch_bars` marks bars whose period hasn't ended as `closed=False`.

### 10. Homework (18:23–23:08)
- Find at least 10 examples on your own chart and note how price reacted after each.
- **Bot version:** `python -m tradingbot.study SYMBOL --timeframe TF --days N`. For every readable closed candle it records the move over the next 5 candles and which side of the candle got taken first. It compares each read against the base rate of all candles on the same chart. Results are saved in `journal/studies/`.

## First homework results (baseline v0-day02, 2026-10-19)

Horizon: 5 candles. "Edge" means hit rate minus base rate.

| Chart | All reads (bull / bear edge) | Notable |
|---|---|---|
| SPY 5Min, 45 days | +1.2% / −0.1% | No reliable edge on its own |
| SPY 1Day, ~6 years | −0.6% / +1.0% | Bullish indecision +22.8% (n=17) |
| GLD 1Day, ~6 years | +2.8% / −0.9% | Bullish strong close +8.1% (n=119) |
| SPY 1Week, ~6 years | +5.7% / +14.7% | Rejections +19.1% bull (n=30), +32.4% bear (n=13) |

What the bot takes from this:
1. **This confirms TJR's point.** Taken alone, candle reads are close to a coin flip on intraday charts. They have to be combined with structure, liquidity and bias from later lessons.
2. **Strong closes are followed by price taking that candle's high (or low) first** 66–88% of the time on every chart. That's short-term continuation. It's a property to test, not a trade.
3. **Rejections looked strongest on the weekly chart**, which is where TJR showed them. The samples are small, so this is a hypothesis.
4. Many groups were compared at once, so a few large edges are expected by chance. Nothing here gets promoted until it holds on data the bot hasn't seen. Open hypotheses are in `journal/hypotheses.md`.
