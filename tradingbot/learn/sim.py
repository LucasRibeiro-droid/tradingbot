"""Fills and exits on the real bid/ask 1-minute path, with slippage and a commission-equivalent.

Long: a market entry fills at the next candle's ask open + slippage; a limit fills when the ask reaches it
(at the limit, or the open if it opens through); the stop triggers on the bid (filled at the stop or the
open beyond it, minus slippage); targets are limit orders on the bid. Shorts mirror on the ask. A candle
that reaches both the stop and a target counts as the stop; the fill candle can stop the trade but can't
reach a target. Everything is closed at the trading day's last minute (16:59 New York): no overnight risk.
R = net result / the risk actually taken (fill to stop).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .market import Market
from .setups import Signal

# per side, in price units: slippage on market/stop fills, and a commission-equivalent on every fill
# (OANDA CFDs charge none; this matches NQ/GC futures, ~$2.25 a side per contract)
COSTS = {"NAS100_USD": {"slip": 0.5, "comm": 0.12}, "XAU_USD": {"slip": 0.05, "comm": 0.025}}
TARGETS = {"0.5R": (0.5, 0.5), "1R": (1.0, 1.0), "2R": (2.0, 2.0), "3R": (3.0, 3.0), "half1R_3R": (1.0, 3.0),
           "half1R_be3R": (1.0, 3.0)}  # _be: after the first half's target, the rest's stop moves to the entry


@dataclass
class Trade:
    signal: Signal
    target: str
    filled: bool
    fill_i: int = -1
    fill: float = 0.0
    exit_i: int = -1
    exits: tuple = ()
    r: float = 0.0
    risk: float = 0.0


def simulate(m: Market, s: Signal, target: str) -> Trade:
    c = COSTS[m.inst]
    d = s.side
    end = m.day_last[int(m.day[s.known])]
    if s.known >= end:
        return Trade(s, target, False)
    # --- entry ---
    if s.kind == "market":
        j0 = s.known + 1
        fill = (m.ao[j0] + c["slip"]) if d == 1 else (m.bo[j0] - c["slip"])
    else:
        hi = min(s.expiry, end)
        seg = slice(s.known + 1, hi + 1)
        hit = (m.al[seg] <= s.entry) if d == 1 else (m.bh[seg] >= s.entry)
        if not hit.any():
            return Trade(s, target, False)
        j0 = s.known + 1 + int(np.argmax(hit))
        fill = min(s.entry, m.ao[j0]) if d == 1 else max(s.entry, m.bo[j0])
    risk = (fill - s.stop) * d
    if risk <= 0:
        return Trade(s, target, False)
    r1, r2 = s.targets if s.targets else TARGETS[target]
    tps = (fill + d * r1 * risk, fill + d * r2 * risk)
    # --- path after the fill (the fill candle can only stop) ---
    if (m.bl[j0] <= s.stop) if d == 1 else (m.ah[j0] >= s.stop):
        exit_px = (min(s.stop, m.bo[j0]) - c["slip"]) if d == 1 else (max(s.stop, m.ao[j0]) + c["slip"])
        exits = ((exit_px, 1.0, "stop", j0),)
    else:
        seg = slice(j0 + 1, end + 1)
        lo, hi, op = (m.bl[seg], m.bh[seg], m.bo[seg]) if d == 1 else (m.ah[seg], m.al[seg], m.ao[seg])
        stop_hit = (lo <= s.stop) if d == 1 else (lo >= s.stop)
        ks = int(np.argmax(stop_hit)) if stop_hit.any() else None
        exits = []
        first_kt = None
        for leg, tp in enumerate(tps):
            tp_hit = (hi >= tp) if d == 1 else (hi <= tp)
            kt = int(np.argmax(tp_hit)) if tp_hit.any() else None
            leg_stop, leg_ks = s.stop, ks
            if leg == 1 and target.endswith("_be") is False and target.endswith("be3R") and first_kt is not None:
                # break even: from the candle after the first target, the stop is the entry price
                be = (lo[first_kt + 1:] <= fill) if d == 1 else (lo[first_kt + 1:] >= fill)
                kbe = first_kt + 1 + int(np.argmax(be)) if be.any() else None
                if ks is not None and ks <= first_kt:
                    kbe = ks
                leg_stop, leg_ks = (fill if (ks is None or ks > first_kt) else s.stop), kbe
            if kt is not None and (leg_ks is None or kt < leg_ks):
                exits.append((tp, 0.5, f"target {r1 if leg == 0 else r2:g}R", j0 + 1 + kt))
                if leg == 0:
                    first_kt = kt
            elif leg_ks is not None:
                px = (min(leg_stop, op[leg_ks]) - c["slip"]) if d == 1 else (max(leg_stop, op[leg_ks]) + c["slip"])
                exits.append((px, 0.5, "break even" if leg_stop == fill else "stop", j0 + 1 + leg_ks))
            else:
                px = (m.bc[end] - c["slip"]) if d == 1 else (m.ac[end] + c["slip"])
                exits.append((px, 0.5, "day end", end))
        exits = tuple(exits)
    gross = sum((px - fill) * d * w for px, w, _, _ in exits)
    net = gross - 2 * c["comm"]
    return Trade(s, target, True, j0, float(fill), max(e[3] for e in exits), exits, float(net / risk), float(risk))
