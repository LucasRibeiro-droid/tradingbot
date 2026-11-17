# Does skipping trend trades that run straight into a rejection zone help strategy A?
exec(open("/home/user/tradingbot/backtest/range_study.py").read())
T = run(trend="st5+st1h", stop_mode=2, atr_mult=4, rr=4, W=9, min_sl=4, max_atr=12, mask=body >= 1.0, ret_trades=True)
pos = pd.Series(np.arange(len(b)), index=b.index)
T["i"] = pos.reindex(T.bar).values
def zone_ahead(i, d, lvl, dist, L=288, zw=0.5, minT=3):
    """count swing highs (for longs) / lows (for shorts) clustered (>= minT within ±zw ATR) between entry and entry ± dist"""
    lo = max(i - L, 0); w = zw * a[i]
    piv = [h[p] for p in wph[lo:i - 5] if p >= 0] if d == 1 else [l[p] for p in wpl[lo:i - 5] if p >= 0]
    piv = np.array(piv)
    if len(piv) == 0: return 0
    sel = piv[(piv > lvl) & (piv < lvl + dist)] if d == 1 else piv[(piv < lvl) & (piv > lvl - dist)]
    best = 0
    for x in sel:
        best = max(best, int((np.abs(piv - x) <= w).sum()))
    return best
for k in [1.0, 2.0]:
    T[f"zone{k}"] = [zone_ahead(int(r.i), r.dir, b.o.values[int(r.i)], k * r.risk_pts) for r in T.itertuples()]
    g = T.groupby(T[f"zone{k}"] >= 3)
    print(f"zone with >=3 rejections within {k}R in the trade's path:")
    print(g.r_net.agg(["size", "mean"]).round(3).to_string())
    for yr, s in T.groupby(T.t.dt.year): print("   ", yr, round(s[s[f'zone{k}'] < 3].r_net.mean(), 3), round(s[s[f'zone{k}'] >= 3].r_net.mean(), 3))
