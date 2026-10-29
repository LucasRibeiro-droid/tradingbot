# Rulebook changelog

Each version is written after the day shown and used from the next trading day. ADD/DROP lines cite the experiment evidence behind the change.

## v2 (written after 2021-01-15, used from the next trading day)
- ADD XAU_USD|continuation|1h>5m|2R|with_1h: 67 experiment trades so far, mean +0.138R, score +0.003

## v3 (written after 2021-01-22, used from the next trading day)
- BENCH XAU_USD|continuation|1h>5m|2R|with_1h: its own strategy trades lost -0.234R over the last 16 (until ~3 months)
- DROP XAU_USD|continuation|1h>5m|2R|with_1h: now 86 trades, mean +0.046R, last 180 days +0.046R over 86

## v4 (written after 2021-01-29, used from the next trading day)
- ADD NAS100_USD|continuation|1h>1m|3R|newyork+with_4h: 62 experiment trades so far, mean +0.364R, score +0.109
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_break|3R|stop>=6sp: 60 experiment trades so far, mean +0.249R, score +0.057
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_break|1R|against_D: 66 experiment trades so far, mean +0.182R, score +0.053

## v5 (written after 2021-02-05, used from the next trading day)
- BENCH XAU_USD (non-CRT): its strategy trades lost -0.278R over the last 31
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|against_D: 103 experiment trades so far, mean +0.147R, score +0.037
- DROP NAS100_USD|continuation|1h>1m|3R|newyork+with_4h: now 73 trades, mean +0.257R, last 180 days +0.257R over 73
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_break|3R|stop>=6sp: now 71 trades, mean +0.128R, last 180 days +0.128R over 71
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_break|1R|against_D: now 89 trades, mean +0.032R, last 180 days +0.032R over 89

## v6 (written after 2021-02-12, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|1R|stop>=10sp: 77 experiment trades so far, mean +0.130R, score +0.028
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|stop>=6sp+newyork: 90 experiment trades so far, mean +0.126R, score +0.021
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|against_D: now 128 trades, mean +0.079R, last 180 days +0.079R over 128

## v7 (written after 2021-02-19, used from the next trading day)
- ADD NAS100_USD|continuation|1h>1m|3R|ny_midday: 71 experiment trades so far, mean +0.313R, score +0.088
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|1R|stop>=6sp+newyork: 73 experiment trades so far, mean +0.203R, score +0.072
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|1R|stop>=10sp: now 97 trades, mean +0.108R, last 180 days +0.108R over 97
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|stop>=6sp+newyork: now 110 trades, mean -0.007R, last 180 days -0.007R over 110

## v8 (written after 2021-02-26, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|against_D: 67 experiment trades so far, mean +0.235R, score +0.058
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|1R|against_D: 77 experiment trades so far, mean +0.137R, score +0.035
- DAY STOPS: stop after +0.5R / NoneR on the day (replayed on the last 40 days: 62% green, +13.4R)

## v9 (written after 2021-03-05, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|against_D: 197 experiment trades so far, mean +0.161R, score +0.072
- ADD NAS100_USD|continuation|1h>5m|3R|stop>=6sp+newyork: 66 experiment trades so far, mean +0.231R, score +0.053
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|stop>=10sp: 136 experiment trades so far, mean +0.132R, score +0.042
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|1R|against_D: now 88 trades, mean +0.130R, last 180 days +0.130R over 88

## v10 (written after 2021-03-12, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|against_D: 216 experiment trades so far, mean +0.127R, score +0.058
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|stop>=6sp: 176 experiment trades so far, mean +0.119R, score +0.041
- DROP NAS100_USD|continuation|1h>1m|3R|ny_midday: now 111 trades, mean +0.138R, last 180 days +0.138R over 111
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|against_D: now 216 trades, mean +0.181R, last 180 days +0.181R over 216
- DROP NAS100_USD|continuation|1h>5m|3R|stop>=6sp+newyork: now 77 trades, mean +0.158R, last 180 days +0.158R over 77
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|stop>=10sp: now 139 trades, mean +0.136R, last 180 days +0.136R over 139

## v11 (written after 2021-03-19, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|0.5R|ny_open: 63 experiment trades so far, mean +0.123R, score +0.033
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|stop>=10sp: 63 experiment trades so far, mean +0.215R, score +0.022
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|half1R_be3R|stop>=3sp: 61 experiment trades so far, mean +0.138R, score +0.008
- ADD NAS100_USD|continuation|1h>1m|half1R_3R|ny_midday: 131 experiment trades so far, mean +0.075R, score +0.000
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|1R|stop>=6sp+newyork: now 123 trades, mean +0.109R, last 180 days +0.109R over 123
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|against_D: now 85 trades, mean +0.109R, last 180 days +0.109R over 85
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|stop>=6sp: now 205 trades, mean +0.066R, last 180 days +0.066R over 205

## v12 (written after 2021-03-26, used from the next trading day)
- BENCH NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|against_D: its own strategy trades lost -0.290R over the last 32 (until ~3 months)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|against_D: 251 experiment trades so far, mean +0.084R, score +0.019
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|1R|newyork+with_4h: 66 experiment trades so far, mean +0.130R, score +0.017
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|against_D: now 251 trades, mean +0.048R, last 180 days +0.048R over 251
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|0.5R|ny_open: now 68 trades, mean +0.056R, last 180 days +0.056R over 68
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|stop>=10sp: now 68 trades, mean +0.122R, last 180 days +0.122R over 68
- DROP NAS100_USD|continuation|1h>1m|half1R_3R|ny_midday: now 149 trades, mean +0.036R, last 180 days +0.036R over 149
- DAY STOPS: stop after +1.0R / NoneR on the day (replayed on the last 60 days: 57% green, +9.8R)

## v13 (written after 2021-04-02, used from the next trading day)
- BENCH NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|against_D: its own strategy trades lost -0.534R over the last 24 (until ~3 months)
- BENCH NAS100_USD (non-CRT): its strategy trades lost -0.173R over the last 148
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|half1R_be3R|stop>=3sp: now 72 trades, mean +0.172R, last 180 days +0.172R over 72
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|against_D: now 276 trades, mean +0.017R, last 180 days +0.017R over 276
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|1R|newyork+with_4h: now 77 trades, mean +0.226R, last 180 days +0.226R over 77
- DAY STOPS: none

## v14 (written after 2021-04-23, used from the next trading day)
- BENCH XAU_USD|continuation|1h>5m|2R|with_1h: its own strategy trades lost -0.234R over the last 16 (until ~3 months)

## v15 (written after 2021-05-07, used from the next trading day)
- BENCH XAU_USD (non-CRT): its strategy trades lost -0.278R over the last 31

## v16 (written after 2021-06-25, used from the next trading day)
- BENCH NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|against_D: its own strategy trades lost -0.507R over the last 17 (until ~3 months)

## v17 (written after 2021-07-02, used from the next trading day)
- BENCH NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|against_D: its own strategy trades lost -0.534R over the last 24 (until ~3 months)
- BENCH NAS100_USD (non-CRT): its strategy trades lost -0.314R over the last 78

