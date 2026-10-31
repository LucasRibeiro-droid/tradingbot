# Day Trading Backtester: ORB + NOWICK (Pine Script v6)

`day_trading_backtester.pine` is a TradingView strategy that backtests two intraday futures
strategies on a 3-minute chart: **ORB** (opening range breakout + EMA20 retest) and **NOWICK**
(no-wick candle levels with a momentum filter). It is built to work on **MNQ, ES, MGC and GC**,
one instrument per chart.

Its main job is to model costs realistically. Commission and slippage are charged on every fill,
take-profits can be slipped too, and a take-profit can be made to count only once price trades
*through* the target. Results are reported per strategy and combined, in a table on the chart.

---

## 1. Adding it to a chart

1. Open a chart of the instrument, for example `CME_MINI:MNQ1!`, `CME_MINI:ES1!`,
   `COMEX_MINI:MGC1!` or `COMEX:GC1!`, and set the timeframe to **3 minutes**.
2. Use **regular (non-adjusted) continuous** data. Back-adjusted contracts shift historical prices,
   which distorts tick-based costs and every price level.
3. Open the **Pine Editor** at the bottom of the screen, delete what's there, and paste the whole
   contents of `day_trading_backtester.pine`.
4. Click **Save**, then **Add to chart**.
5. Open the strategy's **Settings**:
   - Set the **Properties** tab as described in section 3.
   - Set the **Inputs** tab as described in section 2. In particular, set your broker's commission
     in **Costs**.
6. Read the results from the **table on the chart**. The Strategy Tester's own numbers are only
   a reference (see section 4).

For gold, change **NY open** to the time your opening range should start, for example 08:20 for
the COMEX pit open or 09:30 to use the equity open. Also review the ORB cut-off, the NOWICK window
and the flatten time.

---

## 2. Inputs

### General

| Input | Default | What it does |
|---|---|---|
| Enable ORB strategy | on | Turns Strategy 1 on or off. The ORB *bias* is still calculated when ORB is off, because the NOWICK momentum filter option (c) uses it. |
| Enable NOWICK strategy | on | Turns Strategy 2 on or off. |
| Allow ORB and NOWICK positions at the same time | off | **Off:** one position at a time. If both strategies signal on the same bar, ORB is taken. **On:** each strategy may hold one position, but only in the **same direction**. A TradingView strategy has a single net position, so a NOWICK short would close an ORB long instead of coexisting with it. Opposite-direction signals are therefore skipped. |
| Contracts per trade | 1 | Fixed size for every entry. |
| NY open (ET) hour / minute | 09:30 | Starts the trading day. It anchors the opening range, the 15-minute breakout candles, the NY-anchored VWAP and the daily resets. |
| Fast EMA length | 20 | Used for the ORB retest and as the fast line of the NOWICK EMA momentum filter. |
| Slow EMA length | 50 | Slow line of the NOWICK EMA momentum filter. |
| Swing pivot left / right bars | 3 / 3 | Swing highs and lows come from `ta.pivothigh` / `ta.pivotlow`. A pivot only becomes usable *right bars* after it prints, so there is no look-ahead. |
| Max swing age (bars) | 100 | Swing points older than this are ignored when choosing a stop. |
| Stop buffer (ticks) | 0 | Extra ticks placed beyond the swing point or candle used as the stop. |

### Strategy 1: ORB

| Input | Default | What it does |
|---|---|---|
| Opening range length (minutes) | 30 | The range is the high and low from NY open to NY open + this many minutes. |
| Breakout candle timeframe (minutes) | 15 | Breakout candles are built from chart bars and anchored to the NY open (10:15, 10:30, …). The first one to **close** outside the range sets the day's bias, which stays fixed for the rest of the day. |
| Minimum reward:risk | 1.0 | The trade is skipped if `|target − entry| / |entry − stop|` is below this. It is measured from the signal close. |
| Max ORB trades per day | 1 | — |
| No new ORB entries after | 12:00 | The cut-off for new ORB entries, measured on the signal bar's close. |
| Target uses overnight (Globex) high/low | off | **Off:** "day's high/low so far" is measured from the NY open. **On:** it is measured from the 18:00 ET Globex open. |

**ORB logic**
1. The bias is set by the first breakout candle that closes outside the range.
2. Starting on the *next* bar, a long needs a 3m close **below** EMA20, then a later 3m close
   **above** it. The entry signal is that close. Shorts are the mirror image.
3. The sequence restarts after every reclaim, whether or not a trade was taken.
4. The stop is the most recent confirmed swing low **below** entry (swing high above entry for
   shorts).
5. The target is the day's high so far (day's low for shorts), fixed at the moment of entry.
6. The trade is skipped in any of these cases:
   - there is no valid swing point;
   - the target is not beyond entry;
   - the reward:risk is below the minimum;
   - it is past the cut-off time;
   - the daily trade limit is reached;
   - a position is blocking the entry.

