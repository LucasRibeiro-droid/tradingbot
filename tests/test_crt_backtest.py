import unittest

from tradingbot.candles import Candle
from tradingbot.live.crt_backtest import Order, simulate


def bar(m, o, h, l, c):
    return Candle(f"2026-10-20T14:{m:02d}:00Z", o, h, l, c)


class Exits(unittest.TestCase):
    def order(self):
        # Long: entry 100, stop 99 (1R = 1), half at 101, the rest at 103.
        return Order("X", 1, 100.0, 99.0, 101.0, 103.0, placed=1, expires=2, setup_t="t", crh=103.0, crl=98.0)

    def test_half_at_1R_then_stop_is_break_even(self):
        bars = [bar(0, 102, 102, 101, 101.5), bar(5, 101, 101, 99.9, 100.2), bar(10, 100.2, 101.2, 100, 101),
                bar(15, 101, 101, 98.5, 98.8)]
        t = simulate(bars, self.order(), cost_bps=0)
        self.assertEqual([w for _, _, w in t["legs"]], ["1:1", "stop"])
        self.assertAlmostEqual(t["r"], 0.0, places=2)

    def test_full_win(self):
        bars = [bar(0, 102, 102, 101, 101.5), bar(5, 101, 101, 99.9, 100.2), bar(10, 100.2, 101.5, 100, 101.4),
                bar(15, 101.4, 103.5, 101, 103.2)]
        t = simulate(bars, self.order(), cost_bps=0)
        self.assertAlmostEqual(t["r"], 2.0, places=2)  # half +1R, half +3R

    def test_targets_not_counted_on_the_fill_bar(self):
        bars = [bar(0, 102, 102, 101, 101.5), bar(5, 101, 103.5, 99.9, 100.2), bar(10, 100.2, 100.3, 98.9, 99)]
        t = simulate(bars, self.order(), cost_bps=0)
        self.assertEqual([w for _, _, w in t["legs"]], ["stop"])

    def test_unfilled(self):
        bars = [bar(0, 102, 102, 101, 101.5), bar(5, 101.5, 102, 100.5, 101), bar(10, 101, 102, 100.6, 101.5)]
        self.assertIsNone(simulate(bars, self.order(), cost_bps=0))


if __name__ == "__main__":
    unittest.main()
