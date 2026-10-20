# Day 12 — Liquidity, Part 3: using it to trade

Source: TJR Boot Camp, Day 12: Liquidity Pt 3 (https://www.youtube.com/watch?v=KtC2SbemF6w, 20:04).
Studied from the uploaded video (360p, with audio). Transcript made offline with Whisper,
in `sources/day12_liquidity_pt3.md`; charts checked from frames.
**Liquidity is one indicator, taught across Days 8, 10 and 12; see `liquidity.md`.** How the
bot combines it with its other indicators is in `decision.md`. This file keeps what Day 12
itself added, with timestamps.

## What Day 12 adds

### 1. Prominent highs and lows (03:36–05:56)
- Mark highs and lows as liquidity, "most importantly prominent highs and lows". What's prominent varies by timeframe, but "if you just look at the chart, it's relatively easy".
- On the S&P 500 daily (frames at 05:20, 05:55: horizontal lines across 2022): the high at the start of the big downtrend, a double top, and a high that broke structure on the daily ("I would also consider this a prominent high because it broke structure").

### 2. Liquidity is a magnet (05:56–06:51)
- Price is drawn to liquidity because that's where the market makers want it. "Any form of liquidity, consider it a magnet for price." Not "oh buy, oh sell": an area where orders *could* get filled.

### 3. Wait for confirmation; no reaction, no trade (06:21–07:35)
- Pressing sell when a high is hit would "lose way more than you win". Wait for the area to be hit, then wait for confirmation (break of structure and other confluences) that orders were filled.

### 4. Targets: the liquidity on the other side (07:35–10:22)
- If you think price is going lower, it will seek out the lows. Banks that sold at the highs need to exit, and they exit where other traders are exiting too: at the lows.
- "We take out a high, we get a break of structure to the downside ... and then where are we targeting? The lows."

### 5. Walkthroughs (10:28–17:24)
- **S&P 500 daily, 2022** (frames at 11:20, 12:50): a prominent high is taken, the break of structure is a close below the most recent low, entry on the break or a 4-hour fair value gap, target the next prominent low. Later: two sets of highs; price pushes past the first "without much of a reaction", takes the second and breaks down. At recording time price was pushing toward the next untaken high (~4325).
- **GBPUSD 4-hour then 1-hour** (frame at 13:40): highs that look untouched on the 4-hour are swept on the 1-hour (equal highs ~1.2547); break of structure, retrace into an order block, collapse, then lows taken and imbalances filled.
- **GBPUSD 5-minute** (frame at 14:45): highs barely wicked; break of the most recent low "that's applied to a break of structure"; imbalance filled on the 5-minute; short to the lows.
- **Gold 5-minute** (frame at 15:25): a low at 1957.96 swept by a wick to ~1954, a quick close back above, a dip into a shaded imbalance (the entry), then price draws back up to the previous highs and chops.
- Quick examples on several timeframes, 1-minute to 12-hour (frame at 16:35, S&P 12-hour with paired lines at swept lows): "sweep, rally", "sweep, drop".

### 6. A piece, not a strategy (01:41, 13:45, 19:25)
- "It's a piece that we can plug in to a strategy." Not every high or low will be used to fill orders; that's why we wait for a break of structure, then a fair value gap or order block and a reaction.

### Homework (17:39–19:56)
- Find five liquidity sweeps and, for each, the confluence that explains the move: "there was a break of structure ... then it filled an imbalance and reacted off of it, that's where I'm entering."
- **Bot version:** `python -m tradingbot.decision_study` runs the bot's decision process over history and records every decision (`journal/studies/decision_*.json`) with its reasons, entry, stop, target and result, with and without the liquidity indicator.

## Provenance audit (2026-10-20)

- **[TJR]** Prominent highs/lows; liquidity as a magnet; no confirmation, no trade; target the liquidity on the other side; the walkthroughs; "a piece, not a strategy".
- **[Bot]** In the test harness: entry at the break's close, stop beyond the last 10 candles, a 50-candle limit. TJR shows entries on the retracement into an imbalance or order block, and teaches stops on Day 38.
