# tradingbot

A self-improving trading bot for Alpaca (paper trading). It learns a strategy one lesson
at a time from the TJR Boot Camp, measures every rule against real price data, and
changes one variable at a time so each improvement can be traced to its cause.

- `knowledge/`: what the bot has learned, lesson by lesson
- `tradingbot/`: the code (`candles.py` for Day 2, `discipline.py` for Day 3, `study.py` for the homework studies, `data.py` for Alpaca bars)
- `journal/`: study results, open hypotheses and the daily journal

```
python -m unittest discover -s tests -t .           # tests
python -m tradingbot.study SPY --timeframe 1Day --days 2200   # Day 2 study (needs ALPACA_API_KEY / ALPACA_SECRET_KEY)
```

No orders are placed yet. Candle reads are context only, never entries.
