"""Day 8 — Liquidity: why price moves, and the sequence TJR trades.

Source: TJR Boot Camp Day 8: Liquidity Pt 1 (https://www.youtube.com/watch?v=Lxnu7InGhGE).
Full write-up: knowledge/day08_liquidity_pt1.md.

Liquidity is resting orders: stops and limit orders waiting at a price (02:20). Banks
need it to fill their large orders, so price is pushed into it; once their orders are
filled, price turns. The trader's confirmation that this happened is a break of
structure the other way (07:04-09:36). Where liquidity sits (Day 10) and how to
execute (Day 12) come later; for now the bot only recognizes the sequence.
"""
from __future__ import annotations

from typing import Sequence

from .config import LiquidityParams
from .trend import DOWN, NONE, UP, TrendState


def sweep_then_shift(states: Sequence[TrendState], i: int,
                     p: LiquidityParams = LiquidityParams()) -> int:
    """UP if candle ``i`` breaks structure up after liquidity below was taken, DOWN for the
    mirror case, NONE otherwise. Price reaching liquidity alone is never enough (08:38)."""
    s = states[i]
    window = states[max(0, i - p.sweep_lookback + 1):i + 1]
    if s.event == "bos_up" and any(w.took_low for w in window):
        return UP
    if s.event == "bos_down" and any(w.took_high for w in window):
        return DOWN
    return NONE
