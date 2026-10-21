# Day 36 — Daily Bias, Part 3: recap on the charts

Source: TJR Boot Camp, Day 36: Daily Bias pt. 3 (https://www.youtube.com/watch/Y1lqifylC4s, 22:25).
Studied from the uploaded video (360p) and the owner's captions
(`sources/day36_daily_bias_pt3.md`). Frames viewed at 13:30 and 20:30, plus one per minute;
one is saved in `sources/day36_frames/`. Topic file: `daily_bias.md`.

**Classification:** part 3 of 3; **completes the daily bias topic** ("daily bias is wrapped up", 21:52).
Off-topic stretch: 01:40–05:25 (TJR's macro view of the S&P: COVID-era liquidity, inflation).
It's his opinion, not a method.

## What it teaches

### 1. Why the weekly matters (00:24–01:08, 05:28–05:48)
- "If we break structure to the downside on the daily but we're in an uptrend on the weekly, odds are it's going to be a **weekly retrace**. ... Higher time frames hold higher power."
- So use the retracement tools on the weekly (equilibrium, a weekly gap) to see where that daily move is likely to go, "and keep that in mind while we're trading on the daily".

### 2. The routine, once more (05:48–07:41)
1. **Daily structure:** "a break of structure to the upside, cool, we're looking for buys".
2. **4-hour and 1-hour:** buys too, "even better".
3. **On the 4-hour and 1-hour, find the high-confluence areas:** liquidity under hourly lows, imbalances, an order block ("it swept these lows, caused a rally higher").
4. **When price comes into those areas,** map the 15-minute / 5-minute areas, then a sweep and a 5-minute break → long.
- "Not much" on the 4-hour that day: "that's why I didn't trade the S&P on Friday".

### 3. The timeframe ladder (07:41–09:21)
- "15 minute break of structure: one hour retrace. One hour break of structure: four hour retrace. Four hour break of structure: daily retrace. Daily break of structure: weekly retrace. Higher time frame holds higher power."
- "Stop getting trapped into the low time frame bias ... a one minute break of structure could very well just be a five minute retrace."
- **The goal:** "high time frame confluence with low time frame execution to get long-term trades that run pretty far". Take the extension, not the retracement, "every single day".

### 4. No reaction, no trade (09:21–10:12)
- "When price is not in line with your daily bias, you're screwed."
- "If it comes into these areas and doesn't give us a reaction, what do we do? Like it was never there."

### 5. GBPUSD: daily down, weekly up (10:43–15:30; frame at 13:30)
- Daily downtrend, so shorts, but "this downtrend probably won't come all the way down here, why? Because the weekly is in an uptrend". Targets come first:
  1. The weekly discount: "that's like **the bare minimum that I look for for retracements: is it even in a discount**" (11:22–11:27).
  2. A daily order block and an imbalance in the discount.
  3. Hourly liquidity.
- The short TJR took the day before: the 4-hour had broken up, "but look at the daily ... all the way up in a discount" (for a short: above the 50%). Price was in a 4-hour order block (sweep, extension down) and tapped an hourly order block, with "reactions on the 15 and the five minute" → short. That gives "a daily trade where we can then target daily take profits, off a five minute execution" (13:13–14:30).
- "The next draw on liquidity in a downtrend is just the most recent low", then the discount level, liquidity, the order block (14:30–14:40).
- **The bias changes when the daily breaks back up:** "that means the weekly retracement is over ... the next leg up for the weekly is ready to go" (14:52–15:30).

### 6. Gold: weekly and daily down, 4-hour up (15:50–20:53; frame at 20:30)
- "Weekly downtrend, monthly uptrend ... who really cares, because that's such high time frame." The weekly gap "does that really matter with our daily bias? Not really."
- Daily retracing (the 4-hour broke up), "we're in a discount" (for a short), a filled 4-hour imbalance, inside an hourly order block. So: "we're literally just waiting for confirmation to the downside on lower time frames", a 15-minute break down. "Do we have a break of structure to the downside on the 15 minute yet? No we don't, so are we going to execute?" (no).
- **Targets:** daily liquidity and daily order blocks, "take profit one, two, three, four". The first daily take profit is 1:4.79; holding to the last is 1:13.5. "Would I do that? Hell no, because I take partials." He doesn't hold over the weekend / for days (13:06–13:13, 20:00–20:53).
- The frame at 20:30: the short drawn from inside the hourly order block on the 15-minute, stop just above the box, target far below.

### 7. Discipline (21:00–21:44)
- "If you don't have [the trading plan and risk management] down by now you're emotional ... you need to go to demo."
- Next: take profits, then stop losses, then a check-in.

## Connections
- **Days 34, 35:** completes the topic: the weekly–daily relation, the timeframe ladder, "no reaction = never there".
- **Days 26, 28:** the discount as the "bare minimum" for a retracement trade.
- **Days 20–24:** 4-hour and hourly order blocks as the high-confluence areas.
- **Days 30–33:** lower-timeframe execution = the entry models.
- **Day 4, Day 6:** higher timeframes hold higher power; a lower-timeframe break against a higher timeframe is a retracement.
- **Day 18:** partials; **Days 37, 38:** take profits and stops next.

## The bot's test: daily bias + the daily discount (H33, 2026-10-21; `models_study.py --bias`)
Setups labelled "located" when they're in the daily bias's direction and the setup's sweep happened in the daily discount (a long below the daily swing's 50%, a short above it). Model 1's average R per trade:

| Chart | Located | Not located |
|---|---|---|
| SPY 1Hour | −0.15 (n=16) | −0.01 (51) |
| SPY 15Min | **+0.07** (13) | +0.02 (42) |
| SPY 5Min | −0.38 (14) | −0.10 (67) |
| GLD 1Hour | **+0.31** (10) | +0.06 (52) |
| GLD 15Min | −0.30 (8) | +0.28 (48) |
| GLD 5Min | −0.32 (11) | +0.19 (66) |

- Better on 2 of 6 charts; the win rate is *lower* when located on 5 of 6. **Not supported**, with small samples (8–16).
- **Daily bias so far, three filters on the bot's data:**
  - direction (H30);
  - daily + 4-hour agreeing (H32);
  - direction + the daily discount (H33).
- None improves the bot's entry models.
- **Not in these tests yet:**
  - TJR's specific stacking: a 4-hour *and* an hourly order block, then a lower-timeframe reaction.
  - His exits: daily targets, several take profits and partials. His trades aim for 1:4.79 and beyond; the bot's target is the nearest liquidity.

Days 37 (take profits) and 38 (stops) teach those exits, the largest untested part (H19).

## Provenance audit
- **[TJR]**
  - The weekly sets the context: a daily break against it is a weekly retracement.
  - The timeframe ladder (each break = a retracement of the next timeframe up); don't get trapped by lower-timeframe breaks.
  - The routine: daily structure → 4-hour/1-hour areas → lower-timeframe execution.
  - No reaction = it was never there.
  - The discount is the bare minimum for a retracement trade.
  - Bias changes on a daily break back.
  - Targets: next low, discount, liquidity, order block; partials, no multi-day holds.
- **[Inferred]** "Discount" for shorts = the upper half (as Days 26, 28).
- **[Bot]** The H33 labels: the bot's daily bias and daily equilibrium at the setup's break, judged at the sweep's price.
