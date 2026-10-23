# Risk and system events

| Time (UTC) | Event | Impact | Action |
|---|---|---|---|
| 2026-10-21 02:42 | Inspection: paper account verified, $99.98 equity, shorting disabled, live API refuses the keys | none | recorded in README |
| 2026-10-21 02:45 | Alpaca docs unreachable (MCP docs 403, docs.alpaca.markets not resolvable) | PDT and fractional-bracket rules unverified | verify with the first small paper order |
| 2026-10-21 02:45 | Real-time SIP data denied (403); IEX only | thinner real-time bars | trade on IEX, as researched |
| 2026-10-21 13:32 | session start (paper): equity 99.98, buying power 99.98, shorting off |  |  |
| 2026-10-21 13:34 | Watchlist had only stocks priced above the $99.98 buying power (MU, QQQ, NVDA, META, SPCX, TSLA, SNDK, AAPL): nothing could be sized | no trades possible from 09:32 | screener now skips stocks above buying power; session restarted; old list kept as watchlist_2026-10-21_unaffordable.json |
| 2026-10-21 13:34 | session start (paper): equity 99.98, buying power 99.98, shorting off |  |  |
| 2026-10-21 13:35 | Session on the old account (PA3L67J2X, $99.98) stopped: owner installed new API keys, which only reach new sessions | no trades were placed on the old account today | trading continues in a new session with the new keys |
| 2026-10-21 13:36 | New keys verified: paper account PA3PX6CUDFOF, equity $100,000, buying power $400,000, shorting enabled; market open, no positions, no open orders | sizing no longer limited by account size; shorts possible | old-account watchlist and state deleted; session relaunched to screen with the new buying power |
| 2026-10-21 13:36 | session start (paper): equity 100000, buying power 400000, shorting on |  |  |
| 2026-10-21 14:24 | Container restarted (uptime 16 s); session process gone, last state write 13:43 | no trading 13:43–14:25 | Alpaca reconciled: no positions, no orders; session relaunched (unbuffered output) |
| 2026-10-21 14:24 | session start (paper): equity 100000, buying power 400000, shorting on |  |  |
| 2026-10-21 15:00 | Container restarted again (uptime 14 s); bot last wrote state 14:35:54, about 5 min after the conversation went idle | no setup scanning or management ~14:36–15:00; NVDA short protected by its Alpaca stops (222.20) and take profits | Alpaca reconciled (NVDA −230, 3 brackets live, nothing else); session relaunched from saved state |
| 2026-10-21 15:00 | session start (paper): equity 99615.9, buying power 337677.36, shorting on |  |  |
| 2026-10-21 15:00 | start reconcile unavailable: GET /v2/orders?status=all&nested=true&limit=500&after=2026-10-21T04:00:00+00:00: HTTP 422: {"code":40010001,"message":"invalid format for after; format: '2006-01-02T15:04:05Z'"} | instrument cap from saved state only |  |
| 2026-10-21 15:01 | position NVDA -230 at Alpaca is not in the saved state | not managed by this session (its bracket stop and take profit stay live at Alpaca) | closed at flatten; reconcile in the review  **False alarm:** written by a manual test of the reconcile fix, which ran without loading the saved state; the session does manage NVDA |
| 2026-10-21 15:14 | Container restarted a third time (uptime 12 s); bot last wrote state 15:06:08 | no scanning or management ~15:06–15:15; NVDA protected at Alpaca | reconciled (NVDA −230, brackets live); relaunched |
| 2026-10-21 15:14 | session start (paper): equity 99616.45, buying power 337680.23, shorting on |  |  |
| 2026-10-21 15:16 | Bot relaunched as a session-tracked background task (test: does it keep the container from being reclaimed when the conversation is idle?) | a few seconds without management | watch whether state keeps updating while idle |
| 2026-10-21 15:16 | session start (paper): equity 99581.4, buying power 337497.96, shorting on |  |  |
| 2026-10-21 15:20 | Workflow trading-session merged to the default branch (PR #1); container bot stopped so only the GitHub Actions session trades | seconds without management; NVDA protected at Alpaca | GitHub Actions run started manually; scheduled runs every 15 min take over |
| 2026-10-21 15:20 | session start (paper): equity 99691.8, buying power 338072.04, shorting on |  |  |
| 2026-10-21 15:48 | session start (paper): equity 99488.26, buying power 284356.3, shorting on |  |  |
| 2026-10-21 19:55 | flattened before the close | open positions closed at market |  |
| 2026-10-21 19:55 | session end | 5 trades, 5 instruments | review to write |
| 2026-10-21 19:55 | **Flatten failed**: `DELETE /v2/positions?cancel_orders=true` cancelled every stop and take profit but closed nothing (the cancelled legs still held the shares); the bot logged "flattened" without checking, and marked the 5 trades closed with P/L $0 | NVDA, MU, SPCX, TSLA, AAPL held overnight with **no stops** (−$904 open at the close) | found 2026-10-22 15:13 UTC |
| 2026-10-21 20:20 | Daily review session couldn't reach the repo (fresh sessions have no repo attached, GH token invalid) and did nothing; it sent the owner a push about the open positions | no review for 2026-10-21 | review moved into the Claude session that holds the repo |
| 2026-10-22 | GitHub's scheduler didn't start the bot this morning: only 2 scheduled runs fired since 2026-10-21 (19:27 and 22:36 UTC), none 12:00–15:13 UTC today | no trading until 15:2x UTC | session started by hand; a daily start from the Claude session added |
| 2026-10-22 15:17 | Owner chose to close all 5; closed at market: NVDA +$1,223.60, MU −$1,888.82, SPCX +$707.77, TSLA +$108.01, AAPL −$27.54 = **+$123.02**; equity $100,121.47; verified flat, no open orders | the overnight result was luck: at the 2026-10-21 close these were −$904 | flatten fixed (cancel → wait until no open orders → close each → verify, retry; exits recorded only when Alpaca holds nothing); corrected exit records appended to trades.jsonl; trade pages annotated |
| 2026-10-22 15:19 | session start (paper): equity 100121.47, buying power 400485.88, shorting on |  |  |
| 2026-10-22 19:55 | session end | 3 trades, 6 instruments | review to write |
| 2026-10-23 13:22 | session start (paper): equity 99835.19, buying power 399340.76, shorting on |  |  |
| 2026-10-23 14:32 | session start (paper): equity 99792.73, buying power 281000.65, shorting on |  |  |
| 2026-10-23 14:32 | position AMD 19 at Alpaca is not in the saved state | not managed by this session (its bracket stop and take profit stay live at Alpaca) | closed at flatten; reconcile in the review |
| 2026-10-23 14:32 | position INTC 114 at Alpaca is not in the saved state | not managed by this session (its bracket stop and take profit stay live at Alpaca) | closed at flatten; reconcile in the review |
| 2026-10-23 14:32 | position IWM -36 at Alpaca is not in the saved state | not managed by this session (its bracket stop and take profit stay live at Alpaca) | closed at flatten; reconcile in the review |
| 2026-10-23 14:32 | position SPCX 67 at Alpaca is not in the saved state | not managed by this session (its bracket stop and take profit stay live at Alpaca) | closed at flatten; reconcile in the review |
