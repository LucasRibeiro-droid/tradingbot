# No-Wick Entry Model — strategy spec (draft for your confirmation)

Built **only** from the frame-by-frame logs in `strategy_course/logs/` (parts 1–6) and the captions you supplied.
Every rule cites the video timestamp (absolute time in the full video, `MM:SS`) and, where useful, the log frame (e.g. `p1_f106`).
His terminology is used throughout: **no-wick candle**, **internal / external trend**, **BOS**, **two-step BOS**, **pre-entry**,
**retest area**, **leg**, **decision area**, **imbalance**, **breathing room**, **stop loss priority**.

> **All 6 parts are now logged.** Part 6 confirmed the trade management, "trades to avoid" and account-rotation rules
> against the frames. No trading rules appear after 38:42; the rest is homework, the mentorship pitch and the outro.

> **Decision areas are excluded from the baseline**, as you instructed. He tells viewers to learn them from a separate video
> (21:14–21:43, `p4_f012`). The range/decision-area rules he gives in this video are listed in §9 as a **deferred layer**, not
> as part of the baseline.

---

## 1. Market and timeframe

| Rule | Source |
|---|---|
| He trades **forex**. The pairs are on his watchlist: **AUDUSD, AUDJPY, GBPUSD, USDJPY, USDCHF, AUDCHF** (DXY is also on the list). | 16:12–16:30, `p3_f022` |
| He says he has *heard* it works on NQ and some futures, but he trades forex. | 16:16–16:30 |
| **Don't trade gold** ("gold stopped working" after 2024). | 16:38 |
| **The trading timeframe is 15 minutes** ("the 15 minute is where you look for trades"). | 14:56–15:10, `p3_f011`; also 12:25 |
| **Higher-timeframe priority:** if the same no-wick play also exists on the 30m, prioritise the 30m. If it also exists on the 1h, prioritise the 1h. The ladder is 15 → 30 → 1h and goes no higher ("basically up until the 1 hour"). He only focuses on the no-wick candle that has **closed** on that timeframe. | 15:10–16:10, `p3_f012`, `p3_f016`–`f020` |
| **The external trend timeframe is 4 hours** (internal = the 15m he trades on). | 12:25–12:37, `p2_f118` |

## 2. No-wick candle (the setup candle)

| Rule | Source |
|---|---|
| A **bullish no-wick candle** is a bullish candle that closed with **no bottom wick** (flat bottom: open = low). | 02:36–02:53, `p1_f065`–`f073` |
| A **bearish no-wick candle** is a bearish candle that closed with **no top wick** (flat top: open = high). | same |
| He marks them with the **"xGhozt Wickless Candles"** indicator (▲ below bullish, ▼ above bearish; colours set to yellow, tables off). | 02:19–02:36, `p1_f061`–`f065` |
| The candle must have **closed** before it counts. | 04:23 ("once it closes"), 16:02 |
| Why it works: the flat side leaves an "imbalance" that acts as a magnet, so price comes back to it before continuing. | 03:00–04:01, `p1_f077`–`f090` |

## 3. Trend: internal, external, BOS, alignment

| Rule | Source |
|---|---|
| **Uptrend:** higher highs and higher lows. **Downtrend:** lower lows and lower highs. | 07:01–07:51, `p2_f002`–`f009` |
| **BOS (break of structure):** in an uptrend, price closes below the last higher low. In a downtrend, price closes above the last lower high. Breaking the latest high or low in the trend direction is also a BOS ("broken again, BOS to the upside"). | 07:51–08:57, `p2_f013`–`f024` |
| **Swing points and breaks use candle BODIES (closes), not wicks.** "It's always the closure… always the bodies." | 09:01–09:37, `p2_f035`–`f037` |
| **The internal trend is the "lowest possible trend": every single small pivot counts.** The internal trend is the direction of the **most recent BOS**. | 10:27–11:14, `p2_f065`–`f072` |
| For beginners: the "Higher High Lower Low – Live" indicator (LonesomeTheBlue) with the **ZigZag period as low as possible (he sets 2)**. He prefers reading it by eye. | 11:14–11:47, `p2_f077`–`f091` |
| **External trend = the same reading done on the 4h chart.** | 12:25–12:37 |
| **Alignment rule.** When the internal and external trends agree, **one BOS** on the internal trend in that direction is enough to look for trades. | 14:12–14:34, `p3_f004`–`f006` |
| **Counter-external rule.** To trade against the external trend you need **two BOS in a row on the internal trend** (a "two-step BOS"). One isn't enough. | 13:11–14:12, `p2_f134`–`f140`, `p3_f001`–`f002` |
| **Early trend beats late trend.** Prefer setups early in a trend, for example after the first one or two BOS. Avoid entries late in an extended trend. He says late trades *can* still be taken "if they're really good", so this is a preference, not a hard rule. | 17:54–19:30, `p3_f041`–`f058` |

