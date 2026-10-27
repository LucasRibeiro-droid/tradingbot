"""CRT 1-hour -> 5-minute (the owner's rules, crt_owner) on OANDA's 24-hour markets: gold
(XAU_USD) and the Nasdaq-100 CFD (NAS100_USD, tracks NQ). Owner, 2026-10-27: "I only want you
to do this CRT strategy on NQ and XAUUSD".

Data: OANDA practice mid-price 5-minute candles. Costs: the measured median bid/ask spread,
half of it on every fill (``cost_bps``), and a variant with costs only on stop exits. Clock-hour
candles; the day for the previous day's high/low runs 18:00 -> 18:00 New York time.

    python -m tradingbot.live.crt_fx --days 180 --targets 2,3,4,5 --min-stop-pct 0.15
"""
from __future__ import annotations

import argparse
import gzip
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import median

from .crt_backtest import _ts
from .crt_owner import STUDIES, orders_for, simulate, summary
from .oanda import INSTRUMENTS, Practice

CACHE = Path.home() / ".cache" / "tradingbot"


def history(p: Practice, instrument: str, days: int):
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / f"oanda_{instrument}_5m_{days}d_{datetime.now(timezone.utc):%Y%m%d}.json"
    if f.exists():
        from ..candles import Candle
        return [Candle(*x) for x in json.loads(f.read_text())]
    bars = [c for c in p.candles(instrument, "5Min", datetime.now(timezone.utc) - timedelta(days=days)) if c.closed]
    f.write_text(json.dumps([[c.t, c.o, c.h, c.l, c.c, c.closed] for c in bars]))
    return bars


def spread_bps(p: Practice, instrument: str) -> float:
    """Median bid/ask spread over the last ~2 weeks of 5-minute candles, in bps of the price."""
    import urllib.parse
    q = urllib.parse.urlencode({"granularity": "M5", "price": "BA", "count": 4000})
    got = p._call("GET", f"/v3/instruments/{instrument}/candles?{q}")["candles"]
    return median((float(c["ask"]["c"]) - float(c["bid"]["c"])) / float(c["bid"]["c"]) * 1e4 for c in got)


def run(days: int, targets: list[float], min_stop_pct: float) -> tuple[dict, dict]:
    p = Practice()
    now = datetime.now(timezone.utc)
    split = now - timedelta(days=days)
    res = {r: [] for r in targets}
    counts, spreads = {}, {}
    for inst in INSTRUMENTS:
        bars = history(p, inst, 2 * days + 10)
        spreads[inst] = round(spread_bps(p, inst), 2)
        cost = spreads[inst] / 2  # half the spread on each fill
        orders, c = orders_for(inst, bars, min_stop_pct, round_the_clock=True)
        for k, v in c.items():
            counts[f"{inst} {k}"] = v
        for r in targets:
            for o in orders:
                t = simulate(bars, o, r, False, cost_bps=cost, fractional=True)
                if t and "skipped" not in t:
                    t["period"] = "recent" if _ts(o.setup_t) >= split else "earlier"
                    res[r].append(t)
        print(f"{inst}: {len(bars)} bars, spread {spreads[inst]} bps, {len(orders)} orders", flush=True)
    out = {"params": {"days_per_period": days, "min_stop_pct": min_stop_pct, "spread_bps": spreads, "fixed_stop": True,
                      "run_at": now.isoformat()}, "setup_counts": counts, "by_target": {}}
    for r, ts in res.items():
        out["by_target"][f"{r:g}R"] = {
            k: summary([t for t in ts if f(t)]) for k, f in {
                "all": lambda t: True, "recent": lambda t: t["period"] == "recent", "earlier": lambda t: t["period"] == "earlier",
                "XAU_USD": lambda t: t["symbol"] == "XAU_USD", "NAS100_USD": lambda t: t["symbol"] == "NAS100_USD",
                "long": lambda t: t["direction"] == "long", "short": lambda t: t["direction"] == "short"}.items()}
    return out, res


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=180)
    ap.add_argument("--targets", default="2,3,4,5")
    ap.add_argument("--min-stop-pct", type=float, default=0.0)
    args = ap.parse_args()
    out, res = run(args.days, [float(x) for x in args.targets.split(",")], args.min_stop_pct)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = STUDIES / f"crt_fx_5m_minstop{args.min_stop_pct:g}_{stamp}.json"
    path.write_text(json.dumps(out, indent=1))
    with gzip.open(path.with_suffix(".trades.jsonl.gz"), "wt") as f:
        for r, ts in res.items():
            f.writelines(json.dumps({**t, "target_r": r}) + "\n" for t in ts)
    for r, v in out["by_target"].items():
        print(r, {k: (s.get("trades"), s.get("expectancy_r"), s.get("expectancy_r_limit_costs"), s.get("win_rate")) for k, s in v.items()})
    print("saved", path)


if __name__ == "__main__":
    main()
