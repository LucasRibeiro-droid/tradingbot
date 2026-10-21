"""Morning screen: which Alpaca stocks to watch today.

Candidates: Alpaca's most-active stocks by volume, plus SPY and GLD (the instruments the
research tested). Kept if [Bot filters, config.TradingParams]:
  - tradable on Alpaca, not leveraged or inverse (names with 2x/3x/Ultra/Inverse/Bull/Bear)
  - price at least ``min_price``; 20-day average dollar volume at least ``min_dollar_volume``
  - 20-day average daily range at least ``min_range_pct`` of price ("appropriate volatility")
    (consolidated SIP daily bars, which are allowed once 15+ minutes old)
  - a daily bias the account can trade: the last daily break of structure up when shorting is
    disabled [TJR Day 34; LOCKED: never against the higher timeframe]
Ranked by dollar volume; the top ``shortlist`` are watched. At most
``max_instruments_per_day`` of them are traded (LOCKED.max_instruments, Day 4; owner).
"""
from __future__ import annotations

import json
import os
import re
import urllib.request
from datetime import datetime, timedelta, timezone

from ..config import BASELINE, Config
from ..data import fetch_bars
from ..trend import NONE, UP, trend_series

SCREENER_URL = "https://data.alpaca.markets/v1beta1/screener/stocks/most-actives?by={by}&top=50"
ASSET_URL = "https://paper-api.alpaca.markets/v2/assets/{symbol}"
LEVERAGED = re.compile(r"\b(2x|3x|ultra|ultrapro|inverse|short|bull|bear|leveraged|-1x|daily)\b", re.I)


def _get(url: str):
    headers = {"APCA-API-KEY-ID": os.environ["ALPACA_API_KEY"], "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET_KEY"]}
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        return json.load(r)


def screen(config: Config = BASELINE, shorting_enabled: bool = False, extra: tuple[str, ...] = ("SPY", "GLD")) -> dict:
    tp = config.trading
    actives = [x["symbol"] for by in ("volume", "trades")
               for x in _get(SCREENER_URL.format(by=by)).get("most_actives", [])]
    end = datetime.now(timezone.utc) - timedelta(minutes=20)
    rows, rejected = [], {}
    for sym in dict.fromkeys(list(extra) + actives):
        try:
            asset = _get(ASSET_URL.format(symbol=sym))
        except Exception as e:  # unknown or unsupported symbol
            rejected[sym] = f"asset lookup failed: {e}"
            continue
        if not asset.get("tradable"):
            rejected[sym] = "not tradable"
            continue
        if LEVERAGED.search(asset.get("name", "")):
            rejected[sym] = f"leveraged/inverse product: {asset.get('name')}"
            continue
        daily = fetch_bars(sym, "1Day", end - timedelta(days=200), end, feed="sip")
        closed = [c for c in daily if c.closed]
        if len(closed) < 30:
            rejected[sym] = "not enough daily history"
            continue
        price = closed[-1].c
        vols = _daily_volumes(sym, end)
        dollar_vol = sum(p * v for p, v in vols[-20:]) / max(1, len(vols[-20:]))
        bias = trend_series(closed, config.trend)[-1].tradeable_direction
        range_pct = sum((c.h - c.l) / c.c for c in closed[-20:]) / 20 * 100
        why = []
        if price < tp.min_price:
            why.append(f"price {price:.2f} < {tp.min_price}")
        if dollar_vol < tp.min_dollar_volume:
            why.append(f"dollar volume {dollar_vol / 1e6:.0f}M < {tp.min_dollar_volume / 1e6:.0f}M")
        if range_pct < tp.min_range_pct:
            why.append(f"average daily range {range_pct:.2f}% < {tp.min_range_pct}%")
        if bias == NONE:
            why.append("no clear daily bias")
        elif bias != UP and not shorting_enabled:
            why.append("daily bias down; shorting disabled")
        if why:
            rejected[sym] = "; ".join(why)
            continue
        rows.append({"symbol": sym, "price": round(price, 2), "dollar_volume_m": round(dollar_vol / 1e6, 1),
                     "range_pct": round(range_pct, 2),
                     "daily_bias": "up" if bias == UP else "down", "name": asset.get("name")})
    rows.sort(key=lambda r: -r["dollar_volume_m"])
    return {"t": datetime.now(timezone.utc).isoformat(timespec="seconds"), "watch": rows[:tp.shortlist],
            "also_qualified": rows[tp.shortlist:], "rejected": rejected}


def _daily_volumes(symbol: str, end: datetime) -> list[tuple[float, float]]:
    """(close, volume) of recent daily SIP bars."""
    start = (end - timedelta(days=40)).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = (f"https://data.alpaca.markets/v2/stocks/{symbol}/bars?timeframe=1Day&start={start}"
           f"&end={end.strftime('%Y-%m-%dT%H:%M:%SZ')}&feed=sip&adjustment=all&limit=100")
    return [(b["c"], b["v"]) for b in _get(url).get("bars") or []]
