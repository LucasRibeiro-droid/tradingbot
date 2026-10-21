# Rule change log

| Date | Change | Rationale / evidence | Test | Status |
|---|---|---|---|---|
| 2026-10-19 | v0-day02: candle settings | Day 2 | studies | baseline then |
| 2026-10-20 | v1-decision: one decision process; liquidity as a confluence | Days 8–12; H12 | decision_study | adopted |
| 2026-10-20 | H14 pool_strength 5 → 10/20 | Day 10 | worse on 7 of 8 charts | rejected |
| 2026-10-21 | v2-tjr-exits: Day 37 take-profit ladder, Day 38 stop beyond the sweep | H19 | better on 23 of 32 (models study) and 10 of 12 (harness) | adopted |
| 2026-10-21 | Unlock "never against the higher timeframe" | H30 retest: against did better | owner decision | **declined by owner**: rule kept; H34 tested (not explained), H35 open |
| 2026-10-21 | Dynamic stock universe vs LOCKED.max_instruments = 2 | owner's operating brief | — | **awaiting owner decision** |
| 2026-10-21 | Trading settings (`config.TradingParams`): risk 1% per trade; no daily loss limit or trade cap; ≤2 instruments a day from a morning screen | owner's answers to the authorization questions | — | **authorized by owner** |
| 2026-10-21 | Live setup = entry model 1 on the 15-minute, TP1 from the 1-hour, daily bias required (LOCKED), long only (account can't short), entries 09:30–15:30 ET, flat at 15:55, brackets GTC | research (`knowledge/execution.md`, `exits.md`) + account limits | replay: see performance.md | adopted for paper trading |
| 2026-10-21 | Owner's direction: TJR is the baseline, not instructions; the bot learns from trades to be as profitable as possible | owner | — | **adopted**: LOCKED = baseline reference; live settings may override on evidence |
| 2026-10-21 | Daily-bias filter off (`TradingParams.daily_bias_filter = False`); every trade records its bias relation | H30 retest (against +0.49R vs with +0.08R); live replay 120 days: filter off −0.04R/trade (313) vs on −0.11R (118) | replay | adopted; still being tested live |
