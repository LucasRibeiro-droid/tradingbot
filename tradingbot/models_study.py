"""Days 30-33 homework, done by the bot: TJR's four entry models on the same setups.

Every setup is a liquidity sweep + break of structure (the order block's leg took liquidity,
then structure broke; `orderblocks.find_blocks`). From each setup, the four ways to enter
[TJR Day 30, 03:12-06:45; Days 32, 33]:
  1. at the break of structure's close ("this is an execution point", Day 32, 05:02)
  2. when price comes back into the order block, on the touch ("not on the break of
     structure ... we're executing when it comes into the order block", Day 32, 11:19)
  3. when price fills a fair value gap in the new direction and reacts: a candle closing in
     the trade's direction inside it (Day 33, 09:41: "what are we waiting for? Some sort of
     reaction"; Day 16, 08:09). TJR also scales down for a break; one timeframe here [Bot].
  4. as 2 or 3, but only inside the discount of the swing (equilibrium, Day 33, 14:47-15:18)
All four share the stop beyond the sweep ("stops above the highs", Day 30, 04:35) and the
target, the nearest liquidity when the break closes [Day 12]. A model that doesn't get its
entry before the target, the stop or ``max_hold_bars`` takes no trade: 0R [Bot].
TJR ranks them from most risky (1) to safest (4) [Day 30, 05:50] (H29).

With ``--bias``, each setup is also labelled by the daily bias when its break closes: the
direction of the last daily break of structure ("what is the daily market structure? We get
a break of structure to the downside, so I'm bearish on the daily", Day 34, 02:04-02:27).
TJR: setups against it are "short-lived" (Day 33, 23:27; Day 34, 00:31) (H30).
With ``--bias`` the 4-hour trend is read too: "aligned" = the daily and the 4-hour both agree
with the setup ("the S&P looks great for longs today ... the hourly's in an uptrend, the four
hour's in an uptrend, the daily is in an uptrend", Day 35, 13:09-13:19) (H32).
"Located" = with the daily bias AND the setup's sweep happened in the daily discount (a long
below the 50% of the daily swing, a short above it): "that's like the bare minimum that I look
for for retracements: is it even in a discount" (Day 36, 11:22-11:27) (H33).

With ``--exits``, each model's trade is also followed out with TJR's exits (Days 37, 38;
`exits.py`): three take profits, the first the next higher-timeframe draw on liquidity at
least 1:1, then building blocks; equal thirds; stop to break even after the first. The
entries are identical, so the only change is the exit (H19).

Usage:
    python -m tradingbot.models_study SPY --timeframe 1Hour --days 365
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import median
from typing import Sequence

from .candles import BULLISH, Candle
from .config import BASELINE, to_dict
from .decision import Decision, simulate
from .equilibrium import ranges
from .exits import simulate_partials, take_profits
from .fvg import find_gaps
from .liquidity import draw, scan
from .orderblocks import find_blocks
from .trend import NONE, state_at, trend_series

JOURNAL_DIR = Path(__file__).resolve().parent.parent / "journal" / "studies"


def _valid(direction: int, entry: float, stop: float, target: float) -> bool:
    return (entry - stop) * direction > 0 and (target - entry) * direction > 0


def _entry(candles, setup: Decision, until: int, entry_at) -> tuple[int, float] | str:
    """Walk forward from the break until ``entry_at(j)`` gives an entry price: (j, price).
    "missed" if the target is reached first, "no_entry" if the stop is or time runs out."""
    d = setup.direction
    for j in range(setup.index + 1, min(len(candles), until)):
        c = candles[j]
        price = entry_at(j)
        if price is not None and _valid(d, price, setup.stop, setup.target):
            return j, price
        if (c.h >= setup.target) if d == 1 else (c.l <= setup.target):
            return "missed"
        if (c.l <= setup.stop) if d == 1 else (c.h >= setup.stop):
            return "no_entry"
    return "no_entry"


def _single(candles, setup: Decision, entry, touch: bool, max_bars: int) -> dict | None:
    """The bot's exit until Day 37: all at the nearest liquidity, or the stop."""
    if isinstance(entry, str):
        return {"r": 0.0, "exit": entry}
    j, price = entry
    dec = Decision(j, setup.direction, price, setup.stop, setup.target, setup.reasons)
    rr = round(dec.reward_to_risk, 3)
    if touch and ((candles[j].l <= setup.stop) if setup.direction == 1 else (candles[j].h >= setup.stop)):
        return {"r": -1.0, "exit": "stop", "bars": 0, "rr": rr}
    res = simulate(candles, dec, max_bars)
    return res and {**res, "rr": rr}


