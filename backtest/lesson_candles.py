# Real NQ 5m examples for the Day 2 lesson: classify candles with the bot's Day-2 rules and export a few.
import sys, json, numpy as np, pandas as pd
b = pd.read_pickle(sys.argv[1] + "/b_5min.pkl")
b = b[(b.index >= "2025-09-01") & (b.index.hour >= 9) & (b.index.hour < 16)]
o, h, l, c = (b[k].values for k in "ohlc"); rng = h - l; body = np.abs(c - o)
up = h - np.maximum(o, c); dn = np.minimum(o, c) - l
avg = pd.Series(rng).rolling(20).mean().values
def kind(i):
    r = rng[i]
    if r < 0.8 * avg[i] or r <= 0: return None
    pos = (c[i] - l[i]) / r
    if body[i] <= 0.10 * r: return "doji"
    if body[i] >= 0.70 * r and (up[i] if c[i] > o[i] else dn[i]) <= 0.10 * r: return "strong_bull" if c[i] > o[i] else "strong_bear"
    if dn[i] >= 0.5 * r and pos >= 2/3: return "rejection_bull"
    if up[i] >= 0.5 * r and pos <= 1/3: return "rejection_bear"
    if c[i] > o[i] and up[i] >= body[i]: return "weak_bull"
    if c[i] < o[i] and dn[i] >= body[i]: return "weak_bear"
    return None
want = ["strong_bull", "strong_bear", "rejection_bull", "rejection_bear", "weak_bull", "doji", "strong_bear", "rejection_bull"]
rs = np.random.default_rng(7); out = []; used = set()
idx = np.arange(40, len(c) - 10); rs.shuffle(idx)
for w in want:
    for i in idx:
        if i in used or kind(i) != w: continue
        if b.index[i - 30].date() != b.index[i + 8].date(): continue
        used.add(i)
        sl = slice(i - 30, i + 9)
        out.append(dict(kind=w, t=b.index[i].strftime("%a %d %b %Y %H:%M"), focus=30,
                        bars=[[round(float(x), 2) for x in row] for row in zip(o[sl], h[sl], l[sl], c[sl])]))
        break
json.dump(out, open(sys.argv[2], "w"))
print(len(out), [e["kind"] for e in out])
