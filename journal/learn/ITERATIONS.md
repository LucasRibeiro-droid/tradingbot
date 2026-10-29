# Development log of the learning engine

v1-v4: 2021-2024 with 2025+ locked. From v5 the owner released 2025-2026 (2026-10-29) and made CRT optional.

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
| v5 | monthly walk-forward pattern mining (setup × exit × up to 3 concept conditions, kept only if positive in every past year); CRT optional; 2021-01 → 2026-10 | 37.8% (of traded days) | 12.3% | 752 | −0.050 | −37.6 | −58.1 | not chosen | −0.138 |

**Mining test (2026-10-29, owner: "find patterns using everything 2021-2024"):** the best patterns mined on
all of 2021-2024, frozen with day stops chosen on 2021-2024, then traded day by day on 2025-2026, which they
never saw (`studies/research_2026-10-28/learn_mine_split.py`):

| Frozen rulebook | 2021-2024 (where found) | 2025-2026 (unseen) |
|---|---|---|
| top 6 patterns: avg R / total / green traded days / max DD | +0.291 / +226.2R / 54.8% / −17.0R | −0.081 / −31.8R / 38.1% / −43.7R |
| top 12 patterns | +0.253 / +209.4R / 53.9% / −14.0R | −0.050 / −20.7R / 40.7% / −37.6R |

The mined patterns (e.g. NAS100 15m sweep + break against the 1h trend between sessions in the lower third
of the predicted range, +0.55R over 121 trades in 2021-2024) did not hold on new data: in-sample fit, not edge.

**NAS100 only, last 1,000 trading days (2022-12-16 → 2026-10-29), owner 2026-10-29.** New ideas: compression
before the setup, the predictor's expected day size, exits at the predicted high/low. Found on the first 600 days,
tested frozen on the last 400 (`studies/research_2026-10-28/learn_nas_last1000.py`):
- Each new idea alone is negative in both windows for every family (e.g. sweep+break when compressed: −0.37R find,
  −0.28R test; exits at the predicted extreme: −0.09 to −0.33R).
- Mined rulebooks (top 4 / 8 / 15 patterns, with day stops): find +0.80 / +0.87 / +0.65R a trade
  (+128 / +267 / +327R); test +0.01 / −0.04 / −0.04R (+1.2 / −7.4 / −11.9R), profitable traded days 30-35%.
