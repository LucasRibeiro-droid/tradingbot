import unittest

from tradingbot.candles import (BEARISH, BULLISH, NEUTRAL, Candle, FormingCandleError,
                                read, shape)
from tradingbot.config import BASELINE, LOCKED, with_change
from tradingbot.study import reaction, run

P = BASELINE.candle


def ctx(*last: Candle, n: int = 25) -> list[Candle]:
    """Average-sized filler candles (range 2) followed by the candles under test."""
    filler = [Candle(f"f{i}", 100, 101, 99, 100.5) for i in range(n)]
    return filler + list(last)


class Anatomy(unittest.TestCase):
    def test_bullish_parts(self):
        c = Candle("t", o=100, h=106, l=98, c=104)
        self.assertEqual(c.direction, BULLISH)
        self.assertEqual(c.body, 4)
        self.assertEqual(c.upper_wick, 2)
        self.assertEqual(c.lower_wick, 2)

    def test_bearish_open_is_top_of_body(self):
        c = Candle("t", o=104, h=106, l=98, c=100)
        self.assertEqual(c.direction, BEARISH)
        self.assertEqual(c.upper_wick, 2)
        self.assertEqual(c.lower_wick, 2)

    def test_rejects_impossible_candle(self):
        with self.assertRaises(ValueError):
            Candle("t", o=100, h=99, l=98, c=99)


class Shapes(unittest.TestCase):
    def test_doji_family(self):
        self.assertEqual(shape(Candle("t", 100, 100.1, 96, 100.05), 0, P), "dragonfly_doji")
        self.assertEqual(shape(Candle("t", 100, 104, 99.95, 100.05), 0, P), "gravestone_doji")
        self.assertEqual(shape(Candle("t", 100, 102, 98, 100.1), 0, P), "long_legged_doji")

    def test_hammer_vs_hanging_man_depends_on_prior_move(self):
        c = Candle("t", 100, 101.05, 97, 101)
        self.assertEqual(shape(c, BEARISH, P), "hammer")
        self.assertEqual(shape(c, BULLISH, P), "hanging_man")

    def test_strong_close(self):
        self.assertEqual(shape(Candle("t", 100, 104.1, 99.8, 104), 0, P), "strong_close")


class Reads(unittest.TestCase):
    def test_forming_candle_cannot_be_read(self):
        self.assertTrue(LOCKED.closed_candles_only)
        candles = ctx(Candle("live", 100, 104, 99, 103.9, closed=False))
        with self.assertRaises(FormingCandleError):
            read(candles, len(candles) - 1)

    def test_strong_bullish_close_leans_bullish(self):
        candles = ctx(Candle("t", 100, 104.1, 99.8, 104))
        r = read(candles, len(candles) - 1)
        self.assertEqual((r.shape, r.lean), ("strong_close", BULLISH))

    def test_long_lower_wick_closing_high_is_strong_bullish_rejection(self):
        # Day 2, 17:30: massive wick down, tiny wick up, closes almost as bullish as it could.
        candles = ctx(Candle("t", 100, 101.6, 95, 101.5))
        r = read(candles, len(candles) - 1)
        self.assertEqual(r.lean, BULLISH)
        self.assertIn("very strong bullish rejection", " ".join(r.notes))

    def test_bullish_candle_with_fat_upper_wick_is_weakness(self):
        # Day 2, 10:00: pushed up, still closed bullish, but not strong enough to close up there.
        candles = ctx(Candle("t", 100, 104, 99.9, 101.5))
        r = read(candles, len(candles) - 1)
        self.assertEqual(r.lean, BEARISH)
        self.assertIn("bullish weakness", " ".join(r.notes))

    def test_doji_after_selloff_shows_fading_bearish_momentum(self):
        selloff = [Candle(f"s{i}", 100 - 2 * i, 100.2 - 2 * i, 97.8 - 2 * i, 98 - 2 * i) for i in range(6)]
        candles = ctx(*selloff, Candle("d", 88, 89.5, 86.5, 88.1))
        r = read(candles, len(candles) - 1)
        self.assertTrue(r.shape.endswith("doji"))
        self.assertEqual(r.lean, BULLISH)
        self.assertIn("fading", " ".join(r.notes))

    def test_tiny_candle_is_not_read(self):
        candles = ctx(Candle("t", 100, 100.3, 99.9, 100.25))
        self.assertFalse(read(candles, len(candles) - 1).readable)

    def test_reads_are_never_entry_signals(self):
        self.assertFalse(LOCKED.candle_read_is_entry_signal)
        self.assertLessEqual(LOCKED.max_pattern_candles, 2)


class Study(unittest.TestCase):
    def test_reaction_reports_which_side_was_taken_first(self):
        candles = [Candle("a", 100, 101, 99, 100.5), Candle("b", 100.5, 101.5, 100, 101.2),
                   Candle("c", 101.2, 102, 101, 101.8)]
        r = reaction(candles, 0, 2)
        self.assertEqual(r["first_taken"], "high")
        self.assertGreater(r["move"], 0)

    def test_incomplete_window_is_skipped(self):
        candles = [Candle("a", 100, 101, 99, 100.5), Candle("b", 100.5, 101, 100, 100.8, closed=False)]
        self.assertIsNone(reaction(candles, 0, 1))

    def test_run_produces_summary_against_base_rate(self):
        candles = ctx(Candle("t", 100, 104.1, 99.8, 104), *[Candle(f"n{i}", 104 + i, 105.5 + i, 103.5 + i, 105 + i) for i in range(6)])
        result = run(candles)
        self.assertIn("ALL:bull", result["summary"])
        self.assertIn("base_rate", result["summary"]["ALL:bull"])

    def test_with_change_changes_exactly_one_field(self):
        changed = with_change(BASELINE, "candle", "doji_max_body_pct", 0.05)
        self.assertEqual(changed.candle.doji_max_body_pct, 0.05)
        self.assertEqual(changed.candle.long_wick_min_pct, BASELINE.candle.long_wick_min_pct)
        self.assertEqual(changed.study, BASELINE.study)
        self.assertNotEqual(changed.version, BASELINE.version)


if __name__ == "__main__":
    unittest.main()
