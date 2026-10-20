import unittest

from tradingbot.candles import BEARISH, BULLISH, Candle
from tradingbot.fvg import find_gaps, follow


def c(t, o, h, l, cl, closed=True):
    return Candle(f"2026-01-01T00:{t:02d}:00Z", o, h, l, cl, closed)


class Identify(unittest.TestCase):
    def test_bullish_gap_is_candle1_high_to_candle3_low(self):
        # Day 16, 05:15: top of the first candle's wick to the bottom of the third's.
        gaps = find_gaps([c(0, 100, 101, 99, 100.5), c(1, 100.5, 106, 100.3, 105.5), c(2, 105.5, 107, 103, 106)])
        self.assertEqual([(g.side, g.bottom, g.top, g.index) for g in gaps], [(BULLISH, 101, 103, 1)])

    def test_bearish_gap_is_candle1_low_to_candle3_high(self):
        gaps = find_gaps([c(0, 106, 107, 105, 105.5), c(1, 105.5, 105.7, 100, 100.5), c(2, 100.5, 102, 99, 101)])
        self.assertEqual([(g.side, g.bottom, g.top) for g in gaps], [(BEARISH, 102, 105)])

    def test_overlapping_wicks_are_not_a_gap(self):
        # Day 16, 09:41-11:13: the wicks already filled it.
        self.assertEqual(find_gaps([c(0, 100, 104, 99, 100.5), c(1, 100.5, 106, 100.3, 105.5),
                                    c(2, 105.5, 107, 103.5, 106)]), [])

    def test_forming_third_candle_does_not_confirm(self):
        self.assertEqual(find_gaps([c(0, 100, 101, 99, 100.5), c(1, 100.5, 106, 100.3, 105.5),
                                    c(2, 105.5, 107, 103, 106, closed=False)]), [])

    def test_middle_candle_must_move_in_the_gaps_direction(self):
        # A down candle 2 between non-overlapping wicks (e.g. an overnight gap) isn't a void it created.
        self.assertEqual(find_gaps([c(0, 100, 101, 99, 100.5), c(1, 106, 106.5, 104, 104.5),
                                    c(2, 105.5, 107, 103, 106)]), [])


class Follow(unittest.TestCase):
    def setUp(self):
        self.base = [c(0, 100, 101, 99, 100.5), c(1, 100.5, 106, 100.3, 105.5), c(2, 105.5, 107, 103, 106)]

    def test_enter_then_react(self):
        candles = self.base + [c(3, 106, 106.5, 104, 104.5), c(4, 104.5, 105, 102, 102.5),
                               c(5, 102.5, 104.5, 101.8, 104)]
        ev = follow(candles, find_gaps(candles)[0])
        self.assertEqual((ev.entered_at, ev.reacted_at, ev.broken_at), (4, 5, None))

    def test_close_beyond_far_side_breaks_it(self):
        candles = self.base + [c(3, 106, 106.5, 102, 102.5), c(4, 102.5, 103, 99, 100)]
        ev = follow(candles, find_gaps(candles)[0])
        self.assertEqual((ev.entered_at, ev.broken_at), (3, 4))


if __name__ == "__main__":
    unittest.main()
