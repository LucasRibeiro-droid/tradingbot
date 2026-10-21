# Day 34 — Daily Bias, Part 1

Source: TJR Boot Camp, Day 34: Daily Bias (https://www.youtube.com/watch/sjuWqKDsQtI, 20:19).
Studied from the owner's captions (`sources/day34_daily_bias_pt1.md`). The uploaded file
(240p) shows only TJR's webcam for all 20 minutes (checked with one frame per minute), so
the charts he talks through aren't visible. The rules are all spoken. Topic file: `daily_bias.md`.

**Classification:** part 1 of 2 or 3 ("we're gonna do like two of these", 00:07; "maybe we
make this a three-part series", 20:00). Days 35 and 36 are listed as Daily Bias Pt 2 and 3.
The topic stays **open**.

## What it teaches

### 1. Why daily bias (00:15–00:43, 05:30–06:23)
- Execution alone isn't enough: play "into your daily bias as well and understanding where the market wants to go for the day". A trade against it is likely "very short-lived" or a loser.
- On the S&P, "the majority of the daily moves ... is going to be during New York session; everything else is just chop". So trade within the bias "until you're proved wrong". When the market breaks structure against you, "I did everything correctly ... market just wanted to change direction" (05:37–06:23).

### 2. Top-down analysis (00:43–03:16)
- **Weekly:** "literally just look at it ... recent price action ... it's going up, perfect". The line chart helps (00:45–01:03, 01:40–01:58). For day trading TJR doesn't "really care" about the weekly; it matters for swing trades and long-term targets (03:36–03:52, 11:38–11:48).
- **Daily:** "I like to use the daily **current market structure** to figure out my daily bias". "We get a break of structure to the downside, so I'm bearish on the daily. Prior to this candle to the downside I would have been bullish" (02:07–02:27). "What's the trend on the daily? Look at the market structure" (11:30–11:36). **Daily bias = the direction of the last daily break of structure.**
- **4-hour:** "I like to look at the four hour trend as well". Ideal: the 4-hour breaks the same way, "now we have the four hour and the daily both saying bear", then find high-confluence areas on the hourly and execute (02:59–03:21).

### 3. When the 4-hour disagrees (03:23–05:16, 08:43–10:42, 13:42–14:24)
- **Daily bearish, 4-hour bullish (today's S&P):** "this is where it gets tricky ... a perfect example of when we probably wouldn't want to trade the S&P 500 unless we can find some sort of bearish confirmation" (03:26, 04:13–04:22). If you do, "be tentative with our take profits": no long-timeframe targets "because we haven't been proved to the downside on the four hour" (04:44–05:21).
- **Daily bullish, 4-hour bearish:** "that means we're retracing on the daily ... we're prime time getting ready for a setup on the daily". Use the building blocks: price comes into equilibrium and a 4-hour fair value gap; scale down; wait for hourly confirmation (an hourly break up); then lower timeframes for the entry, during the New York open (08:50–10:42). "The four hour, maybe we're in a downtrend because we're in a retracement on the daily, that's ideal" (13:46–13:55).

### 4. The method: imagine a higher-timeframe trade (11:30–14:31, 16:43–17:37)
1. Find the daily trend from market structure.
2. "Find bullish confirmation on high time frames like the four hour or the one hour". Use the building blocks: a 4-hour gap, a daily or 4-hour order block, an hourly break of structure.
3. Once price is in those areas, scale down to the 15-minute and 5-minute and use the execution models: a 15-minute sweep, a 5-minute break, an order block.
- "To find daily bias you're almost imagining that you're trying to take a trade on a high time frame" (14:24–14:31; repeated 17:07–17:14).
- The payoff: a higher-timeframe-confirmed trade with 4-hour or daily take profits, entered off a 5-minute execution (16:43–17:04).
- **Lower-timeframe signals against the bias are ignored:** "on the 15 minute you're probably seeing a liquidity sweep, break of structure to the upside. Are we bullish? No, we're bearish. So we're waiting for these price points to get hit" (17:23–17:37).

### 5. Live example: S&P, bearish daily (14:34–18:45)
- Daily break down, highs above as the draw. The 4-hour swept them; an hourly break down "during London session: are we going to trade that? Hell no, it's the S&P 500, who's trading the S&P during London session".
- Then a sweep, break, gap, order block and equilibrium setting up. "We're not waiting for just a down candle, we're waiting for a five minute break of structure."
- **Targets:** 4-hour retracement levels (an imbalance, the equilibrium of the 4-hour swing, the 4-hour order block) and daily liquidity.
- The weekly is up while the daily is down, "so we're retracing on the weekly". Weekly targets: a gap, liquidity, an order block.

## Connections
- **Day 4:** the higher timeframe outranks the lower; the forecast routine (week, days, today); the line chart.
- **Day 6:** a break against the higher timeframe is a retracement, here applied daily vs 4-hour.
- **Days 30–33:** the four entry models are the lower-timeframe execution inside the bias; Day 33 previewed "short-lived" moves.
- **Days 18, 22:** trade from the New York open; no S&P trades in the London session.
- **Days 37, 38:** take profits and stops; "tentative" take profits when the 4-hour disagrees.

## Issues
1. **When the 4-hour disagrees, two answers:** "probably wouldn't want to trade" (daily bear, 4-hour bull) and "that's ideal" (daily bull, 4-hour bear). Likely the same idea: a 4-hour move against the daily is a daily retracement. Trade only once the hourly or 4-hour confirms back in the daily's direction, and keep targets short until the 4-hour agrees [Inferred]. Days 35–36 may say more.
2. **Which swings define the daily structure:** not said. The bot's two-candle swings make its daily bias flip every few days: GLD had 12 daily breaks between July and September 2026. TJR's daily structure probably uses bigger swings (H31).
3. **The weekly:** "just look at it". Not yet measurable beyond the trend.

## The bot's first test (H30, 2026-10-21; `models_study.py --bias`)
The four entry models' setups (Day 33), split by the bot's daily bias when the setup's break closed. Model 1 (sweep + break) avg R per trade, with vs against the bias:

| Chart | With bias | Against |
|---|---|---|
| SPY 4Hour | −0.22 (n=6) | −0.22 (n=37) |
| SPY 1Hour | −0.12 (26) | +0.01 (41) |
| SPY 15Min | **+0.14** (25) | −0.06 (30) |
| GLD 4Hour | +1.17 (1) | +0.16 (33) |
| GLD 1Hour | **+0.17** (16) | +0.07 (46) |
| GLD 15Min | −0.20 (25) | +0.51 (31) |

- **Better with the bias:** on 2 of the 5 comparable charts. Models 2–4 show no consistent pattern either.
- **Few "with" setups on the 4-hour (6 and 1):** with two-candle daily swings, the daily flips with every few days of movement, so a fresh 4-hour reversal is nearly always "against" it.
- **Verdict:** not supported *with the bot's current definition of daily structure*. That definition is the likely weak point (H31), not necessarily TJR's claim. Retest after Days 35–36.

## Provenance audit
- **[TJR]**
  - Daily bias = the daily market structure (the last daily break).
  - Top-down from weekly (trend, line chart) to daily, then 4-hour.
  - 4-hour agreeing is ideal; a 4-hour against the daily is a daily retracement, so wait for confirmation and keep take profits tentative.
  - Imagine a higher-timeframe trade, then execute on the 15/5-minute.
  - Ignore lower-timeframe signals against the bias.
  - The S&P's daily move is made in the New York session; no S&P trades in London.
- **[Inferred]** The two answers on a disagreeing 4-hour are one rule.
- **[Bot]** Daily structure from two-candle swings; "with/against" = the setup's side vs the last daily break when the setup's break closes.
