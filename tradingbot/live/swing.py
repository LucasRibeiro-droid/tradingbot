"""Stocks: buy a pullback in an uptrend, sell into the first strength (H61; the bot's own strategy,
owner 2026-10-28: "find your own strategy in stocks. you decide").

Rule (tested on 10 years of daily data, journal/studies/swing_down3_2026-10-28.md):
  - entry: the stock closes above its 200-day average after 3 lower closes in a row; buy at the
    close (market-on-close order, decided at 15:45 ET on the last price); when more stocks qualify
    than free slots, the deepest 3-day drop first;
  - exit: the first close above the previous day's high, or after 10 trading days, at the close;
  - a 10% stop below the fill (gtc), so each position (10% of equity) risks 1% of equity;
  - at most 10 positions. Long only; held overnight.
Backtest (78 large caps, 2016-2026, 3 bps a side): +40 bps a trade, 69% winners, 3.8 days held;
portfolio +10.8% a year, worst drawdown -16.6% (SPY: +15.0%, -33.8%), similar in 2016-20 and
2021-26. Weak spots: the edge over simply holding the stocks is small, it fades with 10 bps costs
or a next-open entry, and the stock list is today's large caps (survivorship bias).
"""
from __future__ import annotations

import json
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ..data import fetch_bars_multi
from .broker import BrokerError
from .signals import NY

ROOT = Path(__file__).resolve().parent.parent.parent / "journal" / "trading" / "swing"
STRATEGY = "swing_down3"
SLOTS, POSITION_PCT, STOP_PCT, MAX_DAYS, DOWN = 10, 10.0, 10.0, 10, 3
DECIDE_AT = (15, 45)  # market-on-close orders must reach Alpaca before 15:50 ET
UNIVERSE = (
    "AAPL MSFT AMZN GOOGL META NVDA JPM V JNJ WMT PG XOM UNH MA HD CVX ABBV KO PEP MRK COST AVGO ADBE CSCO TMO MCD "
    "ABT CRM ACN NKE DHR LIN TXN NEE WFC PM BMY UPS RTX HON QCOM LOW INTC AMD AMGN IBM CAT GS SBUX BA MMM GE MS BLK "
    "AXP DE ISRG GILD MDT CVS LMT T VZ C MO SO DUK BKNG ORCL NFLX TSLA PFE MU ADI AMAT LRCX KLAC "
    "SPY QQQ IWM DIA MDY XLK XLF XLE XLV XLY XLP XLI XLU XLB SMH XBI KRE XRT GLD TLT EFA EEM").split()


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _append(name: str, obj: dict) -> None:
    with (ROOT / name).open("a") as f:
        f.write(json.dumps(obj) + "\n")


def event(what: str, impact: str = "", action: str = "") -> None:
    path = ROOT / "events.md"
    if not path.exists():
        path.write_text("# Events (stocks: swing_down3)\n\n| UTC | What | Impact | Action |\n|---|---|---|---|\n")
    with path.open("a") as f:
        f.write(f"| {_now():%Y-%m-%d %H:%M} | {what} | {impact} | {action} |\n")


def signal(closes: list[float], price: float) -> float | None:
    """The 3-day drop if ``price`` (today's close) completes the setup, else None. ``closes``:
    earlier daily closes, oldest first (199+ needed for the 200-day average)."""
    if len(closes) < 199:
        return None
    c = closes + [price]
    if price <= sum(c[-200:]) / 200:
        return None
    if not all(c[-1 - k] < c[-2 - k] for k in range(DOWN)):
        return None
    return price / c[-1 - DOWN] - 1


