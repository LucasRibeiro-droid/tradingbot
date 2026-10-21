import unittest

from tradingbot.candles import BEARISH, BULLISH, Candle
from tradingbot.liquidity import Pool, Taken
from tradingbot.orderblocks import find_blocks, follow_block, wick_zone
from tradingbot.trend import DOWN, UP, TrendState


def c(t, o, h, l, cl, closed=True):
    return Candle(f"2026-01-01T00:{t:02d}:00Z", o, h, l, cl, closed)


# A little uptrend, a leg up from the low at candle 3 that takes the high at 102.2 (candle 5)
# and tops at 104.5 (candle 6), then a close below the low: a break of structure down.
LEG_UP_THEN_BREAK = [
    c(0, 100, 101, 99, 100.5), c(1, 100.5, 102, 100, 101.8), c(2, 101.8, 102.2, 100.5, 100.8),
    c(3, 100.8, 101, 99.5, 100), c(4, 100, 101.5, 99.8, 101.2), c(5, 101.2, 104, 101, 103.8),
    c(6, 103.8, 104.5, 103, 103.2), c(7, 103.2, 103.3, 99, 99.2),
]
BUY_SIDE_TAKEN = Taken(buy_side=(Pool(2, 102.2, "buy_side", 3),))


def states(n, at, event, direction):
    return [TrendState(direction if j >= at else 0, False, None, None, event if j == at else None) for j in range(n)]


def mirror(candles):
    return [Candle(x.t, -x.o, -x.l, -x.h, -x.c, x.closed) for x in candles]


class Identify(unittest.TestCase):
    def test_leg_up_that_swept_liquidity_before_a_break_down(self):
        # Day 20, 03:10: "that move up that causes the liquidity sweep" before the break.
        taken = [Taken()] * 8
        taken[5] = BUY_SIDE_TAKEN
        blocks = find_blocks(LEG_UP_THEN_BREAK, states(8, 7, "bos_down", DOWN), taken)
        self.assertEqual([(b.side, b.start, b.sweep, b.bottom, b.top, b.confirmed_at) for b in blocks],
                         [(BEARISH, 3, 6, 99.5, 104.5, 7)])

    def test_no_liquidity_taken_no_order_block(self):
        # Day 22, 02:43: it's the move that swept liquidity.
        st = states(8, 7, "bos_down", DOWN)
        self.assertEqual(find_blocks(LEG_UP_THEN_BREAK, st, [Taken()] * 8), [])
        self.assertEqual(len(find_blocks(LEG_UP_THEN_BREAK, st, [Taken()] * 8, require_sweep=False)), 1)

    def test_bullish_mirror(self):
        taken = [Taken()] * 8
        taken[5] = Taken(sell_side=(Pool(2, -102.2, "sell_side", 3),))
        blocks = find_blocks(mirror(LEG_UP_THEN_BREAK), states(8, 7, "bos_up", UP), taken)
        self.assertEqual([(b.side, b.start, b.sweep, b.bottom, b.top) for b in blocks],
                         [(BULLISH, 3, 6, -104.5, -99.5)])

    def test_one_block_per_trend_shift(self):
        # Day 20, 07:53: only one order block within a whole trend.
        taken = [Taken()] * 8
        taken[5] = BUY_SIDE_TAKEN
        st = states(8, 7, "bos_down", DOWN)
        self.assertEqual(len(find_blocks(LEG_UP_THEN_BREAK, st, taken)), 1)


class WickZone(unittest.TestCase):
    def test_bearish_block_wick_to_body_at_the_legs_low(self):
        # Day 24, 11:46: "from the wick down to the start of the body", at the end of the leg
        # a retracement reaches first (for a leg up: its low, candle 3, low 99.5, body 100-100.8).
        taken = [Taken()] * 8
        taken[5] = BUY_SIDE_TAKEN
        b = wick_zone(LEG_UP_THEN_BREAK, find_blocks(LEG_UP_THEN_BREAK, states(8, 7, "bos_down", DOWN), taken)[0])
        self.assertEqual((b.bottom, b.top), (99.5, 100))

    def test_bullish_block_mirrors(self):
        taken = [Taken()] * 8
        taken[5] = Taken(sell_side=(Pool(2, -102.2, "sell_side", 3),))
        m = mirror(LEG_UP_THEN_BREAK)
        b = wick_zone(m, find_blocks(m, states(8, 7, "bos_up", UP), taken)[0])
        self.assertEqual((b.bottom, b.top), (-100, -99.5))


class Follow(unittest.TestCase):
    def setUp(self):
        taken = [Taken()] * 8
        taken[5] = BUY_SIDE_TAKEN
        self.block = find_blocks(LEG_UP_THEN_BREAK, states(8, 7, "bos_down", DOWN), taken)[0]

    def test_retrace_into_block_then_react(self):
        # Day 22, 05:12: "draws right back into here, fills more orders and booms".
        candles = LEG_UP_THEN_BREAK + [c(8, 99.2, 100, 98, 99.8), c(9, 99.8, 101, 99.5, 99.6)]
        ev = follow_block(candles, self.block)
        self.assertEqual((ev.entered_at, ev.reacted_at, ev.broken_at), (8, 9, None))

    def test_close_above_the_sweep_breaks_it(self):
        candles = LEG_UP_THEN_BREAK + [c(8, 99.2, 104, 99, 103.9), c(9, 103.9, 105.5, 103.5, 105)]
        ev = follow_block(candles, self.block)
        self.assertEqual((ev.entered_at, ev.broken_at), (8, 9))


if __name__ == "__main__":
    unittest.main()
