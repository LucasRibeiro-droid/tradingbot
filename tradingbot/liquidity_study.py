"""Days 8, 10 and 12 together: trade the liquidity model exactly, judged by target before stop.

Every break of structure gets the same plan (entry at the break's close, stop beyond the
last ``sweep_lookback`` candles' extreme, target the nearest untaken pool beyond the entry),
so the only difference between groups is the condition TJR teaches: was liquidity taken on
the other side just before the break? Results are in R: +reward/risk for a target, -1 for
a stop. The expectancy (average R) is what matters, not the win rate.

Usage:
    python -m tradingbot.liquidity_study SPY --htf 1Day --ltf 1Hour --days 730 [--pool-strength 10]
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Sequence

from .candles import Candle
from .config import BASELINE, Config, to_dict, with_change
from .liquidity import plan, scan, simulate, sweep_then_shift
from .trend import NONE, TrendState, state_at, trend_series

JOURNAL_DIR = Path(__file__).resolve().parent.parent / "journal" / "studies"


def run(ltf: Sequence[Candle], htf: Sequence[Candle], htf_length: timedelta, config: Config = BASELINE) -> dict:
    p = config.liquidity
    states = trend_series(ltf, config.trend)
    htf_states = trend_series(htf, config.trend)
    scanned = scan(ltf, p)
    taken = [t for t, _ in scanned]
    trades = []
    j, current = 0, None
    for i, s in enumerate(states):
        c = ltf[i]
        while j < len(htf) and state_at(htf[j:j + 1], htf_states[j:j + 1], htf_length, c.t) is not None:
            current = htf_states[j]
            j += 1
        if s.event not in ("bos_up", "bos_down"):
            continue
        d = 1 if s.event == "bos_up" else -1
        tp = plan(ltf, states, scanned, i, d, p)
        if tp is None:
            continue
        out = simulate(ltf, tp, p.max_hold_bars)
        if out is None:
            continue
        htf_dir = current.tradeable_direction if current else NONE
        trades.append({"t": c.t, "direction": d, "entry": tp.entry, "stop": tp.stop, "target": tp.target,
                       "rr": round(tp.reward_to_risk, 3), **out,
                       "after_liquidity": sweep_then_shift(states, taken, i, p) == d,
                       "htf": "with" if htf_dir == d else "none" if htf_dir == NONE else "against"})

    groups = defaultdict(list)
    for t in trades:
        liq = "after_liquidity" if t["after_liquidity"] else "no_liquidity"
        groups[f"1.{liq}"].append(t)
        groups[f"2.{liq}_{t['htf']}_htf"].append(t)
    summary = {}
    for key, g in sorted(groups.items()):
        rs = [t["r"] for t in g]
        summary[key] = {"n": len(g), "win_rate": round(sum(t["exit"] == "target" for t in g) / len(g), 3),
                        "avg_r": round(sum(rs) / len(rs), 3), "total_r": round(sum(rs), 2),
                        "median_rr": round(sorted(t["rr"] for t in g)[len(g) // 2], 2)}
    return {"config": to_dict(config), "trades": trades, "summary": summary}


def main() -> None:
    from .data import fetch_bars, timeframe_length

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("symbol")
    ap.add_argument("--htf", default="1Day")
    ap.add_argument("--ltf", default="1Hour")
    ap.add_argument("--days", type=int, default=730)
    ap.add_argument("--pool-strength", type=int, default=None, help="change only this variable")
    args = ap.parse_args()
    config = BASELINE
    if args.pool_strength and args.pool_strength != BASELINE.liquidity.pool_strength:
        config = with_change(BASELINE, "liquidity", "pool_strength", args.pool_strength)

    start = datetime.now(timezone.utc) - timedelta(days=args.days)
    htf = fetch_bars(args.symbol, args.htf, start - timeframe_length(args.htf) * 60)
    ltf = fetch_bars(args.symbol, args.ltf, start)
    result = run(ltf, htf, timeframe_length(args.htf), config)
    print(f"\n{args.symbol} {args.ltf} inside {args.htf}, config {config.version}")
    print(f"{'group':36} {'n':>5} {'win':>6} {'avg R':>7} {'total R':>8} {'med RR':>7}")
    for key, s in result["summary"].items():
        print(f"{key:36} {s['n']:>5} {s['win_rate']:>6.1%} {s['avg_r']:>+7.2f} {s['total_r']:>+8.1f} {s['median_rr']:>7.2f}")
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = JOURNAL_DIR / f"day12_{args.symbol}_{args.ltf}_in_{args.htf}_ps{config.liquidity.pool_strength}_{stamp}.json"
    path.write_text(json.dumps({"symbol": args.symbol, "htf": args.htf, "ltf": args.ltf, **result}, indent=1))


if __name__ == "__main__":
    main()
