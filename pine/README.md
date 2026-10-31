# NOWICK Backtester: no-wick candle levels (Pine Script v6)

`day_trading_backtester.pine` is a TradingView strategy that finds **no-wick candles**, draws a
level from each one, and trades the **close through and close back** of that level. It only takes
setups when price has real momentum, not while it is consolidating.

It runs on a **3-minute chart** of **MNQ, ES, MGC or GC**, one instrument per chart. Commission and
slippage are modelled realistically, and the results are shown in a table on the chart.

---

## 1. Adding it to a chart

1. Open a chart of `MNQ1!`, `ES1!`, `MGC1!` or `GC1!` and set the timeframe to **3m**. If the chart
   has a **B-ADJ** (back-adjust) toggle, turn it off.
2. In the **Pine Editor**, create a new script (**script name ▸ Create new ▸ Strategy**). Delete
   the template code and paste in the whole file.
3. Click **Save**, then **Add to chart** (▶). Don't click **Publish**, which posts the script
   publicly.
4. In the Strategy Tester, set the **date range** to the longest one available, and set the
   **initial capital** to your account size.
5. Under **Inputs ▸ Costs**, enter your broker's commission.

On the **free TradingView plan**:
- leave "High detalization" / bar magnifier **off**, because it is a paid feature and causes a
  runtime error;
- expect only about two weeks of 3-minute history.

---

## 2. What you see on the chart

| Mark | Meaning |
|---|---|
| Red **▼ NW** above a candle | Bearish no-wick candle that **created a level** (momentum was bearish). |
| Teal **▲ NW** below a candle | Bullish no-wick candle that **created a level** (momentum was bullish). |
| Grey **×** | No-wick candle **ignored**: price was consolidating, momentum pointed the wrong way, or the candle was outside the trading window. |
| Thin line from the candle | Active level. |
| Line turns **thick and dashed** | Price has closed through the level. The level is now *armed*, waiting for the close back. |
| Grey dotted line | Level finished: used, or expired. |
| **Red box** | Risk zone, from entry to the stop-loss. The label shows the SL price and its distance in ticks. |
| **Green box** | Reward zone, from entry to the take-profit. The label shows the TP price and the R multiple. |
| White line + "Entry" label | Entry. It starts at the signal close ("Entry ~") and moves to the real fill price on the next bar. |
| Label at the exit | How the trade ended (`TP`, `SL`, `EOD`, `DLL`), plus the net result in currency and in R. |
| Light green / red background | Momentum is bullish / bearish. **No tint means consolidating**, so no setups are taken. |

TradingView's own entry and exit arrows also appear, labelled `NOWICK L` / `NOWICK S` for entries
and `TP` / `SL` / `EOD` for exits.

You can set up **alerts** using Alert ▸ Condition: this strategy ▸ "alert() function calls only".
An alert fires when a level is created and when a trade is entered.

---

## 3. The rules

These are written for a **short**. A long is the mirror image: a bullish candle with no bottom wick
makes a level at its low.

1. **Momentum.** Over the last *Look-back window* minutes (default 30, so 10 bars on a 3m chart),
   two things must both be true:
   - Price has moved **down by at least X × ATR**, measured as the close now minus the close at the
     start of the window.
   - It got there fairly directly. **Efficiency** is the net move ÷ the total distance price
     travelled, and must be ≥ the minimum (default 0.35).

   If either check fails, the market counts as **consolidating** and the no-wick candle is ignored.
2. **Level.** A bearish candle where `high − open ≤ wick tolerance` (default 0 ticks), formed while
   momentum is bearish, creates a level at its high.
3. **Trigger.** Price must **close above** the level and then **close back below** it. The short is
   sent on that close and fills at the next bar's open.
   - The trade is **skipped if momentum has turned bullish** by then.
   - If you turn on "Require momentum still strong at entry", momentum must still be bearish and
     pass both checks.
4. **Stop-loss.** This is the **previous candle's high**.
   - If that is closer than the *Minimum stop distance*, the stop moves to **the high of the candle
     before it**.
   - With *Candles to look back* above 2, it keeps stepping back one candle at a time.
   - If no candle gives a stop far enough away, the trade is skipped.
5. **Take-profit** is placed at **R multiple × risk** (default 2R).
6. **Level lifetime.** A level is removed after *N* bars (default 20) or on its first close back,
   whether or not a trade was taken. If several levels trigger on the same bar, the newest one is
   used.
7. **Position limits.** Only one position is held at a time. Trades are only taken inside the
   trading window, and everything is closed at the flatten time.

---

## 4. Inputs

### No-wick setup
| Input | Default | What it does |
|---|---|---|
| Wick tolerance (ticks) | 0 | How big a wick is still counted as "no wick". |
| Level expires after (bars) | 20 | How long a level stays active. |
| Take profit (R multiple) | 2.0 | Target as a multiple of the stop distance. |
| Trading window (ET) | 09:30–15:45 | Levels are created, and trades taken, only inside this window. |

