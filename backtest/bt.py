import sys; sys.path.insert(0, "/home/user/tradingbot/backtest")
sys.argv = ["x", "/tmp/claude-0/-home-user-tradingbot/df70ef2e-c468-5b83-a3b1-1abfe0c61852/scratchpad/cache"]
exec(open("/home/user/tradingbot/backtest/run.py").read())
def show(tag, d): print(f"{tag:28s}", "  ".join(f"{k}={v:.2f}" if isinstance(v,float) else f"{k}={v}" for k,v in d.items()), flush=True)
