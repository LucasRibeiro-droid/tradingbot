import unittest

from tradingbot.live import hl_predict as H


class Predictor(unittest.TestCase):
    def setUp(self):
        self.m = H.load()
        hist = [{"high": 101.5, "low": 100.0, "close": 100.8}] * 22
        self.f = H.open_features(hist, {"open": 101.0, "pm_h": 101.3, "pm_l": 100.6})

    def test_bands_are_ordered_around_the_open(self):
        o = H.at_open(self.m, self.f, 101.0)
        self.assertTrue(101.0 <= o["high_p10"] <= o["high_p50"] <= o["high_p90"])
        self.assertTrue(o["low_p90"] <= o["low_p50"] <= o["low_p10"] <= 101.0)

    def test_late_day_at_the_low_means_the_high_is_likely_in(self):
        rh = H.at_open(self.m, self.f, 101.0)["range_pct"] / 100
        p = H.p_extreme_in(self.m, 900, high=102.0, low=100.5, last=100.6, range_hat=rh, gap=self.f["gap"])
        self.assertGreater(p["high"], 0.8)
        self.assertLess(p["low"], p["high"])


if __name__ == "__main__":
    unittest.main()