## v18 (written after 2021-08-06, used from the next trading day)
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|stop>=10sp: 99 experiment trades so far, mean +0.458R, score +0.248
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_gap|1R|stop>=6sp+with_D: 69 experiment trades so far, mean +0.293R, score +0.132
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_break|3R|stop>=10sp: 157 experiment trades so far, mean +0.214R, score +0.123
- DAY STOPS: stop after +0.5R / -2.0R on the day (replayed on the last 155 days: 52% green, +32.4R)

## v19 (written after 2021-08-13, used from the next trading day)
- ADD XAU_USD|continuation|4h>15m|half1R_be3R|london+with_4h: 73 experiment trades so far, mean +0.102R, score +0.002
- DAY STOPS: stop after +2.0R / NoneR on the day (replayed on the last 160 days: 53% green, +46.9R)

## v20 (written after 2021-08-20, used from the next trading day)
- ADD XAU_USD|continuation|1h>5m|0.5R|ny_midday: 100 experiment trades so far, mean +0.049R, score +0.003
- DAY STOPS: stop after +0.5R / NoneR on the day (replayed on the last 165 days: 54% green, +44.8R)

## v21 (written after 2021-08-27, used from the next trading day)
- ADD XAU_USD|sweep_bos|1m|sessions|at_break|3R|london: 66 experiment trades so far, mean +0.223R, score +0.023
- DROP XAU_USD|continuation|1h>5m|0.5R|ny_midday: now 101 trades, mean +0.039R, last 180 days +0.048R over 78

## v22 (written after 2021-09-03, used from the next trading day)
- DROP XAU_USD|continuation|4h>15m|half1R_be3R|london+with_4h: now 74 trades, mean +0.086R, last 180 days +0.084R over 57

## v23 (written after 2021-09-10, used from the next trading day)
- BENCH XAU_USD (non-CRT): its strategy trades lost -0.374R over the last 27
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|stop>=10sp: now 114 trades, mean +0.332R, last 180 days +0.363R over 77
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_gap|1R|stop>=6sp+with_D: now 77 trades, mean +0.213R, last 180 days +0.167R over 62
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_break|3R|stop>=10sp: now 178 trades, mean +0.138R, last 180 days +0.142R over 122
- DROP XAU_USD|sweep_bos|1m|sessions|at_break|3R|london: now 68 trades, mean +0.183R, last 180 days +0.176R over 52
- DAY STOPS: none

## v24 (written after 2021-10-01, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h: 67 experiment trades so far, mean +0.701R, score +0.345
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: 67 experiment trades so far, mean +0.412R, score +0.193
- ADD NAS100_USD|continuation|1h>5m|3R|newyork+with_D: 140 experiment trades so far, mean +0.307R, score +0.181
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|3R|stop>=6sp+with_D: 84 experiment trades so far, mean +0.357R, score +0.143
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=6sp+with_D: 79 experiment trades so far, mean +0.292R, score +0.140
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: 137 experiment trades so far, mean +0.254R, score +0.135
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: 73 experiment trades so far, mean +0.294R, score +0.078
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|2R|newyork+with_1h+with_4h: 89 experiment trades so far, mean +0.180R, score +0.047
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|half1R_be3R|ny_open: 81 experiment trades so far, mean +0.126R, score +0.017
- ADD NAS100_USD|continuation|1h>1m|3R|ny_midday: 373 experiment trades so far, mean +0.067R, score +0.015
- DAY STOPS: stop after +0.5R / NoneR on the day (replayed on the last 195 days: 57% green, +43.0R)

## v25 (written after 2021-10-08, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: 95 experiment trades so far, mean +0.260R, score +0.105
- ADD NAS100_USD|sweep_bos|5m|sessions|at_block|1R|stop>=6sp+with_D: 60 experiment trades so far, mean +0.191R, score +0.050
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: now 143 trades, mean +0.217R, last 180 days +0.049R over 91
- DROP NAS100_USD|continuation|1h>1m|3R|ny_midday: now 373 trades, mean +0.067R, last 180 days +0.008R over 204

## v26 (written after 2021-10-22, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|newyork+with_15m: 139 experiment trades so far, mean +0.105R, score +0.032
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: now 104 trades, mean +0.175R, last 180 days +0.044R over 67
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|half1R_be3R|ny_open: now 91 trades, mean +0.047R, last 180 days -0.030R over 67

## v27 (written after 2021-10-29, used from the next trading day)


## v28 (written after 2021-11-05, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: 175 experiment trades so far, mean +0.217R, score +0.121
- ADD NAS100_USD|continuation|1h>1m|3R|ny_midday: 417 experiment trades so far, mean +0.059R, score +0.011
- ADD NAS100_USD|sweep_bos|5m|sessions|at_break|3R|with_4h+with_D: 88 experiment trades so far, mean +0.135R, score +0.003
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: now 91 trades, mean +0.116R, last 180 days -0.062R over 58
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|newyork+with_15m: now 154 trades, mean +0.131R, last 180 days +0.196R over 95
- DROP NAS100_USD|sweep_bos|5m|sessions|at_block|1R|stop>=6sp+with_D: now 65 trades, mean +0.094R, last 180 days +0.121R over 29

## v29 (written after 2021-11-12, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|with_D: 114 experiment trades so far, mean +0.141R, score +0.057
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=6sp+with_D: now 90 trades, mean +0.197R, last 180 days +0.182R over 43
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|2R|newyork+with_1h+with_4h: now 115 trades, mean +0.085R, last 180 days -0.031R over 74
- DROP NAS100_USD|continuation|1h>1m|3R|ny_midday: now 430 trades, mean +0.032R, last 180 days -0.036R over 222
- DROP NAS100_USD|sweep_bos|5m|sessions|at_break|3R|with_4h+with_D: now 90 trades, mean +0.109R, last 180 days +0.310R over 52

## v30 (written after 2021-11-19, used from the next trading day)
- ADD NAS100_USD|sweep_bos|1m|sessions|at_equilibrium|3R|with_4h+with_D: 60 experiment trades so far, mean +0.244R, score +0.022
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 120 experiment trades so far, mean +0.114R, score +0.011

## v31 (written after 2021-11-26, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=6sp+with_D: 96 experiment trades so far, mean +0.246R, score +0.124
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|2R|ny_midday: 211 experiment trades so far, mean +0.160R, score +0.084
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|1R|ny_midday: 69 experiment trades so far, mean +0.121R, score +0.016
- ADD NAS100_USD|continuation|1h>1m|3R|ny_open+with_1h: 279 experiment trades so far, mean +0.070R, score +0.009
- ADD NAS100_USD|sweep_bos|5m|sessions|at_block|1R|stop>=6sp+with_D: 70 experiment trades so far, mean +0.100R, score +0.003
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|with_D: now 120 trades, mean +0.183R, last 180 days +0.177R over 61
- DROP NAS100_USD|sweep_bos|1m|sessions|at_equilibrium|3R|with_4h+with_D: now 63 trades, mean +0.179R, last 180 days +0.532R over 27
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: now 120 trades, mean +0.114R, last 180 days +0.080R over 74
- DAY STOPS: stop after +2.0R / NoneR on the day (replayed on the last 235 days: 44% green, +11.6R)

