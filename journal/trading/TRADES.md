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
| 2026-10-23 13:45 | QQQ | long | tjr_m1 / tjr_ladder | against | -0.14 | -0.04 | -7.25 | [page](trades/2026-10-23_1345_QQQ.md) |
| 2026-10-23 13:45 | NVDA | long | tjr_m1 / ladder_0.5_1_2R | against | -0.73 | -0.53 | -90.41 | [page](trades/2026-10-23_1345_NVDA.md) |
| 2026-10-23 14:00 | AAPL | short | tjr_m1 / tjr_ladder | against | +0.22 | +0.24 | +20.83 | [page](trades/2026-10-23_1400_AAPL.md) |
| 2026-10-23 14:00 | MSFT | long | tjr_m1 / tjr_ladder | against | +0.23 | +0.11 | +31.35 | [page](trades/2026-10-23_1400_MSFT.md) |
| 2026-10-23 14:00 | GOOGL | long | orb30 / 2R | n/a | -1.03 | -1.00 | -58.50 | [page](trades/2026-10-23_1400_GOOGL.md) |
| 2026-10-23 14:00 | GOOG | long | orb30 / ladder_1_2_3R | n/a | -1.02 | -1.00 | -62.41 | [page](trades/2026-10-23_1400_GOOG.md) |
| 2026-10-23 14:15 | IWM | short | orb30 / unknown (adopted after a restart) | n/a | -1.01 | -1.00 | -24.58 | [page](trades/2026-10-23_1415_IWM_orb30.md) |
| 2026-10-23 14:15 | INTC | long | orb30 / unknown (adopted after a restart) | n/a | -0.25 | -0.34 | -35.37 | [page](trades/2026-10-23_1415_INTC_orb30.md) |
| 2026-10-23 14:15 | AMD | long | orb30 / unknown (adopted after a restart) | n/a | +0.23 | +0.24 | +25.84 | [page](trades/2026-10-23_1415_AMD_orb30.md) |
| 2026-10-23 14:15 | SPCX | long | orb30 / unknown (adopted after a restart) | n/a | -1.00 | -1.00 | -142.67 | [page](trades/2026-10-23_1415_SPCX_orb30.md) |
| 2026-10-23 14:30 | MU | long | orb30 / ladder_1_2_3R | n/a | -0.70 | -0.63 | -117.22 | [page](trades/2026-10-23_1430_MU.md) |
| 2026-10-23 14:30 | META | long | orb30 / 2R | n/a | -0.31 | -0.77 | -27.90 | [page](trades/2026-10-23_1430_META.md) |
| 2026-10-23 14:30 | SNDK | long | orb30 / ladder_1_2_3R | n/a | -1.07 | -1.00 | -123.74 | [page](trades/2026-10-23_1430_SNDK.md) |
| 2026-10-23 14:30 | AVGO | long | orb30 / 2R | n/a | -1.00 | -1.00 | -92.70 | [page](trades/2026-10-23_1430_AVGO.md) |
| 2026-10-23 14:30 | TTMI | long | orb30 / ladder_1_2_3R | n/a | +0.35 | +0.29 | +132.84 | [page](trades/2026-10-23_1430_TTMI.md) |
| 2026-10-23 14:30 | MRVL | long | orb30 / ladder_1_2_3R | n/a | -0.54 | -0.45 | -152.61 | [page](trades/2026-10-23_1430_MRVL.md) |
| 2026-10-23 14:30 | TSM | long | orb30 / ladder_1_2_3R | n/a | -0.79 | -0.71 | -77.76 | [page](trades/2026-10-23_1430_TSM.md) |
| 2026-10-23 14:30 | SMH | long | orb30 / ladder_1_2_3R | n/a | -0.91 | -0.70 | -99.09 | [page](trades/2026-10-23_1430_SMH.md) |
| 2026-10-23 14:30 | SOXX | long | orb30 / ladder_1_2_3R | n/a | -1.00 | -0.80 | -126.15 | [page](trades/2026-10-23_1430_SOXX.md) |
| 2026-10-23 14:30 | PLTR | long | orb30 / ladder_1_2_3R | n/a | -0.01 | -0.31 | -1.70 | [page](trades/2026-10-23_1430_PLTR.md) |
| 2026-10-23 14:30 | NBIS | long | orb30 / ladder_1_2_3R | n/a | -0.98 | -1.00 | -173.25 | [page](trades/2026-10-23_1430_NBIS.md) |
| 2026-10-23 14:30 | ORCL | long | orb30 / 2R | n/a | -0.74 | -0.43 | -71.80 | [page](trades/2026-10-23_1430_ORCL.md) |
| 2026-10-23 14:44 | AMZN | long | tjr_m2_1m / tjr_ladder | none | +0.87 | +0.85 | +17.12 | [page](trades/2026-10-23_1444_AMZN.md) |
| 2026-10-23 14:45 | TSLA | long | tjr_m1_15m / tjr_ladder | none | -0.13 | -0.16 | -27.44 | [page](trades/2026-10-23_1445_TSLA.md) |
| 2026-10-23 14:45 | MRNA | long | orb30 / ladder_1_2_3R | n/a | -0.30 | -0.37 | -148.37 | [page](trades/2026-10-23_1445_MRNA.md) |
| 2026-10-23 15:07 | SNDK | long | tjr_m2_1m / tjr_ladder | against | -1.12 | -1.00 | -52.91 | [page](trades/2026-10-23_1507_SNDK.md) |
| 2026-10-23 15:15 | IWM | long | tjr_m2_1m / tjr_ladder | with | +0.34 | +0.56 | +7.50 | [page](trades/2026-10-23_1515_IWM.md) |
| 2026-10-23 15:27 | AMD | long | tjr_m2_1m / ladder_0.5_1_2R | against | +0.07 | +0.17 | +1.63 | [page](trades/2026-10-23_1527_AMD.md) |
| 2026-10-23 15:47 | AMD | long | tjr_m1_1m / ladder_0.5_1_2R | against | +0.27 | +0.26 | +10.04 | [page](trades/2026-10-23_1547_AMD.md) |
| 2026-10-23 16:20 | SNDK | short | tjr_m3_5m / tjr_ladder | with | +1.41 | +1.40 | +222.18 | [page](trades/2026-10-23_1620_SNDK.md) |
| 2026-10-23 16:58 | AMD | long | tjr_m1_1m / tjr_ladder | against | -1.17 | -1.00 | -16.08 | [page](trades/2026-10-23_1658_AMD.md) |
| 2026-10-23 17:50 | GOOGL | short | tjr_m2_1m / ladder_0.5_1_2R | with | +1.24 | +0.18 | +10.90 | [page](trades/2026-10-23_1750_GOOGL.md) |
| 2026-10-23 17:52 | GOOG | short | tjr_m3_1m / ladder_0.5_1_2R | with | +0.03 | +0.11 | +0.36 | [page](trades/2026-10-23_1752_GOOG.md) |
| 2026-10-23 18:04 | AMD | short | tjr_m2_1m / ladder_0.5_1_2R | with | -1.07 | -1.00 | -27.30 | [page](trades/2026-10-23_1804_AMD.md) |
| 2026-10-23 18:17 | GOOG | long | tjr_m1_1m / ladder_0.5_1_2R | against | -1.11 | -1.00 | -10.34 | [page](trades/2026-10-23_1817_GOOG.md) |
| 2026-10-23 18:48 | AMZN | long | tjr_m1_1m / tjr_ladder | none | -0.93 | -1.00 | -9.25 | [page](trades/2026-10-23_1848_AMZN.md) |
| 2026-10-23 19:07 | GOOG | long | tjr_m2_1m / ladder_0.5_1_2R | against | +0.58 | +0.56 | +3.75 | [page](trades/2026-10-23_1907_GOOG.md) |
| 2026-10-23 19:08 | GOOGL | long | tjr_m1_1m / ladder_0.5_1_2R | against | +0.21 | +0.20 | +2.42 | [page](trades/2026-10-23_1908_GOOGL.md) |
| 2026-10-23 19:14 | SNDK | long | tjr_m1_1m / ladder_0.5_1_2R | against | -1.14 | +0.10 | -36.08 | [page](trades/2026-10-23_1914_SNDK.md) |
| 2026-10-23 19:18 | AMD | long | tjr_m3_1m / tjr_ladder | against | -1.06 | -1.00 | -19.57 | [page](trades/2026-10-23_1918_AMD.md) |
| 2026-10-23 19:18 | GOOGL | short | tjr_m2_1m / ladder_0.5_1_2R | with | +1.21 | +1.21 | +17.12 | [page](trades/2026-10-23_1918_GOOGL.md) |
| 2026-10-23 19:18 | GOOG | short | tjr_m2_1m / tjr_ladder | with | +2.33 | +2.52 | +35.44 | [page](trades/2026-10-23_1918_GOOG.md) |
| 2026-10-23 19:27 | SPCX | short | tjr_m3_1m / ladder_0.5_1_2R | none | -1.16 | -1.00 | -23.37 | [page](trades/2026-10-23_1927_SPCX.md) |
| 2026-10-26 13:40 | MRVL | long | crt_1h5m / 1:1 + 3R, fixed stop | n/a | -1.05 | (review) | -57.19 | [page](trades/2026-10-26_1340_MRVL_crt_1h5m.md) |
| 2026-10-26 14:20 | AMD | long | crt_1h5m / 1:1 + 3R, fixed stop | n/a | -1.11 | (review) | -33.69 | [page](trades/2026-10-26_1420_AMD_crt_1h5m.md) |
| 2026-10-26 14:20 | MRVL | long | crt_1h5m / 1:1 + 3R, fixed stop | n/a | +2.19 | (review) | +114.69 | [page](trades/2026-10-26_1420_MRVL_crt_1h5m.md) |
| 2026-10-26 16:45 | SNDK | short | crt_1h5m / 1:1 + 3R, fixed stop | n/a | -1.04 | (review) | -24.25 | [page](trades/2026-10-26_1645_SNDK_crt_1h5m.md) |
| 2026-10-26 16:40 | SNDK | short | crt_1h5m / 1:1 + 3R, fixed stop | n/a | -1.32 | (review) | -16.45 | [page](trades/2026-10-26_1640_SNDK_crt_1h5m.md) |
| 2026-10-26 18:00 | SPCX | long | crt_1h5m / 1:1 + 3R, fixed stop | n/a | -1.80 | (review) | -4.16 | [page](trades/2026-10-26_1800_SPCX_crt_1h5m.md) |
| 2026-10-26 19:00 | SNDK | short | crt_1h5m / 1:1 + 3R, fixed stop | n/a | -2.54 | (review) | -7.63 | [page](trades/2026-10-26_1900_SNDK_crt_1h5m.md) |
| 2026-10-26 19:15 | SPCX | long | crt_1h5m / 1:1 + 3R, fixed stop | n/a | -0.91 | (review) | -6.60 | [page](trades/2026-10-26_1915_SPCX_crt_1h5m.md) |
| 2026-10-26 19:10 | SPCX | long | crt_1h5m / 1:1 + 3R, fixed stop | n/a | -0.98 | (review) | -16.50 | [page](trades/2026-10-26_1910_SPCX_crt_1h5m.md) |
| 2026-10-26 18:55 | SNDK | short | crt_1h5m / 1:1 + 3R, fixed stop | n/a | +3.02 | (review) | +36.39 | [page](trades/2026-10-26_1855_SNDK_crt_1h5m.md) |
