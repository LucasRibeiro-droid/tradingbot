"""Run the day-by-day learning simulation on 2021-2024 and write every deliverable to journal/learn/.

    python -m tradingbot.learn.run              # development period (the holdout stays locked)
"""
from __future__ import annotations

import argparse
import csv
import gzip
import json
import pickle
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from . import data
from .learner import XTrade, Learner, PatternLearner
from .features import add_features
from .miner import Miner, predicate_row
from .market import Market, date_of
from .setups import all_signals
from .sim import TARGETS, simulate

OUT = Path(__file__).resolve().parent.parent.parent / "journal" / "learn"
CACHE = data.CACHE


def experiments(markets: dict[str, Market], tag: str) -> list[XTrade]:
    f = CACHE / f"xtrades_{tag}.pkl"
    if f.exists():
        return pickle.loads(f.read_bytes())
    out, n = [], 0
    for inst, m in markets.items():
        t0 = time.time()
        sig = all_signals(m)
        for s in sig:  # stop size in spreads, as known at the decision
            s.tags["stop_sp"] = round(abs(s.entry - s.stop) / max(s.tags["spread"], 1e-9), 1)
        for s in sig:
            for tg in (["half1R_3R"] if s.targets else list(TARGETS)):
                out.append(XTrade(n, inst, int(m.day[s.known]), s, tg, simulate(m, s, tg)))
                n += 1
        print(f"{inst}: {len(sig)} signals, {time.time() - t0:.0f}s", flush=True)
    out.sort(key=lambda x: (x.day, x.signal.known, x.id))
    f.write_bytes(pickle.dumps(out))
    return out


