# Day 7 — Individuality

Source: TJR Boot Camp, Day 7: Individuality (https://www.youtube.com/watch?v=_6voYEdi5j4, 18:46).
Watched by Gemini (`scripts/gemini_watch.py`) because YouTube blocks downloads here; the
full transcript and screen log are in `sources/day07_individuality.md`. The screen is a
static US Dollar Index weekly chart throughout, so the transcript carries the lesson.
Study: `tradingbot/session_study.py`.

A mindset day. Most of it is about people (wear what you like, voice your opinion, don't
compete with friends). Four ideas carry over to the bot.

## What the lesson teaches, and what it becomes for a bot

### 1. A strategy is simple concepts plugged into an execution order (04:45–05:56)
- "My strategies are all just based off of simple concepts, plugging them into an execution order, and then taking the trade."
- Use the pieces you understand: if liquidity and break of structure click but fair value gaps and order blocks don't, "those two in itself you can take a trade off of".
- **Bot rule:** the strategy will be built from separate components (candle reads, trend, break of structure, and later liquidity, fair value gaps, order blocks), each of which can be switched on or off. "What works for you" becomes measurable: the learning loop tests removing one component at a time and keeps it only if it earns its place (H12).

### 2. Not law: adapt to what works for you (06:00–08:55)
- "There's a million ways to trade ... Don't think that this strategy is so locked down." "Not, 'Oh, TJR said this, so this is law.'"
- **Bot rule:** this is how the bot already separates rules from settings. Things TJR states as absolutes (closed candles only, never trade against the higher timeframe) stay locked as the starting point. Everything else is a setting the bot tests on its own markets and keeps or changes on evidence.

### 3. Find your own edge by watching the same thing every day (06:55–07:25)
- TJR's Forex edge came from watching GBPJPY every London session and noticing that "right when London session opens, it just goes super strong in one direction, but then immediately flips direction". He calls it the London session fakeout, and it was his introduction to liquidity sweeps.
- **Bot version:** the bot trades US stocks, not GBPJPY, so it asked the same question of its own market: does the New York open (9:30 ET) fake out on SPY and GLD?

### 4. Compete with yourself only (08:55–09:35)
- "This is a race between yourself." Everyone's learning curve is different; comparing with others messes up your psychology.
- **Bot rule:** the bot only ever compares a change against its own previous baseline.

## First study: does the New York open fake out? (2026-10-20)

`python -m tradingbot.session_study SYMBOL --days 730 --open-minutes N`. About 480 sessions
each over two years. A "fakeout" here means the session closed on the other side of the
open from where the first N minutes went.

| | First 15 minutes | First 30 minutes |
|---|---|---|
| SPY, all days | 36.5% fakeout | 32.9% |
| SPY, largest third of opening moves | 31.3% | 23.3% |
| GLD, all days | 41.8% | 37.8% |
| GLD, largest third of opening moves | 30.4% | 26.6% |

What the bot takes from this:
- **TJR's London fakeout does not carry over to the New York open on SPY or GLD.** The opposite happened: the first move held to the close about 60–75% of the time, and more often when it was large. That's the lesson of the day in action: his market's behavior isn't law for the bot's market.
- **Caution:** part of this is mechanical. A large early move gives the close a head start in that direction, so "large moves hold more often" is partly expected. The measure also misses TJR's real pattern: a strong move that flips quickly and *then* runs. Liquidity sweeps (Days 8–12) will give a sharper test (H11).

## Provenance audit (2026-10-20)

- **[TJR]** Strategy = simple concepts plugged into an execution order; use the pieces you understand; not law; find your own edge by observation; compete with yourself.
- **[Bot]** The New York open study is the bot's own experiment inspired by TJR's London-session observation; TJR made no claim about the New York open.
