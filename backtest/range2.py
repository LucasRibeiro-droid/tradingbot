"""Range play v2 (user's definition), NQ 5m, 1-minute fills, TP always 1:1.
RANGE over the last N candles (before the signal candle):
  top zone    = [H - zh, H]   H  = highest high of the window,  zh = zone height (× ATR)
  bottom zone = [Lo, Lo + zh] Lo = lowest low of the window
  • no candle CLOSED outside [Lo, H] in the window (true by construction: H/Lo are the extremes)
  • >= k swing highs inside the top zone and >= k swing lows inside the bottom zone (rejections)
  • space between the zones: (H - Lo) >= space × zh
SELL: bearish no-wick whose open (= its high) is in the top zone (a wick above H up to 0.5 zh allowed)
      AND it closes BELOW the top zone.  Stop above max(H, its high) + breath.  TP = 1:1.
BUY : mirror at the bottom zone.  Tap of the open within 9 candles.
"""
exec(open("/home/user/tradingbot/backtest/range_study.py").read())


@njit(cache=False)
def build_range_setups(o, h, l, c, a, nw, okbar, wph, wpl, N, zf, k, space, breath, rr, legs):
    n = len(c)
    S_bar = np.full(n, -1, np.int64); S_dir = np.zeros(n, np.int8); S_e = np.zeros(n); S_s = np.zeros(n); S_t = np.zeros(n)
    S_H = np.zeros(n); S_L = np.zeros(n); S_zh = np.zeros(n)
    cnt = 0
    for i in range(N + 10, n):
        d = nw[i]
        if d == 0 or not okbar[i]: continue
        H = -1e18; Lo = 1e18
        for q in range(i - N, i):
            if h[q] > H: H = h[q]
            if l[q] < Lo: Lo = l[q]
        zh = zf * a[i]
        if H - Lo < space * zh: continue
        nh = 0; nl = 0
        for q in range(i - N, i):                 # swings confirmed before the signal candle
            p = wph[q]
            if p >= i - N and h[p] >= H - zh: nh += 1
            p = wpl[q]
            if p >= i - N and l[p] <= Lo + zh: nl += 1
        if nh < k or nl < k: continue
        # price must swing between the zones: count bottom->top->bottom... legs inside the window
        state = 0; nlegs = 0
        for q in range(i - N, i):
            if l[q] <= Lo + zh and state != -1:
                if state == 1: nlegs += 1
                state = -1
            elif h[q] >= H - zh and state != 1:
                if state == -1: nlegs += 1
                state = 1
        if nlegs < legs: continue
        # the range must still be at the zone we trade: last visit was to that zone
        if (d == -1 and state != 1) or (d == 1 and state != -1): continue
        lvl = o[i]
        if d == -1:
            if not (lvl >= H - zh and lvl <= H + 0.5 * zh and c[i] < H - zh): continue
            st = max(H, h[i]) + breath * a[i]
        else:
            if not (lvl <= Lo + zh and lvl >= Lo - 0.5 * zh and c[i] > Lo + zh): continue
            st = min(Lo, l[i]) - breath * a[i]
        rk = abs(lvl - st)
        if rk <= 0: continue
        S_bar[cnt] = i; S_dir[cnt] = d; S_e[cnt] = lvl; S_s[cnt] = st; S_t[cnt] = lvl + d * rr * rk
        S_H[cnt] = H; S_L[cnt] = Lo; S_zh[cnt] = zh; cnt += 1
    return S_bar[:cnt], S_dir[:cnt], S_e[:cnt], S_s[:cnt], S_t[:cnt], S_H[:cnt], S_L[:cnt], S_zh[:cnt]


def run2(N=96, zf=1.0, k=2, space=4, breath=0.5, rr=1.0, W=9, legs=3, ret=False):
    S = build_range_setups(o, h, l, c, a, nw, okb, wph, wpl, N, zf, k, space, breath, rr, legs)
    R, EIN, EOUT, CODE = sim_setups(*S[:5], W, mstart, mend, m1.h.values, m1.l.values, m1.c.values, m_ok, m_flat, 1440)
    f = ~np.isnan(R)
    T = pd.DataFrame(dict(bar=S[0], dir=S[1], entry=S[2], stop=S[3], tp=S[4], H=S[5], Lo=S[6], zh=S[7]))[f]
    T["r_gross"], T["ein"], T["eout"], T["code"] = R[f], EIN[f], EOUT[f], CODE[f]
    keep = cap_concurrent(T.ein.values, T.eout.values, 3); T = T[keep].copy()
    T["risk"] = (T.entry - T.stop).abs()
    T["r"] = T.r_gross - (COMM + np.where(T.code == 1, 0, SLIP)) / T.risk
    T["t"] = m1.index[T.ein.values]; T["exit_t"] = m1.index[T.eout.values]
    T = T.sort_values("t").reset_index(drop=True)
    if ret: return T
    if len(T) < 30: return dict(n=len(T))
    tr_ = T.t.dt.year <= 2023
    return dict(n=len(T), per_yr=len(T) / yrs_all, win=(T.r > 0).mean() * 100, avgR=T.r.mean(), grossR=T.r_gross.mean(),
                trainR=T.r[tr_].mean(), testR=T.r[~tr_].mean(), stop_pts=T.risk.median())


if globals().get("RUN_GRID"):
    rows = []
    for N, zf, lg, space, br in itertools.product([96, 144, 288], [1.0, 1.5], [3, 4, 5], [3, 5], [0.5, 1.0, 2.0]):
        r = run2(N=N, zf=zf, k=2, space=space, breath=br, legs=lg); r.update(N=N, zf=zf, legs=lg, space=space, breath=br); rows.append(r)
    G = pd.DataFrame(rows); G.to_pickle("/tmp/claude-0/-home-user-tradingbot/df70ef2e-c468-5b83-a3b1-1abfe0c61852/scratchpad/grid_range2.pkl")
    G["minTT"] = G[["trainR", "testR"]].min(axis=1); pd.set_option("display.width", 220)
    print(G[G.n >= 200].sort_values("minTT", ascending=False).head(15).round(3).to_string())
    for kk in ["N", "zf", "legs", "space", "breath"]: print(G.groupby(kk)[["avgR", "grossR", "trainR", "testR"]].mean().round(3).T.to_string())
