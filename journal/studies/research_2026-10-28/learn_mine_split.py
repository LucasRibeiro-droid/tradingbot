"""Mine on 2021-2024 (all of it), freeze the rulebook, trade it day by day on 2025-2026."""
import pickle, sys, json
from collections import defaultdict
import numpy as np
sys.path.insert(0, "/home/user/tradingbot")
from pathlib import Path
from tradingbot.learn import data
from tradingbot.learn.market import Market, date_of
from tradingbot.learn.miner import Miner, predicate_row
from tradingbot.learn.features import add_features
from tradingbot.learn.learner import Rulebook, Rule, apply_rulebook
from tradingbot.learn.run import add_room_tags, OUT
from datetime import date
markets = {i: Market(i, data.load(i)) for i in data.INSTRUMENTS}
xs = pickle.loads((data.CACHE / "xtrades_2021_2026.pkl").read_bytes())
add_room_tags(xs, markets, OUT / "predictor"); add_features(xs, markets, OUT / "predictor" / "predictions.jsonl")
for x in xs:
    if "_pred" not in x.signal.tags:
        x.signal.tags["side_long"] = x.signal.side == 1; x.signal.tags["_pred"] = predicate_row(x.signal.tags)
split = date(2025, 1, 1).toordinal()
miner = Miner(xs)
by_day = defaultdict(list)
for x in xs: by_day[x.day].append(x)
days = sorted(by_day)
train = [d for d in days if d < split]; test = [d for d in days if d >= split]
def evaluate(rb, ds):
    out = []
    for d in ds:
        t = apply_rulebook(rb, by_day[d], markets)
        out.append((sum(x.r for x, _ in t), len(t), [x.r for x, _ in t]))
    dr = np.array([o[0] for o in out if o[1]]); rs = np.array([r for o in out for r in o[2]])
    n = np.array([o[1] for o in out])
    return {"days": len(ds), "traded_days": int((n > 0).sum()), "green_pct_of_traded": round(float((dr > 0).mean()), 3) if len(dr) else None,
            "green_pct_all_days": round(float((dr > 0).sum() / len(ds)), 3), "days_2to5": round(float(((n >= 2) & (n <= 5)).mean()), 3),
            "trades": len(rs), "avg_r": round(float(rs.mean()), 3) if len(rs) else None, "total_r": round(float(rs.sum()), 1),
            "maxdd": round(float((np.cumsum(dr) - np.maximum.accumulate(np.cumsum(dr))).min()), 1) if len(dr) else 0}
for top_n in (6, 12):
    pats = miner.mine(before_day=split, beam=6, depth=3, top=200)
    rules, seen = [], set()
    for p in pats:
        if p.group in seen: continue
        seen.add(p.group)
        rules.append(Rule(p.group[0], p.group[1], p.group[2], "+".join(p.conds), p.score, p.n, p.mean, p.conds))
    core, fb = rules[:top_n], rules[top_n:top_n * 2]
    best = None
    for win in (None, 0.5, 1.0, 2.0):
        for loss in (None, -1.0, -2.0):
            rb = Rulebook(0, "", core, fb, win, loss, force_crt=False)
            ev = evaluate(rb, train[-500:])
            key = (ev["green_pct_all_days"], ev["total_r"])
            if ev["total_r"] > 0 and (best is None or key > best[0]): best = (key, rb, ev)
    rb = best[1] if best else Rulebook(0, "", core, fb, force_crt=False)
    print(f"\n=== top {top_n} patterns, day stops win={rb.day_stop_win} loss={rb.day_stop_loss}")
    for r in core: print("  ", r.inst, r.base, r.target, "|", r.filt, f"n={r.n} mean={r.mean:+.3f} worst-year={r.score:+.3f}")
    print("  TRAIN 2021-2024 (in-sample):", evaluate(rb, train))
    print("  TEST  2025-2026 (unseen)   :", evaluate(rb, test))
