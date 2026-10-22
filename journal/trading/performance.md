# Performance (paper trading)

R = profit or loss ÷ the risk planned at entry. "As planned" = had the plan run to the 15:55 ET
flatten (differs from actual only when execution failed). Costs: Alpaca paper has no
commissions; slippage is inside the fill prices. Updated by the daily review.

## A. Trading scorecard (live, as of 2026-10-22: 8 trades, all `tjr_m1 / tjr_ladder`)
| | Trades | Win rate | Avg win | Avg loss | Expectancy | Total | Max drawdown |
|---|---|---|---|---|---|---|---|
| As planned | 8 | 38% | +0.20R | −0.78R | **−0.42R** | −3.32R | −3.32R |
| Actual (incl. the overnight hold) | 8 | 38% | +1.84R | −1.09R | +0.01R | +0.06R / −$160.78 | n/a |

**By group (as planned; samples tiny, not conclusions):**
| Group | Trades | Total R | Avg R |
|---|---|---|---|
| Short | 4 | −0.38 | −0.10 |
| Long | 4 | −2.94 | −0.74 |
| With the daily bias | 1 | −0.71 | −0.71 |
| Against the daily bias | 3 | −1.94 | −0.65 |
| No daily bias | 4 | −0.67 | −0.17 |
| SPY up day (10-21) | 5 | −0.32 | −0.06 |
| SPY down day (10-22) | 3 | −3.00 | −1.00 |
| Before 12:00 ET | 3 | −1.65 | −0.55 |
| After 12:00 ET | 5 | −1.67 | −0.33 |

**By stock:**
- NVDA: −1.71R (2 trades)
- MU: −0.94R (2)
- META: −1.00R (1)
- SPCX: +0.34R (1)
- TSLA: +0.20R (1)
- AAPL: −0.21R (1)

**Execution:** entry slippage −0.02R on average; stop slippage ≤0.02R.

## B. Learning scorecard
| Measure | Now |
|---|---|
| Completed trades documented and reviewed | 8 of 8 |
| With a pre-trade hypothesis and prediction | 0 of 8 (the experiment record starts 2026-10-23) |
| Independent observations | 7 (MU and NVDA on 10-22: same candle, sector and direction) |
| Diversity | 1 strategy, 1 exit, 6 stocks, both directions, 1 up day and 1 down day |
| Prediction accuracy (moved more toward the target than toward the stop) | 2 of 8 |
| Repeated execution errors | flatten bug (fixed), late start / outages (fixed: Actions + morning check-in), late fill (META) |
| Repeated decision errors | TP1 beyond what the setups deliver (8 of 8 never reached TP1) |
| Hypotheses with evidence | H36 against (live −0.42R, lab −0.06 to −0.08R); H38 half supported (MFE) / half not (exits); H41 supported; H43 rejected |

## Lab (history, with 3 bps/side costs): `journal/studies/lab_120d_20261022T181323Z.json`
| Strategy | In sample (last 120 days) | Out of sample (the 120 before) |
|---|---|---|
| tjr_m1, TJR ladder | −0.079R (n=1638) | −0.061R (n=1519) |
| orb30, 2R | −0.089R (n=1551) | −0.032R (n=1540) |

## Earlier replays (before the first session)
`python -m tradingbot.live.replay --days 120`, long only with the daily bias, no costs:
−0.11R per trade (118 trades). See H36.
