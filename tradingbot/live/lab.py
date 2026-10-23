"""Strategy lab: compare entry strategies and exit methods on the same history, with costs.

Each strategy produces signals (entry, stop, direction) using only data available at the
signal candle's close; each exit method then follows the signal through the same day and
closes what is left at the flatten time, as live does. Results are in R after costs, split
into the last ``days`` (in sample) and the ``days`` before (out of sample).

    python -m tradingbot.live.lab --days 120 --symbols SPY,NVDA,... [--cost-bps 3]

Bars are cached under ~/.cache/tradingbot (IEX, as live). Research only; nothing is traded.
"""
from __future__ import annotations

import argparse
import gzip
import json
import pickle
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean, median

from ..candles import Candle
from ..config import BASELINE
from ..data import fetch_bars, timeframe_length
from .signals import NY, assess_all

CACHE = Path.home() / ".cache" / "tradingbot"
STUDIES = Path(__file__).resolve().parent.parent.parent / "journal" / "studies"


def _ts(t: str) -> datetime:
    return datetime.fromisoformat(t.replace("Z", "+00:00"))


def _ny(t: str) -> datetime:
    return _ts(t).astimezone(NY)


def load(symbol: str, timeframe: str, days: int) -> list[Candle]:
    """Closed bars of the last ``days`` days, cached for the day."""
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"{symbol}_{timeframe}_{days}_{datetime.now(timezone.utc):%Y%m%d}.pkl"
    if path.exists():
        return pickle.loads(path.read_bytes())
    now = datetime.now(timezone.utc)
    bars = [c for c in fetch_bars(symbol, timeframe, now - timedelta(days=days), now) if c.closed]
    path.write_bytes(pickle.dumps(bars))
    return bars


@dataclass
class Signal:
    symbol: str
    strategy: str
    i: int  # index of the signal candle in the 15-minute bars
    t: str
    direction: int
    entry: float
    stop: float
    ladder: list[float]  # the strategy's own targets (may be empty)
    context: dict


def _session_minute(t: str) -> int:
    d = _ny(t)
    return d.hour * 60 + d.minute


# ---- entry strategies ----

TP_TIMEFRAME = {"1Min": "5Min", "5Min": "15Min", "15Min": "1Hour", "1Hour": "4Hour"}
SHORT = {"1Min": "1m", "5Min": "5m", "15Min": "15m", "1Hour": "1h"}


def tjr_models(symbol: str, ltf: list[Candle], htf: list[Candle], daily: list[Candle], first: datetime,
               tf: str = "15Min", models: tuple[int, ...] = (1, 2, 3), wait: int = 20) -> list[Signal]:
    """TJR's entry models 1-3 on any timeframe, exactly as live (signals.assess_all). Every
    model is evaluated on every setup here (live splits the setups between them)."""
    ltf_len, tp_len = timeframe_length(tf), timeframe_length(TP_TIMEFRAME[tf])
    out = []
    for i, c in enumerate(ltf):
        if _ts(c.t) < first:
            continue
        lo = max(0, i - 600)
        t_close = _ts(c.t) + ltf_len
        h = [x for x in htf if _ts(x.t) + tp_len <= t_close][-600:]
        dly = [x for x in daily if _ts(x.t) < t_close]
        for a in assess_all(symbol, ltf[lo:i + 1], h, dly, BASELINE, True, ltf_len, tp_len, models=models, wait=wait):
            if a["decision"] != "APPROVED":
                continue
            p = a["plan"]
            out.append(Signal(symbol, f"tjr_m{a['model']}_{SHORT[tf]}", i, c.t, 1 if p["direction"] == "long" else -1,
                              p["entry"], p["stop"], list(p["take_profits"]),
                              {"bias_relation": a["context"]["bias_relation"], "entry_type": p["entry_type"], "wait": wait}))
    return out


def opening_range_breakout(symbol: str, ltf: list[Candle], htf, daily, first: datetime,
                           range_minutes: int = 30, last_entry: str = "12:00") -> list[Signal]:
    """[Bot] Momentum: the first ``range_minutes`` set the opening range; the first 15-minute
    candle that closes beyond it (before ``last_entry`` ET) is the entry, in that direction;
    stop at the middle of the range. One signal per stock per day."""
    out, by_day = [], {}
    for i, c in enumerate(ltf):
        by_day.setdefault(_ny(c.t).date(), []).append(i)
    lh, lm = map(int, last_entry.split(":"))
    for day, idx in by_day.items():
        if _ts(ltf[idx[0]].t) < first:
            continue
        opening = [j for j in idx if 570 <= _session_minute(ltf[j].t) < 570 + range_minutes]
        if len(opening) * 15 < range_minutes:
            continue
        hi, lo = max(ltf[j].h for j in opening), min(ltf[j].l for j in opening)
        mid = (hi + lo) / 2
        for j in idx:
            m = _session_minute(ltf[j].t)
            if m < 570 + range_minutes or m + 15 > lh * 60 + lm:
                continue
            c = ltf[j]
            d = 1 if c.c > hi else -1 if c.c < lo else 0
            if d:
                out.append(Signal(symbol, "orb30", j, c.t, d, c.c, round(mid, 2), [],
                                  {"range": [hi, lo], "range_pct": round((hi - lo) / mid * 100, 2)}))
                break
    return out


