# Day 28 — Equilibrium, Part 2: on the chart

Source: TJR Boot Camp, Day 28: Equilibrium pt.2 (https://www.youtube.com/watch/-E7plUbSJUk, 20:59).
Studied from the uploaded video (360p) and the owner's captions
(`sources/day28_equilibrium_pt2.md`). I extracted and viewed frames myself at 01:30–17:40;
key ones are saved in `sources/day28_frames/`. Topic file: `equilibrium.md`.

**Classification:** part 2 of 2; **completes the equilibrium topic** (TJR: "I don't think we
need equilibrium part three", 19:50). Worked examples on S&P 500 (daily, 4-hour, 1-hour,
15-minute, 5-minute), GBPJPY and gold (monthly).

## What it teaches

### 1. Summary and how to draw it (00:59–03:46; frame at 02:20)
- "A retracement tool that allows us to measure a premium and a discount market for smart money to enter the market" (01:01–01:10).
- **Uptrend:** measure from the low to the high and find the 50 mark. Everything from 50% up is a **premium**; from 0.5 down to 0 is a **discount**, "where smart money would want to buy" (01:27–02:24).
- **Downtrend:** "we measure it from the high to the low" (02:43–02:49). The half near the low is a premium: "smart money is not looking to go short within here" but "when price gets on sale" (02:56–03:07).
- **Better than equilibrium alone:** "maybe there's a fair value gap within here ... maybe we have an order block, combined with the confirmation of it being in equilibrium. That's what equilibrium is used for: it's a retracement tool" (03:07–03:48).

### 2. Settings (03:51–05:12)
- A **Gann box** with only the levels 0, 0.5 and 1, or a Fibonacci with everything removed except those (03:57–05:12). The frames show the box drawn from wick to wick.

### 3. Which swing, and dragging it (05:33–09:40; frames at 05:50, 06:52, 08:22, 08:30)
- **S&P daily:** break of structure down, a new low. Price "pushes up above equilibrium", fills a fair value gap and takes liquidity, then falls. "When it comes into equilibrium, when it comes into that fair value gap, break of structure, enter; target previous areas of liquidity" (05:36–06:30).
- **Drag it when it isn't hit:** "the high down to this low, does it get hit? No ... so what do we drag this down to ... all the way down to here ... price comes into equilibrium" (06:40–07:04).
- **Equilibrium plus only a break of structure:** "to me that's not much confirmation", though it probably would have worked (07:20–07:36).
- **Every timeframe.** "There's a reason why people love using the 50 mark and the 61.8 on a Fibonacci for retracements ... it's equilibrium" (07:39–08:02).
- **S&P 5-minute:** "We break structure to the upside right here, boom, measure it low up to the high. Doesn't get hit on this move ... we go higher, perfect, we drag it higher." Price falls into equilibrium; scale down; a liquidity sweep, break of structure and an order block fill; break up → long; target liquidity (08:13–08:48). The 08:30 frame shows the box from the low before the break (its wick) up to the high.
- **New measurement after a hit:** "we form a low right here, does this get hit? No ... got to go higher, all the way up here; price finally comes down low enough", fills an imbalance, breaks up and rallies. TJR "literally caught a long off of this today", off an order block (09:01–09:43).

### 4. More examples (10:02–17:46)
- **GBPJPY:** lows, highs, equilibrium. An order block, or "accumulation, whatever"; on the 1-hour a break of structure but "we can't find a good enough entry, perfect, wait for it to come back down into equilibrium". On the 15-minute a break → long, stop under, targets liquidity (10:02–11:03).
- "It's literally just a retracement tool, nothing more than that ... an accurate representation of where price wants to retrace to" (11:07–11:21).
- **A gap aligning with equilibrium:** scale in, wait for a break of structure in that area, long (11:21–11:40). An hourly break, an imbalance and a higher-timeframe order block: "you're starting to see how we can piece all these things together" (11:52–12:12).
- **Gold monthly:** a monthly uptrend (break, retrace, break, retrace); measured monthly low to monthly high, "we're in equilibrium right now"; look for the gap and the order block in there, then scale down to the 4-hour for a break (13:25–13:59).
- **A Discord swing short** (frame at 16:15):
  1. Daily break of structure down, with the weekly also in a downtrend: "I was playing what the market was telling me".
  2. Daily equilibrium hit.
  3. On the 4-hour, price filled a massive imbalance.
  4. 1-hour break down → short, stop above.
  5. Four take profits at liquidity; three hit (15:17–16:31).
- Daily low → high, then an order block or gap in equilibrium, then a rally; "barely taps equilibrium, rallies higher" (16:37–17:46).

### 5. The rule, stated (18:18–18:46)
- "Whenever you see price make a new high in an uptrend, boom, drag it from the low up to the high. Whenever you see a new low made in a downtrend, we're dragging it from the high down to the low. Figure out where price will likely draw to, along with everything else we've learned."

### 6. What's next (19:04–20:40)
- No equilibrium part 3.
- Next: the **trading plan** as text (Day 29), then **putting everything together** parts 1–3 (Days 30, 32, 33).
- Maybe later: session opens, where to set stops and take profits.

## Issues
1. **"Discount" for shorts.** TJR says "smart money never shorts in a premium ... they always buy and short in a discount" (02:06–02:14), as on Day 26 (07:06). With "on sale" (03:07), this shows he uses **discount = a good price for the trade's direction**. For shorts that's the upper half of the swing. Not a mistake, his wording [Inferred]. The bot uses "depth ≥ 0.5 of the retracement" for both directions.
2. **Which low and high:** shown, not defined. The code follows the frames and the drag rule [Inferred]:
   - At the break, start from the extreme the move came from.
   - Drag the end while 50% isn't hit.
   - After a hit and a new extreme, start again from the dip.
3. **Wicks:** from the frames (06:52, 08:22) [Inferred]; 360p, so approximate.

## Connections
- **Day 26:** completes it. "Discount" is now clearly "good price for the trade". Shows the settings, the drag rule and examples.
- **Days 20–24:** equilibrium + order block; a higher-timeframe order block inside the discount.
- **Days 14–18:** a gap aligned with equilibrium is the favourite combination.
- **Day 4, Day 24:** the weekly/daily direction picks the side ("playing what the market was telling me").
- **Day 18:** several take profits at liquidity (four, three hit).

## Provenance audit
- **[TJR]**
  - 50% of the swing; below = discount for longs.
  - Measure low → high in an uptrend, high → low in a downtrend, and drag it as new extremes form.
  - Gann box or Fibonacci at 0 / 0.5 / 1.
  - A gauge: combine with a gap, block or break; equilibrium + break alone is "not much confirmation".
  - Every timeframe; scale down for the entry.
- **[Inferred]**
  - "Discount" for shorts = the upper half.
  - Where the measurement starts after a break; the restart after a hit; wicks.
- **[Bot]** `equilibrium.ranges()` encodes these; "reached the discount" = the retracement's extreme at or beyond 50%.
