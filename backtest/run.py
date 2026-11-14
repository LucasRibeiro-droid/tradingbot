import sys, os, itertools, numpy as np, pandas as pd
from engine import *
from engine import _pivots

C = sys.argv[1]
b = pd.read_pickle(f"{C}/b_5min.pkl"); m1 = pd.read_pickle(f"{C}/m1.pkl")
b15 = pd.read_pickle(f"{C}/b_15min.pkl"); b1h = pd.read_pickle(f"{C}/b_1h.pkl")

# map each 5m bar -> range of 1m rows
mi = m1.index.floor("5min")
pos = np.searchsorted(mi.values, b.index.values, side="left")
mstart = pos.astype(np.int64); mend = np.append(pos[1:], len(m1)).astype(np.int64)

lon = m1.index.tz_convert("Europe/London")
m_ntz = (lon.hour >= 20)                               # 20:00-24:00 London
lon5 = b.index.tz_convert("Europe/London"); ntz5 = (lon5.hour >= 20)
nyh5 = b.index.hour + b.index.minute / 60

o,h,l,c = (b[k].values for k in "ohlc"); a = atr(b)
TOL = 0.25
nw = np.where((c > o) & (o - l <= TOL), 1, np.where((c < o) & (h - o <= TOL), -1, 0)).astype(np.int8)
ph_bar, pl_bar = {}, {}
for p in (1,2,3):
    ph_bar[p], pl_bar[p] = pivots = _pivots(o,h,l,c,p)

trends = {
  "none":     np.where(nw != 0, nw, 1).astype(np.int8),           # accepts every no-wick
  "st5":      supertrend(b),
  "body5":    body_structure(b, 2),
  "st15":     htf_on_5m(b, b15, supertrend(b15)),
  "body15":   htf_on_5m(b, b15, body_structure(b15, 2)),
  "st1h":     htf_on_5m(b, b1h, supertrend(b1h)),
  "body1h":   htf_on_5m(b, b1h, body_structure(b1h, 2)),
}
ema = b.c.ewm(span=200, adjust=False).mean().values
trends["ema200"] = np.where(c > ema, 1, -1).astype(np.int8)
trends["st5+body15"] = np.where(trends["st5"] == trends["body15"], trends["st5"], 0).astype(np.int8)
trends["st5+st1h"] = np.where(trends["st5"] == trends["st1h"], trends["st5"], 0).astype(np.int8)

COMM, SLIP = 0.62, 0.25          # MNQ: $1.24 round trip = 0.62 pts; 1 tick slippage on stop/time exits

def session_of(hh):
    return np.select([(hh >= 18) | (hh < 2), hh < 8, hh < 9.5, hh < 11.5, hh < 15], ["asia","london","ny_pre","ny_am","ny_pm"], "late")

def stats(r, t):
    if len(r) == 0: return dict(n=0)
    w = r > 0; pf = r[w].sum() / max(-r[~w].sum(), 1e-9)
    eq = np.cumsum(r); dd = (np.maximum.accumulate(np.append(0, eq))[1:] - eq).max()
    comp = np.prod(1 + 0.01 * r) - 1
    yrs = (t[-1] - t[0]).days / 365.25
    return dict(n=len(r), win=w.mean()*100, avgR=r.mean(), pf=pf, totR=r.sum(), ddR=dd,
                compound_pct=comp*100, cagr=((1+comp)**(1/max(yrs,0.1))-1)*100, per_yr=len(r)/max(yrs,0.1))

def run(trend="st5", W=9, stop_mode=0, piv=2, breath=1.0, atr_mult=1.0, rr=1.0, pre_pts=0.0, pre_min_sl=1e9,
        max_atr=3.0, min_sl=4.0, max_hold=60*24, sess=None, cap=3, ntz=True, ret_trades=False):
    okbar = ~ntz5 if ntz else np.ones(len(b), bool)
    if sess is not None:
        okbar = okbar & np.isin(session_of(nyh5), sess)
    m_ok = ~m_ntz if ntz else np.ones(len(m1), bool)
    m_flat = m_ntz & ~np.append(False, m_ntz[:-1]) if ntz else np.zeros(len(m1), bool)   # first NTZ minute
    res = simulate(o,h,l,c,a, trends[trend], nw, okbar, mstart, mend, m1.h.values, m1.l.values, m1.c.values,
                   m_ok, m_flat, ph_bar[piv], pl_bar[piv], W, stop_mode, breath, atr_mult, rr, pre_pts, pre_min_sl,
                   max_atr, min_sl, max_hold)
    bar, d, r, rk, ein, eout, code = res
    keep = cap_concurrent(ein, eout, cap)
    bar, d, r, rk, ein, eout, code = (x[keep] for x in res)
    cost = (COMM + np.where(code == 1, 0, SLIP)) / rk
    rn = r - cost
    order = np.argsort(ein); rn = rn[order]; t = m1.index[ein[order]]
    if ret_trades:
        return pd.DataFrame(dict(t=t, bar=b.index[bar[order]], dir=d[order], r_gross=r[order], r_net=rn,
                                 risk_pts=rk[order], code=code[order], sess=session_of(nyh5[bar[order]])))
    return stats(rn, t)
