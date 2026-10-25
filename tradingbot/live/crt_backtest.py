"""Backtest of the owner's Candle Range Theory (CRT) video strategy (2026-10-25), as the video
teaches it; the choices it leaves open are marked [Bot] and listed in the report.

On the 1-hour chart:
  1. trend: the last break of structure, not consolidating (no choppy markets);
  2. a pullback into the discount (premium for shorts) of the impulse leg (equilibrium, 50%);
  3. range candle: a candle against the trend in that zone; its high is the CRH, its low the CRL;
  4. sweep candle: the next candle trades beyond the CRL (CRH for shorts) and closes back inside
     the range. A close beyond invalidates it, and the next counter-trend candle is tried.
On the 5-minute chart (the entry):
  5. fair value gaps that form after the sweep's extreme: at the sweep candle's close, a limit at
     the lowest gap already there (highest for shorts: "in the discount"); every gap that forms
     during the third 1-hour candle adds its own order; orders expire at the end of that candle
     [Bot: the video calls the third candle "the entry"];
  6. entry at the gap's near edge; stop beyond the gap: below the low of the gap's first candle
     [Bot: the video's stop boxes sit 1-2 pips below the gap]; or, with ``--stop sweep``, below
     the sweep candle's low (above its high for shorts) (owner, 2026-10-25);
  7. half closed at 1:1; the other half at "a strong level ahead": the CRH for longs (CRL for
     shorts), or the impulse leg's extreme if that is not beyond 1:1 [Bot: 2 of the video's 3
     examples target the CRH exactly]; the stop is not moved (a 1:1 then stop is break even);
  8. skipped when the previous day's high or low lies between entry and the 1:1 target
     ("a strong higher-timeframe level") [Bot]; news can't be checked in candles.
Positions are held until the stop or target, overnight too, as in the video; a gap through the
stop or target at the open fills at the open. Sizing as the live bot: risk at most 1% of
$100,000 and a position at most 10% of it. Costs per side: 3 bps for stocks, 20 bps for
crypto (Alpaca's crypto fees). A candle that reaches both the stop and a target counts as the
stop. Data: Alpaca's consolidated (SIP) 5-minute bars, regular hours; 1-hour candles are built
from them starting 09:30 ET (the last one 15:30-16:00).

    python -m tradingbot.live.crt_backtest --days 180 --symbols SPY,NVDA,... [--crypto BTC/USD]
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import pickle
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import mean

from ..candles import BEARISH, BULLISH, Candle
from ..data import fetch_bars
from ..equilibrium import ranges
from ..fvg import find_gaps
from ..trend import trend_series
from .signals import NY

CACHE = Path.home() / ".cache" / "tradingbot"
STUDIES = Path(__file__).resolve().parent.parent.parent / "journal" / "studies"
EQUITY, RISK_PCT, POSITION_PCT = 100_000.0, 1.0, 10.0


def _ts(t: str) -> datetime:
    return datetime.fromisoformat(t.replace("Z", "+00:00"))


# ---- data ----

def _crypto_bars(symbol: str, start: datetime, end: datetime) -> list[Candle]:
    url = "https://data.alpaca.markets/v1beta3/crypto/us/bars"
    params = {"symbols": symbol, "timeframe": "5Min", "start": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
              "end": end.strftime("%Y-%m-%dT%H:%M:%SZ"), "limit": 10000}
    headers = {"APCA-API-KEY-ID": os.environ.get("ALPACA_API_KEY", ""), "APCA-API-SECRET-KEY": os.environ.get("ALPACA_SECRET_KEY", "")}
    out = []
    while True:
        with urllib.request.urlopen(urllib.request.Request(url + "?" + urllib.parse.urlencode(params), headers=headers), timeout=60) as r:
            p = json.load(r)
        out += [Candle(b["t"], b["o"], b["h"], b["l"], b["c"]) for b in (p.get("bars") or {}).get(symbol, [])]
        if not p.get("next_page_token"):
            return out
        params["page_token"] = p["next_page_token"]


def five_minute(symbol: str, days: int) -> list[Candle]:
    """Closed 5-minute bars; stocks: SIP, regular hours only. Cached per day."""
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"crt_{symbol.replace('/', '-')}_{days}_{datetime.now(timezone.utc):%Y%m%d}.pkl"
    if path.exists():
        return pickle.loads(path.read_bytes())
    end = datetime.now(timezone.utc) - timedelta(minutes=20)
    start = end - timedelta(days=days)
    if "/" in symbol:
        bars = _crypto_bars(symbol, start, end)
    else:
        bars = [c for c in fetch_bars(symbol, "5Min", start, end, feed="sip") if c.closed]
        bars = [c for c in bars if (9, 30) <= (lambda n: (n.hour, n.minute))(_ts(c.t).astimezone(NY)) < (16, 0)]
    path.write_bytes(pickle.dumps(bars))
    return bars


def aggregate(bars: list[Candle], minutes: int, crypto: bool) -> list[Candle]:
    """Longer bars from 5-minute bars (stocks: buckets from 09:30 ET; crypto: clock-aligned)."""
    if minutes == 5:
        return bars
    out, key_prev = [], None
    for c in bars:
        t = _ts(c.t)
        n = t if crypto else t.astimezone(NY)
        m = n.hour * 60 + n.minute - (0 if crypto else 570)
        key = (n.date(), m // minutes)
        if key != key_prev:
            out.append(Candle(c.t, c.o, c.h, c.l, c.c)); key_prev = key
        else:
            last = out[-1]
            out[-1] = Candle(last.t, last.o, max(last.h, c.h), min(last.l, c.l), c.c)
    return out


def hourly(bars: list[Candle], crypto: bool, hours: int = 1) -> tuple[list[Candle], list[int]]:
    """``hours``-hour candles built from lower-timeframe bars, and the index of each one's first
    bar. Stocks: from 09:30 ET (1-hour: ... 15:30-16:00; 4-hour: 09:30-13:30, 13:30-16:00);
    crypto: clock hours."""
    out, first = [], []
    key_prev = None
    for k, c in enumerate(bars):
        t = _ts(c.t)
        if crypto:
            key = (t.date(), t.hour // hours)
        else:
            n = t.astimezone(NY)
            m = n.hour * 60 + n.minute - 570  # minutes since 09:30
            key = (n.date(), m // (60 * hours))
        if key != key_prev:
            out.append(Candle(c.t, c.o, c.h, c.l, c.c))
            first.append(k)
            key_prev = key
        else:
            last = out[-1]
            out[-1] = Candle(last.t, last.o, max(last.h, c.h), min(last.l, c.l), c.c)
    return out, first


# ---- the strategy ----

@dataclass
class Order:
    symbol: str
    direction: int
    entry: float
    stop: float
    tp1: float
    tp2: float
    placed: int  # 5-minute bar index from which it can fill
    expires: int  # last 5-minute bar index it can fill on
    setup_t: str  # the sweep candle
    crh: float
    crl: float


def setups(symbol: str, bars: list[Candle], crypto: bool, stop_mode: str = "gap", range_hours: int = 1) -> tuple[list[Order], dict]:
    """Every order the strategy would place, and why candidate setups were skipped.
    ``stop_mode``: "gap" = below the gap's first candle; "sweep" = below the sweep candle's low
    (above its high for shorts)."""
    H, first = hourly(bars, crypto, range_hours)
    states = trend_series(H)
    rng = ranges(H, states)
    gaps = find_gaps(bars)
    skipped = {"invalid (closed beyond the range)": 0, "no gap after the sweep": 0, "no room for 1:1": 0,
               "daily level in the way": 0}
    days = {}
    for c in bars:  # each day's high and low, for the "strong level" filter
        d = (_ts(c.t) if crypto else _ts(c.t).astimezone(NY)).date()
        h, l = days.get(d, (c.h, c.l))
        days[d] = (max(h, c.h), min(l, c.l))
    day_list = sorted(days)
    prev_day = {d: days[day_list[k - 1]] for k, d in enumerate(day_list) if k}
    orders = []
    for i in range(1, len(H) - 1):
        r, s = H[i - 1], H[i]
        st = states[i - 1]
        d = st.tradeable_direction
        if d == 0 or states[i].direction != d:
            continue
        counter = (r.c < r.o) if d == 1 else (r.c > r.o)
        zone = rng[i - 1]
        if not counter or zone is None or zone.direction != d or zone.depth(r.l if d == 1 else r.h) < 0.5:
            continue
        crh, crl = r.h, r.l
        swept = (s.l < crl) if d == 1 else (s.h > crh)
        if not swept:
            continue
        if not (crl < s.c <= crh):
            skipped["invalid (closed beyond the range)"] += 1
            continue
        # The 5-minute bars of the sweep candle and of the third candle.
        s0, s1 = first[i], first[i + 1] - 1
        t1 = (first[i + 2] - 1) if i + 2 < len(first) else len(bars) - 1
        extreme = min(range(s0, s1 + 1), key=lambda k: bars[k].l) if d == 1 else max(range(s0, s1 + 1), key=lambda k: bars[k].h)
        side = BULLISH if d == 1 else BEARISH
        own = [g for g in gaps if g.side == side and g.index - 1 >= extreme and g.confirmed_at <= t1]
        at_close = [g for g in own if g.confirmed_at <= s1]
        later = [g for g in own if g.confirmed_at > s1]
        chosen = ([min(at_close, key=lambda g: g.bottom)] if d == 1 else [max(at_close, key=lambda g: g.top)]) if at_close else []
        chosen += later
        if not chosen:
            skipped["no gap after the sweep"] += 1
            continue
        for g in chosen:
            entry = g.top if d == 1 else g.bottom
            c1 = bars[g.index - 1]
            if stop_mode == "sweep":
                stop = s.l if d == 1 else s.h
            else:
                stop = c1.l if d == 1 else c1.h
            risk = (entry - stop) * d
            if risk <= 0:
                continue
            tp1 = entry + d * risk
            target = crh if d == 1 else crl
            if (target - tp1) * d <= 0:
                target = zone.high if d == 1 else zone.low  # the impulse leg's extreme
            if (target - tp1) * d <= 0:
                skipped["no room for 1:1"] += 1
                continue
            third = H[i + 1]  # the previous day's levels as seen from the entry candle
            day = (_ts(third.t) if crypto else _ts(third.t).astimezone(NY)).date()
            ph, pl = prev_day.get(day, (None, None))
            if any(lv is not None and min(entry, tp1) < lv < max(entry, tp1) for lv in (ph, pl)):
                skipped["daily level in the way"] += 1
                continue
            orders.append(Order(symbol, d, entry, stop, tp1, target, max(g.confirmed_at, s1) + 1, t1, s.t, crh, crl))
    return orders, skipped


def simulate(bars: list[Candle], o: Order, cost_bps: float) -> dict | None:
    """Fill the limit, then half at 1:1 and half at the target; the stop stays. None if unfilled."""
    d = o.direction
    fill = next((k for k in range(o.placed, min(o.expires, len(bars) - 1) + 1)
                 if ((bars[k].l <= o.entry) if d == 1 else (bars[k].h >= o.entry))), None)
    if fill is None:
        return None
    risk = abs(o.entry - o.stop)
    qty = min(EQUITY * RISK_PCT / 100 / risk, EQUITY * POSITION_PCT / 100 / o.entry)
    if "/" in o.symbol:  # crypto trades in fractions
        qty = round(qty, 6)
        half = qty / 2
    else:
        qty = int(qty)
        if qty < 2:
            return {"skipped": "position too small to split in halves"}
        half = qty // 2
    legs, open_qty, hit1, k = [], qty, False, fill
    exit_t = None
    while k < len(bars):
        c = bars[k]
        first_bar = k == fill
        # A gap through the stop or a target at this bar's open (overnight) fills at the open.
        if not first_bar and ((c.o <= o.stop) if d == 1 else (c.o >= o.stop)):
            legs.append((c.o, open_qty, "stop (gap)")); open_qty = 0
        elif (c.l <= o.stop) if d == 1 else (c.h >= o.stop):
            legs.append((o.stop, open_qty, "stop")); open_qty = 0
        elif not first_bar:  # on the fill bar its high (low) may have come before the fill: no targets
            if not hit1 and ((c.h >= o.tp1) if d == 1 else (c.l <= o.tp1)):
                px = c.o if ((c.o >= o.tp1) if d == 1 else (c.o <= o.tp1)) else o.tp1
                legs.append((px, half, "1:1")); open_qty -= half; hit1 = True
            if hit1 and ((c.h >= o.tp2) if d == 1 else (c.l <= o.tp2)):
                px = c.o if ((c.o >= o.tp2) if d == 1 else (c.o <= o.tp2)) else o.tp2
                legs.append((px, open_qty, "target")); open_qty = 0
        if open_qty == 0:
            exit_t = c.t
            break
        k += 1
    if open_qty:  # data ran out: close at the last price
        legs.append((bars[-1].c, open_qty, "end of data")); exit_t = bars[-1].t
    gross = sum((px - o.entry) * q * d for px, q, _ in legs)
    cost = cost_bps / 1e4 * (o.entry * qty + sum(px * q for px, q, _ in legs))
    net = gross - cost
    return {"symbol": o.symbol, "direction": "long" if d == 1 else "short", "setup_t": o.setup_t,
            "fill_t": bars[fill].t, "exit_t": exit_t, "entry": round(o.entry, 4), "stop": round(o.stop, 4),
            "tp1": round(o.tp1, 4), "tp2": round(o.tp2, 4), "qty": qty, "risk_pct": round(risk / o.entry * 100, 3),
            "legs": [(round(px, 4), q, why) for px, q, why in legs],
            "pnl_gross": round(gross, 2), "cost": round(cost, 2), "pnl": round(net, 2),
            "r": round(net / (risk * qty), 3), "r_gross": round(gross / (risk * qty), 3),
            "held_hours": round((_ts(exit_t) - _ts(bars[fill].t)).total_seconds() / 3600, 1)}


def summarize(trades: list[dict]) -> dict:
    if not trades:
        return {"trades": 0}
    rs = [t["r"] for t in trades]
    wins = [t for t in trades if t["pnl"] > 0]
    losses = [t for t in trades if t["pnl"] <= 0]
    eq = pk = dd = 0.0
    for t in sorted(trades, key=lambda t: t["exit_t"]):
        eq += t["pnl"]; pk = max(pk, eq); dd = min(dd, eq - pk)
    return {"trades": len(trades), "win_rate": round(len(wins) / len(trades), 3),
            "avg_win_usd": round(mean(t["pnl"] for t in wins), 2) if wins else 0,
            "avg_loss_usd": round(mean(t["pnl"] for t in losses), 2) if losses else 0,
            "expectancy_r": round(mean(rs), 3), "expectancy_r_gross": round(mean(t["r_gross"] for t in trades), 3),
            "total_pnl_usd": round(sum(t["pnl"] for t in trades), 2), "total_costs_usd": round(sum(t["cost"] for t in trades), 2),
            "max_drawdown_usd": round(dd, 2),
            "break_even_trades": sum(1 for t in trades if [w for _, _, w in t["legs"]] == ["1:1", "stop"]),
            "full_wins": sum(1 for t in trades if any(w == "target" for _, _, w in t["legs"])),
            "full_losses": sum(1 for t in trades if t["legs"][0][2].startswith("stop"))}


def run(symbols: list[str], days: int, stop_mode: str = "gap", entry_minutes: int = 5, range_hours: int = 1) -> dict:
    now = datetime.now(timezone.utc)
    split = now - timedelta(days=days)
    trades, skipped, unfilled = [], {}, 0
    for sym in symbols:
        crypto = "/" in sym
        try:
            bars = aggregate(five_minute(sym, 2 * days + 30), entry_minutes, crypto)
        except Exception as e:
            print(f"{sym}: data error {e}", flush=True)
            continue
        orders, sk = setups(sym, bars, crypto, stop_mode, range_hours)
        for k, v in sk.items():
            skipped[k] = skipped.get(k, 0) + v
        n = 0
        for o in orders:
            if _ts(o.setup_t) < now - timedelta(days=2 * days):
                continue
            t = simulate(bars, o, 20.0 if crypto else 3.0)
            if t is None:
                unfilled += 1
            elif "skipped" in t:
                skipped[t["skipped"]] = skipped.get(t["skipped"], 0) + 1
            else:
                t["period"] = "recent" if _ts(o.setup_t) >= split else "earlier"
                trades.append(t); n += 1
        print(f"{sym}: {len(bars)} bars, {len(orders)} orders, {n} trades", flush=True)
    result = {
        "params": {"symbols": symbols, "days_per_period": days, "stop": stop_mode, "entry_timeframe_min": entry_minutes, "range_timeframe_hours": range_hours, "equity": EQUITY, "risk_pct": RISK_PCT,
                   "position_pct": POSITION_PCT, "run_at": now.isoformat(timespec="seconds")},
        "all": summarize(trades),
        "recent": summarize([t for t in trades if t["period"] == "recent"]),
        "earlier": summarize([t for t in trades if t["period"] == "earlier"]),
        "long": summarize([t for t in trades if t["direction"] == "long"]),
        "short": summarize([t for t in trades if t["direction"] == "short"]),
        "by_symbol": {s: summarize([t for t in trades if t["symbol"] == s]) for s in symbols},
        "orders_not_filled": unfilled, "setups_skipped": skipped,
    }
    return result, trades


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=180, help="days per period (recent, and the same before it)")
    ap.add_argument("--symbols", required=True)
    ap.add_argument("--stop", choices=["gap", "sweep"], default="gap",
                    help="gap: below the fair value gap's first candle; sweep: below the sweep candle's low")
    ap.add_argument("--entry-minutes", type=int, choices=[5, 15], default=5,
                    help="the lower timeframe for the fair value gap entry (the video: 5 or 15)")
    ap.add_argument("--range-hours", type=int, choices=[1, 4, 24], default=1,
                    help="the candle range timeframe: 1-hour, 4-hour, or 24 = daily (one candle per session)")
    args = ap.parse_args()
    result, trades = run(args.symbols.split(","), args.days, args.stop, args.entry_minutes, args.range_hours)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = STUDIES / f"crt_backtest_{args.range_hours}h_{args.entry_minutes}m_{args.stop}stop_{stamp}.json"
    with gzip.open(out.with_suffix(".trades.jsonl.gz"), "wt") as f:
        f.writelines(json.dumps(t) + "\n" for t in trades)
    out.write_text(json.dumps(result, indent=1))
    for k in ("all", "recent", "earlier", "long", "short"):
        print(k, result[k])
    print("not filled", result["orders_not_filled"], "skipped", result["setups_skipped"])
    print("saved", out)


if __name__ == "__main__":
    main()
