"""Setups the bot can trade, built from the owner's concepts. Each produces Signals: a decision taken at the
close of a 1-minute candle (``known``) using only what was visible then.

Families (the bot combines them; the learner decides which to keep):
  - crt:        the owner's CRT 1h -> 5m, exactly as live (crt_owner.orders_for, clock hours, 24h day,
                stop at the gap's middle candle, half at 1:1, half at 3R, stops under 3 spreads skipped)
  - sweep_bos:  a liquidity sweep then a break of structure the other way (reversal), on 1m/5m/15m, with
                the entry at the break, at the gap the move left, at the order block, or at equilibrium
  - continuation: a higher-timeframe trend, price retraces into a higher-timeframe fair value gap, a
                lower-timeframe break back in the trend's direction
  - opening_range: a session's opening range (Asia 18:00, London 03:00, New York 09:30), a break, a retest
                of the midpoint, a close back outside
Every signal carries tags (session, higher-timeframe trends, daily bias, discount/premium, pool...) that
the learner may use as filters.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from . import concepts as C
from .market import SESSIONS, Market


@dataclass
class Signal:
    inst: str
    family: str
    base: str            # family + structural parameters (no target)
    side: int
    known: int           # 1-minute index of the decision (at its close)
    kind: str            # "market" (next candle's open) or "limit"
    entry: float         # limit price (or the reference price for market)
    stop: float
    expiry: int          # last 1-minute index a limit may fill
    tags: dict = field(default_factory=dict)
    why: str = ""
    targets: tuple | None = None  # fixed (r1, r2) halves for CRT; None = the learner's target choice


def _trend_at(frame, trend: np.ndarray, i: int) -> int:
    """Trend of the last candle of ``frame`` complete at 1-minute index i (known <= i)."""
    k = int(np.searchsorted(frame.known, i, side="right")) - 1
    return int(trend[k]) if k >= 0 else 0


class Context:
    """Higher-timeframe facts for tagging, all looked up as of a 1-minute index."""

    def __init__(self, m: Market):
        self.m = m
        self.tr = {}
        for tf in ("15m", "1h", "4h", "D"):
            f = m.frames[tf]
            _, self.tr[tf] = C.breaks(f, C.swings(f))

    def tags(self, i: int, side: int) -> dict:
        m = self.m
        t = {"session": m.session_of(i), "hour": int((m.mins[i] // 60 + 18) % 24)}
        for tf in ("15m", "1h", "4h", "D"):
            d = _trend_at(m.frames[tf], self.tr[tf], i)
            t["with_" + tf] = d == side
            t["against_" + tf] = d == -side
        # premium/discount of the current price within the trading day's range so far
        a = m.day_first[int(m.day[i])]
        hi, lo = m.h[a:i + 1].max(), m.l[a:i + 1].min()
        pos = (m.c[i] - lo) / (hi - lo) if hi > lo else 0.5
        t["discount"] = bool(pos < 0.5) if side == 1 else bool(pos > 0.5)
        t["spread"] = float(m.spread[i])
        return t


def _day_end(m: Market, i: int) -> int:
    return m.day_last[int(m.day[i])]


def sweep_bos(m: Market, ctx: Context, tf: str, pools: C.Pools, use_pivots: bool, window: int = 12) -> list[Signal]:
    f = m.frames[tf]
    sw = C.swings(f)
    brk, _ = C.breaks(f, sw)
    piv = C.pivots(f) if use_pivots else None
    sweeps = C.sweeps(m, f, pools, piv)
    gp = C.gaps(f)
    gk = np.array([g.k for g in gp]) if gp else np.array([], int)
    bk = np.array([b.k for b in brk]) if brk else np.array([], int)
    out = []
    pool_kind = "pivots+sessions" if use_pivots else "sessions"
    for s in sweeps:
        # the first break the other way within `window` candles after the sweep
        j = int(np.searchsorted(bk, s.k))
        b = None
        while j < len(brk) and brk[j].k <= s.k + window:
            if brk[j].side == s.side:
                b = brk[j]
                break
            j += 1
        if b is None:
            continue
        i = b.known
        side = s.side
        stop = s.extreme - side * float(m.spread[i])
        hi_leg = f.h[s.k:b.k + 1].max() if side == 1 else f.l[s.k:b.k + 1].min()
        tags = ctx.tags(i, side) | {"pool": s.pool, "tf": tf}
        why = (f"{tf}: {s.pool} {s.level:.2f} swept to {s.extreme:.2f} and closed back inside, then a break of structure "
               f"{'up' if side == 1 else 'down'} through {b.level:.2f}")
        base = f"sweep_bos|{tf}|{pool_kind}"
        expiry = min(_day_end(m, i), int(f.known[min(b.k + 24, len(f) - 1)]))
        out.append(Signal(m.inst, "sweep_bos", base + "|at_break", side, i, "market", float(m.c[i]), stop, i, tags,
                          why + "; entry at the break's close"))
        # the gap the move left, between the sweep and the break
        a0, a1 = int(np.searchsorted(gk, s.k)), int(np.searchsorted(gk, b.k, side="right"))
        g = next((gp[x] for x in range(a1 - 1, a0 - 1, -1) if gp[x].side == side), None)
        if g is not None:
            px = g.top if side == 1 else g.bottom
            out.append(Signal(m.inst, "sweep_bos", base + "|at_gap", side, i, "limit", float(px), stop, expiry, tags,
                              why + f"; limit at the {tf} fair value gap {g.bottom:.2f}-{g.top:.2f} the move left"))
        # the order block: the sweeping candle, from its body to its wick
        ob = max(f.o[s.k], f.c[s.k]) if side == -1 else min(f.o[s.k], f.c[s.k])
        out.append(Signal(m.inst, "sweep_bos", base + "|at_block", side, i, "limit", float(ob), stop, expiry, tags,
                          why + f"; limit at the order block (the sweeping candle's body edge {ob:.2f})"))
        eq = (s.extreme + hi_leg) / 2
        out.append(Signal(m.inst, "sweep_bos", base + "|at_equilibrium", side, i, "limit", float(eq), stop, expiry, tags,
                          why + f"; limit at equilibrium {eq:.2f} (50% of the sweep-to-break leg)"))
    return out


def continuation(m: Market, ctx: Context, htf: str, ltf: str) -> list[Signal]:
    H, L = m.frames[htf], m.frames[ltf]
    hsw = C.swings(H)
    hbrk, htrend = C.breaks(H, hsw)
    hgaps = C.gaps(H)
    lbrk, _ = C.breaks(L, C.swings(L))
    gknown = np.array([g.known for g in hgaps])
    out = []
    for b in lbrk:
        i = b.known
        d = _trend_at(H, htrend, i)
        if d == 0 or b.side != d:
            continue
        # higher-timeframe gaps in the trend's direction visible now, the most recent few
        n = int(np.searchsorted(gknown, i, side="right"))
        for g in reversed(hgaps[max(0, n - 6):n]):
            if g.side != d:
                continue
            touched = (b.leg_extreme <= g.top and b.leg_extreme >= g.bottom - (g.top - g.bottom)) if d == 1 else \
                      (b.leg_extreme >= g.bottom and b.leg_extreme <= g.top + (g.top - g.bottom))
            if not touched:
                continue
            stop = b.leg_extreme - d * float(m.spread[i])
            tags = ctx.tags(i, d) | {"tf": f"{htf}>{ltf}"}
            why = (f"{htf} trend {'up' if d == 1 else 'down'}; price retraced into the {htf} fair value gap "
                   f"{g.bottom:.2f}-{g.top:.2f}; {ltf} break of structure back {'up' if d == 1 else 'down'} through {b.level:.2f}")
            out.append(Signal(m.inst, "continuation", f"continuation|{htf}>{ltf}", d, i, "market", float(m.c[i]), stop, i, tags, why))
            break
    return out


def opening_range(m: Market, ctx: Context, session: str, minutes: int, stop_mode: str) -> list[Signal]:
    """The session's first `minutes`: the box. A 1-minute close outside it (the break), later a candle that
    reaches the midpoint and closes back outside (the retest): enter. First retest only, within 3 hours."""
    out = []
    s0 = SESSIONS[session][0]
    for d in m.days:
        a, b = m.day_first[int(d)], m.day_last[int(d)]
        mins = m.mins[a:b + 1]
        idx = np.nonzero((mins >= s0) & (mins < s0 + minutes))[0]
        if len(idx) < minutes * 0.6:
            continue
        o0, o1 = a + idx[0], a + idx[-1]
        hi, lo = float(m.h[o0:o1 + 1].max()), float(m.l[o0:o1 + 1].min())
        mid = (hi + lo) / 2
        broke = 0
        end = min(b, o1 + 180)
        for i in range(o1 + 1, end + 1):
            if broke == 0:
                if m.c[i] > hi:
                    broke = 1
                elif m.c[i] < lo:
                    broke = -1
                continue
            if broke == 1 and m.l[i] <= mid and m.c[i] > hi or broke == -1 and m.h[i] >= mid and m.c[i] < lo:
                side = broke
                stop = (mid if stop_mode == "mid" else (lo if side == 1 else hi)) - side * float(m.spread[i])
                tags = ctx.tags(i, side) | {"tf": "1m"}
                why = (f"{session} opening range ({minutes} min) {lo:.2f}-{hi:.2f}, midpoint {mid:.2f}: broke "
                       f"{'up' if side == 1 else 'down'}, came back to the midpoint and closed back outside")
                out.append(Signal(m.inst, "opening_range", f"opening_range|{session}|{minutes}m|stop_{stop_mode}", side, i,
                                  "market", float(m.c[i]), stop, i, tags, why))
                break
    return out


def crt(m: Market, ctx: Context) -> list[Signal]:
    """The owner's CRT 1h -> 5m, exactly the live rules (crt_owner.orders_for on clock hours, 24h day)."""
    from ..candles import Candle
    from ..live.crt_owner import orders_for
    from datetime import datetime, timezone
    F = m.frames["5m"]
    bars = [Candle(datetime.fromtimestamp(int(F.t[k]), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                   float(F.o[k]), float(F.h[k]), float(F.l[k]), float(F.c[k])) for k in range(len(F))]
    orders, _ = orders_for(m.inst, bars, round_the_clock=True)
    out = []
    for o in orders:
        i = int(F.known[o.placed - 1])          # decided when the gap's third candle closed
        if 3 * float(m.spread[i]) > abs(o.entry - o.stop):
            continue                            # live rule: stops under 3 spreads are skipped
        tags = ctx.tags(i, o.direction) | {"tf": "1h>5m"}
        why = (f"CRT: 1-hour range candle swept by the next and closed back inside (setup {o.setup_t}); 5-minute fair value gap "
               f"inside the third candle; limit at {o.entry:.2f}, stop at the gap's middle candle {o.stop:.2f}")
        out.append(Signal(m.inst, "crt", "crt|1h>5m", o.direction, i, "limit", float(o.entry), float(o.stop),
                          int(F.last[o.expires]), tags, why, targets=(1.0, 3.0)))
    return out


def all_signals(m: Market) -> list[Signal]:
    ctx = Context(m)
    pools = C.session_pools(m)
    sig = crt(m, ctx)
    for tf, piv in (("1m", False), ("5m", False), ("5m", True), ("15m", True)):
        sig += sweep_bos(m, ctx, tf, pools, piv)
    for htf, ltf in (("1h", "5m"), ("4h", "15m"), ("4h", "5m"), ("1h", "1m")):
        sig += continuation(m, ctx, htf, ltf)
    for sess in ("asia", "london", "newyork"):
        for mins in (5, 15, 30):
            for mode in ("mid", "box"):
                sig += opening_range(m, ctx, sess, mins, mode)
    sig.sort(key=lambda s: s.known)
    return sig
