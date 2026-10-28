import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-tradingbot/efe032f3-ac09-5164-8e64-23adecf81035/scratchpad/research")
import orb_bt as O
import numpy as np
# optimistic bound: the fill bar can't stop the trade (5-minute bars hide the order of moves inside the bar)
src = open(O.__file__).read()
def run_opt(**kw):
    orig = O.run
    return orig(**kw)
# patch: copy run with the fill-bar stop check removed
code = src.split("def run(")[1].split("\ndef rep(")[0]
code = "def run_opt(" + code.replace("for k in range(fill, len(x)):", "for k in range(fill + 1, len(x)):")
exec(code, O.__dict__)
for name, kw in [("OPTIMISTIC fill bar: 0.10 ATR", {}), ("OPTIMISTIC: 0.25 ATR", {"stop_atr": 0.25}), ("OPTIMISTIC: 0.5 ATR", {"stop_atr": 0.5}),
                 ("OPTIMISTIC: 1.0 ATR", {"stop_atr": 1.0})]:
    O.rep(name, O.run_opt(**kw))
