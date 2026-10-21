import unittest

from tradingbot.candles import Candle
from tradingbot.exits import simulate_partials, take_profits


def c(t, o, h, l, cl):
    return Candle(f"2026-01-01T00:{t:02d}:00Z", o, h, l, cl)


class Ladder(unittest.TestCase):
    def test_first_target_is_the_first_higher_timeframe_draw_at_least_one_to_one(self):
        # Day 37, 03:39 and 06:37: the one-higher-timeframe draw on liquidity, minimum 1:1.
        tps = take_profits(1, entry=100, stop=98, htf_draws=[101, 103, 110], other_levels=[104, 106])
        self.assertEqual(tps, [103, 104, 106])

    def test_short_mirrors(self):
        tps = take_profits(-1, entry=100, stop=102, htf_draws=[99, 97], other_levels=[95, 96])
        self.assertEqual(tps, [97, 96, 95])

    def test_no_draw_far_enough_no_ladder(self):
        self.assertEqual(take_profits(1, entry=100, stop=98, htf_draws=[101], other_levels=[110]), [])


class Partials(unittest.TestCase):
    def test_thirds_then_break_even(self):
        # Entry 100, stop 98 (risk 2); TP1 at 102 (+1R on a third), then back to entry.
        candles = [c(0, 100, 100, 100, 100), c(1, 100, 102.5, 99.5, 102), c(2, 102, 102, 99.5, 99.8)]
        res = simulate_partials(candles, 0, 1, 100, 98, [102, 104, 106], max_bars=10)
        self.assertEqual((res["exit"], res["hit"], res["r"]), ("break_even", 1, round(1 / 3, 3)))

    def test_all_targets(self):
        candles = [c(0, 100, 100, 100, 100), c(1, 100, 107, 99.5, 106.5)]
        res = simulate_partials(candles, 0, 1, 100, 98, [102, 104, 106], max_bars=10)
        self.assertEqual((res["exit"], res["r"]), ("target", round((1 + 2 + 3) / 3, 3)))

    def test_stop_first_is_minus_one(self):
        candles = [c(0, 100, 100, 100, 100), c(1, 100, 101, 97.5, 98)]
        self.assertEqual(simulate_partials(candles, 0, 1, 100, 98, [102, 104], max_bars=10)["r"], -1.0)


if __name__ == "__main__":
    unittest.main()
