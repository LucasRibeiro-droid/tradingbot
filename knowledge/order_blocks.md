# Order blocks (topic file: Days 20, 22, 24)

**Status: incomplete.** Day 20 (what they are) and Day 22 (how to spot them) are learned;
Day 24 (putting it together) hasn't been received. Nothing here is an executable rule yet:
order blocks are **not** in the decision harness until Day 24.
Lesson notes: `day20_order_blocks_pt1.md`, `day22_order_blocks_pt2.md`.
Code: `tradingbot/orderblocks.py` (detection, read-only), `tradingbot/orderblock_study.py` (homework).

## What it is [TJR]
- The **move that caused the liquidity sweep**, before the break of structure that shifts the market [Day 20, 03:10; Day 22, 02:36–02:46].
  - Before a break **down**: the leg **up** that took the highs. Price later retraces up into it, and it's where shorts are looked for.
  - Before a break **up**: the leg **down** that took the lows. Longs.
- That price range is where orders were filled; when price comes back, more orders can be filled there, and price continues in the new direction [Day 20, 04:37–06:09; Day 22, 02:08–02:30].
- It's **the whole move**, which can be several candles; on a higher timeframe it may look like one candle [Day 22, 07:03–08:15].
- **One per trend**: it forms at the trend shift; the next one forms at the next shift [Day 20, 07:53–08:52].
- Exists on **every timeframe**; easier to find on lower ones [Day 20, 09:23; Day 22, 03:49].
- **Order block = accumulation area** [Day 20, 11:08–11:18].

## How to spot one [TJR Day 22]
1. Find a break of structure.
2. Ask what move came before it and swept liquidity: "where was the down move prior to the break of structure, where orders were filled?" [04:15].
3. Mark that whole move as the range [07:03]. Scale down to see it precisely [04:37, 08:12].

## What it's for [TJR]
- A **retracement tool**, with fair value gaps and equilibrium; liquidity sweep + break of structure is the start of the move [Day 20, 06:16–06:57].
- TJR's **first choice** for a retracement entry, then the fair value gap, then equilibrium [Day 20, 06:57–07:49].
- Used when sweep + break gives poor reward-to-risk: "why wouldn't I wait for a potentially way better risk reward ratio" [Day 22, 25:11–25:29].

## Using one (examples so far; Day 24 still to come)
- In every worked example, price retraced into the block, TJR **scaled down**, and entered on a **lower-timeframe break of structure** [Day 22, 12:41–13:40, 16:24, 20:20, 23:00–23:15]; sometimes on a gap filled inside the block [Day 22, 17:05].
- **Stop:** depends on the timeframe you're playing. A 4-hour block needs a stop beyond the whole block, not a tight 1-hour stop [Day 22, 09:15–09:59]. "Above the order block itself if you want to play safe" [Day 22, 23:21]; other examples put it under a recent low, "it doesn't really matter" [Day 22, 21:12].
- **Targets:** previous liquidity, on higher timeframes [Day 22, 09:57, 17:17, 23:26]; take profits along the way (an imbalance's 50%, the highs) [Day 22, 14:17].
- **Timing:** no trades pre-market; wait for the open (New York 9:30 in the GBPUSD example; London open in the 15-minute example) [Day 22, 12:50, 16:17–16:24].
- **Not every block gets reached:** "sometimes it's just not going to hit" [Day 22, 19:10].

## How the bot finds one (`orderblocks.find_blocks`)
At each break of structure (`trend.py`, which only marks trend shifts, so one block per shift):
- **The leg's extreme:** the highest high (before a break down) since the previous break [Inferred].
- **The leg's start:** the most recent two-candle low before that extreme [Bot]. TJR boxes "the whole move" by eye.
- **The range:** wick to wick [Bot]; TJR hasn't said whether wicks or bodies bound it.
- **The sweep:** the leg must have taken a liquidity pool from `liquidity.py` [TJR: the move that swept liquidity; pools are themselves Bot-approximated].
- **Follow-up** (`follow_block`): "entered" = a wick reaches the block; "reacted" = a candle closes in the block's direction there; "broken" = a close beyond the sweep's extreme [Bot].
  - Same tests as fair value gaps. TJR hasn't said when a block stops counting.
- A break up mirrors all of this.

## Homework study (2026-10-21, SPY and GLD, 1Day/1Hour/15Min)
`python -m tradingbot.orderblock_study SYMBOL --timeframe TF --days N`; results in `journal/studies/day22_orderblocks_*.json`.

**Price comes back to the block** [TJR claim]:
- Price reached the block before breaking it in 96–100% of blocks (e.g. SPY 1-hour: 71 of 71; GLD daily: 44 of 46).
- This is mostly by construction: the block's near edge is about the level the break closed past, so a small pullback reaches it.

**Continuation after the retrace** (passing the move's extreme before closing beyond the block):
- 57–68% on all six charts.
- Fair value gaps after a plain entry, on the four charts both studies cover: 38–46%.
- This supports TJR's ranking (block first) on 4 of 4 charts.
- Partly by construction: the block's far side is the sweep's extreme, farther away than a gap's far side.

**Waiting for the block vs entering on the break** (same stop beyond the block, same liquidity target):

| Chart | Break: avg R | Block: avg R per block | Break: median RR | Block: median RR | Blocks filled |
|---|---|---|---|---|---|
| SPY 1Day | −0.18 | −0.14 | 1.02 | 1.43 | 32/37 |
| SPY 1Hour | −0.05 | −0.07 | 1.18 | 1.51 | 59/67 |
| SPY 15Min | +0.03 | −0.04 | 1.25 | 1.57 | 44/55 |
| GLD 1Day | +0.12 | −0.05 | 1.59 | 1.90 | 37/44 |
| GLD 1Hour | +0.10 | 0.00 | 1.14 | 1.57 | 51/62 |
| GLD 15Min | +0.20 | +0.10 | 1.09 | 1.27 | 48/56 |

- Waiting gave a better reward-to-risk on 6 of 6 charts, as TJR says.
- But it gave a better average result on only 1 of 6. A bare limit order at the block loses more often than the better ratio pays for.
- TJR never entered on the touch alone: he waited for a lower-timeframe break inside the block. That test (H24) needs Day 24.

## Contradictions and open questions
1. **"One order block per trend" vs "order blocks on every timeframe."** Likely resolved by timeframe: one per trend *on a given timeframe*. A lower-timeframe trend shift inside a higher-timeframe trend makes its own [Inferred].
2. **Whole move vs one candle.** Day 22: "on the four hour this was the candle ... relatively precise, but what was the entire move?" The whole move, scaled down for precision. Where exactly the move starts is not defined.
3. **Wicks or bodies** as the boundaries: not said.
4. **Stop:** beyond the whole block ("play safe") vs under a recent low ("doesn't really matter"). Day 38 teaches stops.
5. **Which open:** New York 9:30 in one example, London in another. Still open from Day 18 (for SPY/GLD the bot uses 9:30 New York).
6. **When a block stops counting** (price closing through it?): not taught; [Bot] uses a close beyond the sweep's extreme.
7. **News days:** "don't trade" on PPI/FOMC days [Day 20, 11:41]. Not executable until Day 19 (news) is received.
8. [Bot note] Other teachers use "order block" for the *last opposite candle* before a move. TJR's definition is the whole leg that swept liquidity. The bot follows TJR and doesn't mix them.
