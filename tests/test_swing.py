import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tradingbot.live import swing


class Signal(unittest.TestCase):
    def test_three_lower_closes_above_the_average(self):
        up = [100 + k * 0.1 for k in range(199)]  # an uptrend
        self.assertIsNone(swing.signal(up, up[-1] + 0.1))  # no pullback
        pull = up[:-2] + [up[-2] - 0.3, up[-2] - 0.6]
        self.assertAlmostEqual(swing.signal(pull, pull[-1] - 0.3), (pull[-1] - 0.3) / up[-3] - 1)
        self.assertIsNone(swing.signal(pull, pull[-1] - 30))  # broke below the 200-day average


class Broker:
    def __init__(self):
        self.orders, self.n = {}, 0

    def simple(self, sym, qty, side, cid, time_in_force="day", order_type="market", stop_price=None):
        self.n += 1
        self.orders[f"o{self.n}"] = {"status": "new", "kind": order_type, "side": side, "stop": stop_price}
        return {"id": f"o{self.n}"}

    def order(self, i):
        return self.orders[i]

    def cancel(self, i):
        self.orders[i]["status"] = "canceled"


class Lifecycle(unittest.TestCase):
    def test_fill_then_stop_then_record(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.object(swing, "ROOT", Path(d)):
            b = Broker()
            s = swing.Swing(b)
            s.positions["AAPL"] = {"status": "pending", "qty": 10, "entry_date": "2026-10-28", "signal_price": 100.0,
                                   "drop_3d": -0.03, "entry_id": b.simple("AAPL", 10, "buy", "x", "cls")["id"], "stop_id": None, "exit_id": None}
            b.orders["o1"].update(status="filled", filled_avg_price="100.0", filled_qty="10")
            s.reconcile()
            p = s.positions["AAPL"]
            self.assertEqual((p["status"], p["stop"]), ("open", 90.0))  # 10% stop placed after the fill
            s.exit("AAPL", p, "close above the previous day's high", "2026-10-30")
            self.assertEqual(b.orders[p["stop_id"]]["status"], "canceled")  # stop cancelled before selling
            b.orders[p["exit_id"]].update(status="filled", filled_avg_price="102.0")
            s.reconcile()
            self.assertNotIn("AAPL", s.positions)
            self.assertIn('"r": 0.2', (Path(d) / "trades.jsonl").read_text())  # +2% on a 10% stop


if __name__ == "__main__":
    unittest.main()