### Stop loss
| Input | Default | What it does |
|---|---|---|
| Minimum stop distance (ticks) | 8 | Stops closer than this are not allowed. MNQ/ES: 8 ticks = 2 points. MGC/GC: 8 ticks = $0.80. |
| Candles to look back for the stop | 2 | 1 = previous candle only. 2 = previous candle, then the one before it. Higher = keep stepping back. |
| Stop buffer (ticks) | 0 | Extra ticks beyond the candle's high or low. |

### Momentum (no trades while consolidating)
| Input | Default | What it does |
|---|---|---|
| Look-back window (minutes) | 30 | 15–30 is the range you asked for. On a 3m chart, 15 = 5 bars and 30 = 10 bars. |
| Minimum net move (× ATR) | 1.0 | How far price must have travelled over the window. Raise it to be stricter. |
| Minimum directional efficiency (0–1) | 0.35 | How "one-way" the move must be. Raise it to filter out more chop. |
| ATR length (bars) | 14 | Volatility yardstick for the net-move test. |
| Require momentum still strong at entry | off | Off: entry is only blocked if momentum turned the other way. On: momentum must still pass both checks. |

The background tint shows what the filter sees. If grey × marks appear on candles you would have
traded, the filter is too strict for your taste; if setups are being taken in obvious ranges, it
is too loose. Adjust the two thresholds accordingly.

### Day trading rules
| Input | Default | What it does |
|---|---|---|
| Contracts per trade | 1 | — |
| Trading day starts (ET) | 09:30 | Daily reset for the loss limit and for the levels. Use 08:20 for gold if you trade the COMEX open. |
| Flatten all at (ET) | 15:55 | Any open position is closed at the next bar's open after this time. |
| Daily loss limit | off / 500 | Adds realised net P&L today to the estimated open P&L. If that reaches −limit, the position is closed and trading stops until the next day. |

### Costs: the stress-test panel
| Input | Default | What it does |
|---|---|---|
| Commission per contract per side | 0.62 | Your all-in rate, charged on entry and exit. |
| Slippage per fill (ticks) | 1 | Charged on every market/stop fill. |
| Apply slippage to take-profit fills too | on | TradingView never slips limit orders; this charges slippage on TP exits as well. |
| Require trade-through / distance | on / 1 tick | A take-profit only counts once price trades this far beyond the target. |
| Slippage set in Properties (ticks) | 1 | **Must equal** Settings ▸ Properties ▸ Slippage. |

### Display
Each element can be switched on or off: the table and its corner, no-wick marks, filtered marks,
level lines, trade boxes and the momentum tint.

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
| Bar magnifier / "High detalization" | Off on the free plan. **On** if your plan allows it. |

---

## 6. The results table

The table has columns for **Longs**, **Shorts** and **All**. It only counts closed trades and
re-prices each one using the Costs inputs:

- **Gross P&L** is the result at frictionless prices. The Tester's own slippage is removed, and
  take-profit fills are moved back to the target.
- **Costs** = commission × 2, plus slippage on each fill.
- **Net P&L** = gross − costs. Win rate, profit factor, expectancy, average win/loss, R and
  drawdown are all calculated on net.
- **Tester net profit (ref.)** is TradingView's own figure. It is usually a little higher than the
  table's, because the Tester fills take-profits beyond the target without slippage.

Two rows below the main table:

- **Setups funnel.** It counts how many no-wick candles appeared, how many were filtered out as
  consolidation, how many became levels, how many closed back through, and how many were traded.
  It also shows why setups were skipped: stop too tight, momentum flipped, or position open /
  outside hours. Use it to see what each rule is doing.
- **Costs line.** It shows the cost settings the run used.

---

## 7. Known limitations

Each place where TradingView's fill assumptions could be optimistic is marked
`⚠ FILL ASSUMPTION` in the code.

- **Stop and target inside the same bar.** Without the bar magnifier (a paid feature), TradingView
  guesses the price path inside the bar, which can turn losers into winners. On the free plan,
  treat trades that open and close within one or two bars with suspicion.
- **Limit fills.** A take-profit is assumed to fill completely once price trades through it by the
  set number of ticks.
- **Stop slippage is a fixed number of ticks.** Real stops at the open or during news can slip
  more. Stress-test with 2–4 ticks.
- **Planned vs actual entry.** The stop and target are calculated from the signal close, but the
  trade fills at the next open. The "Avg R achieved" row reflects the real fill.
- **Daily loss limit** is only checked on bar closes.
- **Early-close days** are detected using TradingView's session calendar. Check trades on holidays.
- **Sample size.** On the free plan, about two weeks of data gives only a handful of trades. Don't
  tune the settings to that; you need 100+ trades before the numbers mean much.
- **Untested.** I couldn't compile this script myself, so reconcile a few trades by hand against
  the chart and paper-trade before risking money.
