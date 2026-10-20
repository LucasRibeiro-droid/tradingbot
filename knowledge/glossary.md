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

## Results

| Term | Meaning |
|---|---|
| **R** | One unit of risk: the distance from entry to stop. +2R means the trade made twice what it risked. |
| **Reward to risk** | Distance to target ÷ distance to stop. |
| **Expectancy (average R)** | The average result per decision, in R. Above zero means the decisions make money over time. |
| **Base rate** | How often price went up (or down) anyway over the same horizon. A read only helps if it beats this. |