## v32 (written after 2021-12-03, used from the next trading day)
- ADD NAS100_USD|sweep_bos|1m|sessions|at_gap|3R|stop>=3sp: 67 experiment trades so far, mean +0.253R, score +0.045
- DROP NAS100_USD|sweep_bos|5m|sessions|at_block|1R|stop>=6sp+with_D: now 73 trades, mean +0.109R, last 180 days +0.155R over 30
- DAY STOPS: stop after +1.0R / NoneR on the day (replayed on the last 240 days: 44% green, +12.7R)

## v33 (written after 2021-12-10, used from the next trading day)
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_gap|1R|stop>=6sp+with_D: 100 experiment trades so far, mean +0.231R, score +0.120
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: 100 experiment trades so far, mean +0.199R, score +0.049
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|1R|ny_midday: now 71 trades, mean +0.116R, last 180 days +0.010R over 44
- DROP NAS100_USD|continuation|1h>1m|3R|ny_open+with_1h: now 287 trades, mean +0.067R, last 180 days +0.291R over 156
- DAY STOPS: stop after +0.5R / NoneR on the day (replayed on the last 245 days: 51% green, +46.6R)

## v34 (written after 2021-12-17, used from the next trading day)
- BENCH NAS100_USD|continuation|1h>5m|3R|newyork+with_D: its own strategy trades lost -0.182R over the last 19 (until ~3 months)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|half1R_be3R|with_4h+with_D: 72 experiment trades so far, mean +0.341R, score +0.150
- ADD NAS100_USD|continuation|1h>5m|2R|newyork+with_D: 185 experiment trades so far, mean +0.153R, score +0.083
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|1R|ny_midday: 72 experiment trades so far, mean +0.128R, score +0.023
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|3R|stop>=6sp+with_D: now 105 trades, mean +0.295R, last 180 days +0.023R over 60
- DROP NAS100_USD|continuation|1h>5m|3R|newyork+with_D: now 185 trades, mean +0.238R, last 180 days +0.115R over 103
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: now 102 trades, mean +0.175R, last 180 days +0.306R over 57

## v35 (written after 2021-12-27, used from the next trading day)


## v36 (written after 2022-01-03, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 60 experiment trades so far, mean +0.639R, score +0.280
- ADD NAS100_USD|sweep_bos|5m|sessions|at_break|2R|with_1h: 60 experiment trades so far, mean +0.414R, score +0.159
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: 108 experiment trades so far, mean +0.330R, score +0.149
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h: now 93 trades, mean +0.411R, last 180 days +0.010R over 52
- DROP NAS100_USD|sweep_bos|1m|sessions|at_gap|3R|stop>=3sp: now 72 trades, mean +0.218R, last 180 days +0.682R over 37
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|1R|ny_midday: now 72 trades, mean +0.128R, last 180 days +0.053R over 37

## v37 (written after 2022-01-10, used from the next trading day)


## v38 (written after 2022-01-17, used from the next trading day)
- BENCH NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=6sp+with_D: its own strategy trades lost -0.206R over the last 17 (until ~3 months)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|half1R_be3R|asia: 60 experiment trades so far, mean +0.596R, score +0.288
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|2R|stop>=6sp+newyork: 108 experiment trades so far, mean +0.304R, score +0.151
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|half1R_be3R|with_4h+with_D: now 73 trades, mean +0.364R, last 180 days +0.473R over 32
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=6sp+with_D: now 109 trades, mean +0.205R, last 180 days +0.167R over 47

## v39 (written after 2022-01-24, used from the next trading day)


## v40 (written after 2022-01-31, used from the next trading day)


## v41 (written after 2022-02-07, used from the next trading day)
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|stop>=6sp+london: 75 experiment trades so far, mean +0.477R, score +0.200
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|2R|ny_midday: now 247 trades, mean +0.139R, last 180 days +0.171R over 109

## v42 (written after 2022-02-14, used from the next trading day)
- ADD NAS100_USD|continuation|1h>5m|3R|newyork+with_4h: 280 experiment trades so far, mean +0.181R, score +0.117
- DROP NAS100_USD|continuation|1h>5m|2R|newyork+with_D: now 205 trades, mean +0.145R, last 180 days +0.009R over 93

## v43 (written after 2022-02-21, used from the next trading day)


## v44 (written after 2022-02-28, used from the next trading day)
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|2R|stop>=6sp+london: 77 experiment trades so far, mean +0.482R, score +0.231
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|stop>=6sp+london: now 77 trades, mean +0.438R, last 180 days +0.835R over 33

## v45 (written after 2022-03-07, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|asia: 67 experiment trades so far, mean +0.629R, score +0.302
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|newyork+with_D: 62 experiment trades so far, mean +0.334R, score +0.143
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_gap|1R|stop>=6sp+asia: 61 experiment trades so far, mean +0.322R, score +0.134
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|half1R_be3R|asia: now 67 trades, mean +0.550R, last 180 days +0.711R over 28
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|2R|stop>=6sp+newyork: now 117 trades, mean +0.253R, last 180 days +0.382R over 40
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_gap|1R|stop>=6sp+with_D: now 119 trades, mean +0.184R, last 180 days +0.101R over 43

## v46 (written after 2022-03-14, used from the next trading day)
- ADD NAS100_USD|continuation|1h>5m|3R|newyork+with_D: 220 experiment trades so far, mean +0.262R, score +0.174
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|2R|newyork+with_1h+with_4h: 124 experiment trades so far, mean +0.221R, score +0.099
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: now 124 trades, mean +0.325R, last 180 days +0.419R over 52
- DROP NAS100_USD|continuation|1h>5m|3R|newyork+with_4h: now 298 trades, mean +0.186R, last 180 days +0.433R over 117

## v47 (written after 2022-03-21, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|2R|stop>=6sp+newyork: 124 experiment trades so far, mean +0.278R, score +0.145
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|newyork+with_D: now 66 trades, mean +0.283R, last 180 days +0.200R over 23

## v48 (written after 2022-03-28, used from the next trading day)


## v49 (written after 2022-04-04, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h: 166 experiment trades so far, mean +0.207R, score +0.127
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|1R|ny_midday: 91 experiment trades so far, mean +0.196R, score +0.084
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: now 64 trades, mean +0.580R, last 180 days -0.502R over 18
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: now 99 trades, mean +0.281R, last 180 days +0.008R over 32

## v50 (written after 2022-04-11, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|ny_open+with_1h: 69 experiment trades so far, mean +0.396R, score +0.170
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|1R|ny_midday: now 92 trades, mean +0.205R, last 180 days +0.496R over 33

## v51 (written after 2022-04-19, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: 130 experiment trades so far, mean +0.292R, score +0.140
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|1R|ny_midday: 92 experiment trades so far, mean +0.205R, score +0.091
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|ny_open+with_1h: now 69 trades, mean +0.396R, last 180 days -0.169R over 21
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|2R|newyork+with_1h+with_4h: now 130 trades, mean +0.209R, last 180 days +0.155R over 51

