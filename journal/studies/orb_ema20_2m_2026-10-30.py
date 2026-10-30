"""Owner's opening-range breakout + 2-minute 20-EMA reclaim (2026-10-30, revised rules), Nasdaq-100, 2021-01 .. 2026-10-29.

1. Mark the high and low of the 9:30-10:00 New York 30-minute candle.
2. On 10-minute candles from 10:00: the first one that CLOSES above the high -> look to buy; below the low -> sell.
3. Then on 2-minute candles (20 EMA on 2m closes), from the end of that 10m candle: wait for price to interact
   with the EMA (long: a candle's low reaches it; short: its high) and reclaim it (a 2m candle that touched or
   went through the line closes back on the trade's side of it: above for longs, below for shorts).
4. Enter at the open of the next 2m candle. Target: the day's high (long) / low (short) as of the reclaim.
   Stop: the low (long) / high (short) of the previous candle = the reclaim candle. Variant "swing": the lowest
   low (highest high) since the first touch of the EMA.

[Bot] choices: "day" = from 9:30 NY; one trade a day; no entries from 15:50; closed at 16:00; skipped when the
target or the stop is on the wrong side of the entry. Costs as in orb_ema20_2026-10-30.py (NQ-futures-like
and OANDA). A minute that reaches both stop and target counts as the stop.
"""
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, ".")
from tradingbot.learn.market import date_of
import importlib.util
spec = importlib.util.spec_from_file_location("orb", "journal/studies/orb_ema20_2026-10-30.py")
orb = importlib.util.module_from_spec(spec); spec.loader.exec_module(orb)
m, px, COSTS, report = orb.m, orb.px, orb.COSTS, orb.report


