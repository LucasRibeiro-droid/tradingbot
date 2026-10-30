import os, runpy, numpy as np
from collections import defaultdict
os.environ["NOWICK_OOS"] = "1"
g = runpy.run_path("journal/studies/nowick_15m_2026-10-30.py", run_name="lib")
m, run, days = g["m"], g["run"], g["days"]
from tradingbot.learn.market import date_of
print("OOS window", date_of(days[0]), date_of(days[-1]), len(days), "days")
for mom in g["MOM"]:
    for rr in (1.0, 2.0):
        _, out = run(mom, 0.0, rr=rr)
        r = np.array([t.r for _, t in out]); yr = defaultdict(list)
        for s, t in out: yr[date_of(int(m.day[s.known]))[:4]].append(t.r)
        print(f"{mom:12s} 1:{rr:g} strict: {len(r)} trades won {(r>0).sum()} lost {(r<=0).sum()} avg {r.mean():+.3f}R total {r.sum():+.1f}R  t={r.mean()/r.std()*len(r)**.5:+.2f} | " +
              " ".join(f"{y}:{sum(v):+.1f}({len(v)})" for y, v in sorted(yr.items())))
_, out = run("A structure", 0.0, rr=2.0)
by = defaultdict(list)
for s, t in out: by[date_of(int(m.day[s.known]))[:4]].append((t.risk, float(m.spread[t.fill_i]), t.r))
for y, v in sorted(by.items()):
    a = np.array(v); print(y, "median stop", np.median(a[:,0]).round(1), "median spread", np.median(a[:,1]).round(2), "spread/stop", np.median(a[:,1]/a[:,0]).round(3), "win", (a[:,2]>0).mean().round(3))
