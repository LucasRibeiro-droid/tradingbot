# tradingbot

A self-improving trading bot for Alpaca paper trading. It learned TJR's 56-video bootcamp as
its **baseline**, and now learns from its own trades to become as profitable as it can.

**Owner's direction (2026-10-21, widened 2026-10-22):** TJR's methodology is the foundation,
not a rulebook. The priority now is to **learn through many well-documented paper trades**:
every trade tests a hypothesis or applies an identifiable approach, is recorded before entry
(expectation, invalidation, uncertainty) and reviewed after (decision quality vs outcome).
The baseline (TJR model 1 + TJR's exits) keeps trading as the reference; experiments trade
beside it. Change one thing at a time, check it out of sample, keep conclusions proportional
to the evidence, and record every change in `journal/trading/rule_changes.md`. Full text:
`journal/DIRECTIVE_2026-10-22.md`; protocol: `journal/trading/README.md` ("How the bot learns").

## Trading records (the owner reads these)

- `journal/trading/TRADES.md`: index of every trade; each links to a page in
  `journal/trading/trades/` with why the bot took it, the plan, the result, and what it learned.
- `journal/trading/reviews/`: daily reviews; `performance.md`, `lessons.md`, `events.md`.
- Live engine: `tradingbot/live/` (`run.py` session, `signals.py` TJR assessment, `experiments.py`
  strategies/exits under test and the pre-trade record, `screener.py`, `broker.py` paper-only
  client, `replay.py` and `lab.py` (strategies × exits with costs) to test on history).
- **The session runs on GitHub Actions** (`.github/workflows/trading-session.yml` on the default
  branch; every 15 min on weekdays, one run at a time, journal pushed here every 2 min). Claude
  containers are shut down minutes after a conversation goes idle, so **don't start the bot in a
  Claude session**; check the Actions run instead, and start one with `run_workflow` if none is running.

## Before working on a bootcamp lesson

Read `knowledge/LEARNING_PROTOCOL.md` and follow it. Then read `knowledge/methodology.md`
(the cumulative knowledge base) and `knowledge/course_map.md` (what has been learned so far).

Key points:
- The lessons are parts of **one** methodology, not separate strategies.
- Tag every rule **[TJR]** (with a timestamp), **[Inferred]**, or **[Bot]**.
- Multi-part topics stay open until their last part is learned.
- Don't turn incomplete teaching into executable rules; document the ambiguity.

## Getting lesson content

- YouTube blocks downloads from cloud sessions. Uploaded video files work.
- Uploaded video with audio: `python scripts/transcribe_local.py VIDEO --out knowledge/sources/dayNN.md --model-dir DIR` (offline Whisper via sherpa-onnx; model from the sherpa-onnx GitHub `asr-models` release).
- YouTube link only: `python scripts/gemini_watch.py URL --out knowledge/sources/dayNN.md --model gemini-3.5-flash` (needs `GEMINI_API_KEY`).
- Captions already pasted: add `--screen-only` so Gemini only describes the screen and quotes the speech at each entry; check those quotes against the captions. Its timing is reliable; its box/price details are not, so ask the owner for screenshots at exact timestamps. Free quota is ~20 requests/day per model; `gemini-3-flash-preview` works when `3.5-flash` is exhausted.
- Look at chart frames yourself with ffmpeg at the timestamps where TJR points or draws.

## Code

- Indicators: `tradingbot/candles.py`, `trend.py` (trend, break of structure), `liquidity.py`, `fvg.py`, `orderblocks.py`, `equilibrium.py`; exits in `exits.py` (Days 37, 38).
- `tradingbot/models_study.py` runs TJR's four entry models (Days 30–33) on the same setups.
- `tradingbot/decision.py` is a **test harness** for combining indicators. It contains [Bot] placeholders (entry, stop) until the lessons that teach them are learned.
- Tests: `python -m unittest discover -s tests -t .`
- Settings are versioned in `tradingbot/config.py`; `LOCKED` holds TJR's absolutes as the baseline reference; `TradingParams` holds the live settings, which may override them on evidence.
- Alpaca keys: `ALPACA_API_KEY`, `ALPACA_SECRET_KEY` (paper account).
