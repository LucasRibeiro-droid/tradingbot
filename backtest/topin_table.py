import sys, numpy as np, pandas as pd
from sklearn.metrics import roc_auc_score
D = pd.read_pickle(sys.argv[1])
UB = [0,.25,.4,.55,.7,.85,1.0,1.2,1.5,99]; PB = [0,.03,.07,.12,.2,.3,.45,.6,99]
def stack(D):
    H = pd.DataFrame(dict(y=D.hiIn, hour=D.hour, used=D.rng_used, pb=D.pb_hi, year=D.year, t=D.index, side=-1, c=D.c, ext=D.runH, atr=D.atr))
    L = pd.DataFrame(dict(y=D.loIn, hour=D.hour, used=D.rng_used, pb=D.pb_lo, year=D.year, t=D.index, side=1, c=D.c, ext=D.runL, atr=D.atr))
    X = pd.concat([H, L], ignore_index=True)
    X["hb"] = ((X.hour.astype(int) - 18) % 24)                 # 0 = 18:00 NY (session open)
    X["ub"] = np.digitize(X.used, UB[1:-1]); X["pbb"] = np.digitize(X.pb.clip(lower=0), PB[1:-1])
    return X
def fit(X, m=40):
    p0 = X.y.mean()
    g1 = X.groupby(["hb","ub"]).y.agg(["sum","size"])
    p1 = (g1["sum"] + m * p0) / (g1["size"] + m)
    g2 = X.groupby(["hb","ub","pbb"]).y.agg(["sum","size"])
    par = p1.reindex(g2.index.droplevel(2)).values
    p2 = (g2["sum"] + m * par) / (g2["size"] + m)
    full = pd.MultiIndex.from_product([range(24), range(len(UB)-1), range(len(PB)-1)], names=["hb","ub","pbb"])
    t = p2.reindex(full)
    fill = p1.reindex(full.droplevel(2)).values
    t = t.fillna(pd.Series(fill, index=full)).fillna(p0)
    return t
X = stack(D)
tr = X.year <= 2023
T = fit(X[tr])
pte = T.reindex(pd.MultiIndex.from_arrays([X.hb[~tr], X.ub[~tr], X.pbb[~tr]])).values
print("lookup-table AUC on 2024-26 (fit on 2021-23):", round(roc_auc_score(X.y[~tr], pte), 3))
cal = pd.DataFrame(dict(p=pte, y=X.y[~tr].values)); cal["bin"] = pd.cut(cal.p, [0,.2,.4,.6,.7,.8,.9,1])
print(cal.groupby("bin", observed=True).agg(n=("y","size"), predicted=("p","mean"), actual=("y","mean")).round(3).to_string())
X["p_oos"] = np.nan; X.loc[~tr, "p_oos"] = pte
# in-sample half for 2021-23 using the reverse fit (2024-26 table) so every row has an out-of-sample prob
T2 = fit(X[~tr]); X.loc[tr, "p_oos"] = T2.reindex(pd.MultiIndex.from_arrays([X.hb[tr], X.ub[tr], X.pbb[tr]])).values
X.to_pickle(sys.argv[2])
Tall = fit(X); Tall.to_pickle(sys.argv[3])
print(Tall.unstack("pbb").loc[[15, 16, 17, 19, 21]].round(2).to_string())   # 09:00, 10:00, 11:00, 13:00, 15:00 NY
