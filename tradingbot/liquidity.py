"""Days 8, 10 and 12 — Liquidity: why price moves, where the orders rest, and how to trade it.

Sources: TJR Boot Camp Day 8: Liquidity Pt 1 (https://www.youtube.com/watch?v=Lxnu7InGhGE),
Day 10: Liquidity Pt 2 (https://www.youtube.com/watch?v=rdz6vnXb8wE) and
Day 12: Liquidity Pt 3 (https://www.youtube.com/watch?v=KtC2SbemF6w).
The three lessons together: knowledge/liquidity.md.

Liquidity is resting orders: stops and limit orders waiting at a price (Day 8, 02:20).
They sit above highs (buy stops of breakout traders, stop losses of shorts) and below
lows (sell stops, stop losses of longs) (Day 10, 02:49-07:14). Banks push price into
them to fill large orders; once filled, price turns. The trader's confirmation is a
break of structure the other way (Day 8, 07:04-09:36). Liquidity on the other side is
where price is drawn to next, like a magnet, so it is the target (Day 12, 05:56-10:22).
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


@dataclass(frozen=True)
class TradePlan:
    """A liquidity trade (Days 8, 10, 12): sweep, break of structure, target the other side."""

    index: int  # the break-of-structure candle; entry at its close
    direction: int
    entry: float
    stop: float  # beyond the extreme of the sweep: where the idea is wrong
    target: float  # the nearest untaken pool on the other side (Day 12, 10:12)

    @property
    def reward_to_risk(self) -> float:
        return abs(self.target - self.entry) / abs(self.entry - self.stop)


def plan(candles: Sequence[Candle], states: Sequence[TrendState],
         scanned: Sequence[tuple[Taken, tuple[Pool, ...]]], i: int, direction: int,
         p: LiquidityParams = LiquidityParams()) -> TradePlan | None:
    """The trade at break-of-structure candle ``i`` in ``direction``, or None without a target.

    Entry at the break's close: TJR waits for a pullback into a fair value gap or order block
    (Day 12, 10:54-11:20; Days 14-24), which the bot doesn't know yet. Stop beyond the most
    extreme price of the last ``sweep_lookback`` candles, which includes the sweep. Target
    the nearest untaken pool beyond the entry: liquidity is the magnet (Day 12, 11:20).
    """
    if direction == NONE:
        return None
    window = candles[max(0, i - p.sweep_lookback + 1):i + 1]
    entry = candles[i].c
    pools = scanned[i][1]
    if direction == UP:
        stop = min(c.l for c in window)
        above = [x.price for x in pools if x.side == "buy_side" and x.price > entry]
        target = min(above) if above else None
    else:
        stop = max(c.h for c in window)
        below = [x.price for x in pools if x.side == "sell_side" and x.price < entry]
        target = max(below) if below else None
    if target is None or stop == entry:
        return None
    return TradePlan(i, direction, entry, stop, target)


def simulate(candles: Sequence[Candle], tp: TradePlan, max_bars: int) -> dict | None:
    """Follow the plan exactly: +reward/risk if the target is hit first, -1 if the stop is.

    A candle that touches both counts as the stop (we can't know which came first). After
    ``max_bars`` candles the trade is closed at that close. None if the data runs out first.
    """
    risk = abs(tp.entry - tp.stop)
    after = candles[tp.index + 1:tp.index + 1 + max_bars]
    for n, c in enumerate(after, 1):
        if not c.closed:
            return None
        hit_stop = c.l <= tp.stop if tp.direction == UP else c.h >= tp.stop
        hit_target = c.h >= tp.target if tp.direction == UP else c.l <= tp.target
        if hit_stop:
            return {"r": -1.0, "exit": "stop", "bars": n}
        if hit_target:
            return {"r": round(tp.reward_to_risk, 3), "exit": "target", "bars": n}
    if len(after) < max_bars:
        return None
    return {"r": round((after[-1].c - tp.entry) * tp.direction / risk, 3), "exit": "time", "bars": max_bars}
