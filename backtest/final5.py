exec(open("/home/user/tradingbot/backtest/bt.py").read())
body = np.abs(c - o) / a
CFG = {
 "A": dict(trend="st5+st1h", atr_mult=4, rr=4, W=9, mask=body >= 1.0),
 "B": dict(trend="st1h", atr_mult=4, rr=4, W=9, mask=body >= 1.0),
 "C": dict(trend="ema200", atr_mult=5, rr=6, W=3, mask=body >= 1.0),
 "D": dict(trend="st5+st1h", atr_mult=4, rr=4, W=9, mask=body >= 0.5),
 "E": dict(trend="st5+st1h", atr_mult=4, rr=4, W=3, mask=None, sess=["london","ny_pre","ny_am"]),
}
for k, cfg in CFG.items():
    T = run(stop_mode=2, min_sl=4, max_atr=12, ret_trades=True, **cfg)
    r = T.r_net.values; eq = np.cumprod(1 + 0.01 * r); dd = (1 - eq / np.maximum.accumulate(eq)).max() * 100
    yrs = T.groupby(T.t.dt.year).r_net.agg(lambda s: (np.prod(1 + 0.01 * s) - 1) * 100).round(1).to_dict()
    print(f"{k}: n={len(r)} win={np.mean(r>0)*100:.0f}% avgR={r.mean():+.3f} total={(eq[-1]-1)*100:+.0f}% maxDD={dd:.0f}%  per-year %: {yrs}")
    print("   exits:", T.code.map({1:'TP',2:'SL',3:'time/NTZ'}).value_counts().to_dict(), " median stop pts:", round(T.risk_pts.median(),1))
