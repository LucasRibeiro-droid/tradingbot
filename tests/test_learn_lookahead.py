"""No-lookahead proof for the learning engine (owner's integrity rule).

1. Truncation: every decision the engine makes on the full history at time T (a signal known at T) must
   be made identically from the data that ends at T. Checked at random cut points on both instruments.
2. Poisoned future: replacing every candle after T with wild prices must not change any decision at or
   before T.
3. The holdout (2025-01-01 onwards) cannot be loaded by development code.
Needs the cached OANDA history (python -m tradingbot.learn.data); skipped without it.
"""
import random
import unittest
from datetime import datetime, timezone

import numpy as np

from tradingbot.learn import data

HAVE = (data.CACHE / "NAS100_USD_M1_202103.npy").exists() and (data.CACHE / "XAU_USD_M1_202103.npy").exists()


def decisions(raw, inst, upto_t=None):
    from tradingbot.learn.market import Market
    from tradingbot.learn.setups import all_signals
    m = Market(inst, raw)
    out = set()
    for s in all_signals(m):
        t = int(m.t[s.known])
        if upto_t is None or t <= upto_t:
            out.add((t, s.base, s.side, round(s.entry, 5), round(s.stop, 5), s.kind))
    return out


@unittest.skipUnless(HAVE, "OANDA history not cached")
class NoLookahead(unittest.TestCase):
    def _raw(self, inst):
        raw = data.load(inst, datetime(2021, 2, 28, tzinfo=timezone.utc), datetime(2021, 4, 1, tzinfo=timezone.utc))
        return raw

    def test_truncated_history_gives_the_same_decisions(self):
        rnd = random.Random(7)
        for inst in data.INSTRUMENTS:
            raw = self._raw(inst)
            full = None
            for _ in range(3):
                cut = rnd.randrange(len(raw) // 3, len(raw) - 10)
                t_cut = int(raw[cut, 0])
                if full is None:
                    full = decisions(raw, inst)
                part = raw[:cut + 1].copy()
                expected = {d for d in full if d[0] <= t_cut}
                got = decisions(part, inst, t_cut)
                missing = expected - got
                self.assertFalse(missing, f"{inst}: {len(missing)} decisions at or before the cut needed later data, e.g. {sorted(missing)[:2]}")

    def test_poisoned_future_changes_nothing_before_it(self):
        inst = "XAU_USD"
        raw = self._raw(inst)
        cut = len(raw) // 2
        t_cut = int(raw[cut, 0])
        poisoned = raw.copy()
        rng = np.random.default_rng(1)
        noise = rng.normal(0, 50, size=(len(raw) - cut - 1, 1))
        poisoned[cut + 1:, 1:] = raw[cut + 1:, 1:] + noise          # every later candle shifted at random
        poisoned[cut + 1:, [2, 6]] = poisoned[cut + 1:, [1, 4, 5, 8]].max(axis=1, keepdims=True).repeat(2, 1)
        poisoned[cut + 1:, [3, 7]] = poisoned[cut + 1:, [1, 4, 5, 8]].min(axis=1, keepdims=True).repeat(2, 1)
        a, b = decisions(raw, inst, t_cut), decisions(poisoned, inst, t_cut)
        self.assertEqual(a - b, set(), "a decision before the cut changed when only the future changed")

    def test_holdout_is_locked(self):
        with self.assertRaises(data.HoldoutLocked):
            data.load("NAS100_USD", datetime(2099, 12, 1, tzinfo=timezone.utc), datetime(2100, 2, 1, tzinfo=timezone.utc))
        with self.assertRaises(data.HoldoutLocked):
            data.fetch_month(None, "XAU_USD", 2100, 3)


if __name__ == "__main__":
    unittest.main()
