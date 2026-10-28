# Day-trading stock strategy search, 2026-10-28 (owner: 2-5 trades a day, flat at the close)

Scripts: `research_2026-10-28/`. Costs 3 bps a side unless stated. Out of sample where a model is fit.

| Rule | Data | Result after costs | Verdict |
|---|---|---|---|
| Trade the NAS100 high/low predictor: long when P(low in) >= 80% (stop below the day's low), mirror short | QQQ 5m, model fit 2016-20, traded 2021-26 | −0.02R a trade (n=1,619), every threshold/target ≈ −0.02R | predictor says *when* the extreme is in, not where price goes |
| Stocks-in-play opening-range breakout (Zarattini, Barbon & Aziz 2024): top 5 by opening relative volume, 0.1 ATR stop, exit at the close | 150 liquid stocks (ranked Oct 2024), 5m SIP, Nov 2024 – Oct 2026 | −0.73R (5m fills: the fill candle usually also reaches the tight stop); optimistic fills −0.13R; 0.5 ATR stop 0.00R | not reproduced |
| Daily pullback signals traded open → close (3 down closes, IBS < 0.2, big prior-day moves, gaps) | 78 large caps, 2016-26 | −8.6 to +3.1 bps; none consistent | the daily edges are earned overnight |
| Intraday momentum/reversal by gain since the open, hold to the close | 150 stocks, 2 years | best: the 3 strongest at 10:00, +8.0 bps, 51% winners, t = 1.1 (quarters +20/+2/+4/+6); 10:30: −4.1; K=10: −0.6; 10 bps costs: −6.0; day-low stop +6.7 | the least bad; not a proven edge |

**Live choice (H63, an experiment):** `day_rs3` — at 10:00 ET buy the 3 strongest stocks since the open
(10% of equity each, stop at the day's low so far), sell at the 15:55 flatten. Exactly 3 trades a day,
inside the owner's 2-5. Expectation: about 0 to +8 bps a trade after costs, i.e. roughly break-even; it
is traded to collect live evidence, and it is replaced as soon as something better passes a test.
