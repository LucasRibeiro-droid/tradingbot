"""The bot living through 2021-2024 one trading day at a time.

Each day:
  1. it trades the day with the rulebook it wrote the evening before (its "strategy" trades: 2-5 a day
     once it has rules, at least one CRT when a valid CRT setup forms), and runs every experiment
     (every setup x target x filter it knows) as "experiment" trades;
  2. after the day ends it reviews: every trade's outcome joins the evidence, lessons are written;
  3. it rewrites the rulebook for the next day from evidence up to today only (the version and the
     reasons go to the changelog).
Nothing from day N+1 or later is visible on day N (asserted). The rulebook used on a day is the one
written before it started.
"""
from __future__ import annotations

import gzip
import json
import math
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .market import Market, date_of
from .setups import Signal
from .sim import TARGETS, Trade, simulate

FILTERS = {
    "all": lambda t: True,
    "with_1h": lambda t: t["with_1h"], "with_4h": lambda t: t["with_4h"], "with_D": lambda t: t["with_D"],
    "against_D": lambda t: t["against_D"], "discount": lambda t: t["discount"],
    "asia": lambda t: t["session"] == "asia", "london": lambda t: t["session"] == "london",
    "newyork": lambda t: t["session"] == "newyork",
    "with_1h+discount": lambda t: t["with_1h"] and t["discount"], "with_4h+with_D": lambda t: t["with_4h"] and t["with_D"],
    "newyork+with_1h": lambda t: t["session"] == "newyork" and t["with_1h"],
    "london+with_1h": lambda t: t["session"] == "london" and t["with_1h"],
    # stop size in spreads at the decision (set by the setup, known then)
    "stop>=3sp": lambda t: t.get("stop_sp", 0) >= 3, "stop>=6sp": lambda t: t.get("stop_sp", 0) >= 6,
    "stop>=10sp": lambda t: t.get("stop_sp", 0) >= 10,
    "stop>=6sp+with_1h": lambda t: t.get("stop_sp", 0) >= 6 and t["with_1h"],
    "stop>=6sp+newyork": lambda t: t.get("stop_sp", 0) >= 6 and t["session"] == "newyork",
    "stop>=6sp+london": lambda t: t.get("stop_sp", 0) >= 6 and t["session"] == "london",
    "stop>=6sp+asia": lambda t: t.get("stop_sp", 0) >= 6 and t["session"] == "asia",
    "stop>=6sp+with_D": lambda t: t.get("stop_sp", 0) >= 6 and t["with_D"],
    "stop>=6sp+discount": lambda t: t.get("stop_sp", 0) >= 6 and t["discount"],
    "day_pool": lambda t: "day" in t.get("pool", ""), "session_pool": lambda t: t.get("pool", "").split(" ")[0] in ("asia", "london", "newyork"),
    "prominent_pool": lambda t: t.get("pool", "").startswith("prominent"),
    # combinations the bot explores from the start (session x higher-timeframe agreement, New York windows)
    "newyork+with_4h": lambda t: t["session"] == "newyork" and t["with_4h"],
    "newyork+with_15m": lambda t: t["session"] == "newyork" and t["with_15m"],
    "newyork+with_D": lambda t: t["session"] == "newyork" and t["with_D"],
    "newyork+with_1h+with_4h": lambda t: t["session"] == "newyork" and t["with_1h"] and t["with_4h"],
    "ny_open": lambda t: t["session"] == "newyork" and 9 <= t["hour"] < 11,
    "ny_midday": lambda t: t["session"] == "newyork" and 11 <= t["hour"] < 14,
    "ny_late": lambda t: t["session"] == "newyork" and t["hour"] >= 14,
    "ny_open+with_1h": lambda t: t["session"] == "newyork" and 9 <= t["hour"] < 11 and t["with_1h"],
    "london+with_4h": lambda t: t["session"] == "london" and t["with_4h"],
    "asia+with_1h": lambda t: t["session"] == "asia" and t["with_1h"],
    "with_1h+with_4h": lambda t: t["with_1h"] and t["with_4h"],
    # the bot's own daily high/low predictor: room left to the predicted high (longs) / low (shorts)
    "room>=1R": lambda t: (t.get("room_R") or -9) >= 1, "room>=2R": lambda t: (t.get("room_R") or -9) >= 2,
    "room>=3R": lambda t: (t.get("room_R") or -9) >= 3, "room<0": lambda t: t.get("room_R") is not None and t["room_R"] < 0,
    "newyork+room>=2R": lambda t: t["session"] == "newyork" and (t.get("room_R") or -9) >= 2,
    "with_1h+room>=2R": lambda t: t["with_1h"] and (t.get("room_R") or -9) >= 2,
}
MAX_TRADES, MIN_TRADES = 5, 2