### Strategy 2: NOWICK

| Input | Default | What it does |
|---|---|---|
| Momentum filter | Fast EMA vs slow EMA | (a) EMA20 above/below EMA50; (b) price above/below VWAP; (c) the ORB bias direction. A flat EMA or no bias yet means no trades. |
| VWAP anchor | NY open | **NY open:** the VWAP resets at the NY open input. **Exchange session:** TradingView's `ta.vwap`, which resets at the 18:00 ET Globex open. |
| Momentum must also agree when the level is created | on | When on, a bearish level is only created while momentum is bearish (bullish levels likewise). Momentum is **always** re-checked at entry. |
| Wick tolerance (ticks) | 0 | A bearish candle counts as "no top wick" if `high − open ≤` this. A bullish candle counts as "no bottom wick" if `open − low ≤` this. |
| Level expires after (bars) | 20 | A level is removed after this many bars, or on its first close back through the level, whether or not that close was traded. |
| Take profit (R multiple) | 2.0 | Target = entry ± R × risk. |
| Minimum stop distance (ticks) | 8 | If the previous candle's high/low is closer than this, the most recent swing high/low beyond entry is used instead. If that is also too close, or doesn't exist, the trade is skipped. |
| NOWICK trading window (ET) | 09:30–15:45 | Levels are created, and trades taken, only inside this window. |

**NOWICK logic.** For a short:
1. A bearish no-top-wick candle creates a level at its high.
2. Price must then **close above** the level, then **close back below** it.
3. The short is entered on that close back below, but only if momentum is still bearish.
4. The stop is the previous candle's high, or the swing-high fallback described above.
5. The target is 2R.

Longs are the mirror image. Several levels can be active at once. If several trigger on the same
bar, the newest level is used and the others are retired. Active levels are drawn as lines, and
retired ones turn grey and dotted.

### Day trading rules

| Input | Default | What it does |
|---|---|---|
| Flatten all at | 15:55 ET | On the close of the first bar that ends at or after this time, everything is closed with a market order. It fills at the next bar's open plus slippage. No new entries are taken from then on. |
| Use daily loss limit / amount | off / 500 | Adds realised net P&L today to the estimated open P&L after costs. If that reaches −amount, everything is flattened and trading stops until the next NY open. A red background marks halted days. |

On days when TradingView's session calendar shows the exchange closing before the flatten time
(holiday early closes), any open position is closed at the last bar's close.

### Costs: the stress-test panel

| Input | Default | What it does |
|---|---|---|
| Commission per contract per side | 0.62 | Your all-in rate: commission + exchange + NFA + clearing. It is charged on entry **and** exit. Typical retail all-in rates are roughly 0.50–1.00 for micros and 2.00–3.00 for minis. |
| Slippage per fill (ticks) | 1 | Charged against you on every market/stop fill: entries, stop-losses, EOD and loss-limit exits. |
| Apply slippage to take-profit (limit) fills too | on | TradingView never slips limit orders. With this on, the slippage is charged on take-profit exits as well. |
| Require price to trade THROUGH the target / distance | on / 1 tick | A take-profit only counts as filled once price trades this many ticks beyond the target. This models your place in the queue at the limit price. |
| Slippage set in Properties (ticks) | 1 | **Must equal** Settings ▸ Properties ▸ Slippage. The script uses it to strip the Tester's own slippage from its fill prices before applying yours. |

**To stress-test, change only these inputs**, for example slippage 1 → 2 → 3 or commission ×1.5.
The table recalculates on the spot. You don't need to touch Properties, as long as "Slippage set in
Properties" still matches the Properties tab.

### Display

These inputs toggle the results table and its corner, the opening range lines, the EMAs, the
NOWICK level lines, and the stop/target lines of open trades.

---

## 3. Strategy Tester "Properties" to match

| Property | Set to | Why |
|---|---|---|
| Initial capital | Your real account size (default 50,000) | Max drawdown % is measured against it. |
| Base currency | Default / USD | — |
| Order size | Anything | Ignored, because the script sends `qty = Contracts per trade`. |
| Pyramiding | **2** | Required for "Allow both". With it off, the script blocks the second entry itself. |
| Commission | Cash per contract, your rate | Only affects the Tester's own reference numbers. The table uses the Costs input. |
| Verify price for limit orders | **0 ticks** | The script applies its own trade-through. Setting this as well would double-count it. |
| Slippage | **Same as "Slippage set in Properties"** (default 1) | Lets the table remove it and apply your slippage instead. |
| Margin for long / short | **0 %** | Turns off TradingView's margin-call simulation, which would wrongly liquidate futures positions. |
| Recalculate: after order is filled / on every tick | **Off / Off** | Signals are calculated on confirmed bar closes only. |
| Fill orders: using bar magnifier ("High detalization" in the newer tester) | **On if your plan allows it** | Off by default in the script, because the free plan throws a runtime error ("upgrade for higher bar detalization") when it is on. On a paid plan, turn it on: it makes stop/target-in-the-same-bar fills far more trustworthy. See the limitations below. |
| Fill orders: on bar close | **Off** | Off is realistic: entries fill at the next bar's open. Turning it on fills at the signal close, which is optimistic, so use it only for comparison. |
| Fill orders: using standard OHLC | On | Only matters on non-standard chart types such as Heikin Ashi. |

