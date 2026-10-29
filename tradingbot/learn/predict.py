"""The bot's own predictor of each trading day's high and low (NAS100 and gold), developed day by day.

At checkpoints in the trading day (18:00 open, 03:00 London, 09:30 New York, 12:00, 14:00 New York) it
predicts the day's final high and low from what it can see then: price, the high and low so far, the time
left, recent days' ranges, the overnight (Asia) range, the previous day's levels. It starts naive (v1: the
median extension of past days at that checkpoint) and each week fits candidate models on past days only,
scores them on the most recent past days they were not fitted on, and switches only when a candidate beats
the current version there. Each switch is a new predictor version in the changelog. Every day's prediction
is made with the version in force at the start of that day.
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np

from .market import Market, date_of

CHECKPOINTS = {"open 18:05": 5, "London 03:00": 540, "New York 09:30": 930, "12:00": 1080, "14:00": 1200}


def daily_rows(m: Market) -> list[dict]:
    """One row per (day, checkpoint): features visible at the checkpoint and the day's actual extremes."""
    D = m.frames["D"]
    rng = np.log(D.h / D.l)
    rows = []
    for k, d in enumerate(D.day):
        if k < 21:
            continue
        a, b = int(D.first[k]), int(D.last[k])
        mins = m.mins[a:b + 1]
        for name, cm in CHECKPOINTS.items():
            j = int(np.searchsorted(mins, cm))
            if j <= 0 or j >= len(mins) - 30:
                continue
            i = a + j - 1                      # the last closed minute at the checkpoint
            H, L, p = float(m.h[a:i + 1].max()), float(m.l[a:i + 1].min()), float(m.c[i])
            asia = (mins < 540)
            asia_rng = float(np.log(m.h[a:a + int(asia.sum())].max() / m.l[a:a + int(asia.sum())].min())) if cm >= 540 and asia.sum() > 30 else 0.0
            f = {
                "r1": rng[k - 1], "r5": rng[k - 5:k].mean(), "r20": rng[k - 20:k].mean(),
                "so_far": math.log(H / L), "left": (1380 - cm) / 1380, "asia": asia_rng,
                "to_pdh": math.log(D.h[k - 1] / p), "to_pdl": math.log(p / D.l[k - 1]),
                "pos": (p - L) / (H - L) if H > L else 0.5, "dow": date_of(d)[:10],
            }
            rows.append({"day": int(d), "cp": name, "i": i, "p": p, "H": H, "L": L, "f": f,
                         "up": math.log(float(D.h[k]) / max(H, p)), "dn": math.log(min(L, p) / float(D.l[k])),
                         "high": float(D.h[k]), "low": float(D.l[k])})
    return rows


def _X(rows, kind):
    if kind == "scaled":
        return np.array([[1.0, math.log(max(r["f"]["r5"], 1e-5))] for r in rows])
    return np.array([[1.0, math.log(max(r["f"]["r1"], 1e-5)), math.log(max(r["f"]["r5"], 1e-5)), math.log(max(r["f"]["r20"], 1e-5)),
                      math.log(max(r["f"]["so_far"], 1e-5)), r["f"]["left"], math.log(max(r["f"]["asia"], 1e-5)) if r["f"]["asia"] else 0.0,
                      r["f"]["pos"], min(r["f"]["to_pdh"], 0.05), min(r["f"]["to_pdl"], 0.05)] for r in rows])


class Model:
    """Predicts log extension up and down (median) and 10%/90% bands, per checkpoint."""

    def __init__(self, kind: str):
        self.kind, self.p = kind, {}

    def fit(self, rows: list[dict]) -> "Model":
        by = defaultdict(list)
        for r in rows:
            by[r["cp"]].append(r)
        for cp, rs in by.items():
            self.p[cp] = {}
            for side in ("up", "dn"):
                y = np.log(np.array([r[side] for r in rs]) + 1e-4)
                if self.kind == "median":
                    pred = np.full(len(y), np.median(y))
                    self.p[cp][side] = ("median", float(np.median(y)))
                else:
                    X = _X(rs, self.kind)
                    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
                    pred = X @ beta
                    self.p[cp][side] = (self.kind, beta.tolist())
                res = y - pred
                self.p[cp][side + "_q"] = np.quantile(res, [0.1, 0.5, 0.9]).tolist()
        return self

    def predict(self, r: dict) -> dict:
        cp = self.p.get(r["cp"])
        if not cp:
            return {}
        out = {}
        for side in ("up", "dn"):
            kind, par = cp[side]
            mu = par if kind == "median" else float(_X([r], kind)[0] @ np.array(par))
            q = cp[side + "_q"]
            ext = [max(math.exp(mu + qq) - 1e-4, 0.0) for qq in q]
            out[side] = ext
        ref_hi, ref_lo = max(r["H"], r["p"]), min(r["L"], r["p"])
        return {"high": [ref_hi * math.exp(e) for e in out["up"]], "low": [ref_lo * math.exp(-e) for e in out["dn"]]}