@dataclass
class XTrade:
    """One experiment trade: a signal traded with one target."""
    id: int
    inst: str
    day: int
    signal: Signal
    target: str
    trade: Trade

    @property
    def r(self) -> float:
        return self.trade.r


@dataclass
class Rule:
    inst: str
    base: str
    target: str
    filt: str
    score: float = 0.0
    n: int = 0
    mean: float = 0.0

    @property
    def key(self) -> str:
        return f"{self.inst}|{self.base}|{self.target}|{self.filt}"

    def matches(self, x: XTrade) -> bool:
        return x.inst == self.inst and x.signal.base == self.base and x.target == self.target and FILTERS[self.filt](x.signal.tags)


@dataclass
class Rulebook:
    version: int
    written_after: str
    rules: list[Rule] = field(default_factory=list)
    fallback: list[Rule] = field(default_factory=list)
    day_stop_win: float | None = None    # stop trading for the day once the day's R reaches this
    day_stop_loss: float | None = None   # ... or falls to this
    notes: list[str] = field(default_factory=list)

    def to_json(self) -> dict:
        r = lambda x: {"instrument": x.inst, "setup": x.base, "target": x.target, "filter": x.filt,
                       "score": round(x.score, 4), "trades_seen": x.n, "mean_r": round(x.mean, 4)}
        return {"version": self.version, "written_after": self.written_after, "always": "the day's first valid CRT setup (either instrument)",
                "rules": [r(x) for x in self.rules], "fallback_if_fewer_than_2_by_11am_new_york": [r(x) for x in self.fallback],
                "day_stop_win_R": self.day_stop_win, "day_stop_loss_R": self.day_stop_loss,
                "max_trades": MAX_TRADES, "min_trades": MIN_TRADES, "notes": self.notes}


