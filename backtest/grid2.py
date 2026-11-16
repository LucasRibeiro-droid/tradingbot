exec(open("/home/user/tradingbot/backtest/bt.py").read())
import itertools
body = np.abs(c - o) / a
masks = {"b0": None, "b05": body >= 0.5, "b1": body >= 1.0}
SESS = {"all": None, "noAsia": ["london","ny_pre","ny_am","ny_pm","late"], "lonNY": ["london","ny_pre","ny_am"], "NYam": ["ny_pre","ny_am"]}
rows = []
for tr, am, rr, W, mk, ss in itertools.product(["st1h","ema200","st5+st1h"], [2.0, 3.0, 4.0], [2, 3, 4], [3, 9], list(masks), list(SESS)):
    r = run(trend=tr, stop_mode=2, atr_mult=am, rr=rr, W=W, min_sl=4, max_atr=9, mask=masks[mk], sess=SESS[ss])
    r.update(trend=tr, atr_mult=am, rr=rr, W=W, body=mk, sess=ss); rows.append(r)
pd.DataFrame(rows).to_pickle("/tmp/claude-0/-home-user-tradingbot/df70ef2e-c468-5b83-a3b1-1abfe0c61852/scratchpad/grid2.pkl")
print("done")
