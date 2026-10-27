"""Paper trading CRT 1h -> 5m on gold and the Nasdaq-100 CFD, on the OANDA practice account,
around the clock (owner, 2026-10-27: "I only want you to do this CRT strategy on NQ and XAUUSD").

    python -m tradingbot.live.fx_run --max-minutes 345   # GitHub Actions (fx-session.yml)
    python -m tradingbot.live.fx_run --dry-run --once     # one assessment, no orders

The rules are crt_owner's, live as in crt_live (clock-hour candles, the day from 18:00 ET):
every fair value gap inside the third 1-hour candle gets two limit orders at its near edge
(half takes profit at 1:1, half at 3R), stop fixed at the gap's middle candle. OANDA holds the
stop and target on each fill and cancels an unfilled order itself when the third candle ends
(good-till-date), so a trade stays protected and on plan between runs. Gaps whose stop is under
3 spreads are skipped (the backtest's tightest stops lost -1.2R a trade). Sizing as on stocks:
at most 1% of equity at risk and 10% of equity in position value per trade.

Records: journal/trading/fx/ (setups.jsonl, trades.jsonl, state.json, events.md, TRADES.md,
trades/*.md). Practice account only (oanda.Practice).
"""
from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from .broker import BrokerError
from .crt_live import crt_assess
from .oanda import INSTRUMENTS, Practice

ROOT = Path(__file__).resolve().parent.parent.parent / "journal" / "trading" / "fx"
NY = ZoneInfo("America/New_York")
TARGET_R, RISK_PCT, POSITION_PCT, MIN_STOP_SPREADS = 3.0, 1.0, 10.0, 3.0
LOOKBACK = timedelta(days=35)
STRATEGY = "crt_fx"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def market_open(now: datetime | None = None) -> bool:
    """Gold and the index CFDs trade Sunday 18:00 to Friday 17:00 New York time, with a daily
    break 17:00-18:00."""
    n = (now or _now()).astimezone(NY)
    wd, hm = n.weekday(), (n.hour, n.minute)
    if wd == 5 or (wd == 4 and hm >= (17, 0)) or (wd == 6 and hm < (18, 0)):
        return False
    return not ((17, 0) <= hm < (18, 0))


def _append(name: str, obj: dict) -> None:
    with (ROOT / name).open("a") as f:
        f.write(json.dumps(obj) + "\n")


def event(what: str, impact: str = "", action: str = "") -> None:
    path = ROOT / "events.md"
    if not path.exists():
        path.write_text("# Events (CRT on OANDA: gold, NAS100)\n\n| UTC | What | Impact | Action |\n|---|---|---|---|\n")
    with path.open("a") as f:
        f.write(f"| {_now():%Y-%m-%d %H:%M} | {what} | {impact} | {action} |\n")


@dataclass
class Trade:
    instrument: str
    setup_t: str
    direction: int
    entry: float
    stop: float
    targets: list[float]
    expires_at: str
    parts: list[dict] = field(default_factory=list)  # {client_id, order_id, units, target, trade_id}
    closed: bool = False
    page: str = ""


def page(a: dict, trade: Trade, units: float, risk_usd: float, equity: str) -> Path:
    folder = ROOT / "trades"
    folder.mkdir(parents=True, exist_ok=True)
    p, ctx = a["plan"], a["context"]
    path = folder / f"{a['t'][:16].replace(':', '').replace('T', '_')}_{a['symbol']}.md"
    lines = [f"# {a['symbol']} {p['direction']} · CRT 1h → 5m · setup candle {a['t']} UTC", "",
             "## Why the bot took it", f"- **Setup:** {a['setup']}"]
    lines += [f"- **{x['concept']}:** {x['evidence']}" for x in a["present"]]
    lines += ["", "## Before entry",
              "- **Hypothesis:** H59: the owner's CRT 1h → 5m is profitable on gold and the Nasdaq-100 CFD (OANDA practice).",
              "- **Expected outcome:** backtest (2 × 180 days, 149 trades with stops of 3+ spreads): about −0.10R per trade after the "
              "spread, 30% winners at 3R; any single trade is close to a coin flip.",
              f"- **Invalidated if:** {p['invalidation']}", "",
              "## The plan",
              f"- Entry {p['entry']} ({p['entry_condition']}); stop {p['stop']} (fixed)",
              f"- Half at {p['take_profits'][0]} (1:1), half at {p['take_profits'][1]} ({TARGET_R:g}R)",
              f"- Size {units:g} units, risking about ${risk_usd:,.2f} (max 1% of equity {equity}; position value max 10% of equity)",
              f"- Spread at the decision: {ctx.get('spread')}", "",
              "## Result", "_open_", "", "## What it learned", "_Filled in by the review._", ""]
    path.write_text("\n".join(lines))
    return path


