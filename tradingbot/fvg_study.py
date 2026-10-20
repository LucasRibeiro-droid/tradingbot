"""Day 16 homework, done by the bot: find every fair value gap and see what price did with it.

Tests two things TJR states (Day 16):
  1. Gaps are for continuation in the trend's direction, not reversals (03:22-04:05):
     compare gaps that agree with the trend when they form against gaps that oppose it.
  2. Don't act on price reaching a gap; wait for a reaction (07:58-08:41): compare what
     happened after a reaction against what happened after a plain entry into the zone.

Outcome [Bot measure, not TJR's]: a continuation succeeds if price goes past the extreme
of the move that left the gap (bullish: above the highest high between the gap forming and
price coming back into it) before any candle closes beyond the gap's far side.

Usage:
    python -m tradingbot.fvg_study SPY --timeframe 4Hour --days 730
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Sequence

from .candles import BULLISH, Candle
from .config import BASELINE, to_dict
from .fvg import find_gaps, follow
from .trend import NONE, trend_series

JOURNAL_DIR = Path(__file__).resolve().parent.parent / "journal" / "studies"


def continued(candles: Sequence[Candle], side: int, start: int, extreme: float, far_side: float) -> bool | None:
    """From candle ``start`` on: True if price passes ``extreme`` before closing beyond
    ``far_side``; False if the close beyond comes first; None if neither happens in the data."""
    for c in candles[start:]:
        if not c.closed:
            return None
        if (c.h > extreme) if side == BULLISH else (c.l < extreme):
            return True
        if (c.c < far_side) if side == BULLISH else (c.c > far_side):
            return False
    return None


def run(candles: Sequence[Candle]) -> dict:
    states = trend_series(candles, BASELINE.trend)
    rows = []
    for g in find_gaps(candles):
        trend = states[g.confirmed_at].tradeable_direction
        rel = "with_trend" if trend == g.side else "no_trend" if trend == NONE else "against_trend"
        ev = follow(candles, g)
        row = {"t": candles[g.index].t, "side": g.side, "top": g.top, "bottom": g.bottom, "trend": rel,
               "entered": ev.entered_at is not None, "reacted": ev.reacted_at is not None}
        if ev.entered_at is not None:
            leg = candles[g.confirmed_at:ev.entered_at + 1]
            extreme = max(c.h for c in leg) if g.side == BULLISH else min(c.l for c in leg)
            far = g.bottom if g.side == BULLISH else g.top
            row["after_entry"] = continued(candles, g.side, ev.entered_at + 1, extreme, far)
            if ev.reacted_at is not None:
                row["after_reaction"] = continued(candles, g.side, ev.reacted_at + 1, extreme, far)
        rows.append(row)

    groups = defaultdict(list)
    for r in rows:
        groups[r["trend"]].append(r)
        groups["all"].append(r)
    summary = {}
    for key, g in sorted(groups.items()):
        entered = [r for r in g if r["entered"]]
        e_res = [r["after_entry"] for r in entered if r.get("after_entry") is not None]
        r_res = [r["after_reaction"] for r in entered if r.get("after_reaction") is not None]
        summary[key] = {"gaps": len(g), "entered": len(entered),
                        "reacted": sum(r["reacted"] for r in entered),
                        "continued_after_entry": round(sum(e_res) / len(e_res), 3) if e_res else None,
                        "n_entry": len(e_res),
                        "continued_after_reaction": round(sum(r_res) / len(r_res), 3) if r_res else None,
                        "n_reaction": len(r_res)}
    return {"config": to_dict(BASELINE), "summary": summary, "gaps": rows}


def main() -> None:
    from .data import fetch_bars

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("symbol")
    ap.add_argument("--timeframe", default="4Hour")
    ap.add_argument("--days", type=int, default=730)
    args = ap.parse_args()
    candles = fetch_bars(args.symbol, args.timeframe, datetime.now(timezone.utc) - timedelta(days=args.days))
    result = run(candles)
    print(f"\n{args.symbol} {args.timeframe}: {len(candles)} candles")
    print(f"{'gaps':16} {'n':>5} {'entered':>8} {'reacted':>8} {'cont. after entry':>18} {'cont. after reaction':>21}")
    for key, s in result["summary"].items():
        ae = f"{s['continued_after_entry']:.1%} (n={s['n_entry']})" if s["continued_after_entry"] is not None else "-"
        ar = f"{s['continued_after_reaction']:.1%} (n={s['n_reaction']})" if s["continued_after_reaction"] is not None else "-"
        print(f"{key:16} {s['gaps']:>5} {s['entered']:>8} {s['reacted']:>8} {ae:>18} {ar:>21}")
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = JOURNAL_DIR / f"day16_fvg_{args.symbol}_{args.timeframe}_{stamp}.json"
    path.write_text(json.dumps({"symbol": args.symbol, "timeframe": args.timeframe, **result}, indent=1))


if __name__ == "__main__":
    main()
