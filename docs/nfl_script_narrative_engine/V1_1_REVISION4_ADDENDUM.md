# NFL Script Engine v1.1 — Revision 4 Addendum (response to ChatGPT section 6)

Status: registry NOT_FROZEN; PR #3 unmerged; main untouched; no commits; no outcome joins; all outcomes below are SIMULATED.

## 1. Structural re-audit using mathematical bounds (not observed maxima)
Method: a feature is STRUCTURAL only if the set of possible name values (every era of every franchise in the identity table, both bases) is disjoint from the mathematically feasible set of the quantity. Feasible sets: days_remaining 0–365; date_digit_sum = every valid calendar date 1999–2099 (4–48); date_digit_root = digital roots of that set; weekday 1–7; schedule_week 1–22 (superset of REG); season wins/losses/ties 0–16 each. The six days_since / months_since quantities have no mathematical upper bound, so none can be structural.
Result: **98 STRUCTURAL / 33 EMPIRICAL_ZERO** (was 106 / 25). The 8 reclassified features are all season_ties × {city, nickname} × {historical, current} × {pythagorean, reverse_root}: ties 13–16 are mathematically possible, so a name value of 13, 15 or 9 is not excluded. No other classification changed. File: proposed_untestable_features_rev4.csv (columns zero_class_rev3, zero_class_rev4, reason_rev4, changed_from_rev3). Structural counts by quantity: weekday 18, date_digit_root 16, schedule_week 14, season_wins/losses/ties 14 each, date_digit_sum 8.
Note: schedule_week 1–22 and wins/losses/ties 0–16 are deliberately generous bounds; tightening them would only move features toward STRUCTURAL, so this is the conservative direction.

## 2. Final-design simulations (A2 stopping rule, stratified residual permutation, frozen coefficients) — CORRECTED MODULE
Design simulated: real 2021–25 schedule structure cycled to 10 seasons, fresh strengths each season, frozen baseline from a separate simulated training set, support recomputed cumulatively at every week-end, ONE evaluation at the first week-end with ≥188 on-support F4 games, B=199, α=0.05. Type I: R=5,000 per cell (MC SE ≤ 0.31 pts). Single shared implementation `scripts/f4_stopping_rule.py` (exact integer right-closed d-bins; sha256 in FREEZE_CHECKLIST_REV4.md). This grid was RE-RUN after the binning correction; the earlier floating-point-binning results are retained as superseded.

Type I (% rejected at δ=0), comparator threshold 10 / 20 (primary) / 40:
| null | thr 10 | thr 20 (primary) | thr 40 |
|---|---|---|---|
| latent SD 0.35 | 4.3 | 4.1 | 4.2 |
| latent SD 0.60 | 4.6 | 4.2 | 4.1 |
| latent SD 0.85 | 4.3 | 4.5 | 4.1 |
| records: g-slope | 4.3 | 4.4 | 4.1 |
| records: cubic | 4.5 | 3.7 | 4.2 |
| records: unequal-G level | 4.3 | 4.6 | 4.4 |
| records: equal-G bonus (small) | 4.2 | 3.9 | 4.5 |
| records: equal-G bonus (large) | 4.6 | 5.1 | 4.0 |
| week shock + week-varying signal scale | 4.1 | 4.1 | 4.3 |
| team random effects | 4.2 | 4.2 | 4.0 |
| season-level home-edge shift | 4.5 | 3.9 | 4.3 |
| combined moderate stress | 4.4 | 4.0 | 4.3 |
All cells 3.7%–5.1% (primary threshold: 3.7%–5.1%); the highest cell (large equal-G bonus, threshold 20) is 5.1%, within one MC SE of 5%. These are simulated nulls, not a proof of exactness.

## 3. Support and effective sample at evaluation (latent SD0.60, R=5,000)
| threshold | supported strata (min/p5/median/p95/max) | on-support F4 at evaluation (p5/median/p95) | effective size (p5/median/p95) | seasons to evaluation (p5/median/p95) | mean total F4 |
|---|---|---|---|---|---|
| 10 | 16 / 17 / 18 / 18 / 18 | 188 / 189 / 195 | 131 / 138 / 144 | 5 / 5 / 6 | 202 |
| 20 | 12 / 15 / 16 / 18 / 18 | 188 / 190 / 209 | 136 / 143 / 153 | 5 / 6 / 7 | 225 |
| 40 | 10 / 11 / 12 / 14 / 16 | 188 / 190 / 220 | 151 / 157 / 174 | 7 / 8 / 9 | 317 |
188 was reached within 10 simulated seasons in 100% of replicates at every threshold. Seasons-to-evaluation is approximate (season-weeks ÷ 18). At threshold 20 the design needs roughly 6 seasons (≈2031).

## 4. Power at the final design (R=4,000 per cell, SE ≤0.8 pts)
latent SD0.60, threshold 20: 8 pts 44.4%; 10 pts 63.5%; 12 pts 80.1%; 14 pts 91.2%. 10 pts at threshold 10 / 40: 61.2% / 70.2%; latent SD0.35: 63.6%; combined null: 67.5%. **80%-power MDE ≈ 12 percentage points.** A 10-point effect remains under-powered (~64%).

## 5. Discovery-refit calibration at ~20-season size (N=5,116 games, ~800–960 F4, R=1,000, B=199, refit inside every permutation) — CORRECTED MODULE
lat060: 3.7%; gslope: 4.1%; eqbonus_big: 4.7%; combo: 4.3%; weekshock: 4.8% (MC SE ≈0.6–0.7 pts). Calibrated at this size under these nulls; discovery inference may be retained as exploratory; it remains non-confirmatory.

## 6. Stopping rule verification
f4_stopping_rule.py: cumulative on-support count is recomputed from cumulative stratum counts at every week-end and checked against brute-force recomputation from scratch on synthetic data at every week-end (assertions pass); counts are monotone; first-week-reaching(188) correct including never-reached; support hash is SHA-256 over sorted on-support game ids and is order-invariant. The same module drives the simulations. NOT yet done: wiring to the real 2026 pregame partitions (needs your approval; outcome-blind, no commit).

## 7. Still pending / unchanged
Tier B test specification separate and pending. Registry NOT_FROZEN. No outcome joins, no outcome-based fitting, no v1.2, no merge. Seed policy: seeds derived from mode, threshold, delta (see script); results in rev4/results.jsonl.

## 8. Post-addendum corrections (2026-11-13)
- d-bin convention: an earlier module used floating-point left-closed binning; the module now follows the documented right-closed convention in exact integer arithmetic, and ineligible (0-games-played) games can never be stratum members (FREEZE_CHECKLIST_REV4.md section D). ALL tables in sections 2-5 above were regenerated with the corrected module.
- Baseline coefficients (provisional): b0 = 0.3509, b1 = 3.896 (reference/baseline_fit/).
- Full-scale B = 100,000 execution check: see F4_PROTOCOL_REV4.md section 5.
