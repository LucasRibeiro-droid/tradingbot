"""The learning engine's fills and exits on a hand-made bid/ask path."""
import unittest
from datetime import datetime, timezone

import numpy as np

from tradingbot.learn.market import Market
from tradingbot.learn.setups import Signal
from tradingbot.learn.sim import COSTS, simulate


def market(mids, spread=1.0):
    """1-minute candles from (open, high, low, close) mids, starting Tuesday 2021-03-02 18:00 New York."""
    t0 = datetime(2021, 3, 2, 23, 0, tzinfo=timezone.utc).timestamp()
    rows = []
    for k, (o, h, l, c) in enumerate(mids):
        rows.append([t0 + 60 * k, o - spread / 2, h - spread / 2, l - spread / 2, c - spread / 2,
                     o + spread / 2, h + spread / 2, l + spread / 2, c + spread / 2])
    return Market("NAS100_USD", np.array(rows, dtype=float))


class Fills(unittest.TestCase):
    def sig(self, kind="market", entry=100.0, stop=90.0, side=1, expiry=5, targets=None):
        return Signal("NAS100_USD", "t", "t|x", side, 0, kind, entry, stop, expiry, {}, "", targets)

    def test_market_long_hits_target_on_the_bid(self):
        m = market([(100, 100, 100, 100), (100, 101, 99, 100), (100, 125, 100, 124), (124, 124, 124, 124)])
        tr = simulate(m, self.sig(), "1R")
        c = COSTS["NAS100_USD"]
        fill = 100 + 0.5 + c["slip"]
        self.assertAlmostEqual(tr.fill, fill)
        self.assertEqual(tr.exits[0][2], "target 1R")
        self.assertAlmostEqual(tr.r, (fill - 90 - 2 * c["comm"]) / (fill - 90) * 1.0 if False else ((fill + (fill - 90)) - fill - 2 * c["comm"]) / (fill - 90))

    def test_same_candle_stop_and_target_counts_as_the_stop(self):
        m = market([(100, 100, 100, 100), (100, 101, 99, 100), (100, 130, 80, 100), (100, 100, 100, 100)])
        tr = simulate(m, self.sig(), "1R")
        self.assertEqual(tr.exits[0][2], "stop")
        self.assertLess(tr.r, -1.0)  # the stop plus slippage and commission

    def test_limit_not_reached_is_no_trade(self):
        m = market([(100, 100, 100, 100)] + [(100, 101, 99, 100)] * 5)
        self.assertFalse(simulate(m, self.sig(kind="limit", entry=95.0, stop=90.0), "1R").filled)

    def test_break_even_after_the_first_target(self):
        m = market([(100, 100, 100, 100), (100, 101, 99, 100), (100, 115, 100, 114), (114, 114, 98, 99), (99, 99, 99, 99)])
        tr = simulate(m, self.sig(), "half1R_be3R")
        kinds = [e[2] for e in tr.exits]
        self.assertEqual(kinds, ["target 1R", "break even"])

    def test_stop_inside_the_spread_is_no_trade(self):
        m = market([(100, 100, 100, 100), (100, 101, 99, 100), (100, 101, 99, 100)])
        self.assertFalse(simulate(m, self.sig(stop=100.5), "1R").filled)

    def test_day_end_exit(self):
        m = market([(100, 100, 100, 100)] + [(100, 101, 99, 100)] * 4)
        tr = simulate(m, self.sig(), "3R")
        self.assertEqual({e[2] for e in tr.exits}, {"day end"})


if __name__ == "__main__":
    unittest.main()
