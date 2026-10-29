# Helix — trading front end

A recreation of a perpetuals-style trading UI (chart, market picker, long/short order
ticket with a multiplier, positions/orders/history) as a static web app with no build step.

## Run

```bash
python3 web/server.py
```

Then open http://localhost:8000. The server reads `ALPACA_API_KEY` and `ALPACA_SECRET_KEY` from the
environment (or a `.env` file in `web/` or the repo root) and proxies Alpaca market-data requests,
so the keys never reach the browser. Set `ALPACA_DATA_FEED=sip` if your plan includes SIP data
(the default is `iex`, the free feed). Opening `index.html` directly still works, but then only
the crypto markets get Alpaca data, because Alpaca serves crypto without keys.

## What works

- **Live chart**: line or candle view over Live (past minute), 1D, 1W, 1M and 1Y, with hover
  crosshair, a current-price marker, and lines for your entries, auto-close levels and limit orders.
- **Prices**: from Alpaca for the markets it covers: BTC, ETH, HYPE, SOL, XRP, DOGE, AVAX, LINK,
  GOOGL, NVDA, AAPL, TSLA, MSFT, AMZN, META and the SPY, QQQ, DIA, GLD, SLV and USO ETFs. Live price,
  24h change and volume come from snapshots every 3 seconds; 1D/1W/1M/1Y charts are Alpaca bars
  (5-minute, 30-minute, 4-hour and daily). Markets Alpaca doesn't carry (ZEC, BNB, SUI, SK Hynix,
  the pre-IPO names, index levels, futures, FX and yields) run on a random-walk simulator, and the
  About tab says which source a market uses.
- **Market picker**: category tabs, favourites (★), Names/Tickers toggle, sortable columns, and
  search with the `/` shortcut, arrow keys and Enter.
- **Order ticket**: Long/Short, Market or Limit, amount shortcuts, a 1×–max multiplier slider,
  optional take-profit/stop-loss, a "what if the price moves X%" calculator, estimated auto-close
  price, position size and fee.
- **Paper account**: $10 starting balance (top up with Deposit), positions with live PnL and Close,
  limit orders that fill when the price crosses, TP/SL and auto-close triggers, and trade history.
  State is saved in `localStorage`; reset it from the avatar menu.
- **Pages**: Markets (with 24h sparklines), Social (simulated trade feed and leaderboard),
  Portfolio (balances, equity chart, positions, orders, history) and Referrals.
- **Pro**: toggles a simulated order book under the ticket.

Fees: 0.045% of notional per side, plus a 0.02% half-spread on market orders. A position auto-closes
when losses reach 90% of its amount.
