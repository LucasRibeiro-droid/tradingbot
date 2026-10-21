# Day 22 — Order Blocks, Part 2: how to spot them

Source: TJR Boot Camp, Day 22: Order Blocks pt.2 (https://www.youtube.com/watch/RQSVIKddFHI,
about 25:56). The owner uploaded it in two halves of 12:59.5 each (part 2's video time =
lesson time − 12:59.5). Studied from the video and the owner's captions
(`sources/day22_order_blocks_pt2.md`). Frames checked at 02:05, 05:20, 08:05, 09:56, 12:45,
14:15, 17:20, 21:30, 23:25. Topic file: `order_blocks.md`.

**Classification:** part 2 of 3: identification, with many worked examples. Still **open**
(Day 24 puts it together).

## What it teaches

### 1. The definition again (01:33–03:04)
- The move prior to the break of structure that swept liquidity. "This is where orders were able to get filled for price to be able to make that break of structure." When price retraces, "they are going to want to fill more orders here, because they were able to fill orders within this price range previously" (02:08–02:30).
- Downtrend version: "this is going to be our order block, because it was the move that swept liquidity" (02:36–02:46).

### 2. How to find one (04:09–06:16; frame at 05:20)
- Find the break of structure, then ask: "where was the down move prior to the break of structure, where orders were filled?" (04:15–04:27).
- On the 4-hour it's one candle; "if we go into the one hour it'll be easier to see" (04:31–04:46). "Your stop will be under here", then price "draws right back into here, fills more orders and booms" (05:06–05:16).
- Lower timeframes are easier: "there's so many more" (03:49–03:57).

### 3. It's the whole move; which timeframe you play matters (07:03–10:39; frames at 08:05, 09:56)
- "Order blocks can be represented on several time frames, but you have to understand it's the **whole move**" (07:03–07:15).
- On the 4-hour, "this was the candle, and yes, that would be relatively precise ... but what was the entire move?" That gives "a big price range to deal with; however, that's why we can scale down" (07:49–08:15).
- **Stops depend on the timeframe you're playing:** a 4-hour order block is "several hourly candles". "What makes you think that when you just see a break of structure on the hourly time frame off of this, you can keep your stop loss super tight? You're gonna get stopped out." For a 4-hour move and 4-hour break, "you're gonna have to put your stop all the way up here", then "target previous areas of liquidity on higher time frames" (09:15–09:59). "Understand your time frames ... that can mess you up big time" (10:25–10:39).

### 4. GBPUSD daily → 1-hour → 15-minute (10:57–15:41; frames at 12:45, 14:15)
- Daily downtrend; the order block is the entire down move prior to the break (11:03–11:21). Scale down for a better entry (11:28).
- The 4-hour break is the retracement; an imbalance on the way is "disrespected" (price pushes right past it, as on Day 18) (11:46).
- 1-hour: a low is swept and structure breaks up, but entering there means a wide stop (12:27).
- Wait for the retracement into the 1-hour order block; scale down to the 15-minute (12:41). It's **pre-market**, so no trade; mark the 9:30 open, watch the highs; 15-minute break of structure → long (12:50–13:40).
- Take profits at an earlier target, the imbalance's 50%, then the highs: "pretty much a one to twelve risk reward" (14:17). Entering on the hourly break would also have worked; patience gave the better trade.

### 5. More examples (15:41–23:43; frames at 17:20, 21:30, 23:25)
- **15-minute, London:** "right during London session, so we're going to wait for London session open"; watch the highs; break → enter. A gap inside the order block: one disrespected, the next filled → long; targets previous areas of liquidity (16:07–17:32).
- GBPJPY: "so volatile ... when it goes it really goes" (18:32).
- **One that misses:** "doesn't quite hit it ... sometimes it's just not going to hit. It's going to fill off of other things and other reasons, and that's something you just have to be okay with" (19:04–19:16).
- After a retrace into an order block: "chop chop chop, fills more orders, break structure again, boom, rallies" (19:41–19:46).
- **4-hour break → 15-minute entry:** stop "can either be under here or underneath here, it doesn't really matter"; several targets hit (20:42–21:28).
- **Short:** sweep, break, price pushes up into the range, scale down, break of structure, short, "stop either above here or above the order block itself if you want to play safe", target previous liquidity (22:45–23:30).

### 6. Homework and the reason for it (23:57–25:29)
- "The only hard part is putting it to work in live action; that's where experience and market intuition comes" (23:57–24:07).
- **Homework:** "find five examples of order blocks on three different time frames ... four hour, five minute, one hour, I don't care, one minute" (24:10–24:23).
- Live, after a break up: "this is the leg down that caused the move up ... this is going to be my retracement area **if I can't find a good risk reward trade off of just a liquidity sweep and break of structure**. If I'm going to get filled all the way up here, why wouldn't I wait for a potentially way better risk reward ratio right here, and make a lot more money, and be patient" (24:48–25:29).

## Connections
- **Day 20:** same definition; adds how to find, the whole-move rule, and stops by timeframe.
- **Day 18:** the same patient entry (retrace + lower-timeframe break), now with an order block as the area; a "disrespected" imbalance = a gap price pushed past; pre-market = no trades.
- **Day 12:** targets at previous liquidity, now "on higher time frames".
- **Day 4:** the timeframe hierarchy now also governs stop size.
- **Day 7:** the London open as a time to watch (TJR's market); for the bot, which open applies is still open.

## Provenance audit
- **[TJR]** The leg before the break that swept liquidity; the whole move, visible on several timeframes; scale down for precision; stop size follows the timeframe you're playing; stop beyond the order block "to play safe"; target previous liquidity; wait for the open; entry on a lower-timeframe break inside the area; sometimes price doesn't reach it; use it when sweep + break gives poor reward-to-risk.
- **[Inferred]** The examples' entries always had a lower-timeframe break of structure inside or after the order block; price touching the block alone was never the entry.
- **[Bot]** Everything exact in `tradingbot/orderblocks.py` (where the leg starts, wick-to-wick boundaries, using `liquidity.py` pools as "liquidity", "broken" = a close beyond the sweep's extreme).
