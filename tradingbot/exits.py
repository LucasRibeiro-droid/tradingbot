"""Exits (Days 37, 38): where TJR takes profit and where his stop goes.

Sources: TJR Boot Camp Day 37: Taking Profits (https://www.youtube.com/watch/FjSiLFrg5fo) and
Day 38: Stop Losses (https://www.youtube.com/watch/1FunNCUw_jM).
Lesson notes: knowledge/day37_taking_profits.md, knowledge/day38_stop_losses.md.

Take profits [TJR Day 37]:
  - at building blocks, "price magnets": liquidity, fair value gaps, order blocks (02:01-03:30,
    08:05-08:33), on the execution timeframe or one higher (02:20-02:26, 05:10-05:23)
  - the first is "the one higher time frame draw on liquidity" in the trade's direction
    (03:39-04:06), and "most of the time my first take profit is going to be minimum one to
    one" (06:37-06:41)
  - "I usually set like three or four take profits"; how many is the trader's choice (04:15-04:42)
  - partials: "I take partials" (Day 36, 20:51); the rest stopped at break even (Day 18 example)
Stops [TJR Day 38]: beyond the liquidity sweep, the point where the idea is invalid (01:16-03:37),
plus room for the spread (06:05-07:25). See orderblocks / models_study for the sweep.

[Bot] choices: the levels are untaken liquidity pools (this timeframe and one higher) and the
near edge of unfilled fair value gaps; three take profits, equal thirds; stop to break even
after the first; a candle touching a target and the stop counts as the stop.
"""
from __future__ import annotations

from typing import Sequence

from .candles import Candle


def take_profits(direction: int, entry: float, stop: float, htf_draws: Sequence[float],
                 other_levels: Sequence[float], n: int = 3, min_r: float = 1.0) -> list[float]:
    """TJR's ladder: the first higher-timeframe draw on liquidity at least ``min_r`` away, then
    the next building blocks beyond it, ``n`` targets in all (fewer if there aren't enough)."""
    risk = abs(entry - stop)
    beyond = lambda p: (p - entry) * direction > 0
    far_enough = lambda p: (p - entry) * direction >= min_r * risk
    first = sorted((p for p in htf_draws if beyond(p) and far_enough(p)), key=lambda p: (p - entry) * direction)
    if not first:
        return []
    tp1 = first[0]
    rest = sorted({p for p in list(htf_draws) + list(other_levels) if (p - tp1) * direction > 0},
                  key=lambda p: (p - entry) * direction)
    return [tp1] + rest[:n - 1]


def simulate_partials(candles: Sequence[Candle], index: int, direction: int, entry: float, stop: float,
                      targets: Sequence[float], max_bars: int, check_entry_candle: bool = False) -> dict | None:
    """Follow a trade with several take profits from the candle after ``index``: equal parts
    close at each target; after the first, the stop moves to break even. Result in R.

    ``check_entry_candle``: the entry was a touch inside candle ``index`` (a limit order), so
    that candle can already hit the stop. None if the data runs out.
    """
    risk = abs(entry - stop)
    part = 1 / len(targets)
    if check_entry_candle:
        c = candles[index]
        if (c.l <= stop) if direction == 1 else (c.h >= stop):
            return {"r": -1.0, "exit": "stop", "bars": 0, "hit": 0}
    r, hit, current_stop = 0.0, 0, stop
    after = candles[index + 1:index + 1 + max_bars]
    for n, c in enumerate(after, 1):
        if not c.closed:
            return None
        if (c.l <= current_stop) if direction == 1 else (c.h >= current_stop):
            r += (1 - part * hit) * (current_stop - entry) * direction / risk
            return {"r": round(r, 3), "exit": "stop" if hit == 0 else "break_even", "bars": n, "hit": hit}
        while hit < len(targets) and ((c.h >= targets[hit]) if direction == 1 else (c.l <= targets[hit])):
            r += part * (targets[hit] - entry) * direction / risk
            hit += 1
            current_stop = entry
        if hit == len(targets):
            return {"r": round(r, 3), "exit": "target", "bars": n, "hit": hit}
    if len(after) < max_bars:
        return None
    r += (1 - part * hit) * (after[-1].c - entry) * direction / risk
    return {"r": round(r, 3), "exit": "time", "bars": max_bars, "hit": hit}
