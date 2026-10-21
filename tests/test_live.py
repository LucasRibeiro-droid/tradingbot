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


if __name__ == "__main__":
    unittest.main()
