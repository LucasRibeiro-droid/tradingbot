# Rulebook changelog

Each version is written after the day shown and used from the next trading day. ADD/DROP lines cite the experiment evidence behind the change.

## v2 (written after 2021-01-15, used from the next trading day)
- ADD XAU_USD|continuation|1h>5m|2R|with_1h: 67 experiment trades so far, mean +0.138R, score +0.003

## v3 (written after 2021-01-22, used from the next trading day)
- DROP XAU_USD|continuation|1h>5m|2R|with_1h: now 86 trades, mean +0.046R, last 180 days +0.046R over 86

## v4 (written after 2021-01-29, used from the next trading day)
- ADD NAS100_USD|continuation|1h>1m|3R|newyork+with_4h: 62 experiment trades so far, mean +0.364R, score +0.109
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_break|3R|stop>=6sp: 60 experiment trades so far, mean +0.249R, score +0.057
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_break|1R|against_D: 66 experiment trades so far, mean +0.182R, score +0.053

## v5 (written after 2021-02-05, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|against_D: 103 experiment trades so far, mean +0.147R, score +0.037
- ADD XAU_USD|continuation|1h>1m|1R|ny_open+with_1h: 60 experiment trades so far, mean +0.122R, score +0.009
- DROP NAS100_USD|continuation|1h>1m|3R|newyork+with_4h: now 73 trades, mean +0.257R, last 180 days +0.257R over 73
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_break|3R|stop>=6sp: now 71 trades, mean +0.128R, last 180 days +0.128R over 71
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_break|1R|against_D: now 91 trades, mean -0.013R, last 180 days -0.013R over 91

## v6 (written after 2021-02-12, used from the next trading day)
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_break|3R|stop>=6sp+discount: 66 experiment trades so far, mean +0.209R, score +0.034
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|1R|stop>=10sp: 77 experiment trades so far, mean +0.130R, score +0.028
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|stop>=6sp+newyork: 90 experiment trades so far, mean +0.126R, score +0.021
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_break|2R|stop>=6sp: 93 experiment trades so far, mean +0.105R, score +0.008
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|against_D: now 128 trades, mean +0.079R, last 180 days +0.079R over 128
- DROP XAU_USD|continuation|1h>1m|1R|ny_open+with_1h: now 69 trades, mean +0.013R, last 180 days +0.013R over 69

## v7 (written after 2021-02-19, used from the next trading day)
- ADD NAS100_USD|continuation|1h>1m|3R|ny_midday: 71 experiment trades so far, mean +0.313R, score +0.088
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_break|1R|stop>=10sp: 70 experiment trades so far, mean +0.195R, score +0.074
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|1R|stop>=6sp+newyork: 73 experiment trades so far, mean +0.203R, score +0.072
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_break|3R|stop>=6sp+discount: now 82 trades, mean -0.274R, last 180 days -0.274R over 82
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|1R|stop>=10sp: now 97 trades, mean +0.108R, last 180 days +0.108R over 97
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|stop>=6sp+newyork: now 110 trades, mean -0.007R, last 180 days -0.007R over 110
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_break|2R|stop>=6sp: now 120 trades, mean +0.003R, last 180 days +0.003R over 120

## v8 (written after 2021-02-26, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|against_D: 67 experiment trades so far, mean +0.235R, score +0.058
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_break|2R|stop>=10sp: 77 experiment trades so far, mean +0.166R, score +0.040
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|1R|against_D: 77 experiment trades so far, mean +0.137R, score +0.035
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_break|1R|stop>=10sp: now 77 trades, mean +0.128R, last 180 days +0.128R over 77
- DAY STOPS: stop after +0.5R / NoneR on the day (replayed on the last 40 days: 62% green, +26.1R)

## v9 (written after 2021-03-05, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|against_D: 198 experiment trades so far, mean +0.151R, score +0.064
- ADD NAS100_USD|continuation|1h>5m|3R|stop>=6sp+newyork: 66 experiment trades so far, mean +0.231R, score +0.053
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|stop>=10sp: 136 experiment trades so far, mean +0.132R, score +0.042
- ADD XAU_USD|continuation|1h>1m|half1R_be3R|stop>=6sp+with_D: 72 experiment trades so far, mean +0.146R, score +0.027
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_break|2R|stop>=10sp: now 83 trades, mean +0.078R, last 180 days +0.078R over 83
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|1R|against_D: now 88 trades, mean +0.130R, last 180 days +0.130R over 88

## v10 (written after 2021-03-12, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|against_D: 217 experiment trades so far, mean +0.118R, score +0.051
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|stop>=6sp: 176 experiment trades so far, mean +0.119R, score +0.041
- DROP NAS100_USD|continuation|1h>1m|3R|ny_midday: now 111 trades, mean +0.138R, last 180 days +0.138R over 111
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|against_D: now 217 trades, mean +0.172R, last 180 days +0.172R over 217
- DROP NAS100_USD|continuation|1h>5m|3R|stop>=6sp+newyork: now 77 trades, mean +0.158R, last 180 days +0.158R over 77
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|stop>=10sp: now 139 trades, mean +0.136R, last 180 days +0.136R over 139

## v11 (written after 2021-03-19, used from the next trading day)
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_break|3R|with_D: 97 experiment trades so far, mean +0.211R, score +0.073
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|0.5R|ny_open: 63 experiment trades so far, mean +0.123R, score +0.033
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|with_D: 77 experiment trades so far, mean +0.204R, score +0.033
- ADD XAU_USD|continuation|1h>1m|1R|stop>=6sp+with_D: 84 experiment trades so far, mean +0.117R, score +0.025
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|stop>=10sp: 63 experiment trades so far, mean +0.215R, score +0.022
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|half1R_be3R|stop>=3sp: 61 experiment trades so far, mean +0.138R, score +0.008
- ADD NAS100_USD|continuation|1h>1m|half1R_3R|ny_midday: 131 experiment trades so far, mean +0.075R, score +0.000
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|1R|stop>=6sp+newyork: now 123 trades, mean +0.109R, last 180 days +0.109R over 123
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|against_D: now 86 trades, mean +0.085R, last 180 days +0.085R over 86
- DROP XAU_USD|continuation|1h>1m|half1R_be3R|stop>=6sp+with_D: now 84 trades, mean +0.138R, last 180 days +0.138R over 84
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|stop>=6sp: now 205 trades, mean +0.066R, last 180 days +0.066R over 205

## v12 (written after 2021-03-26, used from the next trading day)
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_break|half1R_be3R|with_1h: 64 experiment trades so far, mean +0.309R, score +0.127
- ADD XAU_USD|continuation|1h>1m|half1R_3R|stop>=6sp+with_D: 89 experiment trades so far, mean +0.125R, score +0.021
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|1R|newyork+with_4h: 66 experiment trades so far, mean +0.130R, score +0.017
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|against_D: 253 experiment trades so far, mean +0.069R, score +0.006
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_break|3R|with_D: now 125 trades, mean +0.072R, last 180 days +0.072R over 125
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|against_D: now 253 trades, mean +0.033R, last 180 days +0.033R over 253
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|0.5R|ny_open: now 68 trades, mean +0.056R, last 180 days +0.056R over 68
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|with_D: now 97 trades, mean +0.085R, last 180 days +0.085R over 97
- DROP XAU_USD|continuation|1h>1m|1R|stop>=6sp+with_D: now 89 trades, mean +0.097R, last 180 days +0.097R over 89
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|stop>=10sp: now 68 trades, mean +0.122R, last 180 days +0.122R over 68
- DROP NAS100_USD|continuation|1h>1m|half1R_3R|ny_midday: now 149 trades, mean +0.036R, last 180 days +0.036R over 149

