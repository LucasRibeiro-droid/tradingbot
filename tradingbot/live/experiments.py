"""Live experiments (owner's directive, 2026-10-22): every trade tests a stated hypothesis.

A trade comes from an entry **strategy** and is managed by an **exit method**. Each strategy
has a set of exit methods under test; a trade gets one of them by a fixed hash of its own id
(an even, reproducible split, so the exits are compared on the same kind of entries). The
baseline (TJR model 1 with TJR's ladder) always stays in the mix as the reference.

Before entry each trade records its hypothesis, the prediction (with the lab's numbers for
that strategy and exit, and their uncertainty), what invalidates it, and the market context.
The after-close review fills in what happened against that prediction.
"""
from __future__ import annotations

import glob
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Sequence

from ..candles import Candle
from .signals import NY, _last_closed, _ny_minutes, _hhmm

STUDIES = Path(__file__).resolve().parent.parent.parent / "journal" / "studies"

# Hypotheses the live strategies and exits test (full text and status in journal/hypotheses.md).
HYPOTHESES = {
    "tjr_m1_15m": "H36: TJR's entry model 1 (sweep + break of structure, 15-minute) has positive expectancy on liquid US stocks (the baseline).",
    "orb30": "H39: momentum: the first 15-minute close beyond the 30-minute opening range continues in that direction for the rest of the day.",
    "tjr_ladder": "baseline exit: TJR's Day 37 ladder (first target the 1-hour draw on liquidity >= 1R, then building blocks; break even after the first).",
    "ladder_0.5_1_2R": "H38: the setups rarely reach 1R intraday (lab median MFE ~0.35R), so near targets (0.5R, 1R, 2R; break even after the first) do better than TJR's far ladder.",
    "ladder_1_2_3R": "H40: thirds at 1R, 2R, 3R with break even after the first capture momentum days better than a single target.",
    "2R": "H40 (control): everything at 2R, or at the close.",
    "crt_1h5m": "H57: the owner's CRT (1-hour setup, 5-minute fair value gap entry in the third candle) is profitable "
                "live on liquid US stocks (owner 2026-10-25: the only strategy traded this week).",
    "1:1 + 3R, fixed stop": "Owner's exit: half at 1:1, half at 3R, the stop fixed at the gap's middle candle until the end "
                            "(3R lost the least of 2/3/4/5R in the backtest, H56).",
}
# The backtest behind the live CRT (H56: 180 + 180 days, 1h -> 5m, SIP data, costs 3 bps a fill).
CRT_BACKTEST = ("Backtest (H56, 451 trades, 2 x 180 days): -0.56R per trade after costs, about 0R before costs, "
                "26% winners at 3R (about -0.2R if only stop exits pay costs, since entries and targets are limit orders); so this trade is expected to lose a little on average, and any single trade is "
                "close to a coin flip. Live tests whether the backtest's costs and fills hold.")


def hypothesis(strategy: str) -> str:
    if strategy.startswith("tjr_m") and "_" in strategy[5:]:
        model, tf = strategy[5:].split("_", 1)
        base = " (the baseline)" if strategy == "tjr_m1_15m" else ""
        return (f"H44: TJR's entry model {model} on the {tf} candles{base} has positive expectancy after costs "
                f"(owner 2026-10-23: trade TJR's fundamentals on every timeframe; H45 for model 2, H46 for model 3).")
    return HYPOTHESES.get(strategy, strategy)


def model_for(setup_key: str, models: Sequence[int]) -> int:
    """The TJR entry model a setup is traded with: a fixed, even split by the setup's id."""
    return models[int(hashlib.sha256(f"model:{setup_key}".encode()).hexdigest(), 16) % len(models)]


def exit_for(strategy: str, exits: Sequence[str], key: str) -> str:
    """The exit method this trade tests: a fixed, even split by the trade's id."""
    return exits[int(hashlib.sha256(f"{strategy}:{key}".encode()).hexdigest(), 16) % len(exits)]


def targets_for(exit_name: str, direction: int, entry: float, stop: float, ladder: Sequence[float]) -> list[float]:
    risk = abs(entry - stop)
    if exit_name == "tjr_ladder":
        return list(ladder)
    if exit_name.startswith("ladder_"):
        rs = [float(x) for x in exit_name[len("ladder_"):-1].split("_")]
    elif exit_name.endswith("R"):
        rs = [float(exit_name[:-1])]
    else:
        raise ValueError(f"unknown exit {exit_name!r}")
    return [round(entry + direction * k * risk, 2) for k in rs]


