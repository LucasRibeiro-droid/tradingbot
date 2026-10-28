"""Portfolio: each position 10% of equity (1% risk with a 10% catastrophic stop), at most 10 at once;
when more signals than free slots, take the deepest 3-day drop first. Entry/exit at the close, 3 bps a side."""
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-tradingbot/efe032f3-ac09-5164-8e64-23adecf81035/scratchpad/research")
import daily_bt as B
import numpy as np
def sim(data, cost=3, slots=10, stop=0.10, label=""):
    syms = sorted(data); dates = sorted({b.t[:10] for v in data.values() for b in v})
    idx = {s: {b.t[:10]: k for k, b in enumerate(data[s])} for s in syms}
    C = {s: [b.c for b in data[s]] for s in syms}; H = {s: [b.h for b in data[s]] for s in syms}; L = {s: [b.l for b in data[s]] for s in syms}
    eq, pos, curve, trades, held_days = 1.0, {}, [], [], 0
    for d in dates:
        # exits
        for s in list(pos):
            k = idx[s].get(d)
            if k is None: continue
            e = pos[s]; px = None
            if L[s][k] <= e["px"] * (1 - stop): px = min(data[s][k].o, e["px"] * (1 - stop))
            elif C[s][k] > H[s][k - 1] or k - e["k"] >= 10: px = C[s][k]
            if px is not None:
                r = px / e["px"] - 1 - 2 * cost / 1e4
                eq += e["size"] * r; trades.append(r); del pos[s]
        # mark to market for the curve
        mtm = eq + sum(p["size"] * (C[s][idx[s][d]] / p["px"] - 1) for s, p in pos.items() if d in idx[s])
        curve.append(mtm); held_days += len(pos)
        # entries
        cands = []
        for s in syms:
            k = idx[s].get(d)
            if k is None or k < 200 or s in pos: continue
            c = C[s]
            if c[k] > sum(c[k - 199:k + 1]) / 200 and c[k] < c[k - 1] < c[k - 2] < c[k - 3]:
                cands.append((c[k] / c[k - 3] - 1, s, k))
        for _, s, k in sorted(cands)[:max(0, slots - len(pos))]:
            pos[s] = {"px": C[s][k], "k": k, "size": 0.10 * mtm}
    curve = np.array(curve); years = len(dates) / 252
    dd = (curve / np.maximum.accumulate(curve) - 1).min()
    rets = np.diff(np.log(curve)); sharpe = rets.mean() / rets.std() * np.sqrt(252)
    print(f"{label:28s} CAGR {curve[-1] ** (1 / years) - 1:+.1%}  max drawdown {dd:.1%}  Sharpe {sharpe:.2f}  trades {len(trades)}  "
          f"win {np.mean(np.array(trades) > 0):.0%}  avg positions {held_days / len(dates):.1f}")
    return dates, curve
stocks = B.load("stocks"); etfs = B.load("etfs")
for lab, data in (("stocks 2016-2026", stocks), ("ETFs 2016-2026", etfs)):
    sim(data, label=lab)
    sim(data, cost=10, label=lab + " (10 bps costs)")
for lab, k0, k1 in (("stocks 2016-2020", "2015", "2021"), ("stocks 2021-2026", "2020-06", "2027")):
    sub = {s: [b for b in v if k0 <= b.t[:10] < k1] for s, v in stocks.items()}
    sim(sub, label=lab)
spy = [b.c for b in etfs["SPY"]]; c = np.array(spy) / spy[0]; yrs = len(spy) / 252
print(f"{'SPY buy and hold':28s} CAGR {c[-1] ** (1 / yrs) - 1:+.1%}  max drawdown {(c / np.maximum.accumulate(c) - 1).min():.1%}  Sharpe {np.diff(np.log(c)).mean() / np.diff(np.log(c)).std() * np.sqrt(252):.2f}")
