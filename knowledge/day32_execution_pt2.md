# Day 32 — Execution, Part 2: entry models 1 and 2 on the chart

Source: TJR Boot Camp, Day 32: Execution pt.2 (https://www.youtube.com/watch/SLhIA7vW9x8, 23:38).
Studied from the uploaded video (240p) and the owner's captions
(`sources/day32_execution_pt2.md`). Frames viewed at 05:04, 06:28, 11:00, 11:22, 15:20, 16:03.
At 240p the boxes and entry points are visible but prices aren't; the lesson is about
*where* to execute, so that's enough. Two frames are saved in `sources/day32_frames/`.
Topic file: `execution.md`.

**Classification:** part 2 of 3 of execution.
- Day 32: models 1 and 2 (sweep + break; sweep + break + order block).
- Day 33: models 3 and 4 (+ fair value gap; + gap or block + equilibrium) (01:33–02:00, 23:17–23:31).

The topic stays open until Day 33.

## What it teaches

### 1. Framing: the base strategy only (02:11–06:56)
- "This is not the end-all be-all, we have to take a bunch of other things into account ... this is literally just giving you the base strategy" (02:23–02:37). "This itself will not make you profitable" (03:54).
- Daily bias (a two-part series, maybe with live trading), stops and take profits come later. "This isn't showing how to set stop losses, this isn't showing how to take profit, this is literally just showing where to execute" (04:13–04:30, 06:42–06:56).
- On a sweep then a break: "this is where daily bias will come in handy ... you're not ready" to place lots of trades yet (06:05–06:18).

### 2. Model 1: liquidity sweep + break of structure (04:36–10:20; frames at 05:04, 06:28)
- Examples: liquidity under the lows; one sweep without a break (no trade), then a sweep with a break → "this is an **execution point**". Price then draws to previous areas of liquidity (04:43–05:18).
- "The simplest, but also ... the riskiest, the lowest confluence" (05:28–05:42).
- Building blocks are also targets: "our building blocks are essentially draws for price"; e.g. target the top of an imbalance or the highs (07:04–07:47).
- **Homework:** "find 10 examples of a liquidity sweep and break of structure and just look at what happens afterwards" on any pair. "This is just building confidence" (08:05–08:20, 09:26–09:40).

### 3. Model 2: liquidity sweep + break of structure + order block (10:20–20:30; frames at 11:00, 11:22, 15:20, 16:03)
- "What was the candle that caused these highs to get taken out? This ... this candle right here is the candle that filled those orders" (10:54–11:14). The 11:00 frame shows a box over a **single** tall up candle that took the highs. At 16:03 it's a whole leg. So the block is one candle or a leg, whichever made the sweep (Days 22, 24).
- **Where to execute: "Not on the break of structure down here. We're executing when it comes into the order block"** (11:19–11:26). Repeated in every example: "when price comes into the order block, execute" (11:58–12:00, 13:12–13:15, 13:45–13:52).
- "Doesn't matter if it's exact or not" (15:24). The break candle itself can be the entry: "we break structure with this candle, on this candle's down wick into this order block, that's where we execute" (15:13–15:30). "Your break of structure candle, it's right here; this is where you're going to want to enter anyways" (16:01–16:06).
- **Not every block is reached:** "oh, this order block didn't get touched" (12:31).
- Shown on S&P (5-minute), GBPUSD (including a daily example), with a fair value gap inside one block (16:15).
- **Homework:** 10 examples of sweep + break + order block entry, and what price does after (12:04–12:07, 20:38–20:50). "Do as many as possible until it's literally just so robotic", like an aimbot (20:50–22:06). Without this, "we can't move on to daily bias ... take profits" (21:36–21:47).

## What this settles
1. **Model 2 enters on the touch.** No lower-timeframe break and no reaction candle needed: "executing when it comes into the order block". It settles Day 30's open point, and it agrees with Day 26 ("instantly entering when that price point gets hit"). The lower-timeframe break in Days 22 and 24 was a way of getting extra confirmation or a tighter stop, not a requirement [Inferred].
2. **Model 1 enters at the break of structure** ("this is an execution point" at the break, 05:02).

## The homework, by the bot
The bot already did this homework on 2026-10-21 (`orderblock_study.py`, H23) across SPY and GLD, daily, 1-hour and 15-minute, 37–67 blocks each. The setups and exits:
- **Model 1:** sweep + break, enter at the break's close.
- **Model 2:** sweep + break, enter when price comes back to the order block.
- **Exits:** the same for both. Stop beyond the block (Day 30: "stops above the highs"); target the nearest liquidity.

**What price did after:**
- **Continuation:** after price reached the block, it went past the move's extreme before closing back through the block 57–68% of the time.
- **Model 2's reward-to-risk:** higher on 6 of 6 charts (median 1.27–1.90 vs 1.02–1.59).
- **Model 2's average result:** better than model 1 on only 1 of 6. Model 1 ranged from −0.18R to +0.20R; model 2 from −0.14R to +0.10R per setup.

So in the bot's data, entering at the block gives the better reward-to-risk TJR promises, but the win rate drops by more than enough to cancel it. TJR's Day 30 risk ladder says model 2 is safer; the data so far don't show that (H29). Exits are fixed here (one target, no partials). Daily bias, stops and take profits, which TJR says still matter, aren't applied yet.

## Connections
- **Day 30:** models 1 and 2, now with examples; settles model 2's entry.
- **Days 20–24:** the block is the candle or leg that made the sweep; not every one is reached.
- **Days 26, 30:** entering on the hit.
- **Day 3:** robotic repetition builds confidence; the homework is drilling, not new rules.
- **Days 34–39:** daily bias, take profits and stops are what turn the base strategy into trades.

## Provenance audit
- **[TJR]**
  - Model 1 executes at the break.
  - Model 2 executes when price comes into the block, not at the break; it doesn't need to be exact; the break candle's wick can be the entry.
  - Some blocks aren't reached.
  - Building blocks are also draws/targets.
  - This is the base strategy; daily bias, stops and take profits come later.
  - Homework: 10 examples of each.
- **[Inferred]** The lower-timeframe break in Days 22/24 was optional extra confirmation.
- **[Bot]** The bot's homework uses its own detector, stop beyond the block, one liquidity target.
