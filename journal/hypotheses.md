# Open hypotheses

Each hypothesis changes **one** variable against the current baseline, gets tested on data
the bot did not use to form it, and is only promoted to the new baseline if it wins by a
margin larger than chance. Rejected hypotheses stay here with their result so they are not
retried.

Baseline: `v1-decision` (one decision process reading all indicators; see knowledge/decision.md) (candle settings unchanged since `v0-day02`; swings follow Day 6).

| ID | From | Hypothesis | Variable | Status |
|---|---|---|---|---|
| H1 | Day 2 study, 2026-10-19 | Rejection reads have more edge on higher timeframes (weekly > daily > 5Min). | timeframe | open — weekly samples too small (n=13/30) |
| H2 | Day 2 study, 2026-10-19 | After a strong close, price takes that candle's extreme in its direction first more often than the base rate. | (measurement only) | open — 66–88% observed, needs a base-rate comparison for "side taken first" |
| H3 | Day 2 study, 2026-10-19 | A bullish doji after a decline on SPY daily precedes a rise (+22.8%, n=17). | — | open — likely chance given how many groups were compared; retest out of sample |
| H4 | Day 2 lesson, 13:22 | Candle reads that agree with the higher-timeframe trend beat reads that oppose it. | trend filter | open — Day 4 study: better in 6 of 10 comparisons, not conclusive; retest once liquidity (Days 8–12) is learned |
| H5 | Day 4 study, 2026-10-19 | Bigger swings (`swing_strength` 2 → 3 or 5) match TJR's chart swings better and make trend direction more predictive. | trend.swing_strength | superseded — Day 6 defines swings exactly (two candles); pivot kept only for comparison |
| H6 | Day 4 lesson, 18:32 | Swings from closes (line chart) give a cleaner trend than swings from wicks. | trend.swing_source | open |
| H7 | Day 4 lesson, 07:10 | Trend should be judged by whether the next push extends past the last swing, not by the next 5 candles. | (measurement) | open |
| H8 | Day 4 study, 2026-10-19 | A lower-timeframe trend that agrees with the higher timeframe beats one that opposes it. | — | open — with > against in 7 of 10 comparisons, small gaps |
| H9 | Day 6 study, 2026-10-19 | The higher timeframe only overrules breaks that go against the long-run drift: breaks down in an uptrend fail, breaks up in a downtrend don't. | — | open — down against HTF below base rate in 4 of 5 charts, up against HTF above base rate in 5 of 5 |
| H10 | Day 6 lesson, 23:58 | After a fake (a wick past the watched level without a close), price goes back the other way. | — | open — no consistent edge alone (3 of 5 and 2 of 5); retest with Day 8 liquidity context |
| H11 | Day 7 lesson, 06:55 | The New York open fakes out (a strong first move that quickly flips) on SPY/GLD, like TJR's London open on GBPJPY. | — | open — first study: the opposite; the first 15–30 minutes held to the close 58–77% of the time. Retest with Day 8 liquidity sweeps |
| H12 | Day 7 lesson, 04:45 | Each indicator earns its place in the decision process: removing it makes decisions worse. | one indicator on/off | open — liquidity: adding it improved average R on 4 of 6 charts (small samples); kept as a required confluence |
| H13 | Day 8 lesson, 07:04 | A break of structure right after real liquidity is taken beats one without. | liquidity definition | open — folded into H12 (liquidity as a confluence). Retest once entries use fair value gaps / order blocks (Days 14–24) |
| H14 | Day 10 study, 2026-10-20 | Pools from more prominent highs/lows (`pool_strength` 5 → 10 or 20) mark the liquidity that matters more. | liquidity.pool_strength | **rejected** 2026-10-20 — after-liquidity trades got worse on 7 of 8 charts (e.g. SPY 1-hour +0.06R → −0.31R at 20). Baseline stays 5 |
| H15 | Day 12 study, 2026-10-20 | Targeting further liquidity (the 2nd untaken pool, or a minimum reward/risk) improves expectancy. | liquidity target choice | open — side effect of H14: plain breaks gained with farther pools on 1-hour (+0.17R SPY, +0.10R GLD at strength 20) |
| H16 | Day 16 lesson, 03:22 | Fair value gaps that agree with the trend continue more often than counter-trend ones. | — | open — better on 4 of 6 charts (4-hour: SPY 58% vs 45%, GLD 58% vs 44% after a reaction) |
| H17 | Day 16 lesson, 07:58 | Waiting for a reaction inside a gap beats acting when price first enters it. | — | supported on 6 of 6 charts (54–62% vs 38–42%), partly by construction; retest by target-before-stop once Day 18 teaches the trade |
| H18 | Day 16 study, 2026-10-20 | On SPY, gaps created by the overnight session break behave differently from gaps created within a session. | gap source | open |
| H19 | Day 18 lesson, 05:28 | The continuation path needs TJR's exits: a minimum reward/risk, several liquidity targets with partials, a break-even stop. | target / management | open — continuation alone near break-even (−0.17R to +0.08R) with median reward/risk 0.22–0.66 |
| H20 | Day 18 lesson, 12:03 | Refining a higher-timeframe gap with the lower timeframe's wicks improves entries. | gap refinement | open |
| H21 | Day 18 lesson, 09:53 | Gaps lined up with untaken liquidity (or with liquidity taken inside them) work better. | gap + liquidity confluence | open |
| H22 | Day 20 lesson, 06:57 | Order blocks are a better retracement area than fair value gaps (TJR's first choice). | retracement area | supported, partly by construction: after price reaches it, continuation 57–68% vs 38–46% for gaps on 4 of 4 shared charts; the block's far side is farther away |
| H23 | Day 22 lesson, 25:11 | Waiting for the retracement into the order block beats entering on the break of structure (same stop and target). | entry location | mixed: better reward-to-risk on 6 of 6 charts (median 1.27–1.90 vs 1.02–1.59), better average R on only 1 of 6 with a bare limit entry |
| H24 | Days 22, 24 | As the continuation zone (retrace in + lower-timeframe break), a higher-timeframe order block beats a fair value gap. | continuation zone | inconclusive 2026-10-21: higher median reward/risk on 6 of 6 charts; better average R on 2 of 6 (SPY 15m/4h +0.34 vs −0.05, GLD 5m/1h +0.12 vs −0.12); only 8–28 block trades per chart. Gap path stays baseline |
| H26 | Day 24, 11:12 | Boxing an order block from the wick to the start of the body (TJR's way) gives better reactions than the whole leg. | order block zone | 2026-10-21: as a **reaction point**, weakly supported (pullbacks turned inside it 5–25% of the time vs a zone 5–10% of the leg, above on 6 of 8 charts). As the **zone** in the harness, **rejected**: only 1–5 trades per chart. Whole leg stays |
| H28 | Day 26, 09:49 | Continuation entries from a fair value gap inside the discount (below 50% of the swing, for longs) beat those from gaps in the premium. | equilibrium filter | leaning supported 2026-10-21: avg R better on 4 of 6 charts (e.g. SPY 15m/4h −0.05 → +0.07, GLD 1h/1D +0.08 → +0.14), worse on 2; reward/risk drops. Not promoted |
| H29 | Day 30, 05:50 | TJR's risk ladder holds: entry model 4 (sweep + break + zone + discount) wins more often than model 1 (sweep + break alone), with models 2/3 in between. | entry model | **not supported** 2026-10-21 (`models_study.py`, 8 charts, same setups, stop and target): model 4 has the lowest win rate on 7 of 8 (24–38%) and the best reward/risk on 7 of 8. Best avg R per trade: model 3 on 3 charts, 1 on 2, 4 on 2, 2 on 1. Model 3 positive on 6 of 8, model 2 on 2 of 8. Retest with daily bias (Days 34–36) and TJR's exits |
| H27 | Day 24, 09:52 | Order blocks without a prior liquidity sweep work as well as those with one. | orderblocks require_sweep | open |
| H25 | Day 22 lesson, 09:15 | The stop must fit the timeframe being played: beyond the whole higher-timeframe block, not a tight lower-timeframe stop. | stop placement | open |
