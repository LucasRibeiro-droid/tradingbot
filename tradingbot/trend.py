"""Day 4 — Trends: where price wants to go, and why higher timeframes decide it.

Source: TJR Boot Camp Day 4 (https://www.youtube.com/watch?v=viuGHEuv0nw).
Full write-up: knowledge/day04_trends.md.

Everything here works bar by bar without looking ahead: a swing point only counts once
the candles that confirm it have closed, and a trend only changes on a candle close.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Sequence

from .candles import Candle
from .config import TrendParams

UP = 1
DOWN = -1
NONE = 0


@dataclass(frozen=True)
class Swing:
    """A swing high or low: a turning point in price (Day 4, 02:13)."""

    index: int
    price: float
    kind: str  # "high" | "low"
    confirmed_at: int  # first bar index at which the swing is known


@dataclass(frozen=True)
class TrendState:
    """The trend as it was known at the close of one candle."""

    direction: int  # UP, DOWN, or NONE before enough swings exist
    consolidating: bool
    swing_high: float | None
    swing_low: float | None
    shifted: bool = False  # this candle's close changed the direction

    @property
    def tradeable_direction(self) -> int:
        """The direction to trade, or NONE when there is no clear trend (Day 4, 12:32)."""
        return NONE if self.consolidating else self.direction


def _hl(c: Candle, source: str) -> tuple[float, float]:
    # "Use the line chart to your advantage" (Day 4, 18:32): swings from closes only.
    return (c.c, c.c) if source == "close" else (c.h, c.l)


def swings(candles: Sequence[Candle], p: TrendParams = TrendParams()) -> list[Swing]:
    """Swing highs and lows: a bar higher (lower) than ``swing_strength`` bars on each side."""
    n = p.swing_strength
    hl = [_hl(c, p.swing_source) for c in candles]
    out = []
    for i in range(n, len(candles) - n):
        if not all(c.closed for c in candles[i - n:i + n + 1]):
            continue
        h, l = hl[i]
        left, right = hl[i - n:i], hl[i + 1:i + n + 1]
        if h > max(x[0] for x in left) and h >= max(x[0] for x in right):
            out.append(Swing(i, h, "high", i + n))
        if l < min(x[1] for x in left) and l <= min(x[1] for x in right):
            out.append(Swing(i, l, "low", i + n))
    return out


def efficiency(candles: Sequence[Candle], end: int, lookback: int) -> float:
    """Net move over the window divided by its high-low range: 1 is a straight line, 0 is chop."""
    window = candles[max(0, end - lookback + 1):end + 1]
    if len(window) < 2:
        return 1.0
    span = max(c.h for c in window) - min(c.l for c in window)
    return abs(window[-1].c - window[0].o) / span if span > 0 else 0.0


def trend_series(candles: Sequence[Candle], p: TrendParams = TrendParams()) -> list[TrendState]:
    """The trend after each candle closes.

    Up: higher highs and higher lows. Down: lower highs and lower lows (Day 4, 02:13-03:32).
    Once trending, the trend holds until a candle closes beyond the last swing on the other
    side; that close is the structure break that flips it (Day 4, 04:24-05:08; closes only,
    Day 2, 16:50). Consolidation is flagged separately (Day 4, 12:32).
    """
    found = sorted(swings(candles, p), key=lambda s: s.confirmed_at)
    highs: list[float] = []
    lows: list[float] = []
    k = 0
    direction = NONE
    states = []
    for j, c in enumerate(candles):
        while k < len(found) and found[k].confirmed_at <= j:
            (highs if found[k].kind == "high" else lows).append(found[k].price)
            k += 1
        shifted = False
        if c.closed:
            close = c.c
            if direction == NONE and len(highs) >= 2 and len(lows) >= 2:
                if highs[-1] > highs[-2] and lows[-1] > lows[-2]:
                    direction = UP
                elif highs[-1] < highs[-2] and lows[-1] < lows[-2]:
                    direction = DOWN
            elif direction == UP and lows and close < lows[-1]:
                direction, shifted = DOWN, True
            elif direction == DOWN and highs and close > highs[-1]:
                direction, shifted = UP, True
        consolidating = efficiency(candles, j, p.consolidation_lookback) < p.consolidation_max_efficiency
        states.append(TrendState(direction, consolidating, highs[-1] if highs else None,
                                 lows[-1] if lows else None, shifted))
    return states


# Higher timeframes hold higher power (Day 4, 08:13). Ordered from highest to lowest.
TIMEFRAME_RANK = ["1Month", "1Week", "1Day", "4Hour", "1Hour", "30Min", "15Min", "5Min", "1Min"]


@dataclass(frozen=True)
class Bias:
    """Which way the bot may trade, and whether the lower timeframe agrees yet."""

    direction: int  # the higher timeframe's direction, NONE if it has none
    ltf_aligned: bool  # True once the lower timeframe trends the same way (Day 4, 08:44)

    @property
    def ready(self) -> bool:
        return self.direction != NONE and self.ltf_aligned


def bias(htf: TrendState, ltf: TrendState) -> Bias:
    """Trade only with the higher timeframe; use the lower one to time it (Day 4, 08:13-10:53).

    When they disagree, wait for the lower timeframe to turn, never trade the lower one alone.
    """
    direction = htf.tradeable_direction
    return Bias(direction, direction != NONE and ltf.direction == direction)


def state_at(htf_candles: Sequence[Candle], htf_states: Sequence[TrendState],
             htf_length: timedelta, when: str) -> TrendState | None:
    """The higher-timeframe trend as known at ``when``: only higher candles that had closed."""
    t = _ts(when)
    best = None
    for c, s in zip(htf_candles, htf_states):
        if _ts(c.t) + htf_length <= t:
            best = s
        else:
            break
    return best


def _ts(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))
