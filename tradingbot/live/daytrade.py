"""Stocks, day trading (owner, 2026-10-28: "a day trading strategy that takes at least 2 trades a day
and at most 5"): the 3 strongest stocks at 10:00 ET, held to the close (H63, a live experiment).

At the first minute after 10:00 ET: among 150 liquid stocks (journal/studies/research_2026-10-28),
the 3 with the biggest gain from today's open to the 09:55 candle's close (price >= $5) are bought at
market, each 10% of equity, with a stop at the day's low so far (one-triggers-other, day orders).
Everything is closed by the session's verified flatten at 15:55 ET. Long only.

Evidence (be honest): on 2 years of 5-minute data (2024-11 to 2026-10) +8 bps a trade after 3 bps a side,
51% winners, t = 1.1 (indistinguishable from zero); +6.7 bps with the day-low stop; negative with
10 bps costs; it fades by 10:30. Every other day-trading rule tested was worse: stocks-in-play opening
range breakout (Zarattini et al.) about 0R at best after costs, intraday reversal, gap fades, gap-and-go,
open-to-close versions of the daily pullback signals, and trading the NAS100 high/low predictor.
"""
from __future__ import annotations

import json
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ..data import fetch_bars_multi
from .broker import BrokerError
from .signals import NY

ROOT = Path(__file__).resolve().parent.parent.parent / "journal" / "trading" / "day"
UNIVERSE = json.loads((Path(__file__).resolve().parent / "day_universe.json").read_text())
STRATEGY, PICKS, POSITION_PCT, ENTRY_AT = "day_rs3", 3, 10.0, (10, 0)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _append(name: str, obj: dict) -> None:
    with (ROOT / name).open("a") as f:
        f.write(json.dumps(obj) + "\n")


def rank(bars: dict[str, list], today: str) -> list[tuple[float, str, float, float]]:
    """(gain since the open, symbol, last price, day's low) for each stock with today's 09:30 candle,
    strongest first. Uses closed candles only."""
    out = []
    for sym, bs in bars.items():
        day = [c for c in bs if c.closed and datetime.fromisoformat(c.t.replace("Z", "+00:00")).astimezone(NY).date().isoformat() == today]
        day = [c for c in day if (lambda n: (n.hour, n.minute) >= (9, 30))(datetime.fromisoformat(c.t.replace("Z", "+00:00")).astimezone(NY))]
        if not day or not day[0].t or day[0].o < 5:
            continue
        first = datetime.fromisoformat(day[0].t.replace("Z", "+00:00")).astimezone(NY)
        if (first.hour, first.minute) != (9, 30):
            continue
        out.append((day[-1].c / day[0].o - 1, sym, day[-1].c, min(c.l for c in day)))
    return sorted(out, reverse=True)


