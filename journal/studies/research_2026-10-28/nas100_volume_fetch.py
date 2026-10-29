import pickle, sys, urllib.parse
from datetime import datetime, timedelta, timezone
sys.path.insert(0, "/home/user/tradingbot")
from tradingbot.live.oanda import Practice
p = Practice()
vol, frm, end = {}, datetime(2024, 12, 29, tzinfo=timezone.utc), datetime(2026, 10, 29, tzinfo=timezone.utc)
while frm < end:
    q = urllib.parse.urlencode({"granularity": "M1", "price": "M", "count": 5000, "from": frm.strftime("%Y-%m-%dT%H:%M:%S.000000000Z")})
    got = p._call("GET", f"/v3/instruments/NAS100_USD/candles?{q}")["candles"]
    if not got: break
    for c in got:
        if c["complete"]:
            vol[int(datetime.fromisoformat(c["time"][:19] + "+00:00").timestamp())] = int(c["volume"])
    last = datetime.fromisoformat(got[-1]["time"][:19] + "+00:00")
    if len(got) < 5000: break
    frm = last + timedelta(seconds=1)
pickle.dump(vol, open("/root/.cache/tradingbot/learn/nas100_m1_volume_2025_2026.pkl", "wb"))
print(len(vol))
