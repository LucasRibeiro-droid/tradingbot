"""Alpaca paper-trading client (REST, stdlib only).

Paper only, by construction: the base URL is the paper endpoint, and ``Paper.connect`` refuses
an account whose number doesn't start with "PA" (Alpaca's paper accounts). Every order carries
a ``client_order_id`` so a retried request can't create a duplicate. Nothing here assumes an
order filled: callers reconcile with ``order`` / ``positions``.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

PAPER_URL = "https://paper-api.alpaca.markets"


class BrokerError(RuntimeError):
    pass


class Paper:
    def __init__(self, key: str | None = None, secret: str | None = None):
        self._headers = {
            "APCA-API-KEY-ID": key or os.environ["ALPACA_API_KEY"],
            "APCA-API-SECRET-KEY": secret or os.environ["ALPACA_SECRET_KEY"],
            "Content-Type": "application/json",
        }
        self.account_number: str | None = None

    def _call(self, method: str, path: str, body: dict | None = None, retries: int = 2):
        data = json.dumps(body).encode() if body is not None else None
        for attempt in range(retries + 1):
            req = urllib.request.Request(PAPER_URL + path, data=data, method=method, headers=self._headers)
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    raw = r.read()
                    return json.loads(raw) if raw else None
            except urllib.error.HTTPError as e:
                detail = e.read().decode(errors="replace")[:300]
                if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                    time.sleep(2 * (attempt + 1))
                    continue
                raise BrokerError(f"{method} {path}: HTTP {e.code}: {detail}") from None
            except urllib.error.URLError as e:
                if attempt < retries:
                    time.sleep(2 * (attempt + 1))
                    continue
                raise BrokerError(f"{method} {path}: {e.reason}") from None

    def connect(self) -> dict:
        acct = self._call("GET", "/v2/account")
        if not str(acct.get("account_number", "")).startswith("PA"):
            raise BrokerError("refusing to trade: not a paper account")
        if acct.get("trading_blocked") or acct.get("account_blocked") or acct.get("status") != "ACTIVE":
            raise BrokerError(f"account not tradable: status={acct.get('status')}")
        self.account_number = acct["account_number"]
        return acct

    def account(self) -> dict:
        return self._call("GET", "/v2/account")

    def clock(self) -> dict:
        return self._call("GET", "/v2/clock")

    def positions(self) -> list[dict]:
        return self._call("GET", "/v2/positions")

    def orders(self, status: str = "open", after: str | None = None) -> list[dict]:
        q = f"/v2/orders?status={status}&nested=true&limit=500" + (f"&after={after}" if after else "")
        return self._call("GET", q)

    def order(self, order_id: str) -> dict:
        return self._call("GET", f"/v2/orders/{order_id}?nested=true")

    def order_by_client_id(self, client_order_id: str) -> dict | None:
        try:
            return self._call("GET", f"/v2/orders:by_client_order_id?client_order_id={client_order_id}", retries=0)
        except BrokerError:
            return None

    def bracket(self, symbol: str, qty: int, side: str, take_profit: float, stop: float,
                client_order_id: str) -> dict:
        """Market entry with a take-profit limit and a stop: one part of the ladder."""
        existing = self.order_by_client_id(client_order_id)
        if existing:
            return existing  # already submitted (e.g. a retry after a timeout)
        return self._call("POST", "/v2/orders", {
            # gtc: if the session process dies, the stop and take profit stay live at Alpaca.
            "symbol": symbol, "qty": str(qty), "side": side, "type": "market", "time_in_force": "gtc",
            "order_class": "bracket", "client_order_id": client_order_id,
            "take_profit": {"limit_price": f"{take_profit:.2f}"},
            "stop_loss": {"stop_price": f"{stop:.2f}"},
        }, retries=0)

    def replace_stop(self, order_id: str, stop: float) -> dict:
        return self._call("PATCH", f"/v2/orders/{order_id}", {"stop_price": f"{stop:.2f}"})

    def cancel_all(self) -> None:
        self._call("DELETE", "/v2/orders")

    def close_position(self, symbol: str) -> dict:
        """Market order closing the whole position. Fails while open orders (bracket legs)
        still hold the shares: cancel them first and wait until they are gone."""
        return self._call("DELETE", f"/v2/positions/{symbol}", retries=0)
