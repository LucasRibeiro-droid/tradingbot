"""Day 3 — Discipline: doing what the plan says, every time, and showing up every day.

Source: TJR Boot Camp Day 3 (https://www.youtube.com/watch?v=w2CWF0WtLmQ).
Full write-up: knowledge/day03_discipline.md.

TJR (03:25): his students trade the same strategy he does; the difference is that
they skip trades they aren't confident in and bail out of trades early. A bot has
no confidence or motivation to lose, but it can still deviate from its plan through
bugs, overrides or ad-hoc rules. ``audit`` catches those deviations, and
``write_daily_entry`` is the bot's daily habit.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable, Sequence

DAILY_DIR = Path(__file__).resolve().parent.parent / "journal" / "daily"

# Day 3, 09:31: a habit forms in about 21 days; it becomes routine at about 60.
HABIT_DAYS = 21
ROUTINE_DAYS = 60

# Exits the plan allows. Anything else is "bailing out" (03:25).
PLAN_EXITS = frozenset({"stop", "target", "plan_rule", "end_of_session"})


@dataclass(frozen=True)
class Decision:
    """One moment where the plan had something to say, and what the bot actually did."""

    t: str
    setup_valid: bool
    took_trade: bool
    exit_reason: str | None = None
    risk_pct: float | None = None
    plan_risk_pct: float | None = None


@dataclass(frozen=True)
class Violation:
    t: str
    rule: str
    detail: str


def audit(decisions: Iterable[Decision]) -> list[Violation]:
    """Every place the bot did something other than what its plan said."""
    out = []
    for d in decisions:
        if d.setup_valid and not d.took_trade:
            # 03:25: "sometimes you aren't confident enough to take those trades".
            out.append(Violation(d.t, "skipped_valid_setup", "plan said trade, bot did not"))
        if d.took_trade and not d.setup_valid:
            # 24:38: "you can't treat this like a casino ... over trading".
            out.append(Violation(d.t, "trade_without_setup", "traded without a valid setup"))
        if d.took_trade and d.exit_reason is not None and d.exit_reason not in PLAN_EXITS:
            # 03:25: "sometimes you guys are bailing out of trades".
            out.append(Violation(d.t, "exit_off_plan", f"exited for {d.exit_reason!r}"))
        if (d.took_trade and d.risk_pct is not None and d.plan_risk_pct is not None
                and d.risk_pct > d.plan_risk_pct):
            # 24:38: "over leveraging ... professional traders trade with risk management".
            out.append(Violation(d.t, "oversized_risk", f"risked {d.risk_pct}% vs plan {d.plan_risk_pct}%"))
    return out


def adherence(decisions: Sequence[Decision]) -> float:
    """Share of decisions with no violation. 1.0 means the plan was followed exactly."""
    if not decisions:
        return 1.0
    bad = {v.t for v in audit(decisions)}
    return 1 - sum(d.t in bad for d in decisions) / len(decisions)


def streak(days: Iterable[date], today: date) -> int:
    """Consecutive days, ending today or yesterday, that have a journal entry."""
    have = set(days)
    day = today if today in have else today - timedelta(days=1)
    n = 0
    while day in have:
        n += 1
        day -= timedelta(days=1)
    return n


def journal_days(directory: Path = DAILY_DIR) -> list[date]:
    days = []
    for p in directory.glob("*.md"):
        try:
            days.append(date.fromisoformat(p.stem))
        except ValueError:
            continue
    return days


def write_daily_entry(today: date, did: Sequence[str], learned: Sequence[str],
                      next_step: str, violations: Sequence[Violation] = (),
                      directory: Path = DAILY_DIR) -> Path:
    """The bot's daily video diary (31:36): what it did, what it learned, what's next.

    ``next_step`` is required: there is always something to improve (14:27, 26:14).
    """
    if not next_step.strip():
        raise ValueError("every day needs a next improvement step")
    directory.mkdir(parents=True, exist_ok=True)
    n = streak(journal_days(directory) + [today], today)
    milestone = ""
    if n >= ROUTINE_DAYS:
        milestone = f" (routine: {ROUTINE_DAYS}+ days)"
    elif n >= HABIT_DAYS:
        milestone = f" (habit: {HABIT_DAYS}+ days)"
    lines = [f"# {today.isoformat()}", "", f"Streak: {n} day{'s' if n != 1 else ''}{milestone}", "",
             "## Did", *[f"- {x}" for x in did], "", "## Learned", *[f"- {x}" for x in learned], "",
             "## Plan violations", *([f"- {v.t}: {v.rule} ({v.detail})" for v in violations] or ["- none"]),
             "", "## Next improvement", f"- {next_step}", ""]
    path = directory / f"{today.isoformat()}.md"
    path.write_text("\n".join(lines))
    return path
