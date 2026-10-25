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
from ..data import fetch_bars, fetch_bars_multi, timeframe_length
from .broker import BrokerError, Paper
from .screener import screen
from .crt_live import _bucket_end, crt_assess
from .experiments import exit_for, model_for, orb_assess, pre_trade, targets_for
from .signals import assess_all, size, split

ROOT = Path(__file__).resolve().parent.parent.parent / "journal" / "trading"
NY = ZoneInfo("America/New_York")
# Take profit 1 comes from the next timeframe up (Day 37); how far back each timeframe is read.
TP_TIMEFRAME = {"1Min": "5Min", "5Min": "15Min", "15Min": "1Hour", "1Hour": "4Hour"}
# 5-minute: enough 1-hour candles for CRT's trend and ranges (~30 sessions).
LOOKBACK = {"1Min": timedelta(days=3), "5Min": timedelta(days=45), "15Min": timedelta(days=20),
            "1Hour": timedelta(days=60), "4Hour": timedelta(days=200)}
SHORT = {"1Min": "1m", "5Min": "5m", "15Min": "15m", "1Hour": "1h"}
BOT_IDS = ("tjr", "orb30", "crt")  # client order id prefixes of the bot's own orders
CRT_EXIT = "1:1 + 3R, fixed stop"


class BarCache:
    """Candles per timeframe and stock: loaded once, then only the newest candles are fetched
    (one request per timeframe for all stocks). The last stored candle is re-read, since it may
    have been still open."""

    def __init__(self, fetch=fetch_bars_multi, keep: int = 8000):
        self.fetch, self.keep, self.bars = fetch, keep, {}

    def get(self, symbols: list[str], tf: str, now: datetime) -> dict[str, list]:
        have = self.bars.setdefault(tf, {})
        missing = [s for s in symbols if not have.get(s)]
        if missing:
            have.update(self.fetch(missing, tf, now - LOOKBACK[tf]))
        known = [s for s in symbols if s not in missing and have.get(s)]
        if known:
            since = min(datetime.fromisoformat(have[s][-1].t.replace("Z", "+00:00")) for s in known)
            for sym, new in self.fetch(known, tf, since).items():
                old = have.get(sym, [])
                if new:
                    old = [c for c in old if c.t < new[0].t] + new
                have[sym] = old[-self.keep:]
        return {s: have.get(s, []) for s in symbols}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _page(path: str) -> Path:
    """A trade page from its stored path: repo-relative (or absolute, from older records)."""
    p = Path(path)
    if p.is_absolute() and "journal/trading/trades/" in path and not p.exists():
        p = Path("journal/trading/trades/" + path.split("journal/trading/trades/", 1)[1])
    return p if p.is_absolute() else ROOT.parent.parent / p


def _append(path: Path, obj: dict) -> None:
    with path.open("a") as f:
        f.write(json.dumps(obj) + "\n")


