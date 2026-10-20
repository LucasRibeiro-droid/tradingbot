# Fair value gaps (topic file: Days 14, 16, 18)

**Status: complete** (Day 14: what and why; Day 16: how to identify; Day 18: putting it
together). Later lessons may still refine it (order blocks, equilibrium, execution).
Lesson notes: `day14_fair_value_gaps_pt1.md`, `day16_fair_value_gaps_pt2.md`, `day18_fair_value_gaps_pt3.md`.
Code: `tradingbot/fvg.py` (detection); `decision.Continuation` (test harness path).

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

## Using one
- **Never act on price simply reaching a gap.** Wait for a **reaction** (a candle closing in the trend's direction) or scale down to a **lower timeframe** for a break of structure / market structure shift, and let that be the confirmation [TJR Day 16, 07:58–08:41].
- They're everywhere on the chart and "not all of them are going to work", which is why confirmation is needed. "Be very patient with these" [TJR Day 16, 07:26–08:41].
- Higher-timeframe gap + lower-timeframe break of structure in the trend's direction [TJR Day 14, 04:28; Day 16, 12:01, S&P 4-hour then lower timeframe].
- TJR's homework example (Day 16, 09:13–09:28): break of structure down; bearish gap; price fills it and closes bearish; enter; stop above the previous high; target the previous lows. **An example, not a rule.**
- **The patient entry** [TJR Day 18, 05:14–05:46]: after a liquidity sweep and break of structure, if the move leaves no good reward-to-risk, wait for the retracement into a gap, scale down, and enter on a break of structure confirming continuation.
- **A timeframe cascade** [TJR Day 18]: e.g. 15-minute break → 5-minute gap filled → 5-minute break → 1-minute break for the entry; daily and 1-hour breaks → 1-hour gap → 15-minute break.
- **Refine on a lower timeframe:** if a lower-timeframe wick already fills part of a higher-timeframe gap, use the lower timeframe's gap [TJR Day 18, 12:03–12:58].
- **Stops gaps from counting:** "the second we push past this, no longer considering it" [TJR Day 18, 09:43].
- **Confluence:** liquidity in line with the gap made it "perfect" [TJR Day 18, 09:53–10:01]; ideally liquidity is taken inside the gap before the break [TJR Day 18, 12:34].
- **Exits** [TJR Day 18 examples]: stop beyond the retracement's high/low; targets at previous liquidity, an accumulation area, or a gap's start / 50% / end; several take profits; the rest stopped at break even.
- **Only trade from the market open on** [TJR Day 18, 03:13].
- **More a confirmation than an entry:** "I find other reasoning on why I want to get in: an order block, a break of structure, a liquidity sweep within an imbalance then a break of structure" [TJR Day 18, 15:54–16:11].

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

## Harness results: the continuation path (2026-10-20)

`python -m tradingbot.decision_study` with paths "continuation" (higher-timeframe gap +
lower-timeframe break). Average R per decision:

| Lower in higher timeframe | Continuation only | n | Win rate | Median reward/risk |
|---|---|---|---|---|
| SPY 5-min in 1-hour | +0.05 | 45 | 64% | 0.25 |
| GLD 5-min in 1-hour | −0.17 | 48 | 35% | 0.66 |
| SPY 15-min in 4-hour | −0.09 | 64 | 50% | 0.45 |
| GLD 15-min in 4-hour | +0.05 | 62 | 52% | 0.64 |
| SPY 1-hour in daily | −0.15 | 33 | 52% | 0.42 |
| GLD 1-hour in daily | +0.08 | 41 | 68% | 0.22 |

Near break-even; it wins often but the median reward/risk is far below 1. The harness
targets only the nearest liquidity, which is usually the top of the move that left the gap.
TJR waits for gaps *because* they give a better reward/risk, uses several targets, takes
partials, and moves his stop to break even (Day 18). None of that is in the harness yet (H19).

## Open questions
1. What counts as "filled": touched, entered, or fully crossed? (Bot: touched.) Day 18's examples show price trading into the zone.
2. ~~When does a gap stop counting?~~ When price pushes past it [TJR Day 18, 09:43]. Still open: by wick or by close (Bot: close).
3. **Stock session gaps:** SPY doesn't trade overnight, so the open often jumps past the previous candle's range. Those voids weren't made by a candle "with no hesitation", but by the market being closed. TJR trades nearly-24-hour markets (S&P futures, gold, forex), so his lessons don't address it (H18).
4. ~~What is a "secondary entry"?~~ Shown in Day 18 as the patient entry: after a sweep and break, the retracement into a gap with a lower-timeframe break.
5. Which lower timeframe pairs with which higher timeframe for the confirming break?
6. Does a gap's size or age matter?
7. What is the minimum reward/risk TJR waits for? (Day 18 only says a dump "doesn't give us a good risk reward".)
8. Which market open counts for which instrument? (Day 18, 02:32: "we'll talk about the value that market open gives us later.")
