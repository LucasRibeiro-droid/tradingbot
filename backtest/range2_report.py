"""Charts + stats for range play v2.  python3 -I -c "OUT='<dir>'; exec(open('range2_report.py').read())" """
exec(open("/home/user/tradingbot/backtest/range2.py").read())
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

CFG = dict(N=96, zf=1.5, k=2, space=3, breath=1.0, legs=3)
T = run2(ret=True, **CFG)

def plot(k, fn, tag):
    tr = T.iloc[k]; i = int(tr.bar); N = CFG["N"]
    xb = b.index.get_indexer([tr.exit_t.floor("5min")])[0]
    xb = i + 30 if xb < 0 else xb
    a0, a1 = i - N, min(xb + 12, len(c) - 1)
    fig, ax = plt.subplots(figsize=(13, 6.5), dpi=110)
    fig.patch.set_facecolor("#0e1117"); ax.set_facecolor("#0e1117")
    for x, q in enumerate(range(a0, a1 + 1)):
        col = "#26a69a" if c[q] >= o[q] else "#ef5350"
        ax.vlines(x, l[q], h[q], color=col, lw=0.8)
        ax.add_patch(Rectangle((x - 0.35, min(o[q], c[q])), 0.7, max(abs(c[q] - o[q]), 0.25), color=col))
    H, Lo, zh = tr.H, tr.Lo, tr.zh
    pc = "#ab47bc"
    ax.add_patch(Rectangle((0, H - zh), N, zh, facecolor=pc, alpha=0.25, edgecolor=pc, lw=1.5))
    ax.add_patch(Rectangle((0, Lo), N, zh, facecolor=pc, alpha=0.25, edgecolor=pc, lw=1.5))
    ax.text(1, H, "TOP zone (highs reject)", color=pc, fontsize=9, va="bottom")
    ax.text(1, Lo, "BOTTOM zone (lows reject)", color=pc, fontsize=9, va="top")
    xi = i - a0
    xe = b.index.get_indexer([tr.t.floor("5min")])[0] - a0; xx = xb - a0
    ax.axvline(N - 0.5, color="#555", lw=0.8, ls=":")
    ax.annotate("no-wick", (xi, h[i] if tr.dir == -1 else l[i]), xytext=(xi, h[i] + 1.5 * zh if tr.dir == -1 else l[i] - 1.5 * zh),
                color="yellow", fontsize=9, ha="center", arrowprops=dict(color="yellow", arrowstyle="->"))
    ax.hlines(tr.entry, xi, xx, color="white", lw=1.2, ls="--"); ax.text(xx + 0.5, tr.entry, f"entry {tr.entry:.2f}", color="white", fontsize=8, va="center")
    ax.hlines(tr.stop, xe, xx, color="#ff1744", lw=1.6); ax.text(xx + 0.5, tr.stop, f"SL {tr.stop:.2f}", color="#ff1744", fontsize=8, va="center")
    ax.hlines(tr.tp, xe, xx, color="#00e676", lw=1.6); ax.text(xx + 0.5, tr.tp, f"TP 1:1 {tr.tp:.2f}", color="#00e676", fontsize=8, va="center")
    ax.add_patch(Rectangle((xe, min(tr.entry, tr.stop)), xx - xe, abs(tr.entry - tr.stop), color="#ff1744", alpha=0.12))
    ax.add_patch(Rectangle((xe, min(tr.entry, tr.tp)), xx - xe, abs(tr.entry - tr.tp), color="#00e676", alpha=0.12))
    ax.scatter([xe], [tr.entry], marker="^" if tr.dir == 1 else "v", s=120, color="white", zorder=5)
    res = {1: "TP HIT", 2: "STOPPED OUT", 3: "closed 20:00 London"}[int(tr.code)]
    ax.set_title(f"{tag} — {'SELL at top' if tr.dir == -1 else 'BUY at bottom'}  {tr.t.strftime('%a %d %b %Y %H:%M')} NY  →  {res}  {tr.r:+.2f}R",
                 color="white", fontsize=12)
    ticks = list(range(0, a1 - a0 + 1, 12))
    ax.set_xticks(ticks); ax.set_xticklabels([b.index[a0 + t].strftime("%H:%M") for t in ticks], color="#aaa", fontsize=8)
    ax.tick_params(axis="y", colors="#aaa"); ax.grid(color="#222", lw=0.5)
    for s in ax.spines.values(): s.set_color("#333")
    lo_ = min(l[a0:a1 + 1].min(), tr.stop, tr.tp) - zh; hi_ = max(h[a0:a1 + 1].max(), tr.stop, tr.tp) + zh
    ax.set_ylim(lo_, hi_); ax.set_xlim(-1, a1 - a0 + 14)
    fig.tight_layout(); fig.savefig(fn, facecolor=fig.get_facecolor()); plt.close(fig)

r = T.r.values
eq = np.cumprod(1 + 0.005 * r); dd = (1 - eq / np.maximum.accumulate(eq)).max() * 100
lines = [f"config {CFG}", f"trades {len(r)} ({len(r)/yrs_all:.0f}/yr)  win {np.mean(r>0)*100:.1f}%  avg {r.mean():+.3f}R (before costs {T.r_gross.mean():+.3f}R)  median stop {T.risk.median():.1f} pts",
         f"at 0.5% risk: total {(eq[-1]-1)*100:+.1f}%  max DD {dd:.1f}%",
         T.groupby(T.t.dt.year).r.agg(["size", "mean"]).round(3).to_string(),
         "exits " + str(T.code.map({1: 'TP', 2: 'SL', 3: 'NTZ'}).value_counts().to_dict()),
         f"sells {T[T.dir==-1].r.mean():+.3f}R (n={(T.dir==-1).sum()})  buys {T[T.dir==1].r.mean():+.3f}R (n={(T.dir==1).sum()})"]
open(f"{OUT}/stats.txt", "w").write("\n".join(lines)); print("\n".join(lines))
rec = T[T.t >= "2025-01-01"]
for j, k in enumerate(rec[rec.code == 1].index[-3:]): plot(k, f"{OUT}/range_win{j+1}.png", "WIN")
for j, k in enumerate(rec[rec.code == 2].index[-3:]): plot(k, f"{OUT}/range_loss{j+1}.png", "LOSS")
