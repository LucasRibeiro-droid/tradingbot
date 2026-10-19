# Open hypotheses

Each hypothesis changes **one** variable against the current baseline, gets tested on data
the bot did not use to form it, and is only promoted to the new baseline if it wins by a
margin larger than chance. Rejected hypotheses stay here with their result so they are not
retried.

Baseline: `v0-day04` (candle settings unchanged since `v0-day02`).

| ID | From | Hypothesis | Variable | Status |
|---|---|---|---|---|
| H1 | Day 2 study, 2026-10-19 | Rejection reads have more edge on higher timeframes (weekly > daily > 5Min). | timeframe | open — weekly samples too small (n=13/30) |
| H2 | Day 2 study, 2026-10-19 | After a strong close, price takes that candle's extreme in its direction first more often than the base rate. | (measurement only) | open — 66–88% observed, needs a base-rate comparison for "side taken first" |
| H3 | Day 2 study, 2026-10-19 | A bullish doji after a decline on SPY daily precedes a rise (+22.8%, n=17). | — | open — likely chance given how many groups were compared; retest out of sample |
| H4 | Day 2 lesson, 13:22 | Candle reads that agree with the higher-timeframe trend beat reads that oppose it. | trend filter | open — Day 4 study: better in 6 of 10 comparisons, not conclusive; retest once Day 6 (break of structure) is learned |
| H5 | Day 4 study, 2026-10-19 | Bigger swings (`swing_strength` 2 → 3 or 5) match TJR's chart swings better and make trend direction more predictive. | trend.swing_strength | open |
| H6 | Day 4 lesson, 18:32 | Swings from closes (line chart) give a cleaner trend than swings from wicks. | trend.swing_source | open |
| H7 | Day 4 lesson, 07:10 | Trend should be judged by whether the next push extends past the last swing, not by the next 5 candles. | (measurement) | open |
| H8 | Day 4 study, 2026-10-19 | A lower-timeframe trend that agrees with the higher timeframe beats one that opposes it. | — | open — with > against in 7 of 10 comparisons, small gaps |
