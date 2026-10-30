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
        from tradingbot.config import BASELINE
        s.dry_run, s.trades, s.traded_symbols, s.config, s.today = False, [], set(), BASELINE, "2026-10-26"
        s.broker = type("B", (), {
            "orders": lambda self, status, after: [{"symbol": "NVDA", "filled_qty": "77", "client_order_id": "tjr_m1_15m-2026-10-26-NVDA-1000-0", "status": "filled"},
                                                   {"symbol": "AMD", "filled_qty": "0", "client_order_id": "tjr_m1_15m-2026-10-26-AMD-1000-0", "status": "canceled"},
                                                   {"symbol": "TSLA", "filled_qty": "9", "client_order_id": "crt_1h5m-2026-10-23-TSLA-1405-0", "status": "filled"},
                                                   {"symbol": "MU", "filled_qty": "48", "client_order_id": "manual-close"}],
            "positions": lambda self: []})()
        s._reconcile_start()
        self.assertEqual(s.traded_symbols, {"NVDA"})

    def test_reconcile_knows_open_day_trades(self):
        """After a hand-off, a day_rs3 position from its own state is not reported as unknown (2026-10-30 REGN)."""
        from unittest import mock
        from tradingbot.live import run
        from tradingbot.config import BASELINE
        s = run.Session.__new__(run.Session)
        s.dry_run, s.trades, s.traded_symbols, s.config, s.today = False, [], set(), BASELINE, "2026-10-30"
        s.day = type("D", (), {"trades": [{"symbol": "REGN"}, {"symbol": "DELL", "result": {"how": "stop"}}]})()
        s.broker = type("B", (), {"orders": lambda self, status, after: [],
                                  "positions": lambda self: [{"symbol": "REGN", "qty": "10"}, {"symbol": "XYZ", "qty": "1"}]})()
        with mock.patch.object(run, "event") as ev:
            s._reconcile_start()
        flagged = [c.args[0] for c in ev.call_args_list if "not in the saved state" in c.args[0]]
        self.assertEqual(flagged, ["position XYZ 1 at Alpaca is not in the saved state"])


class FakeAlpaca:
    """Like Alpaca: bracket legs hold the shares, so a close fails while orders are open, and a
    cancel takes effect a moment later."""

    def __init__(self, positions, open_orders):
        self._positions = {p: q for p, q in positions.items()}
        self._orders, self._cancelling, self.closed = open_orders, False, []

    def positions(self):
        return [{"symbol": s, "qty": str(q)} for s, q in self._positions.items()]

    def orders(self, status="open", after=None):
        if self._cancelling:  # the cancel lands on the next look
            self._orders, self._cancelling = 0, False
            return [{"id": "leg"}]
        return [{"id": "leg"}] * self._orders

    def cancel_all(self):
        self._cancelling = bool(self._orders)

    def close_position(self, symbol):
        if self._orders:
            raise BrokerError("insufficient qty available for order (held by open orders)")
        self.closed.append(symbol)
        del self._positions[symbol]
        return {}


class Flatten(unittest.TestCase):
    def _session(self, broker):
        from unittest import mock
        from tradingbot.live import run
        s = run.Session.__new__(run.Session)
        s.dry_run, s.trades, s.broker = False, [], broker
        s.manage = lambda: None
        return s, mock.patch.object(run, "event", lambda *a, **k: None)

    def test_waits_for_cancels_then_closes_and_verifies(self):
        broker = FakeAlpaca({"MU": 48, "NVDA": -230}, open_orders=6)
        s, quiet = self._session(broker)
        with quiet:
            self.assertTrue(s.flatten(pause=0))
        self.assertEqual(broker.positions(), [])
        self.assertEqual(sorted(broker.closed), ["MU", "NVDA"])

    def test_reports_failure_when_positions_stay(self):
        broker = FakeAlpaca({"MU": 48}, open_orders=1)
        broker.cancel_all = lambda: None  # cancels never land
        s, quiet = self._session(broker)
        with quiet:
            self.assertFalse(s.flatten(attempts=2, pause=0))


