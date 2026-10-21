import unittest
from datetime import timedelta

from tradingbot.candles import Candle
from tradingbot.live.broker import BrokerError, Paper
from tradingbot.live.signals import assess, size, split


class Sizing(unittest.TestCase):
    def test_one_percent_risk(self):
        # $10,000 equity, 1% = $100; $0.50 risk per share -> 200 shares, if cash allows.
        self.assertEqual(size(10_000, 50_000, 50.0, 49.5, 1.0), 200)

    def test_capped_by_buying_power(self):
        self.assertEqual(size(10_000, 1_000, 50.0, 49.5, 1.0), 20)

    def test_capped_by_position_size(self):
        # $100,000 equity, 10% cap = $10,000 at $200 -> 50 shares, though 1% risk allows 500.
        self.assertEqual(size(100_000, 400_000, 200.0, 198.0, 1.0, 10.0), 50)

    def test_cannot_size(self):
        self.assertEqual(size(99.98, 99.98, 262.0, 260.0, 1.0), 0)

    def test_ladder_split(self):
        self.assertEqual(split(10, [1, 2, 3]), [(4, 1), (3, 2), (3, 3)])
        self.assertEqual(split(2, [1, 2, 3]), [(1, 1), (1, 2)])
        self.assertEqual(split(0, [1, 2, 3]), [])


class PaperGuard(unittest.TestCase):
    def test_refuses_a_live_account(self):
        p = Paper("k", "s")
        p._call = lambda *a, **k: {"account_number": "123456", "status": "ACTIVE"}
        with self.assertRaises(BrokerError):
            p.connect()

    def test_accepts_paper(self):
        p = Paper("k", "s")
        p._call = lambda *a, **k: {"account_number": "PA3L67J2X", "status": "ACTIVE"}
        self.assertEqual(p.connect()["account_number"], "PA3L67J2X")


class Assessment(unittest.TestCase):
    def test_no_setup_no_assessment(self):
        candles = [Candle(f"2026-01-05T15:{m:02d}:00Z", 100, 101, 99, 100.5) for m in range(0, 60, 15)]
        self.assertIsNone(assess("X", candles, candles, candles, ltf_length=timedelta(minutes=15)))


class Restart(unittest.TestCase):
    """The session must survive being stopped and restarted (GitHub Actions hand-offs)."""

    def _clock(self, is_open, next_open_in):
        from datetime import datetime, timezone
        nxt = (datetime.now(timezone.utc) + next_open_in).isoformat()
        return lambda self: {"is_open": is_open, "next_open": nxt}

    def _window(self, clock):
        from unittest import mock
        from tradingbot.live import run
        with mock.patch.object(run.Paper, "__init__", lambda self: None), \
                mock.patch.object(run.Paper, "clock", clock):
            return run.in_session_window()

    def test_window_far_from_open(self):
        self.assertFalse(self._window(self._clock(False, timedelta(hours=10))))

    def test_window_near_open(self):
        from datetime import datetime
        from tradingbot.live.run import NY
        if datetime.now(NY).strftime("%H:%M") >= "15:55":
            self.skipTest("past the flatten time in New York")
        self.assertTrue(self._window(self._clock(False, timedelta(minutes=30))))

    def test_reconcile_counts_filled_symbols(self):
        from tradingbot.live.run import Session
        s = Session.__new__(Session)
        s.dry_run, s.trades, s.traded_symbols = False, [], set()
        s.broker = type("B", (), {
            "orders": lambda self, status, after: [{"symbol": "NVDA", "filled_qty": "77"},
                                                   {"symbol": "AMD", "filled_qty": "0"}],
            "positions": lambda self: []})()
        s._reconcile_start()
        self.assertEqual(s.traded_symbols, {"NVDA"})


if __name__ == "__main__":
    unittest.main()
