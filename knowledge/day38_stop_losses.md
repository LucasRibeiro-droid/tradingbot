# Day 38 — Stop Losses

Source: TJR Boot Camp, Day 38: Stop Losses (https://www.youtube.com/watch/1FunNCUw_jM, 13:13).
Studied from the uploaded video (720p) and the owner's captions (`sources/day38_stop_losses.md`).
Recorded live on Zoom with his Discord, using a trade that had just stopped out. Frame viewed
at 07:35 and saved in `sources/day37_38_frames/`. Topic file: `exits.md`.

**Classification:** a single lesson; **complete**. Methodology (exits) and risk.

## What it teaches

### 1. The stop goes beyond the liquidity sweep (01:00–03:57)
- "I almost always put my stop loss above the liquidity sweep" (01:28–01:36), "whether you're entering off of a fair value gap or an order block" (03:28–03:37).
- **Why: it's the invalidation point.** "If our bias was correct, if liquidity was actually taken out, then price has no reason to come back above this high ... If price ends up coming back above this high then the liquidity sweep was not valid ... there weren't enough orders to be filled ... **our stop loss is essentially our invalidation area**" (01:39–02:55).
- Not just above a nearer high: "price could easily come back a little bit higher and then come back down" (03:39–03:57).

### 2. The exception he doesn't like (04:01–05:16)
- If the sweep is so far away that it gives "a terrible risk to reward", put the stop above a closer order block or gap instead. "But the reason I don't necessarily like doing that is ... the invalidation point is above the liquidity sweep, so price could still technically move up and take you out of the trade and still go within our bias."

### 3. Room for the spread (06:05–07:41; frame at 07:35)
- "Every single time at least put it like 0.5 points below the actual price point, or figure out what your spread is on your broker for the specific pair." Otherwise "you are going to get stopped out by spread".
- The trade of the day: a 5-minute sweep, a 1-minute break up, stop under the sweep; stopped out ("we barely got wicked out"), then price went up anyway. The frame shows the long stopped just under the swept low before the rally.

### 4. Higher-timeframe trades (08:16–09:22)
- With a 15-minute sweep and break, the 15-minute stop can make the first take profit's reward-to-risk too low. "You could scale into a relatively higher time frame and try and find a low ... underneath the liquidity sweep, if you want to be extra safe."

### 5. Risk tolerance (09:22–11:55)
- "All of this is just purely based off of your own risk tolerance." TJR uses a **set lot size**, scaled by confidence for the day (lot sizing next, Day 39). That day he risked **half** his usual size: high-impact news, and a US bank holiday the next day ("relatively low volatility, kind of choppy market conditions"). He'd de-risk all week with high-impact news.
- "Your stop loss should never be based purely off of points or pips. It should be based off of where price is invalidated, where your bias is invalidated" (11:04–11:22).
- Being stopped out doesn't mean the daily bias was wrong: "my overall daily bias was bullish and that is getting fulfilled, but for this specific execution ... this was my invalidation point. It got invalidated, but then price ended up moving higher" (11:22–11:55).

### 6. Bank holidays (12:36–12:58)
- "Don't trade tomorrow ... it's a bank holiday ... and don't trade some random foreign exchange pair, okay? US bank holidays typically slow all the markets."

## Connections
- **Days 8–12:** the sweep is where orders were filled; beyond it, the idea is wrong.
- **Days 22, 30:** stop "above the order block itself to play safe", "stops above the highs". Now the rule.
- **Day 37:** the take-profit ladder; reward-to-risk needs a sensible stop.
- **Days 3, 29 (plan), 39 (lot size):** risk tolerance and sizing.

## Provenance audit
- **[TJR]**
  - The stop beyond the liquidity sweep = the invalidation point, whatever the entry.
  - The exception: above a closer block or gap when the sweep is too far (disliked).
  - A spread buffer (0.5 points on the S&P, or the broker's spread).
  - Higher-timeframe trades: optionally under a higher-timeframe low.
  - Stops by invalidation, never by fixed points.
  - De-risk on high-impact news and before bank holidays; no trading on US bank holidays.
- **[Bot]** The models study's stop is the sweep's extreme (as taught), without a spread buffer (bar data; SPY and GLD spreads are about a cent). The order-block/gap exception isn't tested.
