"""Backtest of the owner's opening-range breakout + 1-minute FVG strategy (2026-10-26), on
OANDA's Nasdaq-100 and S&P 500 CFDs (NAS100_USD for NQ, SPX500_USD for ES; Alpaca has no futures).

Every NYSE trading day (Alpaca's calendar):
  1. range: the high and low of the 15-minute candle that opens at 09:30 ET;
  2. direction: the first 5-minute candle (from 09:45) that CLOSES above the range means long,
     below means short. A later 5-minute close beyond the other side, before any entry, is
     handled by ``--flip``: ``switch`` (take the new direction), ``cancel`` (no trade that day)
     or ``keep`` (ignore it) [the owner asked for this to be explained; all three are reported];
  3. entry: the first 1-minute fair value gap in that direction whose three candles all open
     after the 5-minute close (bullish: candle 1's high below candle 3's low; bearish: candle
     1's low above candle 3's high), any size; market entry at the next candle's open;
  4. stop at the middle candle's wick (its low for longs, high for shorts), target at 2R;
  5. one trade a day; no entry after the day's close (16:00 ET, 13:00 on half days) [Bot];
  6. held until the stop or the target, overnight and over weekends; a gap through either
     fills at the open.
Prices: setups on mid candles; fills on the bid/ask (longs buy the ask and sell the bid), so the
spread OANDA charged at the time is the cost. A 1-minute candle that reaches both the stop and the
target is replayed on 5-second candles to see which came first (owner: count whichever was hit
first); if both fall inside one 5-second candle, the stop is counted. A day whose entry leaves the
stop on the wrong side of the entry price skips that gap and keeps looking.

    python -m tradingbot.live.orb_fvg_backtest --start 2021-01-04 [--instruments NAS100_USD,SPX500_USD]
"""
from __future__ import annotations

import argparse
import gzip
import json
import pickle
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import numpy as np

from .broker import Paper
from .oanda import Practice, _rfc3339
from .signals import NY

CACHE = Path.home() / ".cache" / "tradingbot" / "oanda"
STUDIES = Path(__file__).resolve().parent.parent.parent / "journal" / "studies"
RISK_DOLLARS = 10.0
FIELDS = ("o", "h", "l", "c")


def _epoch(t: str) -> int:
    return int(datetime.fromisoformat(t[:19] + "+00:00").timestamp())


def fetch(p: Practice, instrument: str, granularity: str, start: datetime, end: datetime) -> dict[str, np.ndarray]:
    """Mid, bid and ask candles (complete ones only) as arrays keyed t, mo..mc, bo..bc, ao..ac."""
    rows, frm = [], start
    while frm < end:
        got = p._call("GET", f"/v3/instruments/{instrument}/candles?granularity={granularity}&price=MBA"
                             f"&from={_rfc3339(frm)}&count=5000")["candles"]
        # OANDA returns the candle containing ``from``, so the last one comes back again
        last = rows[-1][0] if rows else -1
        got = [c for c in got if c["complete"] and last < _epoch(c["time"]) < end.timestamp()]
        if not got:
            break
        for c in got:
            rows.append([_epoch(c["time"])] + [float(c[k][f]) for k in ("mid", "bid", "ask") for f in FIELDS])
        frm = datetime.fromtimestamp(rows[-1][0] + 1, timezone.utc)
    a = np.array(rows) if rows else np.zeros((0, 13))
    keys = ["t"] + [k + f for k in ("m", "b", "a") for f in FIELDS]
    return {k: (a[:, i].astype(np.int64) if k == "t" else a[:, i]) for i, k in enumerate(keys)}


def minutes(p: Practice, instrument: str, start: date, end: date) -> dict[str, np.ndarray]:
    """1-minute candles, cached by month."""
    CACHE.mkdir(parents=True, exist_ok=True)
    parts, m = [], date(start.year, start.month, 1)
    while m <= end:
        nxt = date(m.year + (m.month == 12), m.month % 12 + 1, 1)
        path = CACHE / f"{instrument}_M1_{m:%Y-%m}.pkl.gz"
        complete = nxt <= datetime.now(timezone.utc).date()
        if path.exists():
            parts.append(pickle.load(gzip.open(path)))
        else:
            d = fetch(p, instrument, "M1", datetime(m.year, m.month, 1, tzinfo=timezone.utc),
                      min(datetime(nxt.year, nxt.month, 1, tzinfo=timezone.utc), datetime.now(timezone.utc)))
            if complete:
                pickle.dump(d, gzip.open(path, "wb"))
            parts.append(d)
            print(f"  {instrument} {m:%Y-%m}: {len(d['t'])} candles", flush=True)
        m = nxt
    return {k: np.concatenate([x[k] for x in parts]) for k in parts[0]}


