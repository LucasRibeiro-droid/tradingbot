"""H34: does the bot's daily bias lag? Setups "against" it that won may be early entries into
the next daily leg, before the daily break of structure confirms it.

For every setup labelled "against" in the latest `models_study.py --bias` run (TJR's exits,
entry model 1), how many daily candles until the daily breaks structure in the setup's
direction? Compared with:
  - winners vs losers among those setups
  - the base rate: how often the daily flips within the same number of days from any day [Bot]
If H34 holds, the daily flips soon after "against" setups far more often than the base rate,
and more often after the winners. Then the setup isn't against TJR's daily bias at all; the
bot's mechanical reading is late (Day 36, 07:41: a lower-timeframe break can be the start of
the next higher-timeframe leg). TJR's rule stays locked either way.

Usage:
    python -m tradingbot.bias_lag_study
"""
from __future__ import annotations

import glob
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .config import BASELINE
from .trend import _ts, trend_series

JOURNAL_DIR = Path(__file__).resolve().parent.parent / "journal" / "studies"
HORIZONS = (1, 2, 3, 5)


def days_to_flip(daily, states, t: str, side: int, limit: int = 10) -> int | None:
    """Daily candles after ``t`` until the daily breaks structure towards ``side``."""
    when = _ts(t)
    n = 0
    for c, s in zip(daily, states):
        if _ts(c.t) + timedelta(days=1) <= when:
            continue  # already closed when the setup happened
        n += 1
        if s.event == ("bos_up" if side == 1 else "bos_down"):
            return n
        if n >= limit:
            return None
    return None


def base_rate(daily, states, start: str, horizon: int) -> float:
    """From any day in the period: share of days followed by a daily flip within ``horizon``."""
    idx = [k for k, c in enumerate(daily) if c.t >= start]
    flips = [k for k, s in enumerate(states) if s.event in ("bos_up", "bos_down")]
    hit = sum(any(k < f <= k + horizon for f in flips) for k in idx)
    return hit / len(idx) if idx else 0.0


def main() -> None:
    from .data import fetch_bars

    latest = {}
    for f in sorted(glob.glob(str(JOURNAL_DIR / "bias_tjr_exits_models_*.json"))):
        d = json.load(open(f))
        latest[(d["symbol"], d["timeframe"])] = d
    result = {}
    pooled = {"win": [], "loss": []}
    for (symbol, tf), d in sorted(latest.items()):
        rows = [r for r in d["setups"] if r.get("bias") == "against"
                and r["1x"]["exit"] not in ("missed", "no_entry", "no_target")]
        if not rows:
            continue
        first = min(r["t"] for r in rows)
        daily = fetch_bars(symbol, "1Day", datetime.fromisoformat(first.replace("Z", "+00:00")) - timedelta(days=120),
                           datetime.now(timezone.utc))
        states = trend_series(daily, BASELINE.trend)
        out = {"n": len(rows)}
        for label, group in (("win", [r for r in rows if r["1x"]["r"] > 0]), ("loss", [r for r in rows if r["1x"]["r"] <= 0])):
            ds = [days_to_flip(daily, states, r["t"], r["side"]) for r in group]
            pooled[label] += ds
            out[label] = {f"flip_within_{h}d": round(sum(x is not None and x <= h for x in ds) / len(ds), 3) if ds else None
                          for h in HORIZONS} | {"n": len(ds)}
        out["base"] = {f"flip_within_{h}d": round(base_rate(daily, states, first, h), 3) for h in HORIZONS}
        result[f"{symbol} {tf}"] = out
        print(f"{symbol} {tf}: against n={len(rows)}")
        for label in ("win", "loss", "base"):
            s = out[label]
            print(f"  {label:5} " + "  ".join(f"{h}d {s[f'flip_within_{h}d']:.0%}" if s.get(f'flip_within_{h}d') is not None else f"{h}d -" for h in HORIZONS)
                  + (f"  (n={s['n']})" if "n" in s else ""))
    for label in ("win", "loss"):
        ds = pooled[label]
        result[f"pooled {label}"] = {f"flip_within_{h}d": round(sum(x is not None and x <= h for x in ds) / len(ds), 3) for h in HORIZONS} | {"n": len(ds)}
        print(f"pooled {label}: " + "  ".join(f"{h}d {result[f'pooled {label}'][f'flip_within_{h}d']:.0%}" for h in HORIZONS) + f"  (n={len(ds)})")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    (JOURNAL_DIR / f"h34_bias_lag_{stamp}.json").write_text(json.dumps(result, indent=1))


if __name__ == "__main__":
    main()
