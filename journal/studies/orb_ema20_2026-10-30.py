"""Owner's opening-range breakout + 20-EMA pullback (2026-10-30), Nasdaq-100, 2021-01 .. 2026-10-29.

Rules as given:
1. The 9:30-10:00 New York 30-minute candle: mark its high and low.
2. On 10-minute candles from 10:00: the first candle that CLOSES above the high -> look to buy;
   below the low -> look to sell.
3. After that breakout candle, wait for a 10m candle to interact with the 20 EMA (10m, on closes):
   for longs its low reaches the EMA, for shorts its high reaches it.
4. Enter at the open of the very next 10m candle. Stop: the low (long) / high (short) of the previous
   candle, the one that touched the EMA. Target: the high of the day (long) / low of the day (short).

[Bot] choices the owner didn't specify:
- "Day" = the regular session from 9:30 NY; the high/low as of the touching candle's close.
- One trade a day. No entries after 15:50; anything open is closed at 16:00 NY.
- Skipped when the target or the stop is on the wrong side of the entry.
- Data: OANDA NAS100 CFD 1-minute bid/ask (the same index as NQ futures; no NQ futures history here).
  Two cost models: (a) OANDA's real spread + 0.5 pt slippage on stops + 0.12 pt a side;
  (b) NQ-futures-like: mid price +/- 1/2 tick (0.125 pt), 0.25 pt slippage on stops, 0.12 pt a side
  (~$2.40 a side per contract).
- A minute that reaches both the stop and the target counts as the stop.
"""
import sys
from collections import defaultdict
from datetime import datetime, timezone

import numpy as np

sys.path.insert(0, ".")
from tradingbot.learn import data
from tradingbot.learn.market import Market, date_of

INST = "NAS100_USD"
m = Market(INST, data.load(INST, datetime(2021, 1, 1, tzinfo=timezone.utc), datetime(2026, 10, 30, tzinfo=timezone.utc)))