def trade_page(a: dict, parts: list[dict], dry_run: bool) -> Path:
    """The readable record of one trade (the owner reads these): why it was taken and the plan.
    The result and what was learned are added at the exit and in the after-close review."""
    folder = ROOT / "trades"
    folder.mkdir(exist_ok=True)
    stamp = a["t"][:16].replace(":", "").replace("T", "_")
    path = folder / f"{stamp}_{a['symbol']}_{a.get('strategy', 'tjr_m1')}.md"
    p, ctx = a["plan"], a["context"]
    lines = [f"# {a['symbol']} {p['direction']} · setup candle {a['t']} UTC" + (" · DRY RUN" if dry_run else ""), "",
             "## Why the bot took it", f"- **Setup:** {a['setup']}"]
    lines += [f"- **{x['concept']}:** {x['evidence']}" for x in a["present"]]
    lines += [f"- **Conflicting – {x['concept']}:** {x['evidence']}" for x in a["conflicts"]]
    ex, mkt = a.get("experiment") or {}, ctx.get("market") or {}
    lines += [f"- **Daily bias relation:** {ctx['bias_relation']} (traded either way since 2026-10-21; every trade tests it)",
              f"- **Market:** SPY {mkt.get('spy_today_pct', '?')}% today at {mkt.get('time_ny', '?')} ET; "
              f"open positions {mkt.get('open_long', 0)} long / {mkt.get('open_short', 0)} short before this one",
              f"- **Decision:** {a['decision']}", ""]
    if ex:
        lines += ["## Experiment (before entry)",
                  f"- **Strategy:** `{ex['strategy']}`: {ex['hypothesis']}",
                  f"- **Exit tested:** `{ex['exit']}`: {ex['exit_hypothesis']}",
                  f"- **Expectation:** {ex['expect']}",
                  f"- **Invalidated if:** {ex['invalidation']}",
                  f"- **Expected outcome and uncertainty:** {ex['expected_outcome']}", ""]
    lines += ["## The plan",
              f"- Entry {p['entry']} ({p['entry_condition']}); stop {p['stop']}: {p['invalidation']}",
              f"- Take profits {', '.join(f'{x:.2f}' for x in p['take_profits'])}: first at {p['rr_first']}R, last at {p['rr_last']}R"
              + (f" (strategy's own ladder was {', '.join(f'{x:.2f}' for x in p['ladder'])})" if p.get("ladder") and p["ladder"] != p["take_profits"] else ""),
              f"- Size: {a['size']['qty']} shares, risking ${a['size']['risk_dollars']} (max 1% of equity {a['size']['equity']}; "
              f"positions max 10% of equity), in {len(parts)} parts: " + ", ".join(f"{x['qty']} @ {x['target']:.2f}" for x in parts),
              "", "## Result", "_open_", "",
              "## What it learned",
              "_The after-close review answers, from what was known at entry:_ what happened; did the thesis play out; "
              "which parts of the analysis were right or wrong; entry timing; exit; costs (slippage, spread) and the result "
              "after costs; decision quality vs outcome (good decision / bad luck or the reverse); the most plausible "
              "explanation and how sure; validity class 1–4; the lesson; more evidence needed.", ""]
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
        index.write_text("# Trades\n\nEvery trade the bot takes: why, the plan, the result, and what it learned (click the trade).\n\n"
                         "| Setup (UTC) | Stock | Direction | Strategy / exit | Bias relation | R actual | R as planned | P/L actual | Record |\n"
                         "|---|---|---|---|---|---|---|---|---|\n")
    text = path.read_text()
    head = text.splitlines()[0]
    rel = next((l.split(":** ")[1].split(" ")[0] for l in text.splitlines() if l.startswith("- **Daily bias relation")), "n/a")
    r = f"{exit_rec['r']:+.2f}" if exit_rec["r"] is not None else "?"
    with index.open("a") as f:  # "as planned" is filled in by the after-close review
        f.write(f"| {exit_rec['setup_t'][:16].replace('T', ' ')} | {exit_rec['symbol']} | {head.split(' ')[2]} | "
                f"{exit_rec.get('strategy', 'tjr_m1')} / {exit_rec.get('exit_name', 'tjr_ladder')} | {rel} | {r} | (review) | "
                f"{exit_rec['pnl']:+,.2f} | [page](trades/{path.name}) |\n")


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
    strategy: str = "tjr_m1"
    exit_name: str = "tjr_ladder"
    expires_at: str = ""  # a limit entry (model 2) not filled by then is cancelled


