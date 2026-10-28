"""Universe for the stocks-in-play ORB test: US common stocks on Alpaca, ranked by dollar volume
in the 20 sessions BEFORE the test period (no hindsight); top 400 with price >= $5."""
import json, os, pickle, urllib.parse, urllib.request
from datetime import datetime, timezone
H = {"APCA-API-KEY-ID": os.environ["ALPACA_API_KEY"], "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET_KEY"]}
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=120) as r: return json.load(r)
assets = get("https://paper-api.alpaca.markets/v2/assets?status=active&asset_class=us_equity")
syms = [a["symbol"] for a in assets if a["tradable"] and a["exchange"] in ("NYSE", "NASDAQ", "ARCA", "AMEX", "BATS")
        and "." not in a["symbol"] and "/" not in a["symbol"]]
print("assets", len(syms))
def daily(symbols, start, end):
    out = {}
    for i in range(0, len(symbols), 200):
        q = {"symbols": ",".join(symbols[i:i+200]), "timeframe": "1Day", "start": start, "end": end, "limit": 10000, "feed": "sip", "adjustment": "all"}
        while True:
            p = get("https://data.alpaca.markets/v2/stocks/bars?" + urllib.parse.urlencode(q))
            for s, b in (p.get("bars") or {}).items(): out.setdefault(s, []).extend(b)
            if not p.get("next_page_token"): break
            q["page_token"] = p["next_page_token"]
    return out
d = daily(syms, "2024-09-01T00:00:00Z", "2024-10-25T00:00:00Z")
rank = []
for s, b in d.items():
    b = b[-20:]
    if len(b) < 20: continue
    px = b[-1]["c"]; dv = sum(x["c"] * x["v"] for x in b) / 20
    if px >= 5: rank.append((dv, s))
rank.sort(reverse=True)
uni = [s for _, s in rank[:400]]
json.dump(uni, open("/root/.cache/tradingbot/orb/universe_2024-10.json", "w"))
print(len(uni), uni[:30])
