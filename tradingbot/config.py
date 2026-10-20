"""Tunable parameters, versioned so every result can be traced to a baseline.

The learning loop may only change one field at a time (see knowledge/README.md).
Fields under ``LOCKED`` are rules taken directly from the lessons and are never
tuned by the bot.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace


@dataclass(frozen=True)
class CandleParams:
    """Thresholds for reading a single candle (Day 2). Fractions are of the candle's range."""

    # Doji: "small body" (Day 2, 11:00).
    doji_max_body_pct: float = 0.10
    # A wick counts as "long" / "short" relative to the whole range.
    long_wick_min_pct: float = 0.60
    short_wick_max_pct: float = 0.10
    # Long-legged doji: both wicks long.
    long_legged_min_wick_pct: float = 0.30
    # Hammer family: small body with a wick at least this many bodies long.
    hammer_max_body_pct: float = 0.35
    hammer_wick_to_body: float = 2.0
    # Strong close: "full" body, almost no wick on the closing side (Day 2, 15:00 and 17:30).
    strong_close_min_body_pct: float = 0.70
    strong_close_max_close_wick_pct: float = 0.10
    # Weakness: a directional candle whose wick on the closing side is at least this
    # many bodies long ("strong bulls but not strong enough to close", Day 2, 10:00).
    weakness_wick_to_body: float = 1.0
    # Rejection: a wick of at least this fraction of the range, with the close in the
    # opposite third of the candle ("wicks don't lie", Day 2, 16:00-18:00).
    rejection_min_wick_pct: float = 0.50
    # Candles smaller than this multiple of the recent average range say too little to read.
    min_range_vs_avg: float = 0.5
    avg_range_lookback: int = 20
    # Bars used to decide whether a candle follows a rise or a decline (hammer vs hanging man).
    context_lookback: int = 5


@dataclass(frozen=True)
class TrendParams:
    """How the bot finds swings and trends (Days 4 and 6)."""

    # "two_candle": Day 6's definition (up candle then down candle is a high, and the
    # reverse is a low). "pivot": the bot's first Day 4 attempt, kept for comparison.
    swing_method: str = "two_candle"
    # Pivot method only: bars on each side a swing high (low) must be higher (lower) than.
    swing_strength: int = 2
    # "wick": swings from highs and lows. "close": swings from closes, like a line chart (18:32).
    swing_source: str = "wick"
    # Consolidation (12:32): over this many bars, price went nowhere relative to its range.
    consolidation_lookback: int = 20
    consolidation_max_efficiency: float = 0.30


@dataclass(frozen=True)
class LiquidityParams:
    """Days 8, 10 and 12: where liquidity sits, liquidity taken before a break the other way, and
    liquidity on the other side as the target."""

    # Day 10: liquidity rests above clear highs and below clear lows that have held. A
    # pool is a high (low) higher (lower) than this many candles on each side, still
    # untouched since it formed. TJR's examples were prominent swings, not two-candle wiggles.
    pool_strength: int = 5
    # How many candles back (including the break itself) a pool must have been taken
    # for a break of structure to count as the confirmation TJR waits for.
    sweep_lookback: int = 10
    # A liquidity trade still open after this many candles is closed at the close.
    max_hold_bars: int = 50


@dataclass(frozen=True)
class StudyParams:
    """How the bot measures "how price reacted" to a candle (Day 2 homework)."""

    horizon_bars: int = 5
    min_examples: int = 10


@dataclass(frozen=True)
class Locked:
    """Rules stated directly in the lessons. Not tunable."""

    # Day 2, 16:50: "We can only make bias and decision on candles that have formed."
    closed_candles_only: bool = True
    # Day 2, 13:05 and 14:30: candle patterns are one confluence, never a trade on their own.
    candle_read_is_entry_signal: bool = False
    # Day 2, 07:30: no patterns of three or more candles ("mountain tops", W's, head and shoulders).
    max_pattern_candles: int = 2
    # Day 3, 03:25 and 24:38: take every valid setup, take nothing else, exit only where the
    # plan says, never risk more than the plan. Checked by discipline.audit.
    follow_plan_exactly: bool = True
    # Day 3, 14:27 and 26:14: never satisfied; every day ends with a next improvement step.
    always_improving: bool = True
    # Day 4, 08:13-10:22: higher timeframes hold higher power; never trade against them.
    trade_against_htf_trend: bool = False
    # Day 4, 27:04: focus on one or two instruments.
    max_instruments: int = 2
    # Day 6, 12:44: "it is not a break of structure unless the candle closes above a high
    # or below a low". Wicks never break structure.
    bos_requires_close: bool = True
    # Day 8, 08:38: reaching liquidity is not an entry. Wait for the shift in structure;
    # "if we don't see a shift in direction ... hands off."
    liquidity_alone_is_entry: bool = False


@dataclass(frozen=True)
class Config:
    version: str = "v0-day12"
    candle: CandleParams = CandleParams()
    trend: TrendParams = TrendParams()
    liquidity: LiquidityParams = LiquidityParams()
    study: StudyParams = StudyParams()
    # The one or two instruments the bot studies and trades (LOCKED.max_instruments).
    # SPY stands in for TJR's S&P 500 and GLD for gold, the two markets he uses most.
    watchlist: tuple[str, ...] = ("SPY", "GLD")


LOCKED = Locked()
BASELINE = Config()


def with_change(config: Config, section: str, field: str, value) -> Config:
    """Return a new config differing from ``config`` in exactly one field."""
    current = getattr(config, section)
    if not hasattr(current, field):
        raise AttributeError(f"{section} has no field {field!r}")
    changed = replace(current, **{field: value})
    return replace(config, **{section: changed}, version=f"{config.version}+{section}.{field}={value}")


def to_dict(config: Config) -> dict:
    return asdict(config)
