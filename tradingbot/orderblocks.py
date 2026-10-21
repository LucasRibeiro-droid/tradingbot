"""Order blocks (Days 20, 22; Day 24 still to come): the move that swept liquidity.

Sources: TJR Boot Camp Day 20: Order Blocks (Pt 1) and Day 22: Order Blocks pt.2
(https://www.youtube.com/watch/RQSVIKddFHI). Topic notes: knowledge/order_blocks.md.

An order block is "that move up that causes the liquidity sweep" before the break of
structure that shifts the market [TJR Day 20, 03:10; Day 22, 02:36-02:46]. That whole price
range is where orders were filled, so when price retraces into it, more orders can be
filled there and price is sent on in the new direction [TJR Day 20, 04:37-06:09].
  - bearish order block: the leg UP that took buy-side liquidity, before a break DOWN
  - bullish order block: the leg DOWN that took sell-side liquidity, before a break UP
It's "the whole move", which can be several candles [TJR Day 22, 07:03-07:15, 09:20-09:26].
There's one per trend: the next forms at the next trend shift [TJR Day 20, 07:53-09:21].

Part 3 (Day 24) will put it together, so nothing here makes decisions.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .candles import BEARISH, BULLISH, Candle
from .config import BASELINE, LiquidityParams, TrendParams
from .fvg import GapEvent, follow
from .liquidity import Taken, pools_and_takes
from .trend import TrendState, swings, trend_series


@dataclass(frozen=True)
class Block:
    """One order block: the price range of the leg that swept liquidity."""

    side: int  # BEARISH (leg up before a break down: shorts) | BULLISH (leg down before a break up)
    start: int  # first candle of the leg
    sweep: int  # the candle at the leg's extreme, where liquidity was taken
    top: float
    bottom: float
    confirmed_at: int  # the break of structure: only then is it known to be an order block

    @property
    def index(self) -> int:
        return self.sweep


def find_blocks(candles: Sequence[Candle], states: Sequence[TrendState] | None = None,
                taken: Sequence[Taken] | None = None, trend: TrendParams = BASELINE.trend,
                liquidity: LiquidityParams = BASELINE.liquidity, require_sweep: bool = True) -> list[Block]:
    """The order block of each trend shift.

    For a break of structure down at candle ``i``:
      - the leg's extreme is the highest high since the previous break [Inferred: the top of
        the old trend is where the leg up ended];
      - the leg starts at the most recent two-candle low before that extreme [Bot: TJR draws
        the box from where the move up began, by eye; Day 20 frame 03:40, Day 22 frame 08:05];
      - the leg must have taken buy-side liquidity, a pool from ``liquidity.py`` [TJR: "the
        move that swept liquidity", Day 22, 02:43]; ``require_sweep=False`` drops that check.
    The zone is the leg's whole range, wick to wick [Bot: TJR boxes the whole move; he hasn't
    said whether wicks or bodies bound it]. A break up mirrors this.
    """
    states = states if states is not None else trend_series(candles, trend)
    taken = taken if taken is not None else pools_and_takes(candles, liquidity)
    lows = sorted((s for s in swings(candles, trend) if s.kind == "low"), key=lambda s: s.index)
    highs = sorted((s for s in swings(candles, trend) if s.kind == "high"), key=lambda s: s.index)
    out = []
    prev = -1
    for i, st in enumerate(states):
        if st.event not in ("bos_up", "bos_down"):
            continue
        window = range(prev + 1, i)
        prev = i
        if not window:
            continue
        if st.event == "bos_down":
            k = max(window, key=lambda j: candles[j].h)
            before = [s for s in lows if s.index < k]
            start = before[-1].index if before else window[0]
            swept = any(t.buy_side for t in taken[start:k + 1])
            block = Block(BEARISH, start, k, top=candles[k].h,
                          bottom=min(c.l for c in candles[start:k + 1]), confirmed_at=i)
        else:
            k = min(window, key=lambda j: candles[j].l)
            before = [s for s in highs if s.index < k]
            start = before[-1].index if before else window[0]
            swept = any(t.sell_side for t in taken[start:k + 1])
            block = Block(BULLISH, start, k, top=max(c.h for c in candles[start:k + 1]),
                          bottom=candles[k].l, confirmed_at=i)
        if swept or not require_sweep:
            out.append(block)
    return out


def follow_block(candles: Sequence[Candle], block: Block) -> GapEvent:
    """What price did after the break: retraced into the block (entered), closed back in the
    block's direction there (reacted), or closed beyond its far side, the sweep's extreme
    (broken). Same tests as fair value gaps [Bot: TJR: "draws right back into here, fills
    more orders and booms", Day 22, 05:12; when a block stops counting isn't taught yet]."""
    return follow(candles, block)  # type: ignore[arg-type]
