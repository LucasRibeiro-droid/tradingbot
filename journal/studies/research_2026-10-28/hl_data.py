"""Daily table for the NAS100 high/low predictor, from QQQ 5-minute bars (SIP, with pre/post market)."""
import pickle
import numpy as np, pandas as pd
bars = pickle.load(open("/root/.cache/tradingbot/qqq_5m_2016.pkl", "rb"))
df = pd.DataFrame([(c.t, c.o, c.h, c.l, c.c) for c in bars], columns="t o h l c".split())
df["t"] = pd.to_datetime(df.t, utc=True).dt.tz_convert("America/New_York")
df["date"] = df.t.dt.date; df["m"] = df.t.dt.hour * 60 + df.t.dt.minute
rth = df[(df.m >= 570) & (df.m < 960)]; pm = df[(df.m >= 240) & (df.m < 570)]
g = rth.groupby("date")
d = pd.DataFrame({"open": g.o.first(), "high": g.h.max(), "low": g.l.min(), "close": g.c.last(), "n": g.size()})
d["t_high"] = rth.loc[g.h.idxmax(), "m"].values; d["t_low"] = rth.loc[g.l.idxmin(), "m"].values
p = pm.groupby("date"); d["pm_high"] = p.h.max(); d["pm_low"] = p.l.min()
d = d[d.n >= 70].copy()  # full sessions only
d["up"] = np.log(d.high / d.open); d["dn"] = np.log(d.open / d.low); d["rng"] = np.log(d.high / d.low)
d["prev_close"] = d.close.shift(); d["prev_high"] = d.high.shift(); d["prev_low"] = d.low.shift()
d["gap"] = np.log(d.open / d.prev_close)
for k in (1, 5, 22):
    d[f"r{k}"] = d.rng.shift().rolling(k).mean()
d["pm_rng"] = np.log(d.pm_high / d.pm_low)
d = d.dropna()
d.to_pickle("/root/.cache/tradingbot/hl_days.pkl")
print(len(d), d.index[0], d.index[-1])
print(d[["up", "dn", "rng"]].describe().round(4))
print("first-hour share: high in first hour", round((d.t_high < 630).mean(), 3), "low in first hour", round((d.t_low < 630).mean(), 3),
      "either", round(((d.t_high < 630) | (d.t_low < 630)).mean(), 3))
