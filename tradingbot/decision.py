"""Test harness: reads the indicators learned so far and decides buy, sell or nothing.

This is NOT TJR's strategy. It assembles the pieces taught so far to test what each one
contributes. The full methodology is reconstructed in knowledge/methodology.md; parts it
depends on (fair value gaps, order blocks, execution, stops) are not taught yet.

Steps, with provenance ([TJR] taught, [Inferred], [Bot] placeholder):
  1. Trigger: a break of structure, a candle close past the most recent high/low [TJR Day 6].
  2. Only in the higher timeframe's direction [TJR Day 4, locked].
  3. Required confluences from ``DecisionParams.confluences``; today "liquidity_swept":
     liquidity on the other side taken shortly before [TJR Days 8, 12; "shortly" = 10
     candles is Bot].
  4. Entry at the trigger candle's close [Bot]. TJR enters on the retracement into a fair
     value gap or order block, triggered by a LOWER-timeframe break (Day 14, 04:28); this
     harness uses one timeframe for the trigger until Days 16-18 and 30-33 are learned.
  5. Stop beyond the last ``stop_lookback`` candles' extreme [Bot]; stops are taught on Day 38.
  6. Target: the nearest untaken liquidity in the trade's direction [TJR Day 12].

A second path, ``Continuation`` (Days 14-24), trades the retracement into a higher-timeframe
fair value gap or order block with a lower-timeframe break of structure; see its docstring.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .candles import Candle
from .config import BASELINE, LOCKED, Config
from .fvg import Gap
from .liquidity import Pool, Taken, draw, swept_before
from .trend import NONE, UP, TrendState


@dataclass(frozen=True)
class Decision:
    """Buy (direction 1) or sell (-1) at ``entry``, with the reasons each indicator gave."""

    index: int
    direction: int
    entry: float
    stop: float
    target: float
    reasons: tuple[str, ...]

    @property
    def reward_to_risk(self) -> float:
        return abs(self.target - self.entry) / abs(self.entry - self.stop)


def decide(candles: Sequence[Candle], states: Sequence[TrendState],
           scanned: Sequence[tuple[Taken, tuple[Pool, ...]]], i: int,
           htf: TrendState | None, config: Config = BASELINE) -> Decision | None:
    """Decide at the close of candle ``i``. None means do nothing."""
    s = states[i]
    if s.event not in ("bos_up", "bos_down"):
        return None
    d = 1 if s.event == "bos_up" else -1
    reasons = [f"break of structure {'up' if d == UP else 'down'}"]

    htf_dir = htf.tradeable_direction if htf else NONE
    if not LOCKED.trade_against_htf_trend and htf_dir != d:
        return None
    reasons.append("higher timeframe agrees")

    taken = [t for t, _ in scanned]
    for name in config.decision.confluences:
        if name == "liquidity_swept":
            if not swept_before(taken, i, d, config.liquidity):
                return None
            reasons.append("liquidity taken on the other side just before")
        else:
            raise ValueError(f"unknown confluence {name!r}")

    entry = candles[i].c
    window = candles[max(0, i - config.decision.stop_lookback + 1):i + 1]
    stop = min(c.l for c in window) if d == UP else max(c.h for c in window)
    target = draw(scanned[i][1], d, entry)
    if target is None or stop == entry:
        return None
    reasons.append("target: nearest untaken liquidity")
    return Decision(i, d, entry, stop, target, tuple(reasons))


def simulate(candles: Sequence[Candle], dec: Decision, max_bars: int) -> dict | None:
    """Follow the decision exactly: +reward/risk if the target is hit first, -1 if the stop is.

    A candle that touches both counts as the stop (we can't know which came first). After
    ``max_bars`` candles the position is closed at that close. None if the data runs out.
    """
    risk = abs(dec.entry - dec.stop)
    after = candles[dec.index + 1:dec.index + 1 + max_bars]
    for n, c in enumerate(after, 1):
        if not c.closed:
            return None
        hit_stop = c.l <= dec.stop if dec.direction == UP else c.h >= dec.stop
        hit_target = c.h >= dec.target if dec.direction == UP else c.l <= dec.target
        if hit_stop:
            return {"r": -1.0, "exit": "stop", "bars": n}
        if hit_target:
            return {"r": round(dec.reward_to_risk, 3), "exit": "target", "bars": n}
    if len(after) < max_bars:
        return None
    return {"r": round((after[-1].c - dec.entry) * dec.direction / risk, 3), "exit": "time", "bars": max_bars}


# ---------------------------------------------------------------------------------------
# Continuation through fair value gaps (Days 14, 16, 18) or order blocks (Days 20, 22, 24)
# ---------------------------------------------------------------------------------------

def after_market_open(t: str) -> bool:
    """TJR: "we're not going to take any trades that aren't off of market open or after
    market open" (Day 18, 03:13). For the bot's US instruments: 9:30 New York time or later.
    Which open matters for which market is taught later (Day 18, 02:32)."""
    from datetime import datetime, time
    from zoneinfo import ZoneInfo
    ny = datetime.fromisoformat(t.replace("Z", "+00:00")).astimezone(ZoneInfo("America/New_York"))
    return ny.time() >= time(9, 30)


@dataclass
class _Zone:
    gap: Gap
    entered: bool = False
    extreme: float | None = None  # furthest price of the retracement since entering
    done: bool = False


class Continuation:
    """Higher-timeframe fair value gap or order block, retracement into it, lower-timeframe
    break of structure in the trend's direction (Days 14, 16, 18; order blocks Days 20-24).

    ``zone``: "fvg" (fair value gaps), "order_block" (the whole leg) or "order_block_wick"
    (TJR's own box, wick to the start of the body, Day 24, 11:46). Order blocks are TJR's first-choice
    retracement area and are used "off the first retracement" (Day 20, 06:57; Day 24, 16:49);
    the entry is the same: price taps in, then a lower-timeframe break (Day 24, 11:53-12:10).
    Everything else is shared, so the two zone types can be compared one variable at a time.

    [TJR] Only gaps in the higher timeframe's direction (Day 16, 03:22). Never enter when
    price merely reaches the gap; wait for a lower-timeframe break in the trend's direction
    (Day 16, 07:58; Day 18, 04:52-05:46). A gap price pushes past is no longer of interest
    (Day 18, 09:43). Stop beyond the retracement's extreme ("stop above these highs", Day 18,
    07:12). Target previous liquidity (Day 18, 07:18). Only after the market opens (Day 18, 03:13).
    [Bot] "Pushes past" = a lower-timeframe close beyond the far side; "entered" = a wick
    touching the zone; one decision per gap; entry at the break candle's close.
    """

    def __init__(self, htf_candles: Sequence[Candle], htf_length, config: Config = BASELINE,
                 zone: str = "fvg", in_discount: bool = False):
        from .fvg import find_gaps
        from .orderblocks import find_blocks, wick_zone
        from .trend import _ts
        self.config = config
        self.zone = zone
        # Equilibrium (Days 26, 28): optionally require the retracement to reach the higher
        # timeframe's discount (premium for shorts): "a fair value gap within a discounted
        # price and then you get a reaction ... enter" (Day 26, 09:49-10:10).
        self.in_discount = in_discount
        from .equilibrium import ranges
        from .trend import trend_series
        self._eq = [(_ts(c.t) + htf_length, r) for c, r in
                    zip(htf_candles, ranges(htf_candles, trend_series(htf_candles, config.trend)))]
        self._eq_k = 0
        self._range = None
        if zone == "fvg":
            found = find_gaps(htf_candles)
        else:
            found = find_blocks(htf_candles, trend=config.trend, liquidity=config.liquidity)
            if zone == "order_block_wick":  # TJR's own box: wick to the start of the body (Day 24)
                found = [wick_zone(htf_candles, b) for b in found]
        self._pending = sorted(((_ts(htf_candles[g.confirmed_at].t) + htf_length, g)
                                for g in found), key=lambda x: x[0])
        self._k = 0
        self.zones: list[_Zone] = []

    def step(self, candles: Sequence[Candle], states: Sequence[TrendState],
             scanned: Sequence[tuple[Taken, tuple[Pool, ...]]], i: int,
             htf: TrendState | None) -> Decision | None:
        from .trend import _ts
        c = candles[i]
        if not c.closed:
            return None
        now = _ts(c.t)
        while self._k < len(self._pending) and self._pending[self._k][0] <= now:
            self.zones.append(_Zone(self._pending[self._k][1]))
            self._k += 1
        while self._eq_k < len(self._eq) and self._eq[self._eq_k][0] <= now:
            self._range = self._eq[self._eq_k][1]
            self._eq_k += 1
        d = htf.tradeable_direction if htf else NONE
        s = states[i]
        decision = None
        for z in self.zones:
            if z.done:
                continue
            g = z.gap
            if (g.side == UP and c.c < g.bottom) or (g.side != UP and c.c > g.top):
                z.done = True  # price pushed past it
                continue
            if g.side == UP and c.l <= g.top:
                z.entered, z.extreme = True, c.l if z.extreme is None else min(z.extreme, c.l)
            elif g.side != UP and c.h >= g.bottom:
                z.entered, z.extreme = True, c.h if z.extreme is None else max(z.extreme, c.h)
            trigger = "bos_up" if g.side == UP else "bos_down"
            if (decision is None and z.entered and g.side == d and s.event == trigger
                    and after_market_open(c.t)
                    and (not self.in_discount or (self._range is not None and self._range.direction == g.side
                                                  and self._range.depth(z.extreme) >= 0.5))):
                z.done = True
                stop, entry = z.extreme, c.c
                target = draw(scanned[i][1], g.side, entry)
                if target is not None and stop != entry and (stop < entry) == (g.side == UP):
                    decision = Decision(i, g.side, entry, stop, target, (
                        "higher timeframe trend agrees",
                        f"retraced into a higher-timeframe {'bullish' if g.side == UP else 'bearish'} "
                        + ("fair value gap" if self.zone == "fvg" else "order block"),
                        f"lower-timeframe break of structure {'up' if g.side == UP else 'down'}",
                        "stop beyond the retracement's extreme",
                        "target: nearest untaken liquidity"))
        self.zones = [z for z in self.zones if not z.done]
        return decision
