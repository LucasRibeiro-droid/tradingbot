# quick port of the TradeSmart filters to see which rule removes the setups (NQ 5m, last 6 months)
import sys, numpy as np, pandas as pd
b = pd.read_pickle(sys.argv[1] + "/b_5min.pkl"); b = b[b.index >= "2025-11-01"]
o,h,l,c = (b[k].values for k in "ohlc"); n=len(c); tick=0.25
piv=3; swH=swL=np.nan; trend=0; tr=np.zeros(n,int)
for i in range(n):
    p=i-piv
    if p-piv>=0:
        if h[p]==h[p-piv:p+piv+1].max() and (h[p-piv:p]<h[p]).all(): swH=h[p]
        if l[p]==l[p-piv:p+piv+1].min() and (l[p-piv:p]>l[p]).all(): swL=l[p]
    if not np.isnan(swH) and c[i]>swH: trend=1; swH=np.nan
    elif not np.isnan(swL) and c[i]<swL: trend=-1; swL=np.nan
    tr[i]=trend
hr=b.index.hour+b.index.minute/60; asia=(hr>=18)&(hr<21)
gaps=[]; cnt=dict(nw=0,trend=0,asia=0,ext=0,small=0,fvg=0,ok=0)
for i in range(10,n):
    gaps=[g for g in gaps if i-g[3]<=40]
    for g in gaps:
        g[4]=min(g[4],l[i]) if g[0]==1 else max(g[4],h[i])
    gaps=[g for g in gaps if not ((g[0]==1 and g[4]<=g[2]) or (g[0]==-1 and g[4]>=g[1]))]
    if l[i]>h[i-2]: gaps.append([1,l[i],h[i-2],i,l[i]])
    if h[i]<l[i-2]: gaps.append([-1,l[i-2],h[i],i,h[i]])
    bull=c[i]>o[i] and o[i]-l[i]<=0.25; bear=c[i]<o[i] and h[i]-o[i]<=0.25
    if not(bull or bear): continue
    d=1 if bull else -1; cnt["nw"]+=1
    stop=l[i-9:i+1].min()-4*tick if d==1 else h[i-9:i+1].max()+4*tick
    ext= l[i]<=l[i-9:i+1].min() if d==1 else h[i]>=h[i-9:i+1].max()
    if tr[i]!=d: cnt["trend"]+=1; continue
    if asia[i]: cnt["asia"]+=1; continue
    if ext: cnt["ext"]+=1; continue
    if abs(o[i]-stop)<8*tick: cnt["small"]+=1; continue
    cov=lambda g:(g[1]-g[4])/(g[1]-g[2]) if g[0]==1 else (g[4]-g[2])/(g[1]-g[2])
    if any(g[0]==d and cov(g)<0.5 and ((d==1 and g[1]<stop) or (d==-1 and g[2]>stop)) for g in gaps): cnt["fvg"]+=1; continue
    cnt["ok"]+=1
    for k in range(i+1, min(i+10, n)):
        if (d==1 and l[k]<=o[i]) or (d==-1 and h[k]>=o[i]): cnt["tap"]=cnt.get("tap",0)+1; break
        if (d==1 and l[k]-o[i]<=4*tick) or (d==-1 and o[i]-h[k]<=4*tick): cnt["near"]=cnt.get("near",0)+1; break
    else: cnt["late"]=cnt.get("late",0)+1
print(cnt)
