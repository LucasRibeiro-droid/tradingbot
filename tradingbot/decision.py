"""The bot's one decision process: read every indicator at a candle, decide buy, sell or nothing.

Each lesson teaches an indicator, a way of reading the chart, not a strategy of its own:
  - candles (Day 2): what a single closed candle says
  - trend and higher-timeframe bias (Day 4): which direction is allowed
  - break of structure (Day 6): the trigger that the direction has shifted
  - liquidity (Days 8, 10, 12): whether orders were just taken on the other side, and
    where price is drawn to next
  - fair value gaps, order blocks, equilibrium, daily bias: to come (Days 14-36)
This process combines them. As lessons are added, indicators are added here; the learning
loop tests adding or removing one at a time (H12).

Current rules, each from a lesson:
  1. Trigger: a candle closes past the most recent high or low (break of structure, Day 6).
  2. Allowed only in the higher timeframe's direction (Day 4, locked).
  3. Every indicator named in ``DecisionParams.confluences`` must agree.
  4. Entry at the trigger's close. TJR enters on the pullback into a fair value gap or
     order block (Day 12, 10:54); this improves when those indicators are learned.
  5. Stop beyond the most extreme price of the last ``stop_lookback`` candles.
  6. Target: the nearest untaken liquidity in the trade's direction (Day 12). None, no trade.
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
