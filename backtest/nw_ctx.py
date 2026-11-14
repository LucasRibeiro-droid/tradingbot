exec(open("/home/user/tradingbot/backtest/bt.py").read())
import pandas as pd, numpy as np
X = pd.read_pickle(sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].endswith("X.pkl") else "/tmp/claude-0/-home-user-tradingbot/df70ef2e-c468-5b83-a3b1-1abfe0c61852/scratchpad/topinX.pkl")
P = X.pivot_table(index="t", columns="side", values="p_oos")      # side -1 = P(high in), +1 = P(low in)
for tr in ["none", "st5", "body5", "st15", "body15", "st1h"]:
    show(tr, run(trend=tr))
T = run(trend="st5", ret_trades=True)
T["p_hi_in"] = P[-1].reindex(T.bar).values; T["p_lo_in"] = P[1].reindex(T.bar).values
# for a LONG the danger is "the day's LOW is not in / the HIGH is in"; P(against) = P(the extreme in MY direction is already in)
T["p_my_ext_in"] = np.where(T.dir == 1, T.p_hi_in, T.p_lo_in)       # long when the high is in = buying after the top
T["p_opp_ext_in"] = np.where(T.dir == 1, T.p_lo_in, T.p_hi_in)      # long when the low is in = buying after the bottom
for col in ["p_my_ext_in", "p_opp_ext_in"]:
    q = pd.cut(T[col], [0, .2, .4, .6, .8, .9, 1.0])
    print("\n", col); print(T.groupby(q, observed=True).r_net.agg(["size", "mean", lambda s: (s > 0).mean()]).round(3).to_string())
print("\nby session"); print(T.groupby("sess").r_net.agg(["size","mean"]).round(3).to_string())
T.to_pickle("/tmp/claude-0/-home-user-tradingbot/df70ef2e-c468-5b83-a3b1-1abfe0c61852/scratchpad/nw_st5_trades.pkl")
