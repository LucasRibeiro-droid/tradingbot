"""Pre-trade assessment: is there a setup at the last closed candle, and does it qualify?

The setup is TJR's entry model 1 (Day 30, 03:15; Day 32, 05:02): a liquidity sweep, then a
break of structure the other way, entered on the break's close. Each assessment records:
  A. context: price, time, trend per timeframe, daily bias
  B. confluences present, missing or conflicting, each with its evidence
  C. the plan: direction, entry, stop beyond the sweep + spread room (Day 38), take-profit
     ladder (Day 37), reward-to-risk
  D. the decision: APPROVED, or REJECTED with the reasons
Only facts computed from closed candles are recorded as present; nothing is assumed.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Sequence
from zoneinfo import ZoneInfo

from ..candles import BULLISH, Candle
from ..config import BASELINE, LOCKED, Config
from ..exits import gap_edges, take_profits
from ..fvg import find_gaps
from ..liquidity import draw, scan
from ..orderblocks import find_blocks
from ..trend import NONE, UP, _ts, state_at, trend_series

NY = ZoneInfo("America/New_York")


def _last_closed(candles: Sequence[Candle]) -> int | None:
    for k in range(len(candles) - 1, -1, -1):
        if candles[k].closed:
            return k
    return None


def _ny_minutes(t: str) -> int:
    ny = datetime.fromisoformat(t.replace("Z", "+00:00")).astimezone(NY)
    return ny.hour * 60 + ny.minute


def _hhmm(s: str) -> int:
    h, m = map(int, s.split(":"))
    return h * 60 + m


def assess(symbol: str, ltf: Sequence[Candle], tp_tf: Sequence[Candle], daily: Sequence[Candle],
           config: Config = BASELINE, shorting_enabled: bool = False,
           ltf_length: timedelta = timedelta(minutes=15),
           tp_tf_length: timedelta = timedelta(hours=1)) -> dict | None:
    """The assessment of a setup confirmed by the last closed ``ltf`` candle, or None if
    that candle confirms no setup (no sweep + break of structure)."""
    i = _last_closed(ltf)
    if i is None:
        return None
    states = trend_series(ltf, config.trend)
    scanned = scan(ltf, config.liquidity)
    block = next((b for b in find_blocks(ltf, states, [t for t, _ in scanned], config.trend, config.liquidity)
                  if b.confirmed_at == i), None)
    if block is None:
        return None
    tp = config.trading
    c = ltf[i]
    d = 1 if block.side == BULLISH else -1
    daily_state = state_at(daily, trend_series(daily, config.trend), timedelta(days=1), c.t)
    bias = daily_state.tradeable_direction if daily_state else NONE
    entry = c.c
    sweep_extreme = block.bottom if d == 1 else block.top
    buffer = entry * tp.stop_buffer_pct / 100
    stop = round(sweep_extreme - buffer * d, 2)
    tp_scanned = scan(tp_tf, config.liquidity)
    closes_at = _ts(c.t) + ltf_length
    # The last take-profit-timeframe candle closed by then (no look-ahead).
    k = next((j for j in range(len(tp_tf) - 1, -1, -1) if _ts(tp_tf[j].t) + tp_tf_length <= closes_at), None)
    htf_draws = [p.price for p in tp_scanned[k][1]] if k is not None else []
    levels = [p.price for p in scanned[i][1]] + gap_edges(ltf, find_gaps(ltf), i, entry, d)
    tps = take_profits(d, entry, stop, htf_draws, levels, n=config.decision.take_profits,
                       min_r=config.decision.first_tp_min_r)
    nearest = draw(scanned[i][1], d, entry)

    present, missing, conflicts, reasons = [], [], [], []
    present.append({"concept": "liquidity sweep", "evidence": f"the leg to {sweep_extreme} took a liquidity pool "
                    f"({'sell' if d == 1 else 'buy'}-side) [Days 8-12; detector: pools of strength {config.liquidity.pool_strength}]"})
    present.append({"concept": "break of structure", "evidence": f"candle {c.t} closed {'above' if d == 1 else 'below'} "
                    f"the most recent {'high' if d == 1 else 'low'} at {c.c} [Day 6]"})
    present.append({"concept": "order block", "evidence": f"the sweeping leg {block.bottom}-{block.top} [Days 20-24]"})
    if bias == d:
        present.append({"concept": "daily bias", "evidence": f"last daily break of structure is {'up' if d == 1 else 'down'} [Day 34]"})
    else:
        conflicts.append({"concept": "daily bias", "evidence": "daily structure " +
                          ("has no clear direction" if bias == NONE else f"is {'up' if bias == UP else 'down'}") + " [Day 34]"})
        if not LOCKED.trade_against_htf_trend:
            reasons.append("against or without the daily bias (LOCKED, Day 4 / Day 34)")
    if d == -1 and not shorting_enabled:
        reasons.append("short setup, but shorting is disabled on the account")
    if not tps:
        missing.append({"concept": "take profit 1", "evidence": f"no {tp.take_profit_tf} draw on liquidity at least "
                        f"{config.decision.first_tp_min_r}R away [Day 37]"})
        reasons.append("no first take profit at least 1:1")
    minute = _ny_minutes(c.t) + int(ltf_length.total_seconds() // 60)  # the candle's close
    if not (_hhmm("09:30") < minute <= _hhmm(tp.last_entry)):
        reasons.append(f"outside the entry window (New York open to {tp.last_entry} ET) [Day 18]")
    if (entry - stop) * d <= 0:
        reasons.append("stop is not beyond the entry")
    risk = abs(entry - stop)
    return {
        "symbol": symbol, "t": c.t, "price": entry,
        "context": {"ltf": tp.execution_tf, "ltf_trend": states[i].direction, "daily_bias": bias,
                    "consolidating": states[i].consolidating},
        "setup": f"entry model {tp.entry_model}: liquidity sweep + break of structure "
                 f"{'up (long)' if d == 1 else 'down (short)'} [Day 30]",
        "present": present, "missing": missing, "conflicts": conflicts,
        "plan": {"direction": "long" if d == 1 else "short", "entry": entry, "entry_condition": "market order on the break candle's close",
                 "stop": stop, "invalidation": f"beyond the sweep at {sweep_extreme} (+{tp.stop_buffer_pct}% for spread) [Day 38]",
                 "take_profits": tps, "nearest_liquidity": nearest,
                 "rr_first": round(abs(tps[0] - entry) / risk, 2) if tps and risk else None,
                 "rr_last": round(abs(tps[-1] - entry) / risk, 2) if tps and risk else None},
        "decision": "REJECTED" if reasons else "APPROVED",
        "reasons": reasons,
    }


def size(equity: float, buying_power: float, entry: float, stop: float, risk_pct: float) -> int:
    """Whole shares so the loss at the stop is at most ``risk_pct`` of equity and the cost
    fits the buying power. 0 = can't be sized within the limits."""
    risk_per_share = abs(entry - stop)
    if risk_per_share <= 0 or entry <= 0:
        return 0
    by_risk = int(equity * risk_pct / 100 // risk_per_share)
    by_cash = int(buying_power // entry)
    return max(0, min(by_risk, by_cash))


def split(qty: int, targets: Sequence[float]) -> list[tuple[int, float]]:
    """Equal parts for the take-profit ladder (Day 37; thirds), as whole shares. With fewer
    shares than targets, the nearer targets get them."""
    n = min(len(targets), qty)
    if n == 0:
        return []
    base, extra = divmod(qty, n)
    return [(base + (1 if k < extra else 0), targets[k]) for k in range(n)]