class Session:
    def __init__(self, dry_run: bool = False, max_minutes: float | None = None, broker: Practice | None = None):
        self.dry_run, self.max_minutes = dry_run, max_minutes
        self.broker = broker or Practice()
        self.trades: list[Trade] = []
        self.seen: set[tuple[str, str]] = set()
        self.bars: dict[str, list] = {}
        self.failures = 0
        ROOT.mkdir(parents=True, exist_ok=True)
        self.state_path = ROOT / "state.json"

    # ---- state ----
    def load(self) -> None:
        if self.state_path.exists():
            s = json.loads(self.state_path.read_text())
            self.trades = [Trade(**t) for t in s["trades"]]
            self.seen = {tuple(x) for x in s["seen"]}

    def save(self) -> None:
        cutoff = (_now() - timedelta(days=3)).isoformat()
        self.state_path.write_text(json.dumps({
            "trades": [t.__dict__ for t in self.trades if not t.closed or t.setup_t >= cutoff[:19]],
            "seen": sorted(x for x in self.seen if x[1] >= cutoff[:19])}, indent=1))

    # ---- data ----
    def candles(self, inst: str) -> list:
        have = self.bars.get(inst)
        if not have:
            have = self.broker.candles(inst, "5Min", _now() - LOOKBACK)
        else:
            new = self.broker.candles(inst, "5Min", datetime.fromisoformat(have[-1].t.replace("Z", "+00:00")))
            have = [c for c in have if not new or c.t < new[0].t] + new
        self.bars[inst] = have[-12000:]
        return self.bars[inst]

    # ---- assess + execute ----
    def cycle(self) -> None:
        prices = self.broker.pricing(list(INSTRUMENTS) + ["GBP_USD"])
        for inst in INSTRUMENTS:
            px = prices[inst]
            spread = float(px["asks"][0]["price"]) - float(px["bids"][0]["price"])
            bars = self.candles(inst)
            closed = [c for c in bars if c.closed]
            if not closed or datetime.fromisoformat(closed[-1].t.replace("Z", "+00:00")) + timedelta(minutes=5) < _now() - timedelta(minutes=2):
                continue  # no fresh candle (market closed or thin)
            for a in crt_assess(inst, closed, True, TARGET_R, round_the_clock=True, min_stop=MIN_STOP_SPREADS * spread,
                                strategy=STRATEGY):
                key = (inst, a["t"])
                if key in self.seen:
                    continue
                self.seen.add(key)
                a["context"]["spread"] = round(spread, 5)
                if a["decision"] == "APPROVED":
                    self.approve(a, prices)
                a["dry_run"] = self.dry_run
                _append("setups.jsonl", a)
        self.save()

    def approve(self, a: dict, prices: dict) -> None:
        inst, p = a["symbol"], a["plan"]
        d = 1 if p["direction"] == "long" else -1
        # OANDA nets positions: never an order against an open trade in the other direction.
        if any(t.instrument == inst and not t.closed and t.direction != d for t in self.trades):
            a["decision"], a["reasons"] = "REJECTED", ["an open trade in this instrument goes the other way"]
            return
        acct = self.broker.account()
        gbpusd = float(prices["GBP_USD"]["bids"][0]["price"])
        equity_usd = float(acct["NAV"]) * gbpusd if acct["currency"] == "GBP" else float(acct["NAV"])
        risk = abs(p["entry"] - p["stop"])
        units = min(equity_usd * RISK_PCT / 100 / risk, equity_usd * POSITION_PCT / 100 / p["entry"])
        half = [float(self.broker.units(inst, units / 2)), float(self.broker.units(inst, units - units / 2))]
        minimum = float(self.broker.specs(inst)["minimumTradeSize"])
        parts = [(q, tp) for q, tp in zip(half, p["take_profits"]) if q >= minimum]
        a["size"] = {"equity": acct["NAV"], "currency": acct["currency"], "units": round(sum(q for q, _ in parts), 2),
                     "risk_usd": round(sum(q for q, _ in parts) * risk, 2)}
        if not parts:
            a["decision"], a["reasons"] = "REJECTED", ["size under the instrument's minimum"]
            return
        if self.dry_run:
            return
        trade = Trade(inst, a["t"], d, p["entry"], p["stop"], [tp for _, tp in parts], p["expires_at"])
        expires = datetime.fromisoformat(p["expires_at"])
        for k, (q, tp) in enumerate(parts):
            cid = f"{STRATEGY}-{inst}-{a['t'][:16].replace('-', '').replace(':', '').replace('T', '')}-{k}"
            try:
                o = self.broker.limit_bracket(inst, d * q, p["entry"], tp, p["stop"], cid, expires)
                trade.parts.append({"client_id": cid, "order_id": o["id"], "units": q, "target": tp, "trade_id": None})
            except BrokerError as e:
                self.failures += 1
                event(f"order refused {inst} part {k}: {e}", "part not placed", "recorded")
        if trade.parts:
            path = page(a, trade, a["size"]["units"], a["size"]["risk_usd"], f"{acct['NAV']} {acct['currency']}")
            trade.page = str(path.relative_to(ROOT.parent.parent.parent))
            self.trades.append(trade)
            _append("trades.jsonl", {"type": "entry_submitted", "t": _now().isoformat(timespec="seconds"), "instrument": inst,
                                     "setup_t": a["t"], "plan": p, "parts": trade.parts})
        else:
            a["decision"], a["reasons"] = "REJECTED", ["every part was refused by OANDA"]

    # ---- manage: OANDA holds stops, targets and expiry; this only reconciles and records ----
    def manage(self) -> None:
        for t in self.trades:
            if t.closed:
                continue
            try:
                done, fills, exits = True, [], []
                for part in t.parts:
                    if not part.get("trade_id"):
                        o = self.broker.order(part["order_id"])
                        if o["state"] == "PENDING":
                            done = False
                            continue
                        if o["state"] == "FILLED" and o.get("tradeOpenedID"):
                            part["trade_id"] = o["tradeOpenedID"]
                            _append("trades.jsonl", {"type": "entry_filled", "t": _now().isoformat(timespec="seconds"),
                                                     "instrument": t.instrument, "setup_t": t.setup_t, "part": part["client_id"]})
                        else:
                            continue  # cancelled (expired) or filled into another trade: nothing open
                    tr = self.broker.trade(part["trade_id"])
                    fills.append((float(tr["price"]), abs(float(tr["initialUnits"]))))
                    if tr["state"] != "CLOSED":
                        done = False
                        continue
                    px = float(tr["averageClosePrice"])
                    exits.append((px, abs(float(tr["initialUnits"])), "target" if (px - float(tr["price"])) * t.direction > 0 else "stop",
                                  float(tr.get("realizedPL") or 0)))
            except BrokerError as e:
                event(f"status unavailable {t.instrument}: {e}", "can't reconcile this minute", "retry")
                continue
            if done:
                self.record(t, fills, exits)
        self.save()

    def record(self, t: Trade, fills, exits) -> None:
        t.closed = True
        if not fills:
            _append("trades.jsonl", {"type": "not_filled", "t": _now().isoformat(timespec="seconds"), "instrument": t.instrument,
                                     "setup_t": t.setup_t, "limit": t.entry})
            self._result(t, "- Limit entry not filled before the third candle ended: no trade (0R).")
            return
        units = sum(q for _, q in fills)
        entry = sum(px * q for px, q in fills) / units
        gross = sum((px - entry) * q * t.direction for px, q, _, _ in exits)
        r = gross / (abs(entry - t.stop) * units) if entry != t.stop else None
        pl = round(sum(x[3] for x in exits), 2)
        rec = {"type": "exit", "t": _now().isoformat(timespec="seconds"), "instrument": t.instrument, "setup_t": t.setup_t,
               "entry": round(entry, 5), "stop": t.stop, "targets": t.targets, "exits": [x[:3] for x in exits],
               "units": units, "r": round(r, 3) if r is not None else None, "realized_pl_account_ccy": pl}
        _append("trades.jsonl", rec)
        self._result(t, f"- Entry fill {entry:.5g}, exits " + ", ".join(f"{q:g} @ {px:.5g} ({k})" for px, q, k, _ in exits)
                     + f"\n- **{rec['r']}R**, realized P/L {pl} (account currency)")
        index = ROOT / "TRADES.md"
        if not index.exists():
            index.write_text("# CRT trades on OANDA (gold, NAS100)\n\n| Setup (UTC) | Instrument | Direction | R | P/L (GBP) | Record |\n|---|---|---|---|---|---|\n")
        with index.open("a") as f:
            f.write(f"| {t.setup_t[:16].replace('T', ' ')} | {t.instrument} | {'long' if t.direction == 1 else 'short'} | "
                    f"{rec['r']:+.2f} | {pl:+,.2f} | [page](trades/{Path(t.page).name}) |\n")

    def _result(self, t: Trade, text: str) -> None:
        path = ROOT.parent.parent.parent / t.page if t.page else None
        if path and path.exists():
            path.write_text(path.read_text().replace("## Result\n_open_", "## Result\n" + text))

    # ---- loop ----
    def run(self, once: bool = False) -> None:
        acct = self.broker.account()
        if not acct["id"].startswith("101-"):  # OANDA practice account ids start with 101-
            raise SystemExit(f"refusing account {acct['id'][:4]}...: not a practice account")
        self.load()
        event(f"session start ({'dry run' if self.dry_run else 'practice'}): NAV {acct['NAV']} {acct['currency']}, "
              f"{sum(not t.closed for t in self.trades)} trade(s) open in the state")
        deadline = _now() + timedelta(minutes=self.max_minutes) if self.max_minutes else None
        while True:
            try:
                if market_open() and (once or int(_now().timestamp() // 60) % 5 == 0):
                    self.cycle()
                if not self.dry_run:
                    self.manage()
            except (BrokerError, OSError, KeyError, ValueError) as e:
                event(f"error in the cycle: {e}", "this minute skipped", "retry next minute")
            if once:
                return
            if deadline and _now() >= deadline:
                self.save()
                event("session hand-off (runner time limit)", "orders and trades stay protected at OANDA", "next run resumes")
                return
            if not market_open() and not any(not t.closed for t in self.trades):
                self.save()
                event("market closed and nothing open: session end")
                return
            nxt = (_now() + timedelta(minutes=1)).replace(second=20, microsecond=0)
            while _now() < nxt:
                time.sleep(max(0.5, min(5.0, (nxt - _now()).total_seconds())))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--once", action="store_true", help="one assessment of both instruments, then exit")
    ap.add_argument("--max-minutes", type=float)
    ap.add_argument("--only-when-open", action="store_true", help="exit at once while the market is closed")
    args = ap.parse_args()
    if args.only_when_open and not market_open(_now() + timedelta(minutes=10)):
        print("market closed: nothing to do")
        return
    Session(dry_run=args.dry_run, max_minutes=args.max_minutes).run(once=args.once)


if __name__ == "__main__":
    main()
