# F4 revision-4 simulations (SIMULATED outcomes only; no real outcomes)
Configuration (no hard-coded paths): see `paths.py`. Required env: `NFLVERSE_GAMES_CSV` (nflverse games.csv; used only for the 2021-2025 schedule structure in simulations); optional `NFL_REPO_ROOT`, `NFL_DERIVED_DIR` (partitions, only for the real-data check/fit), `F4_OUT_DIR` (results; default `./results`). The shared modules `f4_stopping_rule.py` and `f4_permutation_test.py` live in `<repo>/scripts/`. Dependencies/versions: `ENVIRONMENT.txt`.
- `f4_rev4_sim.py MODE TOL R B DELTA [NSEASONS] [SEED]`: final-design Type I / power (A2, stratified residual permutation, frozen coefficients from a separate simulated training set). Seed = (SEED default 20261120) + TOL + int(DELTA*1000) + sum(ord(MODE)). Driver: `run_all.sh LANE` (lanes 0 and 1).
- `f4_refit20_sim.py R B MODES`: discovery-refit calibration at 20 seasons (seed 20261130).
- `b100k_calibration.py MODE sim|real R SEED`: full-scale B = 100,000 execution check (evaluation r uses seed*1000 + r); `b100k_repro_check.py`; `b100k_unit_checks.py` (exact enumeration).
- `real_pregame_stopping_check.py`: outcome-blind check of the stopping rule on the real prospective pregame partition.
- `binning_old_new_comparison.py`: outcome-blind comparison of the superseded float binning vs exact right-closed binning on real partitions.
- `f4_type1_sim.py`, `f4_refit_sim.py`: legacy revision-3 simulators (M0/M1/M2); now use the exact binning via `strata_ids`, kept for provenance.
- `results/`: committed outputs. `results/SUPERSEDED_f4_stopping_rule_v1_digitize.py` is the first (float, left-closed) module, retained only for the old-vs-new comparison.
