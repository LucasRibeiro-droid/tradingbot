import unittest
from datetime import datetime, timezone

from tradingbot.live.broker import BrokerError
from tradingbot.live.oanda import PRACTICE_URL, Practice

# As the practice account reports them (2026-10-26).
SPECS = {"instruments": [{"name": "XAU_USD", "displayPrecision": 3, "tradeUnitsPrecision": 1},
                         {"name": "NAS100_USD", "displayPrecision": 1, "tradeUnitsPrecision": 2}]}


class Fake:
    def __init__(self, replies):
        self.replies, self.calls = replies, []

    def __call__(self, method, url, body):
        self.calls.append((method, url, body))
        assert url.startswith(PRACTICE_URL)  # practice host only
        for key, reply in self.replies:
            if key in url:
                return reply
        raise AssertionError(url)


class OandaPractice(unittest.TestCase):
    def test_limit_bracket_rounds_and_expires(self):
        fake = Fake([("/instruments?", SPECS), ("/orders", {"orderCreateTransaction": {"id": "7"}})])
        p = Practice("tok", "101-1", transport=fake)
        p.limit_bracket("NAS100_USD", -0.378, 29469.53, 29400.04, 29480.01, "crt-x", datetime(2026, 10, 27, 15, 30, tzinfo=timezone.utc))
        o = fake.calls[-1][2]["order"]
        self.assertEqual((o["units"], o["price"], o["takeProfitOnFill"]["price"], o["stopLossOnFill"]["price"]),
                         ("-0.37", "29469.5", "29400.0", "29480.0"))
        self.assertEqual((o["timeInForce"], o["gtdTime"]), ("GTD", "2026-10-27T15:30:00.000000000Z"))
        self.assertEqual(p.units("XAU_USD", 3.97), "3.9")

    def test_refused_order_raises(self):
        fake = Fake([("/instruments?", SPECS), ("/orders", {"orderRejectTransaction": {"rejectReason": "INSUFFICIENT_MARGIN"}})])
        p = Practice("tok", "101-1", transport=fake)
        with self.assertRaises(BrokerError):
            p.limit_bracket("XAU_USD", 3, 4000, 4010, 3995, "c", datetime(2026, 10, 27, tzinfo=timezone.utc))

    def test_account_usd_converts_gbp(self):
        fake = Fake([("/summary", {"account": {"currency": "GBP", "NAV": "100000", "marginAvailable": "90000"}}),
                     ("/pricing?instruments=GBP_USD", {"prices": [{"closeoutBid": "1.32", "closeoutAsk": "1.34"}]})])
        a = Practice("tok", "101-1", transport=fake).account_usd()
        self.assertAlmostEqual(a["equity"], 133000)
        self.assertAlmostEqual(a["margin_available"], 119700)
        self.assertEqual(a["currency"], "GBP")

    def test_account_usd_needs_no_price_for_usd(self):
        fake = Fake([("/summary", {"account": {"currency": "USD", "NAV": "5000", "marginAvailable": "5000"}})])
        self.assertEqual(Practice("tok", "101-1", transport=fake).account_usd()["equity"], 5000)

    def test_candles(self):
        c = lambda t, done: {"time": t, "complete": done, "mid": {"o": "1", "h": "2", "l": "0.5", "c": "1.5"}}
        fake = Fake([("/candles?", {"candles": [c("2026-10-26T13:00:00.000000000Z", True), c("2026-10-26T13:05:00.000000000Z", False)]})])
        out = Practice("tok", "101-1", transport=fake).candles("XAU_USD", "5Min", datetime(2026, 10, 26, tzinfo=timezone.utc),
                                                              datetime(2026, 10, 27, tzinfo=timezone.utc))
        self.assertEqual([(x.t, x.closed) for x in out], [("2026-10-26T13:00:00Z", True), ("2026-10-26T13:05:00Z", False)])


if __name__ == "__main__":
    unittest.main()