def error(model: Model, rows: list[dict]) -> float:
    """Mean absolute error of the predicted high and low (median), in % of price."""
    e = []
    for r in rows:
        pr = model.predict(r)
        if pr:
            e.append(abs(pr["high"][1] - r["high"]) / r["p"] + abs(pr["low"][1] - r["low"]) / r["p"])
    return float(np.mean(e)) * 50 if e else 9.9   # average of the two, in %


def develop(markets: dict[str, Market], out: Path, refit_every: int = 5) -> dict:
    """Live through the days: predict each day with the version in force, then (weekly) try to improve."""
    out.mkdir(parents=True, exist_ok=True)
    rows = {inst: daily_rows(m) for inst, m in markets.items()}
    log, changelog, versions = [], [], {}
    for inst, rs in rows.items():
        by_day = defaultdict(list)
        for r in rs:
            by_day[r["day"]].append(r)
        days = sorted(by_day)
        current, version = None, 0
        for n, d in enumerate(days):
            if current is not None:
                for r in by_day[d]:
                    pr = current.predict(r)
                    if pr:
                        log.append({"instrument": inst, "date": date_of(d), "checkpoint": r["cp"], "version": version, "price": round(r["p"], 3),
                                    "high_so_far": round(r["H"], 3), "low_so_far": round(r["L"], 3),
                                    "pred_high": round(pr["high"][1], 3), "high_band": [round(pr["high"][0], 3), round(pr["high"][2], 3)],
                                    "pred_low": round(pr["low"][1], 3), "low_band": [round(pr["low"][2], 3), round(pr["low"][0], 3)],
                                    "actual_high": r["high"], "actual_low": r["low"]})
            if (n + 1) % refit_every or n < 40:
                continue
            past = [r for dd in days[:n + 1] for r in by_day[dd]]           # up to today only
            hold = [r for dd in days[max(0, n - 59):n + 1] for r in by_day[dd]]   # the last 60 days
            fit_on = [r for dd in days[:max(0, n - 59)] for r in by_day[dd]]
            if len(fit_on) < 100:
                fit_on = past
            cands = {k: Model(k).fit(fit_on) for k in ("median", "scaled", "full")}
            scores = {k: error(mdl, hold) for k, mdl in cands.items()}
            best = min(scores, key=scores.get)
            cur_kind = current.kind if current else None
            if current is None or (best != cur_kind and scores[best] < scores[cur_kind] - 0.01):
                version += 1
                changelog.append(f"- {inst} predictor v{version} from the day after {date_of(d)}: {best} model "
                                 f"(error on the last 60 days, fitted before them: " + ", ".join(f"{k} {v:.3f}%" for k, v in scores.items()) + ")")
                current = Model(best).fit(past)
            else:
                current = Model(cur_kind).fit(past)   # same model, refreshed with the new days
        versions[inst] = version
    with open(out / "predictions.jsonl", "w") as f:
        f.writelines(json.dumps(x) + "\n" for x in log)
    (out / "PREDICTOR_CHANGELOG.md").write_text("# Daily high/low predictor: versions\n\n" + "\n".join(changelog) + "\n")
    return score(log, out)


def score(log: list[dict], out: Path) -> dict:
    res = {}
    for inst in sorted({x["instrument"] for x in log}):
        for cp in CHECKPOINTS:
            xs = [x for x in log if x["instrument"] == inst and x["checkpoint"] == cp]
            if not xs:
                continue
            eh = np.array([abs(x["pred_high"] - x["actual_high"]) for x in xs])
            el = np.array([abs(x["pred_low"] - x["actual_low"]) for x in xs])
            inb_h = np.mean([x["high_band"][0] <= x["actual_high"] <= x["high_band"][1] for x in xs])
            inb_l = np.mean([x["low_band"][0] <= x["actual_low"] <= x["low_band"][1] for x in xs])
            naive_h = np.array([abs(x["high_so_far"] - x["actual_high"]) for x in xs])
            res[f"{inst} {cp}"] = {"days": len(xs), "high_error_median": round(float(np.median(eh)), 3),
                                   "low_error_median": round(float(np.median(el)), 3),
                                   "high_in_80pct_band": round(float(inb_h), 3), "low_in_80pct_band": round(float(inb_l), 3),
                                   "naive_high_error_median": round(float(np.median(naive_h)), 3)}
    (out / "predictor_scorecard.json").write_text(json.dumps(res, indent=1))
    return res
