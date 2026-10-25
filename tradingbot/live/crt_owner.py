"""The owner's CRT rules (2026-10-25), as agreed point by point after the video backtests.

1-hour setup (as in crt_backtest): clear trend, a range candle against the trend in the
discount (premium for shorts) of the impulse leg, then a candle that sweeps beyond it and
closes back inside.
Entry, on the lower timeframe (5- or 15-minute) of the third 1-hour candle only:
  - every fair value gap whose three candles are all inside the third candle gets a limit order
    at its near edge (the top of a bullish gap, the bottom of a bearish one);
  - a trade starts when price taps back into the gap; several gaps can give several trades;
  - when the third candle closes, unfilled orders are dropped (back to the 1-hour chart);
    filled trades are kept until they finish.
  - skipped when the previous day's high or low lies between entry and 1:1 (video).
Stop: the low of the gap's middle candle (its high for shorts).
Exits: half at 1:1, then the stop moves to the entry price; the other half at ``target_r``
(2, 3, 4 or 5R). Held until the target or the stop, overnight too.
A fill bar can stop the trade but can't reach a target (the order of the two inside it is
unknown); a bar that reaches both the stop and a target counts as the stop. Sizing: at most 1%
risk and 10% of $100,000 per trade. Costs: 3 bps on every fill, and the result with costs
only on stop exits (the entry and targets are limit orders).

    python -m tradingbot.live.crt_owner --days 180 --entry-minutes 5 --target-r 3 --symbols ...
"""
from __future__ import annotations

import argparse
import gzip
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean, pstdev

from ..candles import BEARISH, BULLISH, Candle
from ..equilibrium import ranges
from ..fvg import find_gaps
from ..trend import trend_series
from .crt_backtest import _ts, aggregate, five_minute, hourly
from .signals import NY

STUDIES = Path(__file__).resolve().parent.parent.parent / "journal" / "studies"
EQUITY, RISK_PCT, POSITION_PCT, COST_BPS = 100_000.0, 1.0, 10.0, 3.0


@dataclass
class Order:
    symbol: str
    direction: int
    entry: float
    stop: float
    placed: int  # first bar it can fill on
    expires: int  # last bar it can fill on (the third candle's last bar)
    setup_t: str


def orders_for(symbol: str, bars: list[Candle]) -> tuple[list[Order], dict]:
    H, first = hourly(bars, False, 1)
    states = trend_series(H)
    rng = ranges(H, states)
    gaps = find_gaps(bars)
    days = {}
    for c in bars:
        d = _ts(c.t).astimezone(NY).date()
        h, l = days.get(d, (c.h, c.l))
        days[d] = (max(h, c.h), min(l, c.l))
    order_days = sorted(days)
    prev_day = {d: days[order_days[k - 1]] for k, d in enumerate(order_days) if k}
    counts = {"valid setups": 0, "gaps inside the third candle": 0, "daily level in the way": 0}
    out = []
    for i in range(1, len(H) - 1):
        r, s = H[i - 1], H[i]
        d = states[i - 1].tradeable_direction
        if d == 0 or states[i].direction != d:
            continue
        if not ((r.c < r.o) if d == 1 else (r.c > r.o)):
            continue
        zone = rng[i - 1]
        if zone is None or zone.direction != d or zone.depth(r.l if d == 1 else r.h) < 0.5:
            continue
        if not ((s.l < r.l) if d == 1 else (s.h > r.h)) or not (r.l < s.c <= r.h):
            continue
        counts["valid setups"] += 1
        t0 = first[i + 1]  # the third candle's bars
        t1 = (first[i + 2] - 1) if i + 2 < len(first) else len(bars) - 1
        side = BULLISH if d == 1 else BEARISH
        day = _ts(H[i + 1].t).astimezone(NY).date()
        ph, pl = prev_day.get(day, (None, None))
        for g in gaps:
            if g.side != side or g.index - 1 < t0 or g.confirmed_at > t1:
                continue
            counts["gaps inside the third candle"] += 1
            entry = g.top if d == 1 else g.bottom
            mid = bars[g.index]
            stop = mid.l if d == 1 else mid.h
            risk = (entry - stop) * d
            if risk <= 0:
                continue
            tp1 = entry + d * risk
            if any(lv is not None and min(entry, tp1) < lv < max(entry, tp1) for lv in (ph, pl)):
                counts["daily level in the way"] += 1
                continue
            if g.confirmed_at + 1 <= t1:
                out.append(Order(symbol, d, entry, stop, g.confirmed_at + 1, t1, s.t))
    return out, counts


