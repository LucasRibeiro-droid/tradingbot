# Development log of the learning engine (2021-2024 only; the 2025+ holdout is untouched)

Every row is a full day-by-day run: strategy trades are what each day's rulebook (written the evening
before) took. Results are strategy trades only, after spread, slippage and commission, in R.

| Engine | What changed | Profitable days | Days with 2-5 trades | Trades | Avg R | Total R | Max drawdown | CRT | Gold |
|---|---|---|---|---|---|---|---|---|---|
| v1 | first learner: shrunk mean + recent positive, weekly rewrite | 45.3% | 49.5% | 1,840 | −0.068 | −124.9 | −136.2 | −0.121 | −0.121 |
| v2 | consistency across quarters, hysteresis, more combinations, break-even exits, stop-size filters | 44.6% | 51.5% | 1,902 | −0.057 | −107.5 | −115.8 | −0.153 | −0.280 |
| v3 | bug fix: a stop inside the spread is not a trade (had produced −10⁸R outliers in the evidence) | 44.4% | 53.3% | 1,934 | −0.075 | −144.3 | −146.1 | −0.144 | −0.244 |
| v4 | the bot's own high/low predictor as a filter; rules and instruments benched when the bot's own strategy trades lose | 41.6% | 33.8% | 1,277 | −0.034 | −43.6 | −71.5 | −0.136 | −0.117 |

Findings so far (from the experiments, all 2021-2024):
- Every setup family is negative on average after costs; gold is negative in every family and every year.
- One coherent cluster is positive in 2021-2023: NAS100 sweep + break of structure on 5m/15m in the New
  York session in line with the 1-hour trend (+0.11/+0.09/+0.05R a trade), but −0.03R in 2024.
- Fading moves beyond the predictor's 80% band loses badly (−0.4 to −0.9R); continuing them is ≈ −0.04R.
- No session drift beyond costs on either instrument.
- The bot's daily high/low predictor works as a predictor (median miss at the 18:00 open 62 vs 106 points
  naive on NAS100; bands held 74-82%) but is not a trading edge by itself.
