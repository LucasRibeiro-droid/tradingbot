"""Days 8 and 10 — Liquidity: why price moves, where the orders rest, and the sequence TJR trades.

Sources: TJR Boot Camp Day 8: Liquidity Pt 1 (https://www.youtube.com/watch?v=Lxnu7InGhGE)
and Day 10: Liquidity Pt 2 (https://www.youtube.com/watch?v=rdz6vnXb8wE).
Full write-ups: knowledge/day08_liquidity_pt1.md, knowledge/day10_liquidity_pt2.md.

Liquidity is resting orders: stops and limit orders waiting at a price (Day 8, 02:20).
They sit above highs (buy stops of breakout traders, stop losses of shorts) and below
lows (sell stops, stop losses of longs) (Day 10, 02:49-07:14). Banks push price into
them to fill large orders; once filled, price turns. The trader's confirmation is a
break of structure the other way (Day 8, 07:04-09:36). Execution is Day 12.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .candles import Candle
from .config import LiquidityParams
from .trend import DOWN, NONE, UP, TrendState


@dataclass(frozen=True)
class Pool:
    """Resting orders above a clear high ("buy_side") or below a clear low ("sell_side")."""

    index: int
    price: float
    side: str  # "buy_side" (above a high) | "sell_side" (below a low)
    confirmed_at: int


@dataclass(frozen=True)
class Taken:
    """Liquidity this candle took: pools it traded through, by wick or close."""

    buy_side: tuple[Pool, ...] = ()
    sell_side: tuple[Pool, ...] = ()


def find_pools(candles: Sequence[Candle], p: LiquidityParams = LiquidityParams()) -> list[Pool]:
    """Every pool: a high (low) higher (lower) than ``pool_strength`` closed candles on each
    side. It becomes known once those candles have closed."""
    n = p.pool_strength
    found: list[Pool] = []
    for i in range(n, len(candles) - n):
        window = candles[i - n:i + n + 1]
        if not all(c.closed for c in window):
            continue
        c = candles[i]
        if c.h > max(x.h for x in candles[i - n:i]) and c.h >= max(x.h for x in candles[i + 1:i + n + 1]):
            found.append(Pool(i, c.h, "buy_side", i + n))
        if c.l < min(x.l for x in candles[i - n:i]) and c.l <= min(x.l for x in candles[i + 1:i + n + 1]):
            found.append(Pool(i, c.l, "sell_side", i + n))
    return sorted(found, key=lambda x: x.confirmed_at)


def pools_and_takes(candles: Sequence[Candle], p: LiquidityParams = LiquidityParams()) -> list[Taken]:
    """For each candle, the liquidity pools it took (Day 10). A pool is taken the first time a
    later candle trades past it, by wick or close, and is gone after that."""
    found = find_pools(candles, p)
    active: list[Pool] = []
    k = 0
    out = []
    for j, c in enumerate(candles):
        if not c.closed:
            out.append(Taken())
            continue
        buy = tuple(x for x in active if x.side == "buy_side" and c.h > x.price)
        sell = tuple(x for x in active if x.side == "sell_side" and c.l < x.price)
        active = [x for x in active if x not in buy and x not in sell]
        out.append(Taken(buy, sell))
        while k < len(found) and found[k].confirmed_at <= j:
            active.append(found[k])
            k += 1
    return out


def sweep_then_shift(states: Sequence[TrendState], taken: Sequence[Taken], i: int,
                     p: LiquidityParams = LiquidityParams()) -> int:
    """UP if candle ``i`` breaks structure up after sell-side liquidity (below a clear low)
    was taken within ``sweep_lookback`` candles; DOWN for the mirror case; NONE otherwise.
    Price reaching liquidity alone is never enough (Day 8, 08:38)."""
    s = states[i]
    window = taken[max(0, i - p.sweep_lookback + 1):i + 1]
    if s.event == "bos_up" and any(t.sell_side for t in window):
        return UP
    if s.event == "bos_down" and any(t.buy_side for t in window):
        return DOWN
    return NONE
