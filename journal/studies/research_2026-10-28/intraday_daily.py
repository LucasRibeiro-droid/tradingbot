"""Day trades (open -> close) chosen from yesterday's daily data: 78 large caps, 2016-2026. 3 bps a side.
Baseline: every stock every day open -> close. Top-K per day by signal strength (2-5 trades a day)."""
import pickle, sys
from collections import defaultdict
import numpy as np
sys.path.insert(0, "/home/user/tradingbot")
data = pickle.load(open("/root/.cache/tradingbot/daily_2016/stocks.pkl", "rb"))
COST = 3.0
rows = []  # (date, sym, features..., oc_ret_bps, gap)
for s, b in data.items():
    o = np.array([x.o for x in b]); h = np.array([x.h for x in b]); l = np.array([x.l for x in b]); c = np.array([x.c for x in b])
    for i in range(201, len(b)):
        sma = c[i - 200:i].mean()
        r1 = c[i - 1] / c[i - 2] - 1
        ibs = (c[i - 1] - l[i - 1]) / (h[i - 1] - l[i - 1]) if h[i - 1] > l[i - 1] else 0.5
        d3 = c[i - 1] < c[i - 2] < c[i - 3] < c[i - 4]
        u3 = c[i - 1] > c[i - 2] > c[i - 3] > c[i - 4]
        gap = o[i] / c[i - 1] - 1
        rows.append((b[i].t[:10], s, c[i - 1] > sma, r1, ibs, d3, u3, gap, (c[i] / o[i] - 1) * 1e4))
dates = sorted({r[0] for r in rows})
by = defaultdict(list)
for r in rows: by[r[0]].append(r)
def test(name, pick, K=5, side=1):
    res = []
    for d in dates:
        c = [r for r in by[d] if pick(r) is not None]
        c.sort(key=lambda r: pick(r))
        for r in c[:K]:
            res.append((d, side * r[8] - 2 * COST))
    if not res: print(name, "none"); return
    v = np.array([x[1] for x in res]); a = [x[1] for x in res if x[0] < "2021"]; b_ = [x[1] for x in res if x[0] >= "2021"]
    perday = defaultdict(float)
    for d, x in res: perday[d] += x
    pd_ = np.array(list(perday.values()))
    print(f"{name:50s} n={len(v):6d} {len(v)/len(dates):.1f}/day net={v.mean():+5.1f}bps win={np.mean(v>0):.0%} t={v.mean()/v.std()*len(v)**.5:+5.2f} | 16-20 {np.mean(a):+5.1f} 21-26 {np.mean(b_):+5.1f}")
base = np.array([r[8] for r in rows]); print(f"baseline all stock-days open->close gross {base.mean():+.1f} bps (net {base.mean()-6:+.1f})")
test("long: 3 down closes, above SMA200 (deepest)", lambda r: r[3] if r[5] and r[2] else None)
test("long: IBS<0.2 above SMA200 (lowest IBS)", lambda r: r[4] if r[4] < 0.2 and r[2] else None)
test("long: worst prior day < -3%, above SMA200", lambda r: r[3] if r[3] < -0.03 and r[2] else None)
test("short: best prior day > +3%", lambda r: -r[3] if r[3] > 0.03 else None, side=-1)
test("long: gap down < -1.5%, above SMA200 (biggest gap)", lambda r: r[7] if r[7] < -0.015 and r[2] else None)
test("short: gap up > +1.5% (biggest gap)", lambda r: -r[7] if r[7] > 0.015 else None, side=-1)
test("long: gap up > +1.5% (gap-and-go)", lambda r: -r[7] if r[7] > 0.015 else None)
test("short: gap down < -1.5% (gap-and-go)", lambda r: r[7] if r[7] < -0.015 else None, side=-1)
