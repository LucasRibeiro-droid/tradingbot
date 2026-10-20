# Day 18 — Fair Value Gaps, Part 3: putting it together

Source: TJR Boot Camp, Day 18: FVG Pt. 3 (https://www.youtube.com/watch?v=qecF411R83s, 17:47).
Studied from the uploaded video (480p, 17:46) and the captions the owner provided (tactiq);
charts checked from frames. Topic file: `fair_value_gaps.md`.

**Classification:** part 3 of 3; **completes the fair value gap topic.** A recap plus worked
trades that combine everything taught so far: trend, liquidity sweep, break of structure,
fair value gap. TJR: "it's no longer 'this is what a liquidity sweep is' ... now that you
have these concepts I'm going to move forward as if you fully understand them" (01:11–01:29).

## What it teaches

### 1. TJR's live trade: a timeframe cascade (01:51–04:52; frames at 02:25, 04:30)
- S&P 500: a small uptrend, then a **break of structure down on the 15-minute**. Of the imbalances it left, only one is a real gap; the others are ruled out because wicks overlap (02:12–02:27).
- Price retraces into it during **pre-market** and breaks structure, but "we're not even looking at this ... we're not going to take any trades that aren't off of market open or after market open" (03:01–03:19).
- After the open, price pushes up into **another (5-minute) imbalance**. "Two confirmations": the higher-timeframe break (trend shift), and the higher-timeframe imbalance filled. Then scale down for a break of structure, and scale down again (1-minute) for "a prime time entry": a break of structure on a candle close → short (03:36–04:33).
- Targets: liquidity below, and "a little ... order block". **Both take profits hit before the rest of the position was stopped out at break even** (04:33–04:48).

### 2. Why gaps exist in the process: the patient entry (04:52–05:47)
- Not entering when price reaches the gap, and not entering on the first break alone: "we would have got stopped out".
- "I really like to use these as my patient entry." After a liquidity sweep and a break of structure, if the market dumps and "doesn't give us a good risk reward", wait for a retracement into a gap, scale down, and find a break of structure confirming continuation.

### 3. GBPJPY: sweep, break, gap, lower-timeframe break (05:57–08:19; frame at 07:15)
- Higher-timeframe highs swept; 15-minute break of structure; several gaps, mark them all.
- A **5-minute break up** inside a 15-minute and 1-hour downtrend "doesn't mean complete trend shift ... we'll probably be retracing on the 15 minute": a lower-timeframe break against the higher timeframes is a retracement (reinforces Day 6, 22:13).
- First gap filled → 5-minute break down → short, **stop above these highs**, targets **previous areas of liquidity**, an **accumulation** area, liquidity further down. TJR's position tool on screen: reward-to-risk 1.86.
- "Literally three simple concepts: liquidity sweep, break of structure, imbalance fill, break of structure."

### 4. Gold: when a gap stops counting, and gap + liquidity together (09:02–11:00; frames at 09:48, 10:36)
- 4-hour break of structure, two gaps. Price rallies **through and past** the first: "the second we push past this, no longer considering it."
- The second gap (1967.36–1973.97) has **liquidity lying right in line with it**: "break of structure on the four hour along with the imbalance, this looks perfect." Price spikes into the liquidity, 15-minute break of structure, short.
- Targets offered: previous liquidity, the accumulation that caused the rally, or the gap's start, **50%**, or end.

### 5. GBPUSD: refine the gap on a lower timeframe (11:04–15:02; frame at 12:57)
- Daily break of structure up (bullish), 1-hour break up. Price retraces. A 4-hour gap exists, but a **1-hour wick already fills part of it**, so TJR prioritizes the 1-hour gap: "this isn't even an imbalance ... where's the imbalance actually ... from this wick to here."
- On the 15-minute: ideally liquidity taken inside the gap first; a **doji** shows indecision (Day 2); no break, no break, no break, then a break of structure (the hourly breaks too) → long. First take profit missed, a dip back into the gap, then the rally takes out previous liquidity and fills an imbalance above.

### 6. What gaps really are to TJR (15:16–16:11)
- "Obviously it's easier to do in hindsight, which is why we got to practice ... watching these happen live."
- "I don't even really like taking a lot of trades off of imbalances. To me imbalances are mainly used for retracement tools ... then from there I find other reasoning: an order block, a break of structure, a liquidity sweep within an imbalance then a break of structure. **I use it as more of a confirmation rather than an entry.**"

### 7. What comes next (16:20–16:54)
- Liquidity sweeps, break of structure, fair value gaps: done. Next: **order blocks** (part 1 explain, part 2 spot, part 3 put together), then **equilibrium**, then **strategy**. Also previewed: market open's value, accumulation and distribution.

## Connections
- **Days 14, 16:** completes the topic; resolves "when does a gap stop counting" (price pushing past it) and shows "secondary entry" in practice (the patient entry after a sweep and break).
- **Day 4:** timeframe hierarchy, now a cascade (15m → 5m → 1m; 4h → 15m; daily → 1h → 15m).
- **Day 6:** a lower-timeframe break against the higher timeframes is a retracement.
- **Days 8–12:** sweep and break first; targets at liquidity; liquidity in line with a gap adds confluence.
- **Day 2:** a doji inside the gap as indecision before the break.
- **Day 7:** pick the pieces that give you confirmations.

## Provenance of the harness's continuation path (`decision.Continuation`)
- **[TJR]** Gap in the higher timeframe's direction; wait for price to retrace into it; lower-timeframe break of structure in the trend's direction as the trigger; stop beyond the retracement's extreme; target previous liquidity; no trades before the market opens; a gap price pushes past is dropped.
- **[Bot]** "Pushes past" = a lower-timeframe close beyond the far side; "entered" = a wick touching the zone; one decision per gap; entry at the break candle's close; one target and no partials (TJR used several targets, partial profits and a break-even stop).
