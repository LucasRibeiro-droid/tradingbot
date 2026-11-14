import sys, numpy as np, pandas as pd
exec(open("/home/user/tradingbot/backtest/retrace.py").read().split("s, d, x = E.s")[0].replace("cache=True", "cache=False"))
X = pd.read_pickle(sys.argv[3]); P = X.pivot_table(index="t", columns="side", values="p_oos")
E = E.copy(); E["p_hi"] = P[-1].reindex(E.t).values; E["p_lo"] = P[1].reindex(E.t).values
E["p_ext"] = np.where(E.d == -1, E.p_hi, E.p_lo)          # CHoCH down: P(today's high is in)
s, d, x = E.s.values, E.d.values.astype(np.int64), E.x.values
for rr in [1, 2, 3]:
    R = sim(h, l, c, s, d, x, 0.0, rr, 24, 0.87); E[f"R{rr}"] = R
q = pd.cut(E.p_ext, [0, .2, .4, .6, .8, .9, .95, 1])
print(E.groupby(q, observed=True)[["R1","R2","R3"]].agg(["size","mean"]).round(3).to_string())
E["ext_is_dayext"] = E.ext_is_dayext.astype(bool)
print("\nextreme = day's high/low:"); print(E.groupby(["ext_is_dayext", q], observed=True)[["R2"]].agg(["size","mean"]).round(3).to_string())
print()
for th in [0.8, 0.9]:
    S_ = E[E.p_ext >= th]
    for rr in [1, 2, 3]:
        g = S_.groupby("year")[f"R{rr}"].mean().round(3).to_dict()
        r = S_[f"R{rr}"]; w = (r > 0).mean()
        eq = r.cumsum().values; dd = (np.maximum.accumulate(eq) - eq).max()
        print(f"p>={th} rr={rr} n={len(S_)} ({len(S_)/5.3:.0f}/yr) win={w:.2f} avgR={r.mean():+.3f} totR={r.sum():+.0f} maxDD={dd:.0f}R  {g}")
    print(" hours:", S_.groupby(pd.cut(S_.hour, [0, 9.5, 12, 16, 18, 24], right=False), observed=True).R2.agg(["size", "mean"]).round(3).to_dict())
    print(" risk_atr:", S_.groupby(pd.qcut(S_.risk_atr, 4), observed=True).R2.agg(["size", "mean"]).round(3).to_dict())