## v13 (written after 2021-04-02, used from the next trading day)
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_break|3R|with_1h: 72 experiment trades so far, mean +0.444R, score +0.196
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|2R|newyork+with_4h: 77 experiment trades so far, mean +0.331R, score +0.135
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|newyork+with_1h: 70 experiment trades so far, mean +0.348R, score +0.134
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_4h: 62 experiment trades so far, mean +0.270R, score +0.109
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_break|2R|stop>=10sp: 68 experiment trades so far, mean +0.262R, score +0.098
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=3sp: 72 experiment trades so far, mean +0.215R, score +0.079
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|newyork+with_4h: 63 experiment trades so far, mean +0.267R, score +0.049
- ADD NAS100_USD|continuation|1h>5m|3R|stop>=6sp+newyork: 107 experiment trades so far, mean +0.108R, score +0.009
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_break|half1R_be3R|with_1h: now 72 trades, mean +0.368R, last 180 days +0.368R over 72
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|half1R_be3R|stop>=3sp: now 72 trades, mean +0.172R, last 180 days +0.172R over 72
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|1R|newyork+with_4h: now 77 trades, mean +0.226R, last 180 days +0.226R over 77
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|against_D: now 279 trades, mean -0.005R, last 180 days -0.005R over 279

## v14 (written after 2021-04-09, used from the next trading day)
- ADD NAS100_USD|continuation|1h>5m|3R|newyork+with_D: 60 experiment trades so far, mean +0.492R, score +0.201
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=6sp: 65 experiment trades so far, mean +0.264R, score +0.103
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|stop>=6sp+newyork: 93 experiment trades so far, mean +0.162R, score +0.030
- ADD NAS100_USD|continuation|1h>1m|half1R_3R|ny_midday: 169 experiment trades so far, mean +0.092R, score +0.025
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=3sp: now 82 trades, mean +0.158R, last 180 days +0.158R over 82
- DROP XAU_USD|continuation|1h>1m|half1R_3R|stop>=6sp+with_D: now 96 trades, mean +0.072R, last 180 days +0.072R over 96
- DROP NAS100_USD|continuation|1h>5m|3R|stop>=6sp+newyork: now 115 trades, mean +0.184R, last 180 days +0.184R over 115

## v15 (written after 2021-04-16, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|stop>=6sp+asia: 63 experiment trades so far, mean +0.509R, score +0.188
- ADD XAU_USD|sweep_bos|1m|sessions|at_break|3R|against_D: 63 experiment trades so far, mean +0.359R, score +0.104
- ADD NAS100_USD|continuation|1h>1m|3R|ny_midday: 182 experiment trades so far, mean +0.136R, score +0.044
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|newyork+with_4h: now 70 trades, mean +0.190R, last 180 days +0.190R over 70
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|stop>=6sp+newyork: now 96 trades, mean +0.151R, last 180 days +0.151R over 96
- DROP NAS100_USD|continuation|1h>1m|half1R_3R|ny_midday: now 182 trades, mean +0.080R, last 180 days +0.080R over 182

## v16 (written after 2021-04-23, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|stop>=6sp: 63 experiment trades so far, mean +0.348R, score +0.114
- DROP NAS100_USD|continuation|1h>1m|3R|ny_midday: now 185 trades, mean +0.160R, last 180 days +0.160R over 185

## v17 (written after 2021-04-30, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|stop>=10sp: 64 experiment trades so far, mean +0.355R, score +0.123
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|2R|ny_midday: 70 experiment trades so far, mean +0.323R, score +0.116
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|2R|newyork+with_4h: now 107 trades, mean +0.157R, last 180 days +0.157R over 107
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|stop>=6sp: now 71 trades, mean +0.277R, last 180 days +0.277R over 71

## v18 (written after 2021-05-07, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|ny_open: 65 experiment trades so far, mean +0.430R, score +0.193
- ADD NAS100_USD|continuation|4h>5m|3R|london+with_4h: 101 experiment trades so far, mean +0.252R, score +0.088
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_4h: now 79 trades, mean +0.334R, last 180 days +0.334R over 79
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|newyork+with_1h: now 90 trades, mean +0.195R, last 180 days +0.195R over 90

## v19 (written after 2021-05-14, used from the next trading day)
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|with_1h: 64 experiment trades so far, mean +0.473R, score +0.180
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_gap|1R|stop>=6sp: 90 experiment trades so far, mean +0.231R, score +0.111
- DROP NAS100_USD|continuation|4h>5m|3R|london+with_4h: now 107 trades, mean +0.180R, last 180 days +0.180R over 107
- DROP XAU_USD|sweep_bos|1m|sessions|at_break|3R|against_D: now 82 trades, mean +0.216R, last 180 days +0.216R over 82

## v20 (written after 2021-05-21, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: 66 experiment trades so far, mean +0.229R, score +0.057
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|stop>=6sp+asia: 72 experiment trades so far, mean +0.220R, score +0.029
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_break|3R|with_1h: now 109 trades, mean +0.287R, last 180 days +0.287R over 109
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_gap|1R|stop>=6sp: now 94 trades, mean +0.178R, last 180 days +0.178R over 94

## v21 (written after 2021-05-28, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=10sp: 60 experiment trades so far, mean +0.308R, score +0.123
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|1R|ny_midday: 86 experiment trades so far, mean +0.194R, score +0.078
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_break|3R|with_1h: 122 experiment trades so far, mean +0.185R, score +0.074
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=6sp: now 95 trades, mean +0.213R, last 180 days +0.213R over 95
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|2R|ny_midday: now 86 trades, mean +0.171R, last 180 days +0.171R over 86
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: now 70 trades, mean +0.193R, last 180 days +0.193R over 70

## v22 (written after 2021-06-04, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|ny_open: 61 experiment trades so far, mean +0.815R, score +0.383
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|stop>=10sp: 60 experiment trades so far, mean +0.588R, score +0.250
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|stop>=6sp+asia: now 81 trades, mean +0.363R, last 180 days +0.363R over 81
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|with_1h: now 85 trades, mean +0.145R, last 180 days +0.145R over 85
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|stop>=6sp+asia: now 74 trades, mean +0.182R, last 180 days +0.182R over 74

## v23 (written after 2021-06-11, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|2R|ny_open: 84 experiment trades so far, mean +0.316R, score +0.151
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_break|2R|stop>=10sp: now 105 trades, mean +0.280R, last 180 days +0.280R over 105
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|ny_open: now 84 trades, mean +0.325R, last 180 days +0.325R over 84

## v24 (written after 2021-06-18, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|ny_open: 90 experiment trades so far, mean +0.443R, score +0.237
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|2R|ny_open: now 90 trades, mean +0.394R, last 180 days +0.394R over 90

## v25 (written after 2021-06-25, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|2R|newyork+with_1h+with_4h: 60 experiment trades so far, mean +0.157R, score +0.001
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|1R|ny_midday: now 105 trades, mean +0.045R, last 180 days +0.045R over 105

## v26 (written after 2021-07-02, used from the next trading day)
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_break|3R|stop>=10sp: 121 experiment trades so far, mean +0.346R, score +0.202
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=6sp: 109 experiment trades so far, mean +0.163R, score +0.071
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=10sp: now 70 trades, mean +0.202R, last 180 days +0.202R over 70
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_break|3R|with_1h: now 142 trades, mean +0.131R, last 180 days +0.131R over 142

## v27 (written after 2021-07-09, used from the next trading day)
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_D: 76 experiment trades so far, mean +0.166R, score +0.021
- ADD XAU_USD|continuation|4h>15m|0.5R|london+with_4h: 60 experiment trades so far, mean +0.084R, score +0.008

## v28 (written after 2021-07-16, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: 98 experiment trades so far, mean +0.181R, score +0.060
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|with_1h: 112 experiment trades so far, mean +0.126R, score +0.015
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_D: now 80 trades, mean +0.137R, last 180 days +0.137R over 80
- DROP XAU_USD|continuation|4h>15m|0.5R|london+with_4h: now 62 trades, mean +0.048R, last 180 days +0.034R over 60

## v29 (written after 2021-07-23, used from the next trading day)
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_gap|1R|stop>=6sp+with_D: 66 experiment trades so far, mean +0.354R, score +0.167
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|with_1h: now 119 trades, mean +0.059R, last 180 days +0.067R over 116