STRATEGIES = {"tjr": tjr_models, "orb30": opening_range_breakout}


# ---- exits ----

def fill_limit(ltf: list[Candle], s: Signal, flatten: str = "15:55", bar_minutes: int = 15) -> Signal | None:
    """A limit entry (model 2): filled on the first later candle that trades through the limit,
    within ``wait`` candles and the same day (the flatten cancels it). None if never filled."""
    fh, fm = map(int, flatten.split(":"))
    day = _ny(s.t).date()
    for j in range(s.i + 1, min(len(ltf), s.i + 1 + s.context.get("wait", 20))):
        c, ny = ltf[j], _ny(ltf[j].t)
        if ny.date() != day or ny.hour * 60 + ny.minute + bar_minutes > fh * 60 + fm:
            return None
        if (c.l <= s.entry) if s.direction == 1 else (c.h >= s.entry):
            return Signal(s.symbol, s.strategy, j, c.t, s.direction, s.entry, s.stop, s.ladder, s.context)
    return None


def follow(ltf: list[Candle], s: Signal, targets: list[float], break_even: bool, flatten: str = "15:55",
           bar_minutes: int = 15, entry_candle: bool = False) -> dict:
    """Equal parts at each target (none = hold to the flatten); stop to break even after the
    first target if ``break_even``. R before costs, plus MFE/MAE in R until the exit."""
    risk = abs(s.entry - s.stop)
    d, day = s.direction, _ny(s.t).date()
    fh, fm = map(int, flatten.split(":"))
    part = 1 / len(targets) if targets else 1.0
    r, hit, stop, mfe, mae = 0.0, 0, s.stop, 0.0, 0.0
    last = s.entry
    if entry_candle:  # filled inside this candle (a limit): it can also reach the stop (counted first)
        c = ltf[s.i]
        if ((c.l if d == 1 else c.h) - stop) * d <= 0:
            return {"r": -1.0, "exit": "stop", "hit": 0, "mfe": 0.0, "mae": 1.0}
    for c in ltf[s.i + 1:]:
        ny = _ny(c.t)
        if ny.date() != day or ny.hour * 60 + ny.minute + bar_minutes > fh * 60 + fm:
            break
        last = c.c
        adverse = (c.l if d == 1 else c.h)
        favour = (c.h if d == 1 else c.l)
        if (adverse - stop) * d <= 0:  # stop first: conservative when both touch in one candle
            mae = max(mae, (s.entry - stop) * d / risk)
            r += (1 - part * hit) * (stop - s.entry) * d / risk
            return {"r": r, "exit": "stop" if hit == 0 else "break_even", "hit": hit, "mfe": mfe, "mae": mae}
        mfe = max(mfe, (favour - s.entry) * d / risk)
        mae = max(mae, (s.entry - adverse) * d / risk)
        while hit < len(targets) and (favour - targets[hit]) * d >= 0:
            r += part * (targets[hit] - s.entry) * d / risk
            hit += 1
            if break_even:
                stop = s.entry
        if targets and hit == len(targets):
            return {"r": r, "exit": "target", "hit": hit, "mfe": mfe, "mae": mae}
    r += (1 - part * hit) * (last - s.entry) * d / risk
    return {"r": r, "exit": "close", "hit": hit, "mfe": mfe, "mae": mae}


def exit_methods(s: Signal) -> dict[str, tuple[list[float], bool]]:
    risk = abs(s.entry - s.stop)
    at = lambda *rs: [s.entry + s.direction * k * risk for k in rs]
    out = {"hold_to_close": ([], False), "1R": (at(1), False), "1.5R": (at(1.5), False), "2R": (at(2), False),
           "ladder_1_2_3R": (at(1, 2, 3), True), "ladder_0.5_1_2R": (at(0.5, 1, 2), True)}
    if s.ladder:
        out["tjr_ladder"] = (s.ladder, True)
    return out


# ---- report ----

def summarize(rs: list[float]) -> dict:
    if not rs:
        return {"n": 0}
    eq, peak, dd = 0.0, 0.0, 0.0
    for x in rs:
        eq += x
        peak = max(peak, eq)
        dd = min(dd, eq - peak)
    wins = [x for x in rs if x > 0]
    losses = [x for x in rs if x <= 0]
    return {"n": len(rs), "avg_r": round(mean(rs), 3), "total_r": round(sum(rs), 1),
            "win": round(len(wins) / len(rs), 2), "avg_win": round(mean(wins), 2) if wins else None,
            "avg_loss": round(mean(losses), 2) if losses else None, "max_dd_r": round(dd, 1)}


