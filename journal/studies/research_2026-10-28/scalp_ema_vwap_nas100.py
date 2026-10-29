"""Owner's scalping spec, NAS100, 2025-01 -> 2026-10, fixed standard settings (nothing tuned):
context: EMA200 (or SuperTrend 10,3) on the last CLOSED 15m (or 1h) candle -> longs only above / shorts only below;
signal (1m): EMA9 crosses EMA21 in that direction (or RSI14 crosses 50), price on the same side of the session VWAP
(tick volume, reset 18:00 New York); skip when ATR14 > 2x its 100-minute average (noise);
risk: stop 1 x ATR14 from entry, target 1:1 or 1:2; flat at the day's end; one trade at a time.
Fills on the real bid/ask + 0.5 pt slippage on market/stop fills + 0.12 pt commission a side (sim.py)."""
import pickle, sys
from collections import defaultdict
from datetime import date, datetime, timezone
import numpy as np
sys.path.insert(0, "/home/user/tradingbot")
from tradingbot.learn import data
from tradingbot.learn.market import Market, date_of
from tradingbot.learn.setups import Signal
from tradingbot.learn.sim import simulate

m = Market("NAS100_USD", data.load("NAS100_USD", start=datetime(2024, 10, 1, tzinfo=timezone.utc)))
vol = pickle.load(open("/root/.cache/tradingbot/learn/nas100_m1_volume_2025_2026.pkl", "rb"))
v = np.array([vol.get(int(t), 0) for t in m.t], dtype=float)

def ema(x, n):
    out = np.empty(len(x)); a = 2 / (n + 1); out[0] = x[0]
    for k in range(1, len(x)): out[k] = a * x[k] + (1 - a) * out[k - 1]
    return out
def wilder(x, n):
    out = np.empty(len(x)); out[0] = x[0]
    for k in range(1, len(x)): out[k] = out[k - 1] + (x[k] - out[k - 1]) / n
    return out
def supertrend(f, n=10, mult=3.0):
    tr = np.maximum(f.h - f.l, np.maximum(np.abs(f.h - np.r_[f.c[0], f.c[:-1]]), np.abs(f.l - np.r_[f.c[0], f.c[:-1]])))
    atr = wilder(tr, n); mid = (f.h + f.l) / 2
    up, dn = mid - mult * atr, mid + mult * atr
    d = np.ones(len(f), int); fu, fd = up.copy(), dn.copy()
    for k in range(1, len(f)):
        fu[k] = max(up[k], fu[k - 1]) if f.c[k - 1] > fu[k - 1] else up[k]
        fd[k] = min(dn[k], fd[k - 1]) if f.c[k - 1] < fd[k - 1] else dn[k]
        d[k] = 1 if f.c[k] > fd[k - 1] else (-1 if f.c[k] < fu[k - 1] else d[k - 1])
    return d

def htf_dir(tf, kind):
    f = m.frames[tf]
    d = np.sign(f.c - ema(f.c, 200)).astype(int) if kind == "ema200" else supertrend(f)
    # for each 1-minute candle: the direction of the last CLOSED higher-timeframe candle
    k = np.searchsorted(f.known, np.arange(len(m.c)), side="right") - 1
    return np.where(k >= 0, d[np.maximum(k, 0)], 0)

c = m.c
e9, e21 = ema(c, 9), ema(c, 21)
delta = np.r_[0, np.diff(c)]
rs = wilder(np.maximum(delta, 0), 14) / np.maximum(wilder(np.maximum(-delta, 0), 14), 1e-9)
rsi = 100 - 100 / (1 + rs)
tr = np.maximum(m.h - m.l, np.maximum(np.abs(m.h - np.r_[c[0], c[:-1]]), np.abs(m.l - np.r_[c[0], c[:-1]])))
atr = wilder(tr, 14)
atr_avg = np.convolve(atr, np.ones(100) / 100, "full")[:len(atr)]
tp = (m.h + m.l + c) / 3
vwap = np.empty(len(c))
for d in m.days:
    a, b = m.day_first[int(d)], m.day_last[int(d)]
    pv, vv = np.cumsum(tp[a:b + 1] * v[a:b + 1]), np.cumsum(v[a:b + 1])
    vwap[a:b + 1] = np.where(vv > 0, pv / np.maximum(vv, 1e-9), tp[a:b + 1])
