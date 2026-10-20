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
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .candles import Candle
from .config import BASELINE, LOCKED, Config
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