class Seconds:
    """5-second candles for one minute, fetched on demand and cached."""

    def __init__(self, p: Practice, instrument: str):
        self.p, self.instrument = p, instrument
        self.path = CACHE / f"{instrument}_S5.json"
        self.cache = json.loads(self.path.read_text()) if self.path.exists() else {}

    def __call__(self, t: int) -> list[dict]:
        key = str(t)
        if key not in self.cache:
            s = datetime.fromtimestamp(t, timezone.utc)
            d = fetch(self.p, self.instrument, "S5", s, s + timedelta(minutes=1))
            self.cache[key] = [{k: (int(v[i]) if k == "t" else float(v[i])) for k, v in d.items()} for i in range(len(d["t"]))]
            self.path.write_text(json.dumps(self.cache))
        return self.cache[key]


@dataclass
class Trade:
    day: str
    side: str
    range_high: float
    range_low: float
    breakout_at: str
    flips: int
    entry_at: str
    entry: float
    stop: float
    target: float
    exit_at: str = ""
    exit: float = 0.0
    r: float = 0.0
    outcome: str = "open"
    resolved_by: str = "1m"


def _ny(t: int) -> str:
    return datetime.fromtimestamp(t, timezone.utc).astimezone(NY).strftime("%Y-%m-%d %H:%M")


def _hit(side: int, stop: float, target: float, c: dict, pre: str) -> tuple[str, float] | None:
    """Exit on one candle from the exit side's prices (bid for longs, ask for shorts):
    ('stop'|'target'|'both', price) or None."""
    o, h, l = c[pre + "o"], c[pre + "h"], c[pre + "l"]
    if side > 0:
        if o <= stop:
            return "stop", o
        if o >= target:
            return "target", o
        s, t = l <= stop, h >= target
    else:
        if o >= stop:
            return "stop", o
        if o <= target:
            return "target", o
        s, t = h >= stop, l <= target
    if s and t:
        return "both", 0.0
    return ("stop", stop) if s else ("target", target) if t else None


def exit_trade(tr: Trade, side: int, m: dict, e: int, seconds: Seconds) -> None:
    pre = "b" if side > 0 else "a"
    for i in range(e, len(m["t"])):
        c = {k: m[k][i] for k in m}
        hit = _hit(side, tr.stop, tr.target, c, pre)
        if hit is None:
            continue
        kind, price = hit
        if kind == "both":
            tr.resolved_by = "5s"
            kind, price = "stop", tr.stop
            for s in seconds(int(m["t"][i])):
                h2 = _hit(side, tr.stop, tr.target, s, pre)
                if h2 is None:
                    continue
                kind, price = h2
                if kind == "both":
                    tr.resolved_by = "5s-both"
                    kind, price = "stop", tr.stop
                break
        tr.exit_at, tr.exit, tr.outcome = _ny(int(m["t"][i])), price, kind
        tr.r = round(side * (price - tr.entry) / abs(tr.entry - tr.stop), 3)
        return