def apply_rulebook(rb: Rulebook, day_trades: list[XTrade], markets: dict[str, Market]) -> list[tuple[XTrade, str]]:
    """The strategy trades the rulebook takes on one day, deciding in time order with only what each
    decision moment shows. An accepted order occupies a slot from its decision until it is filled (then
    until its exit) or, if it never fills, until it expires: whether a limit will fill is not known when
    it is placed. Day results count once trades have exited. Returns the accepted orders that filled."""
    pool = rb.rules + rb.fallback
    orders = sorted((x for x in day_trades if x.signal.family == "crt" or any(r.matches(x) for r in pool)),
                    key=lambda x: (x.signal.known, x.id))
    accepted: list[tuple[XTrade, str]] = []
    crt_active_until = -1
    crt_filled = False
    seen = set()

    def live_at(x: XTrade, i: int) -> bool:   # the order or its position still occupies a slot at i
        end = x.trade.exit_i if x.trade.filled else x.signal.expiry
        return end > i

    for x in orders:
        i = x.signal.known
        filled_or_working = [a for a, _ in accepted if (a.trade.filled and a.trade.fill_i <= i) or live_at(a, i)]
        if len([a for a, _ in accepted if a.trade.filled and a.trade.fill_i <= i]) + \
                len([a for a, _ in accepted if not (a.trade.filled and a.trade.fill_i <= i) and live_at(a, i)]) >= MAX_TRADES:
            continue
        closed_r = sum(a.r for a, _ in accepted if a.trade.filled and a.trade.exit_i <= i)
        if rb.day_stop_win is not None and closed_r >= rb.day_stop_win:
            break
        if rb.day_stop_loss is not None and closed_r <= rb.day_stop_loss:
            break
        sid = (x.inst, x.signal.known, x.signal.base, x.signal.entry, x.signal.side)
        if sid in seen:
            continue
        why = None
        if x.signal.family == "crt":
            if not crt_filled and crt_active_until < i:
                why = "CRT (always taken: the day's valid CRT setup)"
        else:
            for k, rule in enumerate(rb.rules):
                if rule.matches(x):
                    why = f"rule {k + 1}: {rule.base} | {rule.target} | filter {rule.filt}"
                    break
            n_now = len([a for a, _ in accepted if (a.trade.filled and a.trade.fill_i <= i) or live_at(a, i)])
            if why is None and n_now < MIN_TRADES and markets[x.inst].mins[i] >= 1020:  # from 11:00 New York
                for rule in rb.fallback:
                    if rule.matches(x):
                        why = f"fallback (fewer than {MIN_TRADES} trades by 11:00 New York): {rule.base} | {rule.target} | {rule.filt}"
                        break
        if why is None:
            continue
        if len([a for a, _ in accepted if a.inst == x.inst and live_at(a, i)]) >= 2:
            continue
        if x.signal.family == "crt":
            crt_active_until = x.signal.expiry if not x.trade.filled else x.trade.exit_i
            # whether it fills is only known later: the next CRT is considered once this one is filled or expired
            crt_filled = crt_filled or x.trade.filled
        seen.add(sid)
        accepted.append((x, why))
    return [(x, w) for x, w in accepted if x.trade.filled]


class Stats:
    """Evidence per variant (instrument, setup, target, filter), from trades that have exited."""

    def __init__(self):
        self.n = defaultdict(int)
        self.s = defaultdict(float)
        self.s2 = defaultdict(float)
        self.recent = defaultdict(list)   # (day, r)
        self.by_day = defaultdict(lambda: defaultdict(float))

    def add(self, x: XTrade):
        for fname, f in FILTERS.items():
            if f(x.signal.tags):
                k = (x.inst, x.signal.base, x.target, fname)
                self.n[k] += 1
                self.s[k] += x.r
                self.s2[k] += x.r * x.r
                self.recent[k].append((x.day, x.r))

    def score(self, k, today: int, k0: float = 40.0) -> tuple[float, float, int]:
        """Evidence that a variant earns: positive in most quarters of its past (not just lately), shrunk
        toward zero for small samples, minus half a standard error. -9 = not trusted."""
        n = self.n[k]
        if n < 60:
            return -9.0, 0.0, n
        mean = self.s[k] / n
        rs = [r for _, r in self.recent[k]]
        q = np.array_split(np.array(rs), 4)
        if sum(1 for b in q if len(b) and b.mean() > 0) < 3:
            return -9.0, mean, n
        rec = [r for d, r in self.recent[k] if d > today - 250]
        if len(rec) < 15 or np.mean(rec) <= 0:
            return -9.0, mean, n
        var = max(self.s2[k] / n - mean * mean, 1e-6)
        shrunk = self.s[k] / (n + k0)
        return shrunk - 0.5 * math.sqrt(var / n), mean, n


def lesson(x: XTrade, stats: "Stats") -> str:
    """The post-trade lesson, written the evening of the trade with the evidence to date."""
    kinds = [e[2] for e in x.trade.exits]
    k = (x.inst, x.signal.base, x.target, "all")
    n, tot = stats.n.get(k, 0), stats.s.get(k, 0.0)
    rec = f"this setup/target's record so far: {n} trades, {tot / n:+.3f}R average" if n else "no record yet"
    if all(e == "stop" for e in kinds):
        what = "stopped: price went back through the invalidation point"
    elif all(e.startswith("target") for e in kinds):
        what = "every target reached"
    elif "stop" in kinds or "break even" in kinds:
        what = "first target reached, the rest " + ("stopped at break even" if "break even" in kinds else "stopped")
    else:
        what = "held to the day's end without reaching the target or the stop"
    return f"{what} ({x.r:+.2f}R); {rec}."


