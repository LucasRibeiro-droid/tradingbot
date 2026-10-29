"""NAS100 only, last 1000 trading days. Find on the first 600 days, test frozen on the last 400.
New: compression before the setup, the predictor's expected expansion, exits at the predicted extreme."""
import copy, pickle, sys
from collections import defaultdict
import numpy as np
sys.path.insert(0, "/home/user/tradingbot")
from tradingbot.learn import data
from tradingbot.learn.market import Market, date_of
from tradingbot.learn.miner import Miner, predicate_row, NAMES
from tradingbot.learn.features import add_features
from tradingbot.learn.learner import Rulebook, Rule, apply_rulebook, XTrade
from tradingbot.learn.run import add_room_tags, OUT
from tradingbot.learn.sim import simulate
INST = "NAS100_USD"
m = Market(INST, data.load(INST)); markets = {INST: m}
xs = [x for x in pickle.loads((data.CACHE / "xtrades_2021_2026.pkl").read_bytes()) if x.inst == INST]
add_room_tags(xs, markets, OUT / "predictor"); add_features(xs, markets, OUT / "predictor" / "predictions.jsonl")
# exits at the predicted extreme: one extra trade per signal, all out at the predicted high (long) / low (short)
extra, nid, done = [], max(x.id for x in xs) + 1, set()
for x in xs:
    s = x.signal
    if id(s) in done or s.family == "crt": continue
    done.add(id(s))
    room = s.tags.get("room_R")
    if room is None or room < 0.5: continue
    s2 = copy.copy(s); s2.targets = (min(room, 8.0), min(room, 8.0))
    tr = simulate(m, s2, "pred_extreme")
    extra.append(XTrade(nid, INST, x.day, s, "pred_extreme", tr)); nid += 1
xs += extra
for x in xs:
    x.signal.tags["side_long"] = x.signal.side == 1
    x.signal.tags["_pred"] = predicate_row(x.signal.tags)
days = sorted({x.day for x in xs})[-1000:]
d0, split = days[0], days[600]
xs = [x for x in xs if x.day >= d0]
print("window", date_of(d0), "->", date_of(days[-1]), "| find until", date_of(split), "| test from", date_of(split))
by_day = defaultdict(list)
for x in xs: by_day[x.day].append(x)
train, test = days[:600], days[600:]
# quick look: each new idea alone, train vs test, for the main families
def stat(sel, ds):
    s = set(ds)
    r = np.array([x.r for x in xs if x.trade.filled and x.day in s and sel(x)])
    return (round(float(r.mean()), 3), len(r)) if len(r) else (None, 0)
ix = {n: NAMES.index(n) for n in NAMES}
for fam in ("sweep_bos", "continuation", "opening_range", "crt"):
    for cond in ("compressed", "expanding_now", "big_day_expected", "small_day_expected"):
        for tg in ("2R", "pred_extreme"):
            sel = lambda x: x.signal.family == fam and x.target == tg and x.signal.tags["_pred"][ix[cond]]
            a, b = stat(sel, train), stat(sel, test)
            if a[1] >= 50: print(f"{fam:13s} {cond:18s} {tg:12s} find {a}  test {b}")
# mining on the first 600 days, frozen, tested on the last 400
miner = Miner(xs)
miner.year = np.where(miner.day < days[300], 0, 1)   # the two halves of the finding window stand in for years
pats = miner.mine(before_day=split, beam=6, depth=3, top=300)
def evaluate(rb, ds):
    out = []
    for d in ds:
        t = apply_rulebook(rb, by_day[d], markets)
        out.append((sum(x.r for x, _ in t), len(t), [x.r for x, _ in t]))
    dr = np.array([o[0] for o in out if o[1]]); rs = np.array([r for o in out for r in o[2]]); n = np.array([o[1] for o in out])
    if not len(rs): return {"trades": 0}
    eq = np.cumsum(dr)
    return {"green_of_traded": round(float((dr > 0).mean()), 3), "green_all_days": round(float((dr > 0).sum() / len(ds)), 3),
            "days_2to5": round(float(((n >= 2) & (n <= 5)).mean()), 3), "trades": len(rs), "avg_r": round(float(rs.mean()), 3),
            "total_r": round(float(rs.sum()), 1), "maxdd": round(float((eq - np.maximum.accumulate(eq)).min()), 1)}
for top_n in (4, 8, 15):
    rules, seen = [], set()
    for p in pats:
        if p.group in seen: continue
        seen.add(p.group); rules.append(Rule(INST, p.group[1], p.group[2], "+".join(p.conds), p.score, p.n, p.mean, p.conds))
    core, fb = rules[:top_n], rules[top_n:2 * top_n]
    best = None
    for win in (None, 0.5, 1.0, 2.0):
        for loss in (None, -1.0, -2.0):
            rb = Rulebook(0, "", core, fb, win, loss, force_crt=False)
            ev = evaluate(rb, train)
            if ev.get("trades") and ev["total_r"] > 0:
                key = (ev["green_all_days"], ev["total_r"])
                if best is None or key > best[0]: best = (key, rb)
    rb = best[1] if best else Rulebook(0, "", core, fb, force_crt=False)
    print(f"\n== top {top_n} mined patterns (stops {rb.day_stop_win}/{rb.day_stop_loss})")
    for r in core[:6]: print("   ", r.base, r.target, "|", r.filt, f"n={r.n} mean={r.mean:+.3f}")
    print("   FIND 600 days:", evaluate(rb, train))
    print("   TEST 400 days:", evaluate(rb, test))