## v30 (written after 2021-07-30, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=6sp+with_D: 62 experiment trades so far, mean +0.234R, score +0.080
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=6sp: now 121 trades, mean +0.127R, last 180 days +0.115R over 103

## v31 (written after 2021-08-06, used from the next trading day)


## v32 (written after 2021-08-13, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|stop>=6sp+with_D: 65 experiment trades so far, mean +0.383R, score +0.145
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|newyork+with_1h: 185 experiment trades so far, mean +0.211R, score +0.126
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: now 118 trades, mean +0.293R, last 180 days +0.190R over 96
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|stop>=10sp: now 104 trades, mean +0.242R, last 180 days +0.216R over 86

## v33 (written after 2021-08-20, used from the next trading day)


## v34 (written after 2021-08-27, used from the next trading day)


## v35 (written after 2021-09-03, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|ny_open: 68 experiment trades so far, mean +0.317R, score +0.092
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=6sp: 141 experiment trades so far, mean +0.148R, score +0.073
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=6sp+with_D: now 74 trades, mean +0.301R, last 180 days +0.450R over 53
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|2R|newyork+with_1h+with_4h: now 85 trades, mean +0.131R, last 180 days +0.082R over 71

## v36 (written after 2021-09-10, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=6sp+with_D: 77 experiment trades so far, mean +0.327R, score +0.161
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|stop>=10sp: 115 experiment trades so far, mean +0.192R, score +0.079
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|stop>=6sp+with_D: now 79 trades, mean +0.189R, last 180 days +0.307R over 66
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=6sp: now 146 trades, mean +0.162R, last 180 days +0.166R over 102

## v37 (written after 2021-09-17, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: 72 experiment trades so far, mean +0.256R, score +0.053
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_break|3R|stop>=10sp: now 191 trades, mean +0.084R, last 180 days +0.056R over 132

## v38 (written after 2021-09-24, used from the next trading day)
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|2R|stop>=10sp: 60 experiment trades so far, mean +0.339R, score +0.122
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|stop>=10sp: now 124 trades, mean +0.104R, last 180 days +0.117R over 85

## v39 (written after 2021-10-01, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: 137 experiment trades so far, mean +0.254R, score +0.135
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|2R|newyork+with_1h+with_4h: 89 experiment trades so far, mean +0.180R, score +0.047
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|stop>=6sp+with_D: 87 experiment trades so far, mean +0.181R, score +0.043
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|newyork+with_1h: now 219 trades, mean +0.197R, last 180 days +0.200R over 149
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|stop>=10sp: now 143 trades, mean +0.089R, last 180 days -0.002R over 105
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|ny_open: now 81 trades, mean +0.147R, last 180 days +0.009R over 58

## v40 (written after 2021-10-08, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: 95 experiment trades so far, mean +0.260R, score +0.105
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|half1R_be3R|with_4h+with_D: 60 experiment trades so far, mean +0.302R, score +0.103
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: now 143 trades, mean +0.217R, last 180 days +0.049R over 91
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|stop>=6sp+with_D: now 88 trades, mean +0.167R, last 180 days +0.152R over 67

## v41 (written after 2021-10-15, used from the next trading day)


## v42 (written after 2021-10-22, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|newyork+with_15m: 139 experiment trades so far, mean +0.105R, score +0.032
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: now 104 trades, mean +0.175R, last 180 days +0.044R over 67

## v43 (written after 2021-10-29, used from the next trading day)
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|0.5R|stop>=10sp: 75 experiment trades so far, mean +0.167R, score +0.074
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|2R|stop>=10sp: now 75 trades, mean +0.198R, last 180 days -0.043R over 49

## v44 (written after 2021-11-05, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: 80 experiment trades so far, mean +0.396R, score +0.199
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: 175 experiment trades so far, mean +0.217R, score +0.121
- ADD XAU_USD|sweep_bos|1m|sessions|at_equilibrium|2R|london: 63 experiment trades so far, mean +0.243R, score +0.052
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_break|3R|stop>=10sp: 255 experiment trades so far, mean +0.088R, score +0.038
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|ny_open: now 173 trades, mean +0.277R, last 180 days +0.185R over 108
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|2R|newyork+with_1h+with_4h: now 113 trades, mean +0.105R, last 180 days -0.004R over 72
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: now 91 trades, mean +0.116R, last 180 days -0.062R over 58
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|newyork+with_15m: now 154 trades, mean +0.131R, last 180 days +0.196R over 95

## v45 (written after 2021-11-12, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=6sp+newyork: 90 experiment trades so far, mean +0.134R, score +0.040
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=6sp+with_D: now 90 trades, mean +0.197R, last 180 days +0.182R over 43

## v46 (written after 2021-11-19, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h: 78 experiment trades so far, mean +0.611R, score +0.318
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 120 experiment trades so far, mean +0.114R, score +0.011
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|ny_open: now 141 trades, mean +0.466R, last 180 days +0.140R over 88
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|0.5R|stop>=10sp: now 83 trades, mean +0.094R, last 180 days -0.088R over 49

## v47 (written after 2021-11-26, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=6sp+with_D: 96 experiment trades so far, mean +0.246R, score +0.124
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=6sp+newyork: now 98 trades, mean +0.163R, last 180 days +0.019R over 58

## v48 (written after 2021-12-03, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|3R|stop>=6sp+with_D: 100 experiment trades so far, mean +0.215R, score +0.063
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|1R|ny_midday: 70 experiment trades so far, mean +0.133R, score +0.025
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|half1R_be3R|with_4h+with_D: now 69 trades, mean +0.249R, last 180 days +0.262R over 41
- DROP XAU_USD|sweep_bos|1m|sessions|at_equilibrium|2R|london: now 70 trades, mean +0.144R, last 180 days +0.065R over 51

## v49 (written after 2021-12-10, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|half1R_be3R|with_4h+with_D: 73 experiment trades so far, mean +0.300R, score +0.123
- ADD NAS100_USD|continuation|1h>1m|3R|ny_open+with_1h: 287 experiment trades so far, mean +0.067R, score +0.008
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|3R|stop>=6sp+with_D: now 104 trades, mean +0.263R, last 180 days +0.147R over 57
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_break|3R|stop>=10sp: now 306 trades, mean -0.019R, last 180 days -0.172R over 201

## v50 (written after 2021-12-17, used from the next trading day)
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|stop>=10sp: 192 experiment trades so far, mean +0.086R, score +0.017
- ADD NAS100_USD|sweep_bos|1m|sessions|at_break|2R|stop>=10sp: 121 experiment trades so far, mean +0.100R, score +0.010
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: now 129 trades, mean +0.112R, last 180 days +0.181R over 73
- DROP NAS100_USD|continuation|1h>1m|3R|ny_open+with_1h: now 297 trades, mean +0.058R, last 180 days +0.208R over 160

## v51 (written after 2021-12-27, used from the next trading day)
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|2R|stop>=10sp: 192 experiment trades so far, mean +0.078R, score +0.016
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|stop>=10sp: now 192 trades, mean +0.086R, last 180 days -0.189R over 123

## v52 (written after 2022-01-03, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 60 experiment trades so far, mean +0.639R, score +0.280
- ADD NAS100_USD|sweep_bos|5m|sessions|at_break|2R|with_1h: 60 experiment trades so far, mean +0.414R, score +0.159
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: 110 experiment trades so far, mean +0.279R, score +0.113
- ADD NAS100_USD|sweep_bos|1m|sessions|at_equilibrium|3R|stop>=10sp: 102 experiment trades so far, mean +0.264R, score +0.097
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h: now 93 trades, mean +0.411R, last 180 days +0.010R over 52
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|1R|ny_midday: now 72 trades, mean +0.128R, last 180 days +0.053R over 37
- DROP NAS100_USD|sweep_bos|1m|sessions|at_break|2R|stop>=10sp: now 129 trades, mean +0.123R, last 180 days +0.296R over 68
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|2R|stop>=10sp: now 193 trades, mean +0.087R, last 180 days -0.149R over 114

## v53 (written after 2022-01-10, used from the next trading day)


