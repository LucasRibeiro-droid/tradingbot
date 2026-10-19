"""Self-improving trading bot.

Knowledge is added one bootcamp lesson at a time (see ``knowledge/``); every
threshold the bot uses lives in ``tradingbot.config`` so the learning loop can
change exactly one variable at a time and compare against the baseline.
"""
