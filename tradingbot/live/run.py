"""One paper-trading session: screen, then assess / execute / manage / record until the close.

    python -m tradingbot.live.run            # trade on the paper account
    python -m tradingbot.live.run --dry-run  # assess and record, place no orders
    python -m tradingbot.live.run --max-minutes 345  # hand off before a runner's time limit

A session can stop and restart at any time: the watchlist and state files resume it, Alpaca
holds every stop and take profit (gtc brackets), and start/flatten reconcile with Alpaca.

Cycle (owner's brief, section 11), every ``execution_tf`` candle close:
  1. assess each watched stock (signals.assess): APPROVED or REJECTED, recorded in setups.jsonl
  2. execute an approved setup: size at the owner's 1% risk, one bracket order per take profit
     (Day 37 ladder; Alpaca brackets carry one take profit each), at most
     ``max_instruments_per_day`` different stocks a day if set (owner: no limit since 2026-10-21)
  3. manage: after the first take profit fills, move the other parts' stops to break even
     (Day 18 example); reconcile every order with Alpaca, never assume a fill
  4. record entries, exits, P/L in R, MFE/MAE in trades.jsonl; incidents in events.md
At ``flatten_at`` everything is closed and a review skeleton is written. Owner's settings: no
daily loss limit and no trade cap. Technical failures (3 failed submissions) stop new entries.
"""
from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from ..config import BASELINE, Config
from ..data import fetch_bars, timeframe_length
from .broker import BrokerError, Paper
from .screener import screen
from .signals import assess, size, split

ROOT = Path(__file__).resolve().parent.parent.parent / "journal" / "trading"
NY = ZoneInfo("America/New_York")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _append(path: Path, obj: dict) -> None:
    with path.open("a") as f:
        f.write(json.dumps(obj) + "\n")


def trade_page(a: dict, parts: list[dict], dry_run: bool) -> Path:
    """The readable record of one trade (the owner reads these): why it was taken and the plan.
    The result and what was learned are added at the exit and in the after-close review."""
    folder = ROOT / "trades"
    folder.mkdir(exist_ok=True)
    stamp = a["t"][:16].replace(":", "").replace("T", "_")
    path = folder / f"{stamp}_{a['symbol']}.md"
    p, ctx = a["plan"], a["context"]
    lines = [f"# {a['symbol']} {p['direction']} · setup candle {a['t']} UTC" + (" · DRY RUN" if dry_run else ""), "",
             "## Why the bot took it", f"- **Setup:** {a['setup']}"]
    lines += [f"- **{x['concept']}:** {x['evidence']}" for x in a["present"]]
    lines += [f"- **Conflicting – {x['concept']}:** {x['evidence']}" for x in a["conflicts"]]
    lines += [f"- **Daily bias relation:** {ctx['bias_relation']} (traded either way since 2026-10-21; every trade tests it)",
              f"- **Decision:** {a['decision']}", "",
              "## The plan",
              f"- Entry {p['entry']} ({p['entry_condition']}); stop {p['stop']}: {p['invalidation']}",
              f"- Take profits {', '.join(f'{x:.2f}' for x in p['take_profits'])}: first at {p['rr_first']}R, last at {p['rr_last']}R",
              f"- Size: {a['size']['qty']} shares, risking ${a['size']['risk_dollars']} (1% of equity {a['size']['equity']}), "
              f"in {len(parts)} parts: " + ", ".join(f"{x['qty']} @ {x['target']:.2f}" for x in parts),
              "", "## Result", "_open_", "", "## What it learned", "_written in the after-close review_", ""]
    path.write_text("\n".join(lines))
    return path