## v54 (written after 2022-01-17, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|half1R_be3R|asia: 61 experiment trades so far, mean +0.543R, score +0.254
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|2R|stop>=6sp+newyork: 108 experiment trades so far, mean +0.304R, score +0.151
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|half1R_be3R|with_4h+with_D: now 74 trades, mean +0.323R, last 180 days +0.473R over 32
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|stop>=6sp+with_D: now 109 trades, mean +0.205R, last 180 days +0.167R over 47

## v55 (written after 2022-01-31, used from the next trading day)


## v56 (written after 2022-02-07, used from the next trading day)
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|stop>=6sp+london: 76 experiment trades so far, mean +0.446R, score +0.181
- DROP NAS100_USD|sweep_bos|1m|sessions|at_equilibrium|3R|stop>=10sp: now 114 trades, mean +0.161R, last 180 days +0.243R over 54

## v57 (written after 2022-02-14, used from the next trading day)


## v58 (written after 2022-02-21, used from the next trading day)
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|2R|stop>=6sp+london: 77 experiment trades so far, mean +0.471R, score +0.223
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|2R|newyork+with_1h+with_4h: 123 experiment trades so far, mean +0.197R, score +0.079
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 152 experiment trades so far, mean +0.158R, score +0.058
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|stop>=6sp+london: now 77 trades, mean +0.427R, last 180 days +0.826R over 37
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: now 123 trades, mean +0.302R, last 180 days +0.373R over 59
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_gap|1R|stop>=6sp+with_D: now 120 trades, mean +0.067R, last 180 days -0.224R over 50

## v59 (written after 2022-02-28, used from the next trading day)


## v60 (written after 2022-03-07, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|asia: 68 experiment trades so far, mean +0.581R, score +0.272
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|newyork+with_D: 62 experiment trades so far, mean +0.334R, score +0.143
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_gap|1R|stop>=6sp+asia: 61 experiment trades so far, mean +0.322R, score +0.134
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|half1R_be3R|asia: now 68 trades, mean +0.503R, last 180 days +0.711R over 28
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|2R|stop>=6sp+newyork: now 117 trades, mean +0.253R, last 180 days +0.382R over 40
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: now 153 trades, mean +0.151R, last 180 days +0.215R over 66

## v61 (written after 2022-03-14, used from the next trading day)


## v62 (written after 2022-03-21, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|2R|stop>=6sp+newyork: 124 experiment trades so far, mean +0.278R, score +0.145
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|1R|newyork+with_D: now 66 trades, mean +0.283R, last 180 days +0.200R over 23

## v63 (written after 2022-03-28, used from the next trading day)


## v64 (written after 2022-04-04, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h: 166 experiment trades so far, mean +0.207R, score +0.127
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|1R|ny_midday: 91 experiment trades so far, mean +0.196R, score +0.084
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: now 64 trades, mean +0.580R, last 180 days -0.502R over 18
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: now 99 trades, mean +0.281R, last 180 days +0.008R over 32

## v65 (written after 2022-04-11, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|ny_open+with_1h: 69 experiment trades so far, mean +0.396R, score +0.170
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: 130 experiment trades so far, mean +0.270R, score +0.122
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|2R|newyork+with_1h+with_4h: now 130 trades, mean +0.187R, last 180 days +0.235R over 55
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|1R|ny_midday: now 92 trades, mean +0.205R, last 180 days +0.496R over 33

## v66 (written after 2022-04-19, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|1R|ny_midday: 92 experiment trades so far, mean +0.205R, score +0.091
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|ny_open+with_1h: now 69 trades, mean +0.396R, last 180 days -0.169R over 21

## v67 (written after 2022-04-26, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|newyork+with_1h: 60 experiment trades so far, mean +0.403R, score +0.132
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|1R|ny_midday: now 92 trades, mean +0.205R, last 180 days +0.464R over 31

## v68 (written after 2022-05-03, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: 183 experiment trades so far, mean +0.294R, score +0.182
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: now 256 trades, mean +0.234R, last 180 days +0.273R over 81

## v69 (written after 2022-05-10, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|1R|ny_midday: 96 experiment trades so far, mean +0.238R, score +0.118
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 175 experiment trades so far, mean +0.180R, score +0.083
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h: now 181 trades, mean +0.143R, last 180 days -0.096R over 64
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|newyork+with_1h: now 64 trades, mean +0.325R, last 180 days +0.650R over 22

## v70 (written after 2022-05-17, used from the next trading day)


## v71 (written after 2022-05-24, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h: 185 experiment trades so far, mean +0.151R, score +0.087
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: now 182 trades, mean +0.156R, last 180 days +0.236R over 62

## v72 (written after 2022-05-31, used from the next trading day)
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_break|3R|ny_open+with_1h: 80 experiment trades so far, mean +0.205R, score +0.076
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|2R|stop>=6sp+london: now 101 trades, mean +0.259R, last 180 days +0.331R over 41

## v73 (written after 2022-06-07, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|newyork+with_1h+with_4h: 77 experiment trades so far, mean +0.500R, score +0.252
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|with_1h: 65 experiment trades so far, mean +0.569R, score +0.234
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: 121 experiment trades so far, mean +0.257R, score +0.143
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|2R|stop>=6sp+newyork: now 154 trades, mean +0.311R, last 180 days +0.491R over 55
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h: now 192 trades, mean +0.182R, last 180 days -0.011R over 64
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_break|3R|ny_open+with_1h: now 80 trades, mean +0.205R, last 180 days +0.443R over 38

## v74 (written after 2022-06-14, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 78 experiment trades so far, mean +0.603R, score +0.306
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: 60 experiment trades so far, mean +0.605R, score +0.246
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|newyork+with_1h+with_4h: now 78 trades, mean +0.519R, last 180 days +0.258R over 24
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|1R|ny_midday: now 105 trades, mean +0.206R, last 180 days +0.375R over 33

## v75 (written after 2022-06-21, used from the next trading day)


## v76 (written after 2022-06-28, used from the next trading day)


## v77 (written after 2022-07-05, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 206 experiment trades so far, mean +0.202R, score +0.110
- DROP NAS100_USD|continuation|1h>5m|3R|newyork+with_D: now 284 trades, mean +0.173R, last 180 days +0.044R over 96

## v78 (written after 2022-07-12, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h: 198 experiment trades so far, mean +0.196R, score +0.126
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: now 125 trades, mean +0.249R, last 180 days +0.061R over 32

## v79 (written after 2022-07-19, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h: 125 experiment trades so far, mean +0.432R, score +0.257
- ADD NAS100_USD|continuation|1h>5m|3R|newyork+with_D: 290 experiment trades so far, mean +0.188R, score +0.124
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: now 81 trades, mean +0.544R, last 180 days +0.272R over 21
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_gap|1R|stop>=6sp+asia: now 76 trades, mean +0.231R, last 180 days -0.173R over 18

## v80 (written after 2022-07-26, used from the next trading day)


## v81 (written after 2022-08-02, used from the next trading day)


## v82 (written after 2022-08-09, used from the next trading day)
- ADD NAS100_USD|continuation|4h>5m|3R|newyork+with_1h+with_4h: 248 experiment trades so far, mean +0.162R, score +0.095
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: now 214 trades, mean +0.156R, last 180 days +0.132R over 63

## v83 (written after 2022-08-16, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|3R|with_4h+with_D: 120 experiment trades so far, mean +0.475R, score +0.274
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|asia: now 90 trades, mean +0.476R, last 180 days +0.180R over 24

## v84 (written after 2022-08-23, used from the next trading day)


## v85 (written after 2022-08-30, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 86 experiment trades so far, mean +0.584R, score +0.310
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h: now 131 trades, mean +0.459R, last 180 days +0.632R over 34

## v86 (written after 2022-09-06, used from the next trading day)


## v87 (written after 2022-09-13, used from the next trading day)


## v88 (written after 2022-09-20, used from the next trading day)


## v89 (written after 2022-09-27, used from the next trading day)


## v90 (written after 2022-10-04, used from the next trading day)