class DayTrade:
    def __init__(self, broker, dry_run: bool = False):
        self.broker, self.dry_run = broker, dry_run
        ROOT.mkdir(parents=True, exist_ok=True)
        self.path = ROOT / "state.json"
        s = json.loads(self.path.read_text()) if self.path.exists() else {}
        today = datetime.now(NY).date().isoformat()
        self.day = s.get("day") if s.get("day") == today else today
        self.trades: list[dict] = s.get("trades", []) if s.get("day") == today else []
        self.entered = bool(s.get("entered")) if s.get("day") == today else False

    def save(self) -> None:
        self.path.write_text(json.dumps({"day": self.day, "entered": self.entered, "trades": self.trades}, indent=1))

    def tick(self) -> None:
        n = datetime.now(NY)
        if self.entered or (n.hour, n.minute) < ENTRY_AT or (n.hour, n.minute) >= (10, 30):
            return
        self.entered = True
        self.save()
        try:
            bars = {}
            for i in range(0, len(UNIVERSE), 50):
                bars.update(fetch_bars_multi(UNIVERSE[i:i + 50], "5Min", _now() - timedelta(hours=3)))
        except Exception as e:
            _append("events.jsonl", {"t": _now().isoformat(timespec="seconds"), "what": f"data error: {e}", "impact": "no trades today"})
            return
        ranked = rank(bars, self.day)
        _append("decisions.jsonl", {"t": _now().isoformat(timespec="seconds"), "top10": [(round(g, 4), s) for g, s, _, _ in ranked[:10]],
                                    "stocks_ranked": len(ranked)})
        acct = self.broker.account()
        equity, bp = float(acct["equity"]), float(acct["buying_power"])
        for gain, sym, px, low in ranked[:PICKS]:
            qty = int(min(equity * POSITION_PCT / 100, bp * 0.9) / px)
            stop = math.floor(low * 100) / 100 - 0.01
            if qty < 1 or stop >= px:
                continue
            t = {"symbol": sym, "gain_at_10": round(gain, 4), "signal_price": px, "stop": stop, "qty": qty,
                 "risk_pct_of_equity": round((px - stop) * qty / equity * 100, 3), "cid": f"{STRATEGY}-{self.day}-{sym}", "order_id": None}
            if not self.dry_run:
                try:
                    t["order_id"] = self.broker.oto(sym, qty, "buy", stop, t["cid"])["id"]
                except BrokerError as e:
                    _append("events.jsonl", {"t": _now().isoformat(timespec="seconds"), "what": f"order refused {sym}: {e}"})
                    continue
            self.trades.append(t)
            bp -= qty * px
            _append("trades.jsonl", {"type": "entry_submitted", "t": _now().isoformat(timespec="seconds"), **t})
        self.save()

    def record(self) -> None:
        """After the flatten: entry and exit fills from Alpaca, result in R (1R = entry to stop) and $."""
        if self.dry_run:
            return
        try:
            closed = self.broker.orders("closed", after=f"{self.day}T13:00:00Z")
        except BrokerError:
            return
        for t in self.trades:
            if t.get("result") or not t.get("order_id"):
                continue
            try:
                o = self.broker.order(t["order_id"])
            except BrokerError:
                continue
            if not o.get("filled_avg_price"):
                t["result"] = "not filled"
                continue
            entry, qty = float(o["filled_avg_price"]), float(o["filled_qty"])
            sells = [x for x in closed if x["symbol"] == t["symbol"] and x["side"] == "sell" and x.get("filled_avg_price")]
            stop_leg = [l for l in (o.get("legs") or []) if l.get("filled_avg_price")]
            fills = [(float(x["filled_avg_price"]), float(x["filled_qty"])) for x in (stop_leg or sells)]
            if not fills:
                continue
            exit_px = sum(p * q for p, q in fills) / sum(q for _, q in fills)
            pnl = round((exit_px - entry) * qty, 2)
            r = round((exit_px - entry) / (entry - t["stop"]), 3) if entry > t["stop"] else None
            t["result"] = {"entry": entry, "exit": round(exit_px, 4), "how": "stop" if stop_leg else "close", "pnl": pnl, "r": r,
                           "return_bps": round((exit_px / entry - 1) * 1e4, 1)}
            _append("trades.jsonl", {"type": "exit", "t": _now().isoformat(timespec="seconds"), "symbol": t["symbol"], **t["result"]})
            index = ROOT / "TRADES.md"
            if not index.exists():
                index.write_text("# Day trades (day_rs3: the 3 strongest stocks at 10:00, to the close)\n\n"
                                 "| Day | Stock | Up at 10:00 | Entry | Exit | How | Return | R | P/L |\n|---|---|---|---|---|---|---|---|---|\n")
            with index.open("a") as f:
                f.write(f"| {self.day} | {t['symbol']} | {t['gain_at_10']:+.2%} | {entry:.2f} | {exit_px:.2f} | {t['result']['how']} | "
                        f"{t['result']['return_bps'] / 100:+.2f}% | {r if r is not None else '?'} | {pnl:+,.2f} |\n")
        self.save()
