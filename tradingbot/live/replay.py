"""Replay the live assessment over recent history: what would the session have done?

Walks every closed execution-timeframe candle of the last ``--days`` days, calls exactly the
live ``signals.assess`` on the data available at that close (no look-ahead), and follows
each APPROVED setup with TJR's exits (`exits.simulate_partials`). Costs ignored [Bot].
It checks the live logic against the research, and how often trades come. Not a forecast.

    python -m tradingbot.live.replay --days 60 [--symbols SPY,GLD]
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ..config import BASELINE
from ..data import fetch_bars, timeframe_length
from ..exits import simulate_partials
from ..trend import _ts
from .signals import NY, assess


def _ny(t: str) -> datetime:
    return datetime.fromisoformat(t.replace("Z", "+00:00")).astimezone(NY)


def replay(symbol: str, days: int, config=BASELINE, ago: int = 0, shorting: bool = True) -> list[dict]:
    """The last ``days`` days, ending ``ago`` days before now (for out-of-sample checks)."""
    tp = config.trading
    now = datetime.now(timezone.utc) - timedelta(days=ago)
    ltf = fetch_bars(symbol, tp.execution_tf, now - timedelta(days=days + 25), now)
    htf = fetch_bars(symbol, tp.take_profit_tf, now - timedelta(days=days + 70), now)
    daily = fetch_bars(symbol, "1Day", now - timedelta(days=days + 220), now)
    ltf_len, tp_len = timeframe_length(tp.execution_tf), timeframe_length(tp.take_profit_tf)
    first = now - timedelta(days=days)
    out = []
    for i, c in enumerate(ltf):
        if not c.closed or _ts(c.t) < first:
            continue
        lo = max(0, i - 600)  # about 20 days of 15-minute candles, as the live session loads
        t_close = _ts(c.t) + ltf_len
        h = [x for x in htf if _ts(x.t) < t_close]
        dly = [x for x in daily if _ts(x.t) < t_close]
        a = assess(symbol, ltf[lo:i + 1], h, dly, config, shorting, ltf_len, tp_len)
        if a is None:
            continue
        rec = {"t": a["t"], "decision": a["decision"], "reasons": a["reasons"], "plan": a["plan"],
               "bias_relation": a["context"]["bias_relation"]}
        if a["decision"] == "APPROVED":
            p = a["plan"]
            # As live: flat before the close (``flatten_at``), so hold only the same day's candles.
            day = _ny(c.t).date()
            fh, fm = map(int, tp.flatten_at.split(":"))
            left = 0
            for x in ltf[i + 1:]:
                closes = _ny(x.t) + ltf_len
                if _ny(x.t).date() != day or (closes.hour, closes.minute) > (fh, fm):
                    break
                left += 1
            if left == 0:
                rec["result"] = {"r": 0.0, "exit": "no_time"}
            else:
                res = simulate_partials(ltf[:i + 1 + left], i, 1 if p["direction"] == "long" else -1, p["entry"], p["stop"],
                                        p["take_profits"], left)
                rec["result"] = res
            out.append(rec)
            continue
        out.append(rec)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=60)
    ap.add_argument("--symbols", default="")
    ap.add_argument("--bias-filter", action="store_true", help="only trade with the daily bias (TJR's baseline rule)")
    ap.add_argument("--ago", type=int, default=0, help="end the replay this many days ago (out-of-sample checks)")
    ap.add_argument("--long-only", action="store_true",
                    help="no short setups (replays before 2026-10-21 were long-only: the old account couldn't short)")
    ap.add_argument("--set", action="append", default=[], metavar="SECTION.FIELD=VALUE",
                    help="change one setting, e.g. trading.execution_tf=1Hour (repeatable)")
    args = ap.parse_args()
    from ..config import with_change
    config = with_change(BASELINE, "trading", "daily_bias_filter", True) if args.bias_filter else BASELINE
    for item in args.set:
        key, value = item.split("=", 1)
        section, field = key.split(".")
        current = getattr(getattr(config, section), field)
        value = type(current)(value) if current is not None and not isinstance(current, bool) else value == "True" if isinstance(current, bool) else value
        config = with_change(config, section, field, value)
    print("config:", config.version)
    root = Path(__file__).resolve().parent.parent.parent / "journal" / "trading"
    syms = args.symbols.split(",") if args.symbols else [r["symbol"] for r in json.loads(sorted(root.glob("watchlist_*.json"))[-1].read_text())["watch"]]
    allres, summary = {}, {}
    for s in syms:
        recs = replay(s, args.days, config, args.ago, shorting=not args.long_only)
        allres[s] = recs
        appr = [r for r in recs if r["decision"] == "APPROVED" and r.get("result") and r["result"]["exit"] != "no_time"]
        rs = [r["result"]["r"] for r in appr]
        reasons = Counter(x for r in recs if r["decision"] == "REJECTED" for x in r["reasons"])
        summary[s] = {"setups": len(recs), "approved": len(appr), "avg_r": round(sum(rs) / len(rs), 3) if rs else None,
                      "total_r": round(sum(rs), 2), "win": round(sum(x > 0 for x in rs) / len(rs), 2) if rs else None,
                      "top_rejections": reasons.most_common(3)}
        print(s, summary[s])
    rs = [r["result"]["r"] for recs in allres.values() for r in recs
          if r["decision"] == "APPROVED" and r.get("result") and r["result"]["exit"] != "no_time"]
    print(f"\nall: {len(rs)} approved trades in {args.days} days, avg R {sum(rs) / len(rs):+.3f}, total {sum(rs):+.1f}R" if rs else "no approved trades")
    for rel in ("with", "against", "none"):
        x = [r["result"]["r"] for recs in allres.values() for r in recs if r["decision"] == "APPROVED" and r.get("result")
             and r["result"]["exit"] != "no_time" and r["bias_relation"] == rel]
        if x:
            print(f"  {rel} the daily bias: {len(x)} trades, avg R {sum(x) / len(x):+.3f}, win {sum(v > 0 for v in x) / len(x):.0%}")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    (root.parent / "studies" / f"live_replay_{args.days}d_ago{args.ago}{'_biasfilter' if args.bias_filter else ''}{''.join('_' + x.replace('=', '-') for x in args.set)}_{stamp}.json").write_text(json.dumps({"summary": summary, "setups": allres}, indent=1))


if __name__ == "__main__":
    main()
