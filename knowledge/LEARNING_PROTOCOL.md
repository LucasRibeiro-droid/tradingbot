# Learning protocol for TJR's bootcamp

The owner's instructions for how every bootcamp lesson is processed (given 2026-10-20).
Followed for every new video, and applied retroactively to Days 2–12.

## Core principle

The 56 videos are one course, not 56 strategies. Each lesson is a module that teaches a
concept, a technique, or part of the methodology. The goal is to reconstruct the one
complete trading methodology they teach together, and to understand how the pieces relate.

## Three levels of knowledge

- **Concept:** a building block (market structure, liquidity, fair value gaps, ...).
- **Technique or condition:** how a concept is used (a confirmation, a filter, an entry trigger, a target, ...).
- **Methodology:** the decision process that combines them. Only call something a separate strategy if TJR explicitly presents it as one.

## For every new lesson

1. Identify the video and its learning objectives.
2. Summarize the knowledge taught (concepts, definitions, rules, examples).
3. Connect it to previous lessons: what it builds on, reinforces, clarifies or changes.
4. Classify it: new concept, expansion, part of a multi-part lesson, or clarification.
5. Update `methodology.md` (the knowledge base) and `course_map.md`.
6. Flag contradictions, ambiguities, missing prerequisites and open questions.
7. Explain its role in the overall methodology.
8. Save everything to the repo so it survives across sessions.

Report a focused summary of the new lesson, not the whole knowledge base.

## Rules

- **Provenance.** Every rule is tagged as **[TJR]** (explicitly taught, with timestamp), **[Inferred]** (reasonably concluded from several lessons), or **[Bot]** (a choice made to make it testable, not from TJR). Never attribute a [Bot] choice to TJR.
- **Multi-part lessons** are one learning unit. Keep their sequence; don't finalize a topic until its last part is in. List what's still missing.
- **Examples are not rules.** A chart example doesn't become a mandatory condition.
- **Later lessons don't silently replace earlier ones.** Record refinements and apparent contradictions with their context.
- **No premature executable rules.** If something can't yet be made an objective, testable condition, document the ambiguity instead of inventing one. Code built to test an idea is a test harness, not TJR's strategy.
- **Not proof of profit.** The methodology must be tested on history, out of sample, with costs and risk limits, before any live use.
