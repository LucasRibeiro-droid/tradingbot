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
| 2026-10-23T19:27 | NBIS | long | n/a | -0.984 | -173.25 | [page](trades/2026-10-23_1430_NBIS.md) | orb30 / ladder_1_2_3R |
| 2026-10-23T19:27 | AMD | long | against | -1.062 | -19.57 | [page](trades/2026-10-23_1918_AMD.md) | tjr_m3_1m / tjr_ladder |
| 2026-10-23T19:29 | AVGO | long | n/a | -0.997 | -92.7 | [page](trades/2026-10-23_1430_AVGO.md) | orb30 / 2R |
| 2026-10-23T19:30 | SPCX | short | none | -1.163 | -23.37 | [page](trades/2026-10-23_1927_SPCX.md) | tjr_m3_1m / ladder_0.5_1_2R |
| 2026-10-23T19:32 | SNDK | long | against | -1.143 | -36.08 | [page](trades/2026-10-23_1914_SNDK.md) | tjr_m1_1m / ladder_0.5_1_2R |
| 2026-10-23T19:41 | AMZN | long | none | -0.929 | -9.25 | [page](trades/2026-10-23_1848_AMZN.md) | tjr_m1_1m / tjr_ladder |
| 2026-10-23T19:41 | GOOGL | short | with | 1.214 | 17.12 | [page](trades/2026-10-23_1918_GOOGL.md) | tjr_m2_1m / ladder_0.5_1_2R |
| 2026-10-23T19:52 | SOXX | long | n/a | -1.001 | -126.15 | [page](trades/2026-10-23_1430_SOXX.md) | orb30 / ladder_1_2_3R |
| 2026-10-23T19:55 | QQQ | long | against | -0.144 | -7.25 | [page](trades/2026-10-23_1345_QQQ.md) | tjr_m1 / tjr_ladder |
| 2026-10-23T19:55 | NVDA | long | against | -0.726 | -90.41 | [page](trades/2026-10-23_1345_NVDA.md) | tjr_m1 / ladder_0.5_1_2R |
| 2026-10-23T19:55 | AAPL | short | against | 0.217 | 20.83 | [page](trades/2026-10-23_1400_AAPL.md) | tjr_m1 / tjr_ladder |
| 2026-10-23T19:55 | MSFT | long | against | 0.231 | 31.35 | [page](trades/2026-10-23_1400_MSFT.md) | tjr_m1 / tjr_ladder |
| 2026-10-23T19:55 | MU | long | n/a | -0.698 | -117.22 | [page](trades/2026-10-23_1430_MU.md) | orb30 / ladder_1_2_3R |
| 2026-10-23T19:55 | META | long | n/a | -0.309 | -27.9 | [page](trades/2026-10-23_1430_META.md) | orb30 / 2R |
| 2026-10-23T19:55 | TTMI | long | n/a | 0.35 | 132.84 | [page](trades/2026-10-23_1430_TTMI.md) | orb30 / ladder_1_2_3R |
| 2026-10-23T19:55 | MRVL | long | n/a | -0.54 | -152.61 | [page](trades/2026-10-23_1430_MRVL.md) | orb30 / ladder_1_2_3R |
| 2026-10-23T19:55 | TSM | long | n/a | -0.792 | -77.76 | [page](trades/2026-10-23_1430_TSM.md) | orb30 / ladder_1_2_3R |
| 2026-10-23T19:55 | SMH | long | n/a | -0.912 | -99.09 | [page](trades/2026-10-23_1430_SMH.md) | orb30 / ladder_1_2_3R |
| 2026-10-23T19:56 | PLTR | long | n/a | -0.009 | -1.7 | [page](trades/2026-10-23_1430_PLTR.md) | orb30 / ladder_1_2_3R |
| 2026-10-23T19:56 | ORCL | long | n/a | -0.742 | -71.8 | [page](trades/2026-10-23_1430_ORCL.md) | orb30 / 2R |
| 2026-10-23T19:56 | TSLA | long | none | -0.126 | -27.44 | [page](trades/2026-10-23_1445_TSLA.md) | tjr_m1_15m / tjr_ladder |
| 2026-10-23T19:56 | MRNA | long | n/a | -0.304 | -148.37 | [page](trades/2026-10-23_1445_MRNA.md) | orb30 / ladder_1_2_3R |
| 2026-10-23T19:56 | IWM | long | with | 0.342 | 7.5 | [page](trades/2026-10-23_1515_IWM.md) | tjr_m2_1m / tjr_ladder |
| 2026-10-23T19:56 | GOOG | short | with | 2.329 | 35.44 | [page](trades/2026-10-23_1918_GOOG.md) | tjr_m2_1m / tjr_ladder |
