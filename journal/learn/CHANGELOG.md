# Rulebook changelog

Each version is written after the day shown and used from the next trading day. ADD/DROP lines cite the experiment evidence behind the change.

## v2 (written after 2021-01-08, used from the next trading day)
- ADD NAS100_USD continuation|1h>1m (3R) when premium and stop>=3sp: 63 past trades, +0.108R average, 29% winners, positive in every past year (worst year shrunk +0.072R)

## v3 (written after 2021-01-15, used from the next trading day)
- BENCH NAS100_USD|continuation|1h>1m|3R|premium+stop>=3sp: its own strategy trades lost -0.653R over the last 20 (until ~3 months)
- ADD NAS100_USD continuation|1h>1m (3R) when premium and stop>=3sp and with_1h: 63 past trades, +0.108R average, 29% winners, positive in every past year (worst year shrunk +0.072R)
- DROP NAS100_USD continuation|1h>1m (3R) when premium+stop>=3sp: no longer among the best patterns that held in every past year

## v4 (written after 2021-02-05, used from the next trading day)
- ADD NAS100_USD sweep_bos|5m|pivots+sessions|at_break (2R) when against_D and stop>=12sp: 40 past trades, +0.634R average, 60% winners, positive in every past year (worst year shrunk +0.362R)
- ADD NAS100_USD sweep_bos|5m|pivots+sessions|at_break (3R) when premium and quiet_day and with_1h: 44 past trades, +0.577R average, 50% winners, positive in every past year (worst year shrunk +0.335R)
- ADD NAS100_USD sweep_bos|5m|pivots+sessions|at_break (half1R_be3R) when quiet_day and stop>=12sp: 49 past trades, +0.399R average, 71% winners, positive in every past year (worst year shrunk +0.239R)
- ADD NAS100_USD sweep_bos|5m|pivots+sessions|at_break (half1R_3R) when quiet_day and stop>=12sp: 49 past trades, +0.409R average, 51% winners, positive in every past year (worst year shrunk +0.226R)
- ADD XAU_USD sweep_bos|15m|pivots+sessions|at_break (3R) when short: 48 past trades, +0.395R average, 46% winners, positive in every past year (worst year shrunk +0.199R)
- ADD NAS100_USD sweep_bos|5m|pivots+sessions|at_equilibrium (3R) when discount and midweek and votes<=1: 43 past trades, +0.453R average, 40% winners, positive in every past year (worst year shrunk +0.187R)
- DROP NAS100_USD continuation|1h>1m (3R) when premium+stop>=3sp+with_1h: no longer among the best patterns that held in every past year

## v5 (written after 2021-02-26, used from the next trading day)
- BENCH NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|against_D+stop>=12sp: its own strategy trades lost -0.210R over the last 16 (until ~3 months)
- ADD NAS100_USD sweep_bos|5m|pivots+sessions|at_break (2R) when against_D and stop>=12sp and stop>=3sp: 40 past trades, +0.634R average, 60% winners, positive in every past year (worst year shrunk +0.362R)
- DROP NAS100_USD sweep_bos|5m|pivots+sessions|at_break (2R) when against_D+stop>=12sp: no longer among the best patterns that held in every past year
- DAY STOPS: stop after 0.5R / NoneR on the day (replay of the last 40 days: 59% of trading days green, +26.0R)

## v6 (written after 2021-03-05, used from the next trading day)
- ADD NAS100_USD sweep_bos|5m|pivots+sessions|at_break (3R) when against_1h and against_D and long: 53 past trades, +0.771R average, 47% winners, positive in every past year (worst year shrunk +0.475R)
- ADD XAU_USD sweep_bos|15m|pivots+sessions|at_break (3R) when short and stop>=6sp: 54 past trades, +0.613R average, 50% winners, positive in every past year (worst year shrunk +0.326R)
- ADD NAS100_USD sweep_bos|5m|pivots+sessions|at_equilibrium (3R) when against_D and long and votes<=1: 42 past trades, +0.636R average, 43% winners, positive in every past year (worst year shrunk +0.315R)
- ADD XAU_USD sweep_bos|15m|pivots+sessions|at_break (2R) when prominent_pool and short: 64 past trades, +0.437R average, 50% winners, positive in every past year (worst year shrunk +0.292R)
- ADD XAU_USD sweep_bos|5m|pivots+sessions|at_break (3R) when between and stop>=6sp: 41 past trades, +0.533R average, 56% winners, positive in every past year (worst year shrunk +0.281R)
- ADD NAS100_USD sweep_bos|5m|pivots+sessions|at_break (2R) when against_D and long and stop>=6sp: 67 past trades, +0.427R average, 52% winners, positive in every past year (worst year shrunk +0.273R)
- DROP NAS100_USD sweep_bos|5m|pivots+sessions|at_break (2R) when against_D+stop>=12sp+stop>=3sp: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|pivots+sessions|at_break (3R) when premium+quiet_day+with_1h: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|pivots+sessions|at_break (half1R_be3R) when quiet_day+stop>=12sp: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|pivots+sessions|at_break (half1R_3R) when quiet_day+stop>=12sp: no longer among the best patterns that held in every past year
- DROP XAU_USD sweep_bos|15m|pivots+sessions|at_break (3R) when short: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|pivots+sessions|at_equilibrium (3R) when discount+midweek+votes<=1: no longer among the best patterns that held in every past year

## v7 (written after 2021-03-26, used from the next trading day)
- BENCH XAU_USD|sweep_bos|15m|pivots+sessions|at_break|2R|prominent_pool+short: its own strategy trades lost -0.446R over the last 18 (until ~3 months)
- ADD XAU_USD sweep_bos|15m|pivots+sessions|at_break (2R) when prominent_pool and short and with_15m: 64 past trades, +0.437R average, 50% winners, positive in every past year (worst year shrunk +0.292R)
- DROP XAU_USD sweep_bos|15m|pivots+sessions|at_break (2R) when prominent_pool+short: no longer among the best patterns that held in every past year