def run(symbols: list[str], days: int, cost_bps: float, tf: str = "15Min", strategies: tuple[str, ...] = ("tjr", "orb30"),
        models: tuple[int, ...] = (1, 2, 3)) -> dict:
    now = datetime.now(timezone.utc)
    split, first = now - timedelta(days=days), now - timedelta(days=2 * days)
    bar_minutes = int(timeframe_length(tf).total_seconds() // 60)
    lead = {"1Min": 3, "5Min": 8, "15Min": 30, "1Hour": 80}[tf]  # history before the first signal
    rows, unfilled = [], {}
    for sym in symbols:
        try:
            ltf = load(sym, tf, 2 * days + lead)
            htf = load(sym, TP_TIMEFRAME[tf], 2 * days + lead * 3)
            daily = load(sym, "1Day", 2 * days + 240)
        except Exception as e:
            print(f"{sym}: data error {e}")
            continue
        for name in strategies:
            if name == "orb30" and tf != "15Min":
                continue
            sigs = tjr_models(sym, ltf, htf, daily, first, tf, models) if name == "tjr" else STRATEGIES[name](sym, ltf, htf, daily, first)
            for s in sigs:
                limit = s.context.get("entry_type") == "limit"
                if limit:
                    filled = fill_limit(ltf, s, bar_minutes=bar_minutes)
                    if filled is None:
                        unfilled[s.strategy] = unfilled.get(s.strategy, 0) + 1
                        continue
                    s = filled
                cost = 2 * cost_bps / 1e4 * s.entry / abs(s.entry - s.stop)
                period = "in_sample" if _ts(s.t) >= split else "out_of_sample"
                for ex, (targets, be) in exit_methods(s).items():
                    res = follow(ltf, s, targets, be, bar_minutes=bar_minutes, entry_candle=limit)
                    rows.append({"symbol": sym, "strategy": s.strategy, "exit": ex, "period": period, "t": s.t,
                                 "direction": s.direction, "r": round(res["r"] - cost, 3), "r_gross": round(res["r"], 3),
                                 "cost_r": round(cost, 3), "mfe": round(res["mfe"], 2), "mae": round(res["mae"], 2),
                                 "how": res["exit"], "context": s.context})
        print(f"{sym}: done", flush=True)
    table = {}
    for row in rows:
        table.setdefault((row["strategy"], row["exit"], row["period"]), []).append(row["r"])
    summary = {f"{k[0]} | {k[1]} | {k[2]}": summarize(v) for k, v in sorted(table.items())}
    mfe = {}
    for row in rows:
        if row["exit"] == "hold_to_close":
            mfe.setdefault(row["strategy"], []).append(row["mfe"])
    mfe_summary = {k: {"n": len(v), "median": round(median(v), 2),
                       "reach_0.5R": round(sum(x >= 0.5 for x in v) / len(v), 2),
                       "reach_1R": round(sum(x >= 1 for x in v) / len(v), 2),
                       "reach_2R": round(sum(x >= 2 for x in v) / len(v), 2)} for k, v in mfe.items()}
    return {"summary": summary, "mfe_hold_to_close": mfe_summary, "limit_not_filled": unfilled, "rows": rows,
            "params": {"symbols": symbols, "days": days, "timeframe": tf, "cost_bps_per_side": cost_bps, "run_at": now.isoformat()}}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=120)
    ap.add_argument("--symbols", required=True)
    ap.add_argument("--cost-bps", type=float, default=3.0, help="spread + slippage per side, basis points")
    ap.add_argument("--timeframe", default="15Min", choices=list(TP_TIMEFRAME))
    ap.add_argument("--strategies", default="tjr,orb30")
    ap.add_argument("--models", default="1,2,3")
    args = ap.parse_args()
    res = run(args.symbols.split(","), args.days, args.cost_bps, args.timeframe, tuple(args.strategies.split(",")),
              tuple(int(m) for m in args.models.split(",")))
    out = STUDIES / f"lab_{args.timeframe}_{args.days}d_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}.json"
    rows = res.pop("rows")
    res["rows_file"] = out.with_suffix(".rows.jsonl.gz").name  # every setup × exit, for breakdowns
    with gzip.open(out.with_suffix(".rows.jsonl.gz"), "wt") as f:
        f.writelines(json.dumps(r) + "\n" for r in rows)
    out.write_text(json.dumps(res, indent=1))
    for k, v in res["summary"].items():
        print(k, v)
    print("MFE (hold to close):", res["mfe_hold_to_close"])
    print("saved", out)


if __name__ == "__main__":
    main()
