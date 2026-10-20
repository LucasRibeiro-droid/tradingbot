"""Days 4 and 6 — Trends and break of structure.

Sources: TJR Boot Camp Day 4: Trends (https://www.youtube.com/watch?v=viuGHEuv0nw) and
Day 6: Break of Structure (https://www.youtube.com/watch?v=PmhuPbY8ZHo).
Full write-ups: knowledge/day04_trends.md, knowledge/day06_break_of_structure.md.

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
    """A high or a low. Day 6, 01:56: a high is a move up then a move down; a low is a
    move down then a move up. Two candles are enough."""

    index: int
    price: float
    kind: str  # "high" | "low"
    confirmed_at: int  # first bar index at which the swing is known


@dataclass(frozen=True)
class TrendState:
    """The trend as it was known at the close of one candle."""

    direction: int  # UP, DOWN, or NONE before the first break of structure
    consolidating: bool
    swing_high: float | None  # most recent high (Day 6, 08:54: only the most recent counts)
    swing_low: float | None  # most recent low
    # "bos_up" / "bos_down": this candle closed beyond the watched level (Day 6, 07:37).
    # "sweep_high" / "sweep_low": its wick went beyond but it did not close there: not a
    # break of structure, often a liquidity sweep (Day 6, 12:10 and 23:50).
    event: str | None = None
    # This candle traded past the most recent high (low), by wick or close: it took the
    # resting orders sitting there (Day 8, 02:20).
    took_high: bool = False
    took_low: bool = False

    @property
    def shifted(self) -> bool:
        """This candle's close broke structure and changed the direction."""
        return self.event in ("bos_up", "bos_down")

    @property
    def tradeable_direction(self) -> int:
        """The direction to trade, or NONE when there is no clear trend (Day 4, 12:32)."""
        return NONE if self.consolidating else self.direction


def _hl(c: Candle, source: str) -> tuple[float, float]:
    # "Use the line chart to your advantage" (Day 4, 18:32): swings from closes only.
    return (c.c, c.c) if source == "close" else (c.h, c.l)


def swings(candles: Sequence[Candle], p: TrendParams = TrendParams()) -> list[Swing]:
    """All highs and lows, using ``p.swing_method``.

    "two_candle" (Day 6, the default): an up candle then a down candle is a high, at the
    higher wick of the two; a down candle then an up candle is a low, at the lower wick of
    the two (Day 6, 02:20-05:02). Known once the second candle closes.
    "pivot" (the bot's first Day 4 attempt): higher (lower) than ``swing_strength``
    candles on each side.
    """
    if p.swing_method == "two_candle":
        return _two_candle_swings(candles, p.swing_source)
    return _pivot_swings(candles, p)


def _two_candle_swings(candles: Sequence[Candle], source: str) -> list[Swing]:
    out = []
    for i in range(len(candles) - 1):
        a, b = candles[i], candles[i + 1]
        if not (a.closed and b.closed):
            continue
        (ah, al), (bh, bl) = _hl(a, source), _hl(b, source)
        if a.direction > 0 and b.direction < 0:
            out.append(Swing(i if ah >= bh else i + 1, max(ah, bh), "high", i + 1))
        elif a.direction < 0 and b.direction > 0:
            out.append(Swing(i if al <= bl else i + 1, min(al, bl), "low", i + 1))
    return out


def _pivot_swings(candles: Sequence[Candle], p: TrendParams) -> list[Swing]:
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
    """The trend after each candle closes, driven by breaks of structure (Day 6, 13:59-18:00).

    1. Identify the trend. 2. In an uptrend, watch the most recent low. 3. In a downtrend,
    watch the most recent high. 4. A candle **close** below the most recent low breaks
    structure down. 5. A close above the most recent high breaks structure up. Before the
    first break, either side counts. Wicks beyond the level are sweeps, not breaks.
    Consolidation is flagged separately (Day 4, 12:32).
    """
    found = sorted(swings(candles, p), key=lambda s: s.confirmed_at)
    high = low = None
    k = 0
    direction = NONE
    states = []
    for j, c in enumerate(candles):
        event = None
        took_high = c.closed and high is not None and c.h > high
        took_low = c.closed and low is not None and c.l < low
        if c.closed:
            watch_high = direction in (NONE, DOWN) and high is not None
            watch_low = direction in (NONE, UP) and low is not None
            if watch_high and c.c > high:
                direction, event = UP, "bos_up"
            elif watch_low and c.c < low:
                direction, event = DOWN, "bos_down"
            elif watch_low and c.l < low:
                event = "sweep_low"
            elif watch_high and c.h > high:
                event = "sweep_high"
        # Swings completed by this candle become the levels to watch from the next one on.
        while k < len(found) and found[k].confirmed_at <= j:
            if found[k].kind == "high":
                high = found[k].price
            else:
                low = found[k].price
            k += 1
        consolidating = efficiency(candles, j, p.consolidation_lookback) < p.consolidation_max_efficiency
        states.append(TrendState(direction, consolidating, high, low, event, took_high, took_low))
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