## v52 (written after 2022-04-26, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|newyork+with_1h: 60 experiment trades so far, mean +0.403R, score +0.132
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|1R|ny_midday: now 92 trades, mean +0.205R, last 180 days +0.464R over 31

## v53 (written after 2022-05-03, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: 183 experiment trades so far, mean +0.294R, score +0.182
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: now 256 trades, mean +0.234R, last 180 days +0.273R over 81

## v54 (written after 2022-05-10, used from the next trading day)
- BENCH NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|2R|stop>=6sp+newyork: its own strategy trades lost -0.223R over the last 15 (until ~3 months)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|2R|newyork: 143 experiment trades so far, mean +0.315R, score +0.185
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|1R|ny_midday: 96 experiment trades so far, mean +0.238R, score +0.118
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 175 experiment trades so far, mean +0.180R, score +0.083
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|2R|stop>=6sp+newyork: now 143 trades, mean +0.315R, last 180 days +0.592R over 53
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h: now 181 trades, mean +0.143R, last 180 days -0.096R over 64
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|newyork+with_1h: now 64 trades, mean +0.325R, last 180 days +0.650R over 22

## v55 (written after 2022-05-17, used from the next trading day)


## v56 (written after 2022-05-24, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h: 185 experiment trades so far, mean +0.151R, score +0.087
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: now 182 trades, mean +0.156R, last 180 days +0.236R over 62

## v57 (written after 2022-05-31, used from the next trading day)
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_break|3R|ny_open+with_1h: 80 experiment trades so far, mean +0.205R, score +0.076
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|2R|stop>=6sp+london: now 100 trades, mean +0.280R, last 180 days +0.386R over 40

## v58 (written after 2022-06-07, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|newyork+with_1h+with_4h: 77 experiment trades so far, mean +0.500R, score +0.252
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|with_1h: 65 experiment trades so far, mean +0.569R, score +0.234
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: 121 experiment trades so far, mean +0.257R, score +0.143
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|2R|newyork: now 154 trades, mean +0.311R, last 180 days +0.491R over 55
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h: now 192 trades, mean +0.182R, last 180 days -0.011R over 64
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_break|3R|ny_open+with_1h: now 80 trades, mean +0.205R, last 180 days +0.443R over 38

## v59 (written after 2022-06-14, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 78 experiment trades so far, mean +0.603R, score +0.306
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: 60 experiment trades so far, mean +0.605R, score +0.246
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|newyork+with_1h+with_4h: now 78 trades, mean +0.519R, last 180 days +0.258R over 24
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|1R|ny_midday: now 105 trades, mean +0.206R, last 180 days +0.375R over 33

## v60 (written after 2022-06-21, used from the next trading day)


## v61 (written after 2022-06-28, used from the next trading day)


## v62 (written after 2022-07-05, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 206 experiment trades so far, mean +0.202R, score +0.110
- DROP NAS100_USD|continuation|1h>5m|3R|newyork+with_D: now 284 trades, mean +0.173R, last 180 days +0.044R over 96

## v63 (written after 2022-07-12, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h: 198 experiment trades so far, mean +0.196R, score +0.126
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: now 125 trades, mean +0.249R, last 180 days +0.061R over 32

## v64 (written after 2022-07-19, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h: 125 experiment trades so far, mean +0.432R, score +0.257
- ADD NAS100_USD|continuation|1h>5m|3R|newyork+with_D: 290 experiment trades so far, mean +0.188R, score +0.124
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: now 81 trades, mean +0.544R, last 180 days +0.272R over 21
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_gap|1R|stop>=6sp+asia: now 75 trades, mean +0.255R, last 180 days -0.091R over 17

## v65 (written after 2022-07-26, used from the next trading day)
- BENCH NAS100_USD|sweep_bos|5m|sessions|at_break|2R|with_1h: its own strategy trades lost -0.189R over the last 21 (until ~3 months)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|with_1h+room>=2R: 62 experiment trades so far, mean +0.547R, score +0.213
- ADD NAS100_USD|sweep_bos|5m|sessions|at_break|2R|stop>=6sp+with_1h: 90 experiment trades so far, mean +0.410R, score +0.211
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|with_1h: now 73 trades, mean +0.465R, last 180 days +0.354R over 28
- DROP NAS100_USD|sweep_bos|5m|sessions|at_break|2R|with_1h: now 98 trades, mean +0.369R, last 180 days +0.286R over 36

## v66 (written after 2022-08-02, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|1R|ny_midday: 108 experiment trades so far, mean +0.206R, score +0.103
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: now 213 trades, mean +0.162R, last 180 days +0.080R over 66

## v67 (written after 2022-08-09, used from the next trading day)
- BENCH NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: its own strategy trades lost -0.390R over the last 15 (until ~3 months)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: 327 experiment trades so far, mean +0.229R, score +0.164
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: now 233 trades, mean +0.271R, last 180 days +0.188R over 73

## v68 (written after 2022-08-16, used from the next trading day)


## v69 (written after 2022-08-23, used from the next trading day)


## v70 (written after 2022-08-30, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 86 experiment trades so far, mean +0.584R, score +0.310
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h: now 131 trades, mean +0.459R, last 180 days +0.632R over 34

## v71 (written after 2022-09-06, used from the next trading day)
- BENCH NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|asia: its own strategy trades lost -0.242R over the last 15 (until ~3 months)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|stop>=6sp+asia: 82 experiment trades so far, mean +0.511R, score +0.260
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|asia: now 91 trades, mean +0.487R, last 180 days +0.089R over 24

## v72 (written after 2022-09-13, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 228 experiment trades so far, mean +0.179R, score +0.096
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|1R|ny_midday: now 113 trades, mean +0.151R, last 180 days +0.156R over 27

## v73 (written after 2022-09-20, used from the next trading day)


## v74 (written after 2022-09-27, used from the next trading day)
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_gap|1R|stop>=6sp+with_D: 164 experiment trades so far, mean +0.170R, score +0.101
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: now 235 trades, mean +0.143R, last 180 days +0.148R over 76

## v75 (written after 2022-10-04, used from the next trading day)


## v76 (written after 2022-10-11, used from the next trading day)


## v77 (written after 2022-10-18, used from the next trading day)


## v78 (written after 2022-10-25, used from the next trading day)


## v79 (written after 2022-11-01, used from the next trading day)


## v80 (written after 2022-11-08, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|stop>=6sp+with_1h: 79 experiment trades so far, mean +0.433R, score +0.183
- ADD NAS100_USD|continuation|1h>5m|3R|ny_midday: 297 experiment trades so far, mean +0.204R, score +0.137
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 253 experiment trades so far, mean +0.179R, score +0.102
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|with_1h+room>=2R: now 73 trades, mean +0.419R, last 180 days +0.025R over 24
- DROP NAS100_USD|continuation|1h>5m|3R|newyork+with_D: now 350 trades, mean +0.170R, last 180 days -0.053R over 92
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_gap|1R|stop>=6sp+with_D: now 178 trades, mean +0.126R, last 180 days -0.218R over 43

