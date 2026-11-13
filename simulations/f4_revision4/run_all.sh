#!/bin/bash
# Type I grid (12 nulls x thresholds 10/20/40, R=5000, B=199) and power cells. Usage: run_all.sh LANE(0|1). Needs NFLVERSE_GAMES_CSV; F4_OUT_DIR optional.
cd "$(dirname "$0")"; lane=$1; i=0
for tol in 20 10 40; do
 for m in lat035 lat060 lat085 gslope cubic levelgap eqbonus eqbonus_big weekshock teamre seasonshift combo; do
  i=$((i+1)); if [ $((i%2)) -eq $lane ]; then python3 f4_rev4_sim.py $m $tol 5000 199 0.0 10 2>/dev/null; fi
 done
done
for spec in "lat060 20 0.08" "lat060 20 0.10" "lat060 20 0.12" "lat060 20 0.14" "lat060 10 0.10" "lat060 40 0.10" "lat035 20 0.10" "combo 20 0.10"; do
  i=$((i+1)); if [ $((i%2)) -eq $lane ]; then set -- $spec; python3 f4_rev4_sim.py $1 $2 4000 199 $3 10 2>/dev/null; fi
done
