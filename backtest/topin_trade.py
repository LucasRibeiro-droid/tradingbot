import sys, numpy as np, pandas as pd
C = sys.argv[1]; X = pd.read_pickle(sys.argv[2])
b = pd.read_pickle(f"{C}/b_5min.pkl"); pos = pd.Series(np.arange(len(b)), index=b.index)
h, l, c = b.h.values, b.l.values, b.c.values
hr = (b.index.hour + b.index.minute/60).values
tday = pd.factorize((b.index + pd.Timedelta(hours=6)).normalize())[0]
X["i"] = pos.reindex(X.t).values; X["d"] = tday[X.i.values]
def trade(th, rr, buf=0.25, h0=0, h1=24, exit_eod=True):
    # first bar per day & side where p >= th (and inside hours window)
    S = X[(X.p_oos >= th) & (X.hour >= h0) & (X.hour < h1)].sort_values("i").groupby(["d","side"]).head(1)
    R = []; Y = []
    for _, r in S.iterrows():
        i = int(r.i); d = r.side; e = c[i]; st = r.ext - d * buf * r.atr; rk = abs(e - st)
        if rk <= 2: continue
        tp = e + d * rr * rk; res = None
        k = i + 1
        while k < len(c) and tday[k] == tday[i]:
            if hr[k] >= 16.9 and hr[k] < 18 and exit_eod: break
            if (d == 1 and l[k] <= st) or (d == -1 and h[k] >= st): res = -1.0; break
            if (d == 1 and h[k] >= tp) or (d == -1 and l[k] <= tp): res = rr; break
            k += 1
        if res is None: res = (c[min(k, len(c)-1)] - e) * d / rk
        R.append(res - 0.87 / rk); Y.append(r.year)
    R = np.array(R); Y = np.array(Y)
    by = " ".join(f"{y}:{R[Y==y].mean():+.2f}" for y in sorted(set(Y)))
    print(f"P>={th:.2f} rr={rr} hours {h0}-{h1}: n={len(R)} win={np.mean(R>0)*100:.0f}% avgR={R.mean():+.3f} totR={R.sum():+.0f} | {by}", flush=True)
for th in [0.6, 0.7, 0.8, 0.9]:
    for rr in [1, 2]:
        trade(th, rr)
for th in [0.7, 0.8]:
    trade(th, 1, h0=9.5, h1=16)
    trade(th, 2, h0=9.5, h1=16)