def lab_expectation(strategy: str, exit_name: str) -> dict | None:
    """The latest lab numbers for this strategy and exit (journal/studies/lab_*.json)."""
    for f in sorted(glob.glob(str(STUDIES / "lab_*.json")), key=lambda f: Path(f).stat().st_mtime, reverse=True):
        try:
            summary = json.loads(Path(f).read_text())["summary"]
        except (OSError, ValueError, KeyError):
            continue
        out = {}
        for period in ("in_sample", "out_of_sample"):
            s = summary.get(f"{strategy} | {exit_name} | {period}")
            if s and s.get("n"):
                out[period] = {k: s[k] for k in ("n", "avg_r", "win", "avg_win", "avg_loss")}
        if out:
            return out
    return None


def orb_assess(symbol: str, ltf: Sequence[Candle], shorting_enabled: bool, range_minutes: int = 30,
               last_entry: str = "12:00") -> dict | None:
    """[Bot] Opening-range breakout at the last closed 15-minute candle: the first close of the
    day beyond the first ``range_minutes``' range. Stop at the middle of the range."""
    i = _last_closed(ltf)
    if i is None:
        return None
    c = ltf[i]
    day = datetime.fromisoformat(c.t.replace("Z", "+00:00")).astimezone(NY).date()
    today = [j for j in range(i + 1)
             if datetime.fromisoformat(ltf[j].t.replace("Z", "+00:00")).astimezone(NY).date() == day]
    opening = [j for j in today if 570 <= _ny_minutes(ltf[j].t) < 570 + range_minutes]
    if len(opening) * 15 < range_minutes:
        return None
    hi, lo = max(ltf[j].h for j in opening), min(ltf[j].l for j in opening)
    after = [j for j in today if _ny_minutes(ltf[j].t) >= 570 + range_minutes]
    if not after or after[-1] != i:
        return None
    if any(ltf[j].c > hi or ltf[j].c < lo for j in after[:-1]):
        return None  # not the first breakout of the day
    d = 1 if c.c > hi else -1 if c.c < lo else 0
    if not d:
        return None
    mid = round((hi + lo) / 2, 2)
    reasons = []
    if _ny_minutes(c.t) + 15 > _hhmm(last_entry):
        reasons.append(f"breakout after {last_entry} ET (the hypothesis is about the morning)")
    if d == -1 and not shorting_enabled:
        reasons.append("short setup, but shorting is disabled on the account")
    return {
        "symbol": symbol, "t": c.t, "price": c.c, "strategy": "orb30",
        "context": {"ltf": "15Min", "opening_range": [hi, lo], "range_pct": round((hi - lo) / mid * 100, 2),
                    "bias_relation": "n/a"},
        "setup": f"[Bot] opening-range breakout {'up (long)' if d == 1 else 'down (short)'}: first 15-minute close "
                 f"beyond the {range_minutes}-minute range {lo:.2f}–{hi:.2f}",
        "present": [{"concept": "opening range", "evidence": f"high {hi:.2f}, low {lo:.2f} (09:30–{9 + (30 + range_minutes) // 60}:{(30 + range_minutes) % 60:02d} ET)"},
                    {"concept": "breakout", "evidence": f"close {c.c:.2f} {'above' if d == 1 else 'below'} the range, first today"}],
        "missing": [], "conflicts": [],
        "plan": {"direction": "long" if d == 1 else "short", "entry": c.c, "entry_condition": "market order on the breakout candle's close",
                 "stop": mid, "invalidation": f"back to the middle of the opening range ({mid:.2f})", "take_profits": []},
        "decision": "REJECTED" if reasons else "APPROVED", "reasons": reasons,
    }


def pre_trade(a: dict, exit_name: str) -> dict:
    """What the bot expects before entry, so the review can compare it with what happened."""
    strategy = a.get("strategy", "tjr_m1")
    p = a["plan"]
    lab = lab_expectation(strategy, exit_name)
    if strategy.startswith("crt"):
        expected = CRT_BACKTEST
    elif lab:
        parts = [f"{k.replace('_', ' ')}: {v['avg_r']:+.2f}R per trade, {v['win']:.0%} winners over {v['n']} trades"
                 for k, v in lab.items()]
        expected = "Lab (with costs): " + "; ".join(parts) + ". Any single trade is close to a coin flip around that."
    else:
        expected = "No lab numbers yet for this combination: the outcome is uncertain; this trade is exploratory."
    return {
        "strategy": strategy, "exit": exit_name,
        "hypothesis": hypothesis(strategy), "exit_hypothesis": HYPOTHESES.get(exit_name, exit_name),
        "expect": f"price moves {'up' if p['direction'] == 'long' else 'down'} from {p['entry']} toward the targets before "
                  f"reaching the stop {p['stop']}",
        "invalidation": p["invalidation"], "expected_outcome": expected, "lab": lab,
    }
