"""Days 4 and 6 study: trend, higher-timeframe agreement and breaks of structure vs the base rate.

Questions, each compared against what price did anyway on the same chart:
  1. After a trend is established, does price keep going that way? (Day 4, 01:01)
  2. Is a lower-timeframe trend more reliable when the higher timeframe agrees? (Day 4, 08:13)
  3. Do Day 2 candle reads work better when they agree with the higher timeframe? (H4)
  4. After a break of structure, does price follow it, and does that depend on the higher
     timeframe? A break against it should be "just a retracement" (Day 6, 22:31).
  5. After a fake (a wick through the level without a close), does price go back the other
     way, as TJR says it often does (Day 6, 23:58)? Day 6's homework: real breaks vs fakes.
  6. Is a break of structure that comes right after liquidity was taken on the other side
     more reliable than one that doesn't (Day 8, 07:04-09:36)? Liquidity as defined in
     Day 10: resting orders beyond clear highs and lows that have held.

Usage:
    python -m tradingbot.trend_study SPY --htf 1Day --ltf 1Hour --days 730 [--swing-method pivot]
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Sequence

from .candles import NEUTRAL, Candle, read
from .config import BASELINE, Config, to_dict, with_change
from .study import reaction
from .liquidity import pools_and_takes, sweep_then_shift
from .trend import NONE, TrendState, state_at, trend_series

JOURNAL_DIR = Path(__file__).resolve().parent.parent / "journal" / "studies"


def _group(rows: list[dict], base: dict) -> dict:
    out = {}
    for key, g in sorted(_by_key(rows).items()):
        side = 1 if key.endswith(":up") else -1
        base_rate = base["up"] / base["n"] if side == 1 else base["down"] / base["n"]
        hit = sum(r["move"] * side > 0 for r in g) / len(g)
        out[key] = {"n": len(g), "hit_rate": round(hit, 3), "base_rate": round(base_rate, 3),
                    "edge": round(hit - base_rate, 3),
                    "avg_move_with_direction": round(sum(r["move"] * side for r in g) / len(g), 3)}
    return out


def _by_key(rows):
    groups = defaultdict(list)
    for r in rows:
        groups[r["key"]].append(r)
    return groups


def run(ltf: Sequence[Candle], htf: Sequence[Candle], htf_length: timedelta,
        config: Config = BASELINE) -> dict:
    horizon = config.study.horizon_bars
    ltf_states = trend_series(ltf, config.trend)
    htf_states = trend_series(htf, config.trend)
    taken = pools_and_takes(ltf, config.liquidity)

    base = {"up": 0, "down": 0, "n": 0}
    rows = []
    j = 0
    current: TrendState | None = None
    for i, c in enumerate(ltf):
        if not c.closed:
            continue
        r = reaction(ltf, i, horizon)
        if r is None:
            continue
        base["n"] += 1
        base["up"] += r["move"] > 0
        base["down"] += r["move"] < 0
        # Advance the higher-timeframe pointer to the last higher candle that closed before this one.
        while j < len(htf) and state_at(htf[j:j + 1], htf_states[j:j + 1], htf_length, c.t) is not None:
            current = htf_states[j]
            j += 1
        htf_dir = current.tradeable_direction if current else NONE
        s = ltf_states[i]
        name = {1: "up", -1: "down"}
        if s.tradeable_direction != NONE:
            d = s.tradeable_direction
            rows.append({"key": f"1.ltf_trend:{name[d]}", "move": r["move"]})
            rel = "with_htf" if htf_dir == d else "no_htf_trend" if htf_dir == NONE else "against_htf"
            rows.append({"key": f"2.ltf_trend_{rel}:{name[d]}", "move": r["move"]})
        if s.event in ("bos_up", "bos_down"):
            d = 1 if s.event == "bos_up" else -1
            rel = "with_htf" if htf_dir == d else "no_htf_trend" if htf_dir == NONE else "against_htf"
            rows.append({"key": f"4.bos_{rel}:{name[d]}", "move": r["move"]})
            after = "after_liquidity" if sweep_then_shift(ltf_states, taken, i, config.liquidity) else "no_liquidity"
            rows.append({"key": f"6.bos_{after}:{name[d]}", "move": r["move"]})
            rows.append({"key": f"7.bos_{after}_{rel}:{name[d]}", "move": r["move"]})
        elif s.event in ("sweep_low", "sweep_high"):
            # A wick below a low that fails to close there points back up, and vice versa.
            d = 1 if s.event == "sweep_low" else -1
            rows.append({"key": f"5.{s.event}_then:{name[d]}", "move": r["move"]})
        cr = read(ltf, i, config.candle)
        if cr.readable and cr.lean != NEUTRAL:
            rel = "with_htf" if htf_dir == cr.lean else "no_htf_trend" if htf_dir == NONE else "against_htf"
            rows.append({"key": f"3.candle_read_{rel}:{name[cr.lean]}", "move": r["move"]})

    return {"config": to_dict(config), "ltf_candles": len(ltf), "htf_candles": len(htf),
            "base": base, "summary": _group(rows, base)}


def print_summary(result: dict, title: str) -> None:
    print(f"\n{title}: {result['ltf_candles']} candles, horizon "
          f"{result['config']['study']['horizon_bars']} bars, config {result['config']['version']}")
    print(f"{'group':40} {'n':>6} {'hit':>6} {'base':>6} {'edge':>7} {'avgmove':>8}")
    for key, s in result["summary"].items():
        print(f"{key:40} {s['n']:>6} {s['hit_rate']:>6.1%} {s['base_rate']:>6.1%} "
              f"{s['edge']:>+7.1%} {s['avg_move_with_direction']:>+8.2f}")


def main() -> None:
    from .data import fetch_bars, timeframe_length

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("symbol")
    ap.add_argument("--htf", default="1Day")
    ap.add_argument("--ltf", default="1Hour")
    ap.add_argument("--days", type=int, default=730)
    ap.add_argument("--swing-method", choices=["two_candle", "pivot"], default=None,
                    help="compare against the baseline by changing only this variable")
    args = ap.parse_args()
    config = BASELINE
    if args.swing_method and args.swing_method != BASELINE.trend.swing_method:
        config = with_change(BASELINE, "trend", "swing_method", args.swing_method)

    start = datetime.now(timezone.utc) - timedelta(days=args.days)
    htf_start = start - timeframe_length(args.htf) * 60  # warm-up so the trend is known on day one
    htf = fetch_bars(args.symbol, args.htf, htf_start)
    ltf = fetch_bars(args.symbol, args.ltf, start)
    result = run(ltf, htf, timeframe_length(args.htf), config)
    title = f"{args.symbol} {args.ltf} inside {args.htf}"
    print_summary(result, title)
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    tag = config.trend.swing_method
    path = JOURNAL_DIR / f"day06_{args.symbol}_{args.ltf}_in_{args.htf}_{tag}_{stamp}.json"
    path.write_text(json.dumps({"symbol": args.symbol, "htf": args.htf, "ltf": args.ltf, **result}, indent=1))
    print(f"saved {path}")


if __name__ == "__main__":
    main()
