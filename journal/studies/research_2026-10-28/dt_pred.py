"""Day trade on the predictor (QQQ): model fit on sessions before 2021, traded 2021-2026 (out of sample).
At each 30-minute checkpoint from START to LAST, if P(low in) >= th and P(high in) <= th2: long at that bar's
close, stop just below the day's low so far, exit at the first of: stop, target (high so far + k*range?),
or 15:55. Mirror for shorts. One trade per day per side max. Costs 3 bps a side (QQQ ~0.3 bps spread)."""
import math, pickle, sys
import numpy as np
sys.path.insert(0, "/home/user/tradingbot")
from tradingbot.live import hl_predict as H
bars = pickle.loads(H.QQQ_CACHE.read_bytes())
m = H.fit(bars, "2021-01-01")
S = H.sessions(bars); days = [d for d in sorted(S) if S[d].get("n", 0) >= 70]
COST = 3e-4
def run(th=0.8, th2=0.5, start=600, last=870, buf=0.0005, target=None, split="2024-01-01"):
    res = []
    for k in range(22, len(days)):
        d = days[k]
        if d.isoformat() < "2021-01-01": continue
        t = S[d]; f = H.open_features([S[x] for x in days[k-22:k]], t)
        if not f: continue
        rh = H.at_open(m, f, t["open"])["range_pct"] / 100
        b = t["bars"]; done = set()
        for T in range(start, last + 1, 30):
            seen = [c for mm, c in b if mm < T]
            rest = [c for mm, c in b if T <= mm < 955]
            if not seen or not rest: continue
            h, l, last_px = max(c.h for c in seen), min(c.l for c in seen), seen[-1].c
            p = H.p_extreme_in(m, T, h, l, last_px, rh, f["gap"])
            for side, d_ in (("long", 1), ("short", -1)):
                if side in done: continue
                pin, pother = (p["low"], p["high"]) if d_ == 1 else (p["high"], p["low"])
                if pin < th or pother > th2: continue
                entry = last_px; stop = l * (1 - buf) if d_ == 1 else h * (1 + buf)
                risk = abs(entry - stop)
                tp = entry + d_ * risk * target if target else None
                exit_px = None
                for c in rest:
                    if (c.l <= stop) if d_ == 1 else (c.h >= stop): exit_px = stop; break
                    if tp and ((c.h >= tp) if d_ == 1 else (c.l <= tp)): exit_px = tp; break
                if exit_px is None: exit_px = rest[-1].c
                gross = (exit_px - entry) * d_
                res.append((d.isoformat(), side, T, gross / risk, (gross - COST * (entry + exit_px)) / risk, gross / entry * 1e4 - 2 * COST * 1e4))
                done.add(side)
    return res
def rep(name, r, split="2024-01-01"):
    if not r: print(name, "none"); return
    a = np.array([x[4] for x in r]); bp = np.array([x[5] for x in r])
    e = [x for x in r if x[0] < split]; l = [x for x in r if x[0] >= split]
    days_n = len({x[0] for x in r})
    print(f"{name:52s} n={len(r):4d} ({len(r)/1460*1:.2f}/day) R={a.mean():+.3f} bps={bp.mean():+5.1f} win={np.mean(a>0):.0%} "
          f"t={a.mean()/a.std()*len(a)**.5:+.2f} | 21-23 {np.mean([x[4] for x in e]):+.3f} (n={len(e)}) 24-26 {np.mean([x[4] for x in l]):+.3f} (n={len(l)})")
    for s in ("long", "short"):
        z = [x[4] for x in r if x[1] == s]
        if z: print(f"{'':52s}   {s}: n={len(z)} R={np.mean(z):+.3f}")
for kw in ({}, {"th": 0.7}, {"th": 0.9}, {"target": 1.0}, {"target": 2.0}, {"start": 630, "last": 780}, {"th2": 0.3}):
    rep(f"P>={kw.get('th',0.8)} other<={kw.get('th2',0.5)} {kw}", run(**kw))
