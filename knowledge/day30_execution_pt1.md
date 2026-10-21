# Day 30 — Execution, Part 1: putting the pieces together

Source: TJR Boot Camp, Day 30: Execution (https://www.youtube.com/watch/ESsy0uoFAz4, 9:15).
Studied from the owner's captions (`sources/day30_execution_pt1.md`). No charts ("we're not
getting into charts today", 00:26); TJR reads from a text list on screen, and the captions
carry all of it. Topic file: `execution.md`.

**Classification:** part 1 of 3 of "putting the pieces together" (Days 30, 32, 33). This is
**methodology**: the first time TJR lists the complete set of entry models. The topic stays
**open** until Day 33; Day 32 shows each model on charts (07:37–08:05).

## What it teaches

### 1. The five building blocks (01:05–01:15)
Liquidity sweep, break of structure, order block, fair value gap, equilibrium.

### 2. What each tells us about the market (01:21–02:46)
| Block | What it tells us |
|---|---|
| **Liquidity sweep** | "The potential for orders to get filled": a high or low taken out. "We don't know whether it's confirmed yet." |
| **Break of structure** | "Confirmation that orders were filled and we see a market structure shift." A sweep then a break the other way: "smart money orders got filled and we're going to go in the opposite direction." |
| **Order block** | "The price range where orders were filled": the move that caused the sweep. |
| **Fair value gap** | "The price range with a lack of liquidity": usually the big imbalance candle with no counteracting orders. |
| **Equilibrium** | "Finding that discounted price between highs and lows." |

### 3. The four entry models (03:12–06:45)
1. **Sweep + break of structure → enter** (03:15–03:53). The orders' potential, then their confirmation. "That's going to be the top of the move."
2. **Sweep + break, poor reward-to-risk → wait for the order block** (03:54–04:39). "We wait, we're patient, because we didn't get the risk reward that we wanted ... we wait for the price range where orders were filled ... to get an optimal entry. **We enter at the order block, stops above the highs.**"
3. **Sweep + break + a fair value gap filled** (04:42–05:31). Not necessarily right away: "you missed the order block entry, price trends lower, and then you see a fair value gap that you enter off of." Entry on "a reaction off of it, **or just for it to get hit**."
4. **Sweep + break + a gap or order block filled + equilibrium** (05:34–06:45). "Ultimate confluence ... a foolproof plan to enter if you are a beginner": the gap or block must be within a discount.

**Risk ladder (05:50–06:08):** "The higher up you get on this list, the more risky you get ... these two [models 2 and 3] are kind of equal; this is the most safe, this is the most risky." So model 1 is the most risky, models 2 and 3 are in between and about equal, and model 4 is the safest. The captions garble the end of the sentence ("one most safe even most risky three most risky"); the first sentence is clear [Inferred].

### 4. Homework (06:51–07:30)
- Write it all down. Choose which models you'll use; they're part of the execution plan. Understand *why* the market moves; not "it's bouncing off the floor" or "the EMAs that cross".

### 5. Where strategy sits (08:13–08:34)
- "Strategy isn't the biggest part of trading ... the bigger issue is when you know how to execute but you can't control your emotions and you can't be robotic with it. But the first step is understanding how to execute."

## Connections
- **Days 6–28:** the definitions are condensed from every building-block lesson. Nothing new is defined; this is the order they're combined in.
- **Days 12, 14, 18, 20, 26:** model 1 = "the start of the move" / "first primary entry" (Days 20, 26). Model 2 = the patient entry (Days 18, 22). Model 4 = "the perfect tools to combine" (Day 26).
- **Day 3, Day 7:** robotic execution; choose the pieces you understand.

## Contradictions and issues
1. **Touch vs confirmation at the zone.** Here model 2 is "enter at the order block" and model 3 allows "just for it to get hit". Days 16, 22 and 24 waited for a reaction or a lower-timeframe break first. Day 26 also said "even just hitting the order block, enter off that." So TJR allows both: a confirmation entry is not required for models 2 and 3. Which to use may be what Day 32's examples show. The bot's earlier tests:
   - H23: a bare entry at the order block had a better reward-to-risk but a worse average result on 5 of 6 charts.
   - H24: the confirmation entry was inconclusive.
2. **Stop placement in model 2: "stops above the highs".** That's the sweep's extreme (above the order block). This agrees with Day 22's "above the order block itself to play safe" [Inferred: "the highs" = the swept high].
3. **The risk ladder is TJR's judgement, not measured.** It's testable: model 4 should win more often than model 1 (H29).
4. **Model 1 entry point.** "Enter" after the break: at the break's close? Not stated; Day 32's examples may show it.

## Provenance audit
- **[TJR]**
  - The five building blocks and what each says.
  - The four entry models.
  - Model 2: enter at the order block, stop above the highs.
  - Model 3: a reaction or just the hit.
  - Model 4 is for beginners.
  - The risk ladder (model 1 riskiest, model 4 safest).
  - Choose your models and write them down.
- **[Inferred]**
  - The ladder's middle (from a garbled sentence).
  - "The highs" = the swept high.
- Nothing executable is changed until Days 32 and 33.
