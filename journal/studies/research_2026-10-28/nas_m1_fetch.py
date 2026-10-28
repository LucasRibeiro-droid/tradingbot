"""OANDA NAS100_USD 1-minute candles with bid and ask, one year."""
import json, pickle, urllib.parse
from datetime import datetime, timedelta, timezone
from tradingbot.live.oanda import Practice
p = Practice()
start = datetime.now(timezone.utc) - timedelta(days=370)
rows, frm = [], start
while True:
    q = urllib.parse.urlencode({"granularity": "M1", "price": "BA", "from": frm.strftime("%Y-%m-%dT%H:%M:%S.000000000Z"), "count": 5000})
    got = p._call("GET", f"/v3/instruments/NAS100_USD/candles?{q}")["candles"]
    new = [c for c in got if c["complete"] and (not rows or c["time"] > rows[-1][0])]
    for c in new:
        b, a = c["bid"], c["ask"]
        rows.append((c["time"][:19] + "Z", float(b["o"]), float(b["h"]), float(b["l"]), float(b["c"]),
                     float(a["o"]), float(a["h"]), float(a["l"]), float(a["c"])))
    if len(got) < 5000 or not new:
        break
    frm = datetime.fromisoformat(rows[-1][0].replace("Z", "+00:00")) + timedelta(seconds=1)
pickle.dump(rows, open("/root/.cache/tradingbot/nas_m1/nas100_m1_ba.pkl", "wb"))
print(len(rows), rows[0][0], rows[-1][0])
