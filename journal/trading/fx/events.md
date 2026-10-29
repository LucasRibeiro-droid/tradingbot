# Events (CRT on OANDA: gold, NAS100)

| UTC | What | Impact | Action |
|---|---|---|---|
| 2026-10-28 15:19 | session start (practice): NAV 100000.0000 GBP, 0 trade(s) open in the state |  |  |
| 2026-10-28 15:33 | session start (practice): NAV 100000.0000 GBP, 0 trade(s) open in the state |  |  |
| 2026-10-28 16:45 | error in the cycle: GET /v3/instruments/XAU_USD/candles?granularity=M5&price=M&from=2026-10-28T16%3A40%3A00.000000000Z&count=5000: HTTP 401: {"errorMessage":"Insufficient authorization to perform request."} | this minute skipped | retry next minute |
| 2026-10-28 19:30 | error in the cycle: GET /v3/instruments/XAU_USD/candles?granularity=M5&price=M&from=2026-10-28T19%3A25%3A00.000000000Z&count=5000: HTTP 401: {"errorMessage":"Insufficient authorization to perform request."} | this minute skipped | retry next minute |
| 2026-10-28 20:00 | error in the cycle: GET /v3/instruments/XAU_USD/candles?granularity=M5&price=M&from=2026-10-28T19%3A55%3A00.000000000Z&count=5000: HTTP 401: {"errorMessage":"Insufficient authorization to perform request."} | this minute skipped | retry next minute |
| 2026-10-28 21:00 | market closed and nothing open: session end |  |  |
| 2026-10-29 00:07 | session start (practice): NAV 100000.0441 GBP, 0 trade(s) open in the state |  |  |
| 2026-10-29 05:52 | session hand-off (runner time limit) | orders and trades stay protected at OANDA | next run resumes |
