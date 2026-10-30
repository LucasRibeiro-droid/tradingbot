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

**Scalping / day-trading direction signals, NAS100, last 1,000 days, nothing fitted (owner 2026-10-29: "no
overfitting, accurate signals for when to buy and sell")** (`studies/scalp_signals_nas100_2026-10-29.txt`):
momentum (5/15 min), reversal, following or fading a 1-minute candle 3x the hour's range, New York-only momentum,
held 5/15/30 minutes. Direction right 46.6%-52.3% of the time in every case; average move before costs
−0.41 to +0.76 points against a spread of 0.9-2.0 points; net −0.4 to −2.6 points a trade.

**Owner's scalping spec, NAS100, 2025-01 → 2026-10 (473 days), standard settings, nothing tuned**
(`studies/scalp_ema_vwap_nas100_2025_2026.txt`): EMA200 or SuperTrend(10,3) on 15m/1h for direction; 1m EMA 9/21
cross or RSI14 crossing 50; price on the right side of the session VWAP (tick volume); ATR noise filter; stop 1×ATR(14)
(median 7.9 pts), target 1:1 or 1:2. All 16 versions lose: 18-50 trades a day, −0.34 to −0.37R a trade, 3-18% of days
profitable. Same entries before any cost: 49% winners at 1:1 (−0.02 to −0.03R), 34-35% at 1:2 (+0.02 to +0.03R):
no edge; the spread (median 2.3 pts) plus slippage and commission is ~0.35R on an 8-point stop.

## 2026-10-30 — owner's 15m "no-wick candle" strategy, NAS100, last 100 trading days (2026-06-12 .. 10-29)
Momentum of the moment (3 readings: 15m structure, 20-EMA, last 3 candles) → bearish candle with no top wick
(bullish with no bottom wick) → limit at its high (low) → stop at the latest 15m swing high (low) = the BOS level,
target 1:1, one trade at a time, real OANDA spread. Strict no wick: ~55-65 trades, 48-53% wins, −0.05 to +0.05R,
total −2.9R to +2.7R (noise; statistically zero). Allowing a 5-10% wick: 350-550 trades, 44-47% wins,
−0.09 to −0.15R a trade, −34R to −82R. Script and output: `journal/studies/nowick_15m_2026-10-30.py`,
`nowick_15m_nas100_2026-10-30.txt`. Not adopted.
Stop variant (owner): stop just beyond the candle before the no-wick candle (median stop ~20 pt instead of ~35).
Strict no wick: 54-65 trades, 27-34 won, −4.5R to +0.1R. 5% wick: 400-429 trades, 40-42% won, −82R to −98R.
10% wick: 644-659 trades, 39-40% won, −158R to −168R. Tighter stop = more stop-outs and the spread is a bigger
share of each trade. Not adopted.
Target 1:2 (owner): with the swing stop, strict no wick turned positive on the last 100 days: 53-63 trades,
20-27 won, +3.4R to +13.7R (t ≈ 1, not significant); wicks allowed −15R to −78R; with the previous-candle stop
−4.8R to +4.4R strict, −81R to −167R with wicks. Out-of-sample check of the strict versions on the untested
history 2021-01 → 2026-06-11 (1402 days, ~1,700-2,000 trades each): 1:1 −0.30 to −0.32R a trade, 1:2 −0.27 to
−0.29R a trade, negative in every year including 2025 and 2026 H1. Stops were small then (median 9-24 pt, the
spread 8-16% of the risk). The last 100 days look like a lucky stretch. Not adopted.
(`journal/studies/nowick_15m_oos_2026-10-30.py`, `nowick_15m_nas100_oos_2026-10-30.txt`)

## 2026-10-30 — owner's 9:30-10:00 opening range → 10m close outside → 20-EMA touch → next-candle entry
Stop at the touching candle's low/high, target the day's high/low (RTH). NAS100 1m, 2021-01 → 2026-10-29,
one trade a day, flat at 16:00. NQ-futures-like costs: 1,307 trades, 21.7% won (283 / 1,024), −0.31R a trade,
−405R; every year negative (−37R to −91R). Last 100 days: 81 trades, 16 won, 65 lost, −33.8R. OANDA costs: −0.39R,
−510R. Longs −0.14R, shorts −0.50R. Planned R:R ~5.7 but the stop (median 11 pt, one 10m candle) is hit 78% of the
time. Not adopted. (`journal/studies/orb_ema20_2026-10-30.py`, `orb_ema20_nas100_2026-10-30.txt`)
Revised (owner): after the 10m close outside the range, 2m candles: touch of the 2m 20 EMA, then a 2m close back on
the trade's side (reclaim), enter the next 2m open; target the day's high/low. Futures-like costs, 2021-01 → 2026-10:
stop at the reclaim candle: 1,446 trades, 355 won / 1,091 lost (24.6%), −0.13R a trade, −190R, every year negative;
stop at the pullback's extreme since the touch: 422 won / 1,024 lost (29.2%), −0.08R, −122R, every year negative.
Last 100 days: 17-19 won / 75-77 lost, −38R to −41R. Longs with the pullback stop +0.03R over 773 trades (flat);
shorts −0.21R. Better than the 10m-EMA version (−0.31R) but no edge. Not adopted.
(`journal/studies/orb_ema20_2m_2026-10-30.py`, `orb_ema20_2m_nas100_2026-10-30.txt`)
Half at 1:1 then break even (owner): win rate rises to 45-47% but the average stays negative. Futures costs,
2021-01 → 2026-10: pullback stop 677 won / 769 lost, −0.10R a trade, −142R, every year negative; reclaim-candle
stop −0.14R to −0.21R a year. ~23% of trades reach 1:1 then go back to entry; ~53% are stopped before 1:1.
