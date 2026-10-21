# tradingbot

A self-improving trading bot for Alpaca paper trading, learning one methodology from TJR's
56-video bootcamp.

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

- Indicators: `tradingbot/candles.py`, `trend.py` (trend, break of structure), `liquidity.py`, `fvg.py`, `orderblocks.py`.
- `tradingbot/decision.py` is a **test harness** for combining indicators. It contains [Bot] placeholders (entry, stop) until the lessons that teach them are learned.
- Tests: `python -m unittest discover -s tests -t .`
- Settings are versioned in `tradingbot/config.py`; `LOCKED` holds rules TJR states as absolutes.
- Alpaca keys: `ALPACA_API_KEY`, `ALPACA_SECRET_KEY` (paper account).
