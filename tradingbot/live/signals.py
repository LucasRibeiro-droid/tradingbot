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
from ..config import BASELINE, Config
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


MODEL_NAMES = {
    1: "entry model 1: liquidity sweep + break of structure, enter on the break's close [Day 30, 03:15; Day 32, 05:02]",
    2: "entry model 2: liquidity sweep + break of structure, limit order at the order block [Day 32, 11:19]",
    3: "entry model 3: liquidity sweep + break of structure, enter on a reaction candle in the new fair value gap [Day 33, 09:41]",
}


def assess(symbol: str, ltf: Sequence[Candle], tp_tf: Sequence[Candle], daily: Sequence[Candle],
           config: Config = BASELINE, shorting_enabled: bool = False,
           ltf_length: timedelta = timedelta(minutes=15),
           tp_tf_length: timedelta = timedelta(hours=1)) -> dict | None:
    """Model 1 at the last closed ``ltf`` candle (the baseline), or None."""
    found = assess_all(symbol, ltf, tp_tf, daily, config, shorting_enabled, ltf_length, tp_tf_length, models=(1,))
    return found[0] if found else None


def _triggers(ltf, i, states, scanned, blocks, gaps, models, wait, stop_buffer_pct):
    """(model, block, entry price, entry type) for each model whose entry is the last closed candle i."""
    out = []
    c = ltf[i]
    now_block = next((b for b in blocks if b.confirmed_at == i), None)
    if now_block is not None:
        d = 1 if now_block.side == BULLISH else -1
        if 1 in models:
            out.append((1, now_block, c.c, "market"))
        if 2 in models:
            near = now_block.top if d == 1 else now_block.bottom
            near = min(near, c.c) if d == 1 else max(near, c.c)  # a limit can't buy above the market
            out.append((2, now_block, round(near, 2), "limit"))
    if 3 in models:
        for b in sorted((b for b in blocks if i - wait <= b.confirmed_at < i), key=lambda b: -b.confirmed_at):
            d = 1 if b.side == BULLISH else -1
            cf = b.confirmed_at
            extreme = b.bottom if d == 1 else b.top
            stop = extreme - extreme * stop_buffer_pct / 100 * d
            target = draw(scanned[cf][1], d, ltf[cf].c)
            if any((x.l <= stop) if d == 1 else (x.h >= stop) for x in ltf[cf + 1:i + 1]):
                continue  # invalidated: the stop was reached
            if target is not None and any((x.h >= target) if d == 1 else (x.l <= target) for x in ltf[cf + 1:i]):
                continue  # missed: the draw was reached before an entry
            own = [g for g in gaps if g.side == b.side and g.index >= b.sweep]

            def reacts(j):
                x = ltf[j]
                for g in own:
                    if g.confirmed_at >= j:
                        continue
                    broken = any((y.c < g.bottom) if d == 1 else (y.c > g.top) for y in ltf[g.confirmed_at + 1:j + 1])
                    if not broken and x.l <= g.top and x.h >= g.bottom and x.direction == b.side:
                        return g
                return None

            g = reacts(i)
            if g is not None and not any(reacts(j) for j in range(cf + 1, i)):
                out.append((3, b, c.c, "market", g))
                break
    return out