def day_trade(m: dict, day: date, close_et: str, flip: str, seconds: Seconds) -> Trade | None:
    t = m["t"]
    open_ = int(datetime.combine(day, datetime.strptime("09:30", "%H:%M").time(), NY).timestamp())
    close = int(datetime.combine(day, datetime.strptime(close_et, "%H:%M").time(), NY).timestamp())
    i0, i15 = np.searchsorted(t, open_), np.searchsorted(t, open_ + 900)
    if i15 - i0 < 10:  # missing data
        return None
    hi, lo = float(m["mh"][i0:i15].max()), float(m["ml"][i0:i15].min())

    side, armed, flips, breakout = 0, None, 0, ""
    j = i15  # next 1-minute candle that could be an FVG's candle 1
    w = open_ + 900
    while w < close:
        end = w + 300
        if side:
            # gaps whose candle 3 has closed by the end of this 5-minute candle
            while j + 3 < len(t) and t[j + 2] + 60 <= end and t[j + 3] < close:
                if t[j] >= armed:
                    c1h, c1l, c3h, c3l = m["mh"][j], m["ml"][j], m["mh"][j + 2], m["ml"][j + 2]
                    gap = c1h < c3l if side > 0 else c1l > c3h
                    if gap:
                        e = j + 3
                        entry = float(m["ao"][e] if side > 0 else m["bo"][e])
                        stop = float(m["ml"][j + 1] if side > 0 else m["mh"][j + 1])
                        if side * (entry - stop) > 0:
                            tr = Trade(str(day), "long" if side > 0 else "short", hi, lo, breakout, flips,
                                       _ny(int(t[e])), entry, stop, entry + side * 2 * abs(entry - stop))
                            exit_trade(tr, side, m, e, seconds)
                            return tr
                j += 1
        a, b = np.searchsorted(t, w), np.searchsorted(t, end)
        if b > a:
            c = m["mc"][b - 1]
            new = 1 if c > hi else -1 if c < lo else 0
            if new and not side:
                side, armed, breakout = new, end, _ny(end)
                j = b
            elif new and new == -side:
                if flip == "cancel":
                    return None
                if flip == "switch":
                    side, armed, flips = new, end, flips + 1
                    j = b
        w = end
    return None


def report(trades: list[Trade], instrument: str, flip: str) -> dict:
    done = [x for x in trades if x.outcome != "open"]
    rs = np.array([x.r for x in done]) if done else np.zeros(0)
    eq = np.cumsum(rs) if len(rs) else np.zeros(1)
    dd = float((np.maximum.accumulate(np.concatenate([[0], eq])) - np.concatenate([[0], eq])).max())
    years = {}
    for x in done:
        years.setdefault(x.day[:4], []).append(x.r)
    stops = [abs(x.entry - x.stop) for x in done]
    return {"instrument": instrument, "flip": flip, "trades": len(done), "open": len(trades) - len(done),
            "wins": int((rs > 0).sum()), "win_rate": round(float((rs > 0).mean()) * 100, 1) if len(rs) else 0,
            "total_r": round(float(rs.sum()), 2), "avg_r": round(float(rs.mean()), 3) if len(rs) else 0,
            "dollars_at_10": round(float(rs.sum()) * RISK_DOLLARS, 2), "max_drawdown_r": round(dd, 2),
            "median_stop_points": round(float(np.median(stops)), 2) if stops else 0,
            "by_year": {y: {"trades": len(v), "total_r": round(sum(v), 2), "win_rate": round(100 * sum(r > 0 for r in v) / len(v), 1)}
                        for y, v in sorted(years.items())},
            "resolved_on_5s": sum(x.resolved_by != "1m" for x in done),
            "both_in_one_5s": sum(x.resolved_by == "5s-both" for x in done)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2021-01-04")
    ap.add_argument("--end", default=str(datetime.now(timezone.utc).date()))
    ap.add_argument("--instruments", default="NAS100_USD,SPX500_USD")
    ap.add_argument("--flips", default="switch,cancel,keep")
    args = ap.parse_args()
    start, end = date.fromisoformat(args.start), date.fromisoformat(args.end)
    p = Practice()
    cal = Paper()._call("GET", f"/v2/calendar?start={start}&end={end}")
    days = [(date.fromisoformat(d["date"]), d["close"]) for d in cal]
    STUDIES.mkdir(parents=True, exist_ok=True)
    out = {"strategy": __doc__.split("\n\n")[0], "start": str(start), "end": str(end), "results": []}
    for ins in args.instruments.split(","):
        m = minutes(p, ins, start, end + timedelta(days=7))
        seconds = Seconds(p, ins)
        for flip in args.flips.split(","):
            trades = [x for d, c in days if (x := day_trade(m, d, c, flip, seconds))]
            r = report(trades, ins, flip)
            out["results"].append(r)
            print(json.dumps(r), flush=True)
            path = STUDIES / f"orb_fvg_{ins}_{flip}_trades.jsonl"
            path.write_text("".join(json.dumps(asdict(x)) + "\n" for x in trades))
    (STUDIES / "orb_fvg_backtest.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
