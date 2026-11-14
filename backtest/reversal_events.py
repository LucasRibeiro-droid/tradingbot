"""Build a dataset of every body CHoCH (trend flip on candle BODIES) on NQ 5m, with context features
and the outcome (did the reversal follow through?).  Data: HistData NSXUSD 1m, 2021 -> Apr 2026.

Usage: python3 -I reversal_events.py <cache_dir> <out.pkl> [piv]
"""
import sys, numpy as np, pandas as pd
from numba import njit
sys.path.insert(0, "/home/user/tradingbot/backtest")
from engine import atr, supertrend, body_structure, htf_on_5m

C, OUT = sys.argv[1], sys.argv[2]
PIV = int(sys.argv[3]) if len(sys.argv) > 3 else 2
b = pd.read_pickle(f"{C}/b_5min.pkl")
b1h = pd.read_pickle(f"{C}/b_1h.pkl")
b15 = pd.read_pickle(f"{C}/b_15min.pkl")
o, h, l, c = (b[k].values for k in "ohlc")
n = len(c)
A = atr(b)

# ── sessions / trading day (futures day starts 18:00 New York) ───────────────────────────────────────
idx = b.index
hr = idx.hour + idx.minute / 60
tday = (idx + pd.Timedelta(hours=6)).normalize()             # 18:00 -> next calendar day
tday_code = pd.factorize(tday)[0]
asia = (hr >= 18) | (hr < 2)
london = (hr >= 2) & (hr < 8)

df = pd.DataFrame(dict(h=h, l=l, o=o, c=c, d=tday_code, asia=asia, lon=london))
g = df.groupby("d")
dHi_run = g.h.cummax().values; dLo_run = g.l.cummin().values          # today's high/low so far
dOpen = g.o.transform("first").values
day = g.agg(H=("h", "max"), L=("l", "min"))
day["rng"] = day.H - day.L
day["adr"] = day.rng.rolling(20).median().shift(1)                    # completed days only
pdH = day.H.shift(1).reindex(tday_code).values
pdL = day.L.shift(1).reindex(tday_code).values
adr = day.adr.reindex(tday_code).values
# Asia / London highs-lows of the current day, available once that session is finished
def sess_levels(mask, end_hour):
    s = df[mask].groupby("d").agg(H=("h", "max"), L=("l", "min"))
    H = s.H.reindex(tday_code).values; L = s.L.reindex(tday_code).values
    done = (hr >= end_hour) & (hr < 18)
    return np.where(done, H, np.nan), np.where(done, L, np.nan)
asH, asL = sess_levels(asia, 2)
lnH, lnL = sess_levels(london, 8)

