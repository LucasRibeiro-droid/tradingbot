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
from .fvg import find_gaps
from .liquidity import draw, scan
from .orderblock_study import block_trade
from .orderblocks import find_blocks
from .trend import trend_series

JOURNAL_DIR = Path(__file__).resolve().parent.parent / "journal" / "studies"


def _valid(direction: int, entry: float, stop: float, target: float) -> bool:
    return (entry - stop) * direction > 0 and (target - entry) * direction > 0


def _wait(candles, setup: Decision, until: int, entry_at) -> dict:
    """Walk forward from the break until ``entry_at(j)`` gives an entry price, the target or
    the stop is reached first (no trade), or time runs out (no trade)."""
    d = setup.direction
    for j in range(setup.index + 1, min(len(candles), until)):
        c = candles[j]
        price = entry_at(j)
        if price is not None and _valid(d, price, setup.stop, setup.target):
            dec = Decision(j, d, price, setup.stop, setup.target, setup.reasons)
            res = simulate(candles, dec, BASELINE.decision.max_hold_bars)
            return res and {**res, "rr": round(dec.reward_to_risk, 3)}
        if (c.h >= setup.target) if d == 1 else (c.l <= setup.target):
            return {"r": 0.0, "exit": "missed"}
        if (c.l <= setup.stop) if d == 1 else (c.h >= setup.stop):
            return {"r": 0.0, "exit": "no_entry"}
    return {"r": 0.0, "exit": "no_entry"}


def run(candles: Sequence[Candle], config=BASELINE) -> dict:
    states = trend_series(candles, config.trend)
    scanned = scan(candles, config.liquidity)
    eq = ranges(candles, states)
    gaps = find_gaps(candles)
    wait = config.decision.max_hold_bars
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
        m1 = simulate(candles, setup, config.decision.max_hold_bars)
        out["1"] = m1 and {**m1, "rr": round(setup.reward_to_risk, 3)}
        out["2"] = block_trade(candles, setup, near, wait)
        out["3"] = _wait(candles, setup, i + 1 + wait, gap_entry)
        out["4"] = _wait(candles, setup, i + 1 + wait, model4)
        if all(out[k] for k in "1234"):
            rows.append(out)

    summary = {}
    for k in "1234":
        res = [r[k] for r in rows]
        taken = [x for x in res if x["exit"] not in ("missed", "no_entry")]
        summary[k] = {
            "setups": len(res), "trades": len(taken),
            "win_rate": round(sum(x["exit"] == "target" for x in taken) / len(taken), 3) if taken else None,
            "avg_r_per_trade": round(sum(x["r"] for x in taken) / len(taken), 3) if taken else None,
            "avg_r_per_setup": round(sum(x["r"] for x in res) / len(res), 3) if res else None,
            "median_rr": median(x["rr"] for x in taken) if taken else None,
        }
    return {"config": to_dict(config), "summary": summary, "setups": rows}


def main() -> None:
    from .data import fetch_bars

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("symbol")
    ap.add_argument("--timeframe", default="1Hour")
    ap.add_argument("--days", type=int, default=365)
    args = ap.parse_args()
    candles = fetch_bars(args.symbol, args.timeframe, datetime.now(timezone.utc) - timedelta(days=args.days))
    result = run(candles)
    print(f"\n{args.symbol} {args.timeframe}: {len(candles)} candles")
    print(f"{'model':6} {'setups':>7} {'trades':>7} {'win':>6} {'avg R/trade':>12} {'avg R/setup':>12} {'med RR':>7}")
    for k, s in result["summary"].items():
        f = lambda v, fmt: format(v, fmt) if v is not None else "-"
        print(f"{k:6} {s['setups']:>7} {s['trades']:>7} {f(s['win_rate'], '.1%'):>6} {f(s['avg_r_per_trade'], '+.2f'):>12} "
              f"{f(s['avg_r_per_setup'], '+.2f'):>12} {f(s['median_rr'], '.2f'):>7}")
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = JOURNAL_DIR / f"day33_models_{args.symbol}_{args.timeframe}_{stamp}.json"
    path.write_text(json.dumps({"symbol": args.symbol, "timeframe": args.timeframe, **result}, indent=1))


if __name__ == "__main__":
    main()
