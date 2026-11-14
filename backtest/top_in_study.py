"""Is the day's HIGH (or LOW) already in?  For every 5m bar, label whether the running day high is the
final high of the trading day (18:00 -> 17:00 New York), and study what predicts it.
Usage: python3 -I top_in_study.py <cache_dir> <out.pkl>
"""
import sys, numpy as np, pandas as pd
sys.path.insert(0, "/home/user/tradingbot/backtest")
from engine import atr, body_structure, supertrend, htf_on_5m

C, OUT = sys.argv[1], sys.argv[2]
b = pd.read_pickle(f"{C}/b_5min.pkl"); b1h = pd.read_pickle(f"{C}/b_1h.pkl")
idx = b.index
hr = (idx.hour + idx.minute / 60).values
tday = pd.factorize((idx + pd.Timedelta(hours=6)).normalize())[0]
df = b.copy(); df["d"] = tday
g = df.groupby("d")
df["runH"] = g.h.cummax(); df["runL"] = g.l.cummin()
df["finH"] = g.h.transform("max"); df["finL"] = g.l.transform("min")
df["dopen"] = g.o.transform("first")
df["n_in_day"] = g.cumcount()
day = g.agg(H=("h", "max"), L=("l", "min"), N=("h", "size"))
day["adr"] = (day.H - day.L).rolling(20).median().shift(1)
df["adr"] = day.adr.reindex(tday).values
df["pdH"] = day.H.shift(1).reindex(tday).values
df["pdL"] = day.L.shift(1).reindex(tday).values
df["full"] = day.N.reindex(tday).values >= 250                    # skip holiday half-days
# bars since the running high / low was set
isNewH = df.h >= df.runH; isNewL = df.l <= df.runL
grpH = isNewH.groupby(tday).cumsum(); grpL = isNewL.groupby(tday).cumsum()
df["barsSinceH"] = df.groupby([tday, grpH]).cumcount()
df["barsSinceL"] = df.groupby([tday, grpL]).cumcount()
A = atr(b); df["atr"] = A
df["bs5"] = body_structure(b, 2)
df["st1h"] = htf_on_5m(b, b1h, supertrend(b1h))
df["bs1h"] = htf_on_5m(b, b1h, body_structure(b1h, 2))

# labels (high is in = no higher high later today)
df["hiIn"] = (df.runH >= df.finH - 1e-9).astype(np.int8)
df["loIn"] = (df.runL <= df.finL + 1e-9).astype(np.int8)
adr = df.adr
df["hour"] = hr
df["rng_used"] = (df.runH - df.runL) / adr
df["pb_hi"] = (df.runH - df.c) / adr            # how far below the high price is now (ADR units)
df["pb_lo"] = (df.c - df.runL) / adr
df["hi_vs_open"] = (df.runH - df.dopen) / adr
df["lo_vs_open"] = (df.dopen - df.runL) / adr
df["took_pdH"] = (df.runH > df.pdH).astype(np.int8)
df["took_pdL"] = (df.runL < df.pdL).astype(np.int8)
df["year"] = idx.year
df = df[df.full & adr.notna()]
df.to_pickle(OUT)
print(len(df), "bars;  P(high already in) overall:", round(df.hiIn.mean(), 3))
