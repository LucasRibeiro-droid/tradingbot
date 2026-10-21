# Strategy performance (live/paper trading)

No trades yet. Results will be grouped by entry model (1–4, Days 30–33), direction, time of day,
daily-bias relation, instrument and market conditions: trades, win rate, average win, average
loss, expectancy (R), max drawdown, after costs.

Research results (backtests, no costs) are separate: `knowledge/exits.md`, `knowledge/execution.md`.

## Replay of the live configuration (before the first session, 2026-10-21)
`python -m tradingbot.live.replay --days 120`, SPY, GLD and the first screen's 8 stocks.
Exactly the live assessment at each 15-minute close, TJR's exits, flat at 15:55, no costs:

| | Approved trades | Win | Avg R | Total R |
|---|---|---|---|---|
| All 10 | 118 | ~37% | **−0.11** | **−12.9** |
| GLD | 14 | 43% | +0.12 | +1.7 |
| MRNA | 13 | 69% | +0.15 | +2.0 |
| Other 8 | 6–17 each | 23–50% | −0.02 to −0.30 | −0.1 to −3.7 |

**The live configuration has had a negative expectancy over the last 120 days.** It's the subset
the research found weakest: long only, with the daily bias (locked). Paper trading proceeds to
gather live evidence (the brief), but no edge is claimed. See H36.
