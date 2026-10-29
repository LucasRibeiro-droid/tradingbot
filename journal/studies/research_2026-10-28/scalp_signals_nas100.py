"""Pre-specified scalping / day-trading direction signals on NAS100 (OANDA 1-minute bid/ask), last 1000 days.
No parameters are fitted: each rule is fixed before looking. Entry at the next minute's open on the ask (long)
or bid (short); exit after a fixed hold at that minute's close on the other side. Reports how often the direction
was right (mid to mid, before costs) and the average result after the real spread + 0.12 pt commission a side."""
import sys
import numpy as np
sys.path.insert(0, "/home/user/tradingbot")
from tradingbot.learn import data
from tradingbot.learn.market import Market
m = Market("NAS100_USD", data.load("NAS100_USD"))
days = m.days[-1000:]
a0 = m.day_first[int(days[0])]
o, h, l, c = m.o, m.h, m.l, m.c
mins, day = m.mins, m.day
N = len(c)
valid = np.zeros(N, bool); valid[a0:] = True
# same-day guard for holds
def run(name, sig, hold):
    """sig: array of +1/-1/0 decided at the close of minute i."""
    idx = np.nonzero((sig != 0) & valid)[0]
    idx = idx[idx + hold < N]
    idx = idx[day[idx + hold] == day[idx]]
    # one trade at a time: skip signals while a trade is open
    keep, busy = [], -1
    for i in idx:
        if i > busy:
            keep.append(i); busy = i + hold
    idx = np.array(keep)
    d = sig[idx]
    e, x = idx + 1, idx + hold
    mid_move = (c[x] - o[e]) * d
    entry = np.where(d == 1, m.ao[e], m.bo[e]); exit_ = np.where(d == 1, m.bc[x], m.ac[x])
    net = (exit_ - entry) * d - 0.24
    per_day = len(idx) / len(days)
    halves = np.array_split(net, 2)
    print(f"{name:58s} hold {hold:3d}m  {per_day:6.1f}/day  direction right {np.mean(mid_move > 0):.1%}  "
          f"gross {mid_move.mean():+.2f} pts  net {net.mean():+.2f} pts  (halves {halves[0].mean():+.2f}/{halves[1].mean():+.2f})  "
          f"spread {np.mean(m.ac[e] - m.bc[e]):.2f}")
ret1 = np.r_[0, np.diff(c)]
r5 = c - np.r_[np.full(5, np.nan), c[:-5]]
r15 = c - np.r_[np.full(15, np.nan), c[:-15]]
rng = h - l
avg_rng = np.convolve(rng, np.ones(60) / 60, "full")[:N]
ny = (mins >= 930) & (mins < 1380)
for hold in (5, 15, 30):
    run("momentum: last 5 min up -> long, down -> short", np.sign(np.nan_to_num(r5)).astype(int), hold)
    run("momentum: last 15 min", np.sign(np.nan_to_num(r15)).astype(int), hold)
    run("reversal: last 5 min up -> short", -np.sign(np.nan_to_num(r5)).astype(int), hold)
    big = (np.abs(ret1) > 3 * avg_rng) & (avg_rng > 0)
    run("fade a 1-minute candle > 3x the hour's average range", np.where(big, -np.sign(ret1), 0).astype(int), hold)
    run("follow a 1-minute candle > 3x the hour's average range", np.where(big, np.sign(ret1), 0).astype(int), hold)
    run("momentum 15 min, New York session only", np.where(ny, np.sign(np.nan_to_num(r15)), 0).astype(int), hold)