## v91 (written after 2022-10-11, used from the next trading day)
- ADD NAS100_USD|crt|1h>5m|half1R_3R|stop>=6sp+with_1h: 66 experiment trades so far, mean +0.230R, score +0.067
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: now 194 trades, mean +0.215R, last 180 days +0.141R over 62

## v92 (written after 2022-10-18, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: 196 experiment trades so far, mean +0.234R, score +0.126
- DROP NAS100_USD|crt|1h>5m|half1R_3R|stop>=6sp+with_1h: now 69 trades, mean +0.190R, last 180 days +0.183R over 24

## v93 (written after 2022-11-01, used from the next trading day)


## v94 (written after 2022-11-08, used from the next trading day)
- ADD NAS100_USD|continuation|1h>5m|3R|ny_midday: 297 experiment trades so far, mean +0.204R, score +0.137
- DROP NAS100_USD|continuation|1h>5m|3R|newyork+with_D: now 350 trades, mean +0.170R, last 180 days -0.053R over 92

## v95 (written after 2022-11-15, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|ny_open+with_1h: 94 experiment trades so far, mean +0.454R, score +0.234
- ADD NAS100_USD|sweep_bos|5m|sessions|at_break|2R|newyork+with_1h: 60 experiment trades so far, mean +0.512R, score +0.221
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: now 96 trades, mean +0.417R, last 180 days +0.345R over 26
- DROP NAS100_USD|sweep_bos|5m|sessions|at_break|2R|with_1h: now 114 trades, mean +0.315R, last 180 days +0.110R over 31
- DAY STOPS: stop after +1.0R / NoneR on the day (replayed on the last 250 days: 52% green, +92.9R)

## v96 (written after 2022-11-22, used from the next trading day)


## v97 (written after 2022-11-29, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|stop>=6sp+with_1h: 82 experiment trades so far, mean +0.379R, score +0.153
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|ny_open+with_1h: 70 experiment trades so far, mean +0.307R, score +0.089
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|with_1h: now 90 trades, mean +0.338R, last 180 days -0.264R over 25
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: now 78 trades, mean +0.345R, last 180 days -0.404R over 21

## v98 (written after 2022-12-06, used from the next trading day)


## v99 (written after 2022-12-13, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_block|3R|stop>=6sp+with_1h: 62 experiment trades so far, mean +0.338R, score +0.084
- DROP NAS100_USD|continuation|4h>5m|3R|newyork+with_1h+with_4h: now 293 trades, mean +0.168R, last 180 days +0.146R over 61

## v100 (written after 2022-12-20, used from the next trading day)


## v101 (written after 2022-12-28, used from the next trading day)


## v102 (written after 2023-01-12, used from the next trading day)


## v103 (written after 2023-01-19, used from the next trading day)
- ADD NAS100_USD|continuation|4h>5m|3R|newyork+with_1h+with_4h: 305 experiment trades so far, mean +0.168R, score +0.109
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|ny_open+with_1h: now 70 trades, mean +0.307R, last 180 days -0.467R over 7

## v104 (written after 2023-01-26, used from the next trading day)


## v105 (written after 2023-02-02, used from the next trading day)


## v106 (written after 2023-02-09, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_break|2R|stop>=6sp+with_1h: 124 experiment trades so far, mean +0.317R, score +0.178
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|ny_open+with_1h: 72 experiment trades so far, mean +0.382R, score +0.139
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|newyork+with_1h: 643 experiment trades so far, mean +0.140R, score +0.107
- DROP NAS100_USD|sweep_bos|5m|sessions|at_break|2R|newyork+with_1h: now 71 trades, mean +0.438R, last 180 days -0.104R over 16
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: now 302 trades, mean +0.222R, last 180 days +0.054R over 69
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|stop>=6sp+with_1h: now 91 trades, mean +0.336R, last 180 days -0.039R over 23

## v107 (written after 2023-02-16, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_break|2R|newyork+with_1h: 73 experiment trades so far, mean +0.481R, score +0.233
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: 311 experiment trades so far, mean +0.272R, score +0.197
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|stop>=6sp+with_1h: 94 experiment trades so far, mean +0.378R, score +0.172
- DROP NAS100_USD|sweep_bos|5m|sessions|at_break|2R|stop>=6sp+with_1h: now 127 trades, mean +0.333R, last 180 days +0.214R over 35
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|ny_open+with_1h: now 72 trades, mean +0.382R, last 180 days +0.300R over 9
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|newyork+with_1h: now 655 trades, mean +0.165R, last 180 days +0.111R over 164

## v108 (written after 2023-02-23, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|ny_open+with_1h: 75 experiment trades so far, mean +0.486R, score +0.210
- DROP NAS100_USD|continuation|4h>5m|3R|newyork+with_1h+with_4h: now 315 trades, mean +0.163R, last 180 days +0.153R over 62

## v109 (written after 2023-03-02, used from the next trading day)
- DAY STOPS: stop after +0.5R / NoneR on the day (replayed on the last 250 days: 53% green, +64.7R)

## v110 (written after 2023-03-09, used from the next trading day)


## v111 (written after 2023-03-16, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 315 experiment trades so far, mean +0.176R, score +0.109
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|3R|with_4h+with_D: now 169 trades, mean +0.279R, last 180 days -0.196R over 35
- DAY STOPS: stop after +1.0R / NoneR on the day (replayed on the last 250 days: 50% green, +52.7R)

## v112 (written after 2023-03-23, used from the next trading day)


## v113 (written after 2023-03-30, used from the next trading day)


## v114 (written after 2023-04-06, used from the next trading day)


## v115 (written after 2023-04-13, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|newyork+with_1h: 60 experiment trades so far, mean +0.865R, score +0.398
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|stop>=6sp+with_1h: now 104 trades, mean +0.355R, last 180 days +0.203R over 28
- DAY STOPS: stop after +0.5R / NoneR on the day (replayed on the last 250 days: 51% green, +65.1R)

## v116 (written after 2023-04-20, used from the next trading day)


## v117 (written after 2023-04-27, used from the next trading day)


## v118 (written after 2023-05-04, used from the next trading day)


## v119 (written after 2023-05-11, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|3R|stop>=6sp+london: 155 experiment trades so far, mean +0.247R, score +0.121
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h: now 307 trades, mean +0.153R, last 180 days -0.056R over 81

## v120 (written after 2023-05-18, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_break|3R|newyork+with_1h: 88 experiment trades so far, mean +0.491R, score +0.255
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|ny_open+with_1h: 201 experiment trades so far, mean +0.314R, score +0.194
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h: 309 experiment trades so far, mean +0.171R, score +0.122
- DROP NAS100_USD|sweep_bos|5m|sessions|at_break|2R|newyork+with_1h: now 88 trades, mean +0.439R, last 180 days +0.282R over 28
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: now 278 trades, mean +0.242R, last 180 days +0.351R over 71
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: now 347 trades, mean +0.150R, last 180 days +0.172R over 87

## v121 (written after 2023-05-25, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|ny_open+with_1h: 174 experiment trades so far, mean +0.190R, score +0.112
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h: now 309 trades, mean +0.171R, last 180 days +0.036R over 74

## v122 (written after 2023-06-08, used from the next trading day)


## v123 (written after 2023-06-15, used from the next trading day)


## v124 (written after 2023-06-22, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 364 experiment trades so far, mean +0.188R, score +0.124
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|3R|stop>=6sp+london: now 165 trades, mean +0.214R, last 180 days +0.577R over 48

## v125 (written after 2023-06-29, used from the next trading day)
- DAY STOPS: stop after +1.0R / NoneR on the day (replayed on the last 250 days: 51% green, +70.1R)

## v126 (written after 2023-07-20, used from the next trading day)


## v127 (written after 2023-07-27, used from the next trading day)


## v128 (written after 2023-08-03, used from the next trading day)