def write_outputs(L: Learner, xs: list[XTrade], markets: dict[str, Market], tag: str) -> dict:
    out = L.out
    # 1. experiment journal (filled trades only), one gzip CSV per year
    cols = ["id", "date", "instrument", "tag", "family", "setup", "target", "timeframes", "session", "side", "decided_ny",
            "entry_kind", "entry", "fill", "stop", "exits", "r", "with_1h", "with_4h", "with_D", "discount", "reasoning"]
    by_year = defaultdict(list)
    for x in xs:
        if not x.trade.filled:
            continue
        s, m = x.signal, markets[x.inst]
        by_year[date_of(x.day)[:4]].append([x.id, date_of(x.day), x.inst, "experiment", s.family, s.base, x.target, s.tags.get("tf"),
                                            s.tags["session"], "long" if s.side == 1 else "short", m.when(s.known), s.kind,
                                            round(s.entry, 3), round(x.trade.fill, 3), round(s.stop, 3),
                                            "; ".join(f"{q:g}@{px:.3f} {k}" for px, q, k, _ in x.trade.exits), round(x.r, 4),
                                            s.tags["with_1h"], s.tags["with_4h"], s.tags["with_D"], s.tags["discount"], s.why])
    for y, rows in by_year.items():
        with gzip.open(out / f"experiments_{tag}_{y}.csv.gz", "wt", newline="") as f:
            w = csv.writer(f)
            w.writerow(cols)
            w.writerows(rows)
    # 2. strategy journal
    scol = ["date", "instrument", "tag", "type", "rule_version", "why_taken", "setup", "target", "timeframes", "session", "side",
            "decided_ny", "entry_kind", "entry", "fill", "stop", "exits", "r", "reasoning", "lesson"]
    rows = []
    for e in L.strategy_log:
        x, s, m = e["x"], e["x"].signal, markets[e["x"].inst]
        rows.append([date_of(x.day), x.inst, "strategy", "CRT" if s.family == "crt" else "self-developed", f"v{e['version']}",
                     e["why"], s.base, x.target, s.tags.get("tf"), s.tags["session"], "long" if s.side == 1 else "short",
                     m.when(s.known), s.kind, round(s.entry, 3), round(x.trade.fill, 3), round(s.stop, 3),
                     "; ".join(f"{q:g}@{px:.3f} {k}" for px, q, k, _ in x.trade.exits), round(x.r, 4), s.why, e["lesson"]])
    with open(out / f"strategy_trades_{tag}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(scol)
        w.writerows(rows)
    (out / "CHANGELOG.md").write_text("# Rulebook changelog\n\nEach version is written after the day shown and used from the next "
                                      "trading day. ADD/DROP lines cite the experiment evidence behind the change.\n\n" + "\n\n".join(L.changelog) + "\n")
    # 3. daily notes, one file per month: the day's strategy trades with reasons and lessons, and any rule change
    strat_by_day = defaultdict(list)
    for e in L.strategy_log:
        strat_by_day[date_of(e["x"].day)].append(e)
    changes = {c.split("written after ")[1][:10]: c for c in L.changelog}
    notes = defaultdict(list)
    for h in L.history:
        d = h["day"]
        lines = [f"### {d} — rulebook v{h['version']}: {h['trades']} strategy trade(s), {h['r']:+.2f}R"]
        for e in strat_by_day.get(d, []):
            x = e["x"]
            lines.append(f"- {x.inst} {'long' if x.signal.side == 1 else 'short'} · {x.signal.base} ({x.target}) → {x.r:+.2f}R. "
                         f"Why: {e['why']}. {x.signal.why}. Lesson: {e['lesson']}")
        if d in changes:
            lines.append("- **Review → rule change:**\n" + "\n".join("  " + l for l in changes[d].splitlines()[1:]))
        notes[d[:7]].append("\n".join(lines))
    (out / "notes").mkdir(exist_ok=True)
    for month, items in notes.items():
        (out / "notes" / f"{month}.md").write_text(f"# {month}\n\n" + "\n\n".join(items) + "\n")
    return report(L, tag)


def report(L: Learner, tag: str) -> dict:
    hist = L.history
    traded = [h for h in hist if h["trades"] > 0]
    day_r = np.array([h["r"] for h in traded])
    rs = np.array([e["x"].r for e in L.strategy_log])
    eq = np.cumsum(day_r) if len(day_r) else np.zeros(1)
    dd = float((eq - np.maximum.accumulate(eq)).min()) if len(day_r) else 0.0
    streak = best = 0
    for r in day_r:
        streak = streak + 1 if r <= 0 else 0
        best = max(best, streak)
    pf = float(rs[rs > 0].sum() / -rs[rs < 0].sum()) if (rs < 0).any() else float("inf")
    def part(sel):
        v = np.array([e["x"].r for e in L.strategy_log if sel(e)])
        return {"trades": int(len(v)), "avg_r": round(float(v.mean()), 4) if len(v) else None, "total_r": round(float(v.sum()), 2),
                "win_rate": round(float((v > 0).mean()), 3) if len(v) else None}
    res = {
        "period": tag, "trading_days": len(hist), "days_with_strategy_trades": len(traded),
        "profitable_days_pct": round(float((day_r > 0).mean()), 4) if len(day_r) else None,
        "losing_days": int((day_r < 0).sum()), "flat_days": int((day_r == 0).sum()),
        "days_with_2_to_5_trades_pct": round(float(np.mean([2 <= h["trades"] <= 5 for h in hist])), 3),
        "longest_losing_day_streak": best, "max_drawdown_r": round(dd, 2),
        "trades": int(len(rs)), "win_rate": round(float((rs > 0).mean()), 3) if len(rs) else None,
        "avg_r": round(float(rs.mean()), 4) if len(rs) else None, "total_r": round(float(rs.sum()), 2), "profit_factor": round(pf, 3),
        "crt": part(lambda e: e["x"].signal.family == "crt"), "self_developed": part(lambda e: e["x"].signal.family != "crt"),
        "NAS100_USD": part(lambda e: e["x"].inst == "NAS100_USD"), "XAU_USD": part(lambda e: e["x"].inst == "XAU_USD"),
        "by_year": {y: part(lambda e, y=y: date_of(e["x"].day).startswith(y)) for y in sorted({h["day"][:4] for h in hist})},
        "rulebook_versions": L.rulebook.version,
    }
    (L.out / f"results_{tag}.json").write_text(json.dumps(res, indent=1))
    return res


def add_room_tags(xs: list[XTrade], markets: dict[str, Market], pred_dir: Path) -> None:
    """Tag each signal with the room the bot's own predictor leaves, as known at the decision: the latest
    checkpoint prediction of that day (made with the predictor version in force that day) of the day's high
    (longs) or low (shorts), minus the entry, in units of the trade's risk."""
    from .predict import CHECKPOINTS, develop
    if not (pred_dir / "predictions.jsonl").exists():
        develop(markets, pred_dir)
    preds = defaultdict(list)
    for line in (pred_dir / "predictions.jsonl").read_text().splitlines():
        p = json.loads(line)
        preds[(p["instrument"], p["date"])].append((CHECKPOINTS[p["checkpoint"]], p["pred_high"], p["pred_low"]))
    done = set()
    for x in xs:
        s = x.signal
        if id(s) in done:
            continue
        done.add(id(s))
        m = markets[x.inst]
        cps = [c for c in preds.get((x.inst, date_of(x.day)), []) if c[0] <= m.mins[s.known]]
        risk = abs(s.entry - s.stop)
        if not cps or risk <= 0:
            s.tags["room_R"] = None
            continue
        cp = max(cps)
        s.tags["room_R"] = round(((cp[1] - s.entry) if s.side == 1 else (s.entry - cp[2])) / risk, 2)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rewrite-every", type=int, default=5)  # weekly
    ap.add_argument("--end", default="2026-10-29")
    ap.add_argument("--engine", default="v5", choices=["v4", "v5"])
    args = ap.parse_args()
    from datetime import datetime, timezone
    end = datetime.fromisoformat(args.end).replace(tzinfo=timezone.utc)
    tag = "2021_2026" if args.end == "2026-10-29" else f"to_{args.end}"
    markets = {inst: Market(inst, data.load(inst, end=end)) for inst in data.INSTRUMENTS}
    xs = experiments(markets, tag)
    add_room_tags(xs, markets, OUT / "predictor")
    add_features(xs, markets, OUT / "predictor" / "predictions.jsonl")
    for x in xs:
        if "_pred" not in x.signal.tags:
            x.signal.tags["side_long"] = x.signal.side == 1
            x.signal.tags["_pred"] = predicate_row(x.signal.tags)
    L = PatternLearner(markets, xs, OUT, Miner(xs)) if args.engine == "v5" else Learner(markets, xs, OUT)
    t0 = time.time()
    L.run(args.rewrite_every)
    print(f"learning {time.time() - t0:.0f}s, {len(L.strategy_log)} strategy trades, rulebook v{L.rulebook.version}")
    res = write_outputs(L, xs, markets, tag)
    print(json.dumps({k: v for k, v in res.items() if k != "by_year"}, indent=1))


if __name__ == "__main__":
    main()