## 4. Entry

| Rule | Source |
|---|---|
| Take **only bullish no-wick candles in a bullish trend** and **only bearish no-wick candles in a bearish trend**, where "trend" means the trend that passes the §3 alignment rules. | 04:01–04:20, `p1_f093`–`f098` |
| **Mark the level:** a horizontal line from the **flat side (open)** of the no-wick candle: the top of a bearish one, the bottom of a bullish one. | 04:23–04:31, `p1_f106`; 06:31 `p1_f140` |
| **Wait for price to retrace and tap that level.** | 04:31–04:47, `p1_f107`–`f108` |
| **Tap window: within 9 candles.** If price taps on the 10th candle after the no-wick candle, don't take the trade. "The less the better", ideally within 4. | 04:47–05:19, `p1_f108`–`f112` |
| **Enter on the tap, in the trend direction.** In every example the position tool's entry sits exactly on the marked level. | 05:19–05:25, `p1_f113`; 06:27–06:31, `p1_f140` |
| **Pre-entry.** When the no-wick candle sits **low in the leg** (for a buy; mirror for a sell), price may not come all the way back. Enter **a bit before** the level, at the **retest area** (the previous high in an uptrend, the previous low in a downtrend). He mentions "about 2–4 pips" but says it is deliberately **not objective**. | 30:06–32:29, `p5_f060`–`f092` |
| **Pre-entry with a Gann box** (an optional aid). Draw a Gann box from the bottom to the top of the leg, **using bodies/closes**. If the no-wick candle is **below 0.5**, enter at **0.5**. If above, enter normally at the level. He also describes "enter one level above the level the no-wick sits in". He says he doesn't use it himself. | 32:30–33:29, `p5_f093`–`f113` |

## 5. Stop loss

He gives **two methods** and says they have about the same win rate ("try out which ones you like").

| Rule | Source |
|---|---|
| **Method 1, structure:** for a sell, the stop goes **above the most recent high** before the no-wick candle (where the BOS is). For a buy, it goes below the most recent low. Add **"a little bit of breathing room"**. | 05:26–05:45, `p1_f113`–`f119`; 28:29–29:13, `p5_f009`–`f021` |
| **Method 2, previous candle:** the stop goes at the **high (sell) or low (buy) of the previous candle**. | 29:35–29:56, `p5_f029`–`f041` |
| **Doji candles are ignored as structure.** If the reference candle is a doji, use the next non-doji structure. | 29:27–29:45, `p5_f027`, `p5_f031` |

## 6. Take profit

| Rule | Source |
|---|---|
| **TP at 1:1** (the same distance as the stop). | 05:47, `p1_f120`; 06:31, `p1_f140` |
| **Stop loss priority / TP feasibility.** If a 1:1 TP would require price to break through several previous highs (buy) or lows (sell), **lower the TP** to a level price can realistically reach, below 1R. This applies to trades with an unusually large stop and target, "not normal trades". | 33:35–35:03, `p5_f115`–`f134` |
| **Imbalance target** (see §8): when trading the imbalance exception, the TP goes at the **top of the imbalance**, which can be more than 1:1. | 27:13–27:21, `p4_f123`–`f124` |

## 7. Trade management

| Rule | Source |
|---|---|
| Normally, once in a trade, **don't touch anything**. | 35:41–35:50, `p6_f009`–`f010` |
| **Only exception: an opposite no-wick candle forms against you** while you're in the trade. Once it has **closed**, wait for price to move a bit in your favour, then **move the stop to breakeven**. Example shown: a GBPUSD 15m short, with a bullish no-wick candle printing just after entry. | 35:50–36:14, `p6_f009`–`f013` |
| If you're **in drawdown** when the opposite no-wick candle appears, **move the TP to breakeven** instead. | 36:06–36:20, `p6_f012`–`f013` (speech only; not demonstrated on the chart) |

## 8. Exceptions that "overrule the trend logic"

