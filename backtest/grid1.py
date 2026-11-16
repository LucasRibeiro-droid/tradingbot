exec(open("/home/user/tradingbot/backtest/bt.py").read())
import itertools, json
rows = []
for tr, (sm, am), rr, ms in itertools.product(list(trends), [(0, 1), (3, 1), (2, 1.5), (2, 3.0)], [1, 1.5, 2, 3], [4, 12]):
    r = run(trend=tr, stop_mode=sm, atr_mult=am, rr=rr, min_sl=ms, max_atr=6)
    r.update(trend=tr, stop=sm, atr_mult=am, rr=rr, min_sl=ms); rows.append(r)
pd.DataFrame(rows).to_pickle("/tmp/claude-0/-home-user-tradingbot/df70ef2e-c468-5b83-a3b1-1abfe0c61852/scratchpad/grid1.pkl")
print("done")
