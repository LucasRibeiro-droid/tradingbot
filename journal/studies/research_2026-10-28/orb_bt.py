"""Stocks-in-play opening-range breakout (Zarattini, Barbon & Aziz 2024), on 150 liquid stocks, 5-minute SIP bars.
Each day: relative volume (first ORB bars' volume / same window's 14-day average); candidates with price >= $5,
ATR14 >= $0.50, RV >= rv_min; the top N by RV. Direction from the opening range candle (green: long on a break of
its high; red: short on a break of its low; doji: none). Stop = stop_atr x ATR14 from the entry. Exit: stop, or the
close (16:00). Fill: the first bar whose range reaches the trigger, at max(trigger, open); a bar that both fills and
reaches the stop counts as stopped. Costs: bps per side (stop exits pay extra slip_bps)."""
import pickle, sys
from collections import defaultdict
import numpy as np
S = pickle.load(open("/root/.cache/tradingbot/orb/bars5_150.pkl", "rb"))
# per symbol per day: bars
days = defaultdict(dict)
for s, a in S.items():
    for d in np.unique(a[:, 0]):
        x = a[a[:, 0] == d]
        if len(x) >= 70 and x[0, 1] == 570:
            days[int(d)][s] = x
dates = sorted(days)
# daily OHLC and ATR14, first-bar volumes per symbol
hist = defaultdict(list)  # s -> list of (date, high, low, close, v1, v3)
for d in dates:
    for s, x in days[d].items():
        hist[s].append((d, x[:, 3].max(), x[:, 4].min(), x[-1, 5], x[0, 6], x[:3, 6].sum()))
prev = {}
for s, h in hist.items():
    for k in range(15, len(h)):
        tr = [max(h[j][1], h[j - 1][3]) - min(h[j][2], h[j - 1][3]) for j in range(k - 14, k)]
        prev[(s, h[k][0])] = {"atr": np.mean(tr), "v1": np.mean([h[j][4] for j in range(k - 14, k)]),
                              "v3": np.mean([h[j][5] for j in range(k - 14, k)]), "close": h[k - 1][3]}
def run(N=5, rv_min=1.0, stop_atr=0.10, orb=1, cost=3.0, slip=0.0, force_min=0, both_dirs=False):
    out = []
    for d in dates:
        cands = []
        for s, x in days[d].items():
            p = prev.get((s, d))
            if not p or x[0, 2] < 5 or p["atr"] < 0.5: continue
            rv = x[:orb, 6].sum() / (p["v1"] if orb == 1 else p["v3"])
            cands.append((rv, s))
        cands.sort(reverse=True)
        chosen = [c for c in cands if c[0] >= rv_min][:N]
        if len(chosen) < force_min: chosen = cands[:force_min]
        for rv, s in chosen:
            x = days[d][s]; p = prev[(s, d)]
            o, h, l, c = x[0, 2], x[:orb, 3].max(), x[:orb, 4].min(), x[orb - 1, 5]
            if abs(c - o) < 1e-9: continue
            dirn = 1 if c > o else -1
            trig = h if dirn == 1 else l
            fill = None
            for k in range(orb, len(x)):
                if (x[k, 3] >= trig) if dirn == 1 else (x[k, 4] <= trig):
                    fill = k; break
            if fill is None: continue
            entry = max(trig, x[fill, 2]) if dirn == 1 else min(trig, x[fill, 2])
            risk = stop_atr * p["atr"]; stop = entry - dirn * risk
            exit_px, kind = None, "close"
            for k in range(fill, len(x)):
                if k > fill and ((x[k, 2] <= stop) if dirn == 1 else (x[k, 2] >= stop)):
                    exit_px, kind = x[k, 2], "stop"; break
                if (x[k, 4] <= stop) if dirn == 1 else (x[k, 3] >= stop):
                    exit_px, kind = stop, "stop"; break
            if exit_px is None: exit_px = x[-1, 5]
            gross = (exit_px - entry) * dirn
            c_ = (cost * (entry + exit_px) + (slip * exit_px if kind == "stop" else 0)) / 1e4
            out.append((d, s, dirn, gross / risk, (gross - c_) / risk, rv, risk / entry * 100))
    return out
def rep(name, r):
    if not r: print(name, "none"); return
    R = np.array([x[4] for x in r]); G = np.array([x[3] for x in r])
    days_ = len(dates); half = dates[len(dates) // 2]
    a = [x[4] for x in r if x[0] < half]; b = [x[4] for x in r if x[0] >= half]
    per_day = defaultdict(float)
    for x in r: per_day[x[0]] += x[4]
    pdv = np.array([per_day.get(d, 0.0) for d in dates])
    print(f"{name:46s} n={len(r):5d} {len(r)/days_:.1f}/day R={R.mean():+.3f} gross={G.mean():+.3f} win={np.mean(R>0):.0%} "
          f"t={R.mean()/R.std()*len(R)**.5:+.2f} | half1 {np.mean(a):+.3f} half2 {np.mean(b):+.3f} | day-Sharpe {pdv.mean()/pdv.std()*252**.5:.2f} stop%={np.median([x[6] for x in r]):.2f}")
if __name__ == "__main__":
    print("days", len(dates), dates[0], dates[-1])
    for name, kw in [("paper-like: top 5, RV>=1, 0.10 ATR, 3 bps", {}),
                     ("top 20", {"N": 20}), ("costs 10 bps + 5 bps stop slip", {"cost": 10, "slip": 5}),
                     ("stop 0.25 ATR", {"stop_atr": 0.25}), ("stop 0.5 ATR", {"stop_atr": 0.5}),
                     ("15-min opening range", {"orb": 3}), ("RV >= 2", {"rv_min": 2.0}),
                     ("at least 2 a day (forced)", {"force_min": 2})]:
        rep(name, run(**kw))
