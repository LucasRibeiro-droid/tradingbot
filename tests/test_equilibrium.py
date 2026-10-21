import unittest

from tradingbot.candles import Candle
from tradingbot.equilibrium import Range, ranges
from tradingbot.trend import DOWN, UP, TrendState


def c(t, o, h, l, cl):
    return Candle(f"2026-01-01T00:{t:02d}:00Z", o, h, l, cl)


def st(event=None, direction=UP):
    return TrendState(direction, False, None, None, event)


class Measure(unittest.TestCase):
    def test_depth_and_discount(self):
        # Day 28, 01:39-02:24: below the 50 mark of low -> high is the discount.
        r = Range(UP, 100, 110)
        self.assertEqual((r.mid, r.depth(110), r.depth(105), r.depth(102)), (105, 0, 0.5, 0.8))
        self.assertEqual(Range(DOWN, 100, 110).depth(108), 0.8)

    def test_drag_the_high_until_equilibrium_is_hit(self):
        # Day 28, 08:20: "doesn't get hit ... we go higher, we drag it higher".
        candles = [c(0, 101, 102, 100, 101.5), c(1, 101.5, 106, 101, 105.5), c(2, 105.5, 106, 104, 104.5),
                   c(3, 104.5, 110, 104, 109)]
        states = [st(direction=0), st("bos_up"), st(), st()]
        r = ranges(candles, states)
        self.assertIsNone(r[0])
        self.assertEqual((r[1].low, r[1].high), (100, 106))
        self.assertEqual((r[3].low, r[3].high), (100, 110))  # dip to 104 didn't reach 103: same low

    def test_measure_again_after_the_dip_reaches_equilibrium(self):
        # Day 28, 09:01: once a dip reaches 50%, the next high is measured from that dip's low.
        candles = [c(0, 101, 102, 100, 101.5), c(1, 101.5, 110, 101, 109), c(2, 109, 109.5, 104, 104.5),
                   c(3, 104.5, 112, 104.5, 111.5)]
        states = [st(direction=0), st("bos_up"), st(), st()]
        r = ranges(candles, states)
        self.assertEqual((r[3].low, r[3].high), (104, 112))


if __name__ == "__main__":
    unittest.main()
