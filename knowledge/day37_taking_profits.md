# Day 37 — Taking Profits

Source: TJR Boot Camp, Day 37: Taking Profits (https://www.youtube.com/watch/FjSiLFrg5fo, 11:05).
Studied from the uploaded video (720p) and the owner's captions (`sources/day37_taking_profits.md`).
Frames viewed at 07:15 and 09:55; one is saved in `sources/day37_38_frames/`. Topic file: `exits.md`.

**Classification:** a single lesson; **complete**. Methodology (exits).

## What it teaches

### 1. Take profit at the building blocks (01:45–03:30)
- "Where are we looking to take profit at? At our building blocks" (02:01–02:07), "on whatever time frame that you're executing on, or one higher time frame" (02:20–02:26).
- Example (a short TJR calls "a stupid short position", only to show placement): take profits at the top and bottom of an order block, the liquidity in line with its bottom, inside and at the bottom of a fair value gap (02:26–03:30).

### 2. The ladder (03:30–05:23)
- "**The one higher time frame draw on liquidity** on whatever execution time frame I'm on": e.g. execute on the 5-minute, scale up to the 15-minute, and "find the first draw on liquidity within the direction that we're taking the trade". That's the first take profit (03:39–04:06).
- The second: e.g. a fair value gap. "I usually set like three or four take profits ... that's not really necessary; you can put that into your trading plan" (04:15–04:42).
- Even for 4-hour trades entered on the 15-minute: "since we're taking trades on lower time frames, I like to set take profits based on the execution time frame" (04:42–05:23).

### 3. Priorities (05:23–06:06)
- "Taking profits is one of the smallest things that you need to worry about": daily bias first, then execution, then stops, then take profits. "If you're getting a good execution point, odds are price is going to go in your favour." First take profits are mostly "one to one, one to one point five ... one to five".

### 4. Minimum 1:1 (06:13–08:33; frame at 07:15)
- S&P 4-hour: a sweep, a break up, a gap entry, stop below. "**Most of the time my first take profit is going to be minimum one to one, that's kind of the goal.**" The 1:1 lines up with a high (a draw on liquidity), so that's take profit 1. Then the next draw, then "another draw on liquidity all the way up here" (06:37–07:12). The frame shows four take-profit lines stacked at the highs above the entry box.
- Forex: a sweep + break, enter, "ideally just want a one to one". Take profits at the top of an imbalance, the base of a 4-hour order block, a 1-hour order block, then liquidity (07:21–08:05).
- "Just use your building blocks, because those are price magnets" (08:05–08:33).

### 5. A live trade (08:33–10:10; frame at 09:55)
- A 1-hour order block, a 5-minute break down, entry on a 1-minute order block.
- Take profit 1 = a 5-minute order block, "not based off of one minute confluences ... higher time frame holds higher power". Take profit 2 = right under the second draw on liquidity; take profit 3 = a 15-minute fair value gap.
- That trade was "closed for break even because price was taking forever" (08:37–08:41).

## Connections
- **Days 8–28:** the building blocks are the targets as well as the entries ("draws for price", Day 32).
- **Day 18:** several take profits and break even in the first examples.
- **Day 36:** "I take partials"; daily targets for bigger trades.
- **Day 38:** stops, the other half of the exit.

## Provenance audit
- **[TJR]**
  - Take profits at building blocks on the execution timeframe or one higher.
  - The first = the next higher-timeframe draw on liquidity in the trade's direction, minimum 1:1 "most of the time".
  - 3–4 take profits (the trader's choice).
  - Don't base take profits on 1-minute confluences.
  - Take profits matter least of daily bias, execution, stops, take profits.
- **[Bot]** (`exits.py`)
  - Three take profits, equal thirds, stop to break even after the first (from the Day 18 example).
  - Levels = untaken liquidity pools on both timeframes plus unfilled gap edges (order block edges not yet used).
