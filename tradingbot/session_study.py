"""Day 7 study: does the US session open fake out, the way TJR's London open did on GBPJPY?

TJR (Day 7, 06:55-07:25) found his own edge by watching the same session every day:
"right when London session opens, it just goes super strong in one direction, but then
immediately flips direction ... it happens every single London session." He calls it the
London session fakeout. The bot trades US stocks, so it asks the same question of the
New York open (9:30 ET) on its own instruments instead of copying TJR's market.

For each day: the direction of the first ``open_minutes`` of the session, then whether
the session closed on the other side of the open (a fakeout). Compared against how often
the close lands on the opposite side of an arbitrary first move by chance: a coin flip
weighted by how often the session closes opposite its own opening direction overall.

Usage:
    python -m tradingbot.session_study SPY --days 730 --open-minutes 15
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from .candles import Candle

NY = ZoneInfo("America/New_York")
SESSION_OPEN, SESSION_CLOSE = time(9, 30), time(16, 0)
JOURNAL_DIR = Path(__file__).resolve().parent.parent / "journal" / "studies"


def sessions(candles: list[Candle]) -> dict[str, list[tuple[datetime, Candle]]]:
    """Regular-session 5-minute candles grouped by New York date."""
    days = defaultdict(list)
    for c in candles:
        t = datetime.fromisoformat(c.t.replace("Z", "+00:00")).astimezone(NY)
        if SESSION_OPEN <= t.time() < SESSION_CLOSE and c.closed:
            days[t.date().isoformat()].append((t, c))
    return days


def run(candles: list[Candle], open_minutes: int) -> dict:
    rows = []
    for day, bars in sorted(sessions(candles).items()):
        if len(bars) < 70:  # skip half days and gaps in the feed
            continue
        first = [c for t, c in bars if t.time() < (datetime.combine(t.date(), SESSION_OPEN)
                                                  + timedelta(minutes=open_minutes)).time()]
        if not first:
            continue
        open_price, early = first[0].o, first[-1].c
        close = bars[-1][1].c
        if early == open_price:
            continue
        direction = 1 if early > open_price else -1
        size = abs(early - open_price) / open_price
        rows.append({"day": day, "first_move": direction, "first_move_pct": round(100 * size, 3),
                     "close_vs_open_pct": round(100 * (close - open_price) / open_price, 3),
                     "fakeout": (close - open_price) * direction < 0})

    def summary(rs):
        if not rs:
            return {"n": 0}
        return {"n": len(rs), "fakeout_rate": round(sum(r["fakeout"] for r in rs) / len(rs), 3)}

    rows_sorted = sorted(rows, key=lambda r: r["first_move_pct"])
    third = len(rows_sorted) // 3
    return {
        "open_minutes": open_minutes,
        "all": summary(rows),
        "first_move_up": summary([r for r in rows if r["first_move"] == 1]),
        "first_move_down": summary([r for r in rows if r["first_move"] == -1]),
        # TJR's fakeout is a *strong* move that flips: compare the biggest opening moves.
        "small_first_moves": summary(rows_sorted[:third]),
        "large_first_moves": summary(rows_sorted[-third:]) if third else {"n": 0},
        "days": rows,
    }


def main() -> None:
    from .data import fetch_bars

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("symbol")
    ap.add_argument("--days", type=int, default=730)
    ap.add_argument("--open-minutes", type=int, default=15)
    args = ap.parse_args()
    candles = fetch_bars(args.symbol, "5Min", datetime.now(timezone.utc) - timedelta(days=args.days))
    result = run(candles, args.open_minutes)
    print(f"{args.symbol}: first {args.open_minutes} minutes of the New York session vs the close")
    for key in ("all", "first_move_up", "first_move_down", "small_first_moves", "large_first_moves"):
        s = result[key]
        print(f"  {key:20} n={s['n']:4}  fakeout rate {s.get('fakeout_rate', 0):.1%}")
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = JOURNAL_DIR / f"day07_session_open_{args.symbol}_{args.open_minutes}m_{stamp}.json"
    path.write_text(json.dumps({"symbol": args.symbol, **result}, indent=1))
    print(f"saved {path}")


if __name__ == "__main__":
    main()
