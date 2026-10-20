"""Fair value gaps (Days 14, 16; Day 18 still to come): where retracements are drawn to.

Sources: TJR Boot Camp Day 14: Fair Value Gaps Pt. 1 (https://www.youtube.com/watch?v=d0AxLACYaqU)
and Day 16: FVG Pt. 2 (https://www.youtube.com/watch?v=S1kY3Fw6JUQ).
Topic notes: knowledge/fair_value_gaps.md.

A fair value gap (= liquidity void = imbalance) is a range with no opposing orders, left by
a strong candle [TJR Day 14]. Identified as a three-candle pattern [TJR Day 16, 04:12]:
  - bullish: from the TOP of candle 1's wick to the BOTTOM of candle 3's wick, when they
    don't overlap (candle 1's high is below candle 3's low) [TJR Day 16, 05:15-05:30]
  - bearish: from the BOTTOM of candle 1's wick to the TOP of candle 3's wick, when
    candle 1's low is above candle 3's high [TJR Day 16, 06:41-06:57, 11:41-11:51]
If the wicks of candles 1 and 3 overlap, price already traded there: not a gap
[TJR Day 16, 09:41-11:13].

Used for retracements and continuations, in the direction of the trend, never for
reversals [TJR Day 16, 03:22-04:05]. Price reaching a gap is not an entry: wait for a
reaction or a lower-timeframe break of structure [TJR Day 16, 07:58-08:41]. How to trade
them is Day 18, so nothing here makes decisions.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .candles import BEARISH, BULLISH, Candle


@dataclass(frozen=True)
class Gap:
    """One fair value gap: the zone between candle 1's wick and candle 3's wick."""

    index: int  # candle 2, the candle that creates the imbalance
    side: int  # BULLISH or BEARISH
    top: float
    bottom: float
    confirmed_at: int  # candle 3: the gap is only known once it has closed


def find_gaps(candles: Sequence[Candle]) -> list[Gap]:
    """Every fair value gap, by TJR's three-candle rule.

    Candle 2 must close in the gap's direction [Inferred: TJR's drawing and examples show a
    "super full" candle in that direction, Day 16, 04:22; it also keeps overnight price gaps
    on stocks, which no candle created, from counting].
    """
    out = []
    for i in range(len(candles) - 2):
        c1, c2, c3 = candles[i], candles[i + 1], candles[i + 2]
        if not (c1.closed and c2.closed and c3.closed):
            continue
        if c1.h < c3.l and c2.direction == BULLISH:
            out.append(Gap(i + 1, BULLISH, top=c3.l, bottom=c1.h, confirmed_at=i + 2))
        elif c1.l > c3.h and c2.direction == BEARISH:
            out.append(Gap(i + 1, BEARISH, top=c1.l, bottom=c3.h, confirmed_at=i + 2))
    return out


@dataclass(frozen=True)
class GapEvent:
    gap: Gap
    entered_at: int | None  # first later candle to trade into the zone ("price fills")
    reacted_at: int | None  # first candle after entering that closes in the gap's direction
    broken_at: int | None  # first candle to close beyond the far side of the zone


def follow(candles: Sequence[Candle], gap: Gap) -> GapEvent:
    """What price did with a gap after it formed.

    - entered: a candle trades into the zone (bullish: its low reaches the top) [TJR "fill"].
    - reacted: after entering, a candle closes in the gap's direction while having traded in
      the zone [TJR Day 16, 08:09 "a reaction like with a bullish candle"; the exact test is Bot].
    - broken: a candle closes beyond the far side (bullish: below the bottom) [Bot: TJR has
      not said when a gap stops counting].
    """
    entered = reacted = broken = None
    for j in range(gap.confirmed_at + 1, len(candles)):
        c = candles[j]
        if not c.closed:
            break
        in_zone = c.l <= gap.top and c.h >= gap.bottom
        if gap.side == BULLISH:
            if entered is None and c.l <= gap.top:
                entered = j
            if c.c < gap.bottom:
                broken = j
                break
        else:
            if entered is None and c.h >= gap.bottom:
                entered = j
            if c.c > gap.top:
                broken = j
                break
        if entered is not None and reacted is None and in_zone and c.direction == gap.side:
            reacted = j
    return GapEvent(gap, entered, reacted, broken)
