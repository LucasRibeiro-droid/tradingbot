import unittest

from tradingbot.candles import Candle
from tradingbot.live.daytrade import rank


class Rank(unittest.TestCase):
    def test_strongest_since_the_open_first(self):
        mk = lambda t, o, h, l, c: Candle(t, o, h, l, c)
        bars = {"A": [mk("2026-10-28T13:30:00Z", 10, 10.5, 9.9, 10.4), mk("2026-10-28T13:35:00Z", 10.4, 11, 10.3, 10.9)],
                "B": [mk("2026-10-28T13:30:00Z", 20, 20.2, 19.5, 19.6)],
                "C": [mk("2026-10-28T13:35:00Z", 30, 31, 29, 31)],  # no 09:30 candle: skipped
                "D": [mk("2026-10-28T13:30:00Z", 3, 3.5, 2.9, 3.4)]}  # under $5: skipped
        r = rank(bars, "2026-10-28")
        self.assertEqual([s for _, s, _, _ in r], ["A", "B"])
        self.assertAlmostEqual(r[0][0], 0.09)
        self.assertEqual(r[0][3], 9.9)  # day's low so far, for the stop


if __name__ == "__main__":
    unittest.main()
