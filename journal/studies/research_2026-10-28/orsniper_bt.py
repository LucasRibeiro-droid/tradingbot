"""Backtest of the owner's TradingView indicator "9:35 Opening Range Sniper" exactly as coded, on OANDA
NAS100_USD 1-minute candles (the owner's chart is 1-minute). Signals on mid prices; trades filled on the
real bid/ask. Entry at the close of the signal candle. One trade at a time (signals while a trade is open
are skipped). Stops from the description: tight (signal candle's low/high), mid (other side of the midpoint),
box (other side of the opening-range box). Targets 1R/2R/3R. A candle that reaches both the stop and the
target counts as the stop. Open trades are closed at 16:59 ET (before the daily break)."""
import pickle, sys
from datetime import datetime
from zoneinfo import ZoneInfo
import numpy as np
NY = ZoneInfo("America/New_York")
rows = pickle.load(open("/root/.cache/tradingbot/nas_m1/nas100_m1_ba.pkl", "rb"))
T, bo, bh, bl, bc, ao, ah, al, ac = zip(*rows)
bo, bh, bl, bc, ao, ah, al, ac = map(np.array, (bo, bh, bl, bc, ao, ah, al, ac))
mo, mh, ml, mc = (bo + ao) / 2, (bh + ah) / 2, (bl + al) / 2, (bc + ac) / 2
ny = [datetime.fromisoformat(t.replace("Z", "+00:00")).astimezone(NY) for t in T]
mins = np.array([n.hour * 60 + n.minute for n in ny])
# TradingView daily bar for this CFD: 18:00 -> 17:00 New York; the "day" is the date the session ends on
day = [(n.date() if n.hour < 18 else (n + __import__("datetime").timedelta(days=1)).date()) for n in ny]
TICK = 0.1

def signals():
    """Exactly the script: per bar, reset on a new day, capture the OR on 09:35-09:39 bars (each overwrites),
    then breakout flags (sticky for the day), then retest conditions."""
    out = []
    orH = orL = orM = None; above = below = False
    for i in range(len(rows)):
        if i > 0 and day[i] != day[i - 1]:
            orH = orL = orM = None; above = below = False
        if 575 <= mins[i] < 580:  # session "0935-0940"
            orH, orL = mh[i], ml[i]; orM = (orH + orL) / 2
        if orH is not None and mc[i] > orH: above = True
        if orL is not None and mc[i] < orL: below = True
        if above and ml[i] <= orM and mc[i] > orH: out.append((i, 1, orH, orL, orM))
        if below and mh[i] >= orM and mc[i] < orL: out.append((i, -1, orH, orL, orM))
    return out

def trade(sigs, stop_mode, R, same_bar="stop"):
    res, busy_until = [], -1
    for i, d, orH, orL, orM in sigs:
        if i <= busy_until: continue
        entry = ac[i] if d == 1 else bc[i]
        if stop_mode == "tight": stop = ml[i] - TICK if d == 1 else mh[i] + TICK
        elif stop_mode == "mid": stop = orM - TICK if d == 1 else orM + TICK
        else: stop = orL - TICK if d == 1 else orH + TICK
        risk = (entry - stop) * d
        if risk <= 0: continue
        tp = entry + d * R * risk
        exit_px, kind, j = None, None, i + 1
        while j < len(rows):
            if day[j] != day[i] or mins[j] >= 1019:  # 16:59 ET: close at that bar's open
                exit_px, kind = (bo[j] if d == 1 else ao[j]), "time"; break
            lo, hi, op = (bl[j], bh[j], bo[j]) if d == 1 else (al[j], ah[j], ao[j])
            hit_stop = (lo <= stop) if d == 1 else (hi >= stop)
            hit_tp = (hi >= tp) if d == 1 else (lo <= tp)
            if hit_stop and (not hit_tp or same_bar == "stop"):
                exit_px = min(op, stop) if d == 1 else max(op, stop); kind = "stop"; break
            if hit_tp:
                exit_px = tp; kind = "target"; break
            j += 1
        if exit_px is None: break
        busy_until = j
        r = (exit_px - entry) * d / risk
        res.append((ny[i], d, r, kind, risk, mins[i]))
    return res

def summary(name, res):
    if not res: print(name, "no trades"); return
    r = np.array([x[2] for x in res]); eq = np.cumsum(r); dd = (eq - np.maximum.accumulate(eq)).min()
    half = ny[len(ny) // 2]
    a = [x[2] for x in res if x[0] < half]; b = [x[2] for x in res if x[0] >= half]
    rth = [x[2] for x in res if 575 <= x[5] < 960]; other = [x[2] for x in res if not 575 <= x[5] < 960]
    pf = r[r > 0].sum() / -r[r < 0].sum() if (r < 0).any() else float("inf")
    print(f"{name:22s} trades {len(r):4d}  win {np.mean(r > 0):4.0%}  avg {r.mean():+.3f}R  total {r.sum():+7.1f}R  "
          f"PF {pf:4.2f}  max DD {dd:6.1f}R | 1st half {np.mean(a):+.3f} 2nd half {np.mean(b):+.3f} | "
          f"9:35-16:00 {np.mean(rth):+.3f} (n={len(rth)}) after 16:00 {np.mean(other) if other else 0:+.3f} (n={len(other)}) "
          f"| median risk {np.median([x[4] for x in res]):.1f} pts")

sigs = signals()
days_n = len(set(day))
print(f"{len(rows)} one-minute candles, {days_n} days {ny[0]:%Y-%m-%d} to {ny[-1]:%Y-%m-%d}; signals {len(sigs)} "
      f"({len(sigs) / days_n:.1f} a day; long {sum(1 for s in sigs if s[1] == 1)}, short {sum(1 for s in sigs if s[1] == -1)})")
print("median spread (points):", round(float(np.median(ac - bc)), 2))
for stop_mode in ("tight", "mid", "box"):
    for R in (1, 2, 3):
        summary(f"stop {stop_mode:5s} target 1:{R}", trade(sigs, stop_mode, R))
print("\nSame, but a candle reaching both counts as the TARGET (optimistic):")
for stop_mode in ("tight", "mid", "box"):
    for R in (1, 2, 3):
        summary(f"stop {stop_mode:5s} target 1:{R}", trade(sigs, stop_mode, R, same_bar="target"))