## v81 (written after 2022-11-15, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|ny_open+with_1h: 94 experiment trades so far, mean +0.454R, score +0.234
- ADD NAS100_USD|sweep_bos|5m|sessions|at_break|2R|newyork+with_1h: 60 experiment trades so far, mean +0.512R, score +0.221
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: now 96 trades, mean +0.417R, last 180 days +0.345R over 26
- DROP NAS100_USD|sweep_bos|5m|sessions|at_break|2R|stop>=6sp+with_1h: now 106 trades, mean +0.346R, last 180 days +0.190R over 29
- DAY STOPS: stop after +1.0R / NoneR on the day (replayed on the last 250 days: 54% green, +88.6R)

## v82 (written after 2022-11-22, used from the next trading day)
- ADD NAS100_USD|continuation|4h>5m|3R|newyork+with_1h+with_4h: 280 experiment trades so far, mean +0.137R, score +0.079
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: now 263 trades, mean +0.137R, last 180 days +0.094R over 81

## v83 (written after 2022-11-29, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|3R|with_4h+with_D: 149 experiment trades so far, mean +0.292R, score +0.160
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|ny_open+with_1h: 70 experiment trades so far, mean +0.307R, score +0.089
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|stop>=6sp+asia: now 99 trades, mean +0.364R, last 180 days -0.315R over 33
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: now 78 trades, mean +0.345R, last 180 days -0.404R over 21

## v84 (written after 2022-12-06, used from the next trading day)


## v85 (written after 2022-12-13, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 273 experiment trades so far, mean +0.154R, score +0.084
- DROP NAS100_USD|continuation|4h>5m|3R|newyork+with_1h+with_4h: now 293 trades, mean +0.168R, last 180 days +0.146R over 61

## v86 (written after 2022-12-20, used from the next trading day)


## v87 (written after 2022-12-28, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: 290 experiment trades so far, mean +0.240R, score +0.165
- ADD NAS100_USD|sweep_bos|5m|sessions|at_block|3R|stop>=6sp+with_1h: 63 experiment trades so far, mean +0.380R, score +0.111
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: now 422 trades, mean +0.197R, last 180 days +0.075R over 108
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|ny_open+with_1h: now 70 trades, mean +0.307R, last 180 days -0.538R over 8

## v88 (written after 2023-01-12, used from the next trading day)


## v89 (written after 2023-01-19, used from the next trading day)
- ADD NAS100_USD|continuation|4h>5m|3R|newyork+with_1h+with_4h: 305 experiment trades so far, mean +0.168R, score +0.109
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: now 288 trades, mean +0.150R, last 180 days +0.059R over 79

## v90 (written after 2023-01-26, used from the next trading day)


## v91 (written after 2023-02-02, used from the next trading day)


## v92 (written after 2023-02-09, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_break|2R|stop>=6sp+with_1h: 124 experiment trades so far, mean +0.317R, score +0.178
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|ny_open+with_1h: 72 experiment trades so far, mean +0.382R, score +0.139
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|newyork+with_1h: 642 experiment trades so far, mean +0.143R, score +0.110
- DROP NAS100_USD|sweep_bos|5m|sessions|at_break|2R|newyork+with_1h: now 71 trades, mean +0.438R, last 180 days -0.104R over 16
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: now 302 trades, mean +0.222R, last 180 days +0.054R over 69
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|stop>=6sp+with_1h: now 91 trades, mean +0.336R, last 180 days -0.039R over 23

## v93 (written after 2023-02-16, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_break|2R|newyork+with_1h: 73 experiment trades so far, mean +0.481R, score +0.233
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: 311 experiment trades so far, mean +0.272R, score +0.197
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|stop>=6sp+with_1h: 94 experiment trades so far, mean +0.378R, score +0.172
- DROP NAS100_USD|sweep_bos|5m|sessions|at_break|2R|stop>=6sp+with_1h: now 127 trades, mean +0.333R, last 180 days +0.214R over 35
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|ny_open+with_1h: now 72 trades, mean +0.382R, last 180 days +0.300R over 9
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|newyork+with_1h: now 654 trades, mean +0.169R, last 180 days +0.125R over 163

## v94 (written after 2023-02-23, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|ny_open+with_1h: 75 experiment trades so far, mean +0.486R, score +0.210
- DROP NAS100_USD|continuation|4h>5m|3R|newyork+with_1h+with_4h: now 315 trades, mean +0.163R, last 180 days +0.153R over 62

## v95 (written after 2023-03-02, used from the next trading day)
- DAY STOPS: stop after +0.5R / NoneR on the day (replayed on the last 250 days: 53% green, +63.7R)

## v96 (written after 2023-03-09, used from the next trading day)


## v97 (written after 2023-03-16, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 314 experiment trades so far, mean +0.186R, score +0.117
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|3R|with_4h+with_D: now 168 trades, mean +0.297R, last 180 days -0.196R over 35
- DAY STOPS: stop after +1.0R / NoneR on the day (replayed on the last 250 days: 50% green, +52.7R)

## v98 (written after 2023-03-23, used from the next trading day)


## v99 (written after 2023-04-06, used from the next trading day)


## v100 (written after 2023-04-13, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|newyork+with_1h: 60 experiment trades so far, mean +0.865R, score +0.398
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|stop>=6sp+with_1h: now 104 trades, mean +0.355R, last 180 days +0.203R over 28
- DAY STOPS: stop after +0.5R / NoneR on the day (replayed on the last 250 days: 51% green, +65.1R)

## v101 (written after 2023-04-20, used from the next trading day)
- ADD XAU_USD|sweep_bos|5m|sessions|at_gap|3R|with_4h: 98 experiment trades so far, mean +0.339R, score +0.150
- DROP NAS100_USD|continuation|1h>5m|3R|ny_midday: now 371 trades, mean +0.173R, last 180 days +0.033R over 78

## v102 (written after 2023-04-27, used from the next trading day)


## v103 (written after 2023-05-04, used from the next trading day)


## v104 (written after 2023-05-11, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|3R|stop>=6sp+london: 154 experiment trades so far, mean +0.267R, score +0.137
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h: now 307 trades, mean +0.153R, last 180 days -0.056R over 81

## v105 (written after 2023-05-18, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_break|3R|newyork+with_1h: 88 experiment trades so far, mean +0.491R, score +0.255
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|ny_open+with_1h: 199 experiment trades so far, mean +0.342R, score +0.217
- ADD NAS100_USD|continuation|1h>5m|3R|ny_midday: 381 experiment trades so far, mean +0.177R, score +0.123
- DROP NAS100_USD|sweep_bos|5m|sessions|at_break|2R|newyork+with_1h: now 88 trades, mean +0.439R, last 180 days +0.282R over 28
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: now 275 trades, mean +0.273R, last 180 days +0.351R over 71
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: now 346 trades, mean +0.159R, last 180 days +0.172R over 87

