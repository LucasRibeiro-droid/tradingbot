# NOWICK Trend Backtester: tap entries on no-wick candles (Pine Script v6)

`day_trading_backtester.pine` is a TradingView strategy that trades **with the trend**. When a
**no-wick candle** forms in the trend's direction, it rests a limit order at that candle's
open-side extreme. It enters when price **taps** that level, with the stop at the **most recent
swing** and a **fixed 1:1** take-profit.

It runs on a **5-minute chart** of **MNQ, ES, MGC or GC**, one instrument per chart. Commission
and slippage are modelled realistically, and the results are shown in a table on the chart.

---

## 1. Adding it to a chart

1. Open `MNQ1!`, `ES1!`, `MGC1!` or `GC1!` and set the timeframe to **5m**. If the chart has a
   **B-ADJ** (back-adjust) toggle, turn it off.
2. In the **Pine Editor**, create a new script (**script name ▸ Create new ▸ Strategy**), or open
   your existing one. Select all, paste the whole file, then click **Save** and **Add to chart**
   (▶). Don't click **Publish**, which posts the script publicly.
3. In the Strategy Tester:
   - set the date range to the longest one available;
   - set the initial capital to your account size;
   - on the **free plan**, leave "High detalization" (bar magnifier) **off**.
4. Under **Inputs ▸ Costs**, enter your broker's commission.

---

## 2. The rules

These are written for a **short**. A long is the mirror image: a bullish candle with no bottom
wick, a buy limit at its low, and the stop at the most recent swing low.

1. **Trend.** Over the last *Look-back window* minutes (default 30, which is 6 bars on 5m), two
   things must both be true:
   - Price has moved **down by at least X × ATR**, measured as the close now minus the close at the
     start of the window.
   - It got there fairly directly. **Efficiency** is the net move ÷ the total distance travelled,
     and must be ≥ the minimum (default 0.35).

   If either check fails, the market counts as **consolidating** and nothing is traded. Only
   bearish no-wick candles in a downtrend, and bullish ones in an uptrend, are used.
2. **No-wick candle.** A bearish candle where `high − open ≤ wick tolerance` (default 0 ticks)
   marks a level at its **high**.
3. **Order.** When that candle closes, a **sell limit** is placed at the level.
4. **Entry.** Price only needs to **tap** the level. The order fills there, or at a better price if
   the bar opens beyond it.
5. **Stop-loss** is at the **most recent confirmed swing high above the entry**. A swing high is a
   high with *left/right* lower highs either side, so it is confirmed *right* bars after it prints.
   The setup is skipped in either of these cases:
   - there is no swing high above the level;
   - the swing is closer than the *Minimum stop distance*.
6. **Take-profit** is fixed at **1:1**: the same distance below entry as the stop is above it. The
   R multiple is an input.
7. **While the order waits,** the stop and target are recalculated every bar, in case a newer
   swing prints. The order is cancelled in any of these cases:
   - it isn't filled within *Cancel the entry order after* bars (default 12 = 1 hour);
   - the trend flips the other way (input, on by default);
   - the trading window ends, the flatten time is reached, or the daily loss limit is hit.

   A newer qualifying no-wick candle replaces the waiting order.
8. **One position at a time.** No-wick candles that form during a trade are ignored. Everything is
   flattened at 15:55 ET.

---

## 3. What you see on the chart

| Mark | Meaning |
|---|---|
| Red **▼ NW** / teal **▲ NW** | A no-wick candle with the trend: a sell / buy limit was placed at its high / low. |
| Grey **×** | A no-wick candle that was ignored: no trend (consolidating), against the trend, or outside the trading window. |
| Thick dashed line | The waiting limit order at the level. It turns grey and dotted when filled, cancelled or replaced. |
| **Red box** | Risk: from entry to the stop-loss. The label shows the SL price and its distance in ticks. |
| **Green box** | Reward: from entry to the take-profit. The label shows the TP price and "1R". |
| White line + "LONG / SHORT" label | Entry level. |
| Label at the exit | How the trade ended (`TP`, `SL`, `EOD`, `DLL`), plus the net result in currency and in R. |
| Light green / red background | Trend up / down. **No tint means consolidating.** |
| Orange dots (optional) | Swing highs and lows used for stops. Turn on "Mark swing highs / lows" in Display. |

