# Day 33 — Execution, Part 3: entry models 3 and 4 on the chart

Source: TJR Boot Camp, Day 33: Execution pt.3 (https://www.youtube.com/watch/K8DwhtmvAW8, 24:00).
Studied from the uploaded video (144p) and the owner's captions
(`sources/day33_execution_pt3.md`). Frames viewed at 07:10, 15:08, 16:55, 22:36, 22:52. At
144p the boxes and the shape of the moves are visible, but not candles or prices; the
teaching is in the speech, so no screenshots were needed. Two frames are in
`sources/day33_frames/`. Topic file: `execution.md`.

**Classification:** part 3 of 3; **completes the execution topic.** Off-topic: 00:00–06:30
(chat, a sponsor).

## What it teaches

### 1. Model 3: sweep + break of structure + fair value gap (06:30–13:58; frame at 07:10)
- **S&P 15-minute, the same day** ("I didn't trade today because Powell was speaking"):
  - Lows taken, a 15-minute break up, an imbalance.
  - "This was not an order block entry, this was a fair value gap entry."
  - "What do you usually do? You scale down to a lower time frame to find confirmation ... maybe you got your confirmation off of this break of structure."
  - Stop "under this low or under these lows; we haven't covered that yet" (06:52–07:44).
- "Price comes in here, fills this imbalance. **What are we waiting for? Some sort of reaction on a lower time frame** ... break of structure on the 15-minute ... close above, execute" (09:41–10:05).
- A gap price runs straight through is dropped: "goes all the way past it, perfect, get rid of it" (09:30–09:35; Day 18).
- One example has no sweep: "we don't necessarily see liquidity get swept but we see a break of structure" (11:27–11:33). Another: the move down was itself the sweep and became an order block, then the gap (12:01–12:16).
- "Seeing an imbalance get filled, there's going to be some sort of reaction, with confirmation, with break of structure" (13:48–13:55).
- **Homework:** 10 examples of sweep + break + gap, and the reaction after (11:01–11:25).

### 2. Model 4: + equilibrium (13:58–23:18; frames at 15:08, 16:55, 22:52)
- "It's literally the same thing ... we're just drawing equilibrium onto it" (14:07–14:19).
- "When you start seeing a retracement candle, when you see a down candle, I'm instantly looking for equilibrium. Where's our equilibrium? **Matching up perfectly with our fair value gap** ... that's a high confluence trade ... enter here" (14:52–15:18). Frame 15:08: the box from the swing low to the high, with its 0.5 line through the gap's box.
- Daily example: sweep, break, gap; "we see one bearish daily candle, boom, we instantly draw this out" (16:31–17:01).
- "**Equilibrium and fair value gaps are kind of like our last chance entries**" (19:14–19:17), after the break and the order block.
- **Stacked confluences** (22:14–23:18; frame at 22:52): sweep, break, the whole leg as an order block, a wick into equilibrium, a 5-minute order block, a 5-minute gap, a break of structure. "Seven confluences ... build up the confidence ... you shouldn't be afraid to spam that buy button."
- **Homework:** 10 examples of model 4 too (20:57–21:04).

### 3. Daily bias is next, and why (17:52–18:22, 23:27–23:55)
- Order: daily bias → take profits → stop losses → a check-in.
- "Maybe you see liquidity sweep, break of structure ... on a lower time frame, but **if it's not in line with our daily bias ... odds are that run will be relatively short-lived** ... that move might not hit your first take profit."

## What this settles
- **Model 3 enters on a reaction:** wait for a reaction or a lower-timeframe break of structure inside the gap (Days 16, 18). Model 2 enters on the touch (Day 32). So: **order blocks on the touch, fair value gaps on confirmation.**
- **Model 4 = model 2 or 3 inside the discount**, best when equilibrium lines up with the gap or block.
- **Execution is complete.** Still to come: daily bias (Days 34–36), take profits (37), stops (38).

## The homework, by the bot: all four models on the same setups (`models_study.py`, 2026-10-21)
For every sweep + break of structure (the order block's leg took a liquidity pool, then structure broke), the bot ran all four entries:
1. **Model 1:** at the break's close.
2. **Model 2:** on the touch of the block. If price is already inside the block at the break, at the break (Day 32, 16:01).
3. **Model 3:** on a reaction candle inside a gap in the new direction [one timeframe; TJR also scales down].
4. **Model 4:** model 2 or 3, but only where the entry is in the discount (depth ≥ 0.5).

All four use the same stop (beyond the sweep: "stops above the highs") and target (the nearest liquidity). An entry that never comes counts as no trade. The results, as win rate / average R per trade / median reward-to-risk:

| Chart (setups) | Model 1 | Model 2 | Model 3 | Model 4 |
|---|---|---|---|---|
| SPY 1Day (37) | 49% / −0.18 / 1.02 | 41% / −0.17 / 1.43 | 59% / **+0.06** / 0.75 | 33% / +0.01 / 2.62 |
| SPY 4Hour (43) | 51% / −0.22 / 0.75 | 45% / **−0.18** / 1.16 | 36% / −0.46 / 0.62 | 31% / −0.23 / 2.31 |
| SPY 1Hour (67) | 43% / −0.04 / 1.18 | 36% / −0.08 / 1.51 | 46% / +0.11 / 1.28 | 37% / **+0.31** / 2.35 |
| SPY 15Min (55) | 47% / **+0.03** / 1.25 | 36% / −0.05 / 1.57 | 38% / −0.29 / 0.91 | 26% / −0.18 / 2.35 |
| GLD 1Day (44) | 48% / **+0.12** / 1.59 | 38% / −0.06 / 1.90 | 44% / +0.06 / 1.44 | 27% / −0.12 / 2.11 |
| GLD 4Hour (34) | 47% / +0.19 / 1.23 | 38% / +0.08 / 1.66 | 50% / **+0.35** / 1.38 | 38% / +0.33 / 2.20 |
| GLD 1Hour (62) | 47% / +0.10 / 1.14 | 35% / +0.00 / 1.57 | 56% / **+0.38** / 1.60 | 24% / −0.05 / 2.07 |
| GLD 15Min (56) | 48% / +0.20 / 1.09 | 42% / +0.12 / 1.27 | 43% / +0.23 / 1.37 | 24% / **+0.29** / 2.59 |

**What the data say:**
- **The risk ladder, read as "wins more often", is not supported** (H29). Model 4 has the *lowest* win rate on 7 of 8 charts. Its entries are deeper, so it has the highest reward-to-risk on 8 of 8 (median 2.07–2.62) and needs fewer wins.
- **No model wins everywhere** on average R per trade:
  - Model 3 is best on 3 charts.
  - Model 1 on 2.
  - Model 4 on 2.
  - Model 2 on 1, and only because all four lost there.
- **Model 3 (gap + reaction) is the most consistent:** positive on 6 of 8 charts.
- **Model 2 (block on the touch) is the weakest per trade:** positive on only 2 of 8. Confirmation seems to matter: an unconfirmed touch loses more often than its better price pays for (also H23, H17).
- **Caveats:**
  - Small samples (12–67 trades per model per chart).
  - One target, no partials.
  - No daily bias. TJR says setups against it are "short-lived", and daily bias is the very next lesson.

## Connections
- **Days 30, 32:** completes the four models.
- **Days 16, 18:** gap entries need a reaction or a lower-timeframe break; a gap price runs through is dropped.
- **Days 26, 28:** equilibrium lined up with the gap is "high confluence".
- **Days 20–24:** an order block inside the move; the whole leg as the block.
- **Day 4:** higher timeframes outrank lower; daily bias next.

## Provenance audit
- **[TJR]**
  - Model 3 waits for a reaction or a lower-timeframe break inside the gap.
  - A gap price runs through is dropped.
  - Model 4 = the same with equilibrium; best when equilibrium lines up with the gap.
  - Gaps and equilibrium are "last chance entries".
  - Stacking confluences builds confidence.
  - Setups against the daily bias are short-lived.
  - Next: daily bias, take profits, stops.
  - Homework: 10 examples of each.
- **[Inferred]** Order blocks on the touch, gaps on confirmation (Days 32 + 33).
- **[Bot]** `models_study.py`: one timeframe, a reaction candle as the confirmation, same stop and target for all models, no trade = 0R.