## v106 (written after 2023-05-25, used from the next trading day)


## v107 (written after 2023-06-01, used from the next trading day)


## v108 (written after 2023-06-08, used from the next trading day)


## v109 (written after 2023-06-15, used from the next trading day)


## v110 (written after 2023-06-22, used from the next trading day)


## v111 (written after 2023-06-29, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 368 experiment trades so far, mean +0.211R, score +0.145
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|3R|stop>=6sp+london: now 164 trades, mean +0.233R, last 180 days +0.577R over 48

## v112 (written after 2023-07-06, used from the next trading day)


## v113 (written after 2023-07-20, used from the next trading day)


## v114 (written after 2023-08-03, used from the next trading day)
- BENCH NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: its own strategy trades lost -0.593R over the last 16 (until ~3 months)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h: 569 experiment trades so far, mean +0.176R, score +0.128
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: now 383 trades, mean +0.212R, last 180 days +0.498R over 89

## v115 (written after 2023-08-10, used from the next trading day)
- BENCH NAS100_USD (non-CRT): its strategy trades lost -0.153R over the last 98
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|2R|stop>=6sp+london: 216 experiment trades so far, mean +0.114R, score +0.047
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|london+with_4h: 317 experiment trades so far, mean +0.095R, score +0.043
- ADD XAU_USD|sweep_bos|5m|sessions|at_break|2R|with_4h+with_D: 264 experiment trades so far, mean +0.089R, score +0.036
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_break|half1R_be3R|ny_open+with_1h: 116 experiment trades so far, mean +0.096R, score +0.034
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|newyork+with_1h: now 68 trades, mean +0.878R, last 180 days +1.110R over 15
- DROP NAS100_USD|sweep_bos|5m|sessions|at_break|3R|newyork+with_1h: now 94 trades, mean +0.481R, last 180 days +0.608R over 23
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: now 369 trades, mean +0.309R, last 180 days +0.710R over 66
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|ny_open+with_1h: now 121 trades, mean +0.404R, last 180 days +0.274R over 22
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|ny_open+with_1h: now 214 trades, mean +0.317R, last 180 days +0.256R over 30
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|ny_open+with_1h: now 92 trades, mean +0.418R, last 180 days +0.547R over 20
- DROP NAS100_USD|sweep_bos|5m|sessions|at_block|3R|stop>=6sp+with_1h: now 90 trades, mean +0.302R, last 180 days -0.235R over 24
- DROP NAS100_USD|continuation|1h>5m|3R|ny_midday: now 414 trades, mean +0.156R, last 180 days -0.043R over 74
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h: now 574 trades, mean +0.179R, last 180 days +0.509R over 139
- DAY STOPS: stop after +0.5R / -2.0R on the day (replayed on the last 250 days: 45% green, +48.6R)

## v116 (written after 2023-08-17, used from the next trading day)


## v117 (written after 2023-08-24, used from the next trading day)


## v118 (written after 2023-08-31, used from the next trading day)
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_break|half1R_be3R|ny_open+with_1h: now 124 trades, mean +0.044R, last 180 days -0.100R over 24

## v119 (written after 2023-09-21, used from the next trading day)
- BENCH NAS100_USD|continuation|1h>5m|3R|ny_midday: its own strategy trades lost -0.197R over the last 25 (until ~3 months)

## v120 (written after 2023-10-05, used from the next trading day)
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_break|3R|with_4h+with_D: 885 experiment trades so far, mean +0.031R, score +0.005
- DAY STOPS: stop after +0.5R / NoneR on the day (replayed on the last 250 days: 45% green, +50.9R)

## v121 (written after 2023-10-12, used from the next trading day)
- ADD XAU_USD|sweep_bos|5m|sessions|at_break|3R|london+with_4h: 125 experiment trades so far, mean +0.203R, score +0.075
- DROP XAU_USD|sweep_bos|5m|sessions|at_break|2R|with_4h+with_D: now 283 trades, mean +0.090R, last 180 days +0.303R over 58

## v122 (written after 2023-10-19, used from the next trading day)
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|london+with_4h: 206 experiment trades so far, mean +0.176R, score +0.082
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|2R|stop>=6sp+london: now 218 trades, mean +0.131R, last 180 days +0.487R over 26

## v123 (written after 2023-10-26, used from the next trading day)


## v124 (written after 2023-11-02, used from the next trading day)
- ADD XAU_USD|sweep_bos|5m|sessions|at_gap|3R|with_4h+with_D: 78 experiment trades so far, mean +0.569R, score +0.276
- DROP XAU_USD|sweep_bos|5m|sessions|at_gap|3R|with_4h: now 125 trades, mean +0.440R, last 180 days +0.780R over 24

## v125 (written after 2023-11-09, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|newyork+with_1h: 75 experiment trades so far, mean +0.837R, score +0.437
- ADD NAS100_USD|sweep_bos|5m|sessions|at_break|3R|newyork+with_1h: 103 experiment trades so far, mean +0.427R, score +0.231
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: 417 experiment trades so far, mean +0.254R, score +0.193
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|ny_open+with_1h: 97 experiment trades so far, mean +0.392R, score +0.187
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h: 204 experiment trades so far, mean +0.254R, score +0.160
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 432 experiment trades so far, mean +0.210R, score +0.150
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|ny_open+with_1h: 190 experiment trades so far, mean +0.192R, score +0.117
- ADD NAS100_USD|continuation|4h>5m|3R|newyork+with_1h+with_4h: 421 experiment trades so far, mean +0.163R, score +0.115
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|london+with_4h: now 216 trades, mean +0.211R, last 180 days +0.264R over 39
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|london+with_4h: now 332 trades, mean +0.115R, last 180 days +0.155R over 40
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_break|3R|with_4h+with_D: now 913 trades, mean +0.044R, last 180 days +0.232R over 178

## v126 (written after 2023-11-16, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|ny_open: 452 experiment trades so far, mean +0.161R, score +0.110
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: 230 experiment trades so far, mean +0.151R, score +0.094
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|london+with_4h: 332 experiment trades so far, mean +0.115R, score +0.063
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|ny_open+with_1h: now 97 trades, mean +0.392R, last 180 days -0.357R over 7
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h: now 205 trades, mean +0.259R, last 180 days -0.115R over 20
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|ny_open+with_1h: now 190 trades, mean +0.192R, last 180 days +0.210R over 16

## v127 (written after 2023-11-23, used from the next trading day)
- BENCH NAS100_USD (non-CRT): its strategy trades lost -0.410R over the last 30
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_break|3R|with_4h+with_D: 916 experiment trades so far, mean +0.049R, score +0.023
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|newyork+with_1h: now 75 trades, mean +0.837R, last 180 days +1.003R over 11
- DROP NAS100_USD|sweep_bos|5m|sessions|at_break|3R|newyork+with_1h: now 103 trades, mean +0.427R, last 180 days +0.047R over 15
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: now 419 trades, mean +0.247R, last 180 days +0.020R over 74
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: now 436 trades, mean +0.198R, last 180 days +0.334R over 88
- DROP NAS100_USD|continuation|4h>5m|3R|newyork+with_1h+with_4h: now 430 trades, mean +0.165R, last 180 days +0.347R over 71
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|ny_open: now 452 trades, mean +0.161R, last 180 days +0.282R over 90
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: now 231 trades, mean +0.151R, last 180 days +0.150R over 31
- DAY STOPS: stop after +0.5R / -2.0R on the day (replayed on the last 250 days: 41% green, +47.1R)

