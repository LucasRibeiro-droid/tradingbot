import unittest
from collections import Counter

from tradingbot.candles import Candle
from tradingbot.live.experiments import exit_for, orb_assess, targets_for


def bars(day, rows):
    """15-minute candles from 09:30 ET (13:30 UTC in October): rows of (o, h, l, c)."""
    out = []
    for k, (o, h, l, c) in enumerate(rows):
        m = 13 * 60 + 30 + 15 * k
        out.append(Candle(f"{day}T{m // 60:02d}:{m % 60:02d}:00Z", o, h, l, c))
    return out


class Exits(unittest.TestCase):
    def test_split_is_even_and_reproducible(self):
        picks = [exit_for("tjr_m1", ("a", "b"), f"X-{i}") for i in range(400)]
        self.assertEqual(picks, [exit_for("tjr_m1", ("a", "b"), f"X-{i}") for i in range(400)])
        n = Counter(picks)
        self.assertTrue(160 < n["a"] < 240, n)

    def test_targets_in_r(self):
        self.assertEqual(targets_for("ladder_0.5_1_2R", 1, 100.0, 98.0, []), [101.0, 102.0, 104.0])
        self.assertEqual(targets_for("2R", -1, 100.0, 101.0, []), [98.0])
        self.assertEqual(targets_for("tjr_ladder", 1, 100.0, 98.0, [103.0, 105.0]), [103.0, 105.0])


class OpeningRangeBreakout(unittest.TestCase):
    def test_first_close_above_the_range_is_a_long(self):
        ltf = bars("2026-10-22", [(100, 101, 99, 100.5), (100.5, 101.2, 99.8, 101), (101, 102, 100.9, 101.8)])
        a = orb_assess("X", ltf, shorting_enabled=True)
        self.assertEqual(a["plan"]["direction"], "long")
        self.assertEqual(a["plan"]["stop"], 100.1)  # middle of 99–101.2
        self.assertEqual(a["decision"], "APPROVED")

    def test_only_the_first_breakout_counts(self):
        ltf = bars("2026-10-22", [(100, 101, 99, 100.5), (100.5, 101, 99.8, 100), (100, 101.5, 99.9, 101.3),
                                  (101.3, 101.4, 100.2, 100.5), (100.5, 101.8, 100.4, 101.6)])
        self.assertIsNone(orb_assess("X", ltf, shorting_enabled=True))

    def test_inside_the_range_is_nothing(self):
        ltf = bars("2026-10-22", [(100, 101, 99, 100.5), (100.5, 101, 99.8, 100), (100, 100.8, 99.5, 100.2)])
        self.assertIsNone(orb_assess("X", ltf, shorting_enabled=True))

    def test_short_needs_shorting(self):
        ltf = bars("2026-10-22", [(100, 101, 99, 100.5), (100.5, 101, 99.8, 100), (100, 100.1, 98, 98.5)])
        self.assertEqual(orb_assess("X", ltf, shorting_enabled=False)["decision"], "REJECTED")


if __name__ == "__main__":
    unittest.main()
