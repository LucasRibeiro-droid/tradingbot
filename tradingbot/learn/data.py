"""OANDA 1-minute bid/ask history for NAS100_USD and XAU_USD, cached per month.

The 2025-01-01 onwards HOLDOUT is locked: nothing in development can load it. Only
``load(..., holdout=True)`` (used once, for the final report) reads it.
"""
from __future__ import annotations

import pickle
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

CACHE = Path.home() / ".cache" / "tradingbot" / "learn"
INSTRUMENTS = ("NAS100_USD", "XAU_USD")
DEV_START = datetime(2021, 1, 3, 22, 0, tzinfo=timezone.utc)   # Sunday 17:00 NY: the week before Jan 4
HOLDOUT_START = datetime(2025, 1, 1, tzinfo=timezone.utc)


class HoldoutLocked(RuntimeError):
    pass


def _month_file(inst: str, y: int, m: int) -> Path:
    return CACHE / f"{inst}_M1_{y:04d}{m:02d}.npy"


def fetch_month(practice, inst: str, y: int, m: int, holdout: bool = False) -> np.ndarray:
    """Columns: epoch seconds, bid o h l c, ask o h l c."""
    start = datetime(y, m, 1, tzinfo=timezone.utc)
    end = datetime(y + (m == 12), m % 12 + 1, 1, tzinfo=timezone.utc)
    if end > HOLDOUT_START and not holdout:
        raise HoldoutLocked(f"{inst} {y}-{m:02d} is in the locked holdout")
    f = _month_file(inst, y, m)
    if f.exists():
        return np.load(f)
    CACHE.mkdir(parents=True, exist_ok=True)
    rows, frm = [], start
    while frm < end:
        q = urllib.parse.urlencode({"granularity": "M1", "price": "BA", "count": 5000,
                                    "from": frm.strftime("%Y-%m-%dT%H:%M:%S.000000000Z")})
        got = practice._call("GET", f"/v3/instruments/{inst}/candles?{q}")["candles"]
        new = 0
        for c in got:
            t = datetime.fromisoformat(c["time"][:19] + "+00:00")
            if t >= end:
                break
            if not c["complete"] or (rows and t.timestamp() <= rows[-1][0]):
                continue
            b, a = c["bid"], c["ask"]
            rows.append((t.timestamp(), float(b["o"]), float(b["h"]), float(b["l"]), float(b["c"]),
                         float(a["o"]), float(a["h"]), float(a["l"]), float(a["c"])))
            new += 1
        if len(got) < 5000 or not new:
            break
        frm = datetime.fromtimestamp(rows[-1][0], timezone.utc) + timedelta(seconds=1)
    arr = np.array(rows, dtype=np.float64)
    if end <= datetime.now(timezone.utc) - timedelta(days=2):
        np.save(f, arr)
    return arr


def load(inst: str, start: datetime = DEV_START, end: datetime = HOLDOUT_START, holdout: bool = False) -> np.ndarray:
    if end > HOLDOUT_START and not holdout:
        raise HoldoutLocked("development code may not read 2025-01-01 onwards")
    if start >= HOLDOUT_START and not holdout:
        raise HoldoutLocked("development code may not read 2025-01-01 onwards")
    parts = []
    y, m = start.year, start.month
    while datetime(y, m, 1, tzinfo=timezone.utc) < end:
        f = _month_file(inst, y, m)
        if not f.exists():
            raise FileNotFoundError(f"{f} missing: run python -m tradingbot.learn.data")
        parts.append(np.load(f))
        y, m = y + (m == 12), m % 12 + 1
    a = np.concatenate(parts)
    return a[(a[:, 0] >= start.timestamp()) & (a[:, 0] < end.timestamp())]


def main() -> None:
    from ..live.oanda import Practice
    p = Practice()
    for inst in INSTRUMENTS:
        for y in range(2021, 2025):
            for m in range(1, 13):
                a = fetch_month(p, inst, y, m)
                print(inst, y, m, len(a), flush=True)


if __name__ == "__main__":
    main()
