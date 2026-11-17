exec(open("/home/user/tradingbot/backtest/range_study.py").read())
rows = []
for buf, zw, minT, (tg, rr), W, mb, L in itertools.product([0.5, 1.0, 2.0], [0.5, 1.0], [3, 4], [(0, 1), (0, 2), (1, 0), (2, 0)], [3, 9], [0.0, 0.5], [288, 864]):
    r = test(L=L, zw=zw, minT=minT, buf=buf, tgt=tg, rr=rr, W=W, minbody=mb)
    r.update(buf=buf, zw=zw, minT=minT, tgt=tg, rr=rr, W=W, mb=mb, L=L); rows.append(r)
G = pd.DataFrame(rows); G.to_pickle("/tmp/claude-0/-home-user-tradingbot/df70ef2e-c468-5b83-a3b1-1abfe0c61852/scratchpad/grid_range.pkl")
G["minTT"] = G[["trainR", "testR"]].min(axis=1); pd.set_option("display.width", 220)
print(G[G.n >= 300].sort_values("minTT", ascending=False).head(20).round(3).to_string())
for k in ["buf", "zw", "minT", "tgt", "rr", "W", "mb", "L"]: print(G.groupby(k)[["avgR", "trainR", "testR"]].mean().round(3).T.to_string())