## v129 (written after 2023-08-10, used from the next trading day)
- ADD XAU_USD|sweep_bos|5m|sessions|at_gap|3R|stop>=6sp+discount: 118 experiment trades so far, mean +0.242R, score +0.101
- DROP NAS100_USD|sweep_bos|5m|sessions|at_block|3R|stop>=6sp+with_1h: now 90 trades, mean +0.302R, last 180 days -0.235R over 24
- DAY STOPS: stop after +0.5R / NoneR on the day (replayed on the last 250 days: 49% green, +63.8R)

## v130 (written after 2023-08-31, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h: 326 experiment trades so far, mean +0.157R, score +0.111
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|ny_open+with_1h: now 179 trades, mean +0.175R, last 180 days -0.116R over 22

## v131 (written after 2023-09-07, used from the next trading day)


## v132 (written after 2023-09-14, used from the next trading day)


## v133 (written after 2023-09-21, used from the next trading day)


## v134 (written after 2023-09-28, used from the next trading day)


## v135 (written after 2023-10-05, used from the next trading day)
- ADD NAS100_USD|continuation|4h>5m|3R|newyork+with_1h+with_4h: 403 experiment trades so far, mean +0.132R, score +0.086
- DROP NAS100_USD|continuation|1h>5m|3R|ny_midday: now 440 trades, mean +0.140R, last 180 days -0.061R over 75

## v136 (written after 2023-10-12, used from the next trading day)


## v137 (written after 2023-10-19, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|newyork+with_1h: 498 experiment trades so far, mean +0.141R, score +0.090
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|ny_open+with_1h: now 240 trades, mean +0.224R, last 180 days -0.294R over 42

## v138 (written after 2023-10-26, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h: 200 experiment trades so far, mean +0.280R, score +0.180
- ADD XAU_USD|sweep_bos|5m|sessions|at_break|3R|london+with_4h: 127 experiment trades so far, mean +0.197R, score +0.072
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|ny_open+with_1h: now 127 trades, mean +0.392R, last 180 days -0.276R over 14
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|newyork+with_1h: now 501 trades, mean +0.134R, last 180 days -0.023R over 106

## v139 (written after 2023-11-02, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|newyork+with_1h: 506 experiment trades so far, mean +0.154R, score +0.102
- DROP XAU_USD|sweep_bos|5m|sessions|at_break|3R|london+with_4h: now 128 trades, mean +0.187R, last 180 days +0.575R over 22

## v140 (written after 2023-11-09, used from the next trading day)
- ADD NAS100_USD|continuation|1h>5m|3R|ny_midday: 456 experiment trades so far, mean +0.144R, score +0.098
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|newyork+with_1h: now 511 trades, mean +0.142R, last 180 days -0.046R over 105

## v141 (written after 2023-11-16, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|ny_open: 452 experiment trades so far, mean +0.161R, score +0.110
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: 230 experiment trades so far, mean +0.151R, score +0.094
- ADD XAU_USD|sweep_bos|5m|sessions|at_break|3R|london+with_4h: 128 experiment trades so far, mean +0.187R, score +0.065
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|ny_open+with_1h: now 97 trades, mean +0.392R, last 180 days -0.357R over 7
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|newyork+with_1h: now 205 trades, mean +0.259R, last 180 days -0.115R over 20
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h: now 349 trades, mean +0.151R, last 180 days -0.004R over 40

## v142 (written after 2023-11-23, used from the next trading day)


## v143 (written after 2023-11-30, used from the next trading day)


## v144 (written after 2023-12-07, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|ny_open+with_1h: 296 experiment trades so far, mean +0.210R, score +0.133
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|2R|ny_open+with_1h: 99 experiment trades so far, mean +0.208R, score +0.078
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: now 446 trades, mean +0.166R, last 180 days +0.282R over 90
- DROP NAS100_USD|continuation|1h>5m|3R|ny_midday: now 464 trades, mean +0.133R, last 180 days -0.135R over 80

## v145 (written after 2023-12-14, used from the next trading day)
- ADD NAS100_USD|continuation|1h>5m|3R|ny_midday: 467 experiment trades so far, mean +0.146R, score +0.100
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|2R|ny_open+with_1h: now 99 trades, mean +0.208R, last 180 days -0.119R over 9

## v146 (written after 2023-12-21, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|3R|with_1h: 178 experiment trades so far, mean +0.152R, score +0.067
- DROP NAS100_USD|continuation|1h>5m|3R|ny_midday: now 474 trades, mean +0.133R, last 180 days -0.111R over 87

## v147 (written after 2023-12-29, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_block|3R|stop>=6sp+with_1h: 107 experiment trades so far, mean +0.312R, score +0.135
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|3R|with_1h: now 180 trades, mean +0.138R, last 180 days +0.194R over 33

## v148 (written after 2024-01-08, used from the next trading day)
- ADD NAS100_USD|continuation|1h>5m|3R|newyork+with_D: 556 experiment trades so far, mean +0.121R, score +0.084
- DROP NAS100_USD|sweep_bos|5m|sessions|at_block|3R|stop>=6sp+with_1h: now 107 trades, mean +0.312R, last 180 days +0.139R over 20

## v149 (written after 2024-01-15, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|3R|with_1h: 182 experiment trades so far, mean +0.147R, score +0.063
- DROP XAU_USD|sweep_bos|5m|sessions|at_break|3R|london+with_4h: now 135 trades, mean +0.153R, last 180 days +0.195R over 19

## v150 (written after 2024-01-22, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|ny_open+with_1h: 132 experiment trades so far, mean +0.391R, score +0.231
- ADD NAS100_USD|sweep_bos|5m|sessions|at_block|3R|stop>=6sp+with_1h: 108 experiment trades so far, mean +0.337R, score +0.153
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|ny_open: now 477 trades, mean +0.181R, last 180 days +0.489R over 80
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|3R|with_1h: now 182 trades, mean +0.147R, last 180 days +0.363R over 30

## v151 (written after 2024-01-29, used from the next trading day)
- ADD XAU_USD|sweep_bos|5m|sessions|at_gap|2R|stop>=10sp: 89 experiment trades so far, mean +0.197R, score +0.067
- DROP XAU_USD|sweep_bos|5m|sessions|at_gap|3R|stop>=6sp+discount: now 125 trades, mean +0.203R, last 180 days -0.461R over 7

## v152 (written after 2024-02-05, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|ny_open: 485 experiment trades so far, mean +0.161R, score +0.113
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|2R|stop>=6sp+london: 231 experiment trades so far, mean +0.127R, score +0.060
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|ny_open+with_1h: now 133 trades, mean +0.380R, last 180 days +0.139R over 12
- DROP XAU_USD|sweep_bos|5m|sessions|at_gap|2R|stop>=10sp: now 91 trades, mean +0.169R, last 180 days -0.419R over 7

## v153 (written after 2024-02-12, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|ny_open+with_1h: 257 experiment trades so far, mean +0.232R, score +0.141
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|ny_open+with_1h: 134 experiment trades so far, mean +0.247R, score +0.133
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|ny_open: now 486 trades, mean +0.159R, last 180 days +0.430R over 79
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|2R|stop>=6sp+london: now 231 trades, mean +0.127R, last 180 days +0.472R over 14

## v154 (written after 2024-02-19, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|stop>=6sp+with_1h: 142 experiment trades so far, mean +0.329R, score +0.180
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|ny_open: 490 experiment trades so far, mean +0.149R, score +0.102
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|2R|stop>=6sp+london: 231 experiment trades so far, mean +0.127R, score +0.060
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|3R|with_1h: 183 experiment trades so far, mean +0.141R, score +0.059
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|newyork+with_1h: now 80 trades, mean +0.804R, last 180 days +0.511R over 11
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|ny_open+with_1h: now 257 trades, mean +0.232R, last 180 days -0.082R over 41
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|ny_open+with_1h: now 135 trades, mean +0.238R, last 180 days +0.036R over 13
- DROP NAS100_USD|continuation|1h>5m|3R|newyork+with_D: now 584 trades, mean +0.119R, last 180 days +0.051R over 105

## v155 (written after 2024-02-26, used from the next trading day)