| Rule | Source |
|---|---|
| **Imbalance exception:** a **one-step BOS** is acceptable against the external trend **as long as you're targeting an unfilled imbalance**. The imbalance must be **immediate**, with **no structure in between**. TP goes at the top of the imbalance; the stop at "the break of the low as usual". | 26:42–27:21, on-screen text at `p4_f121` |
| **An imbalance** is "a big move with only bearish or bullish candles that hasn't gotten filled", meaning a gap in price from a one-directional push. | 26:17–26:42, `p4_f112`–`f117` |
| **Don't trade it if the imbalance was already filled** when you would enter. Once it fills, price tends to continue in its original direction. | 27:26–28:31, `p4_f127`–`f132`, `p5_f001`–`f004` |
| **Decision areas** also overrule the trend rule. This is deferred; see §9. | 25:15–25:33 |

## 9. Deferred: ranges and decision areas (not in the baseline)

He covers these in this video (21:05–26:17) but tells viewers to watch his separate decision-area video first. Following your
instruction, I won't use any outside knowledge of decision areas until you send that video. What he says here is recorded so
it isn't lost:

- When there's no clear trend you have a **range**: price "ping-pongs" between support and resistance (21:47–22:09, `p4_f018`–`f024`).
- **Lower half of the range: prioritise buys. Upper half: prioritise sells** (22:13–22:43, `p4_f029`–`f035`).
- A **no-wick candle plus a tap into a decision area** is "a very strong combination". Stop goes beyond the decision area "with a bit of breathing room", TP 1:1 (22:53–23:33, `p4_f037`–`f043`).
- **Don't buy at the top of a range, or sell at the bottom** (23:43–24:11, `p4_f051`–`f063`).
- Mark decision areas **at the start of the session** (24:03).
- A decision-area tap can justify a **counter-trend** trade ("overrules the trend rule") (25:15–25:33, `p4_f099`).

## 10. Sessions, news and "don't trade" rules

| Rule | Source |
|---|---|
| **Trade London, NY and late Asia.** | 16:42–17:02, `p3_f026`–`f030` (on-screen text) |
| **Avoid the NYSE open, the first 3 hours of Asia, and late NY ("right before market close").** | 16:50–17:02, `p3_f030` |
| **Red-folder news:** ignore the news spike (24:21, `p4_f066`). Don't trade **1 hour before and 1 hour after** red-folder news. | 24:21; 36:46, `p6_f020` (on-screen "6. Avoid trading near red folder news") |
| **"Avoid these trades"** (on-screen list, built up item by item): **1.** trades with conflicting no-wicks ("two no-wicks telling different stories"); **2.** counter-trend trades; **3.** trades tapping into **decision areas** (his speech says "support or resistances"); **4.** trades with a huge SL & TP (or, if taken, put the TP where price can reach it, per §6); **5.** late trends ("super overextended"); **6.** trading near red-folder news (±1h); **7.** trading outside your session; **8.** trades you don't feel confident in. | 36:20–37:08, `p6_f014`–`f024` |

## 11. Account rotation (prop-firm execution layer)

| Rule | Source |
|---|---|
| Buy **3 funded accounts at once** and trade them **in order**. | 37:30–37:46, `p6_f036`–`f044` |
| Move to the next account after **2 wins in a row or 1 loss**. After all three accounts have been traded, **stop for the day**, then reset the next day. Two worked days are shown on screen: day 1 = W W (acc 1), L (acc 2), L (acc 3) → done; day 2 = L (acc 1), W W (acc 2), W W (acc 3) → done. | 37:41–38:16, `p6_f043`–`f063` |
| Effect: worst day = 3 losses (one per account); best day = 6 wins. He says you only need about a 60% win rate with this system. | 37:21, 38:18–38:20, `p6_f030`, `p6_f065`–`f067` |

---

# Open questions / assumptions

Nothing below has been guessed into a rule. Any placeholder needed to make code run will be a **labelled input**, flagged as an
assumption.

**A. Definitions**
1. **How exactly is "no wick" defined?** Is it strictly `open == low` (bullish) / `open == high` (bearish), or is a tolerance of a
   fraction of a pip allowed? The xGhozt indicator decides this, but its source isn't shown. Do you know its exact rule, or
   should I use strict equality with a tolerance input defaulting to 0?
2. **What is a pivot?** He uses "every single small pivot" on bodies, and the zig-zag indicator at period 2. For code I need a
   definition. Should a swing high be a candle whose body top is higher than the body tops of N candles on each side, using
   **body-based pivots with N = 2** (matching his period-2 zig-zag)? Or something else?