def run(candles: Sequence[Candle], config=BASELINE, daily: Sequence[Candle] | None = None,
        four_hour: Sequence[Candle] | None = None, htf: Sequence[Candle] | None = None,
        htf_length: timedelta | None = None) -> dict:
    states = trend_series(candles, config.trend)
    scanned = scan(candles, config.liquidity)
    eq = ranges(candles, states)
    gaps = find_gaps(candles)
    wait = config.decision.max_hold_bars
    if daily is not None:
        daily_states = trend_series(daily, config.trend)
        daily_eq = ranges(daily, daily_states)
    if four_hour is not None:
        h4_states = trend_series(four_hour, config.trend)
    if htf is not None:
        htf_scanned = scan(htf, config.liquidity)
    max_bars = config.decision.max_hold_bars
    rows = []
    for b in find_blocks(candles, states, [t for t, _ in scanned], config.trend, config.liquidity):
        i, d = b.confirmed_at, (1 if b.side == BULLISH else -1)
        near, far = (b.top, b.bottom) if d == 1 else (b.bottom, b.top)
        # Already inside the block when structure breaks: the entry is there ("your break of
        # structure candle, it's right here; this is where you're going to want to enter
        # anyways", Day 32, 16:01). A limit order can't buy above (sell below) the market.
        near = min(near, candles[i].c) if d == 1 else max(near, candles[i].c)
        target = draw(scanned[i][1], d, candles[i].c)
        if target is None or not _valid(d, candles[i].c, far, target):
            continue
        setup = Decision(i, d, candles[i].c, far, target, ("sweep", "break of structure"))
        own = [g for g in gaps if g.side == b.side and g.index >= b.sweep]

        def gap_entry(j, own=own):
            c = candles[j]
            for g in own:
                if g.confirmed_at >= j:
                    continue
                broken = any((x.c < g.bottom) if d == 1 else (x.c > g.top) for x in candles[g.confirmed_at + 1:j + 1])
                if not broken and c.l <= g.top and c.h >= g.bottom and c.direction == b.side:
                    return c.c
            return None

        def block_entry(j):
            c = candles[j]
            touched = c.l <= near if d == 1 else c.h >= near
            return near if touched else None

        def in_discount(j, price):
            r = eq[j - 1]
            return r is not None and r.direction == d and r.depth(price) >= 0.5

        def model4(j):
            for p in (block_entry(j), gap_entry(j)):
                if p is not None and in_discount(j, p):
                    return p
            return None

        out = {"t": candles[i].t, "side": b.side}
        if daily is not None:
            ds = state_at(daily, daily_states, timedelta(days=1), candles[i].t)
            bias = ds.direction if ds else NONE
            out["bias"] = "none" if bias == NONE else "with" if bias == b.side else "against"
            k = _last_closed(daily, timedelta(days=1), candles[i].t)
            r = daily_eq[k] if k is not None else None
            sweep_price = candles[b.sweep].l if d == 1 else candles[b.sweep].h
            out["located"] = (bias == b.side and r is not None and r.direction == b.side
                              and r.depth(sweep_price) >= 0.5)
            if four_hour is not None:
                h4 = state_at(four_hour, h4_states, timedelta(hours=4), candles[i].t)
                out["aligned"] = bias == b.side and h4 is not None and h4.direction == b.side
        entries = {"1": ((i, candles[i].c), False),
                   "2": (_entry(candles, setup, i + 1 + wait, block_entry), True),
                   "3": (_entry(candles, setup, i + 1 + wait, gap_entry), False),
                   "4": (_entry(candles, setup, i + 1 + wait, model4), None)}
        for k, (e, touch) in entries.items():
            if k == "4" and not isinstance(e, str):  # model 4 entered on a touch if at the block
                touch = e[1] == near
            out[k] = _single(candles, setup, e, touch, max_bars)
            if htf is not None:
                out[k + "x"] = _tjr_exit(candles, scanned, gaps, htf, htf_scanned, htf_length, setup, e, touch, max_bars)
        if all(out[k] for k in ("1", "2", "3", "4") + (() if htf is None else ("1x", "2x", "3x", "4x"))):
            rows.append(out)

    def summarize(rows):
        return {k: _summary([r[k] for r in rows]) for k in "1234"}

    summary = summarize(rows)
    if htf is not None:
        summary.update({k + " TJR exits": _summary([r[k + "x"] for r in rows]) for k in "1234"})
    by_bias = {g: summarize([r for r in rows if r.get("bias") == g]) for g in ("with", "against")} if daily is not None else None
    if daily is not None:
        by_bias["daily bias + discount"] = summarize([r for r in rows if r.get("located")])
        by_bias["not located"] = summarize([r for r in rows if r.get("located") is False])
    if four_hour is not None:
        by_bias["daily+4h aligned"] = summarize([r for r in rows if r.get("aligned")])
        by_bias["not aligned"] = summarize([r for r in rows if r.get("aligned") is False])
    return {"config": to_dict(config), "summary": summary, "by_bias": by_bias, "setups": rows}