All of these except the bar magnifier are already set as defaults in the `strategy()` call. You only need to check them if
you've changed something.

---

## 4. How the results are calculated

The **table** on the chart is the realistic ledger. It reads every closed trade
(`strategy.closedtrades.*`), splits it by `entry_id()` ("ORB" / "NOWICK"), and re-prices it:

1. **Gross P&L** is the trade at frictionless prices:
   - the Tester's slippage is removed from the entry and from every market/stop exit;
   - take-profit fills are moved back from *target + trade-through* to the target.
2. **Costs** are:
   - `2 × commission × contracts`, plus
   - `slippage ticks × tick value × contracts` for each slipped fill: the entry, plus the exit
     (a take-profit exit only counts if "apply to TP" is on).
3. **Net P&L** is gross minus costs. Win rate, profit factor, expectancy, average win/loss and
   drawdown all use **net** figures.
4. **R achieved** is net P&L ÷ initial risk, where risk = |entry fill (including your slippage) −
   stop| × contracts × point value.
5. **Max drawdown** is measured on closed-trade net equity, separately for each column.
6. **Avg trades / day** is trades ÷ the number of NY sessions on the chart.
7. **Tester net profit (ref.)** is TradingView's own figure. It is usually *higher* than the
   table's net, because the Tester fills take-profits at target + trade-through and never slips
   them.

Tick size and tick value come from `syminfo.mintick` and `syminfo.pointvalue`. For reference:
MNQ 0.25 = $0.50, ES 0.25 = $12.50, MGC 0.10 = $1.00, GC 0.10 = $10.00.

---

## 5. Known limitations and where the backtest can still flatter you

Every place in the code where TradingView's fill assumptions could be optimistic is marked
`⚠ FILL ASSUMPTION`. In summary:

- **Stop and target inside the same bar.** Without lower-timeframe data, TradingView guesses the
  intrabar path. It assumes price went first to whichever extreme is closer to the open, which can
  turn a loser into a winner.
  - The bar magnifier replays the bar on lower-timeframe data, which fixes most cases. It still
    has to guess when both levels sit inside one *lower-timeframe* bar.
  - The magnifier only reaches back as far as the lower-timeframe history does. Older bars silently
    fall back to the OHLC guess, so treat the early part of a long backtest with more suspicion.
  - In the List of Trades, look for trades that open and close within one or two bars with a wide
    range.
- **Exit orders on the entry bar.** The stop and target become active on the bar where the entry
  fills. That's correct, but it is exactly where the bar's intrabar path matters most.
- **Limit fills.** Even with trade-through, a limit is assumed to fill completely, with no partial
  fills and no queue modelling beyond the X ticks.
- **Stop slippage is a fixed tick count.** Real stops during news or the 09:30 open can slip far
  more. Stress-test with 2–4 ticks. Gaps are filled at the open, which is realistic.
- **R:R and 2R targets are calculated from the signal close**, while the entry fills at the next
  open. The achieved R in the table reflects the real fill.
- **The daily loss limit is checked on bar closes only.** A fast move inside a bar can push the
  real loss beyond the limit. The open-P&L part of the check is an estimate.
- **The table only covers closed trades.** It updates on the last bar and ignores an open position.
  Max drawdown is closed-trade only, so the intrabar drawdown the Strategy Tester reports can be
  deeper.
- **Breakout-candle closes are built from chart bars.** If the exchange printed no bar in a
  bucket's final 3-minute slot, that bucket's close is skipped rather than guessed. This is rare on
  these contracts.
- **Early-close days** are detected using TradingView's session calendar (`session.islastbar`).
  If it misses a holiday schedule, a position could be held into the next session. Check trades on
  holidays.
- **Continuous contracts and rolls.** A trade won't span a roll because everything is flattened
  each day. Pick unadjusted data so prices match what actually traded.
- **One instrument per chart.** "Combined" means ORB + NOWICK on this chart only, not a
  multi-instrument portfolio.
- **Opposite-direction positions can't coexist.** This is a TradingView single-net-position
  limitation; see "Allow both".
- **No volume or liquidity limits.** These matter for large GC/ES size.
- **The strategy is not compiled or validated against live data by this repository.** Always
  reconcile a sample of trades by hand against the chart, and paper-trade before risking capital.