## v8 (written after 2021-04-02, used from the next trading day)
- ADD NAS100_USD sweep_bos|5m|pivots+sessions|at_break (3R) when against_D and mon and prominent_pool: 45 past trades, +0.790R average, 49% winners, positive in every past year (worst year shrunk +0.460R)
- ADD NAS100_USD sweep_bos|5m|pivots+sessions|at_break (2R) when against_D and mon and stop>=6sp: 41 past trades, +0.739R average, 61% winners, positive in every past year (worst year shrunk +0.397R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when ny_open: 41 past trades, +0.955R average, 61% winners, positive in every past year (worst year shrunk +0.395R)
- ADD NAS100_USD sweep_bos|5m|pivots+sessions|at_break (half1R_3R) when against_1h and against_D and mon: 41 past trades, +0.675R average, 51% winners, positive in every past year (worst year shrunk +0.387R)
- ADD XAU_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when stop>=3sp and with_1h: 40 past trades, +0.685R average, 50% winners, positive in every past year (worst year shrunk +0.377R)
- ADD NAS100_USD sweep_bos|5m|pivots+sessions|at_equilibrium (3R) when mon and premium and stop>=3sp: 40 past trades, +0.793R average, 48% winners, positive in every past year (worst year shrunk +0.353R)
- DROP NAS100_USD sweep_bos|5m|pivots+sessions|at_break (3R) when against_1h+against_D+long: no longer among the best patterns that held in every past year
- DROP XAU_USD sweep_bos|15m|pivots+sessions|at_break (3R) when short+stop>=6sp: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|pivots+sessions|at_equilibrium (3R) when against_D+long+votes<=1: no longer among the best patterns that held in every past year
- DROP XAU_USD sweep_bos|15m|pivots+sessions|at_break (2R) when prominent_pool+short+with_15m: no longer among the best patterns that held in every past year
- DROP XAU_USD sweep_bos|5m|pivots+sessions|at_break (3R) when between+stop>=6sp: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|pivots+sessions|at_break (2R) when against_D+long+stop>=6sp: no longer among the best patterns that held in every past year

## v9 (written after 2021-04-16, used from the next trading day)
- BENCH NAS100_USD|continuation|1h>1m|3R|premium+stop>=3sp: its own strategy trades lost -0.653R over the last 20 (until ~3 months)

## v10 (written after 2021-04-30, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_break (3R) when midweek and premium and with_D: 49 past trades, +0.837R average, 61% winners, positive in every past year (worst year shrunk +0.491R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (2R) when ny_open: 51 past trades, +0.731R average, 63% winners, positive in every past year (worst year shrunk +0.457R)
- ADD XAU_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when inside_pd and stop>=3sp and with_1h: 47 past trades, +0.734R average, 53% winners, positive in every past year (worst year shrunk +0.446R)
- ADD XAU_USD sweep_bos|15m|pivots+sessions|at_break (2R) when inside_pd and midweek and with_1h: 48 past trades, +0.730R average, 62% winners, positive in every past year (worst year shrunk +0.429R)
- ADD XAU_USD sweep_bos|15m|pivots+sessions|at_break (3R) when quiet_day and with_1h: 55 past trades, +0.719R average, 55% winners, positive in every past year (worst year shrunk +0.424R)
- DROP NAS100_USD sweep_bos|5m|pivots+sessions|at_break (3R) when against_D+mon+prominent_pool: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|pivots+sessions|at_break (2R) when against_D+mon+stop>=6sp: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|pivots+sessions|at_break (half1R_3R) when against_1h+against_D+mon: no longer among the best patterns that held in every past year
- DROP XAU_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when stop>=3sp+with_1h: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|pivots+sessions|at_equilibrium (3R) when mon+premium+stop>=3sp: no longer among the best patterns that held in every past year
- DAY STOPS: stop after 1.0R / NoneR on the day (replay of the last 85 days: 62% of trading days green, +53.2R)

## v11 (written after 2021-05-28, used from the next trading day)
- BENCH NAS100_USD|continuation|1h>1m|3R|premium+stop>=3sp+with_1h: its own strategy trades lost -0.391R over the last 26 (until ~3 months)
- BENCH NAS100_USD|sweep_bos|5m|pivots+sessions|at_break|2R|against_D+stop>=12sp: its own strategy trades lost -0.210R over the last 16 (until ~3 months)
- BENCH NAS100_USD (non-CRT): its strategy trades lost -0.185R over the last 115
- ADD XAU_USD sweep_bos|15m|pivots+sessions|at_gap (1R) when premium and quiet_day and stop>=6sp: 43 past trades, +0.657R average, 84% winners, positive in every past year (worst year shrunk +0.373R)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when ny_open: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_break (3R) when midweek+premium+with_D: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (2R) when ny_open: no longer among the best patterns that held in every past year
- DROP XAU_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when inside_pd+stop>=3sp+with_1h: no longer among the best patterns that held in every past year
- DROP XAU_USD sweep_bos|15m|pivots+sessions|at_break (2R) when inside_pd+midweek+with_1h: no longer among the best patterns that held in every past year
- DROP XAU_USD sweep_bos|15m|pivots+sessions|at_break (3R) when quiet_day+with_1h: no longer among the best patterns that held in every past year
- DAY STOPS: stop after NoneR / -1.0R on the day (replay of the last 105 days: 75% of trading days green, +10.6R)

## v12 (written after 2021-06-25, used from the next trading day)
- BENCH XAU_USD|sweep_bos|15m|pivots+sessions|at_break|2R|prominent_pool+short: its own strategy trades lost -0.446R over the last 18 (until ~3 months)
- BENCH XAU_USD (non-CRT): its strategy trades lost -0.229R over the last 66
- DROP XAU_USD sweep_bos|15m|pivots+sessions|at_gap (1R) when premium+quiet_day+stop>=6sp: no longer among the best patterns that held in every past year
- DAY STOPS: none

## v13 (written after 2021-08-27, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when long and newyork and premium: 59 past trades, +0.980R average, 61% winners, positive in every past year (worst year shrunk +0.640R)
- ADD NAS100_USD sweep_bos|5m|pivots+sessions|at_break (3R) when beyond_pd and long and newyork: 42 past trades, +0.995R average, 71% winners, positive in every past year (worst year shrunk +0.557R)
- ADD NAS100_USD sweep_bos|5m|pivots+sessions|at_break (2R) when beyond_pd and long and newyork: 42 past trades, +0.823R average, 74% winners, positive in every past year (worst year shrunk +0.460R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when against_1h and long and with_D: 41 past trades, +0.891R average, 56% winners, positive in every past year (worst year shrunk +0.450R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_break (3R) when long and ny_open and premium: 51 past trades, +0.735R average, 75% winners, positive in every past year (worst year shrunk +0.444R)
- ADD NAS100_USD sweep_bos|5m|pivots+sessions|at_block (2R) when between and votes<=1: 49 past trades, +0.765R average, 61% winners, positive in every past year (worst year shrunk +0.417R)
- DAY STOPS: stop after NoneR / -2.0R on the day (replay of the last 170 days: 58% of trading days green, +76.4R)

## v14 (written after 2021-09-17, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when against_1h and premium and with_D: 82 past trades, +0.910R average, 52% winners, positive in every past year (worst year shrunk +0.650R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_break (3R) when beyond_pd and premium and stop>=6sp: 43 past trades, +0.949R average, 79% winners, positive in every past year (worst year shrunk +0.531R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (half1R_3R) when against_1h and premium and with_D: 82 past trades, +0.650R average, 52% winners, positive in every past year (worst year shrunk +0.434R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (2R) when long and premium and with_4h: 86 past trades, +0.588R average, 59% winners, positive in every past year (worst year shrunk +0.423R)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when long+newyork+premium: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when against_1h+long+with_D: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_break (3R) when long+ny_open+premium: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|pivots+sessions|at_block (2R) when between+votes<=1: no longer among the best patterns that held in every past year
- DAY STOPS: stop after NoneR / NoneR on the day (replay of the last 185 days: 58% of trading days green, +72.1R)

## v15 (written after 2021-10-15, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when premium and stop>=6sp and with_D: 54 past trades, +0.827R average, 59% winners, positive in every past year (worst year shrunk +0.467R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_break (half1R_be3R) when asia and midweek and with_D: 59 past trades, +0.628R average, 69% winners, positive in every past year (worst year shrunk +0.415R)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (half1R_3R) when against_1h+premium+with_D: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (2R) when long+premium+with_4h: no longer among the best patterns that held in every past year

## v16 (written after 2021-11-12, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when premium and with_D: 57 past trades, +0.869R average, 60% winners, positive in every past year (worst year shrunk +0.562R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_break (3R) when beyond_pd and premium: 53 past trades, +0.883R average, 75% winners, positive in every past year (worst year shrunk +0.543R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (half1R_be3R) when premium and quiet_day and with_D: 45 past trades, +0.775R average, 84% winners, positive in every past year (worst year shrunk +0.450R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_break (2R) when beyond_pd and premium and stop>=6sp: 51 past trades, +0.749R average, 78% winners, positive in every past year (worst year shrunk +0.443R)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when premium+stop>=6sp+with_D: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_break (3R) when beyond_pd+premium+stop>=6sp: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|pivots+sessions|at_break (2R) when beyond_pd+long+newyork: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_break (half1R_be3R) when asia+midweek+with_D: no longer among the best patterns that held in every past year

## v17 (written after 2021-12-10, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when beyond_pd and stop>=12sp: 41 past trades, +1.175R average, 71% winners, positive in every past year (worst year shrunk +0.617R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_break (3R) when beyond_pd and long: 46 past trades, +1.147R average, 74% winners, positive in every past year (worst year shrunk +0.587R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when long and premium and with_D: 51 past trades, +0.974R average, 67% winners, positive in every past year (worst year shrunk +0.586R)
- ADD NAS100_USD continuation|1h>5m (3R) when mon and premium and with_D: 104 past trades, +0.691R average, 50% winners, positive in every past year (worst year shrunk +0.501R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (2R) when beyond_pd and stop>=12sp: 41 past trades, +0.919R average, 73% winners, positive in every past year (worst year shrunk +0.494R)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when against_1h+premium+with_D: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when premium+with_D: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_break (3R) when beyond_pd+premium: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (half1R_be3R) when premium+quiet_day+with_D: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_break (2R) when beyond_pd+premium+stop>=6sp: no longer among the best patterns that held in every past year

## v18 (written after 2022-01-10, used from the next trading day)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when beyond_pd+stop>=12sp: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_break (3R) when beyond_pd+long: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when long+premium+with_D: no longer among the best patterns that held in every past year
- DROP NAS100_USD continuation|1h>5m (3R) when mon+premium+with_D: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|pivots+sessions|at_break (3R) when beyond_pd+long+newyork: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (2R) when beyond_pd+stop>=12sp: no longer among the best patterns that held in every past year

## v19 (written after 2022-01-17, used from the next trading day)
- ADD NAS100_USD continuation|1h>5m (3R) when newyork and stop>=12sp and votes>=3: 212 past trades, +0.156R average, 45% winners, positive in every past year (worst year shrunk +0.132R)
- ADD NAS100_USD sweep_bos|5m|pivots+sessions|at_break (3R) when ny_open and pred_low_third: 139 past trades, +0.252R average, 45% winners, positive in every past year (worst year shrunk +0.121R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (2R) when premium and stop>=12sp: 271 past trades, +0.129R average, 44% winners, positive in every past year (worst year shrunk +0.110R)
- ADD NAS100_USD continuation|1h>5m (2R) when newyork and stop>=12sp and votes>=3: 212 past trades, +0.085R average, 46% winners, positive in every past year (worst year shrunk +0.072R)
- ADD NAS100_USD continuation|1h>1m (3R) when busy_day and newyork and premium: 212 past trades, +0.086R average, 36% winners, positive in every past year (worst year shrunk +0.069R)
- ADD NAS100_USD continuation|1h>5m (half1R_3R) when newyork and stop>=12sp and votes>=3: 212 past trades, +0.076R average, 47% winners, positive in every past year (worst year shrunk +0.058R)
- DAY STOPS: stop after 0.5R / NoneR on the day (replay of the last 250 days: 52% of trading days green, +33.2R)

## v20 (written after 2022-02-07, used from the next trading day)
- ADD NAS100_USD continuation|1h>5m (3R) when mon and stop>=12sp and with_D: 93 past trades, +0.685R average, 52% winners, positive in every past year (worst year shrunk +0.310R)
- ADD NAS100_USD continuation|1h>1m (3R) when busy_day and short and with_15m: 49 past trades, +0.575R average, 43% winners, positive in every past year (worst year shrunk +0.291R)
- ADD NAS100_USD sweep_bos|5m|pivots+sessions|at_break (3R) when ny_open and pred_low_third and room_pd>=2R: 125 past trades, +0.385R average, 47% winners, positive in every past year (worst year shrunk +0.286R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (2R) when premium and stop>=6sp and with_D: 191 past trades, +0.323R average, 49% winners, positive in every past year (worst year shrunk +0.276R)
- ADD NAS100_USD continuation|1h>5m (2R) when mon and stop>=12sp and with_D: 93 past trades, +0.480R average, 56% winners, positive in every past year (worst year shrunk +0.236R)
- ADD NAS100_USD sweep_bos|5m|sessions|at_equilibrium (2R) when discount and inside_pd and stop>=12sp: 111 past trades, +0.285R average, 46% winners, positive in every past year (worst year shrunk +0.211R)
- DROP NAS100_USD continuation|1h>5m (3R) when newyork+stop>=12sp+votes>=3: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|pivots+sessions|at_break (3R) when ny_open+pred_low_third: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (2R) when premium+stop>=12sp: no longer among the best patterns that held in every past year
- DROP NAS100_USD continuation|1h>5m (2R) when newyork+stop>=12sp+votes>=3: no longer among the best patterns that held in every past year
- DROP NAS100_USD continuation|1h>1m (3R) when busy_day+newyork+premium: no longer among the best patterns that held in every past year
- DROP NAS100_USD continuation|1h>5m (half1R_3R) when newyork+stop>=12sp+votes>=3: no longer among the best patterns that held in every past year

## v21 (written after 2022-03-07, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (2R) when against_1h and stop>=12sp and with_D: 59 past trades, +0.773R average, 63% winners, positive in every past year (worst year shrunk +0.496R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when long and premium and with_D: 154 past trades, +0.691R average, 51% winners, positive in every past year (worst year shrunk +0.390R)
- ADD NAS100_USD continuation|1h>1m (3R) when beyond_pd and ny_midday and pred_high_third: 49 past trades, +0.675R average, 47% winners, positive in every past year (worst year shrunk +0.358R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (2R) when midweek and premium and with_D: 130 past trades, +0.509R average, 56% winners, positive in every past year (worst year shrunk +0.345R)
- ADD NAS100_USD sweep_bos|1m|sessions|at_break (3R) when against_1h and pred_low_third and stop>=12sp: 58 past trades, +0.499R average, 41% winners, positive in every past year (worst year shrunk +0.325R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (half1R_be3R) when against_1h and stop>=12sp and with_D: 59 past trades, +0.523R average, 66% winners, positive in every past year (worst year shrunk +0.296R)
- DROP NAS100_USD continuation|1h>5m (3R) when mon+stop>=12sp+with_D: no longer among the best patterns that held in every past year
- DROP NAS100_USD continuation|1h>1m (3R) when busy_day+short+with_15m: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|pivots+sessions|at_break (3R) when ny_open+pred_low_third+room_pd>=2R: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (2R) when premium+stop>=6sp+with_D: no longer among the best patterns that held in every past year
- DROP NAS100_USD continuation|1h>5m (2R) when mon+stop>=12sp+with_D: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|sessions|at_equilibrium (2R) when discount+inside_pd+stop>=12sp: no longer among the best patterns that held in every past year

## v22 (written after 2022-04-04, used from the next trading day)
- ADD XAU_USD sweep_bos|5m|pivots+sessions|at_break (3R) when between and long and with_1h: 79 past trades, +0.728R average, 56% winners, positive in every past year (worst year shrunk +0.434R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (2R) when long and premium and with_4h: 129 past trades, +0.526R average, 57% winners, positive in every past year (worst year shrunk +0.411R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when inside_pd and pred_high_third and premium: 43 past trades, +0.697R average, 44% winners, positive in every past year (worst year shrunk +0.403R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_break (3R) when long and premium and with_4h: 199 past trades, +0.505R average, 57% winners, positive in every past year (worst year shrunk +0.397R)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when long+premium+with_D: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (2R) when midweek+premium+with_D: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|1m|sessions|at_break (3R) when against_1h+pred_low_third+stop>=12sp: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (half1R_be3R) when against_1h+stop>=12sp+with_D: no longer among the best patterns that held in every past year

## v23 (written after 2022-05-03, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when inside_pd and premium and with_D: 86 past trades, +0.816R average, 56% winners, positive in every past year (worst year shrunk +0.596R)
- ADD XAU_USD sweep_bos|5m|pivots+sessions|at_break (3R) when between and discount and with_1h: 49 past trades, +0.855R average, 55% winners, positive in every past year (worst year shrunk +0.482R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (2R) when against_1h and inside_pd and votes>=3: 55 past trades, +0.720R average, 62% winners, positive in every past year (worst year shrunk +0.463R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when asia and long and midweek: 80 past trades, +0.692R average, 44% winners, positive in every past year (worst year shrunk +0.459R)
- ADD NAS100_USD sweep_bos|5m|pivots+sessions|at_break (3R) when discount and ny_open and quiet_day: 79 past trades, +0.599R average, 49% winners, positive in every past year (worst year shrunk +0.422R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_break (3R) when against_1h and premium and with_D: 215 past trades, +0.488R average, 51% winners, positive in every past year (worst year shrunk +0.419R)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (2R) when against_1h+stop>=12sp+with_D: no longer among the best patterns that held in every past year
- DROP XAU_USD sweep_bos|5m|pivots+sessions|at_break (3R) when between+long+with_1h: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (2R) when long+premium+with_4h: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when inside_pd+pred_high_third+premium: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_break (3R) when long+premium+with_4h: no longer among the best patterns that held in every past year
- DROP NAS100_USD continuation|1h>1m (3R) when beyond_pd+ny_midday+pred_high_third: no longer among the best patterns that held in every past year
- DAY STOPS: stop after NoneR / NoneR on the day (replay of the last 250 days: 48% of trading days green, +80.4R)

## v24 (written after 2022-05-31, used from the next trading day)
- ADD XAU_USD sweep_bos|5m|pivots+sessions|at_break (3R) when between and room_pd>=2R and votes>=3: 41 past trades, +1.227R average, 63% winners, positive in every past year (worst year shrunk +0.626R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when against_1h and premium and with_4h: 54 past trades, +0.925R average, 61% winners, positive in every past year (worst year shrunk +0.571R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (2R) when asia and inside_pd and midweek: 50 past trades, +0.896R average, 64% winners, positive in every past year (worst year shrunk +0.550R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (half1R_be3R) when against_1h and inside_pd and votes>=3: 57 past trades, +0.792R average, 74% winners, positive in every past year (worst year shrunk +0.516R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (half1R_3R) when against_1h and inside_pd and votes>=3: 57 past trades, +0.703R average, 54% winners, positive in every past year (worst year shrunk +0.437R)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when inside_pd+premium+with_D: no longer among the best patterns that held in every past year
- DROP XAU_USD sweep_bos|5m|pivots+sessions|at_break (3R) when between+discount+with_1h: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (2R) when against_1h+inside_pd+votes>=3: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when asia+long+midweek: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|pivots+sessions|at_break (3R) when discount+ny_open+quiet_day: no longer among the best patterns that held in every past year
- DAY STOPS: stop after 0.5R / NoneR on the day (replay of the last 250 days: 55% of trading days green, +91.8R)

## v25 (written after 2022-06-28, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when long and premium and votes>=3: 144 past trades, +0.754R average, 53% winners, positive in every past year (worst year shrunk +0.589R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when premium and votes>=3 and with_4h: 81 past trades, +0.773R average, 54% winners, positive in every past year (worst year shrunk +0.551R)
- ADD NAS100_USD sweep_bos|5m|pivots+sessions|at_break (3R) when ny_open and pred_low_third and quiet_day: 73 past trades, +0.832R average, 55% winners, positive in every past year (worst year shrunk +0.539R)
- ADD NAS100_USD sweep_bos|5m|sessions|at_equilibrium (3R) when midweek and with_1h: 44 past trades, +0.892R average, 52% winners, positive in every past year (worst year shrunk +0.499R)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when against_1h+premium+with_4h: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (half1R_be3R) when against_1h+inside_pd+votes>=3: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (half1R_3R) when against_1h+inside_pd+votes>=3: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_break (3R) when against_1h+premium+with_D: no longer among the best patterns that held in every past year
- DAY STOPS: stop after 2.0R / NoneR on the day (replay of the last 250 days: 53% of trading days green, +111.9R)

## v26 (written after 2022-07-26, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (2R) when asia and long: 46 past trades, +1.266R average, 76% winners, positive in every past year (worst year shrunk +0.600R)
- ADD NAS100_USD sweep_bos|5m|pivots+sessions|at_break (3R) when ny_open and pred_low_third and with_1h: 43 past trades, +0.949R average, 65% winners, positive in every past year (worst year shrunk +0.549R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (half1R_be3R) when against_1h and quiet_day and votes>=3: 42 past trades, +0.982R average, 83% winners, positive in every past year (worst year shrunk +0.522R)
- DROP NAS100_USD sweep_bos|5m|pivots+sessions|at_break (3R) when ny_open+pred_low_third+quiet_day: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|sessions|at_equilibrium (3R) when midweek+with_1h: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (2R) when asia+inside_pd+midweek: no longer among the best patterns that held in every past year

## v27 (written after 2022-08-23, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when against_1h and pred_mid and votes>=3: 42 past trades, +1.387R average, 64% winners, positive in every past year (worst year shrunk +0.775R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when long and ny_open and votes>=3: 69 past trades, +0.929R average, 61% winners, positive in every past year (worst year shrunk +0.597R)
- ADD NAS100_USD sweep_bos|5m|sessions|at_equilibrium (3R) when newyork and with_1h: 40 past trades, +1.110R average, 60% winners, positive in every past year (worst year shrunk +0.589R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (2R) when asia and long and stop>=6sp: 45 past trades, +1.250R average, 76% winners, positive in every past year (worst year shrunk +0.541R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (half1R_be3R) when long and premium and votes>=3: 57 past trades, +0.789R average, 82% winners, positive in every past year (worst year shrunk +0.503R)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (2R) when asia+long: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when long+premium+votes>=3: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when premium+votes>=3+with_4h: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|pivots+sessions|at_break (3R) when ny_open+pred_low_third+with_1h: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (half1R_be3R) when against_1h+quiet_day+votes>=3: no longer among the best patterns that held in every past year
- DAY STOPS: stop after NoneR / NoneR on the day (replay of the last 250 days: 66% of trading days green, +110.9R)

## v28 (written after 2022-09-20, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when long and ny_open and with_4h: 68 past trades, +1.122R average, 63% winners, positive in every past year (worst year shrunk +0.747R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when long and premium and with_4h: 61 past trades, +0.862R average, 61% winners, positive in every past year (worst year shrunk +0.556R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_break (2R) when between and pred_low_third: 40 past trades, +1.025R average, 72% winners, positive in every past year (worst year shrunk +0.513R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (2R) when long and ny_open and votes>=3: 76 past trades, +0.692R average, 62% winners, positive in every past year (worst year shrunk +0.476R)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when against_1h+pred_mid+votes>=3: no longer among the best patterns that held in every past year
- DROP XAU_USD sweep_bos|5m|pivots+sessions|at_break (3R) when between+room_pd>=2R+votes>=3: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when long+ny_open+votes>=3: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (half1R_be3R) when long+premium+votes>=3: no longer among the best patterns that held in every past year

## v29 (written after 2022-10-18, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when long and ny_open and votes>=3: 79 past trades, +0.909R average, 59% winners, positive in every past year (worst year shrunk +0.643R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when long and premium and quiet_day: 83 past trades, +0.835R average, 57% winners, positive in every past year (worst year shrunk +0.578R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (half1R_3R) when long and premium and votes>=3: 63 past trades, +0.707R average, 63% winners, positive in every past year (worst year shrunk +0.476R)
- ADD NAS100_USD continuation|1h>1m (3R) when beyond_pd and busy_day and with_15m: 67 past trades, +0.745R average, 52% winners, positive in every past year (worst year shrunk +0.475R)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when long+ny_open+with_4h: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when long+premium+with_4h: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|sessions|at_equilibrium (3R) when newyork+with_1h: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (2R) when long+ny_open+votes>=3: no longer among the best patterns that held in every past year

## v30 (written after 2022-11-08, used from the next trading day)
- DAY STOPS: stop after 0.5R / NoneR on the day (replay of the last 250 days: 64% of trading days green, +87.4R)

## v31 (written after 2022-11-15, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when long and premium and votes>=3: 65 past trades, +0.847R average, 62% winners, positive in every past year (worst year shrunk +0.544R)
- ADD NAS100_USD sweep_bos|5m|sessions|at_equilibrium (3R) when newyork and with_1h: 45 past trades, +0.962R average, 56% winners, positive in every past year (worst year shrunk +0.477R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (2R) when long and ny_open and with_4h: 77 past trades, +0.682R average, 60% winners, positive in every past year (worst year shrunk +0.459R)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when long+premium+quiet_day: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (2R) when asia+long+stop>=6sp: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (half1R_3R) when long+premium+votes>=3: no longer among the best patterns that held in every past year

## v32 (written after 2022-12-06, used from the next trading day)
- BENCH NAS100_USD (non-CRT): its strategy trades lost -0.303R over the last 48
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when long+ny_open+votes>=3: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when long+premium+votes>=3: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_break (2R) when between+pred_low_third: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|sessions|at_equilibrium (3R) when newyork+with_1h: no longer among the best patterns that held in every past year
- DROP NAS100_USD continuation|1h>1m (3R) when beyond_pd+busy_day+with_15m: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (2R) when long+ny_open+with_4h: no longer among the best patterns that held in every past year
- DAY STOPS: none

## v33 (written after 2023-01-12, used from the next trading day)
- ADD XAU_USD continuation|4h>5m (half1R_3R) when beyond_pd and with_D: 146 past trades, +0.138R average, 43% winners, positive in every past year (worst year shrunk +0.042R)

## v34 (written after 2023-02-09, used from the next trading day)
- DROP XAU_USD continuation|4h>5m (half1R_3R) when beyond_pd+with_D: no longer among the best patterns that held in every past year

## v35 (written after 2023-03-02, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when long and premium and quiet_day: 105 past trades, +0.785R average, 53% winners, positive in every past year (worst year shrunk +0.360R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (2R) when long and quiet_day and stop>=6sp: 137 past trades, +0.422R average, 53% winners, positive in every past year (worst year shrunk +0.236R)
- ADD NAS100_USD continuation|1h>1m (3R) when ny_midday and pred_high_third and premium: 321 past trades, +0.215R average, 33% winners, positive in every past year (worst year shrunk +0.146R)
- ADD NAS100_USD continuation|1h>5m (3R) when ny_midday and with_D: 175 past trades, +0.193R average, 46% winners, positive in every past year (worst year shrunk +0.133R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (half1R_3R) when premium and with_4h: 156 past trades, +0.274R average, 49% winners, positive in every past year (worst year shrunk +0.117R)
- DAY STOPS: stop after 0.5R / NoneR on the day (replay of the last 250 days: 46% of trading days green, +62.0R)

## v36 (written after 2023-03-09, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when ny_open and quiet_day and votes>=3: 81 past trades, +0.796R average, 53% winners, positive in every past year (worst year shrunk +0.450R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (2R) when midweek and range_used<0.5 and room_pd>=2R: 97 past trades, +0.479R average, 51% winners, positive in every past year (worst year shrunk +0.309R)
- ADD NAS100_USD continuation|1h>1m (3R) when beyond_pd and ny_midday and pred_high_third: 134 past trades, +0.420R average, 39% winners, positive in every past year (worst year shrunk +0.261R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (2R) when newyork and quiet_day and with_1h: 72 past trades, +0.496R average, 57% winners, positive in every past year (worst year shrunk +0.204R)
- ADD NAS100_USD sweep_bos|5m|sessions|at_equilibrium (3R) when stop>=6sp and with_1h: 99 past trades, +0.385R average, 39% winners, positive in every past year (worst year shrunk +0.159R)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (2R) when long+quiet_day+stop>=6sp: no longer among the best patterns that held in every past year
- DROP NAS100_USD continuation|1h>1m (3R) when ny_midday+pred_high_third+premium: no longer among the best patterns that held in every past year
- DROP NAS100_USD continuation|1h>5m (3R) when ny_midday+with_D: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (half1R_3R) when premium+with_4h: no longer among the best patterns that held in every past year

## v37 (written after 2023-04-06, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when long and premium and votes>=3: 84 past trades, +0.775R average, 57% winners, positive in every past year (worst year shrunk +0.444R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when long and newyork and with_1h: 102 past trades, +0.579R average, 53% winners, positive in every past year (worst year shrunk +0.292R)
- ADD XAU_USD sweep_bos|5m|sessions|at_gap (3R) when against_1h and pred_low_third and stop>=6sp: 75 past trades, +0.505R average, 47% winners, positive in every past year (worst year shrunk +0.282R)
- ADD NAS100_USD sweep_bos|5m|sessions|at_break (3R) when newyork and stop>=12sp and with_1h: 80 past trades, +0.514R average, 51% winners, positive in every past year (worst year shrunk +0.271R)
- ADD NAS100_USD sweep_bos|5m|sessions|at_block (3R) when stop>=6sp and with_1h: 75 past trades, +0.468R average, 39% winners, positive in every past year (worst year shrunk +0.237R)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when ny_open+quiet_day+votes>=3: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when long+premium+quiet_day: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (2R) when midweek+range_used<0.5+room_pd>=2R: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (2R) when newyork+quiet_day+with_1h: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|sessions|at_equilibrium (3R) when stop>=6sp+with_1h: no longer among the best patterns that held in every past year

## v38 (written after 2023-04-20, used from the next trading day)
- DAY STOPS: stop after NoneR / -2.0R on the day (replay of the last 250 days: 50% of trading days green, +69.9R)

## v39 (written after 2023-05-04, used from the next trading day)
- BENCH NAS100_USD (non-CRT): its strategy trades lost -0.350R over the last 28
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when long+premium+votes>=3: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (3R) when long+newyork+with_1h: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|sessions|at_break (3R) when newyork+stop>=12sp+with_1h: no longer among the best patterns that held in every past year
- DROP NAS100_USD continuation|1h>1m (3R) when beyond_pd+ny_midday+pred_high_third: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|sessions|at_block (3R) when stop>=6sp+with_1h: no longer among the best patterns that held in every past year
- DAY STOPS: stop after NoneR / NoneR on the day (replay of the last 250 days: 52% of trading days green, +8.7R)

## v40 (written after 2023-08-03, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_break (2R) when between and pred_low_third: 70 past trades, +0.795R average, 63% winners, positive in every past year (worst year shrunk +0.422R)
- ADD NAS100_USD sweep_bos|5m|sessions|at_block (3R) when newyork and session_pool and with_1h: 45 past trades, +0.904R average, 49% winners, positive in every past year (worst year shrunk +0.418R)
- ADD NAS100_USD sweep_bos|5m|sessions|at_break (3R) when long and newyork and with_1h: 51 past trades, +0.769R average, 61% winners, positive in every past year (worst year shrunk +0.355R)
- ADD NAS100_USD continuation|1h>1m (3R) when beyond_pd and busy_day and mon: 53 past trades, +0.816R average, 53% winners, positive in every past year (worst year shrunk +0.355R)
- ADD NAS100_USD sweep_bos|5m|sessions|at_break (2R) when long and with_1h and with_D: 52 past trades, +0.565R average, 58% winners, positive in every past year (worst year shrunk +0.278R)

## v41 (written after 2023-08-24, used from the next trading day)
- ADD NAS100_USD sweep_bos|5m|sessions|at_equilibrium (3R) when newyork and session_pool and with_1h: 64 past trades, +0.763R average, 50% winners, positive in every past year (worst year shrunk +0.394R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when inside_pd and london and premium: 97 past trades, +0.592R average, 45% winners, positive in every past year (worst year shrunk +0.389R)
- ADD NAS100_USD sweep_bos|5m|sessions|at_equilibrium (2R) when stop>=3sp and votes>=3 and with_D: 67 past trades, +0.542R average, 52% winners, positive in every past year (worst year shrunk +0.292R)
- DROP NAS100_USD sweep_bos|5m|sessions|at_block (3R) when newyork+session_pool+with_1h: no longer among the best patterns that held in every past year
- DROP XAU_USD sweep_bos|5m|sessions|at_gap (3R) when against_1h+pred_low_third+stop>=6sp: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|sessions|at_break (2R) when long+with_1h+with_D: no longer among the best patterns that held in every past year

## v42 (written after 2023-09-21, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_break (2R) when between and discount and pred_low_third: 68 past trades, +0.637R average, 57% winners, positive in every past year (worst year shrunk +0.351R)
- ADD XAU_USD sweep_bos|5m|sessions|at_gap (3R) when pred_low_third and session_pool and short: 48 past trades, +0.591R average, 46% winners, positive in every past year (worst year shrunk +0.289R)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (3R) when inside_pd+london+premium: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_break (2R) when between+pred_low_third: no longer among the best patterns that held in every past year
- DAY STOPS: stop after 2.0R / NoneR on the day (replay of the last 250 days: 60% of trading days green, +55.8R)

## v43 (written after 2023-10-19, used from the next trading day)


## v44 (written after 2023-11-16, used from the next trading day)
- ADD NAS100_USD sweep_bos|5m|sessions|at_equilibrium (3R) when newyork and room_pd>=2R and with_1h: 50 past trades, +1.097R average, 56% winners, positive in every past year (worst year shrunk +0.419R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_break (2R) when between and pred_low_third: 79 past trades, +0.683R average, 59% winners, positive in every past year (worst year shrunk +0.388R)
- ADD NAS100_USD sweep_bos|5m|sessions|at_block (3R) when newyork and session_pool and with_1h: 53 past trades, +0.759R average, 45% winners, positive in every past year (worst year shrunk +0.309R)
- DROP NAS100_USD sweep_bos|5m|sessions|at_equilibrium (3R) when newyork+session_pool+with_1h: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_break (2R) when between+discount+pred_low_third: no longer among the best patterns that held in every past year
- DROP XAU_USD sweep_bos|5m|sessions|at_gap (3R) when pred_low_third+session_pool+short: no longer among the best patterns that held in every past year
- DAY STOPS: stop after NoneR / NoneR on the day (replay of the last 250 days: 63% of trading days green, +47.4R)

## v45 (written after 2023-11-30, used from the next trading day)
- BENCH NAS100_USD (non-CRT): its strategy trades lost -0.166R over the last 35
- ADD XAU_USD sweep_bos|5m|sessions|at_gap (3R) when against_1h and pred_low_third and stop>=6sp: 88 past trades, +0.487R average, 48% winners, positive in every past year (worst year shrunk +0.282R)
- DROP NAS100_USD sweep_bos|5m|sessions|at_equilibrium (3R) when newyork+room_pd>=2R+with_1h: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_break (2R) when between+pred_low_third: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|sessions|at_break (3R) when long+newyork+with_1h: no longer among the best patterns that held in every past year
- DROP NAS100_USD continuation|1h>1m (3R) when beyond_pd+busy_day+mon: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|sessions|at_block (3R) when newyork+session_pool+with_1h: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|sessions|at_equilibrium (2R) when stop>=3sp+votes>=3+with_D: no longer among the best patterns that held in every past year

## v46 (written after 2024-01-15, used from the next trading day)
- DROP XAU_USD sweep_bos|5m|sessions|at_gap (3R) when against_1h+pred_low_third+stop>=6sp: no longer among the best patterns that held in every past year

## v47 (written after 2024-02-26, used from the next trading day)
- ADD NAS100_USD continuation|1h>5m (3R) when long and ny_midday and stop>=12sp: 260 past trades, +0.269R average, 48% winners, positive in every past year (worst year shrunk +0.121R)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_break (2R) when between and with_D: 147 past trades, +0.244R average, 44% winners, positive in every past year (worst year shrunk +0.058R)
- ADD NAS100_USD continuation|1h>5m (2R) when busy_day and premium and stop>=12sp: 250 past trades, +0.071R average, 45% winners, positive in every past year (worst year shrunk +0.037R)
- DAY STOPS: stop after 0.5R / NoneR on the day (replay of the last 250 days: 48% of trading days green, +26.7R)

## v48 (written after 2024-03-04, used from the next trading day)
- DAY STOPS: stop after 2.0R / NoneR on the day (replay of the last 250 days: 48% of trading days green, +26.4R)

## v49 (written after 2024-03-11, used from the next trading day)
- ADD NAS100_USD continuation|1h>1m (3R) when beyond_pd and busy_day and stop>=12sp: 351 past trades, +0.200R average, 37% winners, positive in every past year (worst year shrunk +0.155R)
- ADD NAS100_USD continuation|1h>5m (2R) when busy_day and ny_midday and with_4h: 89 past trades, +0.151R average, 49% winners, positive in every past year (worst year shrunk +0.073R)
- ADD XAU_USD continuation|1h>5m (2R) when between and stop>=6sp: 246 past trades, +0.082R average, 40% winners, positive in every past year (worst year shrunk +0.028R)
- DROP NAS100_USD continuation|1h>5m (3R) when long+ny_midday+stop>=12sp: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_break (2R) when between+with_D: no longer among the best patterns that held in every past year
- DROP NAS100_USD continuation|1h>5m (2R) when busy_day+premium+stop>=12sp: no longer among the best patterns that held in every past year
- DAY STOPS: stop after 0.5R / NoneR on the day (replay of the last 250 days: 50% of trading days green, +45.1R)

## v50 (written after 2024-04-09, used from the next trading day)
- ADD XAU_USD continuation|1h>5m (2R) when between and inside_pd and stop>=6sp: 183 past trades, +0.126R average, 42% winners, positive in every past year (worst year shrunk +0.066R)
- DROP NAS100_USD continuation|1h>5m (2R) when busy_day+ny_midday+with_4h: no longer among the best patterns that held in every past year
- DROP XAU_USD continuation|1h>5m (2R) when between+stop>=6sp: no longer among the best patterns that held in every past year

## v51 (written after 2024-04-23, used from the next trading day)
- BENCH NAS100_USD|continuation|1h>1m|3R|beyond_pd+busy_day+stop>=12sp: its own strategy trades lost -0.400R over the last 16 (until ~3 months)
- BENCH NAS100_USD (non-CRT): its strategy trades lost -0.331R over the last 27
- DROP NAS100_USD continuation|1h>1m (3R) when beyond_pd+busy_day+stop>=12sp: no longer among the best patterns that held in every past year
- DAY STOPS: stop after NoneR / NoneR on the day (replay of the last 250 days: 42% of trading days green, +1.1R)

## v52 (written after 2024-05-07, used from the next trading day)
- ADD XAU_USD sweep_bos|5m|sessions|at_break (3R) when room_pd>=2R and stop>=3sp and votes>=3: 59 past trades, +0.244R average, 39% winners, positive in every past year (worst year shrunk +0.080R)
- DAY STOPS: stop after 2.0R / NoneR on the day (replay of the last 250 days: 43% of trading days green, +11.6R)

## v53 (written after 2024-06-04, used from the next trading day)
- DROP XAU_USD continuation|1h>5m (2R) when between+inside_pd+stop>=6sp: no longer among the best patterns that held in every past year
- DAY STOPS: stop after NoneR / NoneR on the day (replay of the last 250 days: 44% of trading days green, +8.4R)

## v54 (written after 2024-07-23, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_break (2R) when against_1h and between and inside_pd: 241 past trades, +0.227R average, 44% winners, positive in every past year (worst year shrunk +0.156R)
- DAY STOPS: stop after 0.5R / NoneR on the day (replay of the last 250 days: 41% of trading days green, +12.8R)

## v55 (written after 2024-07-30, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_break (2R) when between and pred_low_third and with_D: 68 past trades, +0.653R average, 57% winners, positive in every past year (worst year shrunk +0.267R)
- ADD NAS100_USD continuation|1h>1m (3R) when beyond_pd and busy_day and stop>=12sp: 387 past trades, +0.191R average, 36% winners, positive in every past year (worst year shrunk +0.155R)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_break (2R) when against_1h+between+inside_pd: no longer among the best patterns that held in every past year
- DAY STOPS: stop after 2.0R / NoneR on the day (replay of the last 250 days: 47% of trading days green, +23.1R)

## v56 (written after 2024-08-27, used from the next trading day)
- ADD XAU_USD opening_range|newyork|5m|stop_box (half1R_3R) when short: 66 past trades, +0.182R average, 45% winners, positive in every past year (worst year shrunk +0.033R)
- ADD XAU_USD sweep_bos|15m|pivots+sessions|at_gap (half1R_3R) when between: 71 past trades, +0.171R average, 51% winners, positive in every past year (worst year shrunk +0.031R)
- ADD XAU_USD sweep_bos|5m|sessions|at_break (2R) when inside_pd and votes>=3: 93 past trades, +0.098R average, 46% winners, positive in every past year (worst year shrunk +0.029R)
- DAY STOPS: stop after 0.5R / NoneR on the day (replay of the last 250 days: 51% of trading days green, +29.4R)

## v57 (written after 2024-09-24, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (2R) when premium and session_pool and with_1h: 126 past trades, +0.257R average, 46% winners, positive in every past year (worst year shrunk +0.143R)
- ADD NAS100_USD sweep_bos|5m|sessions|at_gap (1R) when newyork and session_pool: 89 past trades, +0.151R average, 57% winners, positive in every past year (worst year shrunk +0.081R)
- ADD XAU_USD sweep_bos|15m|pivots+sessions|at_gap (half1R_3R) when between and with_D: 52 past trades, +0.273R average, 56% winners, positive in every past year (worst year shrunk +0.056R)
- DROP XAU_USD opening_range|newyork|5m|stop_box (half1R_3R) when short: no longer among the best patterns that held in every past year
- DROP XAU_USD sweep_bos|15m|pivots+sessions|at_gap (half1R_3R) when between: no longer among the best patterns that held in every past year
- DROP XAU_USD sweep_bos|5m|sessions|at_break (2R) when inside_pd+votes>=3: no longer among the best patterns that held in every past year
- DAY STOPS: stop after 1.0R / NoneR on the day (replay of the last 250 days: 48% of trading days green, +34.6R)

## v58 (written after 2024-10-22, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_break (2R) when between and pred_low_third: 117 past trades, +0.579R average, 56% winners, positive in every past year (worst year shrunk +0.314R)
- ADD NAS100_USD sweep_bos|5m|sessions|at_block (3R) when newyork and session_pool and with_1h: 74 past trades, +0.717R average, 45% winners, positive in every past year (worst year shrunk +0.272R)
- ADD NAS100_USD continuation|1h>1m (3R) when beyond_pd and busy_day and mon: 94 past trades, +0.545R average, 46% winners, positive in every past year (worst year shrunk +0.182R)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_break (2R) when between+pred_low_third+with_D: no longer among the best patterns that held in every past year
- DROP NAS100_USD continuation|1h>1m (3R) when beyond_pd+busy_day+stop>=12sp: no longer among the best patterns that held in every past year
- DROP XAU_USD sweep_bos|15m|pivots+sessions|at_gap (half1R_3R) when between+with_D: no longer among the best patterns that held in every past year
- DAY STOPS: stop after NoneR / NoneR on the day (replay of the last 250 days: 49% of trading days green, +36.6R)

## v59 (written after 2024-11-19, used from the next trading day)
- ADD NAS100_USD sweep_bos|5m|sessions|at_block (half1R_3R) when ny_open and with_1h: 58 past trades, +0.484R average, 48% winners, positive in every past year (worst year shrunk +0.117R)
- ADD NAS100_USD sweep_bos|5m|sessions|at_block (2R) when short and stop>=6sp and with_1h: 73 past trades, +0.266R average, 44% winners, positive in every past year (worst year shrunk +0.085R)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_equilibrium (2R) when premium+session_pool+with_1h: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|sessions|at_gap (1R) when newyork+session_pool: no longer among the best patterns that held in every past year

## v60 (written after 2024-12-17, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_break (2R) when against_1h and between and pred_low_third: 121 past trades, +0.550R average, 55% winners, positive in every past year (worst year shrunk +0.299R)
- ADD NAS100_USD continuation|1h>1m (3R) when beyond_pd and busy_day and stop>=12sp: 437 past trades, +0.208R average, 37% winners, positive in every past year (worst year shrunk +0.155R)
- ADD NAS100_USD sweep_bos|5m|sessions|at_gap (1R) when newyork: 115 past trades, +0.136R average, 57% winners, positive in every past year (worst year shrunk +0.058R)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_break (2R) when between+pred_low_third: no longer among the best patterns that held in every past year
- DROP NAS100_USD continuation|1h>1m (3R) when beyond_pd+busy_day+mon: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|sessions|at_block (half1R_3R) when ny_open+with_1h: no longer among the best patterns that held in every past year
- DAY STOPS: stop after 2.0R / NoneR on the day (replay of the last 250 days: 50% of trading days green, +41.3R)

## v61 (written after 2025-01-02, used from the next trading day)
- DAY STOPS: stop after 0.5R / NoneR on the day (replay of the last 250 days: 50% of trading days green, +35.5R)

## v62 (written after 2025-01-16, used from the next trading day)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_break (2R) when against_1h+between+pred_low_third: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|sessions|at_block (3R) when newyork+session_pool+with_1h: no longer among the best patterns that held in every past year
- DROP NAS100_USD continuation|1h>1m (3R) when beyond_pd+busy_day+stop>=12sp: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|sessions|at_block (2R) when short+stop>=6sp+with_1h: no longer among the best patterns that held in every past year
- DROP XAU_USD sweep_bos|5m|sessions|at_break (3R) when room_pd>=2R+stop>=3sp+votes>=3: no longer among the best patterns that held in every past year
- DROP NAS100_USD sweep_bos|5m|sessions|at_gap (1R) when newyork: no longer among the best patterns that held in every past year
- DAY STOPS: none

## v63 (written after 2025-01-23, used from the next trading day)
- BENCH NAS100_USD|continuation|1h>1m|3R|beyond_pd+busy_day+stop>=12sp: its own strategy trades lost -0.250R over the last 24 (until ~3 months)

## v64 (written after 2025-02-13, used from the next trading day)
- BENCH NAS100_USD (non-CRT): its strategy trades lost -0.180R over the last 45

## v65 (written after 2025-03-27, used from the next trading day)
- ADD XAU_USD continuation|1h>5m (2R) when between and stop>=6sp: 347 past trades, +0.066R average, 39% winners, positive in every past year (worst year shrunk +0.028R)
- DAY STOPS: stop after NoneR / -1.0R on the day (replay of the last 250 days: 37% of trading days green, +3.5R)

## v66 (written after 2025-04-10, used from the next trading day)
- DROP XAU_USD continuation|1h>5m (2R) when between+stop>=6sp: no longer among the best patterns that held in every past year
- DAY STOPS: none

## v67 (written after 2025-04-25, used from the next trading day)
- BENCH NAS100_USD|continuation|1h>1m|3R|beyond_pd+busy_day+stop>=12sp: its own strategy trades lost -0.324R over the last 15 (until ~3 months)

## v68 (written after 2025-06-27, used from the next trading day)
- ADD NAS100_USD continuation|1h>1m (3R) when busy_day and stop>=12sp and with_D: 586 past trades, +0.124R average, 33% winners, positive in every past year (worst year shrunk +0.087R)
- DAY STOPS: stop after 0.5R / NoneR on the day (replay of the last 250 days: 57% of trading days green, +43.6R)

## v69 (written after 2025-08-01, used from the next trading day)
- ADD XAU_USD continuation|1h>5m (2R) when between and quiet_day: 122 past trades, +0.181R average, 43% winners, positive in every past year (worst year shrunk +0.066R)

## v70 (written after 2025-08-22, used from the next trading day)
- BENCH NAS100_USD|continuation|1h>1m|3R|busy_day+stop>=12sp+with_D: its own strategy trades lost -0.218R over the last 16 (until ~3 months)
- ADD NAS100_USD continuation|1h>1m (3R) when busy_day and stop>=12sp and with_4h: 904 past trades, +0.151R average, 34% winners, positive in every past year (worst year shrunk +0.068R)
- DROP NAS100_USD continuation|1h>1m (3R) when busy_day+stop>=12sp+with_D: no longer among the best patterns that held in every past year
- DAY STOPS: stop after NoneR / NoneR on the day (replay of the last 250 days: 45% of trading days green, +34.5R)

## v71 (written after 2025-08-29, used from the next trading day)
- ADD XAU_USD continuation|1h>5m (2R) when between and inside_pd and stop>=12sp: 166 past trades, +0.189R average, 45% winners, positive in every past year (worst year shrunk +0.085R)
- DROP XAU_USD continuation|1h>5m (2R) when between+quiet_day: no longer among the best patterns that held in every past year

## v72 (written after 2025-09-19, used from the next trading day)
- BENCH NAS100_USD (non-CRT): its strategy trades lost -0.151R over the last 26
- DROP NAS100_USD continuation|1h>1m (3R) when busy_day+stop>=12sp+with_4h: no longer among the best patterns that held in every past year
- DAY STOPS: stop after NoneR / -1.0R on the day (replay of the last 250 days: 42% of trading days green, +7.0R)

## v73 (written after 2025-09-26, used from the next trading day)
- ADD XAU_USD continuation|1h>5m (2R) when between and quiet_day: 124 past trades, +0.210R average, 44% winners, positive in every past year (worst year shrunk +0.066R)
- DROP XAU_USD continuation|1h>5m (2R) when between+inside_pd+stop>=12sp: no longer among the best patterns that held in every past year
- DAY STOPS: stop after NoneR / NoneR on the day (replay of the last 250 days: 55% of trading days green, +13.6R)

## v74 (written after 2025-12-19, used from the next trading day)
- DROP XAU_USD continuation|1h>5m (2R) when between+quiet_day: no longer among the best patterns that held in every past year

## v75 (written after 2025-12-29, used from the next trading day)
- ADD NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (2R) when day_pool: 67 past trades, +0.098R average, 42% winners, positive in every past year (worst year shrunk +0.020R)

## v76 (written after 2026-01-20, used from the next trading day)
- DROP NAS100_USD sweep_bos|15m|pivots+sessions|at_gap (2R) when day_pool: no longer among the best patterns that held in every past year
