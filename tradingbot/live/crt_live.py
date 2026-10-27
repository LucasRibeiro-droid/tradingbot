"""Live CRT 1-hour -> 5-minute (owner, 2026-10-25): the rules of ``crt_owner`` (backtested in
H55/H56), applied at each 5-minute close.

When the last two complete 1-hour candles (from 09:30 ET) form a CRT setup, the hour in
progress is the third candle: every fair value gap whose three 5-minute candles are inside it
gets a limit order at its near edge when it is confirmed, stop at the gap's middle candle (fixed
for the whole trade), half at 1:1 and half at ``target_r``. Unfilled orders expire when the third
candle ends; filled trades are held until the stop or the target, overnight too.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Sequence

from ..candles import BEARISH, BULLISH, Candle
from ..equilibrium import ranges
from ..fvg import find_gaps
from ..trend import trend_series
from .crt_backtest import hourly
from .crt_owner import trading_day, valid_setup
from .signals import NY


def _ny(t: str) -> datetime:
    return datetime.fromisoformat(t.replace("Z", "+00:00")).astimezone(NY)


def regular_hours(bars: Sequence[Candle]) -> list[Candle]:
    return [c for c in bars if c.closed and (9, 30) <= (_ny(c.t).hour, _ny(c.t).minute) < (16, 0)]


def _bucket_end(t: str, round_the_clock: bool = False) -> datetime:
    """When the 1-hour candle (from 09:30 ET) containing ``t`` ends (16:00 for the last one);
    24-hour markets: the end of the clock hour."""
    if round_the_clock:
        u = datetime.fromisoformat(t.replace("Z", "+00:00"))
        return u.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    n = _ny(t)
    start = n.replace(hour=9, minute=30, second=0, microsecond=0) + timedelta(hours=(n.hour * 60 + n.minute - 570) // 60)
    return min(start + timedelta(hours=1), n.replace(hour=16, minute=0, second=0, microsecond=0)).astimezone(timezone.utc)


def crt_assess(symbol: str, bars5: Sequence[Candle], shorting_enabled: bool, target_r: float = 3.0,
               min_stop_pct: float = 0.0, round_the_clock: bool = False, min_stop: float = 0.0,
               strategy: str = "crt_1h5m") -> list[dict]:
    """Assessments for the gaps confirmed by the last closed 5-minute bar inside a third candle.
    ``round_the_clock``: gold / index CFDs (clock hours, 18:00 ET day); ``min_stop``: the stop
    must be at least this far in price (24-hour markets: a multiple of the spread)."""
    bars = [c for c in bars5 if c.closed] if round_the_clock else regular_hours(bars5)
    if len(bars) < 200:
        return []
    H, first = hourly(bars, round_the_clock, 1)
    if len(H) < 4:
        return []
    last = len(bars) - 1
    if _bucket_end(bars[last].t, round_the_clock) != _bucket_end(H[-1].t, round_the_clock):
        return []
    states = trend_series(H)
    rng = ranges(H, states)
    i = len(H) - 2  # the sweep candle; H[-1] is the third candle (in progress)
    d = valid_setup(H, states, rng, i)
    if not d:
        return []
    r, s = H[i - 1], H[i]
    t0 = first[-1]
    side = BULLISH if d == 1 else BEARISH
    days = {}
    for c in bars:
        day = trading_day(c.t, round_the_clock)
        h, l = days.get(day, (c.h, c.l))
        days[day] = (max(h, c.h), min(l, c.l))
    prior = [day for day in sorted(days) if day < trading_day(H[-1].t, round_the_clock)]
    ph, pl = days[prior[-1]] if prior else (None, None)
    expires = _bucket_end(H[-1].t, round_the_clock)
    if datetime.fromisoformat(bars[last].t.replace("Z", "+00:00")) + timedelta(minutes=5) >= expires:
        return []  # the third candle's last bar: an order now would expire at once (as the backtest)
    out = []
    for g in find_gaps(bars):
        if g.side != side or g.confirmed_at != last or g.index - 1 < t0:
            continue
        digits = 2 if not round_the_clock else 5
        entry = round(g.top if d == 1 else g.bottom, digits)
        mid = bars[g.index]
        stop = round(mid.l if d == 1 else mid.h, digits)
        risk = (entry - stop) * d
        reasons = []
        if risk <= 0:
            reasons.append("stop is not beyond the entry")
        elif risk / entry * 100 < min_stop_pct:
            reasons.append(f"stop {risk / entry * 100:.3f}% from entry, under the {min_stop_pct}% minimum (H58: costs eat stops this tight)")
        elif risk < min_stop:
            reasons.append(f"stop {risk:g} from entry, under the minimum {min_stop:g} (3 spreads; costs eat stops this tight)")
        tp1, tp2 = round(entry + d * risk, digits), round(entry + d * risk * target_r, digits)
        if any(lv is not None and min(entry, tp1) < lv < max(entry, tp1) for lv in (ph, pl)):
            reasons.append("the previous day's high or low lies between entry and 1:1 (video)")
        if d == -1 and not shorting_enabled:
            reasons.append("short setup, but shorting is disabled on the account")
        out.append({
            "symbol": symbol, "t": bars[last].t, "price": bars[last].c, "strategy": strategy, "timeframe": "5Min",
            "context": {"ltf": "5Min", "range_candle": r.t, "sweep_candle": s.t, "crh": r.h, "crl": r.l,
                        "bias_relation": "n/a"},
            "setup": f"CRT 1h -> 5m {'long' if d == 1 else 'short'}: range candle {r.t} ({r.l}-{r.h}) swept by {s.t} "
                     f"and closed back inside; 5-minute fair value gap {g.bottom:.2f}-{g.top:.2f} in the third candle",
            "present": [{"concept": "trend", "evidence": "1-hour break of structure, not consolidating"},
                        {"concept": "discount" if d == 1 else "premium", "evidence": "range candle beyond the impulse's 50%"},
                        {"concept": "sweep", "evidence": f"{s.t} {'low' if d == 1 else 'high'} {s.l if d == 1 else s.h}, close {s.c} back inside"},
                        {"concept": "fair value gap", "evidence": f"{g.bottom:.2f}-{g.top:.2f}, middle candle {mid.t}"}],
            "missing": [], "conflicts": [],
            "plan": {"direction": "long" if d == 1 else "short", "entry": entry, "entry_type": "limit",
                     "entry_condition": f"limit at the gap's near edge {entry}, cancelled at {expires.astimezone(NY):%H:%M} ET if not filled",
                     "expires_at": expires.isoformat(timespec="seconds"),
                     "stop": stop, "invalidation": f"the gap's middle candle {'low' if d == 1 else 'high'} {stop} (fixed for the whole trade)",
                     "take_profits": [tp1, tp2], "fixed_stop": True,
                     "rr_first": 1.0, "rr_last": target_r},
            "decision": "REJECTED" if reasons else "APPROVED", "reasons": reasons,
        })
    return out
