# Helix — trading front end

A recreation of a perpetuals-style trading UI (chart, market picker, long/short order
ticket with a multiplier, positions/orders/history) as a static web app with no build step.

## Run

```bash
cd web && python3 -m http.server 8000
```

Then open http://localhost:8000. Opening `index.html` directly also works.

## What works

- **Live chart**: line or candle view over Live (past minute), 1D, 1W, 1M and 1Y, with hover
  crosshair, a current-price marker, and lines for your entries, auto-close levels and limit orders.
- **Prices**: crypto markets use Hyperliquid's public API (mids, 24h stats, candles) when reachable;
  everything else, and crypto when offline, runs on a random-walk simulator.
- **Market picker**: category tabs, favourites (★), Names/Tickers toggle, sortable columns, and
  search with the `/` shortcut, arrow keys and Enter.
- **Order ticket**: Long/Short, Market or Limit, amount shortcuts, a 1×–max multiplier slider,
  optional take-profit/stop-loss, a "what if the price moves X%" calculator, estimated auto-close
  price, position size and fee.
- **Paper account**: $1,000 starting balance (top up with Deposit), positions with live PnL and Close,
  limit orders that fill when the price crosses, TP/SL and auto-close triggers, and trade history.
  State is saved in `localStorage`; reset it from the avatar menu.
- **Pages**: Markets (with 24h sparklines), Social (simulated trade feed and leaderboard),
  Portfolio (balances, equity chart, positions, orders, history) and Referrals.
- **Pro**: toggles a simulated order book under the ticket.

Fees: 0.045% of notional per side, plus a 0.02% half-spread on market orders. A position auto-closes
when losses reach 90% of its amount.
