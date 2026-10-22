"""Numbers for the after-close review of one day's trades (the judgement stays with the reviewer).

For each trade in state_<date>.json: fills and exits from Alpaca, result in R and $, costs
(entry slippage vs the signal price, exit slippage vs the stop or target), MFE/MAE in R from
15-minute bars, the result "as planned" (held until the 15:55 ET flatten), what the other exit
methods would have given on the same entry, and whether the expected direction happened.

    python -m tradingbot.live.review 2026-10-22
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ..data import fetch_bars
from .broker import Paper
from .lab import Signal, follow
from .signals import NY

ROOT = Path(__file__).resolve().parent.parent.parent / "journal" / "trading"
EXITS_R = {"1R": [1], "2R": [2], "ladder_0.5_1_2R": [0.5, 1, 2], "ladder_1_2_3R": [1, 2, 3]}


def day_trades(day: str) -> list[dict]:
    return json.loads((ROOT / f"state_{day}.json").read_text())["trades"]


def analyse(t: dict, broker: Paper) -> dict:
    d, entry, stop = t["direction"], t["entry_fill"], t["stop"]
    risk = abs(entry - stop)
    orders = [broker.order(p["order_id"]) for p in t["parts"]]
    exits = []
    for o in orders:
        for leg in o.get("legs") or []:
            if leg["status"] == "filled":
                exits.append((float(leg["filled_avg_price"]), float(leg["filled_qty"]), leg["type"],
                              float(leg.get("stop_price") or leg.get("limit_price"))))
    qty = sum(q for _, q, _, _ in exits)
    pnl = sum((px - entry) * q * d for px, q, _, _ in exits)
    exit_slip = sum((px - ref) * q * d for px, q, _, ref in exits)  # negative = worse than planned
    entry_slip = (entry - t["planned_entry"]) * d * -1  # negative = filled worse than the signal
    start = datetime.fromisoformat(t["setup_t"].replace("Z", "+00:00"))
    ltf = [c for c in fetch_bars(t["symbol"], "15Min", start - timedelta(days=1), start + timedelta(days=1)) if c.closed]
    i = next(k for k, c in enumerate(ltf) if c.t.replace("Z", "") >= t["setup_t"].replace("Z", ""))
    sig = Signal(t["symbol"], t.get("strategy", "tjr_m1"), i, ltf[i].t, d, entry, stop, t["targets"], {})
    planned = follow(ltf, sig, t["targets"], True)
    others = {name: round(follow(ltf, sig, [entry + d * k * risk for k in rs], True)["r"], 2) for name, rs in EXITS_R.items()}
    others["hold_to_close"] = round(follow(ltf, sig, [], False)["r"], 2)
    return {
        "symbol": t["symbol"], "direction": "long" if d == 1 else "short", "setup_t": t["setup_t"],
        "strategy": t.get("strategy", "tjr_m1"), "exit": t.get("exit_name", "tjr_ladder"),
        "entry": round(entry, 4), "stop": stop, "targets": t["targets"], "qty": qty,
        "pnl": round(pnl, 2), "r": round(pnl / (risk * qty), 3) if qty else None,
        "entry_slippage_r": round(entry_slip / risk, 3), "exit_slippage_r": round(exit_slip / (risk * qty), 3) if qty else None,
        "exits": [(px, q, kind) for px, q, kind, _ in exits],
        "mfe_r": round(planned["mfe"], 2), "mae_r": round(planned["mae"], 2),
        "as_planned_r": round(planned["r"], 2), "as_planned_exit": planned["exit"],
        "other_exits_r": others, "direction_right": planned["mfe"] > planned["mae"],
        "time_ny": datetime.fromisoformat(t["setup_t"].replace("Z", "+00:00")).astimezone(NY).strftime("%H:%M"),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("day")
    args = ap.parse_args()
    broker = Paper()
    broker.connect()
    for t in day_trades(args.day):
        if t.get("entry_fill"):
            print(json.dumps(analyse(t, broker)))


if __name__ == "__main__":
    main()