def bars(n):
    key = m.day.astype(np.int64) * 10000 + m.mins // n
    st = np.r_[0, np.nonzero(np.diff(key))[0] + 1]
    en = np.r_[st[1:] - 1, len(key) - 1]
    b = dict(o=m.o[st], h=np.maximum.reduceat(m.h, st), l=np.minimum.reduceat(m.l, st), c=m.c[en],
             day=m.day[st], mins=(m.mins[st] // n) * n, first=st, last=en)
    e = np.empty(len(st)); a = 2 / 21; e[0] = b["c"][0]
    for k in range(1, len(st)):
        e[k] = a * b["c"][k] + (1 - a) * e[k - 1]
    b["ema"] = e
    idx = defaultdict(list)
    for k in range(len(st)):
        idx[int(b["day"][k])].append(k)
    b["by_day"] = idx
    return b


B10, B2 = bars(10), bars(2)


def trade_day(d, cost, stop_mode="prev", partial=False):
    a = m.day_first[d]
    mins = m.mins[a:m.day_last[d] + 1]
    orr = np.nonzero((mins >= 930) & (mins < 960))[0]
    if len(orr) < 20:
        return None
    orh, orl = m.h[a + orr].max(), m.l[a + orr].min()
    side, brk_end = 0, None
    for k in B10["by_day"][d]:
        if not 960 <= B10["mins"][k] < 1320:
            continue
        if B10["c"][k] > orh: side, brk_end = 1, B10["last"][k]; break
        if B10["c"][k] < orl: side, brk_end = -1, B10["last"][k]; break
    if not side:
        return None
    c = COSTS[cost]
    two = [k for k in B2["by_day"][d] if B2["first"][k] > brk_end and B2["mins"][k] < 1320]
    touched_at = None
    for n, k in enumerate(two[:-1]):
        e = B2["ema"][k]
        touch = B2["l"][k] <= e if side == 1 else B2["h"][k] >= e
        if touch and touched_at is None:
            touched_at = n
        if touched_at is None:
            continue
        reclaim = touch and (B2["c"][k] > e if side == 1 else B2["c"][k] < e) or \
                  (n > touched_at and (B2["c"][k] > e if side == 1 else B2["c"][k] < e) and
                   (B2["c"][two[n - 1]] <= B2["ema"][two[n - 1]] if side == 1 else B2["c"][two[n - 1]] >= B2["ema"][two[n - 1]]))
        if not reclaim:
            continue
        nxt = two[n + 1]
        if B2["mins"][nxt] >= 1550:
            return None
        rth = slice(a + orr[0], B2["last"][k] + 1)
        target = m.h[rth].max() if side == 1 else m.l[rth].min()
        if stop_mode == "prev":
            stop = B2["l"][k] if side == 1 else B2["h"][k]
        else:
            seg = two[touched_at:n + 1]
            stop = min(B2["l"][j] for j in seg) if side == 1 else max(B2["h"][j] for j in seg)
        i0 = B2["first"][nxt]
        fill = px(i0, side, "open", cost) + (c["slip"] if c["half"] is None else 0) * side
        if (target - fill) * side <= 0 or (fill - stop) * side <= 0:
            return dict(skip=True)
        risk = (fill - stop) * side
        close_i = a + np.nonzero(mins < 1320)[0][-1]
        # partial: half closed at 1:1, then the rest's stop moves to the entry (break even)
        legs, size, cur_stop, one_r = [], 1.0, stop, fill + side * risk
        for i in range(i0, close_i + 1):
            worst = px(i, -side, "low" if side == 1 else "high", cost)
            best = px(i, -side, "high" if side == 1 else "low", cost)
            if (worst - cur_stop) * side <= 0:
                o_ = px(i, -side, "open", cost)
                ex = (min(cur_stop, o_) if side == 1 else max(cur_stop, o_)) - c["slip"] * side
                legs.append((ex, size, "break even" if legs else "stop")); break
            if i > i0 and partial and not legs and (best - one_r) * side >= 0 and (target - one_r) * side > 0:
                legs.append((one_r, 0.5, "half at 1:1")); size, cur_stop = 0.5, fill
            if i > i0 and (best - target) * side >= 0:
                legs.append((target, size, "target")); break
        else:
            legs.append((px(close_i, -side, "open", cost), size, "16:00 close"))
        pts = sum((ex - fill) * side * w for ex, w, _ in legs) - 2 * c["comm"]
        how = " + ".join(h for _, _, h in legs)
        return dict(skip=False, day=d, side=side, entry=m.when(i0), fill=fill, stop=stop, target=target,
                    rr=(target - fill) * side / risk, r=pts / risk, how=how, risk=risk, pts=pts)
    return None


if __name__ == "__main__":
    days = [int(d) for d in m.days if "2021-01-04" <= date_of(int(d)) <= "2026-10-29"]
    last100 = set(days[-100:])
    for stop_mode, nm in (("prev", "stop = the reclaim candle's low/high"), ("swing", "stop = the pullback's low/high since the touch")):
        for cost in ("futures", "oanda"):
            rows = [x for d in days if (x := trade_day(d, cost, stop_mode)) and not x["skip"]]
            print(f"\n=== {nm} | costs: {cost} ===")
            report([x for x in rows if x["day"] in last100], "last 100 trading days")
            report(rows, "2021-01 .. 2026-10 (all)")
            if cost == "futures":
                for y in sorted({date_of(x["day"])[:4] for x in rows}):
                    report([x for x in rows if date_of(x["day"]).startswith(y)], f"  {y}")
                for s, sn in ((1, "longs"), (-1, "shorts")):
                    report([x for x in rows if x["side"] == s], f"  {sn}")
    print("\n=== half closed at 1:1, stop to break even, rest to the day's high/low (owner) | costs: futures ===")
    for stop_mode, nm in (("prev", "reclaim-candle stop"), ("swing", "pullback stop")):
        rows = [x for d in days if (x := trade_day(d, "futures", stop_mode, partial=True)) and not x["skip"]]
        report([x for x in rows if x["day"] in last100], f"{nm}, last 100 trading days")
        report(rows, f"{nm}, 2021-01 .. 2026-10 (all)")
        for y in sorted({date_of(x["day"])[:4] for x in rows}):
            report([x for x in rows if date_of(x["day"]).startswith(y)], f"  {y}")
        for s_, sn in ((1, "longs"), (-1, "shorts")):
            report([x for x in rows if x["side"] == s_], f"  {sn}")
    print("\nlast 10 trades (reclaim-candle stop, futures costs):")
    rows = [x for d in days[-30:] if (x := trade_day(d, "futures")) and not x["skip"]]
    for x in rows[-10:]:
        print(f"  {x['entry']} {'long ' if x['side'] == 1 else 'short'} fill {x['fill']:.1f} stop {x['stop']:.1f} target {x['target']:.1f} "
              f"-> {x['how']}, {x['r']:+.2f}R ({x['pts']:+.1f} pt)")
