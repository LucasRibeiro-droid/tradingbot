"""Draw what the bot sees on a chart: highs, lows, breaks of structure and fakes.

Used to check by eye that the bot reads structure the way TJR teaches it (Day 6 homework:
10 real breaks and 10 fakes). Needs matplotlib.

Usage:
    python -m tradingbot.chart GLD --timeframe 1Day --bars 120
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .config import BASELINE
from .liquidity import find_pools, pools_and_takes
from .trend import DOWN, UP, swings, trend_series

CHART_DIR = Path(__file__).resolve().parent.parent / "journal" / "charts"
SURFACE, INK, MUTED = "#fcfcfb", "#0b0b0b", "#52514e"
UP_CANDLE, DOWN_CANDLE = "#2a78d6", "#52514e"  # TJR's chart: up candles blue, down dark
BOS, SWEEP, POOL = "#eb6834", "#6250d6", "#1baf7a"


def draw(candles, title: str, path: Path, config=BASELINE) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    states = trend_series(candles, config.trend)
    found = swings(candles, config.trend)
    fig, ax = plt.subplots(figsize=(16, 7), dpi=110)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    for i, c in enumerate(candles):
        color = UP_CANDLE if c.c >= c.o else DOWN_CANDLE
        ax.vlines(i, c.l, c.h, color=color, linewidth=1)
        ax.add_patch(plt.Rectangle((i - 0.32, min(c.o, c.c)), 0.64, max(abs(c.c - c.o), 1e-9),
                                   facecolor=color, edgecolor=color))

    span = max(c.h for c in candles) - min(c.l for c in candles)

    # Day 10: liquidity pools, from the clear high/low that forms them to the candle that
    # takes them; dashed to the right edge while still untaken.
    taken_at = {}
    for j, tk in enumerate(pools_and_takes(candles, config.liquidity)):
        for pool in tk.buy_side + tk.sell_side:
            taken_at[pool] = j
    for pool in find_pools(candles, config.liquidity):
        end = taken_at.get(pool)
        ax.hlines(pool.price, pool.index, end if end is not None else len(candles) - 0.5, color=POOL,
                  linewidth=1.2, linestyles="-" if end is not None else "--")
        if end is not None:
            ax.plot(end, pool.price, marker="o", markersize=5, markerfacecolor=SURFACE,
                    markeredgecolor=POOL, mew=1.5)

    for s in found:
        y = s.price + (0.012 * span if s.kind == "high" else -0.012 * span)
        ax.plot(s.index, y, marker="v" if s.kind == "high" else "^", color=MUTED, markersize=4)

    # Watched level: the most recent low in an uptrend, high in a downtrend (Day 6, 14:46).
    for i, s in enumerate(states):
        level = s.swing_low if s.direction == UP else s.swing_high if s.direction == DOWN else None
        if level is not None:
            ax.hlines(level, i - 0.5, i + 0.5, color=MUTED, linewidth=0.8, linestyles=":")

    for i, (c, s) in enumerate(zip(candles, states)):
        if s.event in ("bos_up", "bos_down"):
            up = s.event == "bos_up"
            y = c.h + 0.05 * span if up else c.l - 0.05 * span
            ax.annotate("BOS ▲" if up else "BOS ▼", (i, c.c), (i, y), ha="center", fontsize=8,
                        color=INK, arrowprops=dict(arrowstyle="-", color=BOS, lw=1.5))
            ax.plot(i, c.c, marker="o", color=BOS, markersize=6)
        elif s.event in ("sweep_low", "sweep_high"):
            low = s.event == "sweep_low"
            y = c.l - 0.035 * span if low else c.h + 0.035 * span
            ax.plot(i, c.l if low else c.h, marker="x", color=SWEEP, markersize=8, mew=2)
            ax.text(i, y, "fake", ha="center", fontsize=7, color=MUTED)

    step = max(1, len(candles) // 12)
    ax.set_xticks(range(0, len(candles), step))
    ax.set_xticklabels([candles[i].t[:10] for i in range(0, len(candles), step)], fontsize=8, color=MUTED)
    ax.tick_params(axis="y", labelsize=8, colors=MUTED)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#d6d5d0")
    ax.grid(axis="y", color="#ecebe7", linewidth=0.6)
    ax.set_xlim(-1, len(candles))
    ax.set_title(title, loc="left", fontsize=12, color=INK, pad=22)
    ax.text(0, 1.01, "▼▲ highs and lows (two-candle rule)   ● BOS: close beyond the watched level   "
            "✕ fake: wick beyond, no close   ⋯ watched level   — liquidity pool (dashed: still untaken), ○ taken",
            transform=ax.transAxes,
            fontsize=8, color=MUTED, va="bottom")
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)
    return path


def main() -> None:
    from .data import fetch_bars, timeframe_length

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("symbol")
    ap.add_argument("--timeframe", default="1Day")
    ap.add_argument("--bars", type=int, default=120)
    args = ap.parse_args()
    start = datetime.now(timezone.utc) - timeframe_length(args.timeframe) * args.bars * 2 - timedelta(days=10)
    candles = [c for c in fetch_bars(args.symbol, args.timeframe, start) if c.closed][-args.bars:]
    path = CHART_DIR / f"{args.symbol}_{args.timeframe}_structure.png"
    print(draw(candles, f"{args.symbol} {args.timeframe}: structure as the bot reads it ({BASELINE.version})", path))


if __name__ == "__main__":
    main()