## v128 (written after 2023-11-30, used from the next trading day)
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|stop>=10sp: 393 experiment trades so far, mean +0.066R, score +0.023
- DAY STOPS: stop after +0.5R / NoneR on the day (replayed on the last 250 days: 42% green, +49.1R)

## v129 (written after 2023-12-07, used from the next trading day)
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|stop>=10sp: now 394 trades, mean +0.071R, last 180 days +0.114R over 56
- DAY STOPS: stop after +0.5R / -2.0R on the day (replayed on the last 250 days: 41% green, +39.1R)

## v130 (written after 2023-12-14, used from the next trading day)
- BENCH XAU_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|london+with_4h: its own strategy trades lost -0.291R over the last 16 (until ~3 months)
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|stop>=10sp: 395 experiment trades so far, mean +0.068R, score +0.025
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|london+with_4h: now 341 trades, mean +0.085R, last 180 days -0.064R over 43
- DAY STOPS: stop after +0.5R / NoneR on the day (replayed on the last 250 days: 42% green, +42.3R)

## v131 (written after 2023-12-21, used from the next trading day)
- BENCH XAU_USD|sweep_bos|15m|pivots+sessions|at_break|3R|with_4h+with_D: its own strategy trades lost -0.257R over the last 25 (until ~3 months)
- BENCH XAU_USD (non-CRT): its strategy trades lost -0.158R over the last 68
- DROP XAU_USD|sweep_bos|5m|sessions|at_gap|3R|with_4h+with_D: now 80 trades, mean +0.526R, last 180 days +0.251R over 13
- DROP XAU_USD|sweep_bos|5m|sessions|at_break|3R|london+with_4h: now 131 trades, mean +0.194R, last 180 days +0.261R over 18
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_break|3R|with_4h+with_D: now 937 trades, mean +0.046R, last 180 days +0.288R over 154
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|stop>=10sp: now 395 trades, mean +0.068R, last 180 days -0.043R over 45
- DAY STOPS: none

## v132 (written after 2024-02-19, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_break|3R|newyork+with_1h: 113 experiment trades so far, mean +0.429R, score +0.244
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: 447 experiment trades so far, mean +0.271R, score +0.211
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|stop>=6sp+with_1h: 142 experiment trades so far, mean +0.329R, score +0.180
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|ny_open+with_1h: 311 experiment trades so far, mean +0.251R, score +0.171
- ADD NAS100_USD|sweep_bos|5m|sessions|at_block|3R|stop>=6sp+with_1h: 109 experiment trades so far, mean +0.323R, score +0.145
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h: 369 experiment trades so far, mean +0.157R, score +0.114
- ADD NAS100_USD|continuation|4h>5m|3R|newyork+with_1h+with_4h: 468 experiment trades so far, mean +0.156R, score +0.112
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|ny_open: 490 experiment trades so far, mean +0.149R, score +0.102
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|3R|with_1h: 183 experiment trades so far, mean +0.141R, score +0.059
- ADD NAS100_USD|continuation|1h>5m|3R|newyork+with_4h: 835 experiment trades so far, mean +0.084R, score +0.057
- DAY STOPS: stop after +0.5R / NoneR on the day (replayed on the last 250 days: 49% green, +33.6R)

## v133 (written after 2024-02-26, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|2R|ny_open+with_1h: 256 experiment trades so far, mean +0.153R, score +0.085
- DROP NAS100_USD|continuation|1h>5m|3R|newyork+with_4h: now 845 trades, mean +0.073R, last 180 days -0.029R over 142

## v134 (written after 2024-03-04, used from the next trading day)
- BENCH NAS100_USD (non-CRT): its strategy trades lost -0.355R over the last 28
- DROP NAS100_USD|sweep_bos|5m|sessions|at_break|3R|newyork+with_1h: now 114 trades, mean +0.428R, last 180 days +0.240R over 19
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: now 452 trades, mean +0.270R, last 180 days +0.050R over 78
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|stop>=6sp+with_1h: now 142 trades, mean +0.329R, last 180 days +0.436R over 17
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|ny_open+with_1h: now 312 trades, mean +0.259R, last 180 days +0.391R over 51
- DROP NAS100_USD|sweep_bos|5m|sessions|at_block|3R|stop>=6sp+with_1h: now 109 trades, mean +0.323R, last 180 days +0.804R over 13
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h: now 370 trades, mean +0.153R, last 180 days +0.013R over 41
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|ny_open: now 496 trades, mean +0.135R, last 180 days +0.304R over 83
- DROP NAS100_USD|continuation|4h>5m|3R|newyork+with_1h+with_4h: now 478 trades, mean +0.135R, last 180 days +0.158R over 85
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|2R|ny_open+with_1h: now 256 trades, mean +0.153R, last 180 days +0.018R over 42
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|3R|with_1h: now 183 trades, mean +0.141R, last 180 days +0.386R over 28
- DAY STOPS: none

## v135 (written after 2024-03-18, used from the next trading day)
- BENCH XAU_USD|sweep_bos|15m|pivots+sessions|at_break|3R|with_4h+with_D: its own strategy trades lost -0.640R over the last 15 (until ~3 months)
- BENCH XAU_USD (non-CRT): its strategy trades lost -0.579R over the last 28

## v136 (written after 2024-05-28, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_break|3R|newyork+with_1h: 115 experiment trades so far, mean +0.415R, score +0.237
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: 473 experiment trades so far, mean +0.252R, score +0.196
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|ny_open+with_1h: 326 experiment trades so far, mean +0.216R, score +0.143
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|stop>=6sp+with_1h: 148 experiment trades so far, mean +0.273R, score +0.141
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|stop>=6sp+asia: 164 experiment trades so far, mean +0.247R, score +0.140
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|ny_open+with_1h: 211 experiment trades so far, mean +0.204R, score +0.133
- ADD NAS100_USD|sweep_bos|5m|sessions|at_gap|1R|stop>=6sp+newyork: 92 experiment trades so far, mean +0.163R, score +0.063
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|stop>=6sp+with_1h: 523 experiment trades so far, mean +0.097R, score +0.055
- ADD NAS100_USD|continuation|4h>5m|3R|ny_open+with_1h: 139 experiment trades so far, mean +0.128R, score +0.037
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|1R|ny_midday: 235 experiment trades so far, mean +0.058R, score +0.017
- DAY STOPS: stop after +0.5R / NoneR on the day (replayed on the last 250 days: 45% green, +30.7R)

