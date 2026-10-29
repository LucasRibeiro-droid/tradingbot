"""Pattern mining with the owner's concepts, done by the bot on PAST trades only (walk-forward).

Every experiment trade is described by yes/no conditions built from the concepts (session and hour,
trend on 15m/1h/4h/daily, premium/discount, liquidity pool type, stop size, position in the bot's own
predicted day range, range used so far, volatility regime, previous day's levels, weekday). For each
setup x exit, the miner searches conjunctions of up to 3 conditions (beam search) and keeps those that
were positive in EVERY past year with enough trades, ranked by the worst year (shrunk toward zero).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .market import date_of

PREDICATES = {
    "asia": lambda t: t["session"] == "asia", "london": lambda t: t["session"] == "london",
    "newyork": lambda t: t["session"] == "newyork", "between": lambda t: t["session"] == "between",
    "ny_open": lambda t: t["session"] == "newyork" and 9 <= t["hour"] < 11,
    "ny_midday": lambda t: t["session"] == "newyork" and 11 <= t["hour"] < 14,
    "ny_late": lambda t: t["session"] == "newyork" and t["hour"] >= 14,
    "with_15m": lambda t: t["with_15m"], "with_1h": lambda t: t["with_1h"], "with_4h": lambda t: t["with_4h"],
    "with_D": lambda t: t["with_D"], "against_D": lambda t: t["against_D"], "against_1h": lambda t: t["against_1h"],
    "votes>=3": lambda t: t.get("trend_votes", 0) >= 3, "votes<=1": lambda t: t.get("trend_votes", 0) <= 1,
    "discount": lambda t: t["discount"], "premium": lambda t: not t["discount"],
    "stop>=3sp": lambda t: t.get("stop_sp", 0) >= 3, "stop>=6sp": lambda t: t.get("stop_sp", 0) >= 6,
    "stop>=12sp": lambda t: t.get("stop_sp", 0) >= 12, "stop<6sp": lambda t: t.get("stop_sp", 0) < 6,
    "pred_low_third": lambda t: t.get("pred_pos") is not None and t["pred_pos"] <= 0.33,
    "pred_mid": lambda t: t.get("pred_pos") is not None and 0.33 < t["pred_pos"] < 0.67,
    "pred_high_third": lambda t: t.get("pred_pos") is not None and t["pred_pos"] >= 0.67,
    "range_used<0.5": lambda t: t.get("range_used") is not None and t["range_used"] < 0.5,
    "range_used>=1": lambda t: t.get("range_used") is not None and t["range_used"] >= 1.0,
    "quiet_day": lambda t: t.get("vol_regime", 1) < 0.5, "busy_day": lambda t: t.get("vol_regime", 0) >= 1.0,
    "beyond_pd": lambda t: bool(t.get("beyond_pd")), "inside_pd": lambda t: t.get("beyond_pd") is False,
    "room_pd>=2R": lambda t: (t.get("to_pdh_r") if t.get("side_long") else t.get("to_pdl_r")) is not None and
                             ((t.get("to_pdh_r") if t.get("side_long") else t.get("to_pdl_r")) or 0) >= 2,
    "day_pool": lambda t: "day" in t.get("pool", ""), "session_pool": lambda t: t.get("pool", "").split(" ")[0] in ("asia", "london", "newyork"),
    "prominent_pool": lambda t: t.get("pool", "").startswith("prominent"),
    "long": lambda t: t.get("side_long", False), "short": lambda t: not t.get("side_long", False),
    "mon": lambda t: t.get("dow") == 0, "fri": lambda t: t.get("dow") == 4, "midweek": lambda t: t.get("dow") in (1, 2, 3),
}
NAMES = list(PREDICATES)


def predicate_row(tags: dict) -> np.ndarray:
    return np.array([bool(PREDICATES[n](tags)) for n in NAMES], dtype=bool)


@dataclass
class Pattern:
    group: tuple          # (inst, base, target)
    conds: tuple          # predicate names
    score: float
    n: int
    mean: float
    win: float
    worst_year: float

    @property
    def key(self) -> str:
        return "|".join(self.group) + "|" + "+".join(self.conds or ("all",))

    def describe(self) -> str:
        return f"{self.group[0]} {self.group[1]} ({self.group[2]}) when " + (" and ".join(self.conds) if self.conds else "always")


class Miner:
    """Holds every experiment trade as arrays; mines on the trades that finished before a given day."""

    def __init__(self, xs):
        filled = [x for x in xs if x.trade.filled]
        self.groups = {}
        g = []
        for x in filled:
            k = (x.inst, x.signal.base, x.target)
            g.append(self.groups.setdefault(k, len(self.groups)))
        self.gid = np.array(g)
        self.day = np.array([x.day for x in filled])
        self.year = np.array([int(date_of(x.day)[:4]) for x in filled])
        self.r = np.array([x.r for x in filled])
        self.P = np.array([x.signal.tags["_pred"] for x in filled]) if filled else np.zeros((0, len(NAMES)), bool)
        self.group_names = {v: k for k, v in self.groups.items()}
        order = np.argsort(self.gid, kind="stable")
        bounds = np.searchsorted(self.gid[order], np.arange(len(self.groups) + 1))
        self.by_group = {gi: order[bounds[gi]:bounds[gi + 1]] for gi in range(len(self.groups))}

    def mine(self, before_day: int, beam: int = 5, depth: int = 3, top: int = 40) -> list[Pattern]:
        past_all = self.day < before_day
        if past_all.sum() < 200:
            return []
        yrs = sorted(set(self.year[past_all]))
        if len(yrs) >= 2:
            period = self.year
        else:   # under two years of evidence: the past's two halves stand in for years
            mid = np.median(self.day[past_all])
            period = (self.day >= mid).astype(int)
            yrs = [0, 1]
        out = []
        for gi, gname in self.group_names.items():
            idx = self.by_group[gi]
            idx = idx[self.day[idx] < before_day]
            if len(idx) < 60:
                continue
            r, P, per = self.r[idx], self.P[idx], period[idx]
            per_masks = [per == y for y in yrs]

            def score(mask):
                n = int(mask.sum())
                if n < 40:
                    return None
                worst = 9.0
                for pm in per_masks:
                    mm = mask & pm
                    ny = int(mm.sum())
                    if ny < 12:
                        return None
                    worst = min(worst, float(r[mm].sum()) / (ny + 15))
                rr = r[mask]
                return worst, n, float(rr.mean()), float((rr > 0).mean())

            frontier = [((), np.ones(len(idx), bool))]
            seen = set()
            for _ in range(depth):
                cand = []
                for conds, mask in frontier:
                    for p, pname in enumerate(NAMES):
                        if pname in conds:
                            continue
                        c2 = tuple(sorted(conds + (pname,)))
                        if c2 in seen:
                            continue
                        seen.add(c2)
                        m2 = mask & P[:, p]
                        sc = score(m2)
                        if sc and sc[0] > 0:
                            cand.append((sc, c2, m2))
                cand.sort(key=lambda c: c[0][0], reverse=True)
                for sc, c2, _ in cand[:beam]:
                    out.append(Pattern(gname, c2, sc[0], sc[1], sc[2], sc[3], sc[0]))
                frontier = [(c2, m2) for _, c2, m2 in cand[:beam]]
                if not frontier:
                    break
        out.sort(key=lambda p: p.score, reverse=True)
        return out[:top]
