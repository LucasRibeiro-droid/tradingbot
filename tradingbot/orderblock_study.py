"""Day 22 homework, done by the bot: find every order block and see what price did with it.

Tests two things TJR states:
  1. Price retraces into the order block and continues in the new direction
     [Day 20, 04:37-06:09; Day 22, 05:12]: how often a block is entered before price closes
     beyond its far side, and whether price then goes past the move's extreme (same measure
     as the fair value gap study, so the two retracement tools can be compared, H22).
  2. Waiting for the retracement into the block gives a better reward-to-risk than entering
     on the break of structure [Day 22, 25:11-25:29; Day 20, 07:01-07:41] (H23). Both trades
     use the same stop, beyond the block ("above the order block itself if you want to play
     safe", Day 22, 23:21), and the same target, the draw on liquidity when the break closes
     [Day 12]. The break trade enters at the break's close; the block trade at the block's
     near edge, only if price comes back to it before the target. A block trade that never
     fills counts as 0R [Bot]. Results in R per block.

Usage:
    python -m tradingbot.orderblock_study SPY --timeframe 1Hour --days 365
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
from .fvg_study import continued
from .liquidity import draw, scan
from .orderblocks import find_blocks, follow_block
from .trend import trend_series

JOURNAL_DIR = Path(__file__).resolve().parent.parent / "journal" / "studies"


def block_trade(candles: Sequence[Candle], dec: Decision, near: float, max_bars: int) -> dict | None:
    """Wait up to ``max_bars`` for price to come back to ``near``; then follow the trade."""
    for j in range(dec.index + 1, min(len(candles), dec.index + 1 + max_bars)):
        c = candles[j]
        if not c.closed:
            return None
        reached_target = c.h >= dec.target if dec.direction == 1 else c.l <= dec.target
        filled = c.l <= near if dec.direction == 1 else c.h >= near
        if filled:
            fill = Decision(j, dec.direction, near, dec.stop, dec.target, dec.reasons)
            rr = round(fill.reward_to_risk, 3)
            if (c.l <= dec.stop) if dec.direction == 1 else (c.h >= dec.stop):
                return {"r": -1.0, "exit": "stop", "bars": 0, "rr": rr}
            res = simulate(candles, fill, max_bars)
            return res and {**res, "rr": rr}
        if reached_target:
            return {"r": 0.0, "exit": "missed", "bars": j - dec.index}
    return {"r": 0.0, "exit": "missed", "bars": max_bars} if dec.index + max_bars < len(candles) else None


def run(candles: Sequence[Candle], config=BASELINE) -> dict:
    states = trend_series(candles, config.trend)
    scanned = scan(candles, config.liquidity)
    blocks = find_blocks(candles, states, [t for t, _ in scanned], config.trend, config.liquidity)
    max_bars = config.decision.max_hold_bars
    rows = []
    for b in blocks:
        i = b.confirmed_at
        direction = 1 if b.side == BULLISH else -1
        near, far = (b.top, b.bottom) if direction == 1 else (b.bottom, b.top)
        row = {"t": candles[b.sweep].t, "side": b.side, "top": b.top, "bottom": b.bottom,
               "leg_candles": b.sweep - b.start + 1}
        ev = follow_block(candles, b)
        row["entered"] = ev.entered_at is not None and (ev.broken_at is None or ev.entered_at <= ev.broken_at)
        if row["entered"]:
            leg = candles[i:ev.entered_at + 1]
            extreme = max(c.h for c in leg) if direction == 1 else min(c.l for c in leg)
            row["continued"] = continued(candles, b.side, ev.entered_at + 1, extreme, far)
        target = draw(scanned[i][1], direction, candles[i].c)
        entry = candles[i].c
        if target is not None and (entry - far) * direction > 0:
            dec = Decision(i, direction, entry, far, target, ("order_block",))
            row["bos"] = simulate(candles, dec, max_bars)
            if row["bos"]:
                row["bos"]["rr"] = round(dec.reward_to_risk, 3)
            ob_entry = near if (near - entry) * direction < 0 else entry
            row["block"] = block_trade(candles, dec, ob_entry, max_bars)
        rows.append(row)

    def avg(xs):
        return round(sum(xs) / len(xs), 3) if xs else None

    traded = [r for r in rows if r.get("bos") and r.get("block")]
    cont = [r["continued"] for r in rows if r.get("continued") is not None]
    filled = [r["block"] for r in traded if r["block"]["exit"] != "missed"]
    summary = {
        "blocks": len(rows),
        "entered_before_broken": sum(r["entered"] for r in rows),
        "continued_after_entry": avg([float(x) for x in cont]), "n_continued": len(cont),
        "trades": len(traded),
        "bos_avg_r": avg([r["bos"]["r"] for r in traded]),
        "bos_median_rr": median([r["bos"]["rr"] for r in traded]) if traded else None,
        "block_filled": len(filled),
        "block_avg_r_per_block": avg([r["block"]["r"] for r in traded]),
        "block_avg_r_when_filled": avg([x["r"] for x in filled]),
        "block_median_rr": median([x["rr"] for x in filled]) if filled else None,
        "median_leg_candles": median([r["leg_candles"] for r in rows]) if rows else None,
    }
    return {"config": to_dict(config), "summary": summary, "blocks": rows}


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
    for k, v in result["summary"].items():
        print(f"  {k:26} {v}")
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = JOURNAL_DIR / f"day22_orderblocks_{args.symbol}_{args.timeframe}_{stamp}.json"
    path.write_text(json.dumps({"symbol": args.symbol, "timeframe": args.timeframe, **result}, indent=1))


if __name__ == "__main__":
    main()
