exec(open("/home/user/tradingbot/backtest/bt.py").read())
import itertools
body = np.abs(c - o) / a
masks = {"b05": body >= 0.5, "b1": body >= 1.0, "b15": body >= 1.5}
rows = []
for tr, am, rr, W, mk in itertools.product(["st1h","ema200","st5+st1h"], [4.0, 5.0, 6.0], [4, 5, 6], [3, 9], list(masks)):
    r = run(trend=tr, stop_mode=2, atr_mult=am, rr=rr, W=W, min_sl=4, max_atr=12, mask=masks[mk])
    r.update(trend=tr, atr_mult=am, rr=rr, W=W, body=mk); rows.append(r)
G = pd.DataFrame(rows); G["minTT"] = G[["trainR","testR"]].min(axis=1)
pd.set_option("display.width", 220)
print(G[G.n >= 800].sort_values("minTT", ascending=False).head(20).round(3).to_string())
