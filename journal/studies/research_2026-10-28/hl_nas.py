"""Transfer check: models fit on QQQ 2016-2020, applied to OANDA NAS100 (Oct 2025 - Oct 2026)."""
import json, glob, pickle, subprocess, sys
import numpy as np, pandas as pd
from pathlib import Path
f = sorted(Path("/root/.cache/tradingbot").glob("oanda_NAS100_USD_5m_*.json"))[-1]
raw = json.loads(f.read_text())
df = pd.DataFrame([(r[0], r[1], r[2], r[3], r[4]) for r in raw], columns="t o h l c".split())
df["t"] = pd.to_datetime(df.t, utc=True).dt.tz_convert("America/New_York")
df["date"] = pd.to_datetime(df.t.dt.date); df["m"] = df.t.dt.hour * 60 + df.t.dt.minute
rth = df[(df.m >= 570) & (df.m < 960)]; pm = df[(df.m >= 240) & (df.m < 570)]
g = rth.groupby("date")
d = pd.DataFrame({"open": g.o.first(), "high": g.h.max(), "low": g.l.min(), "close": g.c.last(), "n": g.size()})
p = pm.groupby("date"); d["pm_high"] = p.h.max(); d["pm_low"] = p.l.min()
d = d[d.n >= 75].copy()
d["up"] = np.log(d.high / d.open); d["dn"] = np.log(d.open / d.low); d["rng"] = np.log(d.high / d.low)
d["gap"] = np.log(d.open / d.close.shift())
for k in (1, 5, 22): d[f"r{k}"] = d.rng.shift().rolling(k).mean()
d["pm_rng"] = np.log(d.pm_high / d.pm_low); d = d.dropna()
for c, s in (("lr1", "r1"), ("lr5", "r5"), ("lr22", "r22"), ("lpm", "pm_rng")): d[c] = np.log(d[s].clip(1e-4))
d["agap"] = d.gap.abs()
q = pd.read_pickle("/root/.cache/tradingbot/hl_days2.pkl"); q.index = pd.to_datetime(q.index); qt = q[q.index < "2021-01-01"]
F = ["lr1", "lr5", "lr22", "lpm", "agap"]; X = lambda z: np.column_stack([np.ones(len(z))] + [z[c].values for c in F])
b, *_ = np.linalg.lstsq(X(qt), np.log(qt.rng.values), rcond=None)
rh = np.exp(X(d) @ b)
print(f"NAS100 days {len(d)}; range forecast MAE {np.abs(rh - d.rng).mean()*1e4:.1f} bps vs naive 22d {np.abs(d.r22 - d.rng).mean()*1e4:.1f}; corr {np.corrcoef(rh, d.rng)[0,1]:.2f}")
d["rng_hat"] = rh
rows = []
for T in (600, 630, 660, 720, 780, 840, 900):
    s = rth[rth.m < T].groupby("date").agg(h=("h", "max"), l=("l", "min"), c=("c", "last")).join(d[["high", "low", "rng_hat", "gap"]], how="inner")
    s["T"] = T; rows.append(s)
x = pd.concat(rows)
x["so_far"] = np.log(x.h / x.l) / x.rng_hat; x["pos"] = ((x.c - x.l) / (x.h - x.l)).clip(0, 1).fillna(.5); x["left"] = (960 - x["T"]) / 390
x["high_in"] = (np.log(x.high / x.h) < 1e-6).astype(float); x["low_in"] = (np.log(x.l / x.low) < 1e-6).astype(float)
sys.argv = ["x"]; exec(open("/tmp/claude-0/-home-user-tradingbot/efe032f3-ac09-5164-8e64-23adecf81035/scratchpad/research/hl_prob_lib.py").read())
qi = pd.read_pickle("/root/.cache/tradingbot/hl_intraday.pkl").join(q[["gap"]]); qi = qi[qi.index < "2021-01-01"]
for side, tgt in (("up", "high_in"), ("dn", "low_in")):
    w = fit(Ff(qi, side), qi[tgt].values); pr = 1 / (1 + np.exp(-Ff(x, side) @ w)); y = x[tgt].values
    print("HIGH" if side == "up" else "LOW", "already in (NAS100, model from QQQ 2016-20):",
          " ".join(f"{T//60}:{T%60:02d} AUC {auc(pr[(x['T']==T).values], y[(x['T']==T).values]):.2f}/P>=80% right {y[(x['T']==T).values & (pr>=.8)].mean():.0%}" for T in (630, 720, 840)))
