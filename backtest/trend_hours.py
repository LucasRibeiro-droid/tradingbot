import sys, numpy as np, pandas as pd
b = pd.read_pickle(sys.argv[1] + "/b_5min.pkl")
b.index = b.index.tz_convert("Europe/London")
b = b[b.index.dayofweek < 5]
b["hk"] = b.index.floor("h")
g = b.groupby("hk")
H = pd.DataFrame(dict(o=g.o.first(), c=g.c.last(), h=g.h.max(), l=g.l.min(), n=g.o.size(),
                      path=g.apply(lambda x: (x.c - x.o).abs().sum() + (x.o - x.c.shift()).abs().fillna(0).sum())))
H = H[H.n >= 11]
H["net"] = (H.c - H.o).abs()
H["eff"] = H.net / H.path                      # efficiency: 1 = straight line, 0 = all chop
H["dirpct"] = H.net / (H.h - H.l)              # how much of the hour's range ended as net move
H["rng"] = H.h - H.l
H["hour"] = H.index.hour
# trend-day continuation: does the hour move in the same direction as the previous hour?
H["sgn"] = np.sign(H.c - H.o)
H["cont"] = (H.sgn == H.sgn.shift()).astype(float)
H["year"] = H.index.year
t = H.groupby("hour").agg(hours=("eff","size"), efficiency=("eff","mean"), net_vs_range=("dirpct","mean"),
                          range_pts=("rng","median"), net_pts=("net","median"), trend_hours_pct=("eff", lambda s: (s > 0.35).mean()*100))
print(t.round(3).to_string())
print("\nefficiency by year (stability):")
print(H.pivot_table(index="hour", columns="year", values="eff", aggfunc="mean").round(2).to_string())
