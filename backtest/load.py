"""Load HistData NSXUSD M1 csv files (EST, no DST) -> 1m and 5m bars in New York time."""
import glob, os, sys, numpy as np, pandas as pd

def load_1m(data_dir):
    files = sorted(glob.glob(os.path.join(data_dir, "DAT_ASCII_NSXUSD_M1_*.csv")))
    dfs = [pd.read_csv(f, sep=";", header=None, names=["t","o","h","l","c","v"]) for f in files]
    df = pd.concat(dfs, ignore_index=True)
    t = pd.to_datetime(df["t"], format="%Y%m%d %H%M%S") + pd.Timedelta(hours=5)   # EST fixed -> UTC
    df.index = t.dt.tz_localize("UTC").dt.tz_convert("America/New_York")
    df = df[~df.index.duplicated()].sort_index()
    return df[["o","h","l","c"]]

def resample(m1, rule):
    b = m1.resample(rule, label="left", closed="left").agg({"o":"first","h":"max","l":"min","c":"last"}).dropna()
    return b

if __name__ == "__main__":
    m1 = load_1m(sys.argv[1]); out = sys.argv[2]
    m1.to_pickle(os.path.join(out, "m1.pkl"))
    for r in ["5min","15min","1h"]:
        resample(m1, r).to_pickle(os.path.join(out, f"b_{r}.pkl"))
    print(len(m1), m1.index[0], m1.index[-1])
