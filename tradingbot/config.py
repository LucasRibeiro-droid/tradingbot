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
    """Liquidity indicator (Days 8, 10, 12): where it sits and when it counts as just taken."""

    # Day 10: liquidity rests above clear highs and below clear lows that have held. A
    # pool is a high (low) higher (lower) than this many candles on each side, still
    # untouched since it formed. TJR's examples were prominent swings, not two-candle wiggles.
    pool_strength: int = 5
    # How many candles back (including the current one) a taken pool still counts as
    # "liquidity was just swept".
    sweep_lookback: int = 10


@dataclass(frozen=True)
class DecisionParams:
    """The one decision process that reads all indicators (decision.py)."""

    # Indicators that must agree before the bot acts on a break of structure. The learning
    # loop adds or removes one at a time (H12). "with_htf" is always applied as well,
    # because trading against the higher timeframe is locked off.
    confluences: tuple[str, ...] = ("liquidity_swept",)
    # Stop beyond the most extreme price of this many candles (up to the trigger).
    stop_lookback: int = 10
    # A position still open after this many candles is closed at the close.
    max_hold_bars: int = 50
    # Exits. "tjr" (default since v2, H19): Day 37's take-profit ladder, the first target the
    # next higher-timeframe draw on liquidity at least ``first_tp_min_r`` away, then building
    # blocks, ``take_profits`` in all, equal parts, stop to break even after the first.
    # "single": everything at the nearest liquidity (the bot's exit before Day 37).
    exits: str = "tjr"
    take_profits: int = 3
    first_tp_min_r: float = 1.0
    # Reversal-path stop. "sweep" (Day 38): beyond the liquidity sweep, the invalidation
    # point. "lookback": beyond the extreme of the last ``stop_lookback`` candles (before v2).
    # On SPY/GLD, 5-minute to 1-hour, the two gave identical trades (the sweep is the extreme).
    stop: str = "sweep"


@dataclass(frozen=True)
class StudyParams:
    """How the bot measures "how price reacted" to a candle (Day 2 homework)."""

    horizon_bars: int = 5
    min_examples: int = 10


