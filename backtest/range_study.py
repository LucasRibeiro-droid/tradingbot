"""Range strategy study: support/resistance zones (repeated swing rejections) + no-wick candles AT the zone
in the rejection direction.  Sell bearish no-wick at resistance, buy bullish no-wick at support.
Stop beyond the zone + breathing room.  Tested with 1-minute fills on NQ 2021 -> Apr 2026.
"""
exec(open("/home/user/tradingbot/backtest/bt.py").read())
import itertools
from numba import njit

PIV = 3
phb, plb = _pivots(o, h, l, c, PIV)          # pivot bar index confirmed at bar i (body pivots)
# use WICK swings for S/R: recompute wick pivots
@njit(cache=False)
def wick_pivots(h, l, piv):
    n = len(h); ph = np.full(n, -1, np.int64); pl = np.full(n, -1, np.int64)
    for i in range(2 * piv, n):
        p = i - piv; isH = True; isL = True
        for k in range(p - piv, p + piv + 1):
            if k != p:
                if h[k] >= h[p]: isH = False
                if l[k] <= l[p]: isL = False
        if isH: ph[i] = p
        if isL: pl[i] = p
    return ph, pl
wph, wpl = wick_pivots(h, l, PIV)


@njit(cache=False)
def build_setups(o, h, l, c, a, nw, okbar, wph, wpl, L, zw, minT, buf, tgt_mode, rr, er, erMax, skipLast):
    """For each no-wick bar: is its level inside a zone with >= minT swing touches (last L bars)?
       bear no-wick at resistance (swing highs) → sell; bull no-wick at support (swing lows) → buy.
       tgt_mode 0 = rr × risk, 1 = opposite zone edge, 2 = middle of the range."""
    n = len(c)
    S_bar = np.full(n, -1, np.int64); S_dir = np.zeros(n, np.int8); S_e = np.zeros(n); S_s = np.zeros(n); S_t = np.zeros(n)
    cnt = 0
    hp = np.zeros(400); lp = np.zeros(400)
    for i in range(L + 10, n):
        d = nw[i]
        if d == 0 or not okbar[i]: continue
        if erMax < 1.0 and er[i] > erMax: continue
        # collect swing highs / lows confirmed in the window, skipping the current swing (last skipLast bars)
        nh = 0; nl = 0
        for k in range(i - L, i + 1):
            if wph[k] >= 0 and wph[k] < i - skipLast and nh < 400:
                hp[nh] = h[wph[k]]; nh += 1
            if wpl[k] >= 0 and wpl[k] < i - skipLast and nl < 400:
                lp[nl] = l[wpl[k]]; nl += 1
        w = zw * a[i]; lvl = o[i]
        if d == -1:
            # resistance zone around the level: swing highs within ±w of the no-wick open
            t = 0; ztop = -1e18; zbot = 1e18
            for j in range(nh):
                if abs(hp[j] - lvl) <= w:
                    t += 1; ztop = max(ztop, hp[j]); zbot = min(zbot, hp[j])
            if t < minT: continue
            st = max(ztop, h[i]) + buf * a[i]
            rk = st - lvl
            if rk <= 0: continue
            # support below: highest cluster of swing lows (>= minT within ±w) below the entry
            sup = -1e18
            for j in range(nl):
                if lp[j] < lvl - rk * 0.5:
                    tt = 0
                    for q in range(nl):
                        if abs(lp[q] - lp[j]) <= w: tt += 1
                    if tt >= minT and lp[j] > sup: sup = lp[j]
            if tgt_mode == 0: tp = lvl - rr * rk
            else:
                if sup < -1e17: continue
                tp = sup + 0.1 * a[i] if tgt_mode == 1 else (lvl + sup) / 2
                if lvl - tp < 0.8 * rk: continue
        else:
            t = 0; ztop = -1e18; zbot = 1e18
            for j in range(nl):
                if abs(lp[j] - lvl) <= w:
                    t += 1; ztop = max(ztop, lp[j]); zbot = min(zbot, lp[j])
            if t < minT: continue
            st = min(zbot, l[i]) - buf * a[i]
            rk = lvl - st
            if rk <= 0: continue
            res = 1e18
            for j in range(nh):
                if hp[j] > lvl + rk * 0.5:
                    tt = 0
                    for q in range(nh):
                        if abs(hp[q] - hp[j]) <= w: tt += 1
                    if tt >= minT and hp[j] < res: res = hp[j]
            if tgt_mode == 0: tp = lvl + rr * rk
            else:
                if res > 1e17: continue
                tp = res - 0.1 * a[i] if tgt_mode == 1 else (lvl + res) / 2
                if tp - lvl < 0.8 * rk: continue
        S_bar[cnt] = i; S_dir[cnt] = d; S_e[cnt] = lvl; S_s[cnt] = st; S_t[cnt] = tp; cnt += 1
    return S_bar[:cnt], S_dir[:cnt], S_e[:cnt], S_s[:cnt], S_t[:cnt]


