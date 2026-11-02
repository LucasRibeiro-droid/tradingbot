# NOWICK Trend Backtester: Forex, 15-minute chart

`nowick_forex.pine` is the **same strategy** as `day_trading_backtester.pine`. It trades with the
trend, places a limit order at the tap of a no-wick candle's high or low, puts the stop at the most
recent swing, and targets a fixed 1:1. The difference is that it's set up for **forex pairs on a
15-minute chart**. For the rules, the chart markings and the results table, see
[README.md](README.md). This file only covers what's different.

## Adding it to a chart
1. Open a forex pair (the script stops with an error on futures or stocks), for example `OANDA:EURUSD`, `FX:GBPUSD` or `OANDA:USDJPY`, and set the
   timeframe to **15m**.
2. In the Pine Editor, create a new script (**script name ▸ Create new ▸ Strategy**). Paste the
   contents of `nowick_forex.pine`, then click **Save** and **Add to chart**.
3. In the Strategy Tester, set the date range to the longest one available and the initial capital
   to your account size. On the free plan, leave "High detalization" **off**.
4. Under **Inputs ▸ Costs**, enter your broker's **spread** and **commission**.

## What's different from the futures version

| | Futures version | Forex version |
|---|---|---|
| Chart | 5m | **15m** |
| Size | Contracts | **Lots** (default 1 lot = 100,000 units) |
| Distances | Ticks | **Pips**. Pip size is detected automatically: 0.01 for JPY-quoted pairs, 0.0001 otherwise. It can be overridden. |
| Main cost | Commission + slippage | **Spread** (paid once per round trip) + commission per lot + slippage |
| P&L currency | Contract currency | Converted to your account currency (USD by default; change it in Properties ▸ Base currency) |
| Order wait | 12 bars (1 hour) | **4 bars (1 hour)** |
| Min stop | 8 ticks | **5 pips** |

The trend filter looks at the **previous 2 hours** (120 minutes = 8 bars on 15m) instead of 30 minutes.
These rules are unchanged: ATR and efficiency thresholds, swing 2/2, 1:1
target, trading window 09:30–15:45 ET and flatten at 15:55 ET. The flatten is before the 17:00 ET
rollover, so no overnight financing (swap) is paid.

## Inputs that only exist here

| Input | Default | What it does |
|---|---|---|
| Lots per trade | 1.0 | Position size. |
| Units per lot | 100,000 | Standard forex lot. |
| Pip size (0 = auto) | 0 | Override if your symbol isn't a standard forex pair. |
| Spread (pips) | 1.0 | Typical spread during your trading hours. A spread-only account like OANDA standard is about 1.0–1.5 on EURUSD. A raw/ECN account is about 0.1–0.3. |
| Commission per lot per side | 0 | 0 on spread-only accounts. On raw/ECN accounts it's typically 3.00–3.50. |
| Slippage per fill (pips) | 0.2 | Charged on stops and EOD exits, and on limit fills if that option is on. |
| Entry / TP trade-through (pips) | 0 / 0.2 | How far price must go beyond the level or target before a fill counts. |

## Properties to match

| Property | Set to |
|---|---|
| Initial capital / Base currency | Your account. |
| Commission | 0 (the table applies yours). |
| Slippage | 0, matching the "Slippage set in Properties" input. |
| Margin long / short | 0 % |
| Recalculate / Fill on bar close | All off |
| Bar magnifier / "High detalization" | Off on the free plan, on if your plan allows it. |

## Forex-specific limitations
- **The 2-hour trend window reacts more slowly.** A trend has to build for a while before setups
  count, and a fresh reversal takes time to register. Shorten **Look-back window** (for example
  to 60) if it reacts too late.
- **Bid prices.** Forex charts usually show bid prices, but buy orders and buy stops really execute
  at the ask. Longs get tapped slightly earlier, and shorts get stopped slightly earlier, than the
  chart shows. The flat spread cost approximates this but doesn't model it exactly, especially
  around news and the 17:00 ET rollover, when spreads widen.
- **Same-bar entry and exit** is more common on 15-minute bars. Without the paid bar magnifier,
  TradingView's guess about which happened first can flatter the results.
- **The free plan gives more history on 15m** than on 5m (about 5,000 bars, or 2–3 months of
  24-hour forex). That still isn't many trades if only NY hours are traded.
- **Untested.** I couldn't compile this script myself. Paper-trade before risking money.
