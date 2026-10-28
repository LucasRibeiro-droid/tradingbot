"""Intraday update: at checkpoint T, given the high/low so far, predict the day's final high and low."""
import pickle
import numpy as np, pandas as pd
d = pd.read_pickle("/root/.cache/tradingbot/hl_days2.pkl"); d.index = pd.to_datetime(d.index)
bars = pickle.load(open("/root/.cache/tradingbot/qqq_5m_2016.pkl", "rb"))
df = pd.DataFrame([(c.t, c.h, c.l, c.c) for c in bars], columns="t h l c".split())
df["t"] = pd.to_datetime(df.t, utc=True).dt.tz_convert("America/New_York")
df["date"] = pd.to_datetime(df.t.dt.date); df["m"] = df.t.dt.hour * 60 + df.t.dt.minute
rth = df[(df.m >= 570) & (df.m < 960) & df.date.isin(d.index)]
# open-time range forecast (from hl_model's HAR fit on 2016-2020)
tr = d[d.index < "2021-01-01"]
F = ["lr1", "lr5", "lr22", "lpm", "agap"]
Xf = lambda x: np.column_stack([np.ones(len(x))] + [x[c].values for c in F])
b, *_ = np.linalg.lstsq(Xf(tr), np.log(tr.rng.values), rcond=None)
d["rng_hat"] = np.exp(Xf(d) @ b)
rows = []
for T in (600, 630, 660, 720, 780, 840, 900):  # 10:00 ... 15:00
    s = rth[rth.m < T].groupby("date").agg(h=("h", "max"), l=("l", "min"), c=("c", "last"))
    s = s.join(d[["open", "high", "low", "rng_hat"]], how="inner")
    s["T"] = T
    rows.append(s)
x = pd.concat(rows)
x["so_far"] = np.log(x.h / x.l) / x.rng_hat           # range used so far, vs the open forecast
x["pos"] = ((x.c - x.l) / (x.h - x.l)).clip(0, 1).fillna(0.5)  # where price sits in today's range
x["left"] = (960 - x["T"]) / 390                     # share of the session left
x["ext_up"] = np.log(x.high / x.h); x["ext_dn"] = np.log(x.l / x.low)
x["high_in"] = (x.ext_up < 1e-6).astype(float); x["low_in"] = (x.ext_dn < 1e-6).astype(float)
x.to_pickle("/root/.cache/tradingbot/hl_intraday.pkl")
trn, tst = x[x.index < "2021-01-01"], x[x.index >= "2021-01-01"]
feats = lambda z: np.column_stack([np.ones(len(z)), z.so_far, z.pos, z.left, z.so_far * z.left, z.pos * z.left, np.log(z.rng_hat)])
out = []
for side, pos_sign in (("up", 1), ("dn", -1)):
    y = trn[f"ext_{side}"].values
    # two parts: P(no further extreme) via a linear probability fit, and the size given an extension
    bb, *_ = np.linalg.lstsq(feats(trn), y, rcond=None)
    pred = np.clip(feats(tst) @ bb, 0, None)
    for T in sorted(tst["T"].unique()):
        m = (tst["T"] == T).values
        e_model = np.abs(pred[m] - tst[f"ext_{side}"].values[m]).mean() * 1e4
        e_naive = np.abs(tst[f"ext_{side}"].values[m]).mean() * 1e4  # "the extreme so far is final"
        p_in = tst["high_in" if side == "up" else "low_in"].values[m].mean()
        out.append((side, T, e_naive, e_model, p_in))
r = pd.DataFrame(out, columns="side T naive model already_in".split())
r["T"] = r["T"].map(lambda v: f"{v // 60}:{v % 60:02d}")
print(r.round(2).to_string(index=False))
