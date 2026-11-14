import sys, numpy as np, pandas as pd
E = pd.read_pickle(sys.argv[1])
E = E[E.risk_atr > 0.3].copy()
y = "hit2R"
base = E[y].mean(); print(f"events {len(E)}  base {y}={base:.3f}  hit1R={E.hit1R.mean():.3f} rev4atr={E.rev4atr.mean():.3f}\n")
bins = ["sw_swing","took_swing","sw_pd","took_pd","sw_asia","took_asia","sw_lon","took_lon","ext_is_dayext","fvg","rsi_div",
        "htf1h_st_agree","htf1h_bs_agree","htf15_bs_agree","nowick_new_dir"]
print("binary feature        n(1)   hit2R|1  hit2R|0   hit1R|1  rev4|1")
for f in bins:
    m = E[f].astype(bool)
    print(f"{f:20s} {m.sum():6d}   {E[y][m].mean():.3f}    {E[y][~m].mean():.3f}    {E.hit1R[m].mean():.3f}   {E.rev4atr[m].mean():.3f}")
conts = ["risk_atr","bars_ext_to_choch","range_used","premium","ext_from_open_adr","ext_ema50_atr","ext_ema200_atr","ext_twap_atr",
         "leg_atr","leg_bars","rej_wick","choch_body_atr","disp_atr","rsi_ext","atr_pct","hour","hour_ext"]
for f in conts:
    q = pd.qcut(E[f], 5, duplicates="drop")
    t = E.groupby(q, observed=True).agg(n=(y,"size"), hit2R=(y,"mean"), hit1R=("hit1R","mean"), rev4=("rev4atr","mean"))
    print(f"\n{f}\n", t.round(3).to_string())
