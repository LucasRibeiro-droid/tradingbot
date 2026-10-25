import unittest

from tradingbot.candles import Candle
from tradingbot.live.crt_owner import Order, simulate


def bar(m, o, h, l, c):
    return Candle(f"2026-10-20T14:{m:02d}:00Z", o, h, l, c)


class OwnerExits(unittest.TestCase):
    order = Order("X", 1, 100.0, 99.0, placed=1, expires=2, setup_t="t")  # 1R = 1

    def test_1to1_then_back_to_entry_is_half_a_win(self):
        bars = [bar(0, 102, 102, 101, 101.5), bar(5, 101, 101, 99.9, 100.2), bar(10, 100.2, 101.3, 100.1, 101),
                bar(15, 101, 101, 99.8, 99.9)]
        t = simulate(bars, self.order, 3)
        self.assertEqual([w for _, _, w in t["legs"]], ["1:1", "break even"])
        self.assertAlmostEqual(t["r_gross"], 0.5, places=2)  # half +1R, half 0

    def test_target(self):
        bars = [bar(0, 102, 102, 101, 101.5), bar(5, 101, 101, 99.9, 100.2), bar(10, 100.2, 101.3, 100.1, 101),
                bar(15, 101, 103.2, 100.6, 103)]
        t = simulate(bars, self.order, 3)
        self.assertAlmostEqual(t["r_gross"], 2.0, places=2)  # half +1R, half +3R

    def test_stopped(self):
        bars = [bar(0, 102, 102, 101, 101.5), bar(5, 101, 101, 99.9, 100.2), bar(10, 100.2, 100.5, 98.8, 99)]
        self.assertAlmostEqual(simulate(bars, self.order, 3)["r_gross"], -1.0, places=2)


if __name__ == "__main__":
    unittest.main()