## v156 (written after 2024-03-04, used from the next trading day)
- DAY STOPS: stop after +NoneR / NoneR on the day (replayed on the last 250 days: 48% green, +67.6R)

## v157 (written after 2024-03-11, used from the next trading day)


## v158 (written after 2024-03-18, used from the next trading day)


## v159 (written after 2024-03-25, used from the next trading day)


## v160 (written after 2024-04-02, used from the next trading day)
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|stop>=6sp+london: 238 experiment trades so far, mean +0.179R, score +0.095
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|stop>=6sp+with_1h: 178 experiment trades so far, mean +0.145R, score +0.071
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|2R|stop>=6sp+london: now 238 trades, mean +0.143R, last 180 days +0.540R over 21
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|3R|with_1h: now 187 trades, mean +0.119R, last 180 days +0.264R over 25
- DAY STOPS: stop after +0.5R / NoneR on the day (replayed on the last 250 days: 48% green, +44.3R)

## v161 (written after 2024-04-09, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|newyork+with_15m: 139 experiment trades so far, mean +0.144R, score +0.047
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|3R|ny_open: now 508 trades, mean +0.117R, last 180 days -0.136R over 75
- DAY STOPS: stop after +1.0R / NoneR on the day (replayed on the last 250 days: 46% green, +56.6R)

## v162 (written after 2024-04-16, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|2R|ny_open+with_1h: 261 experiment trades so far, mean +0.130R, score +0.066
- DROP NAS100_USD|continuation|4h>5m|3R|newyork+with_1h+with_4h: now 516 trades, mean +0.085R, last 180 days -0.194R over 103
- DAY STOPS: stop after +0.5R / NoneR on the day (replayed on the last 250 days: 49% green, +45.0R)

## v163 (written after 2024-04-23, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|half1R_3R|ny_open+with_1h: 467 experiment trades so far, mean +0.204R, score +0.162
- ADD NAS100_USD|sweep_bos|5m|sessions|at_gap|1R|stop>=6sp+newyork: 90 experiment trades so far, mean +0.145R, score +0.049
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: now 467 trades, mean +0.248R, last 180 days +0.211R over 60
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|2R|ny_open+with_1h: now 267 trades, mean +0.102R, last 180 days -0.121R over 25
- DAY STOPS: stop after +1.0R / NoneR on the day (replayed on the last 250 days: 45% green, +46.2R)

## v164 (written after 2024-04-30, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: 470 experiment trades so far, mean +0.256R, score +0.200
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|half1R_3R|ny_open+with_1h: now 470 trades, mean +0.211R, last 180 days +0.266R over 59

## v165 (written after 2024-05-07, used from the next trading day)
- ADD NAS100_USD|continuation|4h>5m|3R|ny_open+with_1h: 138 experiment trades so far, mean +0.137R, score +0.043
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|newyork+with_15m: now 144 trades, mean +0.204R, last 180 days +1.268R over 16

## v166 (written after 2024-05-14, used from the next trading day)


## v167 (written after 2024-05-21, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|half1R_3R|ny_open+with_1h: 473 experiment trades so far, mean +0.208R, score +0.165
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|ny_open+with_1h: 211 experiment trades so far, mean +0.204R, score +0.133
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|half1R_be3R|newyork+with_D: 189 experiment trades so far, mean +0.129R, score +0.065
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: now 473 trades, mean +0.252R, last 180 days +0.289R over 54
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|stop>=6sp+with_1h: now 148 trades, mean +0.273R, last 180 days -0.527R over 13
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|newyork+with_1h+with_4h: now 258 trades, mean +0.165R, last 180 days +0.284R over 27
- DAY STOPS: stop after +0.5R / NoneR on the day (replayed on the last 250 days: 43% green, +31.9R)

## v168 (written after 2024-05-28, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: 473 experiment trades so far, mean +0.252R, score +0.196
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|stop>=6sp+with_1h: 148 experiment trades so far, mean +0.273R, score +0.141
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|ny_open: 538 experiment trades so far, mean +0.068R, score +0.034
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|half1R_3R|ny_open+with_1h: now 473 trades, mean +0.208R, last 180 days +0.307R over 50
- DROP NAS100_USD|sweep_bos|5m|sessions|at_block|3R|stop>=6sp+with_1h: now 115 trades, mean +0.251R, last 180 days -0.256R over 10
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|half1R_be3R|newyork+with_D: now 189 trades, mean +0.129R, last 180 days +0.398R over 19

## v169 (written after 2024-06-04, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|half1R_be3R|newyork+with_D: 192 experiment trades so far, mean +0.150R, score +0.082
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|2R|ny_open+with_1h: 332 experiment trades so far, mean +0.134R, score +0.080
- ADD XAU_USD|sweep_bos|5m|sessions|at_gap|3R|london: 86 experiment trades so far, mean +0.157R, score +0.006
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|ny_open+with_1h: now 332 trades, mean +0.193R, last 180 days +0.054R over 36
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|stop>=6sp+with_1h: now 149 trades, mean +0.265R, last 180 days -0.485R over 12
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|ny_open: now 540 trades, mean +0.063R, last 180 days -0.258R over 83

## v170 (written after 2024-06-11, used from the next trading day)
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|2R|ny_open+with_1h: now 332 trades, mean +0.134R, last 180 days +0.164R over 32

## v171 (written after 2024-06-18, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_block|3R|stop>=6sp+with_1h: 118 experiment trades so far, mean +0.286R, score +0.126
- ADD NAS100_USD|continuation|4h>5m|half1R_be3R|ny_open+with_1h: 140 experiment trades so far, mean +0.087R, score +0.021
- ADD NAS100_USD|sweep_bos|5m|sessions|at_gap|half1R_be3R|stop>=6sp+newyork: 94 experiment trades so far, mean +0.100R, score +0.017
- DROP NAS100_USD|sweep_bos|5m|sessions|at_gap|1R|stop>=6sp+newyork: now 94 trades, mean +0.159R, last 180 days +0.054R over 10
- DROP NAS100_USD|continuation|4h>5m|3R|ny_open+with_1h: now 140 trades, mean +0.120R, last 180 days -0.148R over 24
- DROP XAU_USD|sweep_bos|5m|sessions|at_gap|3R|london: now 87 trades, mean +0.143R, last 180 days -0.140R over 13

## v172 (written after 2024-06-25, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|london+with_1h: 60 experiment trades so far, mean +0.747R, score +0.354
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|ny_open+with_1h: 281 experiment trades so far, mean +0.192R, score +0.112
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|2R|ny_open+with_1h: 339 experiment trades so far, mean +0.119R, score +0.068
- ADD NAS100_USD|sweep_bos|5m|sessions|at_gap|1R|stop>=6sp+newyork: 94 experiment trades so far, mean +0.159R, score +0.061
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|stop>=6sp+with_1h: now 193 trades, mean +0.231R, last 180 days +1.101R over 22
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|stop>=6sp+london: now 255 trades, mean +0.097R, last 180 days -0.509R over 30
- DROP NAS100_USD|sweep_bos|5m|sessions|at_gap|half1R_be3R|stop>=6sp+newyork: now 94 trades, mean +0.100R, last 180 days +0.413R over 8

## v173 (written after 2024-07-09, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_break|2R|newyork+with_1h: 119 experiment trades so far, mean +0.345R, score +0.198
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|half1R_3R|ny_open+with_1h: 489 experiment trades so far, mean +0.175R, score +0.136
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|2R|ny_open+with_1h: 283 experiment trades so far, mean +0.123R, score +0.063
- ADD XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|london+with_4h: 280 experiment trades so far, mean +0.111R, score +0.041
- DROP NAS100_USD|sweep_bos|5m|sessions|at_break|3R|newyork+with_1h: now 119 trades, mean +0.383R, last 180 days +0.110R over 11
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: now 489 trades, mean +0.219R, last 180 days +0.073R over 59
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|ny_open+with_1h: now 283 trades, mean +0.198R, last 180 days +0.186R over 32
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|2R|ny_open+with_1h: now 341 trades, mean +0.112R, last 180 days -0.114R over 39

