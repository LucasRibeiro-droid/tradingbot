"""5-minute bars WITH volume, regular hours only, for the 150 most liquid stocks (no ETFs, ranked Oct 2024),
2024-11-01 to now. Stored as numpy arrays per symbol."""
import json, os, pickle, re, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone
import numpy as np
from zoneinfo import ZoneInfo
NY = ZoneInfo("America/New_York")
H = {"APCA-API-KEY-ID": os.environ["ALPACA_API_KEY"], "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET_KEY"]}
def get(url):
    for a in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=120) as r: return json.load(r)
        except Exception as e:
            time.sleep(2 ** a)
    raise RuntimeError(url)
assets = {a["symbol"]: a["name"] for a in get("https://paper-api.alpaca.markets/v2/assets?status=active&asset_class=us_equity")}
fund = re.compile(r"\b(ETF|ETN|Fund|Trust|Shares|iShares|SPDR|ProShares|Direxion|Invesco|Vanguard|Leveraged|Daily|2X|3X)\b", re.I)
uni = [s for s in json.load(open("/root/.cache/tradingbot/orb/universe_2024-10.json")) if not fund.search(assets.get(s, ""))][:150]
json.dump(uni, open("/root/.cache/tradingbot/orb/stocks150.json", "w"))
print(len(uni), uni[:40], flush=True)
store = {}
end = (datetime.now(timezone.utc).replace(microsecond=0)).isoformat().replace("+00:00", "Z")
for i in range(0, len(uni), 10):
    q = {"symbols": ",".join(uni[i:i+10]), "timeframe": "5Min", "start": "2024-11-01T00:00:00Z", "end": "2026-10-27T21:00:00Z",
         "limit": 10000, "feed": "sip", "adjustment": "all"}
    raw = {}
    while True:
        p = get("https://data.alpaca.markets/v2/stocks/bars?" + urllib.parse.urlencode(q))
        for s, b in (p.get("bars") or {}).items():
            keep = []
            for x in b:
                n = datetime.fromisoformat(x["t"].replace("Z", "+00:00")).astimezone(NY)
                m = n.hour * 60 + n.minute
                if 570 <= m < 960:
                    keep.append((int(n.strftime("%Y%m%d")), m, x["o"], x["h"], x["l"], x["c"], x["v"]))
            raw.setdefault(s, []).extend(keep)
        if not p.get("next_page_token"): break
        q["page_token"] = p["next_page_token"]
    for s, rows in raw.items():
        store[s] = np.array(rows, dtype=np.float64)
    print(i + 10, "symbols", sum(len(v) for v in store.values()), "bars", flush=True)
pickle.dump(store, open("/root/.cache/tradingbot/orb/bars5_150.pkl", "wb"))
print("done")