class Session:
    def __init__(self, config: Config = BASELINE, dry_run: bool = False, max_minutes: float | None = None):
        self.config = config
        self.dry_run = dry_run
        self.max_minutes = max_minutes
        self.broker = Paper()
        self.trades: list[Trade] = []
        self.traded_symbols: set[str] = set()
        self.seen: set[tuple[str, str, str]] = set()
        self.failures = 0
        self.halted = False
        self.watch: list[str] = []
        self.today = datetime.now(NY).strftime("%Y-%m-%d")
        self._daily, self._daily_day = None, None
        self.cache = BarCache()
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
        self._warm_up()
        return acct

    def _warm_up(self) -> None:
        """Load every timeframe's candles before the open, so the first cycles are quick."""
        tp = self.config.trading
        now = _now()
        tfs = set(tp.tjr_timeframes) | {TP_TIMEFRAME[x] for x in tp.tjr_timeframes} if "tjr" in tp.strategies else set()
        tfs |= {"15Min"} if "orb30" in tp.strategies else set()
        tfs |= {"5Min"} if "crt" in tp.strategies else set()
        for tf in sorted(tfs, key=lambda x: timeframe_length(x)):
            try:
                self.cache.get(self.watch, tf, now)
            except Exception as e:
                event(f"warm-up failed for {tf}: {e}", "loaded at the first cycle instead", "")

    def _reconcile_start(self) -> None:
        """After a restart, Alpaca is the truth: count today's filled symbols toward the instrument
        cap, and report positions the saved state doesn't know (it was lost before a save)."""
        if self.dry_run:
            return
        open_ny = datetime.now(NY).replace(hour=0, minute=0, second=0, microsecond=0)
        if self.config.trading.hold_overnight:
            open_ny -= timedelta(days=10)  # trades held overnight may come from earlier days
        try:
            orders = self.broker.orders(status="all", after=open_ny.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
            positions = self.broker.positions()
        except BrokerError as e:
            event(f"start reconcile unavailable: {e}", "instrument cap from saved state only", "")
            return
        # Only the bot's own entries (manual or other orders don't count as instruments traded).
        filled = {o["symbol"] for o in orders if float(o.get("filled_qty") or 0) > 0
                  and str(o.get("client_order_id", "")).startswith(BOT_IDS) and self.today in str(o.get("client_order_id"))}
        self.traded_symbols |= filled
        self._adopt(orders, {p["symbol"] for p in positions})
        known = {t.symbol for t in self.trades if not t.closed}
        for pos in positions:
            if pos["symbol"] not in known:
                event(f"position {pos['symbol']} {pos['qty']} at Alpaca is not in the saved state",
                      "not managed by this session (its bracket stop and take profit stay live at Alpaca)",
                      "reconcile in the review" if self.config.trading.hold_overnight else "closed at flatten; reconcile in the review")

    def _adopt(self, orders: list[dict], held: set[str]) -> None:
        """Rebuild trades the saved state lost (e.g. a run stopped before it saved), from the
        bot's own orders at Alpaca: the client order id is <strategy>-<date>-<symbol>-<hhmm>-<part>."""
        mine = {p["order_id"] for t in self.trades for p in t.parts}
        groups: dict[str, list[dict]] = {}
        for o in orders:
            cid = str(o.get("client_order_id", ""))
            if not cid.startswith(BOT_IDS) or cid.count("-") < 5 or o.get("id") in mine:
                continue
            groups.setdefault(cid.rsplit("-", 1)[0], []).append(o)
        terminal = ("filled", "canceled", "expired", "rejected")
        for key, group in groups.items():
            strategy, y, m, d, sym, hhmm = key.split("-", 5)
            strategy = "tjr_m1_15m" if strategy == "tjr" else strategy  # ids from before the playbooks
            legs = [leg for o in group for leg in (o.get("legs") or [])]
            if sym not in held and all(o["status"] in terminal for o in group) and all(l["status"] in terminal for l in legs):
                continue  # finished while no one was watching: the review reconciles it
            stops = [float(l["stop_price"]) for l in legs if l["type"] in ("stop", "stop_limit")]
            parts = []
            for o in sorted(group, key=lambda o: o["client_order_id"]):
                target = next((float(l["limit_price"]) for l in (o.get("legs") or []) if l["type"] == "limit"), None)
                parts.append({"client_id": o["client_order_id"], "order_id": o["id"], "qty": int(float(o["qty"])), "target": target})
            first = group[0]
            setup_t = f"{y}-{m}-{d}T{hhmm[:2]}:{hhmm[2:]}:00Z"
            crt = strategy.startswith("crt")
            trade = Trade(sym, setup_t, 1 if first["side"] == "buy" else -1,
                          float(first.get("limit_price") or first.get("filled_avg_price") or 0), stops[0] if stops else 0.0,
                          [p["target"] for p in parts if p["target"] is not None], parts,
                          strategy=strategy, exit_name=CRT_EXIT if crt else "unknown (adopted after a restart)",
                          expires_at=_bucket_end(setup_t).isoformat(timespec="seconds") if crt else "")
            self.trades.append(trade)
            event(f"adopted {sym} {strategy} ({len(parts)} parts) from Alpaca's orders",
                  "the saved state had lost it; managed again from now", "")

    def _load_state(self) -> None:
        if self.state_path.exists():
            s = json.loads(self.state_path.read_text())
            self.trades = [Trade(**t) for t in s["trades"]]
            self.traded_symbols = set(s["traded_symbols"])
            # (symbol, candle) keys from before the strategies existed belong to TJR's model 1.
            self.seen = {tuple(x) if len(x) == 3 else (x[0], x[1], "tjr_m1") for x in s["seen"]}
        elif self.config.trading.hold_overnight:
            # A new day: trades still open from the last session are carried over and managed.
            earlier = sorted(p for p in ROOT.glob("state_*.json") if p.name < self.state_path.name)
            if earlier:
                s = json.loads(earlier[-1].read_text())
                self.trades = [Trade(**t) for t in s["trades"] if not t["closed"]]
                if self.trades:
                    event(f"carried over {len(self.trades)} open trade(s) from {earlier[-1].name}", "managed until stop or target", "")

    def _save_state(self) -> None:
        self.state_path.write_text(json.dumps({"trades": [t.__dict__ for t in self.trades],
                                               "traded_symbols": sorted(self.traded_symbols),
                                               "seen": sorted(self.seen)}, indent=1))

    # ---- assess + execute ----
    def due_timeframes(self, now: datetime) -> list[str]:
        """Timeframes whose candle closed at the last minute boundary (bars are clock-aligned)."""
        tp = self.config.trading
        minute = int(now.timestamp() // 60)
        tfs = set(tp.tjr_timeframes if "tjr" in tp.strategies else ()) | ({"15Min"} if "orb30" in tp.strategies else set())
        tfs |= {"5Min"} if "crt" in tp.strategies else set()
        return sorted((tf for tf in tfs if minute % int(timeframe_length(tf).total_seconds() // 60) == 0),
                      key=lambda tf: timeframe_length(tf))

    def cycle(self, timeframes: list[str] | None = None) -> None:
        """Assess every playbook whose candle just closed: TJR's models on each timeframe, and
        the opening-range breakout on the 15-minute. One request per timeframe for all stocks."""
        tp = self.config.trading
        now = _now()
        timeframes = self.due_timeframes(now) if timeframes is None else timeframes
        if not timeframes:
            return
        market = None
        try:
            if self._daily is None or self._daily_day != datetime.now(NY).date():
                self._daily = fetch_bars_multi(self.watch, "1Day", now - timedelta(days=200))
                self._daily_day = datetime.now(NY).date()
        except Exception as e:
            event(f"data error (daily bars): {e}", "cycle skipped", "retry next minute")
            return
        for tf in timeframes:
            length = timeframe_length(tf)
            up = TP_TIMEFRAME[tf]
            try:
                bars = self.cache.get(self.watch, tf, now)
                upper = self.cache.get(self.watch, up, now) if "tjr" in tp.strategies else {}
            except Exception as e:
                event(f"data error ({tf} bars): {e}", f"{tf} skipped this cycle", "retry at the next close")
                continue
            for sym in self.watch:
                ltf = [c for c in bars.get(sym, [])][-600:]
                closed = [c for c in ltf if c.closed]
                # Only a candle that closed at this boundary is news; thin stocks may have none.
                if not closed or datetime.fromisoformat(closed[-1].t.replace("Z", "+00:00")) + length < now - timedelta(minutes=1):
                    continue
                found = []
                if "crt" in tp.strategies and tf == "5Min":
                    found += crt_assess(sym, bars.get(sym, []), self.shorting, tp.crt_target_r)
                if "tjr" in tp.strategies and tf in tp.tjr_timeframes:
                    for a in assess_all(sym, ltf, upper.get(sym, []), self._daily.get(sym, []), self.config, self.shorting,
                                        length, timeframe_length(up), models=tp.tjr_models, wait=tp.model_wait_candles):
                        # Each setup is traded with one entry model, by a fixed even split, so the
                        # models are compared on the same kind of setups (one position per stock).
                        if model_for(f"{sym}-{tf}-{a['block_t']}", tp.tjr_models) != a["model"]:
                            continue
                        a["strategy"] = f"tjr_m{a['model']}_{SHORT[tf]}"
                        a["timeframe"] = tf
                        found.append(a)
                if "orb30" in tp.strategies and tf == "15Min":
                    a = orb_assess(sym, ltf, self.shorting)
                    if a is not None:
                        a["timeframe"] = tf
                        found.append(a)
                for a in found:
                    key = (sym, a["t"], a["strategy"])
                    if key in self.seen:
                        continue
                    self.seen.add(key)
                    if market is None:
                        market = self._market_context(now)
                    a["context"]["market"] = market
                    if a["decision"] == "APPROVED":
                        self._approve(a)
                    a["dry_run"] = self.dry_run
                    _append(ROOT / "setups.jsonl", a)
        self._save_state()

    def _market_context(self, now: datetime) -> dict:
        """Broad conditions at the decision: SPY's move today, time of day, open positions."""
        ctx = {"time_ny": datetime.now(NY).strftime("%H:%M"),
               "open_long": sum(1 for t in self.trades if not t.closed and t.direction == 1),
               "open_short": sum(1 for t in self.trades if not t.closed and t.direction == -1)}
        try:
            ny = lambda c: datetime.fromisoformat(c.t.replace("Z", "+00:00")).astimezone(NY)
            session = [c for c in fetch_bars("SPY", "15Min", now - timedelta(days=1)) if c.closed
                       and ny(c).date() == datetime.now(NY).date() and (ny(c).hour, ny(c).minute) >= (9, 30)]
            if session:
                ctx["spy_today_pct"] = round((session[-1].c / session[0].o - 1) * 100, 2)
        except Exception:
            pass  # context only; never blocks a decision
        return ctx

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
        strategy = a.get("strategy", "tjr_m1")
        crt = strategy.startswith("crt")
        d = 1 if plan["direction"] == "long" else -1
        if crt:
            # CRT: every gap in the third candle is its own trade, so trades in the same direction
            # stack on a stock; never the opposite direction (Alpaca nets positions).
            if any(t.symbol == sym and not t.closed and t.direction != d for t in self.trades):
                a["decision"], a["reasons"] = "REJECTED", ["an open trade in this stock goes the other way"]
                return
            if not self.dry_run:
                try:
                    held = [float(p["qty"]) for p in self.broker.positions() if p["symbol"] == sym]
                except BrokerError:
                    held = [-d]
                if any(q * d < 0 for q in held):
                    a["decision"], a["reasons"] = "REJECTED", ["Alpaca holds a position in this stock the other way"]
                    return
        elif any(t.symbol == sym and not t.closed for t in self.trades):
            a["decision"], a["reasons"] = "REJECTED", ["a position in this stock is still open"]
            return
        if not self.dry_run and not crt:
            try:  # Alpaca is the truth: never stack a second position or order on a stock
                busy = {p["symbol"] for p in self.broker.positions()} | {o["symbol"] for o in self.broker.orders()}
            except BrokerError:
                busy = {sym}
            if sym in busy:
                a["decision"], a["reasons"] = "REJECTED", ["Alpaca already holds a position or open order in this stock"]
                return
        family = "tjr" if strategy.startswith("tjr") else strategy
        if crt:  # the owner's exits: half at 1:1, half at the target, stop fixed
            exit_name = CRT_EXIT
        else:
            exits = dict(tp.exits_under_test).get(family, ("tjr_ladder",))
            exit_name = exit_for(strategy, exits, f"{sym}-{a['t']}")
            plan["ladder"] = list(plan.get("take_profits") or [])
            plan["take_profits"] = targets_for(exit_name, d, plan["entry"], plan["stop"], plan["ladder"])
        if not plan["take_profits"]:
            a["decision"], a["reasons"] = "REJECTED", [f"exit {exit_name}: no target"]
            return
        risk = abs(plan["entry"] - plan["stop"])
        plan["rr_first"] = round(abs(plan["take_profits"][0] - plan["entry"]) / risk, 2)
        plan["rr_last"] = round(abs(plan["take_profits"][-1] - plan["entry"]) / risk, 2)
        a["experiment"] = pre_trade(a, exit_name)
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
        limit = plan["entry"] if plan.get("entry_type") == "limit" else None
        expires = plan.get("expires_at", "")
        if limit is not None and not expires:
            expires = (_now() + timeframe_length(a.get("timeframe", "15Min")) * (plan.get("valid_candles") or tp.model_wait_candles)
                       ).isoformat(timespec="seconds")
        trade = Trade(sym, a["t"], d, plan["entry"], plan["stop"], [t for _, t in parts],
                      strategy=strategy, exit_name=exit_name, expires_at=expires)
        for k, (q, target) in enumerate(parts):
            cid = f"{strategy}-{self.today}-{sym}-{a['t'][11:16].replace(':', '')}-{k}"
            try:
                o = self.broker.bracket(sym, q, "buy" if d == 1 else "sell", target, plan["stop"], cid, limit_price=limit)
                trade.parts.append({"client_id": cid, "order_id": o["id"], "qty": q, "target": target})
            except BrokerError as e:
                # Alpaca's wash-trade guard can refuse an order next to the stock's other open
                # orders: that is a refusal, not a technical failure.
                self.failures += 0 if "wash" in str(e).lower() else 1
                event(f"order rejected {sym} part {k}: {e}", "part not placed", "recorded; trade continues with placed parts")
                if self.failures >= 3:
                    self.halted = True
                    event("3 failed submissions: new entries halted", "no new trades today", "review before next session")
        if trade.parts:
            page = trade_page(a, trade.parts, self.dry_run)
            trade.page = str(page.relative_to(ROOT.parent.parent)) if page.is_relative_to(ROOT.parent.parent) else str(page)
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
            if t.expires_at and _now() >= datetime.fromisoformat(t.expires_at) and \
                    any(o["status"] in ("new", "accepted", "pending_new", "partially_filled") for o in orders):
                for o in orders:
                    if o["status"] in ("new", "accepted", "pending_new", "partially_filled"):
                        try:
                            self.broker.cancel(o["id"])
                        except BrokerError as e:
                            event(f"cancel failed {t.symbol} {o['id']}: {e}", "limit entry may still fill", "retry next minute")
                continue  # look again next minute, once the cancels have landed
            if t.expires_at and all(o["status"] in ("canceled", "expired", "rejected") and not float(o.get("filled_qty") or 0)
                                    for o in orders):
                t.closed = True
                _append(ROOT / "trades.jsonl", {"type": "not_filled", "t": _now().isoformat(timespec="seconds"),
                                                "symbol": t.symbol, "setup_t": t.setup_t, "strategy": t.strategy,
                                                "limit": t.planned_entry})
                if t.page and _page(t.page).exists():
                    _page(t.page).write_text(_page(t.page).read_text().replace(
                        "## Result\n_open_", "## Result\n- Limit entry not filled before it expired: no trade (0R)."))
                continue
            fills = [o for o in orders if o.get("filled_avg_price")]
            if fills and t.entry_fill is None:
                t.entry_fill = sum(float(o["filled_avg_price"]) * float(o["filled_qty"]) for o in fills) / sum(float(o["filled_qty"]) for o in fills)
                _append(ROOT / "trades.jsonl", {"type": "entry_filled", "t": _now().isoformat(timespec="seconds"),
                                                "symbol": t.symbol, "avg_price": round(t.entry_fill, 4),
                                                "slippage": round((t.entry_fill - t.planned_entry) * t.direction, 4)})
            legs = [(p, leg) for p, o in zip(t.parts, orders) for leg in (o.get("legs") or [])]
            tp_filled = any(leg["type"] == "limit" and leg["status"] == "filled" for _, leg in legs)
            if tp_filled and not t.be_moved and t.entry_fill and not t.strategy.startswith("crt"):  # CRT: stop fixed
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
                # Legs cancelled (e.g. by the flatten) don't mean the position is closed: unless
                # the legs sold every filled share, only record the exit once Alpaca holds
                # nothing in this stock (other trades may share the stock).
                bought = sum(float(o.get("filled_qty") or 0) for o in orders)
                sold = sum(float(leg.get("filled_qty") or 0) for _, leg in legs)
                if sold < bought:
                    try:
                        held = any(p["symbol"] == t.symbol for p in self.broker.positions())
                    except BrokerError:
                        held = True
                    if held:
                        continue
                self._record_exit(t, legs, covered=sold >= bought)
        self._save_state()

    def _record_exit(self, t: Trade, legs, covered: bool = False) -> None:
        exits = [(float(leg["filled_avg_price"]), float(leg["filled_qty"]), leg["type"]) for _, leg in legs if leg["status"] == "filled"]
        # Parts closed by the end-of-day flatten are sold by separate orders, not by a leg.
        known = {p["order_id"] for p in t.parts} | {leg["id"] for _, leg in legs}
        try:
            for o in ([] if covered else self.broker.orders("closed", after=t.setup_t)):
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
               "r": round(pnl / risk, 3) if risk else None, "be_moved": t.be_moved,
               "strategy": t.strategy, "exit_name": t.exit_name}
        _append(ROOT / "trades.jsonl", rec)
        if t.page:
            finish_page(_page(t.page), rec)

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
                        if "HTTP 404" in str(e):
                            continue  # already closed (the previous round's order filled)
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
        fh, fm = map(int, (tp.session_end if tp.hold_overnight else tp.flatten_at).split(":"))
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
            try:
                clock = self.broker.clock()
                if clock["is_open"]:
                    self.cycle()
                    if not self.dry_run:
                        self.manage()
            except BrokerError as e:
                event(f"broker error in the cycle: {e}", "this minute skipped", "retry next minute")
            # Every minute, just after the candle closes (bars are clock-aligned).
            nxt = (_now() + timedelta(minutes=1)).replace(second=15, microsecond=0)
            until = min(nxt, flatten.astimezone(timezone.utc), deadline or nxt)
            while _now() < until:
                time.sleep(max(0.5, min(5.0, (until - _now()).total_seconds())))
        if tp.hold_overnight:
            if not self.dry_run:
                self.manage()  # cancels the last third candle's unfilled orders
            self._save_state()
            open_ = sum(1 for t in self.trades if not t.closed)
            event("session end (no flatten: CRT trades are held until stop or target)",
                  f"{open_} trade(s) still open, protected by their gtc stops at Alpaca", "review to write")
            return
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
    tp = config.trading
    fh, fm = map(int, (tp.session_end if tp.hold_overnight else tp.flatten_at).split(":"))
    now_ny = datetime.now(NY)
    if now_ny >= now_ny.replace(hour=fh, minute=fm, second=0, microsecond=0):
        return False
    if clock["is_open"]:
        return True
    next_open = datetime.fromisoformat(clock["next_open"])
    return next_open - _now() <= timedelta(minutes=45)


if __name__ == "__main__":
    main()
