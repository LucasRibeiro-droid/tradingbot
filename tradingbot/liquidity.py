"""Liquidity indicator (Days 8, 10 and 12): where resting orders sit, and when price takes them.

Sources: TJR Boot Camp Day 8: Liquidity Pt 1 (https://www.youtube.com/watch?v=Lxnu7InGhGE),
Day 10: Liquidity Pt 2 (https://www.youtube.com/watch?v=rdz6vnXb8wE) and
Day 12: Liquidity Pt 3 (https://www.youtube.com/watch?v=KtC2SbemF6w).
The three lessons together: knowledge/liquidity.md.

Liquidity is resting orders: stops and limit orders waiting at a price (Day 8, 02:20).
They sit above highs (buy stops of breakout traders, stop losses of shorts) and below
lows (sell stops, stop losses of longs) (Day 10, 02:49-07:14). Banks push price into
them to fill large orders; once filled, price turns. The trader's confirmation is a
break of structure the other way (Day 8, 07:04-09:36). Liquidity on the other side is
where price is drawn to next, like a magnet (Day 12, 05:56-10:22).

This module only reads the chart. What it tells the bot:
  - ``scan``: which pools exist, and which ones each candle took.
  - ``swept_before``: liquidity was just taken on one side, evidence that a reversal the
    other way is likely (but never a reason to trade by itself).
  - ``draw``: the nearest untaken liquidity in a direction, where price is likely headed.
How these combine with the other indicators into buy / sell / nothing is decision.py.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .candles import Candle
from .config import LiquidityParams
from .trend import DOWN, UP


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


def scan(candles: Sequence[Candle], p: LiquidityParams = LiquidityParams()) -> list[tuple[Taken, tuple[Pool, ...]]]:
    """For each candle: the pools it took (Day 10), and the pools still untaken after it closes.

    A pool is taken the first time a later candle trades past it, by wick or close, and is
    gone after that. The untaken ones are the liquidity price is drawn to (Day 12, 05:56).
    """
    found = find_pools(candles, p)
    active: list[Pool] = []
    k = 0
    out = []
    for j, c in enumerate(candles):
        if not c.closed:
            out.append((Taken(), tuple(active)))
            continue
        buy = tuple(x for x in active if x.side == "buy_side" and c.h > x.price)
        sell = tuple(x for x in active if x.side == "sell_side" and c.l < x.price)
        active = [x for x in active if x not in buy and x not in sell]
        while k < len(found) and found[k].confirmed_at <= j:
            active.append(found[k])
            k += 1
        out.append((Taken(buy, sell), tuple(active)))
    return out


def pools_and_takes(candles: Sequence[Candle], p: LiquidityParams = LiquidityParams()) -> list[Taken]:
    """For each candle, the liquidity pools it took (Day 10)."""
    return [t for t, _ in scan(candles, p)]


def swept_before(taken: Sequence[Taken], i: int, direction: int,
                 p: LiquidityParams = LiquidityParams()) -> bool:
    """Was liquidity on the opposite side taken in the last ``sweep_lookback`` candles up to
    ``i``? For an UP move that means a pool below a low (sell-side) was taken, and vice versa.
    That is TJR's precondition for a reversal (Day 8, 07:04)."""
    window = taken[max(0, i - p.sweep_lookback + 1):i + 1]
    if direction == UP:
        return any(t.sell_side for t in window)
    if direction == DOWN:
        return any(t.buy_side for t in window)
    return False


def draw(pools: Sequence[Pool], direction: int, price: float) -> float | None:
    """The nearest untaken liquidity beyond ``price`` in ``direction``: where price is drawn
    to next (Day 12, 05:56). None if there is none."""
    if direction == UP:
        above = [x.price for x in pools if x.side == "buy_side" and x.price > price]
        return min(above) if above else None
    if direction == DOWN:
        below = [x.price for x in pools if x.side == "sell_side" and x.price < price]
        return max(below) if below else None
    return None
