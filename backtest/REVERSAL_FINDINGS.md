# Reversal study — NQ 5m, Jan 2021 → Apr 2026 (HistData NSXUSD 1-minute, 1.78M candles)

Scripts: `load.py` (1m → 5m/15m/1h), `reversal_events.py` (every body CHoCH + features + outcome),
`analyze.py` / `model.py` (feature lift, ML out-of-sample), `top_in_study.py` / `topin_table.py`
("is today's high/low already in" probability), `choch_p.py` (CHoCH × probability → trades).

## 1. Building blocks at a CHoCH (21,900 flips, entry at CHoCH close, stop at the swing extreme)
Base: 50.3% reach 1R, 33.6% reach 2R → identical to a random walk.
No building block moved this by more than ~2 pts: liquidity sweeps (swing, PDH/PDL, Asia, London),
FVG, displacement, RSI divergence, premium/discount, ADR used, distance from EMA/TWAP, rejection wick,
HTF agreement, opposite no-wick. A gradient-boosting model with all of them: top decile 53% vs 50% (1R).
Retracement entries (50%, 61.8%, OTE 70.5%) were WORSE (−0.1 to −0.2R): fills select the failing reversals.

## 2. What IS predictable: "today's high / low is already in"
Time of day + ADR used + pull-back from the extreme. Learned on 2021-23, tested on 2024-26:
AUC 0.86, well calibrated (said 80-90% → held 89%; said 90%+ → held 97%).

## 3. Trading it
- Shorting/buying as soon as P ≥ 70-90%: ≈ 0R (the move after is still random).
- CHoCH away from the extreme while P ≥ 80%, target 2R: n≈2,640 (≈500/yr), 37% win, +0.048R/trade
  after costs, 4 of 6 years positive. 12:00-16:00 NY: +0.07…0.09R. Small edge.

## 4. Side finding — no-wick strategy on this data (1-minute fills, MNQ costs)
Every trend filter gave ≈ −0.02R gross / −0.09R net at 1:1 (≈49% win). Costs on small stops
(< 15 pts) are the main drag; stops ≥ 25 pts were slightly positive. TradingView without bar
magnifier assumes an intrabar path that can flatter limit-order strategies — worth re-checking.
