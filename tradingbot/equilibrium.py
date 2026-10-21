"""Equilibrium (Days 26, 28): the 50% of the swing, splitting it into premium and discount.

Sources: TJR Boot Camp Day 26: Equilibrium (https://www.youtube.com/watch/j1pVK897oZQ) and
Day 28: Equilibrium pt.2 (https://www.youtube.com/watch/-E7plUbSJUk).
Topic notes: knowledge/equilibrium.md.

Measure the swing and find the 50 mark [TJR Day 26, 06:32; Day 28, 01:27]. In an uptrend,
below it is the discount, where smart money buys; above it is the premium [Day 28, 01:39-02:24].
"Whenever you see price make a new high in an uptrend, drag it from the low up to the high";
in a downtrend from the high down to the low [Day 28, 18:23-18:42].
  - The low stays; the high is dragged up while price makes new highs without reaching 50%
    ("doesn't get hit ... we go higher, we drag it higher", Day 28, 08:20-08:26).
  - Once price has dipped to 50% and then makes a new high, measure again from that dip's low
    ("we form a low right here ... got to go higher", Day 28, 09:01-09:16).
  - At a break of structure, start from the extreme the break came from (the low before a
    break up) [Inferred from the 08:30 frame].
  - Wick to wick [Inferred from the frames at 06:52 and 08:22: the box sits on the wicks].
Equilibrium is a gauge, not an entry: a block, gap or break of structure inside the discount
is the reason to get in [TJR Day 26, 08:21-08:48; Day 28, 03:07-03:43].
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .candles import Candle
from .trend import DOWN, UP, TrendState


@dataclass(frozen=True)
class Range:
    """The swing being measured after one candle closes."""

    direction: int  # UP: low -> high, discount below the middle; DOWN: high -> low
    low: float
    high: float

    @property
    def mid(self) -> float:
        return (self.low + self.high) / 2

    def depth(self, price: float) -> float:
        """How far a retracement to ``price`` reaches: 0 at the extreme it retraces from,
        0.5 at equilibrium, 1 at the swing's origin. Above 0.5 is the discount for an uptrend
        (premium for a downtrend): the side smart money trades from."""
        span = self.high - self.low
        if span <= 0:
            return 0.0
        return (self.high - price) / span if self.direction == UP else (price - self.low) / span


def ranges(candles: Sequence[Candle], states: Sequence[TrendState]) -> list[Range | None]:
    """The swing being measured at each candle close, by the rules in the module docstring."""
    out: list[Range | None] = []
    direction = 0
    origin = extreme = 0.0
    ext_i = last_bos = 0
    hit = False
    for i, (c, s) in enumerate(zip(candles, states)):
        if not c.closed:
            out.append(out[-1] if out else None)
            continue
        moved = True  # the break or a new extreme: not a retracement candle
        if s.event in ("bos_up", "bos_down"):
            direction = UP if s.event == "bos_up" else DOWN
            window = candles[last_bos:i + 1]
            if direction == UP:
                origin = min(x.l for x in window)
                extreme, ext_i = max((x.h, j) for j, x in enumerate(window, last_bos))
            else:
                origin = max(x.h for x in window)
                extreme, ext_i = min((x.l, j) for j, x in enumerate(window, last_bos))
            last_bos, hit = i, False
        elif direction == UP and c.h > extreme:
            if hit:  # the dip reached equilibrium; measure again from its low
                origin, hit = min(x.l for x in candles[ext_i + 1:i + 1]), False
            extreme, ext_i = c.h, i
        elif direction == DOWN and c.l < extreme:
            if hit:
                origin, hit = max(x.h for x in candles[ext_i + 1:i + 1]), False
            extreme, ext_i = c.l, i
        else:
            moved = False
        if direction == 0:
            out.append(None)
            continue
        r = Range(direction, origin, extreme) if direction == UP else Range(direction, extreme, origin)
        if not moved and r.depth(c.l if direction == UP else c.h) >= 0.5:
            hit = True
        out.append(r)
    return out