class Swing:
    def __init__(self, broker, dry_run: bool = False):
        self.broker, self.dry_run = broker, dry_run
        ROOT.mkdir(parents=True, exist_ok=True)
        self.path = ROOT / "state.json"
        s = json.loads(self.path.read_text()) if self.path.exists() else {}
        self.positions: dict[str, dict] = s.get("positions", {})
        self.decided: str = s.get("decided", "")

    def save(self) -> None:
        self.path.write_text(json.dumps({"positions": self.positions, "decided": self.decided}, indent=1))

    def daily(self, symbols) -> dict[str, list]:
        """Completed daily bars (SIP, up to yesterday)."""
        today = datetime.now(NY).date().isoformat()
        out = {}
        for i in range(0, len(symbols), 50):
            got = fetch_bars_multi(list(symbols[i:i + 50]), "1Day", _now() - timedelta(days=330),
                                   _now() - timedelta(minutes=20), feed="sip")
            out.update({k: [c for c in v if c.t[:10] < today] for k, v in got.items()})
        return out

    def last_prices(self, symbols) -> dict[str, float]:
        out = {}
        for i in range(0, len(symbols), 50):
            got = fetch_bars_multi(list(symbols[i:i + 50]), "1Min", _now() - timedelta(minutes=30))
            out.update({k: v[-1].c for k, v in got.items() if v})
        return out

    # ---- once a day, 15:45 ET ----
    def decide(self) -> None:
        today = datetime.now(NY).date().isoformat()
        self.decided = today
        try:
            bars = self.daily(UNIVERSE)
            prices = self.last_prices(UNIVERSE)
        except Exception as e:
            event(f"data error at the decision: {e}", "no entries or exits today", "")
            self.save()
            return
        # exits: the first close above yesterday's high, or 10 trading days
        for sym, p in list(self.positions.items()):
            if p["status"] != "open" or sym not in prices or not bars.get(sym):
                continue
            days = sum(1 for c in bars[sym] if c.t[:10] > p["entry_date"]) + 1
            why = ("close above the previous day's high" if prices[sym] > bars[sym][-1].h
                   else f"{MAX_DAYS} trading days" if days >= MAX_DAYS else None)
            if why:
                self.exit(sym, p, why, today)
        # entries
        acct = self.broker.account()
        equity, bp = float(acct["equity"]), float(acct["buying_power"])
        held = {s for s, p in self.positions.items() if p["status"] in ("pending", "open")}
        try:
            held |= {x["symbol"] for x in self.broker.positions()}
        except BrokerError:
            pass
        cands = []
        for sym in UNIVERSE:
            if sym in held or sym not in prices or len(bars.get(sym, [])) < 199:
                continue
            drop = signal([c.c for c in bars[sym]], prices[sym])
            if drop is not None:
                cands.append((drop, sym))
        free = SLOTS - len(held)
        rec = {"t": _now().isoformat(timespec="seconds"), "date": today, "candidates": sorted(cands)[:20], "free_slots": free}
        _append("decisions.jsonl", rec)
        for drop, sym in sorted(cands)[:max(free, 0)]:
            qty = int(min(equity * POSITION_PCT / 100, bp * 0.9) / prices[sym])
            if qty < 1:
                continue
            cid = f"{STRATEGY}-{today}-{sym}-in"
            entry = {"status": "pending", "qty": qty, "entry_date": today, "signal_price": prices[sym], "drop_3d": round(drop, 4),
                     "entry_cid": cid, "entry_id": None, "stop_id": None, "exit_id": None}
            if not self.dry_run:
                try:
                    entry["entry_id"] = self.broker.simple(sym, qty, "buy", cid, time_in_force="cls")["id"]
                except BrokerError as e:
                    event(f"entry refused {sym}: {e}", "not placed", "")
                    continue
            self.positions[sym] = entry
            bp -= qty * prices[sym]
            _append("trades.jsonl", {"type": "entry_submitted", "t": rec["t"], "symbol": sym, "qty": qty,
                                     "signal_price": prices[sym], "drop_3d": round(drop, 4)})
            self.page(sym, entry, bars[sym])
        self.save()

    def exit(self, sym: str, p: dict, why: str, today: str) -> None:
        p["exit_reason"] = why
        if self.dry_run:
            return
        try:
            if p.get("stop_id"):
                self.broker.cancel(p["stop_id"])
                for _ in range(10):  # the stop holds the shares until its cancel lands
                    if self.broker.order(p["stop_id"])["status"] in ("canceled", "filled", "expired"):
                        break
                    import time
                    time.sleep(1)
                if self.broker.order(p["stop_id"])["status"] == "filled":
                    return  # stopped out meanwhile: reconcile records it
            p["exit_id"] = self.broker.simple(sym, int(p["qty"]), "sell", f"{STRATEGY}-{today}-{sym}-out", time_in_force="cls")["id"]
            p["status"] = "exiting"
        except BrokerError as e:
            event(f"exit failed {sym}: {e}", "position stays, stop re-placed at reconcile", "retry tomorrow")

    # ---- every minute: fills, stops, records ----
    def reconcile(self) -> None:
        if self.dry_run:
            return
        for sym, p in list(self.positions.items()):
            try:
                if p["status"] == "pending" and p.get("entry_id"):
                    o = self.broker.order(p["entry_id"])
                    if o["status"] == "filled":
                        p.update(status="open", entry_fill=float(o["filled_avg_price"]), qty=int(float(o["filled_qty"])))
                        _append("trades.jsonl", {"type": "entry_filled", "t": _now().isoformat(timespec="seconds"), "symbol": sym,
                                                 "price": p["entry_fill"], "qty": p["qty"]})
                    elif o["status"] in ("canceled", "expired", "rejected"):
                        p["status"] = "not_filled"
                        _append("trades.jsonl", {"type": "not_filled", "t": _now().isoformat(timespec="seconds"), "symbol": sym})
                if p["status"] == "open" and not p.get("stop_id"):
                    stop = round(p["entry_fill"] * (1 - STOP_PCT / 100), 2)
                    p["stop_id"] = self.broker.simple(sym, p["qty"], "sell", f"{STRATEGY}-{p['entry_date']}-{sym}-stop",
                                                      time_in_force="gtc", order_type="stop", stop_price=stop)["id"]
                    p["stop"] = stop
                if p["status"] in ("open", "exiting"):
                    for key, kind in (("exit_id", "close"), ("stop_id", "stop")):
                        if p.get(key):
                            o = self.broker.order(p[key])
                            if o["status"] == "filled":
                                self.record(sym, p, float(o["filled_avg_price"]), kind)
                                break
                    else:
                        if p["status"] == "exiting" and self.broker.order(p["exit_id"])["status"] in ("canceled", "expired", "rejected"):
                            p.update(status="open", stop_id=None)  # exit didn't happen: protect again, retry tomorrow
            except BrokerError as e:
                event(f"reconcile {sym}: {e}", "retry next minute", "")
        self.positions = {s: p for s, p in self.positions.items() if p["status"] not in ("closed", "not_filled")}
        self.save()

    def record(self, sym: str, p: dict, px: float, kind: str) -> None:
        p["status"] = "closed"
        ret = px / p["entry_fill"] - 1
        pnl = round((px - p["entry_fill"]) * p["qty"], 2)
        r = round(ret / (STOP_PCT / 100), 3)  # 1R = the 10% stop
        rec = {"type": "exit", "t": _now().isoformat(timespec="seconds"), "symbol": sym, "entry": p["entry_fill"],
               "exit": px, "qty": p["qty"], "kind": kind, "reason": p.get("exit_reason", "stop"), "return_pct": round(ret * 100, 3),
               "r": r, "pnl": pnl, "entry_date": p["entry_date"]}
        _append("trades.jsonl", rec)
        page = ROOT / "trades" / f"{p['entry_date']}_{sym}.md"
        if page.exists():
            page.write_text(page.read_text().replace("## Result\n_open_", f"## Result\n- Bought {p['entry_fill']}, sold {px} "
                                                     f"({rec['reason']}): {ret:+.2%}, ${pnl:+,.2f}, {r:+.2f}R"))
        index = ROOT / "TRADES.md"
        if not index.exists():
            index.write_text("# Stock trades (swing_down3)\n\n| Bought | Stock | Return | R | P/L | Exit | Record |\n|---|---|---|---|---|---|---|\n")
        with index.open("a") as f:
            f.write(f"| {p['entry_date']} | {sym} | {ret:+.2%} | {r:+.2f} | {pnl:+,.2f} | {rec['reason']} | [page](trades/{page.name}) |\n")

    def page(self, sym: str, p: dict, bars) -> None:
        folder = ROOT / "trades"
        folder.mkdir(exist_ok=True)
        c = [x.c for x in bars]
        sma = (sum(c[-199:]) + p["signal_price"]) / 200
        (folder / f"{p['entry_date']}_{sym}.md").write_text("\n".join([
            f"# {sym} long · swing_down3 · {p['entry_date']}", "",
            "## Why the bot took it",
            f"- 3 lower closes in a row: {c[-3]:.2f} → {c[-2]:.2f} → {c[-1]:.2f} → {p['signal_price']:.2f} (last price at 15:45 ET), "
            f"{p['drop_3d']:+.2%} in 3 days",
            f"- Still above its 200-day average ({sma:.2f}): a pullback inside an uptrend", "",
            "## Before entry",
            "- **Hypothesis:** H61: buying 3-day pullbacks in stocks above their 200-day average and selling the first strong close is "
            "profitable after costs.",
            "- **Expected:** backtest +40 bps a trade, 69% winners, about 4 days held; any single trade is uncertain (31% lose).",
            f"- **Plan:** buy {p['qty']} at the close (market-on-close); sell at the first close above the previous day's high or after "
            f"{MAX_DAYS} days; stop 10% below the fill (risk 1% of equity).", "",
            "## Result", "_open_", "", "## What it learned", "_Filled in by the review._", ""]))

    def tick(self) -> None:
        n = datetime.now(NY)
        today = n.date().isoformat()
        if n.weekday() < 5 and (n.hour, n.minute) >= DECIDE_AT and (n.hour, n.minute) < (15, 50) and self.decided != today:
            self.decide()
        self.reconcile()
