# Lessons (from trades)

Each lesson: what was seen, the trades, execution or methodology, and the hypothesis it feeds.
One trade never changes a rule; lessons from fewer than ~10 independent trades are leads, not findings.

| # | Lesson | Trades | Kind | Feeds | Strength |
|---|---|---|---|---|---|
| L1 | An exit order isn't an exit: verify with Alpaca that the position is gone (the flatten cancelled the stops and sold nothing) | 10-21: all 5 | execution | fixed in code + tests | certain |
| L2 | The bot must be running when the setup confirms: outages and late starts cost setups (4 missed) and fills (META −0.23R) | 10-21 outages, 10-22 META/AAPL | execution | morning start check-in; Actions | certain |
| L3 | TJR model 1's first target is usually far beyond what the move delivers (0 of 8 reached TP1; best 0.9R) | all 8 | methodology | H38 (lab: 18% reach 1R; exits don't change the result) | strong (lab n≈3,000) |
| L4 | Tight stops make costs a big share of R (AAPL 0.36% stop ≈ 0.17R round trip) | 10-21 AAPL, 10-22 NVDA | methodology | H41 (lab: cost >0.2R → −0.39R) | strong (lab) |
| L5 | Same-candle, same-sector trades are one bet | 10-22 MU + NVDA | evaluation | correlation counted in the scorecard | certain |
| L6 | A loss pattern in a few trades (longs on a down day) didn't survive the lab test | 10-22: 3 longs | evaluation | H43 rejected | lab n≈6,000 |
