# Day 14 — Fair Value Gaps, Part 1: what they are and why they matter

Source: TJR Boot Camp, Day 14: Fair Value Gaps Pt. 1 (https://www.youtube.com/watch?v=d0AxLACYaqU, 10:07).
Studied from the uploaded video (360p, with audio, 10:06). Transcript made offline with
Whisper, in `sources/day14_fair_value_gaps_pt1.md`. **No charts are shown:** the whole video
is TJR talking to the camera (recorded on a trip, after his laptop overheated), so the
transcript is the lesson.

**Classification:** new concept, part 1 of a 3-part topic. Part 2 (Day 16) teaches how to
spot fair value gaps; Part 3 (Day 18) is expected to cover using them. **The topic is
incomplete;** nothing here is final.

## What it teaches

1. **Three names, one thing.** Fair value gap = liquidity void = imbalance. TJR calls it a liquidity void [TJR 02:02–02:08].
2. **The opposite of liquidity.** Liquidity is where orders rest; a liquidity void is a price range with **no opposing orders**. Price moves up fast through a range with no sell orders, and drops fast through a range with no resting buy orders. If there were orders, price would hesitate ("go down, pull up a little bit, go down a little bit more") [TJR 02:11–03:04].
3. **What it looks like:** "most of the time it's a big candle", a move "with no hesitation" [TJR 02:46, 05:31–05:50]. The exact way to identify one is Day 16.
4. **What it's for: retracements.** In a trend, pullbacks are drawn back into these voids. Market makers execute their orders there, knowing that once they do, price will move their way again [TJR 03:12–03:44, 05:50–05:59].
5. **Its role next to liquidity:** "I use liquidity sweeps to understand where markets going, and then I use fair value gaps to figure out where price maybe wants to draw to, or for a secondary entry" [TJR 03:52–04:22]. Fair value gaps are "not for entries necessarily".
6. **The entry pattern described:** price in an uptrend retraces into a fair value gap **on a larger timeframe**; then a **break of structure on a smaller timeframe** in the trend's direction; execute [TJR 04:24–05:05]. In summary: "When we see a retracement, figure out where the imbalance is, scale down to a lower timeframe, find a break of structure continuation" [TJR 06:34].
7. **The pieces chained together:** "liquidity sweep, break of structure, and we see the trend starting to form. Now I have a fair value gap. Oh, I notice it gets filled. Smaller timeframe, break of structure. Boom" [TJR 06:11].
8. **Modular confirmations:** "All of these are pretty much execution pieces ... which ones you want to use. And the more that you know the better ... five different confirmations" [TJR 07:33–07:55]. Works on any timeframe and market, scalps or swings [TJR 06:56–07:27].
9. **Homework:** none for trading; do something productive and uncomfortable, and balance work with fun [TJR 08:15–09:39].

## Connections to earlier lessons

- **Liquidity (Days 8–12):** the void is liquidity's opposite. Liquidity tells where price is going and where reversals start; voids tell where retracements go.
- **Trend (Day 4):** voids matter for the higher lows (lower highs) of a trend, i.e. continuation.
- **Break of structure (Day 6):** used again as the trigger, now on a **lower** timeframe inside a higher-timeframe zone.
- **Higher timeframes (Day 4):** this is the clearest example yet of TJR's multi-timeframe process: zone on the higher timeframe, trigger on the lower.
- **Day 12** already showed this in action: "dip down into this imbalance ... probably where you would have wanted to get your orders filled" (gold 5-minute, 15:14), and "filling this imbalance ... areas to take profit" (13:55).
- **Day 7:** the pieces are modular confirmations, restated here (07:33).

## What changes in the methodology

- Adds the **continuation** path: trend → retracement into a fair value gap → lower-timeframe break of structure. The reversal path (sweep → break) came from the liquidity lessons.
- Confirms that entries are **two-timeframe**: context and zone on the higher, trigger on the lower. The bot's test harness currently uses one timeframe for the trigger; that's flagged in `decision.md`.

## Open questions (for Days 16 and 18)

- How exactly is a fair value gap identified on a chart?
- What counts as the gap being "filled": touched, entered, or fully crossed?
- Which lower timeframe pairs with which higher timeframe?
- What does "secondary entry" mean?
- Does an unfilled gap also act as a target (Day 12 said imbalances are areas to take profit)?

## What the bot does with this now

Nothing executable yet. TJR hasn't taught how to identify a fair value gap, so the bot
doesn't detect them; that waits for Day 16. The concept, its role and the questions above
are recorded in `methodology.md` and `glossary.md`.