class Cache(unittest.TestCase):
    def test_loads_once_then_only_new_candles(self):
        from datetime import datetime, timezone
        from tradingbot.live.run import BarCache
        calls = []
        series = [Candle(f"2026-10-23T14:0{m}:00Z", 1, 2, 0.5, 1.5) for m in range(5)]

        def fetch(symbols, tf, start):
            calls.append((tuple(symbols), start))
            return {s: [c for c in series if c.t >= start.strftime("%Y-%m-%dT%H:%M:%SZ")] for s in symbols}

        cache = BarCache(fetch)
        now = datetime(2026, 10, 23, 14, 5, 30, tzinfo=timezone.utc)
        first = cache.get(["A"], "1Min", now)
        self.assertEqual(len(first["A"]), 5)
        series.append(Candle("2026-10-23T14:05:00Z", 1.5, 3, 1, 2.5))
        second = cache.get(["A"], "1Min", now)
        self.assertEqual([c.t[-9:-4] for c in second["A"]][-2:], ["14:04", "14:05"])
        self.assertEqual(len(second["A"]), 6)  # no duplicates
        self.assertEqual(calls[1][1], datetime(2026, 10, 23, 14, 4, tzinfo=timezone.utc))  # only from the last candle


class Adopt(unittest.TestCase):
    def test_rebuilds_a_lost_trade_from_alpaca_orders(self):
        from unittest import mock
        from tradingbot.live import run
        s = run.Session.__new__(run.Session)
        s.trades = []
        legs = lambda tp: [{"type": "limit", "status": "new", "limit_price": tp}, {"type": "stop", "status": "held", "stop_price": "40.5"}]
        orders = [{"id": f"o{k}", "client_order_id": f"orb30-2026-10-23-INTC-1415-{k}", "symbol": "INTC", "side": "buy",
                   "qty": "38", "status": "filled", "filled_avg_price": "42.0", "legs": legs(str(43 + k))} for k in range(3)]
        orders.append({"id": "x", "client_order_id": "tjr_m1_15m-2026-10-23-AAPL-1400-0", "symbol": "AAPL", "side": "sell",
                       "qty": "5", "status": "filled", "legs": [{"type": "stop", "status": "filled", "stop_price": "350"}]})
        with mock.patch.object(run, "event", lambda *a, **k: None):
            s._adopt(orders, held={"INTC"})
        self.assertEqual(len(s.trades), 1)  # AAPL finished and isn't held: left to the review
        t = s.trades[0]
        self.assertEqual((t.symbol, t.direction, t.stop, t.setup_t, t.strategy), ("INTC", 1, 40.5, "2026-10-23T14:15:00Z", "orb30"))
        self.assertEqual(t.targets, [43.0, 44.0, 45.0])


