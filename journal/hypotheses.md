# Open hypotheses

Each hypothesis changes **one** variable against the current baseline, gets tested on data
the bot did not use to form it, and is only promoted to the new baseline if it wins by a
margin larger than chance. Rejected hypotheses stay here with their result so they are not
retried.

Baseline: `v0-day08` (candle settings unchanged since `v0-day02`; swings follow Day 6).

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
| H12 | Day 7 lesson, 04:45 | Each strategy component earns its place: removing it makes results worse. | one component on/off | open — needs the full strategy |
| H13 | Day 8 lesson, 07:04 | A break of structure right after real liquidity is taken beats one without. | liquidity definition | blocked — with every two-candle high/low counted as liquidity, ~99% of breaks qualify; needs Day 10's definition of where liquidity sits |
