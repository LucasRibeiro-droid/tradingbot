# Order blocks (topic file: Days 20, 22, 24)

**Status: complete** (Day 20: what they are; Day 22: how to spot them; Day 24: putting it
together). One detail is still pending: which candle TJR's "wick to start of the body" box
applies to (screenshots requested). Order blocks are in the test harness as an alternative
continuation zone (`Continuation(zone="order_block")`), being compared with fair value gaps (H24).
Lesson notes: `day20_order_blocks_pt1.md`, `day22_order_blocks_pt2.md`, `day24_order_blocks_pt3.md`.
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
- The sweep is "almost always best" [Day 24, 09:52]: a softening of Days 20 and 22, where the block *is* the move that swept. "If you see a liquidity sweep and then a leg higher, you should assume there's going to be an order block there" [Day 24, 23:45].

## How to spot one [TJR Day 22]
1. Find a break of structure.
2. Ask what move came before it and swept liquidity: "where was the down move prior to the break of structure, where orders were filled?" [04:15].
3. Mark that whole move as the range [07:03]. Scale down to see it precisely [04:37, 08:12].

**How to box it [TJR Day 24]:**
- **Whole leg** ("your best bet", and what beginners should do) [10:15–10:26, 25:16–25:54].
- **TJR's own way:** "from the wick down to the start of the body", because price often reacts at the wick area or "the base of the body, right where the body starts", "just market experience" [10:38–11:49, 26:13]. Which candle's wick is not clear from the speech; see the open questions.

## What it's for [TJR]
- A **retracement tool**, with fair value gaps and equilibrium; liquidity sweep + break of structure is the start of the move [Day 20, 06:16–06:57].
- TJR's **first choice** for a retracement entry, then the fair value gap, then equilibrium [Day 20, 06:57–07:49].
- "Fair value gap for really **any** retracement, order block off the **first** retracement" [Day 24, 16:49–16:52].
- Also a **take profit** [Day 24, 13:39].
- Used when sweep + break gives poor reward-to-risk: "why wouldn't I wait for a potentially way better risk reward ratio" [Day 22, 25:11–25:29].

## Using one
- In every worked example, price retraced into the block, TJR **scaled down**, and entered on a **lower-timeframe break of structure** [Day 22, 12:41–13:40, 16:24, 20:20, 23:00–23:15]; sometimes on a gap filled inside the block [Day 22, 17:05].
- **Stop:** depends on the timeframe you're playing. A 4-hour block needs a stop beyond the whole block, not a tight 1-hour stop [Day 22, 09:15–09:59]. "Above the order block itself if you want to play safe" [Day 22, 23:21]; other examples put it under a recent low, "it doesn't really matter" [Day 22, 21:12].
- **Targets:** previous liquidity, on higher timeframes [Day 22, 09:57, 17:17, 23:26]; take profits along the way (an imbalance's 50%, the highs) [Day 22, 14:17].
- **Timing:** no trades pre-market; wait for the open (New York 9:30 in the GBPUSD example; London open in the 15-minute example) [Day 22, 12:50, 16:17–16:24].
- **Not every block gets reached:** "sometimes it's just not going to hit" [Day 22, 19:10].
- **Tap in, then a break of structure, then enter** [Day 24, 11:53–12:10, 13:06, 17:30]. Or skip the first break and enter on the next retracement into the block or a gap inside it, on a 15-minute break, for "crazy RR" [Day 24, 17:41–18:02].
- **A higher-timeframe block alone is not enough:** a daily block needs a 4-hour break, then an hourly break off the hourly block [Day 24, 21:00–21:44].
- **Bias:** "especially if it's in line with our daily and our weekly bias" [Day 24, 20:23].
- **Too big a range, or already inside it at the break:** scale down, or wait for "double confirmation" [Day 24, 23:12–25:10].
- Price can return to the same block more than once [Day 24, 14:45].

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

## Harness test: order blocks vs fair value gaps as the continuation zone (H24, 2026-10-21)
The same path as the fair value gap continuation (higher-timeframe zone in the trend's direction, retrace in, lower-timeframe break, after 9:30, stop at the retracement's extreme, target the nearest liquidity). The only change is the zone type.

| Chart | Gaps: n, avg R, median RR | Blocks: n, avg R, median RR |
|---|---|---|
| SPY 1Hour in 1Day (730d) | 33, −0.15, 0.42 | 10, −0.38, 0.44 |
| SPY 15Min in 4Hour (700d) | 118, −0.05, 0.46 | 25, **+0.34**, 0.66 |
| SPY 5Min in 1Hour (150d) | 63, +0.00, 0.34 | 18, −0.21, 0.54 |
| GLD 1Hour in 1Day (730d) | 41, +0.08, 0.22 | 8, −0.23, 0.68 |
| GLD 15Min in 4Hour (700d) | 134, +0.10, 0.57 | 28, +0.01, 0.86 |
| GLD 5Min in 1Hour (150d) | 83, −0.12, 0.55 | 19, **+0.12**, 0.76 |

- Order blocks gave a higher median reward-to-risk on 6 of 6 charts, as TJR says.
- Average R was better on 2 of 6. Samples are small (8–28 trades): inconclusive. Blocks are not promoted; the fair value gap path stays the baseline.
- Blocks produce far fewer trades (one per trend shift, versus many gaps).

## Contradictions and open questions
1. **"One order block per trend" vs "order blocks on every timeframe."** Likely resolved by timeframe: one per trend *on a given timeframe*. A lower-timeframe trend shift inside a higher-timeframe trend makes its own [Inferred].
2. **Whole move vs one candle.** Day 22: "on the four hour this was the candle ... relatively precise, but what was the entire move?" The whole move, scaled down for precision. Where exactly the move starts is not defined.
3. **Wicks or bodies** as the boundaries: not said.
4. **Stop:** beyond the whole block ("play safe") vs under a recent low ("doesn't really matter"). Day 38 teaches stops.
5. **Which open:** New York 9:30 in one example, London in another. Still open from Day 18 (for SPY/GLD the bot uses 9:30 New York).
6. **When a block stops counting:** Day 24 says blocks work "off the first retracement", yet shows price coming back a second time [14:45]. [Bot] uses a close beyond the sweep's extreme, and one trade per block.
9. **Sweep required?** Days 20/22: the block *is* the move that swept. Day 24: a sweep is "almost always best". The bot requires a sweep (`require_sweep=True`); the alternative is a one-variable test.
10. **"Wick to the start of the body": which candle?** Probably the candle at the leg's far end, where price returns first. Gemini's description of 10:13–10:35 contradicts itself; screenshots requested at 10:20, 10:45, 11:30.
7. **News days:** "don't trade" on PPI/FOMC days [Day 20, 11:41]. Not executable until Day 19 (news) is received.
8. [Bot note] Other teachers use "order block" for the *last opposite candle* before a move. TJR's definition is the whole leg that swept liquidity. The bot follows TJR and doesn't mix them.
