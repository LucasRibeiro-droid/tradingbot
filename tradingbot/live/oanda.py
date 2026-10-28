"""OANDA practice (demo) client for gold and the Nasdaq-100 CFD (REST v20, stdlib only).

Owner, 2026-10-26: paper trade NQ and XAUUSD; Alpaca has neither. OANDA's practice account
has XAU_USD (spot gold) and NAS100_USD (a CFD on the Nasdaq-100 index, which NQ futures track).

Practice only, by construction: every request goes to the practice host, which rejects live
accounts' tokens. Every order carries a client id so a retry can't duplicate it, and nothing
assumes a fill: callers reconcile with ``orders`` / ``open_trades``.

Keys: ``OANDA_API_TOKEN`` and ``OANDA_ACCOUNT_ID`` (environment variables / repository secrets).
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

from ..candles import Candle
from .broker import BrokerError

PRACTICE_URL = "https://api-fxpractice.oanda.com"
INSTRUMENTS = ("XAU_USD", "NAS100_USD")
GRANULARITY = {"1Min": "M1", "5Min": "M5", "15Min": "M15", "1Hour": "H1"}


def _rfc3339(t: datetime) -> str:
    return t.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000000000Z")


class Practice:
    def __init__(self, token: str | None = None, account_id: str | None = None, transport=None):
        self._headers = {"Authorization": f"Bearer {token or os.environ['OANDA_API_TOKEN']}",
                         "Content-Type": "application/json", "Accept-Datetime-Format": "RFC3339"}
        self.account_id = account_id or os.environ.get("OANDA_ACCOUNT_ID") or os.environ["OANDA_ACCOUNT"]
        self._transport = transport  # tests: (method, url, body) -> dict
        self._specs: dict[str, dict] = {}

    def _call(self, method: str, path: str, body: dict | None = None, retries: int = 2):
        url = PRACTICE_URL + path
        if self._transport is not None:
            return self._transport(method, url, body)
        data = json.dumps(body).encode() if body is not None else None
        for attempt in range(retries + 1):
            req = urllib.request.Request(url, data=data, method=method, headers=self._headers)
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    raw = r.read()
                    return json.loads(raw) if raw else None
            except urllib.error.HTTPError as e:
                detail = e.read().decode(errors="replace")[:300]
                if (e.code in (429, 500, 502, 503, 504) or (e.code == 401 and method == "GET")) and attempt < retries:
                    time.sleep(2 ** attempt)
                    continue
                raise BrokerError(f"{method} {path}: HTTP {e.code}: {detail}") from None
            except urllib.error.URLError as e:
                if attempt < retries:
                    time.sleep(2 ** attempt)
                    continue
                raise BrokerError(f"{method} {path}: {e.reason}") from None

    # ---- account ----
    def account(self) -> dict:
        return self._call("GET", f"/v3/accounts/{self.account_id}/summary")["account"]

    def specs(self, instrument: str) -> dict:
        """Price and size precision, minimum size (from the account's instrument list)."""
        if not self._specs:
            names = ",".join(INSTRUMENTS)
            for i in self._call("GET", f"/v3/accounts/{self.account_id}/instruments?instruments={names}")["instruments"]:
                self._specs[i["name"]] = i
        return self._specs[instrument]

    def price(self, instrument: str, value: float) -> str:
        return f"{value:.{self.specs(instrument)['displayPrecision']}f}"

    def units(self, instrument: str, value: float) -> str:
        """Rounded toward zero to the instrument's size precision (never more than asked)."""
        p = self.specs(instrument)["tradeUnitsPrecision"]
        q = int(abs(value) * 10 ** p) / 10 ** p
        return f"{q if value >= 0 else -q:.{p}f}"

    # ---- data ----
    def candles(self, instrument: str, timeframe: str, start: datetime, end: datetime | None = None) -> list[Candle]:
        """Mid-price candles, oldest first; the last one may still be forming (``closed`` False)."""
        out: list[Candle] = []
        frm = start
        end = end or datetime.now(timezone.utc)
        while True:
            q = urllib.parse.urlencode({"granularity": GRANULARITY[timeframe], "price": "M", "from": _rfc3339(frm), "count": 5000})
            got = self._call("GET", f"/v3/instruments/{instrument}/candles?{q}")["candles"]
            new = [c for c in got if not out or c["time"] > out[-1].t]
            for c in new:
                m = c["mid"]
                out.append(Candle(c["time"][:19] + "Z", float(m["o"]), float(m["h"]), float(m["l"]), float(m["c"]), bool(c["complete"])))
            if len(got) < 5000 or not new or datetime.fromisoformat(out[-1].t.replace("Z", "+00:00")) >= end:
                return [c for c in out if datetime.fromisoformat(c.t.replace("Z", "+00:00")) < end]
            frm = datetime.fromisoformat(out[-1].t.replace("Z", "+00:00")) + timedelta(seconds=1)

    # ---- orders ----
    def limit_bracket(self, instrument: str, units: float, entry: float, take_profit: float, stop: float,
                      client_id: str, expires: datetime) -> dict:
        """A limit entry with its stop and take profit attached, cancelled by OANDA itself at
        ``expires`` if not filled (GTD). ``units`` > 0 buys, < 0 sells."""
        order = {"type": "LIMIT", "instrument": instrument, "units": self.units(instrument, units),
                 "price": self.price(instrument, entry), "timeInForce": "GTD", "gtdTime": _rfc3339(expires),
                 "positionFill": "DEFAULT", "clientExtensions": {"id": client_id},
                 "takeProfitOnFill": {"price": self.price(instrument, take_profit), "timeInForce": "GTC"},
                 "stopLossOnFill": {"price": self.price(instrument, stop), "timeInForce": "GTC"}}
        r = self._call("POST", f"/v3/accounts/{self.account_id}/orders", {"order": order})
        if "orderCancelTransaction" in r or "orderRejectTransaction" in r:
            why = (r.get("orderCancelTransaction") or r.get("orderRejectTransaction"))
            raise BrokerError(f"order {client_id} refused: {why.get('reason') or why.get('rejectReason')}")
        return r["orderCreateTransaction"]

    def pricing(self, instruments) -> dict[str, dict]:
        q = urllib.parse.urlencode({"instruments": ",".join(instruments)})
        return {x["instrument"]: x for x in self._call("GET", f"/v3/accounts/{self.account_id}/pricing?{q}")["prices"]}

    def order(self, order_id: str) -> dict:
        return self._call("GET", f"/v3/accounts/{self.account_id}/orders/{order_id}")["order"]

    def orders(self) -> list[dict]:
        return self._call("GET", f"/v3/accounts/{self.account_id}/pendingOrders")["orders"]

    def open_trades(self) -> list[dict]:
        return self._call("GET", f"/v3/accounts/{self.account_id}/openTrades")["trades"]

    def trade(self, trade_id: str) -> dict:
        return self._call("GET", f"/v3/accounts/{self.account_id}/trades/{trade_id}")["trade"]

    def cancel(self, order_id: str) -> dict:
        return self._call("PUT", f"/v3/accounts/{self.account_id}/orders/{order_id}/cancel")

    def transactions_since(self, transaction_id: str) -> list[dict]:
        return self._call("GET", f"/v3/accounts/{self.account_id}/transactions/sinceid?id={transaction_id}")["transactions"]