class Learner:
    def __init__(self, markets: dict[str, Market], xtrades: list[XTrade], out: Path):
        self.markets, self.out = markets, out
        self.by_day: dict[int, list[XTrade]] = defaultdict(list)
        for x in xtrades:
            self.by_day[x.day].append(x)
        self.days = sorted(self.by_day)
        self.stats = Stats()
        self.rulebook = Rulebook(1, "start (no evidence yet)", notes=["Day 1: no custom strategy yet; only CRT is traded as strategy."])
        self.history: list[dict] = []
        self.live = defaultdict(list)        # rule key -> [(day, r)] of its strategy trades
        self.benched: dict[str, int] = {}    # rule key or "instrument:X" -> benched until this day
        self.changelog: list[str] = []
        self.strategy_log: list[dict] = []

    # ---- the evening review: evidence -> next rulebook ----
    def review_own_trades(self, today: int) -> list[str]:
        """Learning from its own strategy trades: a rule whose live record turns bad is benched for 60 trading
        days; an instrument whose recent strategy trades (excluding CRT) lose is benched too."""
        notes = []
        for key, recs in self.live.items():
            recent = [r for d, r in recs if d > today - 120]
            if len(recent) >= 15 and np.mean(recent) < -0.15 and self.benched.get(key, 0) <= today:
                self.benched[key] = today + 85
                notes.append(f"BENCH {key}: its own strategy trades lost {np.mean(recent):+.3f}R over the last {len(recent)} (until ~3 months)")
        for inst in self.markets:
            recent = [r for k, recs in self.live.items() if k.startswith(inst + "|") for d, r in recs if d > today - 120]
            tag = "instrument:" + inst
            if len(recent) >= 25 and np.mean(recent) < -0.15 and self.benched.get(tag, 0) <= today:
                self.benched[tag] = today + 85
                notes.append(f"BENCH {inst} (non-CRT): its strategy trades lost {np.mean(recent):+.3f}R over the last {len(recent)}")
        return notes

    def rewrite(self, today: int, last_index: dict[str, int]) -> None:
        bench_notes = self.review_own_trades(today)
        cand = []
        for k in self.stats.n:
            key = "|".join(k)
            if self.benched.get(key, 0) > today or self.benched.get("instrument:" + k[0], 0) > today:
                continue
            sc, mean, n = self.stats.score(k, today)
            if sc > 0:
                cand.append((sc, k, mean, n))
        cand.sort(reverse=True)
        keep = {r.key for r in self.rulebook.rules}
        cand.sort(key=lambda c: (c[0] + (0.02 if "|".join(c[1]) in keep else 0.0)), reverse=True)
        rules, used = [], defaultdict(int)
        for sc, k, mean, n in cand:
            inst, base, target, filt = k
            if used[(inst, base)] >= 1:      # one target/filter per setup: the best-scoring
                continue
            used[(inst, base)] += 1
            rules.append(Rule(inst, base, target, filt, sc, n, mean))
            if len(rules) >= 10:
                break
        fallback = []
        best_all = sorted(((self.stats.s[k] / (self.stats.n[k] + 40), k) for k in self.stats.n
                           if self.stats.n[k] >= 60 and self.stats.s[k] > 0 and self.benched.get("|".join(k), 0) <= today
                           and self.benched.get("instrument:" + k[0], 0) <= today), reverse=True)
        for sc, k in best_all:
            if all(r.key != "|".join(k) for r in rules):
                fallback.append(Rule(*k, score=sc, n=self.stats.n[k], mean=self.stats.s[k] / self.stats.n[k]))
            if len(fallback) >= 8:
                break
        # day stop rules: chosen on the last 250 days by replaying the candidate rules (past days only)
        best = (None, None, -1.0, -1e9)
        past = [d for d in self.days if d <= today][-250:]
        if rules and len(past) >= 40:
            for win in (None, 0.5, 1.0, 2.0):
                for loss in (None, -1.0, -2.0):
                    rb = Rulebook(0, "", rules, fallback, win, loss)
                    day_r = [sum(x.r for x, _ in apply_rulebook(rb, self.by_day[d], self.markets)) for d in past]
                    traded = [r for r in day_r if r != 0]
                    if not traded:
                        continue
                    green = np.mean([r > 0 for r in traded])
                    total = float(np.sum(traded))
                    if total > 0 and (green, total) > best[2:]:
                        best = (win, loss, green, total)
        new_keys = [r.key for r in rules]
        old_keys = [r.key for r in self.rulebook.rules]
        changed = bool(bench_notes) or new_keys != old_keys or (best[0], best[1]) != (self.rulebook.day_stop_win, self.rulebook.day_stop_loss)
        if changed:
            v = self.rulebook.version + 1
            added = [r for r in rules if r.key not in old_keys]
            dropped = [r for r in self.rulebook.rules if r.key not in new_keys]
            notes = list(bench_notes)
            for r in added:
                notes.append(f"ADD {r.key}: {r.n} experiment trades so far, mean {r.mean:+.3f}R, score {r.score:+.3f}")
            for r in dropped:
                k = (r.inst, r.base, r.target, r.filt)
                n = self.stats.n[k]
                rec = [x for d, x in self.stats.recent[k] if d > today - 180]
                notes.append(f"DROP {r.key}: now {n} trades, mean {self.stats.s[k] / max(n, 1):+.3f}R, last 180 days "
                             f"{np.mean(rec) if rec else 0:+.3f}R over {len(rec)}")
            if (best[0], best[1]) != (self.rulebook.day_stop_win, self.rulebook.day_stop_loss):
                notes.append(f"DAY STOPS: stop after +{best[0]}R / {best[1]}R on the day (replayed on the last {len(past)} days: "
                             f"{best[2]:.0%} green, {best[3]:+.1f}R)" if best[2] >= 0 else "DAY STOPS: none")
            self.rulebook = Rulebook(v, date_of(today), rules, fallback, best[0], best[1], notes)
            self.changelog.append(f"## v{v} (written after {date_of(today)}, used from the next trading day)\n" + "\n".join(f"- {n}" for n in notes))
            (self.out / "rulebook").mkdir(parents=True, exist_ok=True)
            (self.out / "rulebook" / f"strategy_v{v:03d}.json").write_text(json.dumps(self.rulebook.to_json(), indent=1))

    def run(self, rewrite_every: int = 5) -> None:
        self.out.mkdir(parents=True, exist_ok=True)
        (self.out / "rulebook").mkdir(exist_ok=True)
        (self.out / "rulebook" / "strategy_v001.json").write_text(json.dumps(self.rulebook.to_json(), indent=1))
        for n, d in enumerate(self.days):
            rb = self.rulebook  # written before this day started
            taken = apply_rulebook(rb, self.by_day[d], self.markets)
            for x, why in taken:
                self.strategy_log.append({"day": d, "x": x, "why": why, "version": rb.version})
                key = next((r.key for r in rb.rules + rb.fallback if r.matches(x)), None) if x.signal.family != "crt" else None
                if key:
                    self.live[key].append((d, x.r))
            day_r = sum(x.r for x, _ in taken)
            self.history.append({"day": date_of(d), "version": rb.version, "trades": len(taken), "r": round(day_r, 4),
                                 "crt": sum(1 for x, _ in taken if x.signal.family == "crt")})
            # the review: today's experiments join the evidence (all exited by today's last minute)
            last = {i: m.day_last.get(d, -1) for i, m in self.markets.items()}
            for x in self.by_day[d]:
                if x.trade.filled:
                    assert x.trade.exit_i <= last[x.inst], "an experiment outcome from the future"
                    self.stats.add(x)
            for e in self.strategy_log[len(self.strategy_log) - len(taken):]:
                e["lesson"] = lesson(e["x"], self.stats)   # written the evening of the trade, with evidence to date
            if (n + 1) % rewrite_every == 0:
                self.rewrite(d, last)