def assess_all(symbol: str, ltf: Sequence[Candle], tp_tf: Sequence[Candle], daily: Sequence[Candle],
               config: Config = BASELINE, shorting_enabled: bool = False,
               ltf_length: timedelta = timedelta(minutes=15),
               tp_tf_length: timedelta = timedelta(hours=1), models: tuple[int, ...] = (1,), wait: int = 20) -> list[dict]:
    """Assessments of every TJR entry model (1, 2, 3) whose entry is the last closed ``ltf``
    candle, on any timeframe. Model 2's entry is a limit order at the order block."""
    i = _last_closed(ltf)
    if i is None:
        return []
    states = trend_series(ltf, config.trend)
    scanned = scan(ltf, config.liquidity)
    blocks = find_blocks(ltf, states, [t for t, _ in scanned], config.trend, config.liquidity)
    gaps = find_gaps(ltf)
    tp = config.trading
    out = []
    for trig in _triggers(ltf, i, states, scanned, blocks, gaps, models, wait, tp.stop_buffer_pct):
        model, block, entry, entry_type = trig[:4]
        c = ltf[i]
        d = 1 if block.side == BULLISH else -1
        daily_state = state_at(daily, trend_series(daily, config.trend), timedelta(days=1), c.t)
        bias = daily_state.tradeable_direction if daily_state else NONE
        sweep_extreme = block.bottom if d == 1 else block.top
        buffer = entry * tp.stop_buffer_pct / 100
        stop = round(sweep_extreme - buffer * d, 2)
        tp_scanned = scan(tp_tf, config.liquidity)
        closes_at = _ts(c.t) + ltf_length
        # The last take-profit-timeframe candle closed by then (no look-ahead).
        k = next((j for j in range(len(tp_tf) - 1, -1, -1) if _ts(tp_tf[j].t) + tp_tf_length <= closes_at), None)
        htf_draws = [p.price for p in tp_scanned[k][1]] if k is not None else []
        levels = [p.price for p in scanned[i][1]] + gap_edges(ltf, gaps, i, entry, d)
        tps = take_profits(d, entry, stop, htf_draws, levels, n=config.decision.take_profits,
                           min_r=config.decision.first_tp_min_r)
        nearest = draw(scanned[i][1], d, entry)

        present, missing, conflicts, reasons = [], [], [], []
        present.append({"concept": "liquidity sweep", "evidence": f"the leg to {sweep_extreme} took a liquidity pool "
                        f"({'sell' if d == 1 else 'buy'}-side) [Days 8-12; detector: pools of strength {config.liquidity.pool_strength}]"})
        bos = ltf[block.confirmed_at]
        present.append({"concept": "break of structure", "evidence": f"candle {bos.t} closed {'above' if d == 1 else 'below'} "
                        f"the most recent {'high' if d == 1 else 'low'} at {bos.c} [Day 6]"})
        present.append({"concept": "order block", "evidence": f"the sweeping leg {block.bottom}-{block.top} [Days 20-24]"})
        if model == 2:
            present.append({"concept": "entry at the order block", "evidence": f"limit {'buy' if d == 1 else 'sell'} at {entry} "
                            f"(the block's near edge), valid {wait} candles [Day 32, 11:19]"})
        if model == 3:
            g = trig[4]
            present.append({"concept": "fair value gap reaction", "evidence": f"candle {c.t} traded into the gap "
                            f"{g.bottom}-{g.top} and closed {'up' if d == 1 else 'down'} [Day 33, 09:41; Day 16, 08:09]"})
        if bias == d:
            present.append({"concept": "daily bias", "evidence": f"last daily break of structure is {'up' if d == 1 else 'down'} [Day 34]"})
        else:
            conflicts.append({"concept": "daily bias", "evidence": "daily structure " +
                              ("has no clear direction" if bias == NONE else f"is {'up' if bias == UP else 'down'}") + " [Day 34]"})
            if tp.daily_bias_filter:
                reasons.append("against or without the daily bias (TJR Day 4 / Day 34; filter on)")
        if d == -1 and not shorting_enabled:
            reasons.append("short setup, but shorting is disabled on the account")
        if not tps:
            missing.append({"concept": "take profit 1", "evidence": f"no draw on liquidity on the next timeframe up at least "
                            f"{config.decision.first_tp_min_r}R away [Day 37]"})
            reasons.append("no first take profit at least 1:1")
        minute = _ny_minutes(c.t) + int(ltf_length.total_seconds() // 60)  # the candle's close
        if not (_hhmm("09:30") < minute <= _hhmm(tp.last_entry)):
            reasons.append(f"outside the entry window (New York open to {tp.last_entry} ET) [Day 18]")
        if (entry - stop) * d <= 0:
            reasons.append("stop is not beyond the entry")
        risk = abs(entry - stop)
        condition = {"market": f"market order on the {'break' if model == 1 else 'reaction'} candle's close",
                     "limit": f"limit order at {entry}, cancelled after {wait} candles if not filled"}[entry_type]
        out.append({
            "symbol": symbol, "t": c.t, "price": c.c, "model": model, "block_t": ltf[block.confirmed_at].t,
            "context": {"ltf": f"{int(ltf_length.total_seconds() // 60)}Min" if ltf_length < timedelta(hours=1) else f"{int(ltf_length.total_seconds() // 3600)}Hour",
                        "ltf_trend": states[i].direction, "daily_bias": bias,
                        "bias_relation": "with" if bias == d else "none" if bias == NONE else "against",
                        "consolidating": states[i].consolidating},
            "setup": f"{MODEL_NAMES[model]}, {'up (long)' if d == 1 else 'down (short)'}",
            "present": present, "missing": missing, "conflicts": conflicts,
            "plan": {"direction": "long" if d == 1 else "short", "entry": entry, "entry_type": entry_type,
                     "entry_condition": condition, "valid_candles": wait if entry_type == "limit" else None,
                     "stop": stop, "invalidation": f"beyond the sweep at {sweep_extreme} (+{tp.stop_buffer_pct}% for spread) [Day 38]",
                     "take_profits": tps, "nearest_liquidity": nearest,
                     "rr_first": round(abs(tps[0] - entry) / risk, 2) if tps and risk else None,
                     "rr_last": round(abs(tps[-1] - entry) / risk, 2) if tps and risk else None},
            "decision": "REJECTED" if reasons else "APPROVED",
            "reasons": reasons,
        })
    return out


def size(equity: float, buying_power: float, entry: float, stop: float, risk_pct: float,
         max_position_pct: float | None = None) -> int:
    """Whole shares so the loss at the stop is at most ``risk_pct`` of equity, the cost fits
    the buying power and, if set, at most ``max_position_pct`` of equity. 0 = can't be sized."""
    risk_per_share = abs(entry - stop)
    if risk_per_share <= 0 or entry <= 0:
        return 0
    by_risk = int(equity * risk_pct / 100 // risk_per_share)
    by_cash = int(buying_power // entry)
    by_position = int(equity * max_position_pct / 100 // entry) if max_position_pct else by_cash
    return max(0, min(by_risk, by_cash, by_position))


def split(qty: int, targets: Sequence[float]) -> list[tuple[int, float]]:
    """Equal parts for the take-profit ladder (Day 37; thirds), as whole shares. With fewer
    shares than targets, the nearer targets get them."""
    n = min(len(targets), qty)
    if n == 0:
        return []
    base, extra = divmod(qty, n)
    return [(base + (1 if k < extra else 0), targets[k]) for k in range(n)]
