"""Day 4 homework, done by the bot: predict where price wants to go, write it down, grade it later.

TJR (Day 4, 23:39-27:04): for one or two instruments, say where price wants to go this
week, then over the next couple of days, then today. Journal it. No trade, no stop, just
the direction. The bot grades each call once its horizon has passed, so every prediction
becomes an outcome it can learn from.

Usage:
    python -m tradingbot.forecast make     # today's forecasts for the watchlist
    python -m tradingbot.forecast grade    # grade every forecast whose horizon has passed
"""
from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from .config import BASELINE, LOCKED, Config
from .trend import DOWN, NONE, UP, TrendState, trend_series

FORECAST_DIR = Path(__file__).resolve().parent.parent / "journal" / "forecasts"
WORD = {UP: "up", DOWN: "down", NONE: "no call"}


def _last_closed(states: list[TrendState], candles) -> TrendState:
    for c, s in zip(reversed(candles), reversed(states)):
        if c.closed:
            return s
    raise ValueError("no closed candles")


def call(htf: TrendState, ltf: TrendState) -> dict:
    """One horizon's call: the higher timeframe's direction, and whether the lower agrees."""
    d = htf.tradeable_direction
    note = ("higher timeframe is consolidating: no call" if htf.consolidating else
            "no clear trend yet: no call" if d == NONE else
            "lower timeframe agrees" if ltf.direction == d else
            f"lower timeframe is going {WORD[ltf.direction]}: wait for it to turn {WORD[d]}")
    return {"direction": WORD[d], "note": note}


def make(symbol: str, config: Config = BASELINE, today: date | None = None) -> dict:
    from .data import fetch_bars

    now = datetime.now(timezone.utc)
    weekly = fetch_bars(symbol, "1Week", now - timedelta(days=7 * 150))
    daily = fetch_bars(symbol, "1Day", now - timedelta(days=400))
    hourly = fetch_bars(symbol, "1Hour", now - timedelta(days=30))
    w = _last_closed(trend_series(weekly, config.trend), weekly)
    d = _last_closed(trend_series(daily, config.trend), daily)
    h = _last_closed(trend_series(hourly, config.trend), hourly)
    ref = next(c for c in reversed(hourly) if c.closed)
    return {
        "symbol": symbol,
        "made_at": now.isoformat(timespec="seconds"),
        "date": (today or now.date()).isoformat(),
        "config": config.version,
        "reference": {"t": ref.t, "price": ref.c},
        # Week: weekly trend, checked against the daily. Couple of days: daily, checked
        # against the hourly. Today: the daily bias, timed by the hourly (Day 4, 24:17-26:30).
        "week": call(w, d),
        "next_days": call(d, h),
        "today": call(d, h),
        "grades": {},
    }


def write(forecasts: list[dict], day: str) -> Path:
    FORECAST_DIR.mkdir(parents=True, exist_ok=True)
    path = FORECAST_DIR / f"{day}.json"
    path.write_text(json.dumps(forecasts, indent=1))
    return path


def _target_close(daily, start: date, horizon: str):
    """The daily close a horizon is graded on, or None if it hasn't happened yet."""
    days = [c for c in daily if c.closed and date.fromisoformat(c.t[:10]) >= start]
    if horizon == "today":
        pick = [c for c in days if date.fromisoformat(c.t[:10]) == start]
    elif horizon == "next_days":
        pick = days[2:3]  # the second trading day after today's close
    else:  # week: last close of the same week, once the following week has started
        same = [c for c in days if date.fromisoformat(c.t[:10]).isocalendar()[:2] == start.isocalendar()[:2]]
        later = [c for c in days if date.fromisoformat(c.t[:10]).isocalendar()[:2] > start.isocalendar()[:2]]
        pick = same[-1:] if later else []
    return pick[0] if pick else None


def grade_file(path: Path) -> list[dict]:
    from .data import fetch_bars

    forecasts = json.loads(path.read_text())
    for f in forecasts:
        start = date.fromisoformat(f["date"])
        daily = fetch_bars(f["symbol"], "1Day", datetime.combine(start, datetime.min.time(), timezone.utc))
        for horizon in ("today", "next_days", "week"):
            if horizon in f["grades"] or f[horizon]["direction"] == "no call":
                continue
            target = _target_close(daily, start, horizon)
            if target is None:
                continue
            move = target.c - f["reference"]["price"]
            predicted = 1 if f[horizon]["direction"] == "up" else -1
            f["grades"][horizon] = {"close": target.c, "t": target.t, "move": round(move, 4),
                                    "correct": move * predicted > 0}
    path.write_text(json.dumps(forecasts, indent=1))
    return forecasts


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("action", choices=["make", "grade"])
    args = ap.parse_args()
    if args.action == "make":
        watchlist = BASELINE.watchlist[:LOCKED.max_instruments]
        forecasts = [make(s) for s in watchlist]
        path = write(forecasts, forecasts[0]["date"])
        for f in forecasts:
            print(f"{f['symbol']} @ {f['reference']['price']}: week {f['week']['direction']} "
                  f"({f['week']['note']}); next days {f['next_days']['direction']} "
                  f"({f['next_days']['note']}); today {f['today']['direction']} ({f['today']['note']})")
        print(f"saved {path}")
    else:
        for path in sorted(FORECAST_DIR.glob("*.json")):
            for f in grade_file(path):
                print(path.stem, f["symbol"], {k: v["correct"] for k, v in f["grades"].items()} or "nothing to grade yet")


if __name__ == "__main__":
    main()
