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
from .broker import Paper  # noqa: F401 (kept for callers)
from .lab import Signal, follow
from .signals import NY

ROOT = Path(__file__).resolve().parent.parent.parent / "journal" / "trading"
EXITS_R = {"1R": [1], "2R": [2], "ladder_0.5_1_2R": [0.5, 1, 2], "ladder_1_2_3R": [1, 2, 3]}


def day_trades(day: str) -> list[dict]:
    return json.loads((ROOT / f"state_{day}.json").read_text())["trades"]


TIMEFRAME = {"1m": "1Min", "5m": "5Min", "15m": "15Min", "1h": "1Hour"}


def timeframe_of(strategy: str) -> str:
    """The candles a playbook trades on (tjr_m<model>_<tf>; the breakout and old ids: 15-minute)."""
    if strategy.startswith("crt"):
        return "5Min"
    return TIMEFRAME.get(strategy.rsplit("_", 1)[-1], "15Min") if strategy.startswith("tjr_m") else "15Min"


def analyse(t: dict, exit_rec: dict | None, broker: Paper | None = None) -> dict:
    """``exit_rec``: the bot's exit record (trades.jsonl) with the realized fills."""
    d, entry, stop = t["direction"], t["entry_fill"], t["stop"]
    risk = abs(entry - stop)
    tf = timeframe_of(t.get("strategy", "tjr_m1"))
    minutes = {"1Min": 1, "5Min": 5, "15Min": 15, "1Hour": 60}[tf]
    exits = [tuple(x) for x in (exit_rec or {}).get("exits", [])]
    qty = sum(q for _, q, _ in exits)
    pnl = (exit_rec or {}).get("pnl")
    stop_exits = [(px, q) for px, q, kind in exits if kind in ("stop", "stop_limit")]
    entry_slip_bps = (t["planned_entry"] - entry) * d / t["planned_entry"] * 1e4  # + = better than the signal
    stop_slip_bps = (sum((px - stop) * q * d for px, q in stop_exits) / sum(q for _, q in stop_exits) / stop * 1e4
                     if stop_exits else None)
    start = datetime.fromisoformat(t["setup_t"].replace("Z", "+00:00"))
    bars = [c for c in fetch_bars(t["symbol"], tf, start - timedelta(days=1), start + timedelta(days=1)) if c.closed]
    i = next(k for k, c in enumerate(bars) if c.t.replace("Z", "") >= t["setup_t"].replace("Z", ""))
    sig = Signal(t["symbol"], t.get("strategy", "tjr_m1"), i, bars[i].t, d, entry, stop, t["targets"], {})
    planned = follow(bars, sig, t["targets"], True, bar_minutes=minutes)
    others = {name: round(follow(bars, sig, [entry + d * k * risk for k in rs], True, bar_minutes=minutes)["r"], 2)
              for name, rs in EXITS_R.items()}
    others["hold_to_close"] = round(follow(bars, sig, [], False, bar_minutes=minutes)["r"], 2)
    return {
        "symbol": t["symbol"], "direction": "long" if d == 1 else "short", "setup_t": t["setup_t"],
        "strategy": t.get("strategy", "tjr_m1"), "exit": t.get("exit_name", "tjr_ladder"), "timeframe": tf,
        "entry": round(entry, 4), "stop": stop, "risk_pct": round(risk / entry * 100, 3), "targets": t["targets"], "qty": qty,
        "pnl": pnl, "r": (exit_rec or {}).get("r"), "exits": exits,
        "entry_slippage_bps": round(entry_slip_bps, 1), "stop_slippage_bps": round(stop_slip_bps, 1) if stop_slip_bps is not None else None,
        "entry_slippage_r": round((t["planned_entry"] - entry) * d / risk, 3),
        "mfe_r": round(planned["mfe"], 2), "mae_r": round(planned["mae"], 2),
        "as_planned_r": round(planned["r"], 2), "as_planned_exit": planned["exit"],
        "other_exits_r": others, "direction_right": planned["mfe"] > planned["mae"],
        "time_ny": datetime.fromisoformat(t["setup_t"].replace("Z", "+00:00")).astimezone(NY).strftime("%H:%M"),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("day")
    args = ap.parse_args()
    exits = {}
    for line in (ROOT / "trades.jsonl").read_text().splitlines():
        r = json.loads(line)
        if r.get("type") in ("exit", "exit_correction"):
            exits[(r["symbol"], r["setup_t"])] = r  # a correction replaces the original
    for t in day_trades(args.day):
        if t.get("entry_fill"):
            print(json.dumps(analyse(t, exits.get((t["symbol"], t["setup_t"])))))


if __name__ == "__main__":
    main()
