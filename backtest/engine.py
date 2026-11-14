"""No-wick backtest engine on 5m bars with 1-minute fill resolution (numba)."""
import numpy as np, pandas as pd
from numba import njit

# ── indicators ────────────────────────────────────────────────────────────────────────────────────
def atr(b, n=14):
    pc = b.c.shift(1)
    tr = np.maximum(b.h - b.l, np.maximum((b.h - pc).abs(), (b.l - pc).abs())).fillna(b.h - b.l)
    return tr.ewm(alpha=1/n, adjust=False).mean().values      # RMA like Pine

@njit(cache=True)
def _supertrend(h, l, c, a, factor):
    n = len(c); d = np.ones(n, np.int8); up = np.zeros(n); dn = np.zeros(n)
    for i in range(n):
        hl2 = (h[i] + l[i]) / 2
        u = hl2 + factor * a[i]; lo = hl2 - factor * a[i]
        if i == 0:
            up[i] = u; dn[i] = lo; d[i] = 1; continue
        dn[i] = lo if (lo > dn[i-1] or c[i-1] < dn[i-1]) else dn[i-1]
        up[i] = u if (u < up[i-1] or c[i-1] > up[i-1]) else up[i-1]
        if d[i-1] == -1:   # was down (price below upper band)
            d[i] = 1 if c[i] > up[i] else -1
        else:
            d[i] = -1 if c[i] < dn[i] else 1
    return d   # +1 up, -1 down

def supertrend(b, n=10, factor=3.0):
    return _supertrend(b.h.values, b.l.values, b.c.values, atr(b, n), factor)

@njit(cache=True)
def _body_structure(o, c, piv):
    """Trend from body breaks: close above the last swing-high BODY top -> up; below last swing-low body bottom -> down."""
    n = len(c); tr = np.zeros(n, np.int8)
    top = np.maximum(o, c); bot = np.minimum(o, c)
    lastH = np.nan; lastL = np.nan; t = 0
    for i in range(n):
        p = i - piv
        if p - piv >= 0:
            isH = True; isL = True
            for k in range(p - piv, p + piv + 1):
                if k != p:
                    if top[k] >= top[p]: isH = False
                    if bot[k] <= bot[p]: isL = False
            if isH: lastH = top[p]
            if isL: lastL = bot[p]
        if not np.isnan(lastH) and c[i] > lastH: t = 1; lastH = np.nan
        elif not np.isnan(lastL) and c[i] < lastL: t = -1; lastL = np.nan
        tr[i] = t
    return tr

def body_structure(b, piv=2):
    return _body_structure(b.o.values, b.c.values, piv)

def htf_on_5m(b5, bh, arr):
    """Value of a higher-TF series from the LAST CLOSED higher-TF bar, aligned to 5m bars (no lookahead)."""
    s = pd.Series(arr, index=bh.index)
    dur = bh.index[1] - bh.index[0]
    s.index = s.index + dur                                    # available at the HTF bar's close
    s5 = s.reindex(b5.index.union(s.index)).ffill().reindex(b5.index + pd.Timedelta(minutes=5))
    return np.nan_to_num(s5.values).astype(np.int8)            # known at the 5m bar's close

# ── swing pivots (body pivots, wick extreme stored) ───────────────────────────────────────────────
@njit(cache=True)
def _pivots(o, h, l, c, piv):
    n = len(c); top = np.maximum(o, c); bot = np.minimum(o, c)
    ph_bar = np.full(n, -1, np.int64); pl_bar = np.full(n, -1, np.int64)
    for i in range(2 * piv, n):
        p = i - piv; isH = True; isL = True
        for k in range(p - piv, p + piv + 1):
            if k != p:
                if top[k] >= top[p]: isH = False
                if bot[k] <= bot[p]: isL = False
        if isH: ph_bar[i] = p       # confirmed at bar i
        if isL: pl_bar[i] = p
    return ph_bar, pl_bar

