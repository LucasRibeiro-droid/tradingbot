import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

from tradingbot.live import fx_run


class Hours(unittest.TestCase):
    def test_market_open(self):
        utc = lambda *a: datetime(*a, tzinfo=timezone.utc)
        self.assertTrue(fx_run.market_open(utc(2026, 10, 27, 15, 0)))    # Tuesday 11:00 ET
        self.assertFalse(fx_run.market_open(utc(2026, 10, 27, 21, 30)))  # daily break 17:30 ET
        self.assertFalse(fx_run.market_open(utc(2026, 10, 31, 15, 0)))   # Saturday
        self.assertFalse(fx_run.market_open(utc(2026, 11, 1, 21, 0)))    # Sunday 16:00 ET (EST)
        self.assertTrue(fx_run.market_open(utc(2026, 11, 1, 23, 30)))    # Sunday 18:30 ET


class Broker:
    def __init__(self):
        self.orders = {"1": {"state": "FILLED", "tradeOpenedID": "11"}, "2": {"state": "FILLED", "tradeOpenedID": "12"}}
        self.trades = {"11": {"state": "CLOSED", "price": "4000.0", "initialUnits": "1.5", "averageClosePrice": "4002.0", "realizedPL": "2.2"},
                       "12": {"state": "OPEN", "price": "4000.0", "initialUnits": "1.5"}}

    def order(self, i):
        return self.orders[i]

    def trade(self, i):
        return self.trades[i]


class Manage(unittest.TestCase):
    def test_records_only_when_every_part_is_closed(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.object(fx_run, "ROOT", Path(d)):
            b = Broker()
            s = fx_run.Session(broker=b)
            t = fx_run.Trade("XAU_USD", "2026-10-27T15:00:00Z", 1, 4000.0, 3998.0, [4002.0, 4006.0], "2026-10-27T15:30:00+00:00",
                             parts=[{"order_id": "1", "client_id": "a"}, {"order_id": "2", "client_id": "b"}])
            s.trades = [t]
            s.manage()
            self.assertFalse(t.closed)
            b.trades["12"] = {"state": "CLOSED", "price": "4000.0", "initialUnits": "1.5", "averageClosePrice": "3998.0", "realizedPL": "-2.2"}
            s.manage()
            self.assertTrue(t.closed)
            last = (Path(d) / "trades.jsonl").read_text().strip().splitlines()[-1]
            self.assertIn('"r": 0.0', last)  # +1R on half, -1R on half
            self.assertIn('"stop"', last)

    def test_not_filled(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.object(fx_run, "ROOT", Path(d)):
            b = Broker()
            b.orders = {"1": {"state": "CANCELLED"}}
            s = fx_run.Session(broker=b)
            t = fx_run.Trade("NAS100_USD", "2026-10-27T15:00:00Z", -1, 29000.0, 29010.0, [28990.0], "x", parts=[{"order_id": "1", "client_id": "a"}])
            s.trades = [t]
            s.manage()
            self.assertTrue(t.closed)
            self.assertIn("not_filled", (Path(d) / "trades.jsonl").read_text())


if __name__ == "__main__":
    unittest.main()