@njit(cache=False)
def sim_setups(S_bar, S_dir, S_e, S_s, S_t, W, mstart, mend, m_h, m_l, m_c, m_ok, m_flat, max_hold):
    m = len(S_bar); n5 = len(mstart)
    R = np.full(m, np.nan); EIN = np.full(m, -1, np.int64); EOUT = np.full(m, -1, np.int64); CODE = np.zeros(m, np.int8)
    for j in range(m):
        i = S_bar[j]; d = S_dir[j]; e = S_e[j]; st = S_s[j]; tp = S_t[j]
        if i + 1 >= n5: continue
        endb = min(i + W, n5 - 1); fill = -1
        for mm in range(mstart[i + 1], mend[endb]):
            if not m_ok[mm]: continue
            # target reached before the tap → setup used up
            if (d == 1 and m_h[mm] >= tp) or (d == -1 and m_l[mm] <= tp): break
            if (d == 1 and m_l[mm] <= e) or (d == -1 and m_h[mm] >= e):
                fill = mm; break
        if fill < 0: continue
        code = 0; xp = 0.0; xm = -1
        if (d == 1 and m_l[fill] <= st) or (d == -1 and m_h[fill] >= st):
            code = 2; xp = st; xm = fill
        else:
            lim = min(fill + max_hold, len(m_c) - 1)
            for mm in range(fill + 1, lim + 1):
                if m_flat[mm]:
                    code = 3; xm = mm; xp = m_c[mm - 1]; break
                if (d == 1 and m_l[mm] <= st) or (d == -1 and m_h[mm] >= st):
                    code = 2; xp = st; xm = mm; break
                if (d == 1 and m_h[mm] >= tp) or (d == -1 and m_l[mm] <= tp):
                    code = 1; xp = tp; xm = mm; break
            if code == 0:
                code = 3; xm = lim; xp = m_c[lim]
        R[j] = (xp - e) * d / abs(e - st); EIN[j] = fill; EOUT[j] = xm; CODE[j] = code
    return R, EIN, EOUT, CODE


# efficiency ratio over the last 48 bars (0 = pure chop, 1 = straight line)
dc = np.abs(np.diff(c, prepend=c[0]))
er = (np.abs(b.c - b.c.shift(48)) / pd.Series(dc).rolling(48).sum().values).fillna(1).values
m_ok = ~m_ntz
m_flat = m_ntz & ~np.append(False, m_ntz[:-1])
okb = ~ntz5
body = np.abs(c - o) / a
yrs_all = (m1.index[-1] - m1.index[0]).days / 365.25


def test(L=288, zw=0.5, minT=3, buf=0.25, tgt=0, rr=1.0, W=9, erMax=1.0, skipLast=6, minbody=0.0, sess=None, cap=3, ret=False):
    ok = okb & (body >= minbody)
    if sess is not None:
        ok = ok & np.isin(session_of(nyh5), sess)
    S = build_setups(o, h, l, c, a, nw, ok, wph, wpl, L, zw, minT, buf, tgt, rr, er, erMax, skipLast)
    R, EIN, EOUT, CODE = sim_setups(*S, W, mstart, mend, m1.h.values, m1.l.values, m1.c.values, m_ok, m_flat, 1440)
    f = ~np.isnan(R)
    bar, d, e, s_, t_ = (x[f] for x in S); R, EIN, EOUT, CODE = R[f], EIN[f], EOUT[f], CODE[f]
    keep = cap_concurrent(EIN, EOUT, cap)
    rk = np.abs(e - s_)[keep]
    rn = R[keep] - (COMM + np.where(CODE[keep] == 1, 0, SLIP)) / rk
    t = m1.index[EIN[keep]]; order = np.argsort(t.values); rn = rn[order]; t = t[order]
    if ret:
        return pd.DataFrame(dict(t=t, r=rn, dir=d[keep][order], risk=rk[order], code=CODE[keep][order]))
    if len(rn) < 30: return dict(n=len(rn))
    tr_ = t.year <= 2023
    return dict(n=len(rn), per_yr=len(rn) / yrs_all, win=(rn > 0).mean() * 100, avgR=rn.mean(),
                trainR=rn[tr_].mean(), testR=rn[~tr_].mean(), risk_pts=np.median(rk))
