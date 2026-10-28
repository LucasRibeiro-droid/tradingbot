"""Predicting the Nasdaq-100's high and low of the New York session (09:30-16:00 ET).
Owner, 2026-10-27: "find a way of PREDICTING the highs and lows of the day for nas100".

Two parts, both fit on QQQ 5-minute bars (SIP, 2016 onwards; QQQ tracks the Nasdaq-100):
  1. At the open: the session's range, and bands for the high and low (10%, 50%, 90%), from the
     last 1/5/22 sessions' ranges, the premarket range (04:00-09:30) and the opening gap.
     Out of sample (fit 2016-20, tested 2021-26): the range is predictable (correlation 0.66, 15%
     better than the 22-day average); which side extends is not (high/low errors ~45/54 bps, only
     ~7% better than half the average range). The 80% bands held 78-80% of the time.
  2. During the session (every 30 minutes): the probability that the high, and the low, of the
     day is already in, from the range so far vs the forecast, where price sits in it, how far it
     is from each extreme, the gap and the time left. Out of sample AUC 0.77-0.93; when it says
     80% or more it was right 86-98% of the time (2021-26 QQQ) and 79-100% on OANDA NAS100.

    python -m tradingbot.live.hl_predict --fit   # refit on all QQQ history -> hl_model.json
"""
from __future__ import annotations

import argparse
import json
import math
import pickle
from datetime import date, datetime
from pathlib import Path
from typing import Sequence

from ..candles import Candle
from .signals import NY

MODEL = Path(__file__).resolve().parent / "hl_model.json"
QQQ_CACHE = Path.home() / ".cache" / "tradingbot" / "qqq_5m_2016.pkl"
CHECKPOINTS = tuple(range(600, 960, 30))  # 10:00 ... 15:30 ET
OPEN_FEATURES = ("lr1", "lr5", "lr22", "lpm", "agap")
SIDE_FEATURES = ("lr1", "lr5", "lr22", "lpm", "agap", "gpos", "gneg")


def _minutes(t: str) -> tuple[date, int]:
    n = datetime.fromisoformat(t.replace("Z", "+00:00")).astimezone(NY)
    return n.date(), n.hour * 60 + n.minute


def sessions(bars: Sequence[Candle]) -> dict[date, dict]:
    """Per New York date: the session's open/high/low/close and the 04:00-09:30 premarket range."""
    out: dict[date, dict] = {}
    for c in bars:
        d, m = _minutes(c.t)
        s = out.setdefault(d, {"bars": [], "pm_h": None, "pm_l": None})
        if 240 <= m < 570:
            s["pm_h"] = c.h if s["pm_h"] is None else max(s["pm_h"], c.h)
            s["pm_l"] = c.l if s["pm_l"] is None else min(s["pm_l"], c.l)
        elif 570 <= m < 960:
            s["bars"].append((m, c))
    for s in out.values():
        b = s["bars"]
        if b:
            s.update(open=b[0][1].o, high=max(c.h for _, c in b), low=min(c.l for _, c in b), close=b[-1][1].c, n=len(b))
    return out


def open_features(history: list[dict], today: dict) -> dict | None:
    """``history``: complete earlier sessions, oldest first (at least 22); ``today``: needs open, pm_h, pm_l."""
    if len(history) < 22 or not today.get("pm_h") or not today.get("open"):
        return None
    rng = [math.log(s["high"] / s["low"]) for s in history[-22:]]
    gap = math.log(today["open"] / history[-1]["close"])
    return {"lr1": math.log(rng[-1]), "lr5": math.log(sum(rng[-5:]) / 5), "lr22": math.log(sum(rng) / 22),
            "lpm": math.log(max(math.log(today["pm_h"] / today["pm_l"]), 1e-4)), "agap": abs(gap),
            "gpos": max(gap, 0.0), "gneg": max(-gap, 0.0), "gap": gap}


def _dot(coef: list[float], names: Sequence[str], f: dict) -> float:
    return coef[0] + sum(c * f[n] for c, n in zip(coef[1:], names))


def at_open(model: dict, f: dict, open_px: float) -> dict:
    """Range forecast and 10/50/90% bands for the session's high and low, in price."""
    rng = math.exp(_dot(model["range"], OPEN_FEATURES, f))
    out = {"range_pct": round(rng * 100, 3)}
    for side, sign in (("high", 1), ("low", -1)):
        m = model[side]
        mu = _dot(m["coef"], SIDE_FEATURES, f)
        for q, r in zip(("p10", "p50", "p90"), m["resid_q"]):
            move = math.exp(mu + r) - 5e-4
            out[f"{side}_{q}"] = open_px * math.exp(sign * max(move, 0.0))
    return out