def finish_page(path: Path, exit_rec: dict) -> None:
    """Fill in the result section and the index row (journal/trading/TRADES.md)."""
    if not path.exists():
        return
    res = (f"- Entry fill {exit_rec['entry']}, exits " + ", ".join(f"{q:g} @ {px} ({kind})" for px, q, kind in exit_rec["exits"])
           + f"\n- P/L ${exit_rec['pnl']}, **{exit_rec['r']}R**; stop moved to break even: {exit_rec['be_moved']}")
    path.write_text(path.read_text().replace("## Result\n_open_", "## Result\n" + res))
    index = ROOT / "TRADES.md"
    if not index.exists():
        index.write_text("# Trades\n\nEvery trade the bot takes: why, result, lesson (click the trade).\n\n"
                         "| Date (UTC) | Stock | Direction | Bias relation | R | P/L | Record |\n|---|---|---|---|---|---|---|\n")
    head = path.read_text().splitlines()[0]
    rel = next((l.split(":** ")[1].split(" ")[0] for l in path.read_text().splitlines() if l.startswith("- **Daily bias relation")), "")
    with index.open("a") as f:
        f.write(f"| {exit_rec['t'][:16]} | {exit_rec['symbol']} | {head.split(' ')[2]} | {rel} | {exit_rec['r']} | {exit_rec['pnl']} | [page](trades/{path.name}) |\n")


def event(what: str, impact: str = "", action: str = "") -> None:
    with (ROOT / "events.md").open("a") as f:
        f.write(f"| {_now().strftime('%Y-%m-%d %H:%M')} | {what} | {impact} | {action} |\n")


@dataclass
class Trade:
    symbol: str
    setup_t: str
    direction: int
    planned_entry: float
    stop: float
    targets: list[float]
    parts: list[dict] = field(default_factory=list)  # {client_id, order_id, qty, target}
    entry_fill: float | None = None
    be_moved: bool = False
    closed: bool = False
    page: str = ""