## v137 (written after 2024-06-04, used from the next trading day)
- BENCH NAS100_USD (non-CRT): its strategy trades lost -0.708R over the last 25
- DROP NAS100_USD|sweep_bos|5m|sessions|at_break|3R|newyork+with_1h: now 116 trades, mean +0.403R, last 180 days +0.513R over 10
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: now 479 trades, mean +0.236R, last 180 days +0.203R over 56
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|ny_open+with_1h: now 332 trades, mean +0.193R, last 180 days +0.054R over 36
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|stop>=6sp+with_1h: now 149 trades, mean +0.265R, last 180 days -0.485R over 12
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|stop>=6sp+asia: now 166 trades, mean +0.231R, last 180 days +0.302R over 18
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|ny_open+with_1h: now 211 trades, mean +0.204R, last 180 days +0.398R over 19
- DROP NAS100_USD|sweep_bos|5m|sessions|at_gap|1R|stop>=6sp+newyork: now 92 trades, mean +0.163R, last 180 days +0.258R over 10
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|stop>=6sp+with_1h: now 527 trades, mean +0.088R, last 180 days -0.235R over 54
- DROP NAS100_USD|continuation|4h>5m|3R|ny_open+with_1h: now 139 trades, mean +0.128R, last 180 days +0.019R over 24
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|1R|ny_midday: now 236 trades, mean +0.062R, last 180 days +0.431R over 33
- DAY STOPS: none

## v138 (written after 2024-06-11, used from the next trading day)
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|london+with_4h: 269 experiment trades so far, mean +0.152R, score +0.076
- ADD XAU_USD|sweep_bos|5m|sessions|at_gap|3R|london: 85 experiment trades so far, mean +0.176R, score +0.019

## v139 (written after 2024-06-18, used from the next trading day)
- DROP XAU_USD|sweep_bos|5m|sessions|at_gap|3R|london: now 86 trades, mean +0.162R, last 180 days -0.140R over 13

## v140 (written after 2024-07-16, used from the next trading day)
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|london+with_4h: now 276 trades, mean +0.151R, last 180 days -0.006R over 53

## v141 (written after 2024-09-03, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_break|3R|newyork+with_1h: 127 experiment trades so far, mean +0.371R, score +0.214
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|3R|with_1h+room>=2R: 138 experiment trades so far, mean +0.333R, score +0.183
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: 125 experiment trades so far, mean +0.269R, score +0.125
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|newyork+with_1h: 251 experiment trades so far, mean +0.172R, score +0.108
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|0.5R|ny_open+with_1h: 226 experiment trades so far, mean +0.133R, score +0.093
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|half1R_be3R|ny_midday: 255 experiment trades so far, mean +0.091R, score +0.043
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|2R|newyork+with_D: 212 experiment trades so far, mean +0.109R, score +0.042
- ADD NAS100_USD|continuation|4h>15m|3R|ny_open: 155 experiment trades so far, mean +0.070R, score +0.005
- DAY STOPS: stop after +1.0R / NoneR on the day (replayed on the last 250 days: 44% green, +24.8R)

## v142 (written after 2024-09-10, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_gap|half1R_be3R|stop>=6sp+newyork: 101 experiment trades so far, mean +0.097R, score +0.017
- DROP NAS100_USD|continuation|4h>15m|3R|ny_open: now 156 trades, mean +0.063R, last 180 days +0.177R over 26
- DAY STOPS: stop after +0.5R / NoneR on the day (replayed on the last 250 days: 46% green, +27.4R)

## v143 (written after 2024-09-17, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_block|3R|newyork+with_1h: 73 experiment trades so far, mean +0.760R, score +0.374
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|newyork+with_1h: 94 experiment trades so far, mean +0.659R, score +0.365
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|ny_open+with_1h: 305 experiment trades so far, mean +0.237R, score +0.155
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: 516 experiment trades so far, mean +0.203R, score +0.154
- ADD NAS100_USD|sweep_bos|5m|sessions|at_gap|1R|stop>=6sp+newyork: 104 experiment trades so far, mean +0.161R, score +0.069
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|half1R_be3R|ny_midday: now 258 trades, mean +0.090R, last 180 days +0.377R over 33
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|2R|newyork+with_D: now 216 trades, mean +0.116R, last 180 days -0.056R over 33
- DROP NAS100_USD|sweep_bos|5m|sessions|at_gap|half1R_be3R|stop>=6sp+newyork: now 104 trades, mean +0.123R, last 180 days +0.545R over 15

## v144 (written after 2024-09-24, used from the next trading day)
- BENCH NAS100_USD (non-CRT): its strategy trades lost -0.279R over the last 27
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|0.5R|ny_open+with_1h: 106 experiment trades so far, mean +0.053R, score +0.007
- DROP NAS100_USD|sweep_bos|5m|sessions|at_block|3R|newyork+with_1h: now 76 trades, mean +0.761R, last 180 days +0.693R over 17
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|newyork+with_1h: now 97 trades, mean +0.649R, last 180 days -0.078R over 17
- DROP NAS100_USD|sweep_bos|5m|sessions|at_break|3R|newyork+with_1h: now 134 trades, mean +0.382R, last 180 days +0.121R over 20
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: now 129 trades, mean +0.353R, last 180 days +1.177R over 18
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|3R|with_1h+room>=2R: now 139 trades, mean +0.324R, last 180 days +1.107R over 24
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|ny_open+with_1h: now 307 trades, mean +0.227R, last 180 days +0.150R over 50
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: now 522 trades, mean +0.195R, last 180 days -0.367R over 64
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|newyork+with_1h: now 259 trades, mean +0.199R, last 180 days +0.466R over 41
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|0.5R|ny_open+with_1h: now 232 trades, mean +0.143R, last 180 days +0.237R over 30
- DROP NAS100_USD|sweep_bos|5m|sessions|at_gap|1R|stop>=6sp+newyork: now 104 trades, mean +0.161R, last 180 days +0.317R over 15
- DAY STOPS: none

## v145 (written after 2024-12-24, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_block|3R|newyork+with_1h: 81 experiment trades so far, mean +0.799R, score +0.424
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|newyork+with_1h: 107 experiment trades so far, mean +0.681R, score +0.405
- ADD NAS100_USD|sweep_bos|5m|sessions|at_break|3R|newyork+with_1h: 145 experiment trades so far, mean +0.375R, score +0.229
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: 134 experiment trades so far, mean +0.316R, score +0.166
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|ny_open+with_1h: 157 experiment trades so far, mean +0.245R, score +0.141
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|stop>=6sp+with_1h: 216 experiment trades so far, mean +0.212R, score +0.135
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|ny_open+with_1h: 336 experiment trades so far, mean +0.201R, score +0.129
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|0.5R|ny_open+with_1h: 233 experiment trades so far, mean +0.144R, score +0.103
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 625 experiment trades so far, mean +0.141R, score +0.098
- ADD NAS100_USD|sweep_bos|5m|sessions|at_gap|1R|stop>=6sp+newyork: 115 experiment trades so far, mean +0.136R, score +0.055
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|0.5R|ny_open+with_1h: now 107 trades, mean +0.057R, last 180 days +0.492R over 14
