import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-tradingbot/efe032f3-ac09-5164-8e64-23adecf81035/scratchpad/research")
import intraday_rs as I
import numpy as np
def test(T=600, K=3, stop=None, min_ret=0.0, cost=6, label=""):
    res = []
    for d in I.dates:
        sc = []
        for s, x in I.days[d].items():
            k = int(np.searchsorted(x[:, 1], T))
            if k < 1 or k >= len(x) - 1 or x[0, 2] < 5: continue
            sc.append(((x[k - 1, 5] / x[0, 2] - 1), s, k))
        if len(sc) < 50: continue
        sc.sort()
        for r, s, k in sc[-K:]:
            if r < min_ret: continue
            x = I.days[d][s]; entry = x[k - 1, 5]; exitp = x[-1, 5]
            if stop == "daylow":
                lo = x[:k, 4].min()
                for j in range(k, len(x)):
                    if x[j, 4] <= lo: exitp = min(lo, x[j, 2]); break
            elif stop:
                st = entry * (1 - stop)
                for j in range(k, len(x)):
                    if x[j, 4] <= st: exitp = min(st, x[j, 2]); break
            res.append((d, (exitp / entry - 1) * 1e4 - cost))
    v = np.array([x[1] for x in res]); half = I.dates[len(I.dates) // 2]
    q = [I.dates[int(len(I.dates) * f)] for f in (0.25, 0.5, 0.75)]
    parts = [np.mean([x[1] for x in res if lo <= x[0] < hi]) for lo, hi in zip([0] + q, q + [99999999])]
    print(f"{label:40s} n={len(v)} net={v.mean():+6.1f}bps win={np.mean(v>0):.0%} t={v.mean()/v.std()*len(v)**.5:+5.2f} | quarters " + " ".join(f"{p:+.1f}" for p in parts))
for T in (585, 600, 615, 630):
    test(T=T, label=f"T={T//60}:{T%60:02d} K=3")
for K in (2, 5, 10):
    test(K=K, label=f"T=10:00 K={K}")
test(stop="daylow", label="T=10:00 K=3 stop at day's low")
test(stop=0.02, label="T=10:00 K=3 stop 2%")
test(cost=20, label="T=10:00 K=3 costs 10 bps a side")
test(min_ret=0.02, label="T=10:00 K=3 only if up >= 2%")
