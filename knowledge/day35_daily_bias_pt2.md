# Day 35 — Daily Bias, Part 2: live, on the charts

Source: TJR Boot Camp, Day 35: Daily Bias pt. 2 (https://www.youtube.com/watch/UPA9LQW7phk, 14:59).
Studied from the uploaded video (480p) and the owner's captions
(`sources/day35_daily_bias_pt2.md`). Frames viewed at 01:15, 04:08, 05:15, 06:12, 08:55,
09:08, 11:05, 12:55; two are saved in `sources/day35_frames/`. Recorded live with his
Discord, about 17 minutes before the New York open (00:00–00:31), with the charts Day 34
was missing (00:45). Topic file: `daily_bias.md`.

**Classification:** part 2 of 3 (Day 36 = part 3). Topic still **open**.

## What it teaches

### 1. Weekly, then daily (01:02–04:41; frame at 04:08)
- Start on the weekly, "figure out where's our overall direction ... we can even use a line chart". The S&P weekly is up, about to break monthly structure up (01:04–01:57).
- Then the daily, "because we are trying to base our trades based off of daily candles" (02:53–03:03).
- **Trade the extension, not the retracement:** "if we're bullish but we're in a retracement on the daily, are we going to try and take a trade off a short ... or would we want to take the extension? Because the extension is always way larger ... ideally you're trying to catch longs in an uptrend" (03:12–03:39).
- **How sensitive the daily structure is** (frame at 04:08): "we broke structure to the downside right here, and this is why I took shorts yesterday". In the frame that break is a pullback of about 4–5 daily candles below a recent small low after a new high. "We just recently closed back above here, we broke structure back to the upside on the daily, so we're bullish again". **TJR's daily bias flips within days, off small daily swings** (03:41–04:15).
- **His own mistake:** shorts on a daily liquidity sweep "although ... we didn't have confirmation on lower time frames, and that's where I messed up" (03:46–04:00).
- **Don't force a bias:** "as much as I would like to force my bias on the market and say, oh, the fundamentals ... we can't do that ... we have to take a trade based off of what the market gives us" (04:13–04:41).

### 2. GBPUSD: the weekly says up, the daily says down (05:08–08:38; frames at 05:15, 06:12)
- Weekly bullish (a weekly order block: liquidity swept, then a rally); daily: a break down. "On the daily, where we're trying to guess where the market's going to go, we're still bearish, so **until we flip bullish on the daily**" (05:08–05:44). **The daily governs; the weekly is an overview.**
- The daily is retracing up ("which probably means we broke structure on the four hour"). "This is when it's **prime time to try and catch a short**, and this is where we can use our building blocks": a fair value gap and an order block above, from a sweep and a big break down. With "a break of structure on the 15 minute I'm ready to go" (05:44–06:30).
- **The process, stated** (06:51–08:15):
  1. The daily trend (bearish).
  2. "A building block area of high confluence within our bias": a bearish gap or order block on the 4-hour. "This whole price zone is a high-confidence price zone to go short on the four hour."
  3. Scale lower and use the same building blocks there: a 15-minute sweep, a 15-minute break and order block entry, then a 5-minute break: "that's our sniper entry".
  4. Target higher-timeframe take profits.
- Later (13:56–14:12): a GU short needs "at least a 15-minute break of structure, because we're bullish on the hourly and bullish on the four hour even though our daily bias is short".

### 3. Gold: weekly and daily bearish, the daily retracing (08:49–10:04; frames at 08:55, 09:08)
- "What are we doing right now? We're retracing on the daily, even better."
- The retracement tools: equilibrium ("we're not yet in a discount") and a fair value gap within the discount (for a short, the upper half).
- On a lower timeframe: an imbalance and liquidity above the highs. "Probably going to draw towards these highs, probably going to fill this imbalance". Then on an even lower timeframe, wait for the sweep and the fill, and a 15-minute sweep + break. "We're taking an hourly and a four hour type of trade, but we're getting good entries."

### 4. S&P: everything aligned for longs (10:40–13:30; frames at 11:05, 12:55)
- Mark every building block in line with the bias:
  - one-hour lows (liquidity);
  - a 15-minute order block ("this whole move down ... swept this liquidity without closing below it, caused a huge rally up");
  - imbalances.
- "It doesn't matter where the market goes, we just need to adapt to it. We mark out all of these building blocks that are in line with our daily bias" (12:43–12:56).
- "The S&P looks great for longs today. Why? The hourly's in an uptrend, the four hour's in an uptrend, the daily is in an uptrend, the weekly's in an uptrend, 15 minute's in an uptrend" (13:09–13:19). Then: price fills one of the areas, a lower-timeframe break up for confirmation, enter.
- **Execution timeframes:** "on Forex like the 15 and the five minute; on the S&P ... the five minute and the one minute" (11:43–11:51).
- News in 30 minutes: "trade after news comes out" (02:04, 14:54).

## What this settles and changes
1. **Daily structure is sensitive in TJR's own charts.** A few-candle pullback breaking a recent small daily low counted as a daily break; one close back above flipped it. So the bot's two-candle daily swings aren't obviously wrong. **H31 weakened** [Inferred from frames 04:08, 05:15].
2. **The daily governs the weekly.** The weekly gives the overview and targets [TJR 05:31–05:44].
3. **Daily bias isn't only a filter; it's a location.** First find the high-confluence building-block area on the 4-hour / 1-hour within the bias, then execute inside it on the 15/5-minute (or 5/1-minute on the S&P) [TJR 06:51–08:15].
4. Trade the extension, not the retracement [TJR 03:12].
5. A lower-timeframe break is required even when the daily level is reached [TJR 03:46–04:00, his own lesson].

## The bot's test: the timeframes aligned (H32, 2026-10-21; `models_study.py --bias`)
Setups labelled "aligned" when the daily *and* the 4-hour trend agree with the setup. Model 1's average R per trade:

| Chart | Aligned | Not aligned |
|---|---|---|
| SPY 1Hour | **+0.21** (n=7) | −0.07 (60) |
| SPY 15Min | −0.18 (17) | +0.12 (38) |
| SPY 5Min | **+0.07** (26) | −0.25 (55) |
| GLD 1Hour | **+0.23** (5) | +0.08 (57) |
| GLD 15Min | −0.23 (20) | +0.43 (36) |
| GLD 5Min | −0.07 (31) | +0.24 (46) |

- **Aligned does better on 3 of 6 charts.** Two of those have only 5–7 aligned trades.
- **Models 2–4** show the same lack of pattern.
- **Not supported.** Agreement between timeframes alone, applied to every sweep + break, isn't TJR's method. He also requires the setup to happen *inside* a higher-timeframe building block within the bias (H33). The harness's continuation path (a higher-timeframe zone in the higher-timeframe trend, then a lower-timeframe break) is the nearest thing the bot has; its results so far are near break-even.

## Connections
- **Day 34:** the same method, now with charts; settles how sensitive the daily structure is.
- **Days 30–33:** the entry models are step 3, the "sniper entry".
- **Days 20–28:** building blocks on the 4-hour as the high-confluence area.
- **Day 4:** higher timeframe outranks lower; weekly → daily → today.
- **Day 3, Day 7:** don't force a view; follow the plan.

## Provenance audit
- **[TJR]**
  - Weekly overview, then the daily governs.
  - Trade the extension.
  - Don't force a bias from fundamentals.
  - Need lower-timeframe confirmation.
  - A daily retracement is "prime time" for a trade in the daily's direction, at a 4-hour building block.
  - The process: daily trend → high-confluence area → lower-timeframe building blocks → 5-minute break.
  - Everything aligned = "looks great".
  - Execution timeframes per market.
  - Trade after news.
- **[Inferred]**
  - Daily structure is as sensitive as the bot's, from the frames.
  - Bias as a location as well as a direction.
- **[Bot]** The H32 labels: the bot's own daily and 4-hour trend at the setup's break.