3. **What counts as a doji?** He says to skip dojis as structure but never defines one. I'd need a threshold, for example
   body ≤ X% of range, as an input.
4. **How do I count "within 9 candles"?** I read it as: the tap must happen on one of the 9 candles after the no-wick candle
   (a tap on candle 10 or later is invalid). Correct?
5. **What counts as "tapping" the level?** Any touch of the level by a wick, or must price trade through it?

**B. Trend and alignment**
6. **How should the counter-external two-step BOS work?** Once there have been two internal BOS against the external trend, does
   permission persist until the next opposite BOS? And does one BOS back in the external direction reset it?
7. **How should "early trend vs late trend" be handled?** He calls it a preference ("you can still take them if they're really
   good"). Should it be (a) ignored in the baseline, (b) an optional filter such as "only take the first N setups after a BOS",
   or (c) something you define?

**C. Timeframes**
8. **How should 15m / 30m / 1h priority work in code?** When the 15m no-wick candle's 30m (or 1h) parent candle is also a
   no-wick, should the trade use the **higher-timeframe** level, tap window and stop? Or should it simply prefer that one when
   both exist?
9. **External trend on the 4h:** should it use the same body-based pivot / most-recent-BOS method as the internal trend?

**D. Entry details**
10. **Is pre-entry in or out?** He says it's deliberately "not objective". Options:
    (a) off in the baseline;
    (b) the Gann rule (no-wick below 0.5 of the leg → limit at 0.5);
    (c) the "retest area" rule (previous high/low).
    Which do you want, if any? I'd add it as a switchable input.
11. **What is a "leg" for the Gann rule?** From the last swing low to the current swing high, on bodies?

**E. Stop and target**
12. **Which stop method is the default:** structure (most recent high/low before the no-wick) or previous candle? He says both
    have about the same win rate. I can make both selectable inputs.
13. **How much "breathing room"?** He never gives a number. Should it be an input in pips, defaulting to 0?
14. **Should "stop loss priority" (lowering the TP below 1:1) be coded?** It's discretionary ("a feasible area"). One option is to
    cap the TP just before the first opposing swing high/low that 1R would have to break. Or leave it out of the baseline and
    keep a fixed 1:1?

**F. Management, avoid list and rotation (Part 6)**
15a. **Contradiction to resolve (for when you send the decision-area video).** The on-screen avoid list says "Avoid trades
    tapping into decision areas" (36:28, `p6_f016`). But in Part 4 he calls a no-wick candle plus a decision-area tap "a very
    strong combination" and trades it in ranges (22:53–24:51). My reading is that tapping a decision area *against* your
    trade is to be avoided, while trading *from* a decision area in a range is the separate range play. This won't affect the
    baseline, since decision areas are excluded until you send that video.
15. **Breakeven rule details:** "wait for price to come down a bit" after the opposite no-wick candle closes before moving the
    stop to breakeven. How far is "a bit"? Should "in drawdown → move TP to breakeven" be coded as described?
16. **What counts as a "conflicting" no-wick candle?** For example, a bullish and a bearish no-wick candle both active and
    untapped at the same time?
17. **Imbalance exception:** do you want it in the baseline? If so, I need an objective imbalance definition, for example N
    consecutive same-colour candles with an unfilled gap, and a definition of "immediate, with no structure in between".
18. **Account rotation:** should this be simulated in the backtest, i.e. stop for the day after the 3-account sequence is used
    up, giving at most 6 wins / 3 losses per day? Or kept outside the strategy?

**G. Market and sessions**
19. **Which market should the baseline run on?** He trades the six forex pairs. You've been trading futures (MNQ/MES/MGC).
    Should the baseline target forex, as he teaches? And note he says don't trade gold, which rules out MGC.
20. **Session hours:** he names London, NY and late Asia, and the windows to avoid, but gives no clock times. What exact hours
    (New York time) should I use for:
    - London;
    - NY;
    - late Asia;
    - the "NYSE open" window to avoid;
    - the first 3 hours of Asia;
    - "late NY"?
21. **Red-folder news:** TradingView can't read an economic calendar inside a backtest. Should the news filter be left out, or
    should I add a manual input of news times?

Once you confirm or adjust these, and send Part 6 so I can verify §7, §10 and §11 against the frames, I'll write the Pine
Script with a timestamp citation on every rule.
