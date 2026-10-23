# Performance (paper trading)

R = profit or loss ÷ the risk planned at entry. "As planned" = had the plan run to the 15:55 ET
flatten (differs from actual only when execution failed). Costs: Alpaca paper has no
commissions; slippage is inside the fill prices. Updated by the daily review.

## A. Trading scorecard (live, as of 2026-10-23: 51 trades over 3 days)
"As planned" = to the 15:55 ET flatten (differs from actual only on 2026-10-21's overnight hold).

| | Trades | Win rate | Avg win | Avg loss | Expectancy | Total | Max drawdown |
|---|---|---|---|---|---|---|---|
| All, as planned | 51 | 37% | +0.51R | −0.76R | **−0.29R** | −14.56R | −17.29R |
| All, actual | 51 | 35% | +0.84R | −0.85R | −0.25R | −12.79R | −18.95R |
| P/L actual | | | | | | **−$1,481** (equity $98,518.65) | |

**By playbook (as planned):**
| Playbook | Trades | Win | Expectancy | Total | Lab, gross (in / out of sample) |
|---|---|---|---|---|---|
| tjr_m1_15m (baseline) | 13 | 38% | −0.28R | −3.70R | −0.01 / −0.00R |
| orb30 | 19 | 11% | −0.63R | −11.98R | +0.01 / +0.05R |
| tjr_m1_1m | 6 | 50% | −0.41R | −2.44R | +0.07 / +0.03R |
| tjr_m2_1m | 9 | 78% | +0.45R | +4.05R | −0.04 / −0.02R |
| tjr_m3_1m | 3 | 33% | −0.63R | −1.89R | +0.05 / +0.10R |
| tjr_m3_5m | 1 | 100% | +1.40R | +1.40R | +0.07 / +0.00R |

**By exit (2026-10-23 only):**

| Exit | Trades | Expectancy |
|---|---|---|
| tjr_ladder | 12 | +0.12R |
| 0.5/1/2R ladder | 12 | −0.06R |
| 1/2/3R ladder (ORB) | 11 | −0.61R |
| 2R (ORB) | 4 | −0.80R |

**By direction (2026-10-23):**
- Long: 34 trades, −0.47R
- Short: 9 trades, +0.35R

**By time (ET, 2026-10-23):**
- 10:00–11:00: 23 trades, −10.9R (the breakout cluster)
- Other hours: 20 trades, −1.4R

**By market:**
- SPY up day (10-21): 5 trades, −0.32R
- Down day (10-22): 3 trades, −3.0R
- 10-23: 43 trades

**Execution (live, paper fills):**
- Entry slippage: median +0.5 bps vs the signal (1-minute +0.3 bps)
- Stop slippage: median −0.2 bps

## B. Learning scorecard
| Measure | Now |
|---|---|
| Trades documented and reviewed | 51 of 51 |
| With a pre-trade hypothesis and prediction | 39 of 51 (all of 2026-10-23 except the 4 rebuilt trades) |
| Independent observations | ~35: the 12 same-candle breakouts count as ~1; MU+NVDA (10-22) and GOOG+GOOGL (same company, same candle) each count as 1 |
| Diversity | 6 playbooks on 3 timeframes, 4 exits, 27 stocks, long and short, up and down days |
| Prediction accuracy (moved toward the target before the stop) | 25 of 51 (49%) |
| Repeated execution errors | restarts losing state (fixed: rebuild from Alpaca); late starts (fixed: morning check-in); the flatten bug (fixed) |
| Repeated decision errors | correlated same-candle entries (H48); first targets beyond what the setups deliver (H38) |
| Hypotheses with evidence | H36, H39, H44 against (lab + live); H45 against in the lab, live 9 trades for (uncertain); H47 rejected; H48 new |

## Lab (history, with 3 bps/side costs): `journal/studies/lab_120d_20261022T181323Z.json`
| Strategy | In sample (last 120 days) | Out of sample (the 120 before) |
|---|---|---|
| tjr_m1, TJR ladder | −0.079R (n=1638) | −0.061R (n=1519) |
| orb30, 2R | −0.089R (n=1551) | −0.032R (n=1540) |

## Earlier replays (before the first session)
`python -m tradingbot.live.replay --days 120`, long only with the daily bias, no costs:
−0.11R per trade (118 trades). See H36.
