"""The concepts the owner taught, computed causally on one timeframe's candles.

Every result carries ``known``: the 1-minute index at whose close it becomes visible. A consumer
may use it only at or after that index. Definitions follow knowledge/ (closed candles only; highs
and lows are two-candle turns; a break of structure is a body close past the most recent high or
low; a fair value gap is a three-candle void; equilibrium is the 50% of a swing; liquidity rests
beyond highs and lows; an order block is the leg that swept the liquidity).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .market import Frame, Market


@dataclass
class Swing:
    k: int          # frame index of the swing's first candle
    level: float
    side: int       # +1 high, -1 low
    known: int


@dataclass
class Break:
    k: int          # frame index of the breaking candle
    side: int       # +1 broke up, -1 broke down
    level: float
    known: int
    leg_extreme: float  # the extreme of the leg before the break (low before a break up)
    leg_k: int


@dataclass
class Gap:
    k: int          # frame index of the third candle
    side: int
    top: float
    bottom: float
    known: int


@dataclass
class Sweep:
    k: int
    side: int       # -1: took highs (bearish idea), +1: took lows (bullish idea)
    level: float
    extreme: float
    pool: str
    known: int


def swings(f: Frame) -> list[Swing]:
    """[TJR Day 6] a high = an up candle then a down candle (level: the higher wick of the two); a low the reverse."""
    up, dn = f.c > f.o, f.c < f.o
    out = []
    for k in range(len(f) - 1):
        if up[k] and dn[k + 1]:
            out.append(Swing(k, max(f.h[k], f.h[k + 1]), 1, int(f.known[k + 1])))
        elif dn[k] and up[k + 1]:
            out.append(Swing(k, min(f.l[k], f.l[k + 1]), -1, int(f.known[k + 1])))
    return out


def breaks(f: Frame, sw: list[Swing]) -> tuple[list[Break], np.ndarray]:
    """[TJR Day 6] a candle body closing past the most recent high (low). Returns the breaks and the trend
    after each candle (+1 up, -1 down, 0 none yet), each candle's trend known at its own close."""
    trend = np.zeros(len(f), np.int8)
    out: list[Break] = []
    last_hi = last_lo = None
    j, state = 0, 0
    lo_since, lo_k, hi_since, hi_k = np.inf, 0, -np.inf, 0
    for k in range(len(f)):
        # swings confirmed by the previous candle are usable from this candle on
        while j < len(sw) and sw[j].k + 1 < k:
            if sw[j].side == 1:
                last_hi = sw[j]
            else:
                last_lo = sw[j]
            j += 1
        if f.l[k] < lo_since:
            lo_since, lo_k = f.l[k], k
        if f.h[k] > hi_since:
            hi_since, hi_k = f.h[k], k
        body_hi, body_lo = max(f.o[k], f.c[k]), min(f.o[k], f.c[k])
        if last_hi is not None and f.c[k] > last_hi.level and body_hi > last_hi.level and state != 1:
            out.append(Break(k, 1, last_hi.level, int(f.known[k]), lo_since, lo_k))
            state, hi_since, hi_k = 1, f.h[k], k
            lo_since, lo_k = f.l[k], k
        elif last_lo is not None and f.c[k] < last_lo.level and body_lo < last_lo.level and state != -1:
            out.append(Break(k, -1, last_lo.level, int(f.known[k]), hi_since, hi_k))
            state, lo_since, lo_k = -1, f.l[k], k
            hi_since, hi_k = f.h[k], k
        trend[k] = state
    return out, trend


def gaps(f: Frame) -> list[Gap]:
    """[TJR Day 16] bullish: candle 3's low above candle 1's high; bearish: candle 3's high below candle 1's low."""
    out = []
    for k in range(2, len(f)):
        if f.l[k] > f.h[k - 2]:
            out.append(Gap(k, 1, f.l[k], f.h[k - 2], int(f.known[k])))
        elif f.h[k] < f.l[k - 2]:
            out.append(Gap(k, -1, f.l[k - 2], f.h[k], int(f.known[k])))
    return out


