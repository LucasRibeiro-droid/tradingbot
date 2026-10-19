"""Day 2 homework, done by the bot: find candle reads on a chart and record how price reacted.

TJR (Day 2, 20:30): "find at least 10 examples ... not only find examples of this on the
chart but find how price ended up reacting off of these examples."

For every readable closed candle the bot records what happened over the next
``horizon_bars`` candles, then compares each read against the base rate of all
candles on the same chart. That comparison is the control: a read only "works"
if it beats what price did anyway.

Usage:
    python -m tradingbot.study SPY --timeframe 5Min --days 30
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Sequence

from .candles import BEARISH, BULLISH, NEUTRAL, Candle, read
from .config import BASELINE, Config, to_dict

JOURNAL_DIR = Path(__file__).resolve().parent.parent / "journal" / "studies"


def reaction(candles: Sequence[Candle], i: int, horizon: int) -> dict | None:
    """What price did after ``candles[i]`` closed, or None if the window is incomplete."""
    window = [c for c in candles[i + 1:i + 1 + horizon] if c.closed]
    if len(window) < horizon:
        return None
    base = candles[i]
    scale = base.range or 1.0
    # Which side of the candle got taken first ("rallies higher, takes out these highs", 18:23).
    first_taken = None
    for c in window:
        took_high, took_low = c.h > base.h, c.l < base.l
        if took_high and took_low:
            first_taken = "both"  # same bar: order unknown
            break
        if took_high or took_low:
            first_taken = "high" if took_high else "low"
            break
    return {
        "move": (window[-1].c - base.c) / scale,  # in multiples of the signal candle's range
        "first_taken": first_taken,
    }


def agrees(lean: int, r: dict) -> bool:
    if lean == BULLISH:
        return r["move"] > 0
    if lean == BEARISH:
        return r["move"] < 0
    return False


def run(candles: Sequence[Candle], config: Config = BASELINE) -> dict:
    horizon = config.study.horizon_bars
    rows = []
    base = {"up": 0, "down": 0, "n": 0}
    for i in range(len(candles)):
        if not candles[i].closed:
            continue
        r = reaction(candles, i, horizon)
        if r is None:
            continue
        base["n"] += 1
        if r["move"] > 0:
            base["up"] += 1
        elif r["move"] < 0:
            base["down"] += 1
        cr = read(candles, i, config.candle)
        if not cr.readable or cr.lean == NEUTRAL:
            continue
        took_expected = r["first_taken"] == ("high" if cr.lean == BULLISH else "low")
        rows.append({"t": candles[i].t, "shape": cr.shape, "kind": cr.kind, "lean": cr.lean, "strength": cr.strength,
                     "notes": list(cr.notes), "move": round(r["move"], 3),
                     "first_taken": r["first_taken"], "agreed": agrees(cr.lean, r),
                     "took_expected_side_first": took_expected})

    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        side = "bull" if row["lean"] == BULLISH else "bear"
        groups[f"ALL:{side}"].append(row)
        groups[f"kind={row['kind']}:{side}"].append(row)
        groups[f"shape={row['shape']}:{side}"].append(row)

    base_up = base["up"] / base["n"] if base["n"] else 0.0
    base_down = base["down"] / base["n"] if base["n"] else 0.0
    summary = {}
    for key, g in sorted(groups.items()):
        base_rate = base_up if key.endswith(":bull") else base_down
        hit = sum(r["agreed"] for r in g) / len(g)
        summary[key] = {
            "n": len(g),
            "hit_rate": round(hit, 3),
            "base_rate": round(base_rate, 3),
            "edge": round(hit - base_rate, 3),
            "took_expected_side_first": round(sum(r["took_expected_side_first"] for r in g) / len(g), 3),
            "avg_move_in_lean_direction": round(sum(r["move"] * r["lean"] for r in g) / len(g), 3),
            "enough_examples": len(g) >= config.study.min_examples,
        }
    return {"config": to_dict(config), "candles": len(candles), "base": base,
            "summary": summary, "examples": rows}


def save(result: dict, symbol: str, timeframe: str) -> Path:
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = JOURNAL_DIR / f"day02_{symbol}_{timeframe}_{stamp}.json"
    path.write_text(json.dumps({"symbol": symbol, "timeframe": timeframe, **result}, indent=1))
    return path


def print_summary(result: dict, symbol: str, timeframe: str) -> None:
    print(f"\n{symbol} {timeframe}: {result['candles']} candles, "
          f"horizon {result['config']['study']['horizon_bars']} bars, config {result['config']['version']}")
    print(f"{'read':32} {'n':>5} {'hit':>6} {'base':>6} {'edge':>7} {'side1st':>8} {'avgmove':>8}")
    for key, s in result["summary"].items():
        flag = "" if s["enough_examples"] else "  (fewer than 10 examples)"
        print(f"{key:32} {s['n']:>5} {s['hit_rate']:>6.1%} {s['base_rate']:>6.1%} {s['edge']:>+7.1%} "
              f"{s['took_expected_side_first']:>8.1%} {s['avg_move_in_lean_direction']:>+8.2f}{flag}")


def main() -> None:
    from .data import fetch_bars

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("symbol")
    ap.add_argument("--timeframe", default="5Min")
    ap.add_argument("--days", type=int, default=30, help="calendar days of history")
    args = ap.parse_args()

    start = datetime.now(timezone.utc) - timedelta(days=args.days)
    candles = fetch_bars(args.symbol, args.timeframe, start)
    result = run(candles)
    print_summary(result, args.symbol, args.timeframe)
    print(f"\nsaved {save(result, args.symbol, args.timeframe)}")


if __name__ == "__main__":
    main()
