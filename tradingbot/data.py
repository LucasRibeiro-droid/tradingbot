"""Market data from Alpaca (stocks and ETFs).

Reads ``ALPACA_API_KEY`` and ``ALPACA_SECRET_KEY`` from the environment. Uses the
free IEX feed by default. Bars whose period has not ended are marked
``closed=False`` so they can never be read (Day 2, 16:50).
"""
from __future__ import annotations

import json
import os
import re
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

from .candles import Candle

DATA_URL = "https://data.alpaca.markets/v2/stocks/{symbol}/bars"
_UNITS = {"Min": "minutes", "Hour": "hours", "Day": "days", "Week": "weeks"}


def timeframe_length(timeframe: str) -> timedelta:
    m = re.fullmatch(r"(\d+)(Min|Hour|Day|Week)", timeframe)
    if not m:
        raise ValueError(f"unsupported timeframe {timeframe!r}; use e.g. 5Min, 1Hour, 1Day, 1Week")
    return timedelta(**{_UNITS[m.group(2)]: int(m.group(1))})


def fetch_bars(symbol: str, timeframe: str, start: datetime, end: datetime | None = None,
               feed: str = "iex") -> list[Candle]:
    headers = {
        "APCA-API-KEY-ID": os.environ["ALPACA_API_KEY"],
        "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET_KEY"],
    }
    params = {"timeframe": timeframe, "start": start.isoformat(), "limit": 10000,
              "feed": feed, "adjustment": "all"}
    if end is not None:
        params["end"] = end.isoformat()

    raw: list[dict] = []
    while True:
        url = DATA_URL.format(symbol=symbol) + "?" + urllib.parse.urlencode(params)
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
            payload = json.load(r)
        raw.extend(payload.get("bars") or [])
        token = payload.get("next_page_token")
        if not token:
            break
        params["page_token"] = token

    now = datetime.now(timezone.utc)
    length = timeframe_length(timeframe)
    candles = []
    for b in raw:
        opened = datetime.fromisoformat(b["t"].replace("Z", "+00:00"))
        # Daily and weekly bars are stamped at midnight; the session closes later that day.
        closes_at = opened + length if length < timedelta(days=1) else opened + length - timedelta(hours=4)
        candles.append(Candle(b["t"], b["o"], b["h"], b["l"], b["c"], closed=closes_at <= now))
    return candles
