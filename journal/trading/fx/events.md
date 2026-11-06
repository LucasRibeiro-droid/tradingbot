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
| 2026-10-29 05:53 | session start (practice): NAV 100000.0441 GBP, 0 trade(s) open in the state |  |  |
| 2026-10-29 11:38 | session hand-off (runner time limit) | orders and trades stay protected at OANDA | next run resumes |
| 2026-10-29 11:39 | session start (practice): NAV 100000.0441 GBP, 0 trade(s) open in the state |  |  |
| 2026-10-29 13:00 | error in the cycle: GET /v3/instruments/XAU_USD/candles?granularity=M5&price=M&from=2026-10-29T12%3A55%3A00.000000000Z&count=5000: HTTP 401: {"errorMessage":"Insufficient authorization to perform request."} | this minute skipped | retry next minute |
| 2026-10-29 17:00 | error in the cycle: GET /v3/instruments/XAU_USD/candles?granularity=M5&price=M&from=2026-10-29T16%3A55%3A00.000000000Z&count=5000: HTTP 401: {"errorMessage":"Insufficient authorization to perform request."} | this minute skipped | retry next minute |
| 2026-10-29 17:25 | session hand-off (runner time limit) | orders and trades stay protected at OANDA | next run resumes |
| 2026-10-29 17:26 | session start (practice): NAV 100000.0441 GBP, 0 trade(s) open in the state |  |  |
| 2026-10-29 21:00 | market closed and nothing open: session end |  |  |
| 2026-10-29 22:00 | session start (practice): NAV 100000.0441 GBP, 0 trade(s) open in the state |  |  |
| 2026-10-30 03:46 | session hand-off (runner time limit) | orders and trades stay protected at OANDA | next run resumes |
| 2026-10-30 03:46 | session start (practice): NAV 100000.0441 GBP, 0 trade(s) open in the state |  |  |
| 2026-10-30 09:32 | session hand-off (runner time limit) | orders and trades stay protected at OANDA | next run resumes |
| 2026-10-30 09:32 | session start (practice): NAV 100000.0441 GBP, 0 trade(s) open in the state |  |  |
| 2026-10-30 15:18 | session hand-off (runner time limit) | orders and trades stay protected at OANDA | next run resumes |
| 2026-10-30 15:19 | session start (practice): NAV 100000.0441 GBP, 0 trade(s) open in the state |  |  |
| 2026-10-30 21:00 | market closed and nothing open: session end |  |  |
| 2026-11-02 00:03 | session start (practice): NAV 100000.0441 GBP, 0 trade(s) open in the state |  |  |
| 2026-11-02 05:49 | session hand-off (runner time limit) | orders and trades stay protected at OANDA | next run resumes |
| 2026-11-02 05:49 | session start (practice): NAV 100000.0441 GBP, 0 trade(s) open in the state |  |  |
| 2026-11-02 07:00 | error in the cycle: GET /v3/accounts/101-004-40823841-001/pricing?instruments=XAU_USD%2CNAS100_USD%2CGBP_USD: HTTP 401: {"errorMessage":"Insufficient authorization to perform request."} | this minute skipped | retry next minute |
| 2026-11-02 11:35 | session hand-off (runner time limit) | orders and trades stay protected at OANDA | next run resumes |
| 2026-11-02 11:36 | session start (practice): NAV 100000.0441 GBP, 0 trade(s) open in the state |  |  |
| 2026-11-02 13:25 | error in the cycle: GET /v3/instruments/NAS100_USD/candles?granularity=M5&price=M&from=2026-11-02T13%3A20%3A00.000000000Z&count=5000: HTTP 504: error code: 504
 | this minute skipped | retry next minute |
| 2026-11-02 16:00 | error in the cycle: GET /v3/instruments/NAS100_USD/candles?granularity=M5&price=M&from=2026-11-02T15%3A55%3A00.000000000Z&count=5000: HTTP 504: error code: 504
 | this minute skipped | retry next minute |
