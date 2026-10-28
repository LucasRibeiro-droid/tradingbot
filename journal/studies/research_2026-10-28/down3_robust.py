import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-tradingbot/efe032f3-ac09-5164-8e64-23adecf81035/scratchpad/research")
import daily_bt as B
from statistics import mean
def make(n_down=3, ma=200, exit_rule="hi", maxd=10, entry="close", stop=None):
    def s(o, h, l, c, i):
        m = B.sma(c, ma, i)
        if m is None or c[i] <= m or i < n_down or not all(c[i - k] < c[i - k - 1] for k in range(n_down)): return None
        if entry == "open":
            if i + 1 >= len(c): return None
            ep, i0 = o[i + 1], i + 1
        else:
            ep, i0 = c[i], i
        for k in range(i0 + (0 if entry == "open" else 1), min(i + maxd, len(c) - 1) + 1):
            if stop and l[k] <= ep * (1 - stop): return (ep, k, min(o[k], ep * (1 - stop)))
            if (exit_rule == "hi" and k > i and c[k] > h[k - 1]) or (exit_rule == "ma5" and c[k] > B.sma(c, 5, k)): return (ep, k, c[k])
        k = min(i + maxd, len(c) - 1); return (ep, k, c[k])
    return s
for which in ("etfs", "stocks"):
    data = B.load(which)
    print("=====", which)
    for name, kw, cost in [("base (3 down, SMA200, exit close>prior high)", {}, 3),
                           ("costs 10 bps a side", {}, 10),
                           ("enter next open instead of the close", {"entry": "open"}, 3),
                           ("2 down closes", {"n_down": 2}, 3), ("4 down closes", {"n_down": 4}, 3),
                           ("SMA100 trend filter", {"ma": 100}, 3), ("SMA50 trend filter", {"ma": 50}, 3),
                           ("exit close > 5-day average", {"exit_rule": "ma5"}, 3),
                           ("with a 10% catastrophic stop", {"stop": 0.10}, 3),
                           ("no trend filter (SMA1)", {"ma": 1}, 3)]:
        B.COST = cost
        B.report(f"{which}: {name}", B.run(data, make(**kw)))
    B.COST = 3