@dataclass(frozen=True)
class TradingParams:
    """Live (paper) trading settings. The risk settings are the owner's, authorized 2026-10-21;
    the rest are [Bot] choices from the research (journal/trading/README.md)."""

    # Owner: risk 1% of equity per trade (entry to stop).
    risk_per_trade_pct: float = 1.0
    # Owner: no daily loss limit and no cap on trades; "take as many trades there are to take
    # as long as you follow a clear logic". None = no limit.
    max_daily_loss_pct: float | None = None
    max_trades_per_day: int | None = None
    # Owner, 2026-10-21 (later): "take as many trades as it wants as long as it follows a clear
    # logic baseline". No cap on instruments (TJR's Day 4 "one or two" stays in LOCKED as the
    # baseline reference). None = no limit; every trade comes from the watchlist screen.
    max_instruments_per_day: int | None = None
    # Owner, 2026-10-21: "the bot does not have to buy big positions". Each position's cost is
    # capped at this % of equity; the 1% risk stays the ceiling. Results are measured in R.
    max_position_pct: float = 10.0
    # Owner's directive, 2026-10-22: experiment to learn. Entry strategies traded live (each
    # trade tests a hypothesis, journal/hypotheses.md) and, per strategy, the exit methods
    # under test, split evenly across its trades (live/experiments.py). TJR's model 1 with
    # TJR's ladder stays in as the baseline.
    # Owner, 2026-10-23: "trade in every way" with TJR's core fundamentals on all candles: TJR's
    # entry models 1-3 (Days 30-33) on the 1-minute, 5-minute, 15-minute and 1-hour, each its
    # own playbook (tjr_m<model>_<timeframe>; tjr_m1_15m is the baseline, the old "tjr_m1").
    # Take profit 1 comes from the next timeframe up (Day 37).
    # Owner, 2026-10-25: "switch the live paper bot to CRT 1h to 5m. I only want you trading this
    # strategy for the whole week" (rules: live/crt_owner.py, backtest H56: -0.56R per trade after
    # costs at 3R with the stop fixed, the least negative target). "tjr" and "orb30" are off.
    strategies: tuple[str, ...] = ("crt",)
    crt_target_r: float = 3.0  # half at 1:1, half here; stop fixed at the gap's middle candle
    # H58 (2026-10-26, from the first live day and the H56 backtest): skip a gap whose stop is
    # closer than this % of the price. Below it, the spread and stop slippage cost most of 1R
    # (backtest: -0.56R -> -0.30R per trade, better in both periods). The stop rule is unchanged.
    crt_min_stop_pct: float = 0.15
    # CRT trades are held until their stop or target, overnight too (no flatten); the session
    # ends just after the last third candle's orders expire at 16:00.
    hold_overnight: bool = True
    session_end: str = "16:02"
    tjr_models: tuple[int, ...] = (1, 2, 3)
    tjr_timeframes: tuple[str, ...] = ("1Min", "5Min", "15Min", "1Hour")
    model_wait_candles: int = 20  # model 2's limit order and model 3's window, in candles
    exits_under_test: tuple[tuple[str, tuple[str, ...]], ...] = (
        ("tjr", ("tjr_ladder", "ladder_0.5_1_2R")),
        ("orb30", ("ladder_1_2_3R", "2R")),
    )
    # [Bot] Execution on the 15-minute: the entry models with TJR's exits were positive on
    # SPY and GLD 15-minute and 1-hour, not on the 5-minute for SPY (knowledge/exits.md).
    # Take profit 1 from the next timeframe up (Day 37).
    execution_tf: str = "15Min"
    take_profit_tf: str = "1Hour"
    # Entry model 1 (sweep + break, enter on the break's close; Day 30, Day 32): the best
    # per-setup results with TJR's exits on 3 of 4 intraday charts (knowledge/execution.md).
    entry_model: int = 1
    # New entries from the New York open [TJR Day 18] until this time (ET); flat before the
    # close [Bot: TJR doesn't hold trades for days, Day 36, 20:00].
    last_entry: str = "15:30"
    flatten_at: str = "15:55"
    # Day 38: room beyond the sweep for the spread. TJR used 0.5 points on the S&P (~0.01%).
    stop_buffer_pct: float = 0.02
    # Overrides of the TJR baseline, from evidence (rule_changes.md).
    # TJR (LOCKED.trade_against_htf_trend = False, Days 4, 34): only with the daily bias. The
    # research found setups against the bot's daily bias did better (H30 retest), so the
    # filter is off and every trade records its relation to the bias, to keep testing it.
    daily_bias_filter: bool = False
    # [Bot] Screening filters.
    min_price: float = 5.0
    min_dollar_volume: float = 50_000_000.0  # average daily, last 20 days
    min_range_pct: float = 1.0  # average daily high-low range, last 20 days, % of price
    shortlist: int = 25  # owner, 2026-10-22: a wider universe for more, more varied evidence
    movers: int = 10  # of which up to this many are the day's biggest movers (relative strength/weakness)


@dataclass(frozen=True)
class Locked:
    """TJR's absolutes: the baseline, as he states them in the lessons.

    Owner, 2026-10-21: TJR is the baseline, not instructions to follow; the bot learns from its
    trades and keeps whatever is most profitable. So these are the starting point and the
    reference, and live trading may override one (``TradingParams``) when the evidence says so,
    recorded in journal/trading/rule_changes.md."""

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
    version: str = "v2-tjr-exits"
    candle: CandleParams = CandleParams()
    trend: TrendParams = TrendParams()
    liquidity: LiquidityParams = LiquidityParams()
    decision: DecisionParams = DecisionParams()
    study: StudyParams = StudyParams()
    trading: TradingParams = TradingParams()
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
