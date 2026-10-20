# Fair value gaps (topic file: Days 14, 16, 18)

**Status: incomplete.** Part 1 (Day 14: what and why) and Part 2 (Day 16: how to identify)
are learned. Part 3 (Day 18: how to trade them with liquidity sweeps and break of
structure, per Day 16, 01:12–01:21) is not received yet. Nothing here is final.
Lesson notes: `day14_fair_value_gaps_pt1.md`, `day16_fair_value_gaps_pt2.md`.
Code: `tradingbot/fvg.py` (detection only; not used in decisions until Day 18).

## What it is [TJR]
- Fair value gap = liquidity void = imbalance [Day 14, 02:02; Day 16, 01:57].
- A price range with **no resting orders opposing** the direction price moved, so price went through it fast, usually as one big candle [Day 14, 02:22–03:04; Day 16, 01:59–02:06].
- The opposite of liquidity: liquidity is where orders rest; a void is where they don't [Day 14, 02:08–02:25].

## How to identify one [TJR Day 16]
- A **three-candle pattern**. Candle 2 is "the candle that creates the imbalance", "super full" [04:12–04:30].
- **Bullish:** the zone runs from the **top of candle 1's wick** to the **bottom of candle 3's wick** [05:15–05:30].
- **Bearish:** from the **bottom of candle 1's wick** to the **top of candle 3's wick** [06:41–06:57, 11:41–11:51].
- **Not a gap** if the wicks of candles 1 and 3 overlap: price already traded there, the void is filled, and the wicks show resting orders [09:41–11:13].
- "You literally just look for areas that do not have wicks covering it" [06:30].
- Draw a box over the zone, wait for price to fill it, wait for a reaction [05:39–05:45].
- Bot: `find_gaps()`, exactly this, plus one [Inferred] condition: candle 2 must close in the gap's direction.

## What it's for [TJR]
- **Retracements and continuations, not reversals** [Day 16, 03:22–04:05]. In an uptrend (higher highs and higher lows, confirmed by a break of structure), look only for **bullish** gaps that price retraces into, not bearish gaps to turn price around.
- Fair value gaps and equilibrium are both continuation and retracement tools [Day 16, 04:01] (equilibrium: Days 26, 28).
- Liquidity sweeps tell where the market is going; fair value gaps tell where a retracement goes, or give a "secondary entry" [Day 14, 03:52–04:22].
- Unfilled gaps are also places to take profit [Day 12, 13:55].

## Using one (as far as taught)
- **Never act on price simply reaching a gap.** Wait for a **reaction** (a candle closing in the trend's direction) or scale down to a **lower timeframe** for a break of structure / market structure shift, and let that be the confirmation [TJR Day 16, 07:58–08:41].
- They're everywhere on the chart and "not all of them are going to work", which is why confirmation is needed. "Be very patient with these" [TJR Day 16, 07:26–08:41].
- Higher-timeframe gap + lower-timeframe break of structure in the trend's direction [TJR Day 14, 04:28; Day 16, 12:01, S&P 4-hour then lower timeframe].
- TJR's homework example (Day 16, 09:13–09:28): break of structure down; bearish gap; price fills it and closes bearish; enter; stop above the previous high; target the previous lows. He adds: "we're not even at the point of being able to execute yet; we're still putting the pieces together." **An example, not a rule.**

## Chart examples (frames checked)
- 05:40: TJR's drawing of the three candles with the box from candle 1's wick to candle 3's.
- 06:20: S&P 4-hour, bullish gap (~4165–4195), price retraces in, chops, breaks structure, rallies.
- 07:05: S&P daily, bearish gap (February 2023), price fills it and drops.
- 09:28: S&P weekly, a 2022 bearish gap that price is reaching into.
- 12:04: S&P 4-hour (September 2022), large bearish gap; price rallies into it; scale down for the break of structure.

## What the bot found (2026-10-20)

`python -m tradingbot.fvg_study SYMBOL --timeframe TF`, about 480–1,250 gaps per chart on
SPY and GLD (daily, 4-hour, 1-hour). Outcome [Bot measure]: did price go past the extreme
of the move that left the gap before closing beyond the gap's far side?

| Chart | After price entered the gap | After a reaction candle | With trend vs against (after reaction) |
|---|---|---|---|
| SPY daily | 41.5% | 57.3% | 62.4% vs 50.0% |
| GLD daily | 40.5% | 55.5% | 53.3% vs 52.8% |
| SPY 4-hour | 42.1% | 60.1% | 58.3% vs 44.7% |
| GLD 4-hour | 37.7% | 54.5% | 57.9% vs 43.8% |
| SPY 1-hour | 39.4% | 59.8% | 56.9% vs 62.5% |
| GLD 1-hour | 39.2% | 58.8% | 59.4% vs 56.9% |

- **Waiting for a reaction: supported on all 6 charts** (about +15–20 points). Part of this is built in (a gap that fails right away never gets a reaction), but filtering out those failures is exactly what waiting does.
- **With the trend beat against it on 4 of 6 charts** (clearest on the 4-hour: SPY +13.6, GLD +14.1 points), even on 1, reversed on SPY 1-hour. Supports "not for reversals", not yet conclusive.

## Open questions
1. What counts as "filled": touched, entered, or fully crossed? (Bot: touched.)
2. When does a gap stop counting? (Bot: a close beyond its far side.)
3. **Stock session gaps:** SPY doesn't trade overnight, so the open often jumps past the previous candle's range. Those voids weren't made by a candle "with no hesitation", but by the market being closed. TJR trades nearly-24-hour markets (S&P futures, gold, forex), so his lessons don't address it (H18).
4. What is a "secondary entry"? (Day 14)
5. Which lower timeframe pairs with which higher timeframe for the confirming break?
6. Does a gap's size or age matter?
