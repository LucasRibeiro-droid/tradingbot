import tempfile
import unittest
from datetime import date
from pathlib import Path

from tradingbot.config import LOCKED
from tradingbot.discipline import (Decision, adherence, audit, streak, write_daily_entry)


class Audit(unittest.TestCase):
    def rules(self, *decisions):
        return [v.rule for v in audit(decisions)]

    def test_following_the_plan_has_no_violations(self):
        ds = [Decision("a", True, True, "target", 1.0, 1.0), Decision("b", False, False)]
        self.assertEqual(self.rules(*ds), [])
        self.assertEqual(adherence(ds), 1.0)

    def test_skipping_a_valid_setup_is_a_violation(self):
        self.assertEqual(self.rules(Decision("a", True, False)), ["skipped_valid_setup"])

    def test_trading_without_a_setup_is_a_violation(self):
        self.assertEqual(self.rules(Decision("a", False, True, "stop")), ["trade_without_setup"])

    def test_bailing_out_is_a_violation(self):
        self.assertEqual(self.rules(Decision("a", True, True, "manual")), ["exit_off_plan"])

    def test_oversized_risk_is_a_violation(self):
        self.assertEqual(self.rules(Decision("a", True, True, "stop", 2.0, 1.0)), ["oversized_risk"])

    def test_adherence_counts_decisions_not_violations(self):
        ds = [Decision("a", False, True, "manual"), Decision("b", True, True, "target")]
        self.assertEqual(adherence(ds), 0.5)

    def test_rules_are_locked(self):
        self.assertTrue(LOCKED.follow_plan_exactly)
        self.assertTrue(LOCKED.always_improving)


class Habit(unittest.TestCase):
    def test_streak_counts_back_from_today_or_yesterday(self):
        days = [date(2026, 10, d) for d in (15, 16, 17, 18)]
        self.assertEqual(streak(days, date(2026, 10, 18)), 4)
        self.assertEqual(streak(days, date(2026, 10, 19)), 4)
        self.assertEqual(streak(days, date(2026, 10, 20)), 0)

    def test_daily_entry_requires_a_next_step_and_tracks_the_streak(self):
        with tempfile.TemporaryDirectory() as d:
            folder = Path(d)
            with self.assertRaises(ValueError):
                write_daily_entry(date(2026, 10, 19), ["x"], ["y"], " ", directory=folder)
            write_daily_entry(date(2026, 10, 18), ["x"], ["y"], "z", directory=folder)
            p = write_daily_entry(date(2026, 10, 19), ["x"], ["y"], "z", directory=folder)
            self.assertIn("Streak: 2 days", p.read_text())


if __name__ == "__main__":
    unittest.main()
