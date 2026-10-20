# Day 3 — Discipline

Source: TJR Boot Camp, Day 3: Discipline (https://www.youtube.com/watch?v=w2CWF0WtLmQ, 33:39).
Studied from the full video plus the captions. The whole video is TJR talking over a static
S&P 500 chart, so the captions carry the entire lesson.
Code: `tradingbot/discipline.py`. Locked rules: `follow_plan_exactly`, `always_improving` in `tradingbot/config.py`.

The course alternates between trading days and discipline days (01:09). This is the first
discipline day.

## What the lesson teaches, and what it becomes for a bot

A bot has no motivation to lose and no fear to overcome, so most of this lesson is about
humans. Four ideas do carry over directly.

### 1. Same strategy, different results: the gap is execution (03:25–03:54)
- TJR's students trade the same strategy he does, often the same trades. They still lose because they skip trades they aren't confident in and bail out of trades early.
- "The trading part is relatively easy." What separates profitable traders is doing what the plan says, every time.
- **Bot rule (locked):** `LOCKED.follow_plan_exactly`. `discipline.audit` checks every decision for:
  - `skipped_valid_setup`: the plan said trade and the bot didn't
  - `trade_without_setup`: the bot traded when the plan didn't say to
  - `exit_off_plan`: the bot exited anywhere other than its stop, target or a plan rule
  - `oversized_risk`: the bot risked more than the plan allows
- `discipline.adherence` scores the share of decisions that followed the plan exactly. When the bot starts trading, any score below 100% means a bug or a rule gap, not a strategy result.
- This also protects the learning loop: a result only says something about the strategy if the strategy was actually followed.

### 2. Copy what the person you want to become does now (24:00–25:38)
- "Imagine your dream self. What do they do every single day? Copy that."
- For trading: "How do professional traders trade? With risk management, with no emotion, with discipline." Not over-trading, not over-leveraging, not treating it like a casino.
- **Bot rule:** covered by `trade_without_setup` and `oversized_risk` above. The actual risk numbers come from Day 13 (Risk Management) and Day 29 (Trading Plan).

### 3. Never satisfied: always be improving, 1% a day (14:27–15:33, 26:14)
- "Always be seeking improvement. There is always something you can improve upon."
- Doing the same thing every day keeps you where you are; to get a different result something has to change.
- **Bot rule (locked):** `LOCKED.always_improving`. Every daily journal entry must name a next improvement step; `write_daily_entry` refuses an empty one. This is the same loop as the hypotheses in `journal/hypotheses.md`: one change at a time, kept only if it beats the baseline.

### 4. Daily habit, documented (07:05–11:37, 22:43, 31:36–33:15)
- Pick one habit that's uncomfortable and do it every day. Habits form in about 21 days and become routine at about 60 (09:31).
- Motivation fades after about a week; discipline is what's left (11:04, 27:07).
- Take progress pictures every week, and document the journey daily, like a video diary, which also creates accountability.
- **Bot rule:** `write_daily_entry` writes `journal/daily/YYYY-MM-DD.md` with what the bot did, what it learned, any plan violations, and the next improvement. It tracks the streak and marks the 21-day (habit) and 60-day (routine) milestones.

## What does not carry over

Overcoming fear of judgment, confidence, fitness and reading goals are human habits. The
bot has nothing to translate them into. The one part of the homework that applies to *you*:
TJR asks every student to start one uncomfortable, beneficial habit today.

## Provenance audit (2026-10-20)

- **[TJR]** Students lose on the same strategy by skipping trades and bailing early (03:25); trade with risk management, no over-trading or over-leveraging (24:38); one uncomfortable habit daily; 21/60 days; always improving; document the journey.
- **[Inferred]** Turning "don't skip, don't bail" into an audit of four violations (skipped setup, trade without setup, exit off plan, oversized risk).
- **[Bot]** The daily journal format and streak counter.