ema50 = b.c.ewm(span=50, adjust=False).mean().values
ema200 = b.c.ewm(span=200, adjust=False).mean().values
delta = b.c.diff()
up = delta.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
dn = (-delta.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
rsi = (100 - 100 / (1 + up / dn)).values
# "VWAP" proxy (no volume in the data): session TWAP of typical price from 18:00
tp = (h + l + c) / 3
twap = pd.Series(tp).groupby(tday_code).expanding().mean().reset_index(level=0, drop=True).sort_index().values
st1h = htf_on_5m(b, b1h, supertrend(b1h))
bs1h = htf_on_5m(b, b1h, body_structure(b1h, 2))
bs15 = htf_on_5m(b, b15, body_structure(b15, 2))


@njit(cache=True)
def events(o, h, l, c, A, piv):
    """Body-structure trend; record each flip (CHoCH). For a flip DOWN at bar s:
       extreme bar = highest high since the previous flip (the top that should be the reversal),
       stop = extreme high, entry = close[s]. Outcome scanned forward on 5m bars (tie = stop first)."""
    n = len(c); top = np.maximum(o, c); bot = np.minimum(o, c)
    lastH = np.nan; lastL = np.nan; lastHbar = -1; lastLbar = -1
    t = 0; flipbar = 0
    prevSwH = np.full(n, np.nan); prevSwL = np.full(n, np.nan)   # most recent confirmed pivot (wick) before bar
    psH = np.nan; psL = np.nan
    ev_s = []; ev_d = []; ev_x = []; ev_brk = []; ev_brkbar = []; ev_prevflip = []
    for i in range(n):
        p = i - piv
        if p - piv >= 0:
            isH = True; isL = True
            for k in range(p - piv, p + piv + 1):
                if k != p:
                    if top[k] >= top[p]: isH = False
                    if bot[k] <= bot[p]: isL = False
            if isH:
                lastH = top[p]; lastHbar = p; psH = h[p]
            if isL:
                lastL = bot[p]; lastLbar = p; psL = l[p]
        prevSwH[i] = psH; prevSwL[i] = psL
        nt = t
        brk = np.nan; bb = -1
        if not np.isnan(lastH) and c[i] > lastH:
            nt = 1; brk = lastH; bb = lastHbar; lastH = np.nan
        elif not np.isnan(lastL) and c[i] < lastL:
            nt = -1; brk = lastL; bb = lastLbar; lastL = np.nan
        if nt != t and t != 0 and i - flipbar <= 400:
            # extreme since previous flip
            x = flipbar
            for k in range(flipbar, i + 1):
                if nt == -1 and h[k] >= h[x]: x = k
                if nt == 1 and l[k] <= l[x]: x = k
            ev_s.append(i); ev_d.append(nt); ev_x.append(x); ev_brk.append(brk); ev_brkbar.append(bb)
            ev_prevflip.append(flipbar)
        if nt != t:
            t = nt; flipbar = i
    return (np.array(ev_s), np.array(ev_d), np.array(ev_x), np.array(ev_brk), np.array(ev_brkbar),
            np.array(ev_prevflip), prevSwH, prevSwL)


@njit(cache=True)
def outcomes(h, l, c, A, s_arr, d_arr, stop_arr, maxbars):
    m = len(s_arr)
    r1 = np.zeros(m, np.int8); r2 = np.zeros(m, np.int8); r3 = np.zeros(m, np.int8)
    mfeA = np.zeros(m); mfeR = np.zeros(m); barsToStop = np.full(m, -1)
    for j in range(m):
        s = s_arr[j]; d = d_arr[j]; e = c[s]; st = stop_arr[j]; rk = abs(e - st)
        if rk <= 0: continue
        best = 0.0
        for k in range(s + 1, min(s + maxbars, len(c))):
            adv = (h[k] >= st) if d == -1 else (l[k] <= st)
            fav = (e - l[k]) if d == -1 else (h[k] - e)
            if adv:
                barsToStop[j] = k - s; break
            if fav > best: best = fav
        mfeR[j] = best / rk; mfeA[j] = best / A[s]
        r1[j] = best >= rk; r2[j] = best >= 2 * rk; r3[j] = best >= 3 * rk
    return r1, r2, r3, mfeA, mfeR, barsToStop


s, d, x, brk, brkbar, pflip, prevSwH, prevSwL = events(o, h, l, c, A, PIV)
stop = np.where(d == -1, h[x], l[x])
r1, r2, r3, mfeA, mfeR, b2s = outcomes(h, l, c, A, s, d, stop, 288)   # up to 1 day

E = pd.DataFrame(dict(t=idx[s], s=s, d=d, x=x, bars_ext_to_choch=s - x))
E["risk_atr"] = np.abs(c[s] - stop) / A[s]
E["risk_pts"] = np.abs(c[s] - stop)
E["hit1R"], E["hit2R"], E["hit3R"], E["mfe_atr"], E["mfe_R"] = r1, r2, r3, mfeA, mfeR
E["rev4atr"] = (mfeA >= 4).astype(np.int8)                   # a "real" reversal: 4 ATR before the stop
E["hour"] = hr[s]; E["hour_ext"] = hr[x]
E["year"] = idx[s].year


def sweep_of(level_arr, xi, di):
    """extreme bar took the level (wick beyond) and that bar closed back inside, level fresh (not traded 12 bars before)."""
    lv = level_arr[xi]
    if np.isnan(lv): return 0
    lo_ = max(xi - 12, 0)
    if di == -1:
        return int(h[xi] > lv and c[xi] < lv and (xi == lo_ or h[lo_:xi].max() < lv))
    return int(l[xi] < lv and c[xi] > lv and (xi == lo_ or l[lo_:xi].min() > lv))

def took(level_arr, xi, di):
    lv = level_arr[xi]
    if np.isnan(lv): return 0
    return int(h[xi] > lv) if di == -1 else int(l[xi] < lv)

rows = []
for j in range(len(E)):
    xi, si, di = x[j], s[j], d[j]
    # the swing that was in place BEFORE the extreme (liquidity resting above highs / below lows)
    swH = prevSwH[max(xi - 1, 0)]; swL = prevSwL[max(xi - 1, 0)]
    f = {}
    f["sw_swing"] = sweep_of(np.full(n, swH if di == -1 else swL), xi, di) if not np.isnan(swH if di == -1 else swL) else 0
    f["took_swing"] = (h[xi] > swH) if di == -1 else (l[xi] < swL)
    f["sw_pd"] = sweep_of(pdH if di == -1 else pdL, xi, di)
    f["took_pd"] = took(pdH if di == -1 else pdL, xi, di)
    f["sw_asia"] = sweep_of(asH if di == -1 else asL, xi, di)
    f["took_asia"] = took(asH if di == -1 else asL, xi, di)
    f["sw_lon"] = sweep_of(lnH if di == -1 else lnL, xi, di)
    f["took_lon"] = took(lnH if di == -1 else lnL, xi, di)
    # extreme = the day's high (for tops) / low (for bottoms) so far
    f["ext_is_dayext"] = int(h[xi] >= dHi_run[si]) if di == -1 else int(l[xi] <= dLo_run[si])
    rngUsed = (dHi_run[si] - dLo_run[si]) / adr[si] if adr[si] > 0 else np.nan
    f["range_used"] = rngUsed
    dr = dHi_run[si] - dLo_run[si]
    f["premium"] = ((h[xi] - dLo_run[si]) / dr if di == -1 else (dHi_run[si] - l[xi]) / dr) if dr > 0 else np.nan
    f["ext_from_open_adr"] = ((h[xi] - dOpen[si]) if di == -1 else (dOpen[si] - l[xi])) / adr[si] if adr[si] > 0 else np.nan
    f["ext_ema50_atr"] = ((h[xi] - ema50[xi]) if di == -1 else (ema50[xi] - l[xi])) / A[xi]
    f["ext_ema200_atr"] = ((h[xi] - ema200[xi]) if di == -1 else (ema200[xi] - l[xi])) / A[xi]
    f["ext_twap_atr"] = ((h[xi] - twap[xi]) if di == -1 else (twap[xi] - l[xi])) / A[xi]
    leg0 = pflip[j]
    f["leg_atr"] = ((h[xi] - l[leg0:xi + 1].min()) if di == -1 else (h[leg0:xi + 1].max() - l[xi])) / A[xi]
    f["leg_bars"] = xi - leg0
    rngx = h[xi] - l[xi]
    f["rej_wick"] = ((h[xi] - max(o[xi], c[xi])) if di == -1 else (min(o[xi], c[xi]) - l[xi])) / rngx if rngx > 0 else 0
    f["choch_body_atr"] = abs(c[si] - o[si]) / A[si]
    # biggest body between extreme and CHoCH (displacement)
    f["disp_atr"] = (np.abs(c[xi:si + 1] - o[xi:si + 1]) / A[si]).max()
    # FVG created in the move away from the extreme
    fvg = 0
    for k in range(xi + 2, si + 1):
        if di == -1 and h[k] < l[k - 2]: fvg = 1
        if di == 1 and l[k] > h[k - 2]: fvg = 1
    f["fvg"] = fvg
    # RSI divergence: extreme beyond the previous swing but RSI lower
    lb = max(xi - 60, 0)
    if di == -1:
        pk = lb + int(np.argmax(h[lb:max(xi - 3, lb + 1)]))
        f["rsi_div"] = int(h[xi] > h[pk] and rsi[xi] < rsi[pk] - 2)
        f["rsi_ext"] = rsi[xi]
    else:
        pk = lb + int(np.argmin(l[lb:max(xi - 3, lb + 1)]))
        f["rsi_div"] = int(l[xi] < l[pk] and rsi[xi] > rsi[pk] + 2)
        f["rsi_ext"] = 100 - rsi[xi]
    f["htf1h_st_agree"] = int(st1h[si] == di)
    f["htf1h_bs_agree"] = int(bs1h[si] == di)
    f["htf15_bs_agree"] = int(bs15[si] == di)
    f["nowick_new_dir"] = int(any(((c[k] > o[k]) and (o[k] - l[k] <= 0.25)) if di == 1 else ((c[k] < o[k]) and (h[k] - o[k] <= 0.25)) for k in range(xi, si + 1)))
    f["atr_pct"] = A[si] / c[si] * 100
    rows.append(f)
F = pd.DataFrame(rows)
E = pd.concat([E, F], axis=1)
E.to_pickle(OUT)
print(len(E), "events")
print(E[["hit1R", "hit2R", "hit3R", "rev4atr"]].mean())
