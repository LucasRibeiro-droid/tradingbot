# Glossary

The trading terms the bot knows: what each means, how the bot measures it, and what it
signals. Updated as lessons are learned. Lesson notes have the full detail and timestamps.

## Candles (Day 2)

| Term | Meaning | How the bot measures it | Signals |
|---|---|---|---|
| **Candle** | One span of time (1 minute, 5 minutes, 1 day…) summarized as open, high, low, close. | `Candle` | — |
| **Timeframe** | How long one candle takes to close. | Alpaca timeframe, e.g. `5Min`, `1Day` | Higher timeframes outrank lower ones (Day 4). |
| **Body** | The part between open and close. | `Candle.body` | Big body = commitment. |
| **Wick** | The part of the range price visited but didn't close at. | `upper_wick`, `lower_wick` | Where price was rejected. "Wicks don't lie." |
| **Bullish / bearish candle** | Closes above / below its open. | `Candle.direction` | — |
| **Closed candle** | A candle whose time is over. Only closed candles count. | `Candle.closed` | Locked: never decide on a forming candle. |
| **Strong close** | Full body, almost no wick on the closing side. | read `kind="strong_close"` | Momentum continuing that way. |
| **Rejection** | A long wick, with the close at the other end of the candle. | read `kind="rejection"` | Price refused that side. |
| **Weakness** | A bullish (bearish) close with a fat wick on the closing side. | read `kind="weakness"` | Couldn't hold the high (low); often liquidity was taken there. |
| **Doji** | A tiny body; indecision. Variants: long-legged, dragonfly, gravestone, cross, inverted cross. | `shape()` | After a move: that move is losing momentum. |
| **Hammer / hanging man / inverted hammer / shooting star** | Small body with one long wick; named by the move before it. | `shape()` | Rejection of the wick's side. |

## Trend and structure (Days 4 and 6)

| Term | Meaning | How the bot measures it | Signals |
|---|---|---|---|
| **High** | A move up then a move down: an up candle followed by a down candle, at the higher wick of the two. | `swings()` | — |
| **Low** | A move down then a move up, at the lower wick of the two. | `swings()` | — |
| **Uptrend / downtrend** | Higher highs and higher lows / lower highs and lower lows. | `trend_series()` | Which way price wants to go. |
| **Consolidation** | Price going sideways: highs and lows with no break. | `TrendState.consolidating` | No direction: no call. |
| **Break of structure (BOS)** | A candle **closes** past the most recent high (up) or low (down). Wicks don't count. | `event="bos_up"/"bos_down"` | The trend has shifted. The decision trigger. |
| **Fake / sweep of structure** | A wick past the level being watched, without a close. | `event="sweep_high"/"sweep_low"` | Not a break; often a liquidity sweep. |
| **Higher-timeframe bias** | The trend on the larger timeframe. | `bias()`, `state_at()` | Locked: only trade in its direction. |
| **Retracement** | A move against the higher-timeframe trend. | — | A break against the higher timeframe is often just this. |
| **Line chart** | Closes only, joined up; makes direction easy to see. | `swing_source="close"` | — |

## Liquidity (Days 8, 10, 12)