## v174 (written after 2024-07-16, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_break|3R|newyork+with_1h: 120 experiment trades so far, mean +0.371R, score +0.209
- ADD NAS100_USD|continuation|4h>15m|3R|ny_open: 147 experiment trades so far, mean +0.070R, score +0.003
- DROP NAS100_USD|sweep_bos|5m|sessions|at_break|2R|newyork+with_1h: now 120 trades, mean +0.334R, last 180 days -0.066R over 12
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|half1R_3R|ny_open+with_1h: now 493 trades, mean +0.166R, last 180 days -0.039R over 62
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|2R|ny_open+with_1h: now 287 trades, mean +0.117R, last 180 days +0.193R over 36
- DROP XAU_USD|sweep_bos|5m|pivots+sessions|at_gap|3R|london+with_4h: now 280 trades, mean +0.111R, last 180 days -0.006R over 53

## v175 (written after 2024-07-23, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|2R|ny_open+with_1h: 288 experiment trades so far, mean +0.124R, score +0.064

## v176 (written after 2024-07-30, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: 122 experiment trades so far, mean +0.269R, score +0.123
- DROP NAS100_USD|continuation|4h>15m|3R|ny_open: now 149 trades, mean +0.094R, last 180 days +0.325R over 25

## v177 (written after 2024-08-06, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: 497 experiment trades so far, mean +0.205R, score +0.155

## v178 (written after 2024-08-13, used from the next trading day)
- ADD NAS100_USD|continuation|4h>15m|3R|ny_open: 152 experiment trades so far, mean +0.081R, score +0.013
- ADD NAS100_USD|sweep_bos|5m|sessions|at_gap|1R|stop>=6sp+with_D: 135 experiment trades so far, mean +0.059R, score +0.002
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: now 498 trades, mean +0.203R, last 180 days -0.397R over 51
- DROP NAS100_USD|sweep_bos|5m|sessions|at_gap|1R|stop>=6sp+newyork: now 96 trades, mean +0.156R, last 180 days +0.235R over 8

## v179 (written after 2024-08-20, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: 499 experiment trades so far, mean +0.200R, score +0.151
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|stop>=6sp+with_1h: 200 experiment trades so far, mean +0.216R, score +0.134
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|ny_open+with_1h: 291 experiment trades so far, mean +0.177R, score +0.101
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|0.5R|ny_open+with_1h: 226 experiment trades so far, mean +0.133R, score +0.093
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|1R|ny_open+with_1h: 151 experiment trades so far, mean +0.084R, score +0.027
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_gap|2R|london+with_1h: now 60 trades, mean +0.747R, last 180 days +1.759R over 13
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: now 124 trades, mean +0.247R, last 180 days +0.326R over 16
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_break|3R|ny_open+with_1h: now 226 trades, mean +0.139R, last 180 days -0.161R over 26
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|2R|ny_open+with_1h: now 291 trades, mean +0.111R, last 180 days +0.007R over 34
- DROP NAS100_USD|continuation|4h>5m|half1R_be3R|ny_open+with_1h: now 143 trades, mean +0.079R, last 180 days -0.245R over 18

## v180 (written after 2024-08-27, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|newyork+with_1h: 250 experiment trades so far, mean +0.165R, score +0.102
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: now 505 trades, mean +0.186R, last 180 days -0.536R over 53
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|ny_open+with_1h: now 297 trades, mean +0.153R, last 180 days -0.336R over 39
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|1R|ny_open+with_1h: now 151 trades, mean +0.084R, last 180 days +0.242R over 16

## v181 (written after 2024-09-03, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_block|3R|newyork+with_1h+with_4h: 125 experiment trades so far, mean +0.269R, score +0.125
- DROP NAS100_USD|sweep_bos|5m|sessions|at_block|3R|stop>=6sp+with_1h: now 129 trades, mean +0.235R, last 180 days -0.247R over 20
- DROP NAS100_USD|sweep_bos|5m|sessions|at_gap|1R|stop>=6sp+with_D: now 138 trades, mean +0.035R, last 180 days +0.030R over 17

## v182 (written after 2024-09-10, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_gap|half1R_be3R|stop>=6sp+newyork: 101 experiment trades so far, mean +0.097R, score +0.017
- DROP NAS100_USD|continuation|4h>15m|3R|ny_open: now 156 trades, mean +0.063R, last 180 days +0.177R over 26

## v183 (written after 2024-09-17, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_block|3R|newyork+with_1h: 73 experiment trades so far, mean +0.760R, score +0.374
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|newyork+with_1h: 94 experiment trades so far, mean +0.659R, score +0.365
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: 516 experiment trades so far, mean +0.203R, score +0.154
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_block|3R|ny_open+with_1h: 307 experiment trades so far, mean +0.219R, score +0.140
- ADD NAS100_USD|sweep_bos|5m|sessions|at_gap|1R|stop>=6sp+newyork: 104 experiment trades so far, mean +0.161R, score +0.069
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|half1R_be3R|newyork+with_D: now 216 trades, mean +0.091R, last 180 days -0.194R over 33
- DROP NAS100_USD|sweep_bos|5m|sessions|at_gap|half1R_be3R|stop>=6sp+newyork: now 104 trades, mean +0.123R, last 180 days +0.545R over 15

## v184 (written after 2024-09-24, used from the next trading day)
- ADD NAS100_USD|continuation|4h>5m|half1R_be3R|ny_open+with_1h: 148 experiment trades so far, mean +0.091R, score +0.026
- DROP NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|3R|ny_open+with_1h: now 522 trades, mean +0.195R, last 180 days -0.367R over 64
- DAY STOPS: stop after +0.5R / -2.0R on the day (replayed on the last 250 days: 42% green, +10.5R)

## v185 (written after 2024-10-01, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|2R|newyork+with_1h: 98 experiment trades so far, mean +0.412R, score +0.219
- ADD XAU_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|0.5R|ny_open+with_1h: 106 experiment trades so far, mean +0.053R, score +0.007
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|newyork+with_1h: now 98 trades, mean +0.632R, last 180 days -0.130R over 18
- DROP NAS100_USD|continuation|4h>5m|half1R_be3R|ny_open+with_1h: now 148 trades, mean +0.091R, last 180 days +0.016R over 14

## v186 (written after 2024-10-08, used from the next trading day)


## v187 (written after 2024-10-15, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|3R|newyork+with_1h: 101 experiment trades so far, mean +0.662R, score +0.382
- DROP NAS100_USD|sweep_bos|5m|sessions|at_equilibrium|2R|newyork+with_1h: now 101 trades, mean +0.429R, last 180 days +0.236R over 20

## v188 (written after 2024-11-05, used from the next trading day)
- ADD NAS100_USD|continuation|4h>5m|3R|ny_open+with_1h: 151 experiment trades so far, mean +0.156R, score +0.062
- DROP XAU_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|0.5R|ny_open+with_1h: now 107 trades, mean +0.057R, last 180 days +0.392R over 15

## v189 (written after 2024-11-12, used from the next trading day)


## v190 (written after 2024-12-03, used from the next trading day)
- ADD NAS100_USD|sweep_bos|5m|pivots+sessions|at_equilibrium|3R|newyork+with_1h+with_4h: 624 experiment trades so far, mean +0.138R, score +0.096
- DROP NAS100_USD|continuation|4h>5m|3R|ny_open+with_1h: now 156 trades, mean +0.135R, last 180 days +0.187R over 17
- DAY STOPS: stop after +0.5R / NoneR on the day (replayed on the last 250 days: 43% green, +7.8R)

## v191 (written after 2024-12-10, used from the next trading day)


## v192 (written after 2024-12-17, used from the next trading day)
- ADD NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|ny_open+with_1h: 157 experiment trades so far, mean +0.245R, score +0.141
- DROP NAS100_USD|sweep_bos|15m|pivots+sessions|at_equilibrium|2R|newyork+with_1h: now 269 trades, mean +0.184R, last 180 days +0.378R over 44

## v193 (written after 2024-12-24, used from the next trading day)
- DAY STOPS: none