class Session:
    def __init__(self, config: Config = BASELINE, dry_run: bool = False, max_minutes: float | None = None):
        self.config = config
        self.dry_run = dry_run
        self.max_minutes = max_minutes
        self.broker = Paper()
        self.trades: list[Trade] = []
        self.traded_symbols: set[str] = set()
        self.seen: set[tuple[str, str]] = set()
        self.failures = 0
        self.halted = False
        self.watch: list[str] = []
        self.today = datetime.now(NY).strftime("%Y-%m-%d")
        self.state_path = ROOT / f"state_{self.today}.json"

    # ---- start ----
    def start(self) -> dict:
        acct = self.broker.connect()
        self.shorting = bool(acct.get("shorting_enabled"))
        event(f"session start ({'dry run' if self.dry_run else 'paper'}): equity {acct['equity']}, "
              f"buying power {acct['buying_power']}, shorting {'on' if self.shorting else 'off'}")
        wl = ROOT / f"watchlist_{self.today}.json"
        if wl.exists():
            result = json.loads(wl.read_text())
        else:
            result = screen(self.config, self.shorting, buying_power=float(acct["buying_power"]))
            wl.write_text(json.dumps(result, indent=1))
        self.watch = [r["symbol"] for r in result["watch"]]
        self._load_state()
        self._reconcile_start()
        return acct

    def _reconcile_start(self) -> None:
        """After a restart, Alpaca is the truth: count today's filled symbols toward the instrument
        cap, and report positions the saved state doesn't know (it was lost before a save)."""
        if self.dry_run:
            return
        open_ny = datetime.now(NY).replace(hour=0, minute=0, second=0, microsecond=0)
        try:
            orders = self.broker.orders(status="all", after=open_ny.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
            positions = self.broker.positions()
        except BrokerError as e:
            event(f"start reconcile unavailable: {e}", "instrument cap from saved state only", "")
            return
        filled = {o["symbol"] for o in orders if float(o.get("filled_qty") or 0) > 0}
        self.traded_symbols |= filled
        known = {t.symbol for t in self.trades if not t.closed}
        for pos in positions:
            if pos["symbol"] not in known:
                event(f"position {pos['symbol']} {pos['qty']} at Alpaca is not in the saved state",
                      "not managed by this session (its bracket stop and take profit stay live at Alpaca)",
                      "closed at flatten; reconcile in the review")

    def _load_state(self) -> None:
        if self.state_path.exists():
            s = json.loads(self.state_path.read_text())
            self.trades = [Trade(**t) for t in s["trades"]]
            self.traded_symbols = set(s["traded_symbols"])
            self.seen = {tuple(x) for x in s["seen"]}

    def _save_state(self) -> None:
        self.state_path.write_text(json.dumps({"trades": [t.__dict__ for t in self.trades],
                                               "traded_symbols": sorted(self.traded_symbols),
                                               "seen": sorted(self.seen)}, indent=1))

    # ---- assess + execute ----
    def cycle(self) -> None:
        tp = self.config.trading
        now = _now()
        ltf_len, tp_len = timeframe_length(tp.execution_tf), timeframe_length(tp.take_profit_tf)
        for sym in self.watch:
            try:
                ltf = fetch_bars(sym, tp.execution_tf, now - timedelta(days=20))
                htf = fetch_bars(sym, tp.take_profit_tf, now - timedelta(days=60))
                daily = fetch_bars(sym, "1Day", now - timedelta(days=200))
            except Exception as e:
                event(f"data error {sym}: {e}", "symbol skipped this cycle", "retry next cycle")
                continue
            if not ltf or (now - datetime.fromisoformat(ltf[-1].t.replace("Z", "+00:00"))) > timedelta(hours=1):
                continue  # stale or no data: never act on it
            a = assess(sym, ltf, htf, daily, self.config, self.shorting, ltf_len, tp_len)
            if a is None or (sym, a["t"]) in self.seen:
                continue
            self.seen.add((sym, a["t"]))
            if a["decision"] == "APPROVED":
                self._approve(a)
            a["dry_run"] = self.dry_run
            _append(ROOT / "setups.jsonl", a)
        self._save_state()

    def _approve(self, a: dict) -> None:
        tp = self.config.trading
        sym, plan = a["symbol"], a["plan"]
        if self.halted:
            a["decision"], a["reasons"] = "REJECTED", ["new entries halted after technical failures"]
            return
        cap = tp.max_instruments_per_day
        if cap is not None and sym not in self.traded_symbols and len(self.traded_symbols) >= cap:
            a["decision"], a["reasons"] = "REJECTED", [f"already traded {cap} instruments today"]
            return
        if any(t.symbol == sym and not t.closed for t in self.trades):
            a["decision"], a["reasons"] = "REJECTED", ["a position in this stock is still open"]
            return
        acct = self.broker.account()
        qty = size(float(acct["equity"]), float(acct["buying_power"]), plan["entry"], plan["stop"],
                   tp.risk_per_trade_pct, tp.max_position_pct)
        parts = split(qty, plan["take_profits"])
        a["size"] = {"equity": acct["equity"], "buying_power": acct["buying_power"], "qty": qty,
                     "risk_dollars": round(qty * abs(plan["entry"] - plan["stop"]), 2), "parts": parts}
        if not parts:
            a["decision"], a["reasons"] = "REJECTED", ["can't size: risk, position or buying-power limit allows less than one share"]
            return
        if self.dry_run:
            return
        d = 1 if plan["direction"] == "long" else -1
        trade = Trade(sym, a["t"], d, plan["entry"], plan["stop"], [t for _, t in parts])
        for k, (q, target) in enumerate(parts):
            cid = f"tjr-{self.today}-{sym}-{a['t'][11:16].replace(':', '')}-{k}"
            try:
                o = self.broker.bracket(sym, q, "buy" if d == 1 else "sell", target, plan["stop"], cid)
                trade.parts.append({"client_id": cid, "order_id": o["id"], "qty": q, "target": target})
            except BrokerError as e:
                self.failures += 1
                event(f"order rejected {sym} part {k}: {e}", "part not placed", "recorded; trade continues with placed parts")
                if self.failures >= 3:
                    self.halted = True
                    event("3 failed submissions: new entries halted", "no new trades today", "review before next session")
        if trade.parts:
            trade.page = str(trade_page(a, trade.parts, self.dry_run))
            self.trades.append(trade)
            self.traded_symbols.add(sym)
            _append(ROOT / "trades.jsonl", {"type": "entry_submitted", "t": _now().isoformat(timespec="seconds"),
                                            "symbol": sym, "setup_t": a["t"], "plan": plan, "parts": trade.parts})
        else:
            a["decision"], a["reasons"] = "REJECTED", ["all order parts were rejected by Alpaca"]

    # ---- manage ----
    def manage(self) -> None:
        for t in self.trades:
            if t.closed:
                continue
            try:
                orders = [self.broker.order(p["order_id"]) for p in t.parts]
            except BrokerError as e:
                event(f"order status unavailable {t.symbol}: {e}", "can't reconcile this cycle", "retry next cycle")
                continue
            fills = [o for o in orders if o.get("filled_avg_price")]
            if fills and t.entry_fill is None:
                t.entry_fill = sum(float(o["filled_avg_price"]) * float(o["filled_qty"]) for o in fills) / sum(float(o["filled_qty"]) for o in fills)
                _append(ROOT / "trades.jsonl", {"type": "entry_filled", "t": _now().isoformat(timespec="seconds"),
                                                "symbol": t.symbol, "avg_price": round(t.entry_fill, 4),
                                                "slippage": round((t.entry_fill - t.planned_entry) * t.direction, 4)})
            legs = [(p, leg) for p, o in zip(t.parts, orders) for leg in (o.get("legs") or [])]
            tp_filled = any(leg["type"] == "limit" and leg["status"] == "filled" for _, leg in legs)
            if tp_filled and not t.be_moved and t.entry_fill:
                for _, leg in legs:
                    if leg["type"] in ("stop", "stop_limit") and leg["status"] in ("new", "accepted", "held"):
                        try:
                            self.broker.replace_stop(leg["id"], t.entry_fill)
                        except BrokerError as e:
                            event(f"break-even move failed {t.symbol}: {e}", "stop stays at the original level", "retry next cycle")
                            break
                else:
                    t.be_moved = True
                    _append(ROOT / "trades.jsonl", {"type": "stop_to_break_even", "t": _now().isoformat(timespec="seconds"),
                                                    "symbol": t.symbol, "stop": round(t.entry_fill, 2)})
            done = all(o["status"] in ("filled", "canceled", "expired", "rejected") for o in orders) and \
                all(leg["status"] in ("filled", "canceled", "expired", "rejected") for _, leg in legs)
            if done and legs:
                # Legs cancelled (e.g. by the flatten) don't mean the position is closed: only
                # record the exit once Alpaca holds nothing in this stock.
                try:
                    held = any(p["symbol"] == t.symbol for p in self.broker.positions())
                except BrokerError:
                    held = True
                if held:
                    continue
                self._record_exit(t, legs)
        self._save_state()

    def _record_exit(self, t: Trade, legs) -> None:
        exits = [(float(leg["filled_avg_price"]), float(leg["filled_qty"]), leg["type"]) for _, leg in legs if leg["status"] == "filled"]
        # Parts closed by the end-of-day flatten are sold by separate orders, not by a leg.
        known = {p["order_id"] for p in t.parts} | {leg["id"] for _, leg in legs}
        try:
            for o in self.broker.orders("closed", after=t.setup_t):
                if (o["symbol"] == t.symbol and o["id"] not in known and o.get("filled_avg_price")
                        and o["side"] == ("sell" if t.direction == 1 else "buy")):
                    exits.append((float(o["filled_avg_price"]), float(o["filled_qty"]), "flatten"))
        except BrokerError as e:
            event(f"closing orders unavailable {t.symbol}: {e}", "exit record may be incomplete", "reconcile in the review")
        qty = sum(q for _, q, _ in exits)
        pnl = sum((p - t.entry_fill) * q * t.direction for p, q, _ in exits) if t.entry_fill else 0.0
        risk = abs(t.entry_fill - t.stop) * qty if t.entry_fill else 0.0
        t.closed = True
        rec = {"type": "exit", "t": _now().isoformat(timespec="seconds"), "symbol": t.symbol,
               "setup_t": t.setup_t, "entry": t.entry_fill, "stop": t.stop, "targets": t.targets,
               "exits": exits, "qty": qty, "pnl": round(pnl, 2),
               "r": round(pnl / risk, 3) if risk else None, "be_moved": t.be_moved}
        _append(ROOT / "trades.jsonl", rec)
        if t.page:
            finish_page(Path(t.page), rec)

    # ---- end of day ----
    def flatten(self, attempts: int = 5, pause: float = 3.0) -> bool:
        """Close everything before the close and verify it with Alpaca. The bracket legs hold
        the shares, so: cancel all orders, wait until none are open, then close each position.
        (2026-10-21: closing with cancel_orders in one call cancelled the stops but sold
        nothing, and five positions were held overnight unprotected.)"""
        if self.dry_run:
            return True
        for attempt in range(attempts):
            try:
                positions = self.broker.positions()
                if not positions:
                    if attempt:
                        event("flattened before the close", f"verified flat after {attempt} round(s)", "")
                    self.manage()
                    return True
                self.broker.cancel_all()
                for _ in range(10):
                    if not self.broker.orders():
                        break
                    time.sleep(pause)
                for p in positions:
                    try:
                        self.broker.close_position(p["symbol"])
                    except BrokerError as e:
                        event(f"close failed {p['symbol']} {p['qty']}: {e}", "position still open", "retrying")
            except BrokerError as e:
                event(f"flatten round {attempt + 1} failed: {e}", "positions may still be open", "retrying")
            time.sleep(pause * 2)
        event("FLATTEN FAILED: positions still open after the close", "held overnight without stops",
              "close them by hand at Alpaca")
        return False

    def run(self) -> None:
        tp = self.config.trading
        self.start()
        deadline = _now() + timedelta(minutes=self.max_minutes) if self.max_minutes else None
        step = timeframe_length(tp.execution_tf)
        fh, fm = map(int, tp.flatten_at.split(":"))
        while True:
            now_ny = datetime.now(NY)
            flatten = now_ny.replace(hour=fh, minute=fm, second=0, microsecond=0)
            if now_ny >= flatten:
                break
            if deadline and _now() >= deadline:
                self._save_state()
                event("session hand-off (runner time limit)", "positions stay protected at Alpaca",
                      "next run resumes from the saved state")
                return
            clock = self.broker.clock()
            if clock["is_open"]:
                self.cycle()
                if not self.dry_run:
                    self.manage()
            # Sleep to just after the next candle close (or the open), managing every minute.
            nxt = (_now() + step).replace(second=20, microsecond=0)
            nxt -= timedelta(minutes=nxt.minute % int(step.total_seconds() // 60))
            until = min(nxt, flatten.astimezone(timezone.utc), deadline or nxt)
            while _now() < until:
                time.sleep(60)
                if clock["is_open"] and not self.dry_run:
                    self.manage()
        self.flatten()
        event("session end", f"{len(self.trades)} trades, {len(self.traded_symbols)} instruments", "review to write")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max-minutes", type=float, help="exit cleanly (no flatten) after this long")
    ap.add_argument("--only-in-session", action="store_true",
                    help="do nothing unless the market opens within 45 minutes or is open before the flatten time")
    args = ap.parse_args()
    if args.only_in_session and not in_session_window():
        print("outside the session window: nothing to do")
        return
    Session(dry_run=args.dry_run, max_minutes=args.max_minutes).run()


def in_session_window(config: Config = BASELINE) -> bool:
    """For schedulers that fire repeatedly (GitHub Actions): start only around a real session."""
    clock = Paper().clock()
    fh, fm = map(int, config.trading.flatten_at.split(":"))
    now_ny = datetime.now(NY)
    if now_ny >= now_ny.replace(hour=fh, minute=fm, second=0, microsecond=0):
        return False
    if clock["is_open"]:
        return True
    next_open = datetime.fromisoformat(clock["next_open"])
    return next_open - _now() <= timedelta(minutes=45)


if __name__ == "__main__":
    main()
