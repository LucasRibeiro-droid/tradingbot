"""Range play (S/R zones + no-wick, 5m NQ): stats + chart images of winning and losing trades.
Usage: python3 -I range_report.py <out_dir>"""
import sys
OUT = sys.argv[1]
exec(open("/home/user/tradingbot/backtest/range_study.py").read())
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

CONFIGS = {
    "by_eye": dict(L=288, zw=1.0, minT=4, buf=0.25, tgt=0, rr=1.0, W=9),   # stop just past the zone, 1:1
    "best":   dict(L=288, zw=1.0, minT=5, buf=4.0, tgt=2, rr=0, W=9),      # best found: wide stop, mid-range target
}

def trades(cfg):
    ok = okb.copy()
    S = build_setups(o, h, l, c, a, nw, ok, wph, wpl, cfg["L"], cfg["zw"], cfg["minT"], cfg["buf"], cfg["tgt"], cfg["rr"], er, 1.0, 6)
    R, EIN, EOUT, CODE = sim_setups(*S, cfg["W"], mstart, mend, m1.h.values, m1.l.values, m1.c.values, m_ok, m_flat, 1440)
    f = ~np.isnan(R)
    bar, d, e, s_, t_ = (x[f] for x in S); R, EIN, EOUT, CODE = R[f], EIN[f], EOUT[f], CODE[f]
    keep = cap_concurrent(EIN, EOUT, 3)
    T = pd.DataFrame(dict(bar=bar, dir=d, entry=e, stop=s_, tp=t_, r_gross=R, ein=EIN, eout=EOUT, code=CODE))[keep]
    T["risk"] = (T.entry - T.stop).abs()
    T["r"] = T.r_gross - (COMM + np.where(T.code == 1, 0, SLIP)) / T.risk
    T["t"] = m1.index[T.ein.values]
    T["exit_t"] = m1.index[T.eout.values]
    return T.sort_values("t").reset_index(drop=True)

def summary(T, name):
    r = T.r.values
    out = [f"=== {name} ===",
           f"trades {len(r)}  ({len(r)/yrs_all:.0f}/yr)   win {np.mean(r>0)*100:.1f}%   avg {r.mean():+.3f}R   "
           f"median stop {T.risk.median():.1f} pts   PF {r[r>0].sum()/-r[r<=0].sum():.2f}"]
    for rp in (0.5, 1.0):
        eq = np.cumprod(1 + rp / 100 * r); dd = (1 - eq / np.maximum.accumulate(eq)).max() * 100
        out.append(f"  at {rp}% risk: total {(eq[-1]-1)*100:+.1f}%   max drawdown {dd:.1f}%")
    yr = T.groupby(T.t.dt.year).r.agg(["size", "mean", lambda s: (np.prod(1 + 0.005 * s) - 1) * 100])
    yr.columns = ["trades", "avgR", "%@0.5%"]
    out.append(yr.round(3).to_string())
    out.append("exits: " + str(T.code.map({1: "TP", 2: "SL", 3: "time/NTZ"}).value_counts().to_dict()))
    out.append("longs avg %+.3fR (n=%d)   shorts avg %+.3fR (n=%d)" % (T[T.dir == 1].r.mean(), (T.dir == 1).sum(), T[T.dir == -1].r.mean(), (T.dir == -1).sum()))
    return "\n".join(out)

def zone_of(i, d, cfg):
    """the zone the no-wick sat in + the opposite zone (same logic as the backtest)"""
    L, w = cfg["L"], cfg["zw"] * a[i]
    hs = np.array([h[p] for p in wph[i - L:i + 1] if 0 <= p < i - 6])
    ls = np.array([l[p] for p in wpl[i - L:i + 1] if 0 <= p < i - 6])
    P, Q = (hs, ls) if d == -1 else (ls, hs)
    z = P[np.abs(P - o[i]) <= w]
    opp = None
    cand = [x for x in Q if (x < o[i] if d == -1 else x > o[i]) and (np.abs(Q - x) <= w).sum() >= cfg["minT"]]
    if cand:
        x = max(cand) if d == -1 else min(cand)
        zz = Q[np.abs(Q - x) <= w]; opp = (zz.min(), zz.max(), len(zz))
    return (z.min(), z.max(), len(z)), opp, hs, ls