def simulate(bars: list[Candle], o: Order, target_r: float) -> dict | None:
    d = o.direction
    fill = next((k for k in range(o.placed, min(o.expires, len(bars) - 1) + 1)
                 if ((bars[k].l <= o.entry) if d == 1 else (bars[k].h >= o.entry))), None)
    if fill is None:
        return None
    risk = abs(o.entry - o.stop)
    qty = int(min(EQUITY * RISK_PCT / 100 / risk, EQUITY * POSITION_PCT / 100 / o.entry))
    if qty < 2:
        return {"skipped": True}
    half = qty // 2
    tp1, tp2 = o.entry + d * risk, o.entry + d * risk * target_r
    stop, legs, open_qty, hit1 = o.stop, [], qty, False
    for k in range(fill, len(bars)):
        c = bars[k]
        if k > fill and ((c.o <= stop) if d == 1 else (c.o >= stop)):  # gap through the stop at the open
            legs.append((c.o, open_qty, "stop" if not hit1 else "break even")); open_qty = 0
        elif (c.l <= stop) if d == 1 else (c.h >= stop):
            legs.append((stop, open_qty, "stop" if not hit1 else "break even")); open_qty = 0
        elif k > fill:
            if not hit1 and ((c.h >= tp1) if d == 1 else (c.l <= tp1)):
                px = c.o if ((c.o >= tp1) if d == 1 else (c.o <= tp1)) else tp1
                legs.append((px, half, "1:1")); open_qty -= half; hit1 = True
                stop = o.entry  # the rest is now risk-free
                if not ((c.h >= tp2) if d == 1 else (c.l <= tp2)) and ((c.l <= stop) if d == 1 else (c.h >= stop)):
                    legs.append((stop, open_qty, "break even")); open_qty = 0  # back to entry in the same bar
            if open_qty and hit1 and ((c.h >= tp2) if d == 1 else (c.l <= tp2)):
                px = c.o if ((c.o >= tp2) if d == 1 else (c.o <= tp2)) else tp2
                legs.append((px, open_qty, f"{target_r:g}R")); open_qty = 0
        if open_qty == 0:
            break
    if open_qty:
        legs.append((bars[-1].c, open_qty, "end of data"))
    gross = sum((px - o.entry) * q * d for px, q, _ in legs)
    cost_all = COST_BPS / 1e4 * (o.entry * qty + sum(px * q for px, q, _ in legs))
    cost_stops = COST_BPS / 1e4 * sum(px * q for px, q, w in legs if w in ("stop", "break even"))
    rq = risk * qty
    return {"symbol": o.symbol, "direction": "long" if d == 1 else "short", "setup_t": o.setup_t, "fill_t": bars[fill].t,
            "entry": round(o.entry, 4), "stop": round(o.stop, 4), "qty": qty, "risk_pct": round(risk / o.entry * 100, 3),
            "legs": [(round(px, 4), q, w) for px, q, w in legs], "outcome": legs[-1][2] if hit1 else legs[0][2],
            "r_gross": round(gross / rq, 3), "r": round((gross - cost_all) / rq, 3), "r_limit_costs": round((gross - cost_stops) / rq, 3),
            "pnl": round(gross - cost_all, 2)}


def summary(ts: list[dict]) -> dict:
    if not ts:
        return {"trades": 0}
    rs = [t["r"] for t in ts]
    out = {"trades": len(ts), "win_rate": round(sum(t["pnl"] > 0 for t in ts) / len(ts), 3),
           "full_wins": sum(1 for t in ts if t["outcome"].endswith("R")),
           "break_even_after_1to1": sum(1 for t in ts if t["outcome"] == "break even"),
           "stopped": sum(1 for t in ts if t["outcome"] == "stop"),
           "expectancy_r": round(mean(rs), 3), "expectancy_r_gross": round(mean(t["r_gross"] for t in ts), 3),
           "expectancy_r_limit_costs": round(mean(t["r_limit_costs"] for t in ts), 3),
           "total_pnl_usd": round(sum(t["pnl"] for t in ts), 2)}
    if len(rs) > 1 and pstdev(rs):
        out["t_stat"] = round(mean(rs) / (pstdev(rs) / len(rs) ** 0.5), 2)
    return out


def run(symbols: list[str], days: int, entry_minutes: int, targets: list[float]) -> dict:
    now = datetime.now(timezone.utc)
    split, start = now - timedelta(days=days), now - timedelta(days=2 * days)
    res = {r: [] for r in targets}
    counts = {}
    for sym in symbols:
        bars = aggregate(five_minute(sym, 2 * days + 30), entry_minutes, False)
        orders, c = orders_for(sym, bars)
        for k, v in c.items():
            counts[k] = counts.get(k, 0) + v
        orders = [o for o in orders if _ts(o.setup_t) >= start]
        for r in targets:
            for o in orders:
                t = simulate(bars, o, r)
                if t and "skipped" not in t:
                    t["period"] = "recent" if _ts(o.setup_t) >= split else "earlier"
                    res[r].append(t)
        print(f"{sym}: {len(orders)} orders, {len(res[targets[0]])} trades so far", flush=True)
    out = {"params": {"symbols": symbols, "days_per_period": days, "entry_minutes": entry_minutes, "run_at": now.isoformat()},
           "setup_counts": counts, "by_target": {}}
    for r, ts in res.items():
        out["by_target"][f"{r:g}R"] = {p: summary([t for t in ts if p == "all" or t["period"] == p or t["direction"] == p])
                                       for p in ("all", "recent", "earlier", "long", "short")}
    return out, res


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=180)
    ap.add_argument("--entry-minutes", type=int, choices=[5, 15], default=5)
    ap.add_argument("--targets", default="2,3,4,5")
    ap.add_argument("--symbols", required=True)
    args = ap.parse_args()
    out, res = run(args.symbols.split(","), args.days, args.entry_minutes, [float(x) for x in args.targets.split(",")])
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = STUDIES / f"crt_owner_{args.entry_minutes}m_{stamp}.json"
    path.write_text(json.dumps(out, indent=1))
    with gzip.open(path.with_suffix(".trades.jsonl.gz"), "wt") as f:
        for r, ts in res.items():
            f.writelines(json.dumps({**t, "target_r": r}) + "\n" for t in ts)
    for r, v in out["by_target"].items():
        print(r, v["all"])
    print("saved", path)


if __name__ == "__main__":
    main()
