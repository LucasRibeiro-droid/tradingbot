# Trades

Every trade the bot takes: why, the plan, the result, and what it learned (click the trade).
"As planned" = the result had the plan been followed to the end (flat at 15:55 ET); it differs from the actual result only when execution failed (2026-10-21: the flatten bug held positions overnight).

| Setup (UTC) | Stock | Direction | Strategy / exit | Bias relation | R actual | R as planned | P/L actual | Record |
|---|---|---|---|---|---|---|---|---|
| 2026-10-21 14:00 | NVDA | short | tjr_m1 / tjr_ladder | with | +1.47 | -0.71 | +1,223.60 | [page](trades/2026-10-21_1400_NVDA.md) |
| 2026-10-21 15:30 | MU | long | tjr_m1 / tjr_ladder | against | -1.75 | +0.06 | -1,888.82 | [page](trades/2026-10-21_1530_MU.md) |
| 2026-10-21 17:00 | SPCX | short | tjr_m1 / tjr_ladder | none | +2.06 | +0.34 | +707.77 | [page](trades/2026-10-21_1700_SPCX.md) |
| 2026-10-21 17:30 | TSLA | short | tjr_m1 / tjr_ladder | none | +2.00 | +0.20 | +108.01 | [page](trades/2026-10-21_1730_TSLA.md) |
| 2026-10-21 18:45 | AAPL | short | tjr_m1 / tjr_ladder | none | -0.68 | -0.21 | -27.54 | [page](trades/2026-10-21_1845_AAPL.md) |
| 2026-10-22 15:00 | META | long | tjr_m1 / tjr_ladder | against | -1.00 | -1.00 | -131.36 | [page](trades/2026-10-22_1500_META.md) |
| 2026-10-22 17:15 | MU | long | tjr_m1 / tjr_ladder | against | -1.02 | -1.00 | -111.78 | [page](trades/2026-10-22_1715_MU.md) |
| 2026-10-22 17:15 | NVDA | long | tjr_m1 / tjr_ladder | none | -1.02 | -1.00 | -41.66 | [page](trades/2026-10-22_1715_NVDA.md) |
| 2026-10-23T15:04 | SNDK | long | n/a | -1.07 | -123.74 | [page](trades/2026-10-23_1430_SNDK.md) | orb30 / ladder_1_2_3R |
| 2026-10-23T15:18 | SNDK | long | against | -1.119 | -52.91 | [page](trades/2026-10-23_1507_SNDK.md) | tjr_m2_1m / tjr_ladder |
| 2026-10-23T15:36 | AMD | long | against | 0.073 | 1.63 | [page](trades/2026-10-23_1527_AMD.md) | tjr_m2_1m / ladder_0.5_1_2R |
| 2026-10-23T15:56 | AMD | long | against | 0.27 | 10.04 | [page](trades/2026-10-23_1547_AMD.md) | tjr_m1_1m / ladder_0.5_1_2R |
| 2026-10-23T17:13 | AMD | long | against | -1.167 | -16.08 | [page](trades/2026-10-23_1658_AMD.md) | tjr_m1_1m / tjr_ladder |
| 2026-10-23T17:32 | GOOGL | long | n/a | -1.026 | -58.5 | [page](trades/2026-10-23_1400_GOOGL.md) | orb30 / 2R |
| 2026-10-23T17:33 | GOOG | long | n/a | -1.023 | -62.41 | [page](trades/2026-10-23_1400_GOOG.md) | orb30 / ladder_1_2_3R |
| 2026-10-23T18:06 | GOOG | short | with | 0.027 | 0.36 | [page](trades/2026-10-23_1752_GOOG.md) | tjr_m3_1m / ladder_0.5_1_2R |
| 2026-10-23T18:22 | GOOG | long | against | -1.112 | -10.34 | [page](trades/2026-10-23_1817_GOOG.md) | tjr_m1_1m / ladder_0.5_1_2R |
| 2026-10-23T18:33 | AMD | short | with | -1.075 | -27.3 | [page](trades/2026-10-23_1804_AMD.md) | tjr_m2_1m / ladder_0.5_1_2R |
| 2026-10-23T18:38 | AMZN | long | none | 0.873 | 17.12 | [page](trades/2026-10-23_1444_AMZN.md) | tjr_m2_1m / tjr_ladder |
| 2026-10-23T18:39 | GOOGL | short | with | 1.239 | 10.9 | [page](trades/2026-10-23_1750_GOOGL.md) | tjr_m2_1m / ladder_0.5_1_2R |
| 2026-10-23T19:08 | SNDK | short | with | 1.411 | 222.18 | [page](trades/2026-10-23_1620_SNDK.md) | tjr_m3_5m / tjr_ladder |
| 2026-10-23T19:15 | GOOGL | long | against | 0.207 | 2.42 | [page](trades/2026-10-23_1908_GOOGL.md) | tjr_m1_1m / ladder_0.5_1_2R |
| 2026-10-23T19:18 | GOOG | long | against | 0.576 | 3.75 | [page](trades/2026-10-23_1907_GOOG.md) | tjr_m2_1m / ladder_0.5_1_2R |