| 2026-11-02 17:21 | session hand-off (runner time limit) | orders and trades stay protected at OANDA | next run resumes |
| 2026-11-02 17:22 | session start (practice): NAV 100000.0441 GBP, 0 trade(s) open in the state |  |  |
| 2026-11-02 21:00 | error in the cycle: GET /v3/accounts/101-004-40823841-001/pricing?instruments=XAU_USD%2CNAS100_USD%2CGBP_USD: HTTP 401: {"errorMessage":"Insufficient authorization to perform request."} | this minute skipped | retry next minute |
| 2026-11-02 22:00 | market closed and nothing open: session end |  |  |
| 2026-11-03 03:47 | session start (practice): NAV 100000.0441 GBP, 0 trade(s) open in the state |  |  |
| 2026-11-03 09:33 | session hand-off (runner time limit) | orders and trades stay protected at OANDA | next run resumes |
| 2026-11-03 09:33 | session start (practice): NAV 100000.0441 GBP, 0 trade(s) open in the state |  |  |
| 2026-11-03 15:19 | session hand-off (runner time limit) | orders and trades stay protected at OANDA | next run resumes |
| 2026-11-03 15:20 | session start (practice): NAV 100000.0441 GBP, 0 trade(s) open in the state |  |  |
| 2026-11-03 21:05 | session hand-off (runner time limit) | orders and trades stay protected at OANDA | next run resumes |
| 2026-11-03 21:07 | session start (practice): NAV 100000.0441 GBP, 0 trade(s) open in the state |  |  |
| 2026-11-03 22:00 | market closed and nothing open: session end |  |  |
| 2026-11-03 23:40 | session start (practice): NAV 100000.0441 GBP, 0 trade(s) open in the state |  |  |
| 2026-11-04 05:25 | session hand-off (runner time limit) | orders and trades stay protected at OANDA | next run resumes |
| 2026-11-04 05:26 | session start (practice): NAV 100032.5529 GBP, 0 trade(s) open in the state |  |  |
| 2026-11-04 11:12 | session hand-off (runner time limit) | orders and trades stay protected at OANDA | next run resumes |
| 2026-11-04 11:13 | session start (practice): NAV 100032.5529 GBP, 0 trade(s) open in the state |  |  |
| 2026-11-04 16:58 | session hand-off (runner time limit) | orders and trades stay protected at OANDA | next run resumes |
| 2026-11-04 17:00 | session start (practice): NAV 100032.5529 GBP, 0 trade(s) open in the state |  |  |
| 2026-11-04 22:00 | market closed and nothing open: session end |  |  |
| 2026-11-04 23:51 | session start (practice): NAV 100032.5529 GBP, 0 trade(s) open in the state |  |  |
| 2026-11-05 05:37 | session hand-off (runner time limit) | orders and trades stay protected at OANDA | next run resumes |
| 2026-11-05 05:38 | session start (practice): NAV 100032.5529 GBP, 0 trade(s) open in the state |  |  |
| 2026-11-05 11:23 | session hand-off (runner time limit) | orders and trades stay protected at OANDA | next run resumes |
| 2026-11-05 11:24 | session start (practice): NAV 100032.5529 GBP, 0 trade(s) open in the state |  |  |
| 2026-11-05 14:30 | error in the cycle: GET /v3/accounts/101-004-40823841-001/pricing?instruments=XAU_USD%2CNAS100_USD%2CGBP_USD: HTTP 401: {"errorMessage":"Insufficient authorization to perform request."} | this minute skipped | retry next minute |
| 2026-11-05 15:00 | error in the cycle: GET /v3/instruments/XAU_USD/candles?granularity=M5&price=M&from=2026-11-05T14%3A55%3A00.000000000Z&count=5000: HTTP 401: {"errorMessage":"Insufficient authorization to perform request."} | this minute skipped | retry next minute |
| 2026-11-05 15:25 | error in the cycle: GET /v3/accounts/101-004-40823841-001/pricing?instruments=XAU_USD%2CNAS100_USD%2CGBP_USD: HTTP 401: {"errorMessage":"Insufficient authorization to perform request."} | this minute skipped | retry next minute |
| 2026-11-05 16:10 | error in the cycle: GET /v3/accounts/101-004-40823841-001/pricing?instruments=XAU_USD%2CNAS100_USD%2CGBP_USD: HTTP 401: {"errorMessage":"Insufficient authorization to perform request."} | this minute skipped | retry next minute |
| 2026-11-05 17:10 | session hand-off (runner time limit) | orders and trades stay protected at OANDA | next run resumes |
| 2026-11-05 17:11 | session start (practice): NAV 100032.5529 GBP, 0 trade(s) open in the state |  |  |
| 2026-11-05 22:00 | market closed and nothing open: session end |  |  |
| 2026-11-06 01:00 | session start (practice): NAV 100032.5529 GBP, 0 trade(s) open in the state |  |  |
| 2026-11-06 01:20 | error in the cycle: GET /v3/instruments/XAU_USD/candles?granularity=M5&price=M&from=2026-11-06T01%3A15%3A00.000000000Z&count=5000: HTTP 401: {"errorMessage":"Insufficient authorization to perform request."} | this minute skipped | retry next minute |
| 2026-11-06 05:25 | error in the cycle: GET /v3/accounts/101-004-40823841-001/pricing?instruments=XAU_USD%2CNAS100_USD%2CGBP_USD: HTTP 401: {"errorMessage":"Insufficient authorization to perform request."} | this minute skipped | retry next minute |
| 2026-11-06 05:50 | error in the cycle: GET /v3/accounts/101-004-40823841-001/pricing?instruments=XAU_USD%2CNAS100_USD%2CGBP_USD: HTTP 401: {"errorMessage":"Insufficient authorization to perform request."} | this minute skipped | retry next minute |
