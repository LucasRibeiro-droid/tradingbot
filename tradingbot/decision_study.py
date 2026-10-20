"""Test the decision process, and what each indicator adds to it, judged by target before stop.

Runs the harness on every candle and follows each decision exactly. Repeats with one
indicator added or removed from ``DecisionParams.confluences`` at a time (H12), and with the
fair value gap continuation path alone and together with the reversal path. Results are in R:
+reward/risk for a target, -1 for a stop. Expectancy (average R) is what matters.

Usage:
    python -m tradingbot.decision_study SPY --htf 1Day --ltf 1Hour --days 730
"""
from __future__ import annotations

import argparse
import json
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Sequence

from .candles import Candle
from .config import BASELINE, Config, to_dict
from .decision import Continuation, decide, simulate
from .liquidity import scan
from .trend import state_at, trend_series

JOURNAL_DIR = Path(__file__).resolve().parent.parent / "journal" / "studies"
# Each variant changes the baseline's confluences by exactly one indicator.
INDICATORS = ("liquidity_swept",)


def variants(config: Config) -> dict[str, Config]:
    base = config.decision.confluences
    out = {"baseline " + ("+".join(base) or "(break of structure only)"): config}
    for name in INDICATORS:
        changed = tuple(x for x in base if x != name) if name in base else base + (name,)
        label = ("without " if name in base else "with ") + name
        out[label] = replace(config, decision=replace(config.decision, confluences=changed),
                             version=f"{config.version}+confluences={'+'.join(changed) or 'none'}")
    return out


def run(ltf: Sequence[Candle], htf: Sequence[Candle], htf_length: timedelta, config: Config,
        paths: tuple[str, ...] = ("reversal",)) -> dict:
    """Run the harness. ``paths``: "reversal" (liquidity sweep + break, Days 6-12) and/or
    "continuation" (higher-timeframe fair value gap + lower-timeframe break, Days 14-18)."""
    states = trend_series(ltf, config.trend)
    htf_states = trend_series(htf, config.trend)
    scanned = scan(ltf, config.liquidity)
    cont = Continuation(htf, htf_length, config) if "continuation" in paths else None
    trades = []
    j, current = 0, None
    for i, c in enumerate(ltf):
        while j < len(htf) and state_at(htf[j:j + 1], htf_states[j:j + 1], htf_length, c.t) is not None:
            current = htf_states[j]
            j += 1
        dec = decide(ltf, states, scanned, i, current, config) if "reversal" in paths else None
        if cont is not None:
            cdec = cont.step(ltf, states, scanned, i, current)
            dec = dec or cdec
        if dec is None:
            continue
        out = simulate(ltf, dec, config.decision.max_hold_bars)
        if out is not None:
            trades.append({"t": c.t, "direction": dec.direction, "entry": dec.entry, "stop": dec.stop,
                           "target": dec.target, "rr": round(dec.reward_to_risk, 3),
                           "reasons": list(dec.reasons), **out})
    rs = [t["r"] for t in trades]
    summary = {"n": len(trades)}
    if trades:
        summary.update(win_rate=round(sum(t["exit"] == "target" for t in trades) / len(trades), 3),
                       avg_r=round(sum(rs) / len(rs), 3), total_r=round(sum(rs), 2),
                       median_rr=round(sorted(t["rr"] for t in trades)[len(trades) // 2], 2))
    return {"config": to_dict(config), "summary": summary, "trades": trades}


def main() -> None:
    from .data import fetch_bars, timeframe_length

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("symbol")
    ap.add_argument("--htf", default="1Day")
    ap.add_argument("--ltf", default="1Hour")
    ap.add_argument("--days", type=int, default=730)
    args = ap.parse_args()
    start = datetime.now(timezone.utc) - timedelta(days=args.days)
    htf = fetch_bars(args.symbol, args.htf, start - timeframe_length(args.htf) * 60)
    ltf = fetch_bars(args.symbol, args.ltf, start)

    print(f"\n{args.symbol} {args.ltf} inside {args.htf}")
    print(f"{'variant':44} {'n':>5} {'win':>6} {'avg R':>7} {'total R':>8} {'med RR':>7}")
    results = {}
    runs = [(label, config, ("reversal",)) for label, config in variants(BASELINE).items()]
    runs += [("continuation (fair value gaps) only", BASELINE, ("continuation",)),
             ("reversal + continuation", BASELINE, ("reversal", "continuation"))]
    for label, config, paths in runs:
        r = run(ltf, htf, timeframe_length(args.htf), config, paths)
        results[label] = r
        s = r["summary"]
        if s["n"]:
            print(f"{label:44} {s['n']:>5} {s['win_rate']:>6.1%} {s['avg_r']:>+7.2f} {s['total_r']:>+8.1f} {s['median_rr']:>7.2f}")
        else:
            print(f"{label:44} {0:>5}")
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = JOURNAL_DIR / f"decision_{args.symbol}_{args.ltf}_in_{args.htf}_{stamp}.json"
    path.write_text(json.dumps({"symbol": args.symbol, "htf": args.htf, "ltf": args.ltf, "variants": results}, indent=1))


if __name__ == "__main__":
    main()
