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
| L7 | A restart must not lose trades: rebuild them from the broker, and check the broker before entering | 10-23: IWM, INTC, AMD, SPCX | execution | fixed in code + tests | certain |
| L8 | Many stocks breaking out on the same candle is one market bet (12 longs at 10:30 ET, all reversed) | 10-23: 12 breakouts | evaluation / risk | H48 | one day: a lead |
| L9 | A small gross edge doesn't survive costs: lower timeframes are +0.03 to +0.07R gross, negative at any realistic cost | lab 10-23 | methodology | H47 rejected | strong (lab n≈20,000) |
| L10 | On 1-minute, R and dollars diverge: 10% position cap × 0.1–0.2% stops = $2–5 per R | 10-23: 1m trades | evaluation | report $ beside R | certain |
| L11 | CRT gaps with stops under ~0.15% of price lose to the spread and stop slippage (1 cent can be 0.25R) | 10-26: SPCX 18:00, SNDK 16:40/19:00, SPCX 19:15 | methodology / cost | H58 (backtest: worse the tighter; filter adopted) | strong (backtest n=451 + live) |
| L12 | Stacked CRT gaps share levels: a newer gap's stop is an older order's entry, so one move stops one and fills the other | 10-26: SNDK, AMD | methodology | to test next | lead (3 cases) |