| Term | Meaning | How the bot measures it | Signals |
|---|---|---|---|
| **Liquidity** | Resting orders: stop losses and pending orders waiting at a price. | `scan()` | Where banks can fill large orders. |
| **Buy-side liquidity** | Orders resting above a high (breakout buy stops, shorts' stop losses). | `Pool.side="buy_side"` | A magnet above. |
| **Sell-side liquidity** | Orders resting below a low (breakdown sell stops, longs' stop losses). | `Pool.side="sell_side"` | A magnet below. |
| **Prominent high / low** | A clear high or low that has held: the start of a trend, a double top, one that broke structure. | pivot with `pool_strength` 5 | Holds the most liquidity. |
| **Pool** | Liquidity at one prominent high or low that price hasn't traded through yet. | `Pool` | — |
| **Liquidity sweep / taken** | Price trades past a pool. | `Taken` | Orders filled there; a reversal the other way becomes likely. Not an entry alone. |
| **Draw on liquidity** | The nearest untaken pool in a direction. | `draw()` | Where price is likely headed: the target. |
| **Market movers** | Banks and institutions whose orders move price. | — | They need liquidity to fill. |
| **Confluence** | Several indicators agreeing. | `DecisionParams.confluences` | Required before the bot acts. |

## Fair value gaps and execution terms (Days 14, 16, 18)

| Term | Meaning | How the bot measures it | Signals |
|---|---|---|---|
| **Fair value gap (FVG)** / **liquidity void** / **imbalance** | Three names for one thing: a price range with no opposing orders, so price moved through it fast, usually as a big candle with no hesitation [TJR Day 14]. | `find_gaps()`: three candles; bullish = candle 1 high to candle 3 low, bearish = candle 1 low to candle 3 high, when they don't overlap [TJR Day 16] | Where retracements are drawn back to in a trend; with a reaction or lower-timeframe break inside it, an entry for continuation. Not for reversals. |
| **Retracement** | A pullback against the trend before it continues. | — | In a trend, retracements are drawn into fair value gaps [TJR Day 14]. |
| **Filled** | Price has come back into a gap [TJR Day 16]. Exact meaning not specified. | `follow()`: touched [Bot] | — |
| **Reaction** | After a gap is filled, a candle closing in the trend's direction [TJR Day 16, 08:09]. | `follow()` [Bot test] | Confirmation to act. |
| **Secondary entry / patient entry** | After a sweep and break, waiting for the retracement into a gap and a lower-timeframe break for a better reward-to-risk [TJR Days 14, 18]. | `decision.Continuation` | — |
| **Scale down** | Moving to a lower timeframe to find the entry trigger, sometimes several times (15m → 5m → 1m) [TJR Days 14, 18]. | higher/lower timeframe pair in the harness | — |
| **Market open** | The session open; TJR only takes trades from the open on [TJR Day 18]. | `after_market_open()`: 9:30 New York | Its full value is taught later. |
| **Take profit / partials** | Closing part of a position at a target; TJR used several [TJR Day 18 example]. | not yet | — |
| **Break even** | Moving the stop to the entry price so the rest of the trade can't lose [TJR Day 18 example]. | not yet | — |
| **Accumulation** | An area where orders built up before a move; used as a target [TJR Day 18]. Day 20: the same as an order block. | — | — |

## Order blocks (Days 20, 22, 24)

| Term | Meaning | How the bot measures it | Signals |
|---|---|---|---|
| **Order block** | The whole move that caused a liquidity sweep, before the break of structure that shifted the market: the leg up that took the highs (before a break down), or the leg down that took the lows (before a break up). Orders were filled there [TJR Days 20, 22]. | `find_blocks()`: leg from the last two-candle low/high to the sweep's extreme, wick to wick, must take a pool [Bot] | Price tends to retrace into it and continue the new way. TJR's first-choice retracement area. One per trend. |
| **Wick to start of body** | TJR's own way to box an order block: from a candle's wick to where its body starts, where price often reacts [TJR Day 24, 11:46]. Beginners box the whole leg. | `wick_zone()`: the leg's candle nearest the retracement [Inferred from frames] | A reaction point; pullbacks often go deeper. |
| **Double confirmation** | Waiting for another break of structure when price is already inside the block at the first break [TJR Day 24, 24:46]. | — | — |
| **Accumulation area** | Same as an order block [TJR Day 20, 11:08]. | — | Also a target (Day 18). |
| **Retracement tools** | Order blocks, fair value gaps and equilibrium, in TJR's order of preference [TJR Day 20, 06:24–07:49]. | — | Where to re-enter after missing the sweep-and-break entry. |
| **Disrespected** | Price pushed straight past a gap or block instead of reacting [TJR Day 22, 11:46, 17:05]. | `follow()` "broken" [Bot] | Drop it. |
| **Pre-market** | Before the session open; TJR doesn't trade it [TJR Days 18, 22]. | `after_market_open()` | — |
| **London session** | The London open; TJR waited for it on a GBPUSD 15-minute example [TJR Day 22, 16:17]. | not used (US instruments) | — |
| **News days** | Days with major releases (PPI, FOMC); TJR says not to trade them [TJR Day 20, 11:41]. | not yet (Day 19) | — |

## Results

| Term | Meaning |
|---|---|
| **R** | One unit of risk: the distance from entry to stop. +2R means the trade made twice what it risked. |
| **Reward to risk** | Distance to target ÷ distance to stop. |
| **Expectancy (average R)** | The average result per decision, in R. Above zero means the decisions make money over time. |
| **Base rate** | How often price went up (or down) anyway over the same horizon. A read only helps if it beats this. |
