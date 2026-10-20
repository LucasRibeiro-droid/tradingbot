# Day 16 — Fair Value Gaps, Part 2: how to identify them

Source: TJR Boot Camp, Day 16: FVG Pt. 2 (https://www.youtube.com/watch?v=S1kY3Fw6JUQ, 12:40).
Studied from the uploaded video (480p, 12:39) and the captions the owner provided (tactiq);
charts checked from frames. Topic file: `fair_value_gaps.md`.

**Classification:** part 2 of 3 of the fair value gap topic. Expands Day 14 with the
identification rule and a usage constraint. Part 3 (Day 18) will cover taking trades with
gaps together with liquidity sweeps and break of structure (01:12–01:21).

## What it teaches
1. **Recap** of Day 14: a liquidity void, no resting orders opposing price's direction; price draws back into it and reacts [00:01:55–00:02:56].
2. **Not for reversals.** Gaps are a retracement and continuation tool. In a bullish market (higher highs, higher lows), look for retracements into **bullish** gaps, not bearish gaps to turn price [03:22–04:05]. Equilibrium is the same kind of tool [04:01].
3. **Identification:** a three-candle pattern; bullish = top of candle 1's wick to bottom of candle 3's wick; bearish = bottom of candle 1's wick to top of candle 3's wick; candle 2 is the full candle that creates the imbalance [04:12–05:45, 06:41–06:57, 11:26–11:55].
4. **What's not a gap:** wicks of candles 1 and 3 overlapping, because price already traded through and the wicks show resting orders [09:41–11:13].
5. **Examples:** bullish gap after a confirmed break of structure up; price draws in, chops, breaks structure, rallies [05:56–06:28]. Bearish gap after a break of structure down; retrace, fill, drop [06:41–07:15].
6. **Caution:** "it isn't as valuable as you may think"; gaps are everywhere and not all work. Don't execute purely on a gap being hit. Wait for a reaction (a bullish or bearish candle) or a lower-timeframe break of structure / market structure shift as confirmation. Be patient [07:15–08:41].
7. **Homework:** on one instrument, identify 10 gaps and write a hypothetical way to trade each; also learn to recognize the ones that aren't real [08:46–09:28, 12:06–12:21]. TJR's example: break down, bearish gap filled with a bearish close, enter, stop above the previous high, target the previous lows. "We're not even at the point of being able to execute" [09:28].

## Connections
- **Day 14:** same concept; this adds the exact rule and the "not reversals" constraint.
- **Day 6:** a break of structure confirms the bias before looking for gaps, and a lower-timeframe break confirms the entry.
- **Day 4:** trade with the trend; gaps follow the trend.
- **Days 8–12:** liquidity is the reversal tool; gaps are the continuation tool. Day 12's targets (previous lows) reappear in the homework example.
- **Day 2:** a reaction candle (closing in the trend's direction) is a candle read used as confirmation.
- **Day 26, 28 (equilibrium):** previewed as the same kind of tool.

## What changed in the knowledge base
- Fair value gap identification is now explicit [TJR] and implemented (`tradingbot/fvg.py`).
- New exception: gaps are not used for reversals.
- New confirmation rule: reaction candle or lower-timeframe break before acting.
- New open questions: what "filled" means, when a gap stops counting, overnight gaps on stocks.

## Provenance of the code
- **[TJR]** The three-candle rule, the zone boundaries, the overlapping-wicks exclusion, the direction constraint, the reaction requirement.
- **[Inferred]** Candle 2 must close in the gap's direction (TJR's drawing and examples; also excludes stock overnight gaps where candle 2 moved the other way).
- **[Bot]** "Entered" = a wick touches the zone; "reacted" = a candle that traded in the zone closes in the gap's direction; "broken" = a close beyond the far side; the study's continuation measure.
