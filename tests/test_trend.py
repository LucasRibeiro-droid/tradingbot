import unittest
from datetime import timedelta

from tradingbot.candles import Candle
from tradingbot.config import LOCKED, TrendParams
from tradingbot.trend import (DOWN, NONE, UP, TrendState, bias, efficiency, state_at, swings,
                              trend_series)


def path(*closes: float, wick: float = 0.2) -> list[Candle]:
    """Candles that walk through the given closes, each opening at the previous close."""
    out, prev = [], closes[0]
    for i, c in enumerate(closes):
        o = prev
        out.append(Candle(f"2026-01-01T00:{i:02d}:00Z", o, max(o, c) + wick, min(o, c) - wick, c))
        prev = c
    return out


def zigzag(points: list[float], steps: int = 3) -> list[float]:
    """Straight-line closes between turning points, like TJR's drawn trend (Day 4, 02:13)."""
    out = [points[0]]
    for a, b in zip(points, points[1:]):
        out += [a + (b - a) * k / steps for k in range(1, steps + 1)]
    return out


P = TrendParams(consolidation_lookback=6)


class Swings(unittest.TestCase):
    def test_finds_turning_points_only_after_they_are_confirmed(self):
        candles = path(*zigzag([100, 110, 104, 116]))
        found = swings(candles, P)
        kinds = [(s.kind, s.index) for s in found]
        self.assertIn(("high", 3), kinds)
        self.assertIn(("low", 6), kinds)
        for s in found:
            self.assertEqual(s.confirmed_at, s.index + P.swing_strength)


class Trends(unittest.TestCase):
    def test_higher_highs_and_higher_lows_is_an_uptrend(self):
        states = trend_series(path(*zigzag([100, 110, 104, 116, 110, 122, 116, 128])), P)
        self.assertEqual(states[-1].direction, UP)

    def test_lower_highs_and_lower_lows_is_a_downtrend(self):
        states = trend_series(path(*zigzag([128, 118, 124, 112, 118, 106, 112, 100])), P)
        self.assertEqual(states[-1].direction, DOWN)

    def test_close_below_the_last_higher_low_flips_the_trend(self):
        # Day 4, 04:24: "higher high, now lower low because we just surpassed this".
        states = trend_series(path(*zigzag([100, 110, 104, 116, 110, 122, 116, 128, 100])), P)
        self.assertEqual(states[-1].direction, DOWN)
        self.assertTrue(any(s.shifted for s in states))

    def test_no_direction_until_two_highs_and_two_lows(self):
        states = trend_series(path(*zigzag([100, 110, 104])), P)
        self.assertEqual(states[-1].direction, NONE)

    def test_forming_candle_never_flips_the_trend(self):
        candles = path(*zigzag([100, 110, 104, 116, 110, 122, 116, 128]))
        last = candles[-1]
        candles.append(Candle("live", last.c, last.c, 90, 91, closed=False))
        self.assertEqual(trend_series(candles, P)[-1].direction, UP)

    def test_line_chart_swings_use_closes(self):
        candles = path(*zigzag([100, 110, 104, 116]), wick=5)
        prices = {s.price for s in swings(candles, TrendParams(swing_source="close"))}
        self.assertIn(110, prices)


class Consolidation(unittest.TestCase):
    def test_chop_is_consolidation_and_has_no_tradeable_direction(self):
        candles = path(100, 101, 100, 101, 100, 101, 100, 101)
        self.assertLess(efficiency(candles, len(candles) - 1, 6), 0.3)
        s = TrendState(UP, True, 101, 100)
        self.assertEqual(s.tradeable_direction, NONE)

    def test_straight_move_is_efficient(self):
        candles = path(*range(100, 110))
        self.assertGreater(efficiency(candles, len(candles) - 1, 6), 0.8)


class Timeframes(unittest.TestCase):
    def test_lower_timeframe_must_agree_with_higher(self):
        htf_down, ltf_up, ltf_down = (TrendState(DOWN, False, 1, 0), TrendState(UP, False, 1, 0),
                                      TrendState(DOWN, False, 1, 0))
        # Day 4, 08:44: the 15-minute says up, the daily says down: wait.
        self.assertEqual(bias(htf_down, ltf_up).direction, DOWN)
        self.assertFalse(bias(htf_down, ltf_up).ready)
        self.assertTrue(bias(htf_down, ltf_down).ready)

    def test_no_bias_when_higher_timeframe_consolidates(self):
        self.assertFalse(bias(TrendState(UP, True, 1, 0), TrendState(UP, False, 1, 0)).ready)

    def test_only_closed_higher_candles_count(self):
        daily = [Candle("2026-01-05T05:00:00Z", 1, 2, 0.5, 1.5), Candle("2026-01-06T05:00:00Z", 1.5, 2, 1, 1.8)]
        states = [TrendState(UP, False, 2, 0.5), TrendState(DOWN, False, 2, 1)]
        # Midday on Jan 6: that day's candle has not closed, so Jan 5's state applies.
        self.assertEqual(state_at(daily, states, timedelta(days=1), "2026-01-06T15:00:00Z").direction, UP)

    def test_rule_is_locked(self):
        self.assertFalse(LOCKED.trade_against_htf_trend)
        self.assertLessEqual(LOCKED.max_instruments, 2)


if __name__ == "__main__":
    unittest.main()


class Forecast(unittest.TestCase):
    def test_call_follows_the_higher_timeframe(self):
        from tradingbot.forecast import call
        self.assertEqual(call(TrendState(DOWN, False, 1, 0), TrendState(UP, False, 1, 0))["direction"], "down")
        self.assertIn("wait", call(TrendState(DOWN, False, 1, 0), TrendState(UP, False, 1, 0))["note"])
        self.assertEqual(call(TrendState(UP, True, 1, 0), TrendState(UP, False, 1, 0))["direction"], "no call")

    def test_grading_targets(self):
        from datetime import date
        from tradingbot.forecast import _target_close
        days = [Candle(f"2026-10-{d:02d}T04:00:00Z", 1, 2, 0.5, 1 + d / 100) for d in (19, 20, 21, 22, 23, 26)]
        start = date(2026, 10, 19)
        self.assertEqual(_target_close(days, start, "today").t[:10], "2026-10-19")
        self.assertEqual(_target_close(days, start, "next_days").t[:10], "2026-10-21")
        self.assertEqual(_target_close(days, start, "week").t[:10], "2026-10-23")
        self.assertIsNone(_target_close(days[:5], start, "week"))  # week not over yet
