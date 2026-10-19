"""Day 2 — Candlesticks: reading what a single closed candle says about price.

Source: TJR Boot Camp Day 2 (https://www.youtube.com/watch?v=bEkbNGUzQME).
Timestamps in comments point to the lesson. The full write-up is in
knowledge/day02_candlesticks.md.

A read is context for the rest of the strategy. It is never an entry on its own
(``config.LOCKED.candle_read_is_entry_signal``).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from .config import LOCKED, CandleParams

BULLISH = 1
NEUTRAL = 0
BEARISH = -1


class FormingCandleError(ValueError):
    """Raised when asked to read a candle that has not closed yet."""


@dataclass(frozen=True)
class Candle:
    """One candle: the open, high, low and close of a fixed span of time (Day 2, 03:05)."""

    t: str
    o: float
    h: float
    l: float
    c: float
    closed: bool = True

    def __post_init__(self):
        if self.h < max(self.o, self.c) or self.l > min(self.o, self.c):
            raise ValueError(f"inconsistent candle at {self.t}: o={self.o} h={self.h} l={self.l} c={self.c}")

    @property
    def range(self) -> float:
        return self.h - self.l

    @property
    def body(self) -> float:
        return abs(self.c - self.o)

    # Wicks show where price went during the candle but did not close (Day 2, 05:13).
    @property
    def upper_wick(self) -> float:
        return self.h - max(self.o, self.c)

    @property
    def lower_wick(self) -> float:
        return min(self.o, self.c) - self.l

    @property
    def direction(self) -> int:
        # Bullish: close above open. Bearish: close below open (Day 2, 04:25 and 06:42).
        return BULLISH if self.c > self.o else BEARISH if self.c < self.o else NEUTRAL

    def pct(self, part: float) -> float:
        return part / self.range if self.range > 0 else 0.0

    @property
    def close_location(self) -> float:
        """Where the close sits in the range: 0 = at the low, 1 = at the high."""
        return (self.c - self.l) / self.range if self.range > 0 else 0.5


@dataclass(frozen=True)
class CandleRead:
    """What one candle says. ``lean`` is a direction hint, not a trade signal."""

    shape: str
    kind: str  # strong_close | rejection | weakness | indecision | none
    lean: int
    strength: float
    notes: tuple[str, ...] = field(default_factory=tuple)
    readable: bool = True


def average_range(candles: Sequence[Candle], end: int, lookback: int) -> float:
    window = candles[max(0, end - lookback):end]
    return sum(c.range for c in window) / len(window) if window else 0.0


def prior_move(candles: Sequence[Candle], end: int, lookback: int) -> int:
    """Direction of the move into ``candles[end]``, from closes over ``lookback`` bars."""
    if end - lookback < 0:
        return NEUTRAL
    change = candles[end - 1].c - candles[end - lookback].c
    return BULLISH if change > 0 else BEARISH if change < 0 else NEUTRAL


def shape(candle: Candle, prior: int, p: CandleParams) -> str:
    """Name the candle using only the single-candle row TJR keeps (Day 2, 08:14-09:09)."""
    body = candle.pct(candle.body)
    up = candle.pct(candle.upper_wick)
    lo = candle.pct(candle.lower_wick)
    if candle.range == 0:
        return "flat"
    if body <= p.doji_max_body_pct:
        if up <= p.short_wick_max_pct and lo >= p.long_wick_min_pct:
            return "dragonfly_doji"
        if lo <= p.short_wick_max_pct and up >= p.long_wick_min_pct:
            return "gravestone_doji"
        if up >= p.long_legged_min_wick_pct and lo >= p.long_legged_min_wick_pct:
            return "long_legged_doji"
        if lo > up and candle.close_location >= 2 / 3:
            return "cross_doji"
        if up > lo and candle.close_location <= 1 / 3:
            return "inverted_cross_doji"
        return "doji"
    if body <= p.hammer_max_body_pct:
        if candle.lower_wick >= p.hammer_wick_to_body * candle.body and up <= p.short_wick_max_pct:
            return "hanging_man" if prior == BULLISH else "hammer"
        if candle.upper_wick >= p.hammer_wick_to_body * candle.body and lo <= p.short_wick_max_pct:
            # Same shape as an inverted hammer; after a rise it is usually called a shooting star.
            return "shooting_star" if prior == BULLISH else "inverted_hammer"
    if body >= p.strong_close_min_body_pct:
        close_wick = up if candle.direction == BULLISH else lo
        if close_wick <= p.strong_close_max_close_wick_pct:
            return "strong_close"
    return "regular"


def read(candles: Sequence[Candle], i: int, p: CandleParams = CandleParams()) -> CandleRead:
    """Read ``candles[i]`` the way TJR reads a closed candle, using earlier candles for context."""
    candle = candles[i]
    if LOCKED.closed_candles_only and not candle.closed:
        # Day 2, 16:50: "We can only make bias and decision on candles that have formed."
        raise FormingCandleError(f"candle at {candle.t} has not closed")

    avg = average_range(candles, i, p.avg_range_lookback)
    prior = prior_move(candles, i, p.context_lookback)
    name = shape(candle, prior, p)
    if name == "flat" or (avg > 0 and candle.range < p.min_range_vs_avg * avg):
        return CandleRead(name, "none", NEUTRAL, 0.0, ("too small to read",), readable=False)

    up = candle.pct(candle.upper_wick)
    lo = candle.pct(candle.lower_wick)
    notes: list[str] = []
    lean, strength, kind = NEUTRAL, 0.0, "none"

    # Strong close: a full body says where price wants to go (Day 2, 15:00).
    if name == "strong_close":
        lean, strength, kind = candle.direction, candle.pct(candle.body), "strong_close"
        notes.append("full-body close: momentum continues")

    # Rejection: a long wick that price pulled back from, closing at the other end (16:00-18:00).
    # Strongest when it also closes in that direction with almost no opposite wick (17:30).
    elif lo >= p.rejection_min_wick_pct and candle.close_location >= 2 / 3:
        lean, strength, kind = BULLISH, lo, "rejection"
        notes.append("long lower wick rejected: buyers pushed price back up")
        if candle.direction == BULLISH and up <= p.short_wick_max_pct:
            strength = min(1.0, strength + 0.25)
            notes.append("closed near the high: very strong bullish rejection")
    elif up >= p.rejection_min_wick_pct and candle.close_location <= 1 / 3:
        lean, strength, kind = BEARISH, up, "rejection"
        notes.append("long upper wick rejected: sellers pushed price back down")
        if candle.direction == BEARISH and lo <= p.short_wick_max_pct:
            strength = min(1.0, strength + 0.25)
            notes.append("closed near the low: very strong bearish rejection")

    # Weakness: still a bullish (bearish) close, but a fat wick on the closing side shows it
    # was not strong enough to close higher (lower). Often liquidity was taken there (10:00).
    # Dojis are excluded: with almost no body, every wick would count as "fat".
    elif name.endswith("doji"):
        pass
    elif candle.direction == BULLISH and candle.upper_wick >= p.weakness_wick_to_body * candle.body:
        lean, strength, kind = BEARISH, min(1.0, up), "weakness"
        notes.append("bullish close but failed to hold the high: bullish weakness")
    elif candle.direction == BEARISH and candle.lower_wick >= p.weakness_wick_to_body * candle.body:
        lean, strength, kind = BULLISH, min(1.0, lo), "weakness"
        notes.append("bearish close but failed to hold the low: bearish weakness")

    # Doji: indecision; after a move it shows that move losing momentum (11:00-12:38).
    if name.endswith("doji") and lean == NEUTRAL:
        kind = "indecision"
        notes.append("indecision")
        if prior != NEUTRAL:
            lean, strength = -prior, 0.25
            notes.append("momentum of the prior move is fading")

    return CandleRead(name, kind, lean, round(strength, 3), tuple(notes))
