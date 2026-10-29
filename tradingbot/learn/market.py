"""One instrument's market as the bot lives through it: 1-minute bid/ask candles, the trading day
(18:00 -> 17:00 New York, the futures day), sessions, and higher-timeframe candles that exist only
once they have closed.

Every higher-timeframe candle carries ``known`` = the index of the 1-minute candle whose close
completes it. Anything computed from a candle is usable from ``known`` onwards, never earlier:
that is the engine's no-lookahead rule, checked by tests/test_learn_lookahead.py.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import numpy as np

NY = ZoneInfo("America/New_York")
# minutes after 18:00 New York (the start of the trading day) for each named session
SESSIONS = {"asia": (0, 540), "london": (540, 840), "newyork": (930, 1380)}  # 18:00-03:00, 03:00-08:00, 09:30-17:00
TIMEFRAMES = {"5m": 5, "15m": 15, "1h": 60, "4h": 240}


@dataclass
class Frame:
    """Candles of one timeframe (mid prices). ``first``/``last``: 1-minute indexes they span;
    ``known``: index of the 1-minute candle at whose close the candle is complete."""
    t: np.ndarray
    o: np.ndarray
    h: np.ndarray
    l: np.ndarray
    c: np.ndarray
    first: np.ndarray
    last: np.ndarray
    known: np.ndarray
    day: np.ndarray

    def __len__(self) -> int:
        return len(self.t)


class Market:
    def __init__(self, inst: str, raw: np.ndarray):
        self.inst = inst
        self.t = raw[:, 0].astype(np.int64)
        self.bo, self.bh, self.bl, self.bc = raw[:, 1], raw[:, 2], raw[:, 3], raw[:, 4]
        self.ao, self.ah, self.al, self.ac = raw[:, 5], raw[:, 6], raw[:, 7], raw[:, 8]
        self.o, self.h, self.l, self.c = ((raw[:, 1] + raw[:, 5]) / 2, (raw[:, 2] + raw[:, 6]) / 2,
                                          (raw[:, 3] + raw[:, 7]) / 2, (raw[:, 4] + raw[:, 8]) / 2)
        self.spread = raw[:, 8] - raw[:, 4]
        # minutes since 18:00 New York, and the trading day (the New York date the session ends on)
        ny_min, day = np.empty(len(raw), np.int32), np.empty(len(raw), np.int32)
        cache: dict[int, tuple[int, int]] = {}
        for k, ts in enumerate(self.t):
            hour_key = int(ts // 3600)
            if hour_key not in cache:
                n = datetime.fromtimestamp(hour_key * 3600, timezone.utc).astimezone(NY)
                m0 = (n.hour * 60 + n.minute - 1080) % 1440
                d = n.date().toordinal() + (1 if n.hour >= 18 else 0)
                cache[hour_key] = (m0, d)
            m0, d = cache[hour_key]
            ny_min[k] = m0 + (ts % 3600) // 60
            day[k] = d
        self.mins, self.day = ny_min, day
        self.days = np.unique(day)
        self.day_first = {int(d): int(i) for d, i in zip(*np.unique(day, return_index=True))}
        self.day_last = {int(d): int(i) for d, i in zip(self.days, np.r_[np.unique(day, return_index=True)[1][1:] - 1, len(day) - 1])}
        self.frames = {name: self._aggregate(n) for name, n in TIMEFRAMES.items()}
        self.frames["1m"] = Frame(self.t, self.o, self.h, self.l, self.c, np.arange(len(raw)), np.arange(len(raw)),
                                  np.arange(len(raw)), self.day)
        self.frames["D"] = self._daily()

    def _aggregate(self, n: int) -> Frame:
        """Candles of ``n`` minutes aligned to 18:00 New York; a bucket is complete when its last
        minute closes, or (for the last bucket of a day) at the day's last minute."""
        key = self.day.astype(np.int64) * 10000 + self.mins // n
        starts = np.r_[0, np.nonzero(np.diff(key))[0] + 1]
        ends = np.r_[starts[1:] - 1, len(key) - 1]
        h = np.maximum.reduceat(self.h, starts)
        l = np.minimum.reduceat(self.l, starts)
        return Frame(self.t[starts], self.o[starts], h, l, self.c[ends], starts, ends, ends, self.day[starts])

    def _daily(self) -> Frame:
        starts = np.array([self.day_first[int(d)] for d in self.days])
        ends = np.array([self.day_last[int(d)] for d in self.days])
        return Frame(self.t[starts], self.o[starts], np.maximum.reduceat(self.h, starts), np.minimum.reduceat(self.l, starts),
                     self.c[ends], starts, ends, ends, self.days.astype(np.int32))

    def session_of(self, i: int) -> str:
        m = int(self.mins[i])
        for name, (a, b) in SESSIONS.items():
            if a <= m < b:
                return name
        return "between"

    def when(self, i: int) -> str:
        return datetime.fromtimestamp(int(self.t[i]), timezone.utc).astimezone(NY).strftime("%Y-%m-%d %H:%M")


def date_of(day: int) -> str:
    from datetime import date
    return date.fromordinal(int(day)).isoformat()
