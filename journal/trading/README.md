# Trading operations: readiness and records

The application phase: the bot trades on Alpaca, starting from TJR's methodology as the
baseline and keeping whatever its own trades and tests show is more profitable (owner, 2026-10-21). This folder holds the
persistent records the owner's operating brief requires (2026-10-21). Nothing has been traded yet.

## Records (persistent: committed to git and pushed)
| File | What it holds |
|---|---|
| `TRADES.md` + `trades/` | **The readable record**: one page per trade with why the bot took it, the plan, the result, and what it learned; an index table. |
| `setups.jsonl` | Every evaluated setup: context, confluences, missing ones, plan, decision (APPROVED / WAIT / REJECTED). One JSON object per line. |
| `trades.jsonl` | Every executed trade: orders, fills, exits, P/L, MFE/MAE, link to its setup. |
| `reviews/YYYY-MM-DD.md` | Daily review: market conditions, setups found, trades taken, missed valid setups, risk-limit status, execution quality, and the post-trade review of each completed trade (validity class 1–4, what went right/wrong, lesson). |
| `performance.md` | Results by setup type, direction, time of day, market conditions: expectancy, win rate, average win/loss, drawdown. |
| `lessons.md` | Repeated errors, recurring strengths, hypotheses, with trade references. |
| `rule_changes.md` | Every proposed or validated rule change: rationale, test, approval. |
| `events.md` | Risk and system events: limit breaches, order failures, stale data, outages. |

The research history (studies, hypotheses H1–H35) stays in `journal/studies/` and `journal/hypotheses.md`.

## How the bot learns from its trades (owner, 2026-10-21)
Goal: learn from mistakes and be as profitable as possible, measured in R (profit or loss ÷ the
risk planned at entry), within the owner's guidelines. Positions are small on purpose (≤10% of
equity each); there is no cap on trades or instruments as long as each trade follows the logic.

1. **Every trade is reviewed** after the close (a scheduled session every weekday, 16:20 ET):
   reconciled with Alpaca; its page gets MFE/MAE, what went right and wrong, validity class 1–4
   judged on what was known at entry, and the lesson. `performance.md` is updated by direction,
   bias relation, time of day, stock and setup.
2. **One trade never changes a rule.** A lesson that repeats becomes a hypothesis in
   `journal/hypotheses.md` with a test: one setting changed, everything else the same.
3. **The test** is `tradingbot.live.replay` on the same stocks, shorts included: the last 120
   days (in sample) and the 120 days before (`--ago 120`, out of sample).
4. **Adopted only if** the change has a higher average R per trade in *both* periods, with at
   least 30 trades in each, and total R is not lower out of sample. Otherwise it is rejected or
   left open, with the numbers. At most one change at a time, recorded in `rule_changes.md`, and
   applied in `config.TradingParams` with a comment pointing to the evidence.
5. **Checked live:** after 20 live trades under a change, live average R is compared with the
   replay's; if live is worse than the previous setting's replay average, the change is reverted.
6. Mistakes of execution (the bot not doing what its logic says: missed setups from outages,
   wrong sizes, orders not reconciled) are fixed in code at once, logged in `events.md`; they are
   not rule changes.

## Inspection, 2026-10-21 (before the session)
**Knowledge base:** `knowledge/methodology.md` and the topic files cover the building blocks, execution models, daily bias and exits (Days 2–4, 6–8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32–38).
- **Not studied:** 1, 5, 9, 11, **13 (Risk Management)**, 15, 17, **19 (News)**, 21, 23, 25, 27, **29 (Trading Plan; owner asked to erase)**, 31, **39 (Lot Size)**, 40–55 (backtesting, journaling, weekly analysis, applied daily bias).
- So risk management, position sizing, news handling and the trading plan aren't from TJR yet. They need the owner's settings.

**Alpaca (verified through the API):**
- Account PA3L67J2X is a **paper** account. The keys are rejected by the live API (401), so live trading is impossible with them.
- Status ACTIVE: equity **$99.98**, cash $99.98, buying power $99.98, multiplier 1 (no margin). No positions, no open orders.
- **Shorting disabled** on the account (`shorting_enabled: false`); account config `no_shorting: false`, `fractional_trading: true`, `max_margin_multiplier: 4`. **Long-only for now.**
- Options level 3 approved (not part of the methodology; not used).
- Universe: 13,503 tradable US equities; 7,790 fractionable; 5,321 shortable (not usable without account shorting).
- Market data:
  - **Real-time: IEX only.** One exchange, so bars are thin.
  - Real-time SIP (all exchanges) is denied (403).
  - SIP history older than 15 minutes is available.
  - The research used IEX bars, so live and research data match.
- Orders (MCP `place_stock_order`): market, limit, stop, stop-limit, trailing stop; day/gtc/opg/cls/ioc/fok; bracket, OCO, OTO; `client_order_id` for idempotency.
- Market clock: closed at inspection; next open 2026-10-21 09:30 ET.

**Not verified** (Alpaca's docs are blocked from this environment; to confirm with a first small paper order):
- **Pattern-day-trader protection** (accounts under $25k: 3 day trades per 5 business days; Alpaca applies it to paper too). With $99.98, intraday trading is capped at about 3 round trips per week.
- **Fractional quantities can't be bracket orders.** Protected positions need whole shares, so only stocks under about $99 are reachable, and the three take profits need at least 3 shares.

## What the evidence supports so far
- **Exits:** TJR's exits (v2) beat a single target: 23 of 32 comparisons in the four-model study, 10 of 12 in the harness. Models 1–2 were positive on all four intraday SPY/GLD charts.
- **Never tested beyond SPY and GLD.** Never tested with costs, and never on stocks screened dynamically.
- **Daily-bias filters didn't help** (H30–H33); the "against" edge is unexplained (H34, H35).

## Gaps before autonomous trading
1. **Owner's risk settings:**
   - risk per trade;
   - maximum daily loss;
   - maximum trades per day;
   - aggregate and correlated exposure;
   - halt rules;
   - overnight policy.
2. **Universe vs a locked rule.** The brief asks for a dynamic universe, but `LOCKED.max_instruments = 2` (TJR Day 4: "focus on one or two instruments"). It's the owner's decision.
3. **Account size.** $99.98 limits positions to whole shares under about $99, and probably 3 day trades per 5 days.
4. **Execution engine (to build):**
   - a live screener on IEX bars;
   - the signal engine on live candles (`models_study` / `decision` logic);
   - bracket orders with the take-profit ladder (Alpaca brackets carry one take profit, so the ladder means one bracket per part);
   - order reconciliation;
   - journal writers.
5. **Scheduling.** This container isn't always on. Sessions need a scheduled task at the open, or a session started by the owner.
