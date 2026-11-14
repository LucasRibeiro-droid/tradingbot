import sys, numpy as np, pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
D = pd.read_pickle(sys.argv[1])
# symmetric: build a "high" dataset and a mirrored "low" dataset and stack them
H = pd.DataFrame(dict(y=D.hiIn, hour=D.hour, used=D.rng_used, pb=D.pb_hi, ext=D.hi_vs_open, took=D.took_pdH,
                      since=D.barsSinceH, s5=(D.bs5==-1).astype(int), s1h=(D.st1h==-1).astype(int), b1h=(D.bs1h==-1).astype(int), year=D.year))
L = pd.DataFrame(dict(y=D.loIn, hour=D.hour, used=D.rng_used, pb=D.pb_lo, ext=D.lo_vs_open, took=D.took_pdL,
                      since=D.barsSinceL, s5=(D.bs5==1).astype(int), s1h=(D.st1h==1).astype(int), b1h=(D.bs1h==1).astype(int), year=D.year))
X = pd.concat([H, L], ignore_index=True)
feats = ["hour","used","pb","ext","took","since","s5","s1h","b1h"]
tr = X.year <= 2023; te = ~tr
gb = HistGradientBoostingClassifier(max_depth=4, max_iter=300, learning_rate=0.05, min_samples_leaf=500).fit(X.loc[tr, feats], X.y[tr])
p = gb.predict_proba(X.loc[te, feats])[:, 1]
print("test base", X.y[te].mean().round(3))
cal = pd.DataFrame(dict(p=p, y=X.y[te].values)); cal["bin"] = pd.cut(cal.p, [0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1])
print(cal.groupby("bin", observed=True).agg(n=("y","size"), predicted=("p","mean"), actual=("y","mean")).round(3).to_string())
from sklearn.metrics import roc_auc_score
print("GBM AUC test", round(roc_auc_score(X.y[te], p), 3))
# simple baselines: hour only, used+pb only
for fs in [["hour"], ["used","pb"], ["hour","used","pb"], ["hour","used","pb","since"]]:
    g2 = HistGradientBoostingClassifier(max_depth=3, max_iter=200, min_samples_leaf=500).fit(X.loc[tr, fs], X.y[tr])
    print(fs, "AUC", round(roc_auc_score(X.y[te], g2.predict_proba(X.loc[te, fs])[:, 1]), 3))