You can set up **alerts** using Alert ▸ Condition: this strategy ▸ "alert() function calls only".
An alert fires when an order is placed and when it fills.

---

## 4. Inputs

### No-wick setup
| Input | Default | What it does |
|---|---|---|
| Wick tolerance (ticks) | 0 | How big a wick is still counted as "no wick". |
| Cancel the entry order after (bars) | 12 | How long the limit waits for the tap. |
| Take profit (R multiple) | 1.0 | 1.0 = 1:1. |
| Trading window (ET) | 09:30–15:45 | Orders are only placed, and only fill, inside this window. |

### Stop loss (most recent swing)
| Input | Default | What it does |
|---|---|---|
| Swing left / right bars | 2 / 2 | Defines a swing. A larger *right* value means fewer, but later-confirmed, swings. |
| Max swing age (bars) | 60 | Older swings are ignored. |
| Minimum stop distance (ticks) | 8 | Skips setups whose swing stop is closer than this. |
| Stop buffer (ticks) | 0 | Extra ticks beyond the swing. |

### Trend filter
| Input | Default | What it does |
|---|---|---|
| Look-back window (minutes) | 30 | 15–30 recommended. |
| Minimum net move (× ATR) | 1.0 | How far price must have moved over the window. |
| Minimum directional efficiency | 0.35 | How "one-way" the move must be. |
| ATR length | 14 | — |
| Cancel a waiting order if the trend flips | on | — |

### Day trading rules
| Input | Default | What it does |
|---|---|---|
| Contracts per trade | 1 | — |
| Trading day starts (ET) | 09:30 | Daily reset for the loss limit. Use 08:20 for gold if you trade the COMEX open. |
| Flatten all at (ET) | 15:55 | Closes any position and cancels any waiting order. |
| Daily loss limit | off / 500 | When reached, closes everything and stops trading until the next day. |

### Costs: the stress-test panel
| Input | Default | What it does |
|---|---|---|
| Commission per contract per side | 0.62 | Your all-in rate, charged on entry and exit. |
| Slippage per fill (ticks) | 1 | Always charged on stop-loss, EOD and DLL exits. |
| Apply slippage to limit fills too | on | Also charges slippage on tap entries and take-profits. TradingView never slips limits. |
| Entry: ticks price must trade THROUGH the level | 0 | 0 = a tap fills you, as your rule says. Try 1 to see how much the results depend on perfect tap fills. |
| Take-profit: ticks price must trade THROUGH the target | 1 | A take-profit only counts once price goes this far beyond it. |
| Slippage set in Properties (ticks) | 1 | **Must equal** Settings ▸ Properties ▸ Slippage. |

---

## 5. Strategy Tester "Properties"

| Property | Set to |
|---|---|
| Initial capital | Your account size. This drives max drawdown %. |
| Commission | Cash per contract, your rate. This only affects the Tester's own numbers. |
| Slippage | Same as the "Slippage set in Properties" input (default 1). |
| Verify price for limit orders | 0 |
| Margin long / short | 0 % |
| Recalculate after order filled / on every tick | Off / Off |
| Fill orders on bar close | Off |
| Bar magnifier / "High detalization" | Off on the free plan. **On** if your plan allows it, because it matters a lot for this setup. |

---

## 6. The results table

The table has columns for **Longs**, **Shorts** and **All**. It only counts closed trades, each
re-priced using the Costs inputs:

- **Gross P&L** is the result at frictionless prices: entry at the level, take-profit at the
  target, and the Tester's own slippage removed.