def pivots(f: Frame, n: int = 5) -> list[Swing]:
    """Prominent highs/lows [Bot stand-in for TJR's 'prominent', Day 12]: higher (lower) than n candles each side;
    known only after the n candles to its right have closed."""
    out = []
    for k in range(n, len(f) - n):
        win_h, win_l = f.h[k - n:k + n + 1], f.l[k - n:k + n + 1]
        if f.h[k] == win_h.max() and (win_h == f.h[k]).sum() == 1:
            out.append(Swing(k, float(f.h[k]), 1, int(f.known[k + n])))
        if f.l[k] == win_l.min() and (win_l == f.l[k]).sum() == 1:
            out.append(Swing(k, float(f.l[k]), -1, int(f.known[k + n])))
    return out


@dataclass
class Pools:
    """Liquidity levels by 1-minute index of availability: (known, level, side, name, valid_until)."""
    items: list[tuple[int, float, int, str, int]] = field(default_factory=list)


def session_pools(m: Market) -> Pools:
    """The previous trading day's high and low, and each session's high and low (Asia, London, New York),
    each known once that day/session has ended and valid until the end of the next trading day."""
    from .market import SESSIONS
    p = Pools()
    D = m.frames["D"]
    for k in range(len(D) - 1):
        nxt_end = int(D.last[k + 1])
        p.items.append((int(D.known[k]), float(D.h[k]), 1, "previous day high", nxt_end))
        p.items.append((int(D.known[k]), float(D.l[k]), -1, "previous day low", nxt_end))
    for d in m.days:
        a, b = m.day_first[int(d)], m.day_last[int(d)]
        mins = m.mins[a:b + 1]
        for name, (s, e) in SESSIONS.items():
            idx = np.nonzero((mins >= s) & (mins < e))[0]
            if len(idx) < 10:
                continue
            i0, i1 = a + idx[0], a + idx[-1]
            nxt = m.day_last[int(m.days[np.searchsorted(m.days, d) + 1])] if np.searchsorted(m.days, d) + 1 < len(m.days) else b
            p.items.append((int(i1), float(m.h[i0:i1 + 1].max()), 1, f"{name} high", int(nxt)))
            p.items.append((int(i1), float(m.l[i0:i1 + 1].min()), -1, f"{name} low", int(nxt)))
    p.items.sort()
    return p


def sweeps(m: Market, f: Frame, pools: Pools, piv: list[Swing] | None = None, max_pool_age: int = 0) -> list[Sweep]:
    """[TJR Days 8-12] a candle whose wick takes a liquidity level and whose body closes back inside.
    A level must be known before the candle opens, and is used once."""
    events = [(kn, lvl, side, name, until) for kn, lvl, side, name, until in pools.items]
    if piv:
        events += [(s.known, s.level, s.side, "prominent " + ("high" if s.side == 1 else "low"), 10 ** 12) for s in piv]
    events.sort()
    out, active, j = [], [], 0
    for k in range(len(f)):
        start = int(f.first[k])
        while j < len(events) and events[j][0] < start:
            active.append(list(events[j]) + [False])
            j += 1
        if len(active) > 60:
            active = [a for a in active if not a[5] and a[4] >= start][-60:]
        for a in active:
            kn, lvl, side, name, until, used = a
            if used or until < start:
                continue
            if side == 1 and f.h[k] > lvl:
                a[5] = True
                if f.c[k] < lvl:
                    out.append(Sweep(k, -1, lvl, float(f.h[k]), name, int(f.known[k])))
            elif side == -1 and f.l[k] < lvl:
                a[5] = True
                if f.c[k] > lvl:
                    out.append(Sweep(k, 1, lvl, float(f.l[k]), name, int(f.known[k])))
    return out
