"""Daily strategy tests. Entry/exit at the close unless noted; 3 bps per side.
Each trade: net return (bps), days held. Benchmark: buy-and-hold's average daily return times days held
(a long strategy must beat the drift it was exposed to)."""
import pickle, sys
from statistics import mean, pstdev
D = "/root/.cache/tradingbot/daily_2016/"
COST = 3.0
def load(name):
    return pickle.load(open(D + name + ".pkl", "rb"))
def sma(x, n, i):
    return sum(x[i - n + 1:i + 1]) / n if i >= n - 1 else None
def rsi(c, n, i):
    if i < n: return None
    g = [max(c[k] - c[k - 1], 0) for k in range(i - n + 1, i + 1)]
    l = [max(c[k - 1] - c[k], 0) for k in range(i - n + 1, i + 1)]
    return 100.0 if sum(l) == 0 else 100 - 100 / (1 + sum(g) / sum(l))

def run(data, strat):
    trades = []
    for sym, bars in data.items():
        o = [b.o for b in bars]; h = [b.h for b in bars]; l = [b.l for b in bars]; c = [b.c for b in bars]
        drift = mean(c[k] / c[k - 1] - 1 for k in range(1, len(c)))
        i = 200
        while i < len(c) - 1:
            sig = strat(o, h, l, c, i)
            if not sig:
                i += 1; continue
            entry_px, exit_i, exit_px = sig
            ret = (exit_px / entry_px - 1) * 1e4 - 2 * COST
            held = max(exit_i - i, 0) + (0 if exit_px is not c[exit_i] else 0)
            trades.append((bars[i].t[:10], sym, ret, max(exit_i - i, 1), drift * 1e4 * max(exit_i - i, 1)))
            i = max(exit_i, i + 1)
    return trades

def report(name, tr, split="2021-01-01"):
    if not tr: print(name, "no trades"); return
    t = lambda x: mean(x) / (pstdev(x) / len(x) ** .5) if len(x) > 1 and pstdev(x) else 0
    def line(sub):
        r = [x[2] for x in sub]; ex = [x[2] - x[4] for x in sub]
        return f"n={len(sub):5d} net={mean(r):+6.1f}bps win={mean(v > 0 for v in r):.0%} days={mean(x[3] for x in sub):4.1f} excess={mean(ex):+6.1f} t={t(r):+5.2f}"
    a = [x for x in tr if x[0] < split]; b = [x for x in tr if x[0] >= split]
    yrs = sorted({x[0][:4] for x in tr})
    by = " ".join(f"{y[2:]}:{mean(x[2] for x in tr if x[0][:4] == y):+.0f}" for y in yrs)
    print(f"{name:38s} ALL {line(tr)}\n{'':38s} 16-20 {line(a)}\n{'':38s} 21-26 {line(b)}\n{'':38s} by year {by}")

# ---- strategies: return (entry price, exit index, exit price) or None ----
def rsi2(o, h, l, c, i, lo=10, maxd=10):
    if c[i] <= sma(c, 200, i) or rsi(c, 2, i) >= lo: return None
    for k in range(i + 1, min(i + maxd, len(c) - 1) + 1):
        if c[k] > sma(c, 5, k): return (c[i], k, c[k])
    k = min(i + maxd, len(c) - 1); return (c[i], k, c[k])
def ibs(o, h, l, c, i, lo=0.2):
    if h[i] == l[i] or (c[i] - l[i]) / (h[i] - l[i]) >= lo: return None
    return (c[i], i + 1, c[i + 1])
def overnight(o, h, l, c, i):
    return (c[i], i + 1, o[i + 1])
def down3(o, h, l, c, i):
    if c[i] <= sma(c, 200, i) or not (c[i] < c[i - 1] < c[i - 2] < c[i - 3]): return None
    for k in range(i + 1, min(i + 10, len(c) - 1) + 1):
        if c[k] > h[k - 1]: return (c[i], k, c[k])
    k = min(i + 10, len(c) - 1); return (c[i], k, c[k])
def donchian(o, h, l, c, i):
    if c[i] <= sma(c, 200, i) or c[i] < max(h[i - 20:i]): return None
    for k in range(i + 1, len(c)):
        if c[k] < min(l[k - 10:k]): return (c[i], k, c[k])
    return (c[i], len(c) - 1, c[-1])
def gap_down(o, h, l, c, i):
    if i + 1 >= len(c) or o[i + 1] >= l[i] * 0.99 or c[i] <= sma(c, 200, i): return None
    return (o[i + 1], i + 1, c[i + 1])

if __name__ == "__main__":
    which = sys.argv[1]
    data = load(which)
    for name, s in [("RSI2<10 above SMA200, exit >SMA5", rsi2), ("IBS<0.2, hold 1 day", ibs),
                    ("overnight close->open", overnight), ("3 down closes above SMA200", down3),
                    ("20d breakout, 10d-low exit", donchian), ("gap down >1% below low, open->close", gap_down)]:
        report(f"{which}: {name}", run(data, s))