- **Costs** = commission × 2, plus slippage on each fill.
- **Net P&L** = gross − costs. Win rate, profit factor, expectancy, average win/loss, R and
  drawdown are all calculated on net.
- **Tester net profit (ref.)** is TradingView's own figure.

Two rows below the main table:

- **Setups funnel.** It counts how many no-wick candles appeared, how many were filtered out (no
  trend), how many orders were placed, and how many were tapped and filled. It also shows why
  orders didn't fill (expired, trend flipped, replaced) and why setups were skipped (no valid
  swing stop, already in a trade).
- **Costs line.** It shows the cost settings the run used.

**At 1:1, costs matter a lot.** On MNQ, one round trip costs about $2.24 with the defaults, while
an 8-tick stop risks $4. You'd need to win well over 50% of trades just to break even. Watch the
"Costs % of gross P&L" and "Avg R achieved" rows.

---

## 7. Known limitations

Each place where TradingView's fill assumptions could be optimistic is marked
`⚠ FILL ASSUMPTION` in the code.

- **Entry and exit in the same bar.** Tap entries fill inside a bar, so the entry and the stop or
  target are often touched in the same 5-minute bar. Without the bar magnifier (a paid feature),
  TradingView guesses which happened first, and that guess can turn real losers into winners. This
  is the biggest weakness of a free-plan test of this setup. Be suspicious of trades that open and
  close in the same bar.
- **Tap fills.** A resting order at the exact level is assumed to fill completely on a single tap.
  Live, you may not be filled because of your place in the queue. Test with entry trade-through =
  1 to see how sensitive the results are.
- **Stop slippage is a fixed number of ticks.** Stress-test with 2–4 ticks.
- **Swing confirmation lag.** A swing only counts once *right* bars have passed, so a very recent
  high may not be used yet.
- **Daily loss limit** is only checked on bar closes.
- **Early-close days** are detected using TradingView's session calendar. Check trades on holidays.
- **Sample size.** About two weeks of free-plan data isn't enough to judge anything. Aim for 100+
  trades.
- **Untested.** I couldn't compile this script myself, so reconcile a few trades by hand and
  paper-trade before risking money.

---

## 8. Other versions in this folder

| File | Market | Chart | Notes |
|---|---|---|---|
| `day_trading_backtester.pine` | Futures | 5m | This README. |
| `nowick_futures_15m.pine` | Futures (MNQ, NQ, ES, MES, MGC, GC) | **15m** | Same rules and inputs as this README. The defaults are adjusted so they mean the same time on 15m: the order waits **4 bars (1 hour)**, and the 30-minute trend window is 2 bars (raise it to 60–120 for a steadier read). It stops with an error on non-futures charts. |
| `nowick_version_a_5m.pine` | Futures (MNQ, MES, MGC) | **5m only** | **Version A**: exactly the 15m script's logic and settings run on 5-minute candles, so the entry order waits **4 bars (20 minutes)**. It's identical to what you got by loading `nowick_futures_15m.pine` on a 5m chart, but stops with an error on any timeframe other than 5m. |
| `nowick_version_a_5m_multi.pine` | Futures (MNQ, MES, MGC) | **5m only** | **Version A Multi**: the same rules as Version A, but **up to 3 trades at once** (input "Max trades open at once"). Every qualifying no-wick candle keeps its own limit order (no replacing), and each order or trade has its own ID (`NW1`, `NW2`…), stop, target and drawing. Open trades plus waiting orders never exceed the maximum, and all trades are in one direction. A setup against the open trades is skipped. The 15:55 flatten closes all of them. |
| `nowick_forex.pine` | Forex pairs | 15m | Lots, pips and spread. See [README_forex.md](README_forex.md). It stops with an error on non-forex charts. |

**Commission reminder:** the 0.62 default is a **micro** rate (MNQ, MES, MGC). For **NQ, ES or GC**,
enter your broker's full-size rate, usually about 2.00–2.50 per side.