start = date(2025, 1, 1).toordinal()
test_days = [d for d in m.days if d >= start]
first_i = m.day_first[int(test_days[0])]

def run(ctx_tf, ctx_kind, trigger, target):
    hd = htf_dir(ctx_tf, ctx_kind)
    if trigger == "ema9/21":
        up = (e9 > e21) & (np.r_[False, e9[:-1] <= e21[:-1]])
        dn = (e9 < e21) & (np.r_[False, e9[:-1] >= e21[:-1]])
    else:
        up = (rsi > 50) & (np.r_[False, rsi[:-1] <= 50])
        dn = (rsi < 50) & (np.r_[False, rsi[:-1] >= 50])
    calm = atr <= 2 * atr_avg
    long_sig = up & (hd == 1) & (c > vwap) & calm
    short_sig = dn & (hd == -1) & (c < vwap) & calm
    idx = np.nonzero((long_sig | short_sig) & (np.arange(len(c)) >= first_i))[0]
    trades, busy = [], -1
    for i in idx:
        if i <= busy or m.mins[i] >= 1375:
            continue
        side = 1 if long_sig[i] else -1
        s = Signal("NAS100_USD", "scalp", "scalp", side, int(i), "market", float(c[i]), float(c[i] - side * atr[i]), int(i), {}, "")
        t = simulate(m, s, target)
        if not t.filled:
            continue
        busy = t.exit_i
        trades.append((int(m.day[i]), side, t.r, m.session_of(int(i))))
    r = np.array([x[2] for x in trades])
    if not len(r):
        print(ctx_tf, ctx_kind, trigger, target, "no trades"); return
    per_day = defaultdict(float)
    for d, _, rr, _ in trades: per_day[d] += rr
    dr = np.array([per_day.get(d, 0.0) for d in test_days])
    traded = dr[np.array([d in per_day for d in test_days])]
    eq = np.cumsum(dr); dd = (eq - np.maximum.accumulate(eq)).min()
    y25 = r[np.array([date_of(x[0]) < "2026" for x in trades])]; y26 = r[np.array([date_of(x[0]) >= "2026" for x in trades])]
    lo = r[np.array([x[1] == 1 for x in trades])]; sh = r[np.array([x[1] == -1 for x in trades])]
    ny = r[np.array([x[3] == "newyork" for x in trades])]
    print(f"{ctx_kind:9s} {ctx_tf:3s} {trigger:8s} {target}: {len(r) / len(test_days):5.1f}/day  win {np.mean(r > 0):.0%}  avg {r.mean():+.3f}R  "
          f"total {r.sum():+7.1f}R  profitable days {np.mean(traded > 0):.0%}  max DD {dd:6.1f}R | 2025 {y25.mean():+.3f} 2026 {y26.mean():+.3f} | "
          f"long {lo.mean():+.3f} short {sh.mean():+.3f} | NY session {ny.mean():+.3f} (n={len(ny)})")

print(f"NAS100 {date_of(test_days[0])} -> {date_of(test_days[-1])}, {len(test_days)} trading days")
for ctx_tf in ("15m", "1h"):
    for ctx_kind in ("ema200", "supertrend"):
        for trigger in ("ema9/21", "rsi50"):
            for target in ("1R", "2R"):
                run(ctx_tf, ctx_kind, trigger, target)

# what the same entries do before any cost: mid-price fills, no slippage, no commission
import tradingbot.learn.sim as S
m.ao = m.bo = m.o; m.ah = m.bh = m.h; m.al = m.bl = m.l; m.ac = m.bc = m.c; m.spread = np.zeros(len(c)) + 1e-9
S.COSTS["NAS100_USD"] = {"slip": 0.0, "comm": 0.0}
print("\nBEFORE COSTS (mid prices, no spread/slippage/commission); median stop", round(float(np.median(atr[first_i:])), 2), "pts; median spread",
      round(float(np.median((data.load('NAS100_USD', start=datetime(2025,1,1,tzinfo=timezone.utc))[:, 8] - data.load('NAS100_USD', start=datetime(2025,1,1,tzinfo=timezone.utc))[:, 4]))), 2), "pts")
for ctx_tf, ctx_kind, trigger in (("15m", "ema200", "ema9/21"), ("1h", "supertrend", "ema9/21"), ("15m", "ema200", "rsi50")):
    for target in ("1R", "2R"):
        run(ctx_tf, ctx_kind, trigger, target)
