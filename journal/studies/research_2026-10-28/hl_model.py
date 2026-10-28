import numpy as np, pandas as pd
d = pd.read_pickle("/root/.cache/tradingbot/hl_days.pkl")
d.index = pd.to_datetime(d.index)
tr, te = d[d.index < "2021-01-01"], d[d.index >= "2021-01-01"]
def X(df, cols):
    return np.column_stack([np.ones(len(df))] + [df[c].values for c in cols])
d["lr1"], d["lr5"], d["lr22"], d["lpm"] = np.log(d.r1), np.log(d.r5), np.log(d.r22), np.log(d.pm_rng.clip(1e-4))
d["agap"] = d.gap.abs(); d["gpos"] = d.gap.clip(lower=0); d["gneg"] = (-d.gap).clip(lower=0)
# where the open sits in the premarket range (0 = at the low, 1 = at the high)
d["pm_pos"] = ((d.open - d.pm_low) / (d.pm_high - d.pm_low)).clip(0, 1).fillna(0.5)
tr, te = d[d.index < "2021-01-01"], d[d.index >= "2021-01-01"]
bps = lambda x: x * 1e4
def score(name, up_hat, dn_hat, df=te):
    e_up, e_dn = np.abs(up_hat - df.up.values), np.abs(dn_hat - df.dn.values)
    print(f"{name:44s} MAE high {bps(e_up.mean()):5.1f} bps  low {bps(e_dn.mean()):5.1f} bps  (~{bps(e_up.mean())*2.95:4.0f}/{bps(e_dn.mean())*2.95:4.0f} NAS100 pts)")
score("naive: half of yesterday's range", te.r1.values / 2, te.r1.values / 2)
score("naive: half of the 22-day average range", te.r22.values / 2, te.r22.values / 2)
feats = ["lr1", "lr5", "lr22", "lpm", "agap", "gpos", "gneg", "pm_pos"]
fits = {}
for tgt in ("up", "dn"):
    y = np.log(tr[tgt].values + 5e-4)
    b, *_ = np.linalg.lstsq(X(tr, feats), y, rcond=None)
    res = y - X(tr, feats) @ b
    fits[tgt] = (b, res)
pred = {}
for tgt in ("up", "dn"):
    b, res = fits[tgt]
    # median of the log model = exp(fit); the residual's median keeps it unbiased for MAE
    pred[tgt] = np.exp(X(te, feats) @ b + np.median(res)) - 5e-4
score("model (log OLS, open features)", pred["up"], pred["dn"])
for tgt in ("up", "dn"):
    b, res = fits[tgt]
    lo, hi = np.quantile(res, [0.1, 0.9])
    lo_p, hi_p = np.exp(X(te, feats) @ b + lo) - 5e-4, np.exp(X(te, feats) @ b + hi) - 5e-4
    cov = ((te[tgt].values >= lo_p) & (te[tgt].values <= hi_p)).mean()
    print(f"  {tgt}: 80% band coverage out of sample {cov:.1%}; coef", dict(zip(["c"] + feats, np.round(b, 2))))
# range only (HAR)
yb = np.log(tr.rng.values)
b, *_ = np.linalg.lstsq(X(tr, ["lr1", "lr5", "lr22", "lpm", "agap"]), yb, rcond=None)
rh = np.exp(X(te, ["lr1", "lr5", "lr22", "lpm", "agap"]) @ b)
print(f"range model: MAE {bps(np.abs(rh - te.rng.values).mean()):.1f} bps vs naive 22d {bps(np.abs(te.r22.values - te.rng.values).mean()):.1f} bps; corr {np.corrcoef(rh, te.rng)[0,1]:.2f}")
d.to_pickle("/root/.cache/tradingbot/hl_days2.pkl")
