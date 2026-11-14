import sys, numpy as np, pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
E = pd.read_pickle(sys.argv[1]); E = E[E.risk_atr > 0.3].copy()
feats = [c for c in E.columns if c not in ("t","s","d","x","hit1R","hit2R","hit3R","mfe_atr","mfe_R","rev4atr","year","risk_pts")]
X = E[feats].astype(float).fillna(-1).values
tr = (E.year <= 2023).values; te = ~tr
for y in ["hit1R","hit2R","rev4atr"]:
    Y = E[y].values
    m = HistGradientBoostingClassifier(max_depth=3, max_iter=200, learning_rate=0.05, min_samples_leaf=200).fit(X[tr], Y[tr])
    p = m.predict_proba(X[te])[:,1]
    q = pd.qcut(p, 10, labels=False)
    r = pd.DataFrame({"q":q,"y":Y[te]}).groupby("q").y.agg(["size","mean"]).round(3)
    print(f"\n{y}: train base {Y[tr].mean():.3f}  test base {Y[te].mean():.3f}  test by score decile (0=lowest,9=highest):")
    print(r.T.to_string())
