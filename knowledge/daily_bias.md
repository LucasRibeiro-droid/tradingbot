# Daily bias (topic file: Days 34, 35, 36)

**Status: complete** (Days 34, 35, 36).
Lesson notes: `day34_daily_bias_pt1.md`, `day35_daily_bias_pt2.md`, `day36_daily_bias_pt3.md`.

## What it is [TJR Day 34]
- Where the market wants to go for the day. Trades against it are likely "short-lived" or losers [00:15–00:43; Day 33, 23:27].
- **Daily bias = the daily market structure**: the direction of the last daily break of structure [02:07–02:27, 11:30–11:36].

## How to find it [TJR Day 34]
1. **Weekly:** the trend; the line chart; "just look at it". Long-term targets and swing trades; less important day to day [00:45–01:58, 11:38].
2. **Daily:** the market structure gives the bias [02:07].
3. **4-hour:** ideally agrees [02:59–03:21]. If it doesn't, the daily is retracing: wait for the building blocks on the 4-hour / 1-hour (equilibrium, gap, order block) and an hourly break back in the daily's direction. Keep take profits tentative until the 4-hour agrees [03:26–05:21, 08:50–10:42, 13:46].
4. **Execute on the 15-minute / 5-minute** with the entry models, inside those areas, during the session (New York open for the S&P) [13:58–14:24, 16:37–16:45].
- "You're almost imagining that you're trying to take a trade on a high time frame" [14:24, 17:07].
- Ignore lower-timeframe setups against the bias [17:23–17:37].

## Added by Day 35 (live, with charts)
- **The daily governs; the weekly is the overview** [Day 35, 05:31–05:44].
- **Trade the extension, not the retracement** [Day 35, 03:12–03:39].
- **Bias is a location too:**
  1. Find "a building block area of high confluence within our bias" on the 4-hour / 1-hour.
  2. Scale down and use the same building blocks there (15-minute sweep, break, order block).
  3. Take the 5-minute break as the "sniper entry".
  4. Target higher-timeframe take profits [Day 35, 06:51–08:15].
- **Everything aligned** (1-hour, 4-hour, daily, weekly, 15-minute) = "looks great" [Day 35, 13:09].
- **Lower-timeframe confirmation is required** even at a daily level: TJR's own loss the day before [Day 35, 03:46].
- **Don't force a bias from fundamentals** [Day 35, 04:13].
- **Execution timeframes:** Forex 15/5-minute; S&P 5/1-minute [Day 35, 11:43].
- **The daily structure is sensitive:** in the 04:08 frame a pullback of 4–5 daily candles below a recent small low is a daily break, and one close back above flips it [Inferred from frames].

## Added by Day 36
- **The weekly sets the context:** a daily break against the weekly trend is a weekly retracement. Use the weekly retracement tools to see how far it goes [Day 36, 00:24–01:08].
- **The timeframe ladder:** a 15-minute break = a 1-hour retrace; a 1-hour break = a 4-hour retrace; a 4-hour break = a daily retrace; a daily break = a weekly retrace. Don't get trapped by lower-timeframe breaks [Day 36, 07:41–08:30].
- **The discount is "the bare minimum"** for a retracement trade [Day 36, 11:22].
- **No reaction in the area = "like it was never there"** [Day 36, 09:56].
- **The bias changes on a daily break back** in the weekly's direction: "the weekly retracement is over" [Day 36, 14:52–15:30].
- **Targets in the bias:** the most recent low, the discount level, daily liquidity, daily order blocks. Partials; no multi-day holds [Day 36, 14:30–14:40, 19:41–20:53].

## How the bot measures it so far
- The harness's higher-timeframe filter (`trend.state_at` on daily candles) is already "the last daily break of structure".
- `models_study.py --bias` labels setups with / against it.
- The bot's daily swings are two-candle swings, so its daily bias flips every few days (GLD: 12 times in about 12 weeks). Day 35's frames show TJR's flips within days too, so this is probably not the weak point (H31 weakened).

## Tests so far (2026-10-21)
- **H30, with the daily bias vs against it:** model 1 better with it on 2 of 5 charts. Not supported.
- **H32, daily and 4-hour aligned:** better on 3 of 6 charts, two of those with 5–7 trades. Not supported.
- **H33, with the bias and in the daily discount:** better on 2 of 6 charts, lower win rate on 5 of 6. Not supported.
- None of the three filters improves the bot's entry models. Not yet tested: TJR's stacking of 4-hour and hourly order blocks with a lower-timeframe reaction, and his exits (daily targets, partials). Details in the three lesson files.

## Retest with TJR's exits (2026-10-21)
The weak results above used the old single-target exit. Rerun on SPY and GLD, 1-hour, 15-minute and 5-minute, all four models, with TJR's exits:

| Filter | Better than its opposite (model × chart) | Model 1, pooled avg R per trade |
|---|---|---|
| H30: with the daily bias vs against | 4 of 24 | **with +0.08 (163 trades) vs against +0.49 (225)** |
| H32: daily + 4-hour aligned vs not | 3 of 24 | aligned −0.05 (105) vs not +0.46 (283) |
| H33: bias + daily discount vs not | 10 of 24 | located +0.28 (70) vs not +0.33 (318) |

- **With the bot's definitions, setups *against* the daily bias did better.** Against beat with in 9 of 12 half-periods (each chart's period split in two), so it isn't one stretch of market. The samples are small (7–23 trades per cell).
- **This contradicts TJR and a locked rule** (Day 4: never trade against the higher timeframe; the harness's reversal path applies it). Locked rules aren't changed by the bot; this is for the owner to decide.
- **Possible reasons:**
  - The bot's daily bias is a lagging, mechanical stand-in. A lower-timeframe sweep + break "against" it is often the start of the next daily leg, before the daily break confirms it. TJR reads that from context the bot doesn't have.
  - SPY/GLD intraday mean reversion.
  - In-sample, no costs.
- **H34, does the bot's daily bias lag?** Not supported as an explanation (`bias_lag_study.py`).
  - Within 3 days the daily flipped toward 46% of the "against" winners vs 21% of the losers. But a winning move often causes that flip, so this is circular.
  - "Against" setups as a group were followed by a flip about 31% of the time, the same as any day.
- **Still unexplained.** Next idea (H35): "with" setups come late in a daily leg, with less room left.

## Still open
1. ~~Which daily swings define the structure (H31).~~ Day 35's frames: small daily swings, like the bot's.
2. ~~Exactly when a 4-hour move against the daily may be traded.~~ Day 36: once it reaches the daily discount and a higher-timeframe area, on a lower-timeframe reaction.
3. ~~How the weekly enters.~~ Day 36: context and targets; the daily decides.
4. Take-profit rules when the timeframes disagree (Day 37).