def intraday_features(minute: int, high: float, low: float, last: float, range_hat: float, gap: float, side: str) -> list[float]:
    so_far = math.log(high / low) / range_hat
    pos = (last - low) / (high - low) if high > low else 0.5
    left = (960 - minute) / 390
    if side == "high":
        p, dist, g = pos, math.log(high / last), gap
    else:
        p, dist, g = 1 - pos, math.log(last / low), -gap
    return [1.0, left, so_far, p, dist / range_hat, g * 100, so_far * left, p * left]


def p_extreme_in(model: dict, minute: int, high: float, low: float, last: float, range_hat: float, gap: float) -> dict:
    out = {}
    for side in ("high", "low"):
        z = sum(w * x for w, x in zip(model["p_in"][side], intraday_features(minute, high, low, last, range_hat, gap, side)))
        out[side] = 1 / (1 + math.exp(-z))
    return out


def load() -> dict:
    return json.loads(MODEL.read_text())


# ---- fitting (offline, numpy) ----
def fit(bars: Sequence[Candle], until: str | None = None) -> dict:
    import numpy as np
    S = sessions(bars)
    days = [d for d in sorted(S) if S[d].get("n", 0) >= 70]
    rows, intr = [], {"high": ([], []), "low": ([], [])}
    for k in range(22, len(days)):
        d = days[k]
        if until and d.isoformat() >= until:
            break
        today, hist = S[d], [S[x] for x in days[k - 22:k]]
        f = open_features(hist, today)
        if not f:
            continue
        rows.append((f, today))
    X = lambda names: np.array([[1.0] + [f[n] for n in names] for f, _ in rows])
    rng_y = np.array([math.log(t["high"] / t["low"]) for _, t in rows])
    b_rng, *_ = np.linalg.lstsq(X(OPEN_FEATURES), np.log(rng_y), rcond=None)
    model = {"fit_on": f"QQQ 5-minute SIP, {days[22]} to {rows[-1][1]['bars'][0][1].t[:10]}", "range": b_rng.tolist()}
    for side in ("high", "low"):
        y = np.array([math.log((t["high"] / t["open"]) if side == "high" else (t["open"] / t["low"])) for _, t in rows])
        ly = np.log(y + 5e-4)
        b, *_ = np.linalg.lstsq(X(SIDE_FEATURES), ly, rcond=None)
        res = ly - X(SIDE_FEATURES) @ b
        model[side] = {"coef": b.tolist(), "resid_q": np.quantile(res, [0.1, 0.5, 0.9]).tolist()}
    # intraday probabilities
    for f, t in rows:
        rh = math.exp(_dot(model["range"], OPEN_FEATURES, f))
        for T in CHECKPOINTS:
            seen = [c for m, c in t["bars"] if m < T]
            if not seen:
                continue
            h, l, last = max(c.h for c in seen), min(c.l for c in seen), seen[-1].c
            for side in ("high", "low"):
                intr[side][0].append(intraday_features(T, h, l, last, rh, f["gap"], side))
                intr[side][1].append(1.0 if (t["high"] <= h if side == "high" else t["low"] >= l) else 0.0)
    model["p_in"] = {}
    for side in ("high", "low"):
        Xs, ys = np.array(intr[side][0]), np.array(intr[side][1])
        w = np.zeros(Xs.shape[1])
        for _ in range(50):
            p = 1 / (1 + np.exp(-Xs @ w)); W = p * (1 - p) + 1e-9
            w += np.linalg.solve((Xs.T * W) @ Xs + 1e-6 * np.eye(len(w)), Xs.T @ (ys - p))
        model["p_in"][side] = w.tolist()
    return model


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fit", action="store_true")
    ap.add_argument("--until", help="fit only on sessions before this date (YYYY-MM-DD)")
    args = ap.parse_args()
    if args.fit:
        model = fit(pickle.loads(QQQ_CACHE.read_bytes()), args.until)
        MODEL.write_text(json.dumps(model, indent=1))
        print("saved", MODEL, model["fit_on"])


if __name__ == "__main__":
    main()
