"""P(the day's high / low is already in) at each checkpoint: logistic regression (numpy IRLS),
trained 2016-2020, tested 2021-2026. Compared with the base rate at that time of day."""
import numpy as np, pandas as pd
x = pd.read_pickle("/root/.cache/tradingbot/hl_intraday.pkl")
d = pd.read_pickle("/root/.cache/tradingbot/hl_days2.pkl"); d.index = pd.to_datetime(d.index)
x = x.join(d[["gap"]])
def F(z, side):
    pos = z.pos if side == "up" else 1 - z.pos       # distance-to-extreme framing: 1 = sitting at the extreme
    dist = np.log(z.h / z.c) if side == "up" else np.log(z.c / z.l)  # how far price is from that extreme
    g = z.gap if side == "up" else -z.gap
    return np.column_stack([np.ones(len(z)), z.left, z.so_far, pos, dist / z.rng_hat, g * 100, z.so_far * z.left, pos * z.left])
def fit(X, y, it=50):
    w = np.zeros(X.shape[1])
    for _ in range(it):
        p = 1 / (1 + np.exp(-X @ w)); W = p * (1 - p) + 1e-9
        w += np.linalg.solve((X.T * W) @ X + 1e-6 * np.eye(len(w)), X.T @ (y - p))
    return w
def auc(p, y):
    o = np.argsort(p); r = np.empty(len(p)); r[o] = np.arange(1, len(p) + 1)
    n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
trn, tst = x[x.index < "2021-01-01"], x[x.index >= "2021-01-01"]
for side, tgt in (("up", "high_in"), ("dn", "low_in")):
    w = fit(F(trn, side), trn[tgt].values)
    p = 1 / (1 + np.exp(-F(tst, side) @ w)); y = tst[tgt].values
    print(f"{'HIGH' if side == 'up' else 'LOW'} already in — out of sample 2021-2026")
    for T in sorted(tst["T"].unique()):
        m = (tst["T"] == T).values
        base = trn[trn["T"] == T][tgt].mean()
        brier_m = ((p[m] - y[m]) ** 2).mean(); brier_b = ((base - y[m]) ** 2).mean()
        hi = m & (p >= 0.8); lo = m & (p <= 0.2)
        print(f"  {T//60}:{T%60:02d} base {y[m].mean():.0%} AUC {auc(p[m], y[m]):.2f} Brier {brier_m:.3f} vs {brier_b:.3f} | "
              f"when P>=80%: right {y[hi].mean() if hi.any() else float('nan'):.0%} on {hi.sum() / m.sum():.0%} of days | "
              f"when P<=20%: still to come {1 - y[lo].mean() if lo.any() else float('nan'):.0%} on {lo.sum() / m.sum():.0%} of days")
