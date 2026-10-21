# Daily bias (topic file: Days 34, 35, 36)

**Status: incomplete.** Day 34 is learned; Days 35 and 36 haven't been received.
Lesson notes: `day34_daily_bias_pt1.md`.

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

## How the bot measures it so far
- The harness's higher-timeframe filter (`trend.state_at` on daily candles) is already "the last daily break of structure".
- `models_study.py --bias` labels setups with / against it.
- **Weak point:** the bot's daily swings are two-candle swings, so its daily bias flips every few days. On GLD it broke 12 times in about 12 weeks (July to September 2026) (H31).

## Test so far (H30, 2026-10-21)
With the bias vs against it, model 1's average R per trade:
- Better with the bias on 2 of 5 comparable charts; no consistent pattern for the other models.
- Not supported with the current definition. Details: `day34_daily_bias_pt1.md`.

## Open until Days 35, 36
1. Which daily swings define the structure (H31).
2. Exactly when a 4-hour move against the daily may be traded.
3. How the weekly enters (targets only, or a filter).
4. Take-profit rules when the timeframes disagree (Day 37).