def _tjr_exit(candles, scanned, gaps, htf, htf_scanned, htf_length, setup: Decision, entry, touch, max_bars):
    """The same entry, followed out with TJR's exits (Days 37, 38; `exits.py`)."""
    if isinstance(entry, str):
        return {"r": 0.0, "exit": entry}
    j, price = entry
    d = setup.direction
    k = _last_closed(htf, htf_length, candles[j].t)
    htf_draws = [p.price for p in htf_scanned[k][1]] if k is not None else []
    ltf_pools = [p.price for p in scanned[j][1]]
    # Unfilled gaps beyond the entry: their near edge, where price is drawn to first [Bot].
    gap_edges = []
    for g in gaps:
        if g.confirmed_at >= j:
            continue
        edge = g.bottom if d == 1 else g.top
        traded = any(x.h >= g.bottom and x.l <= g.top for x in candles[g.confirmed_at + 1:j + 1])
        if not traded and (edge - price) * d > 0:
            gap_edges.append(edge)
    tps = take_profits(d, price, setup.stop, htf_draws, ltf_pools + gap_edges)
    if not tps:
        return {"r": 0.0, "exit": "no_target"}
    res = simulate_partials(candles, j, d, price, setup.stop, tps, max_bars, check_entry_candle=bool(touch))
    return res and {**res, "rr": round((tps[0] - price) * d / abs(price - setup.stop), 3), "tps": len(tps)}


def _last_closed(htf: Sequence[Candle], length: timedelta, when: str) -> int | None:
    """Index of the last higher-timeframe candle closed by ``when``."""
    from .trend import _ts
    t, k = _ts(when), None
    for j, c in enumerate(htf):
        if _ts(c.t) + length <= t:
            k = j
        else:
            break
    return k


def _summary(res: list[dict]) -> dict:
    taken = [x for x in res if x["exit"] not in ("missed", "no_entry", "no_target")]
    return {
        "setups": len(res), "trades": len(taken),
        # "win" = ended with a profit (a target, or break even after a target hit)
        "win_rate": round(sum(x["r"] > 0 for x in taken) / len(taken), 3) if taken else None,
        "avg_r_per_trade": round(sum(x["r"] for x in taken) / len(taken), 3) if taken else None,
        "avg_r_per_setup": round(sum(x["r"] for x in res) / len(res), 3) if res else None,
        "median_rr": median(x["rr"] for x in taken) if taken else None,
    }


def main() -> None:
    from .data import fetch_bars, timeframe_length

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("symbol")
    ap.add_argument("--timeframe", default="1Hour")
    ap.add_argument("--days", type=int, default=365)
    ap.add_argument("--bias", action="store_true", help="label setups by the daily bias (Day 34)")
    ap.add_argument("--exits", action="store_true", help="also follow every trade with TJR's exits (Days 37, 38)")
    args = ap.parse_args()
    start = datetime.now(timezone.utc) - timedelta(days=args.days)
    candles = fetch_bars(args.symbol, args.timeframe, start)
    daily = fetch_bars(args.symbol, "1Day", start - timedelta(days=120)) if args.bias else None
    four_hour = fetch_bars(args.symbol, "4Hour", start - timedelta(days=30)) if args.bias else None
    htf_tf = {"5Min": "15Min", "15Min": "1Hour", "1Hour": "4Hour", "4Hour": "1Day", "1Day": "1Week"}[args.timeframe]
    htf = fetch_bars(args.symbol, htf_tf, start - timedelta(days=120)) if args.exits else None
    result = run(candles, daily=daily, four_hour=four_hour, htf=htf,
                 htf_length=timeframe_length(htf_tf) if args.exits else None)
    print(f"\n{args.symbol} {args.timeframe}: {len(candles)} candles")
    print(f"{'model':6} {'setups':>7} {'trades':>7} {'win':>6} {'avg R/trade':>12} {'avg R/setup':>12} {'med RR':>7}")
    for k, s in result["summary"].items():
        f = lambda v, fmt: format(v, fmt) if v is not None else "-"
        print(f"{k:6} {s['setups']:>7} {s['trades']:>7} {f(s['win_rate'], '.1%'):>6} {f(s['avg_r_per_trade'], '+.2f'):>12} "
              f"{f(s['avg_r_per_setup'], '+.2f'):>12} {f(s['median_rr'], '.2f'):>7}")
    for g, summ in (result["by_bias"] or {}).items():
        print(f"  {g} the daily bias: " + "  ".join(
            f"m{k} n={s['trades']} win={s['win_rate'] if s['win_rate'] is None else format(s['win_rate'], '.0%')} "
            f"R={s['avg_r_per_trade'] if s['avg_r_per_trade'] is None else format(s['avg_r_per_trade'], '+.2f')}"
            for k, s in summ.items()))
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = JOURNAL_DIR / f"{'day37_exits' if args.exits else 'day34_bias' if args.bias else 'day33'}_models_{args.symbol}_{args.timeframe}_{stamp}.json"
    path.write_text(json.dumps({"symbol": args.symbol, "timeframe": args.timeframe, **result}, indent=1))


if __name__ == "__main__":
    main()
