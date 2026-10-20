# tradingbot

A self-improving trading bot for Alpaca (paper trading). It learns a strategy one lesson
at a time from the TJR Boot Camp, measures every rule against real price data, and
changes one variable at a time so each improvement can be traced to its cause.

- `knowledge/`: what the bot has learned, lesson by lesson
- `tradingbot/`: the code (`candles.py` for Day 2, `discipline.py` for Day 3, `trend.py` for Days 4 and 6, `forecast.py` for Day 4, `liquidity.py` for Days 8 and 10, `chart.py` to draw what the bot sees, `study.py` for the homework studies, `data.py` for Alpaca bars)
- `journal/`: study results, open hypotheses, forecasts and the daily journal

```
python -m unittest discover -s tests -t .           # tests
python -m tradingbot.study SPY --timeframe 1Day --days 2200   # Day 2 study (needs ALPACA_API_KEY / ALPACA_SECRET_KEY)
python -m tradingbot.trend_study SPY --htf 1Day --ltf 1Hour  # Days 4 and 6 study
python -m tradingbot.chart GLD --timeframe 1Day             # draw highs, lows, breaks and fakes (needs matplotlib)
python -m tradingbot.session_study SPY --open-minutes 15     # Day 7 study: does the New York open fake out?
python scripts/gemini_watch.py URL --out knowledge/sources/dayNN.md  # Gemini watches a lesson (needs GEMINI_API_KEY)
python scripts/transcribe_local.py VIDEO --out knowledge/sources/dayNN.md --model-dir DIR  # offline transcript
python -m tradingbot.forecast make | grade                   # Day 4 homework: forecasts, graded later
```

No orders are placed yet. Candle reads are context only, never entries.
