"""More concept features for every signal, all as known at the decision (no later data):

- pred_pos: where the entry sits inside the bot's predicted high-low range for the day (0 = predicted low,
  1 = predicted high), from the latest checkpoint prediction made with the predictor version in force
- range_used: the day's range so far / the predicted day range
- vol_regime: the day's range so far / the average daily range of the last 20 days
- to_pdh_r / to_pdl_r: distance from the entry to the previous day's high / low, in units of the trade's risk
- beyond_pd: the entry is already beyond the previous day's high (longs) / low (shorts)
- trend_votes: how many of 15m, 1h, 4h, daily trends agree with the trade (0-4)
- dow: weekday of the trading day (0 = Monday)
- compression: average 1-minute candle range over the last 30 minutes / over the last 10 hours (low = a quiet,
  compressed market just before the setup)
- exp_expansion: the day's predicted range (first prediction of the day) / the average daily range of the last
  20 days (high = the predictor expects a bigger day than usual)
"""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import date
from pathlib import Path

import numpy as np

from .market import Market, date_of
from .predict import CHECKPOINTS


def add_features(xs, markets: dict[str, Market], pred_file: Path) -> None:
    preds = defaultdict(list)
    for line in pred_file.read_text().splitlines():
        p = json.loads(line)
        preds[(p["instrument"], p["date"])].append((CHECKPOINTS[p["checkpoint"]], p["pred_high"], p["pred_low"]))
    avg_rng = {}
    for inst, m in markets.items():
        D = m.frames["D"]
        r = (D.h - D.l)
        avg_rng[inst] = {int(D.day[k]): float(r[max(0, k - 20):k].mean()) if k else float(r[0]) for k in range(len(D))}
        prev = {int(D.day[k]): (float(D.h[k - 1]), float(D.l[k - 1])) for k in range(1, len(D))}
        avg_rng[inst + ":prev"] = prev
    done = set()
    for x in xs:
        s = x.signal
        if id(s) in done:
            continue
        done.add(id(s))
        m, t = markets[x.inst], s.tags
        i, d = s.known, int(m.day[s.known])
        a = m.day_first[d]
        hi, lo = float(m.h[a:i + 1].max()), float(m.l[a:i + 1].min())
        risk = abs(s.entry - s.stop) or 1e-9
        cps = [c for c in preds.get((x.inst, date_of(d)), []) if c[0] <= m.mins[i]]
        if cps:
            _, ph, pl = max(cps)
            span = max(ph - pl, 1e-9)
            pos = (s.entry - pl) / span
            t["pred_pos"] = round(pos if s.side == 1 else 1 - pos, 3)   # 0 = at the predicted extreme against the trade
            t["range_used"] = round((hi - lo) / span, 3)
        else:
            t["pred_pos"] = t["range_used"] = None
        ar = avg_rng[x.inst].get(d) or 1e-9
        t["vol_regime"] = round((hi - lo) / ar, 3)
        pdh, pdl = avg_rng[x.inst + ":prev"].get(d, (None, None))
        if pdh is not None:
            t["to_pdh_r"] = round((pdh - s.entry) / risk, 2)
            t["to_pdl_r"] = round((s.entry - pdl) / risk, 2)
            t["beyond_pd"] = bool(s.entry > pdh) if s.side == 1 else bool(s.entry < pdl)
        t["trend_votes"] = sum(bool(t.get("with_" + tf)) for tf in ("15m", "1h", "4h", "D"))
        rng1 = m.h[max(0, i - 599):i + 1] - m.l[max(0, i - 599):i + 1]
        t["compression"] = round(float(rng1[-30:].mean() / max(rng1.mean(), 1e-9)), 3)
        first = min(preds.get((x.inst, date_of(d)), [(0, None, None)]), key=lambda c: c[0])
        t["exp_expansion"] = round((first[1] - first[2]) / ar, 3) if first[1] is not None and first[0] <= m.mins[i] else None
        t["dow"] = date.fromordinal(d).weekday()
