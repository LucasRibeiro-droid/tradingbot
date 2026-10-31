"""Owner's no-wick 15m strategy with a fixed stop of 10 pips (NAS100 at OANDA: 1 pip = 1 index point) beyond the
entry and the target always 1:2 (20 points). Momentum of the moment: the three readings of
nowick_15m_2026-10-30.py (15m structure, 20-EMA, last 3 candles). Last 100 trading days and the earlier
untested history 2021-01 .. 2026-06-11. Costs: OANDA's real spread (+0.5 pt stop slippage, 0.12 pt a side) and
NQ-futures-like (mid +/- 0.125 pt, 0.25 pt stop slippage, 0.12 pt a side)."""
import copy, os, runpy, sys
from collections import defaultdict
import numpy as np
os.environ["NOWICK_OOS"] = "1"
sys.path.insert(0, ".")
g = runpy.run_path("journal/studies/nowick_15m_2026-10-30.py", run_name="lib")
from tradingbot.learn import sim
from tradingbot.learn.market import date_of
m, run = g["m"], g["run"]
G = run.__globals__
all_days = [int(d) for d in m.days if date_of(int(d)) <= "2026-10-29"][5:]
fut = copy.copy(m)
half = 0.125
fut.bo, fut.bh, fut.bl, fut.bc = m.o - half, m.h - half, m.l - half, m.c - half
fut.ao, fut.ah, fut.al, fut.ac = m.o + half, m.h + half, m.l + half, m.c + half
fut.spread = np.full(len(m.o), 2 * half)


def go(window, cost, mom, tol):
    G["first_day"], G["days"] = window[0], window
    if cost == "futures":
        G["m"] = fut; saved = dict(sim.COSTS["NAS100_USD"]); sim.COSTS["NAS100_USD"] = {"slip": 0.25, "comm": 0.12}
    try:
        _, out = run(mom, tol, stop_mode=10.0, rr=2.0)
    finally:
        G["m"] = m
        if cost == "futures": sim.COSTS["NAS100_USD"] = saved
    return out


def line(out, label):
    r = np.array([t.r for _, t in out])
    if not len(r): return print(label, "no trades")
    by = defaultdict(float)
    for s, t in out: by[date_of(int(m.day[s.known]))[:4]] += t.r
    pts = sum(t.r * t.risk for _, t in out)
    print(f"{label}: {len(r)} trades, won {(r > 0).sum()} lost {(r <= 0).sum()} ({(r > 0).mean():.1%}), avg {r.mean():+.3f}R, "
          f"total {r.sum():+.1f}R ({pts:+,.0f} pts; NQ $20/pt ${pts * 20:+,.0f})" + ("  | " + " ".join(f"{y} {v:+.0f}R" for y, v in sorted(by.items())) if len(by) > 1 else ""))


for cost in ("futures", "oanda"):
    print(f"\n=== costs: {cost} ===")
    for mom in G["MOM"]:
        for tol in (0.0, 0.05, 0.10):
            line(go(all_days[-100:], cost, mom, tol), f"{mom:12s} wick<={tol:.0%} last 100 days")
            line(go(all_days[:-100], cost, mom, tol), f"{'':12s} wick<={tol:.0%} 2021-01..2026-06 ")
