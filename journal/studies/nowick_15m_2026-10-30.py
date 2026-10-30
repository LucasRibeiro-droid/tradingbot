"""Owner's 15m "no-wick" strategy (2026-10-30), NAS100, last 100 trading days, on OANDA 1m bid/ask.

Momentum of the moment (15m): down -> look for bearish candles with no top wick; mark the candle's high;
short when price comes back to it. Stop at the break-of-structure level (the latest confirmed 15m swing
high for a short); target 1:1. Longs mirror (bullish candle with no bottom wick, buy at its low, stop at
the latest swing low).

Rule choices the owner didn't specify ([Bot], each varied below):
- momentum: A = 15m market structure (direction of the last break of structure), B = close vs a rising /
  falling 20-EMA, C = last 3 candles (close below/above the close 3 candles ago)
- "no wick": the wick is <= tol x the candle's range (tol 0 = exactly none, 0.05, 0.10)
- the zone stays live until it is tapped, a newer zone replaces it, the momentum flips, 16 candles (4h)
  pass, or the trading day ends (17:00 NY; everything is flat at the day end)
- one trade at a time
- costs: OANDA's real spread + 0.5 pt slippage on stops + 0.12 pt a side (also shown with no costs)
"""
import sys
from collections import defaultdict
from datetime import datetime, timezone

import numpy as np

sys.path.insert(0, ".")
from tradingbot.learn import data, sim
from tradingbot.learn.concepts import breaks, swings
from tradingbot.learn.market import Market, date_of
from tradingbot.learn.setups import Signal

INST = "NAS100_USD"
raw = data.load(INST, datetime(2026, 4, 1, tzinfo=timezone.utc), datetime(2026, 10, 30, tzinfo=timezone.utc))
m = Market(INST, raw)
F = m.frames["15m"]
days = [d for d in m.days if len(m.days)][:-1] if date_of(int(m.days[-1])) >= "2026-10-30" else list(m.days)
days = [int(d) for d in days if date_of(int(d)) <= "2026-10-29"][-100:]
first_day = days[0]

sw = swings(F)
_, trend_bos = breaks(F, sw)
ema = np.empty(len(F)); a = 2 / 21; ema[0] = F.c[0]
for k in range(1, len(F)):
    ema[k] = a * F.c[k] + (1 - a) * ema[k - 1]
trend_ema = np.where((F.c < ema) & (ema < np.r_[ema[0], ema[:-1]]), -1, np.where((F.c > ema) & (ema > np.r_[ema[0], ema[:-1]]), 1, 0))
trend_3 = np.r_[np.zeros(3), np.sign(F.c[3:] - F.c[:-3])].astype(int)
MOM = {"A structure": trend_bos, "B ema20": trend_ema, "C last3": trend_3}

# latest confirmed swing high / low at each 15m candle (as known at that candle's close)
last_hi = np.full(len(F), np.nan); last_lo = np.full(len(F), np.nan)
j, hi, lo = 0, np.nan, np.nan
for k in range(len(F)):
    while j < len(sw) and sw[j].known <= F.known[k]:
        if sw[j].side == 1: hi = sw[j].level
        else: lo = sw[j].level
        j += 1
    last_hi[k], last_lo[k] = hi, lo


def run(mom, tol, costs=True):
    tr = MOM[mom]
    rng = F.h - F.l
    sigs = []
    for k in range(1, len(F)):
        d = int(F.day[k])
        if d < first_day or d > days[-1] or rng[k] <= 0:
            continue
        side = -int(tr[k]) * -1  # bias of the moment at this candle's close
        if side == -1 and F.c[k] < F.o[k] and F.h[k] - F.o[k] <= tol * rng[k]:
            entry, stop = F.h[k], last_hi[k]
        elif side == 1 and F.c[k] > F.o[k] and F.o[k] - F.l[k] <= tol * rng[k]:
            entry, stop = F.l[k], last_lo[k]
        else:
            continue
        if np.isnan(stop) or (stop - entry) * side >= 0:   # the BOS level must be beyond the entry
            continue
        # expiry: momentum flips, 16 candles, day end
        exp_k = min(k + 16, len(F) - 1)
        flip = np.nonzero(tr[k + 1:exp_k + 1] != side)[0]
        if len(flip):
            exp_k = k + 1 + flip[0]
        expiry = min(int(F.known[exp_k]), m.day_last[d])
        sigs.append(Signal(INST, "nowick", f"nowick {mom}", side, int(F.known[k]), "limit", float(entry), float(stop), expiry,
                           targets=(1.0, 1.0)))
    # a newer zone replaces the pending one
    for a_, b_ in zip(sigs, sigs[1:]):
        a_.expiry = min(a_.expiry, b_.known)
    saved = dict(sim.COSTS[INST])
    if not costs:
        sim.COSTS[INST] = {"slip": 0.0, "comm": 0.0}
    out, busy = [], -1
    for s in sigs:
        if s.known < busy:
            continue
        t = sim.simulate(m, s, "1R")
        if not costs and t.filled:   # no spread either: redo R on mids (target/stop hit = +1/-1, day end = mark)
            pass
        if t.filled:
            out.append((s, t)); busy = t.exit_i
    sim.COSTS[INST] = saved
    return sigs, out


def summary(out):
    r = np.array([t.r for _, t in out])
    if not len(r):
        return "no trades"
    byday = defaultdict(float)
    for s, t in out:
        byday[int(m.day[s.known])] += t.r
    dr = np.array(list(byday.values()))
    eq = np.cumsum(r); dd = (eq - np.maximum.accumulate(eq)).min()
    pts = np.array([t.risk for _, t in out])
    return (f"{len(r):4d} trades ({len(r)/100:.1f}/day) win {np.mean(r>0):5.1%}  avg {r.mean():+.3f}R  total {r.sum():+7.1f}R  "
            f"profitable days {np.mean(dr>0):5.1%} of {len(dr)}  maxDD {dd:.1f}R  median stop {np.median(pts):.1f}pt")


if __name__ == "__main__":
    print(f"NAS100 15m, {date_of(days[0])} .. {date_of(days[-1])} ({len(days)} trading days)\n")
    for mom in MOM:
        for tol in (0.0, 0.05, 0.10):
            sigs, out = run(mom, tol)
            _, out0 = run(mom, tol, costs=False)
            r0 = np.array([t.r for _, t in out0])
            print(f"{mom:12s} wick<={tol:.0%}: {summary(out)}")
            print(f"{'':12s}   no slippage/commission (spread kept): avg {r0.mean() if len(r0) else 0:+.3f}R, total {r0.sum():+.1f}R")

    print("\nNew York hours only (zone and fill 09:30-16:00 NY), and by side:")
    for mom in MOM:
        for tol in (0.0, 0.05):
            _, out = run(mom, tol)
            ny = [(s, t) for s, t in out if 930 <= m.mins[s.known] and m.mins[t.fill_i] < 1320]
            print(f"{mom:12s} wick<={tol:.0%} NY: {summary(ny)}")
            for side, nm in ((1, "longs"), (-1, "shorts")):
                print(f"{'':12s}   {nm:6s}: {summary([(s, t) for s, t in out if s.side == side])}")
