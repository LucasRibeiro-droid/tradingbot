# Daily bias (topic file: Days 34, 35, 36)

**Status: incomplete.** Days 34 and 35 are learned; Day 36 hasn't been received.
Lesson notes: `day34_daily_bias_pt1.md`, `day35_daily_bias_pt2.md`.

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

## How the bot measures it so far
- The harness's higher-timeframe filter (`trend.state_at` on daily candles) is already "the last daily break of structure".
- `models_study.py --bias` labels setups with / against it.
- The bot's daily swings are two-candle swings, so its daily bias flips every few days (GLD: 12 times in about 12 weeks). Day 35's frames show TJR's flips within days too, so this is probably not the weak point (H31 weakened).

## Tests so far (2026-10-21)
- **H30, with the daily bias vs against it:** model 1 better with it on 2 of 5 charts. Not supported.
- **H32, daily and 4-hour aligned:** better on 3 of 6 charts, two of those with 5–7 trades. Not supported.
- **What's missing is the location** (H33): TJR takes the setup only *inside* a higher-timeframe building block within the bias. Details: `day34_daily_bias_pt1.md`, `day35_daily_bias_pt2.md`.

## Open until Days 35, 36
1. ~~Which daily swings define the structure (H31).~~ Day 35's frames: small daily swings, like the bot's.
2. Exactly when a 4-hour move against the daily may be traded.
3. How the weekly enters (targets only, or a filter).
4. Take-profit rules when the timeframes disagree (Day 37).