# 10-minute candles on the clock (mid prices), with the 20 EMA on their closes
key = m.day.astype(np.int64) * 1000 + m.mins // 10
starts = np.r_[0, np.nonzero(np.diff(key))[0] + 1]
ends = np.r_[starts[1:] - 1, len(key) - 1]
B = dict(o=m.o[starts], h=np.maximum.reduceat(m.h, starts), l=np.minimum.reduceat(m.l, starts), c=m.c[ends],
         day=m.day[starts], mins=(m.mins[starts] // 10) * 10, first=starts, last=ends)
ema = np.empty(len(starts)); a = 2 / 21; ema[0] = B["c"][0]
for k in range(1, len(starts)):
    ema[k] = a * B["c"][k] + (1 - a) * ema[k - 1]
by_day = defaultdict(list)
for k in range(len(starts)):
    by_day[int(B["day"][k])].append(k)

COSTS = {"oanda": dict(half=None, slip=0.5, comm=0.12), "futures": dict(half=0.125, slip=0.25, comm=0.12)}


def px(i, side, kind, cost):
    """Price of a fill at minute i. kind: open/low/high on the side that trades."""
    c = COSTS[cost]
    if c["half"] is None:
        buy = {"open": m.ao, "high": m.ah, "low": m.al}[kind][i]
        sell = {"open": m.bo, "high": m.bh, "low": m.bl}[kind][i]
    else:
        mid = {"open": m.o, "high": m.h, "low": m.l}[kind][i]
        buy, sell = mid + c["half"], mid - c["half"]
    return buy if side == 1 else sell


def trade_day(d, cost):
    a = m.day_first[d]; b = m.day_last[d]
    mins = m.mins[a:b + 1]
    orr = np.nonzero((mins >= 930) & (mins < 960))[0]
    if len(orr) < 20:
        return None
    orh, orl = m.h[a + orr].max(), m.l[a + orr].min()
    bars = [k for k in by_day[d] if 960 <= B["mins"][k] < 1320]
    side, j0 = 0, None
    for n, k in enumerate(bars):
        if B["c"][k] > orh: side, j0 = 1, n; break
        if B["c"][k] < orl: side, j0 = -1, n; break
    if not side:
        return None
    c = COSTS[cost]
    for n in range(j0 + 1, len(bars) - 1):
        k = bars[n]
        touched = B["l"][k] <= ema[k] if side == 1 else B["h"][k] >= ema[k]
        if not touched:
            continue
        nxt = bars[n + 1]
        if B["mins"][nxt] >= 1550:
            return None
        rth = slice(a + orr[0], B["last"][k] + 1)
        target = m.h[rth].max() if side == 1 else m.l[rth].min()
        stop = B["l"][k] if side == 1 else B["h"][k]
        i0 = B["first"][nxt]
        fill = px(i0, side, "open", cost) + (c["slip"] if c["half"] is None else 0) * side
        if (target - fill) * side <= 0 or (fill - stop) * side <= 0:
            return dict(skip=True)
        risk = (fill - stop) * side
        close_i = a + np.nonzero(mins < 1320)[0][-1]
        for i in range(i0, close_i + 1):
            lo_ = px(i, -side, "low" if side == 1 else "high", cost)    # the exit side's worst price
            hi_ = px(i, -side, "high" if side == 1 else "low", cost)
            if (lo_ - stop) * side <= 0:
                ex = min(stop, px(i, -side, "open", cost)) if side == 1 else max(stop, px(i, -side, "open", cost))
                ex -= c["slip"] * side; how = "stop"; break
            if i > i0 and (hi_ - target) * side >= 0:
                ex, how = target, "target"; break
        else:
            ex, how = px(close_i, -side, "open", cost), "16:00 close"
        r = ((ex - fill) * side - 2 * c["comm"]) / risk
        return dict(skip=False, day=d, side=side, entry=m.when(i0), fill=fill, stop=stop, target=target,
                    rr=(target - fill) * side / risk, r=r, how=how, risk=risk, pts=(ex - fill) * side - 2 * c["comm"])
    return None


def report(rows, label):
    r = np.array([x["r"] for x in rows]); p = np.array([x["pts"] for x in rows])
    if not len(r):
        print(label, "no trades"); return
    hows = defaultdict(int)
    for x in rows: hows[x["how"]] += 1
    eq = np.cumsum(r)
    print(f"{label}: {len(r)} trades, won {(r > 0).sum()} lost {(r <= 0).sum()} ({(r > 0).mean():.1%}), "
          f"avg {r.mean():+.3f}R, total {r.sum():+.1f}R, {p.sum():+,.0f} pts (NQ $20/pt: ${p.sum() * 20:+,.0f} for 1 contract), "
          f"maxDD {(eq - np.maximum.accumulate(eq)).min():.1f}R, median stop {np.median([x['risk'] for x in rows]):.1f} pt, "
          f"median planned R:R {np.median([x['rr'] for x in rows]):.2f}, exits {dict(hows)}")


if __name__ == "__main__":
    days = [int(d) for d in m.days if "2021-01-04" <= date_of(int(d)) <= "2026-10-29"]
    for cost in ("futures", "oanda"):
        rows = [x for d in days if (x := trade_day(d, cost)) and not x["skip"]]
        print(f"\n=== costs: {cost} ===")
        report([x for x in rows if x["day"] in set(days[-100:])], "last 100 trading days")
        report(rows, "2021-01 .. 2026-10 (all)")
        for y in sorted({date_of(x["day"])[:4] for x in rows}):
            report([x for x in rows if date_of(x["day"]).startswith(y)], f"  {y}")
        for s, nm in ((1, "longs"), (-1, "shorts")):
            report([x for x in rows if x["side"] == s], f"  {nm}")
    print("\nlast 10 trades (futures costs):")
    rows = [x for d in days[-40:] if (x := trade_day(d, "futures")) and not x["skip"]]
    for x in rows[-10:]:
        print(f"  {x['entry']} {'long ' if x['side'] == 1 else 'short'} fill {x['fill']:.1f} stop {x['stop']:.1f} target {x['target']:.1f} "
              f"-> {x['how']}, {x['r']:+.2f}R ({x['pts']:+.1f} pt)")