def plot_trade(T, k, cfg, fn, title):
    tr = T.iloc[k]; i = int(tr.bar)
    xb = b.index.get_indexer([tr.exit_t.floor("5min")])[0]
    xb = i + 40 if xb < 0 else xb
    a0, a1 = max(i - 90, 0), min(xb + 15, len(c) - 1)
    fig, ax = plt.subplots(figsize=(13, 6.5), dpi=110)
    fig.patch.set_facecolor("#0e1117"); ax.set_facecolor("#0e1117")
    xs = np.arange(a0, a1 + 1) - a0
    for x, k_ in zip(xs, range(a0, a1 + 1)):
        up = c[k_] >= o[k_]; col = "#26a69a" if up else "#ef5350"
        ax.vlines(x, l[k_], h[k_], color=col, lw=0.8)
        ax.add_patch(Rectangle((x - 0.35, min(o[k_], c[k_])), 0.7, max(abs(c[k_] - o[k_]), 0.25), color=col))
    (zlo, zhi, zn), opp, hs, ls = zone_of(i, int(tr.dir), cfg)
    pad = 0.15 * a[i]
    zc = "#ab47bc"
    ax.add_patch(Rectangle((0, zlo - pad), a1 - a0, zhi - zlo + 2 * pad, color=zc, alpha=0.22))
    ax.text(1, zhi + pad, f"{'RESISTANCE' if tr.dir == -1 else 'SUPPORT'} zone ({zn} rejections)", color=zc, fontsize=9, va="bottom")
    if opp:
        ax.add_patch(Rectangle((0, opp[0] - pad), a1 - a0, opp[1] - opp[0] + 2 * pad, color=zc, alpha=0.12))
        ax.text(1, opp[0] - pad, f"{'SUPPORT' if tr.dir == -1 else 'RESISTANCE'} zone ({opp[2]})", color=zc, fontsize=9, va="top")
    xi, xe = i - a0, (b.index.get_indexer([tr.t.floor("5min")])[0]) - a0
    xx = xb - a0
    ax.annotate("no-wick", (xi, h[i] if tr.dir == -1 else l[i]), xytext=(xi, (h[i] + 1.2 * a[i]) if tr.dir == -1 else (l[i] - 1.2 * a[i])),
                color="yellow", fontsize=9, ha="center", arrowprops=dict(color="yellow", arrowstyle="->"))
    ax.hlines(tr.entry, xi, xx, color="white", lw=1.2, ls="--"); ax.text(xx + 0.5, tr.entry, f"entry {tr.entry:.2f}", color="white", fontsize=8, va="center")
    ax.hlines(tr.stop, xe, xx, color="#ff1744", lw=1.6); ax.text(xx + 0.5, tr.stop, f"SL {tr.stop:.2f}", color="#ff1744", fontsize=8, va="center")
    ax.hlines(tr.tp, xe, xx, color="#00e676", lw=1.6); ax.text(xx + 0.5, tr.tp, f"TP {tr.tp:.2f}", color="#00e676", fontsize=8, va="center")
    ax.add_patch(Rectangle((xe, min(tr.entry, tr.stop)), xx - xe, abs(tr.entry - tr.stop), color="#ff1744", alpha=0.12))
    ax.add_patch(Rectangle((xe, min(tr.entry, tr.tp)), xx - xe, abs(tr.entry - tr.tp), color="#00e676", alpha=0.12))
    ax.scatter([xe], [tr.entry], marker="^" if tr.dir == 1 else "v", s=120, color="white", zorder=5)
    res = {1: "TP HIT", 2: "STOPPED OUT", 3: "closed (time / 20:00 London)"}[int(tr.code)]
    ax.set_title(f"{title} — {'SELL' if tr.dir == -1 else 'BUY'} {tr.t.strftime('%a %d %b %Y %H:%M')} NY   →   {res}  {tr.r:+.2f}R",
                 color="white", fontsize=12)
    ticks = list(range(0, a1 - a0 + 1, 12))
    ax.set_xticks(ticks); ax.set_xticklabels([b.index[a0 + t].strftime("%H:%M") for t in ticks], color="#aaa", fontsize=8)
    ax.tick_params(axis="y", colors="#aaa"); ax.grid(color="#222", lw=0.5)
    for s in ax.spines.values(): s.set_color("#333")
    lo_ = min(l[a0:a1 + 1].min(), tr.stop, tr.tp) - a[i]; hi_ = max(h[a0:a1 + 1].max(), tr.stop, tr.tp) + a[i]
    ax.set_ylim(lo_, hi_); ax.set_xlim(-1, a1 - a0 + 12)
    fig.tight_layout(); fig.savefig(fn, facecolor=fig.get_facecolor()); plt.close(fig)

def equity_plot(Ts, fn):
    fig, ax = plt.subplots(figsize=(12, 5), dpi=110)
    fig.patch.set_facecolor("#0e1117"); ax.set_facecolor("#0e1117")
    for (name, T), col in zip(Ts.items(), ["#ef5350", "#26a69a"]):
        eq = (np.cumprod(1 + 0.005 * T.r.values) - 1) * 100
        ax.plot(T.t.values, eq, color=col, lw=1.5, label=f"{name} (0.5% risk/trade)")
    ax.axhline(0, color="#666", lw=0.8)
    ax.set_title("Range play + no-wick, NQ 5m 2021 → Apr 2026 — account % over time", color="white")
    ax.legend(facecolor="#1a1d24", labelcolor="white"); ax.tick_params(colors="#aaa"); ax.grid(color="#222")
    for s in ax.spines.values(): s.set_color("#333")
    fig.tight_layout(); fig.savefig(fn, facecolor=fig.get_facecolor()); plt.close(fig)

Ts = {}
txt = []
for name, cfg in CONFIGS.items():
    T = trades(cfg); Ts[name] = T
    txt.append(summary(T, name + "  " + str(cfg)))
    recent = T[T.t >= "2025-06-01"]
    wins = recent[recent.code == 1].index[-3:]; losses = recent[recent.code == 2].index[-3:]
    for j, k in enumerate(wins):
        plot_trade(T, k, cfg, f"{OUT}/{name}_win{j+1}.png", f"{name.upper()} WIN")
    for j, k in enumerate(losses):
        plot_trade(T, k, cfg, f"{OUT}/{name}_loss{j+1}.png", f"{name.upper()} LOSS")
equity_plot(Ts, f"{OUT}/equity.png")
open(f"{OUT}/stats.txt", "w").write("\n\n".join(txt))
print("\n\n".join(txt))
