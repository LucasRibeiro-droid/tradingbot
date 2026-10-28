"""Intraday cross-section, 150 liquid stocks, 2024-11 -> 2026-10 (5-minute SIP): at time T, rank stocks by return
since the open; long the K strongest (momentum) or the K weakest (reversal); hold to the close. 3 bps a side.
Also with a stop at the day's extreme so far."""
import pickle, sys
from collections import defaultdict
import numpy as np
S = pickle.load(open("/root/.cache/tradingbot/orb/bars5_150.pkl", "rb"))
days = defaultdict(dict)
for s, a in S.items():
    for d in np.unique(a[:, 0]):
        x = a[a[:, 0] == d]
        if len(x) >= 75 and x[0, 1] == 570: days[int(d)][s] = x
dates = sorted(days)
def test(T, K, mode, side):
    res = []
    for d in dates:
        sc = []
        for s, x in days[d].items():
            k = int(np.searchsorted(x[:, 1], T))
            if k < 1 or k >= len(x) - 1 or x[0, 2] < 5: continue
            sc.append(((x[k - 1, 5] / x[0, 2] - 1), s, k))
        if len(sc) < 50: continue
        sc.sort()
        pick = sc[-K:] if mode == "strong" else sc[:K]
        for r, s, k in pick:
            x = days[d][s]; entry = x[k - 1, 5]; exitp = x[-1, 5]
            res.append((d, side * (exitp / entry - 1) * 1e4 - 6))
    v = np.array([x[1] for x in res]); half = dates[len(dates) // 2]
    a = [x[1] for x in res if x[0] < half]; b = [x[1] for x in res if x[0] >= half]
    print(f"T={T//60}:{T%60:02d} {mode:6s} {'long ' if side == 1 else 'short'} K={K}: n={len(v)} net={v.mean():+6.1f}bps win={np.mean(v>0):.0%} t={v.mean()/v.std()*len(v)**.5:+5.2f} | h1 {np.mean(a):+6.1f} h2 {np.mean(b):+6.1f}")
for T in (600, 630, 720, 840):
    for mode, side in (("strong", 1), ("weak", 1), ("strong", -1), ("weak", -1)):
        test(T, 3, mode, side)