class CrtLive(unittest.TestCase):
    """CRT trades: same-direction trades stack on a stock, the stop stays fixed after 1:1, and a
    trade is recorded when its own legs sold every filled share (another may still hold the stock)."""

    def _session(self, broker):
        from tradingbot.config import BASELINE
        from tradingbot.live import run
        s = run.Session.__new__(run.Session)
        s.config, s.dry_run, s.trades, s.traded_symbols, s.halted, s.failures = BASELINE, False, [], set(), False, 0
        s.today, s.broker = "2026-10-26", broker
        s._save_state = lambda: None
        return s

    def _assessment(self, direction="long"):
        d = 1 if direction == "long" else -1
        return {"symbol": "MU", "t": "2026-10-26T15:05:00Z", "strategy": "crt_1h5m", "timeframe": "5Min",
                "plan": {"direction": direction, "entry": 100.0, "entry_type": "limit", "stop": 100.0 - d * 0.2,
                         "expires_at": "2026-10-26T15:30:00+00:00", "take_profits": [100.0 + d * 0.2, 100.0 + d * 0.6],
                         "invalidation": "x", "entry_condition": "x", "rr_first": 1.0, "rr_last": 3.0},
                "context": {"bias_relation": "n/a"}, "setup": "x", "present": [], "conflicts": [], "decision": "APPROVED"}

    def test_stacks_same_direction_and_refuses_the_other(self):
        from unittest import mock
        from tradingbot.live import run
        placed = []
        broker = type("B", (), {
            "positions": lambda self: [{"symbol": "MU", "qty": "50"}],
            "account": lambda self: {"equity": "100000", "buying_power": "200000"},
            "bracket": lambda self, *a, **k: placed.append((a, k)) or {"id": f"o{len(placed)}"}})()
        s = self._session(broker)
        s.trades = [run.Trade("MU", "2026-10-26T15:00:00Z", 1, 99.0, 98.8, [99.2, 99.6], strategy="crt_1h5m")]
        with mock.patch.object(run, "event", lambda *a, **k: None), mock.patch.object(run, "trade_page", lambda *a: run.ROOT / "x.md"), \
                mock.patch.object(run, "_append", lambda *a: None):
            a = self._assessment("long")
            s._approve(a)
            self.assertEqual(a["decision"], "APPROVED")
            self.assertEqual(len(placed), 2)  # half at 1:1, half at 3R
            self.assertEqual([k["limit_price"] for _, k in placed], [100.0, 100.0])
            self.assertEqual(s.trades[-1].expires_at, "2026-10-26T15:30:00+00:00")
            self.assertEqual(s.trades[-1].targets, [100.2, 100.6])
            b = self._assessment("short")
            b["t"] = "2026-10-26T15:10:00Z"
            s._approve(b)
            self.assertEqual(b["decision"], "REJECTED")
        self.assertEqual(len(placed), 2)

    def test_stop_stays_fixed_and_exit_recorded_from_own_legs(self):
        from unittest import mock
        from tradingbot.live import run
        orders = {"o1": {"id": "o1", "status": "filled", "filled_qty": "25", "filled_avg_price": "100.0",
                         "legs": [{"id": "l1", "type": "limit", "status": "filled", "filled_qty": "25", "filled_avg_price": "100.2"},
                                  {"id": "s1", "type": "stop", "status": "canceled", "filled_qty": "0"}]},
                  "o2": {"id": "o2", "status": "filled", "filled_qty": "25", "filled_avg_price": "100.0",
                         "legs": [{"id": "l2", "type": "limit", "status": "new", "filled_qty": "0"},
                                  {"id": "s2", "type": "stop", "status": "held", "filled_qty": "0"}]}}
        moved = []
        broker = type("B", (), {"order": lambda self, i: orders[i], "replace_stop": lambda self, *a: moved.append(a),
                                "positions": lambda self: [{"symbol": "MU", "qty": "75"}]})()
        s = self._session(broker)
        t = run.Trade("MU", "2026-10-26T15:05:00Z", 1, 100.0, 99.8, [100.2, 100.6], strategy="crt_1h5m",
                      parts=[{"order_id": "o1"}, {"order_id": "o2"}])
        s.trades = [t]
        recs = []
        with mock.patch.object(run, "event", lambda *a, **k: None), mock.patch.object(run, "_append", lambda p, r: recs.append(r)):
            s.manage()
            self.assertEqual(moved, [])  # 1:1 filled, the stop stays where it was
            self.assertFalse(t.closed)
            orders["o2"]["legs"] = [{"id": "l2", "type": "limit", "status": "canceled", "filled_qty": "0"},
                                    {"id": "s2", "type": "stop", "status": "filled", "filled_qty": "25", "filled_avg_price": "99.8"}]
            s.manage()  # MU is still held (another trade), but this trade's legs sold all 50 shares
        self.assertTrue(t.closed)
        exit_rec = recs[-1]
        self.assertEqual(exit_rec["type"], "exit")
        self.assertAlmostEqual(exit_rec["r"], 0.0)  # +1R on half, -1R on half


if __name__ == "__main__":
    unittest.main()