# ── main simulation ───────────────────────────────────────────────────────────────────────────────
@njit(cache=True)
def simulate(o, h, l, c, a, trend, nwdir, okbar, mstart, mend, m_h, m_l, m_c, m_ok, m_flat, ph_bar, pl_bar,
             W, stop_mode, breath, atr_mult, rr, pre_pts, pre_min_sl, max_atr, min_sl, max_hold_min):
    """One trade per no-wick setup (independent). Returns arrays per setup.
    stop_mode 0 = recent swing wick, 1 = previous candle (or the one before), 2 = ATR multiple."""
    n = len(c)
    out_bar = np.full(n, -1, np.int64); out_dir = np.zeros(n, np.int8)
    out_r = np.zeros(n); out_risk = np.zeros(n); out_ein = np.full(n, -1, np.int64); out_eout = np.full(n, -1, np.int64)
    out_code = np.zeros(n, np.int8)   # 1 TP, 2 SL, 3 time exit
    cnt = 0
    for i in range(30, n - 1):
        d = nwdir[i]
        if d == 0 or not okbar[i]: continue
        if trend[i] != d: continue
        lvl = o[i]
        # stop
        st = np.nan
        if stop_mode == 0:
            if d == 1:
                for k in range(i, max(i - 400, 0), -1):
                    p = pl_bar[k]
                    if p >= 0 and l[p] < lvl:
                        st = l[p] - breath; break
            else:
                for k in range(i, max(i - 400, 0), -1):
                    p = ph_bar[k]
                    if p >= 0 and h[p] > lvl:
                        st = h[p] + breath; break
        elif stop_mode == 1:
            if d == 1:
                for k in range(i - 1, i - 4, -1):
                    if l[k] < lvl - 0.001: st = l[k] - breath; break
            else:
                for k in range(i - 1, i - 4, -1):
                    if h[k] > lvl + 0.001: st = h[k] + breath; break
        else:
            st = lvl - d * atr_mult * a[i]
        if np.isnan(st): continue
        risk = abs(lvl - st)
        if risk < min_sl or risk > max_atr * a[i]: continue
        entry = lvl + d * (pre_pts if risk > pre_min_sl else 0.0)
        tp = entry + d * rr * abs(entry - st)
        # tap window: bars i+1 .. i+W, cut when trend flips (flip known at that bar's close)
        endb = min(i + W, n - 1)
        for k in range(i + 1, endb + 1):
            if trend[k] != d:
                endb = k; break
        fill = -1
        for m in range(mstart[i + 1], mend[endb]):
            if not m_ok[m]: continue
            if (d == 1 and m_l[m] <= entry) or (d == -1 and m_h[m] >= entry):
                fill = m; break
            # invalidation: price runs to TP before tapping -> setup used up? (keep it simple: no)
        if fill < 0: continue
        code = 0; xp = 0.0; xm = -1
        # fill minute: stop only (conservative)
        if (d == 1 and m_l[fill] <= st) or (d == -1 and m_h[fill] >= st):
            code = 2; xp = st; xm = fill
        else:
            lim = min(fill + max_hold_min, len(m_c) - 1)
            for m in range(fill + 1, lim + 1):
                if m_flat[m]:
                    code = 3; xm = m; xp = m_c[m - 1]; break
                hitS = (d == 1 and m_l[m] <= st) or (d == -1 and m_h[m] >= st)
                hitT = (d == 1 and m_h[m] >= tp) or (d == -1 and m_l[m] <= tp)
                if hitS:
                    code = 2; xp = st; xm = m; break
                if hitT:
                    code = 1; xp = tp; xm = m; break
            if code == 0:
                code = 3; xm = lim; xp = m_c[lim]
        rk = abs(entry - st)
        out_bar[cnt] = i; out_dir[cnt] = d; out_r[cnt] = (xp - entry) * d / rk; out_risk[cnt] = rk
        out_ein[cnt] = fill; out_eout[cnt] = xm; out_code[cnt] = code; cnt += 1
    return out_bar[:cnt], out_dir[:cnt], out_r[:cnt], out_risk[:cnt], out_ein[:cnt], out_eout[:cnt], out_code[:cnt]

def cap_concurrent(ein, eout, cap):
    order = np.argsort(ein, kind="stable"); keep = np.zeros(len(ein), bool); open_ = []
    for j in order:
        open_ = [x for x in open_ if x > ein[j]]
        if len(open_) < cap:
            keep[j] = True; open_.append(eout[j])
    return keep
