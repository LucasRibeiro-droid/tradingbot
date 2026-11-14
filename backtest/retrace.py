import sys, numpy as np, pandas as pd
from numba import njit
C = sys.argv[1]; E = pd.read_pickle(sys.argv[2]); E = E[E.risk_atr > 0.3]
b = pd.read_pickle(f"{C}/b_5min.pkl"); h, l, c = b.h.values, b.l.values, b.c.values

@njit(cache=True)
def sim(h, l, c, s_arr, d_arr, x_arr, frac, rr, wait, cost):
    m = len(s_arr); R = np.full(m, np.nan)
    for j in range(m):
        s = s_arr[j]; d = d_arr[j]; x = x_arr[j]
        ext = h[x] if d == -1 else l[x]
        st = ext + (0.25 if d == -1 else -0.25)
        e = c[s] + (ext - c[s]) * frac              # frac 0 = at CHoCH close, 0.5 = equilibrium
        rk = abs(e - st)
        if rk < 2: continue
        tp = e - d * rr * rk if False else e + (-1 if d == -1 else 1) * rr * rk
        f = -1
        for k in range(s + 1, min(s + 1 + wait, len(c))):
            if (d == -1 and l[k] <= tp) or (d == 1 and h[k] >= tp): break      # ran away, no fill
            if (d == -1 and h[k] >= e) or (d == 1 and l[k] <= e):
                f = k; break
        if frac == 0: f = s
        if f < 0: continue
        res = np.nan
        for k in range(f + (0 if frac > 0 else 1), min(f + 300, len(c))):
            if (d == -1 and h[k] >= st) or (d == 1 and l[k] <= st): res = -1.0; break
            if k > f or frac == 0:
                if (d == -1 and l[k] <= tp) or (d == 1 and h[k] >= tp): res = rr; break
        if np.isnan(res): res = ((c[min(f + 299, len(c)-1)] - e) * d) / rk
        R[j] = res - cost / rk
    return R
s, d, x = E.s.values, E.d.values.astype(np.int64), E.x.values
print("frac  rr   n      win%   avgR(net)  totR    by-year avgR")
for frac in [0.0, 0.5, 0.618, 0.705, 0.79]:
    for rr in [1, 2, 3]:
        R = sim(h, l, c, s, d, x, frac, rr, 24, 0.87)
        ok = ~np.isnan(R); yr = E.year.values[ok]; r = R[ok]
        by = " ".join(f"{y}:{r[yr==y].mean():+.3f}" for y in sorted(set(yr)))
        print(f"{frac:5.3f} {rr}  {ok.sum():6d}  {np.mean(r>0)*100:5.1f}   {r.mean():+.3f}   {r.sum():+8.1f}   {by}")
