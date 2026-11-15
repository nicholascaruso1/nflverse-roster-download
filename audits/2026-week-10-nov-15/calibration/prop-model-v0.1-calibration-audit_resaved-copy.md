# NFL Player Prop pilot v0.1: walk-forward calibration audit (research branch, v0.1 of this audit)

**Status:** research document for independent review. **NFL Player Prop Model v2.2 and the Nov 15 Lock 2 card are FROZEN and unchanged. No model parameter was changed or tuned.** Run Sun Nov 15 2026 after the 1:00 PM ET kickoffs, as approved by Nick. Nothing here promotes, demotes or re-grades any pregame classification.

**One-paragraph result.** For receptions and rushing yards the pilot's probabilities are roughly calibrated on average (pooled predicted P(Over) within about 1 point of the realized rate), but they are **overconfident at the extremes** (for example, model probabilities of 80-90% for receptions hit about 73%) and overconfident specifically in **low-volume receivers, QB rushing and passing-yards Unders**, which are exactly the archetypes behind the five LEANs. Passing yards are the weakest market: the model under-predicts Overs by about 5 points and its pass-yardage Unders overstate by about 7 points. **I found no evidence of a structural Under bias in receptions or rushing in aggregate**; the overstatement shows up on both sides (Over-leaning +3.2 points, Under-leaning +1.4 points). Discrimination within a given threshold is modest (AUC about 0.54-0.60 for receptions and rushing), and Brier skill over a threshold-only benchmark is about +1% for receptions and rushing and negative for passing yards. The simple opponent and game-script specifications I tested (B, C) did **not** improve out-of-sample Brier score (differences about +0.001, confidence interval touching zero). Using full-sample constants (the original pilot) inflated apparent pass-yardage performance by about 0.008 Brier. The audit cannot say anything about profitability.

## 1. Data provenance and chronological boundaries
- **Data:** nflverse 2026 play-by-play, snap counts and rosters (downloaded about 12:30 PM ET Nov 15), regular season weeks 1-10. Week 10 contains one game (WAS @ NYG), not used in the walk-forward test. Pregame `spread_line` and `total_line` come from the play-by-play file (market lines at kickoff as stored by nflverse); they are used only in spec C.
- **Test window:** target weeks **3-9** (week 2 excluded: each player has at most 1 prior game; the protocol said weeks 2-9, and the rule "at least 2 prior active games" removes week 2). Each target-week prediction uses **only games in earlier weeks** for: the player's volume and efficiency history, the catch/ypc/ypa shrinkage, the league yardage distributions, league means, opponent allowed rates and the game-script slopes.
- **Eligibility (pre-specified, not tuned):** active in the target week (offense snaps > 0), at least 2 prior active games; receptions: WR/TE/RB with exponentially weighted (half-life 3) targets >= 1.0; rushing: carries EW >= 0.5; passing: QBs with attempts EW >= 10.
- **Observations:** 1434 receptions, 730 rushing, 197 passing player-games (total 2361); per week: {3: 347, 4: 362, 5: 345, 6: 318, 7: 322, 8: 330, 9: 337}. Each is evaluated at three standardized thresholds, so threshold-cases are 3x the observations and are **not independent** (same player, same game).
- **Standardized thresholds (no historical lines available):** center L0 = floor(model mean)+0.5 for receptions, round(mean)+0.5 for yardage, taken from spec A's walk-forward mean (same thresholds for all specs); offsets L0 -/+ step (step = 1 reception; max(1, round(0.2 x mean)) yards). Because thresholds are set from the model's own mean, they test calibration around the model's expectation, **not** the prices a sportsbook would have posted.
- **Outcomes:** receptions and yards from the same nflverse plays (QB kneel-downs and spikes excluded, as in the pilot; official stats can differ slightly). Monte Carlo: 6,000 draws per observation per spec, fixed seed per player-game-market, shared across specs (paired comparison). MC error is about 0.6 points on any single probability.

## 2. Recomputed historical constants (leakage reconciliation)
League inputs used by the pilot, recomputed using only earlier weeks (rows) beside the full-sample values used in the original pilot (last row). pf_g / rf_g = pass / rush attempts faced per game. Slopes = change in team pass (rush) attempts per point of expected margin (negative: favorites throw less).

| asof | ypc | qb_ypc | ypa | cmp | pf_g | rf_g | gs_pass_slope | gs_rush_slope |
|---|---|---|---|---|---|---|---|---|
| weeks<2 | 4.622 | 6.000 | 6.395 | 0.610 | 33.281 | 26.312 |  |  |
| weeks<3 | 4.347 | 5.776 | 6.326 | 0.609 | 33.688 | 26.156 |  |  |
| weeks<4 | 4.335 | 5.733 | 6.300 | 0.606 | 34.542 | 26.021 | -0.168 | -0.062 |
| weeks<5 | 4.340 | 5.705 | 6.324 | 0.606 | 34.961 | 25.891 | -0.058 | -0.036 |
| weeks<6 | 4.366 | 5.932 | 6.244 | 0.605 | 35.244 | 25.927 | -0.039 | -0.046 |
| weeks<7 | 4.313 | 5.860 | 6.162 | 0.601 | 35.835 | 25.692 | -0.025 | -0.009 |
| weeks<8 | 4.341 | 5.786 | 6.231 | 0.604 | 35.496 | 25.895 | -0.050 | -0.009 |
| weeks<9 | 4.350 | 5.617 | 6.221 | 0.603 | 35.270 | 26.108 | -0.109 | 0.040 |
| weeks<10 | 4.332 | 5.576 | 6.223 | 0.601 | 35.179 | 26.128 | -0.095 | 0.089 |
| FULL (orig) | 4.329 | 5.555 | 6.231 | 0.601 | 35.174 | 26.145 | -0.094 | 0.089 |

**What was and was not recomputed.** Recomputed walk-forward: league yards per carry/attempt, the QB carry yardage mean, the empirical per-play yardage distributions, opponent ypc/ypa allowed, completion-rate-allowed and attempts-faced (spec B), and game-script slopes (spec C). **Held fixed at their original values:** dispersion r (targets 13.5, carries 8.1, attempts 26.3) and the position catch-rate priors (WR .62, TE .72, RB .78) with 15/50/100 pseudo-observations. I do not have the derivation of those values documented in this session, so whether they were originally fit on weeks that overlap the test window is **unresolved**; this leakage is not reconciled and could flatter the results. Specs: **A_orig** = pilot with full-sample league constants (what was originally used); **A0** = pilot with no opponent adjustment of any kind; **A** = pilot with chronologically recomputed league constants (the pilot's 50% opponent efficiency adjustment for yardage is kept); **B** = A plus 50%-shrunk opponent adjustments to volume (attempts or carries faced) and to catch rate (completion rate allowed); **C** = B plus game-script multiplier on pass and rush volume from pregame expected margin relative to the team's own average (slope estimated from prior weeks only, active from week 4, once 3 prior weeks exist, multiplier clipped to 0.75-1.25).

**Effect of the leakage on calibration** (paired Brier difference, lower is better; positive = chronological constants scored worse than the full-sample constants; 95% bootstrap interval, resampling players):

| comparison | mkt | n | dBrier | ci_lo | ci_hi |
|---|---|---|---|---|---|
| A minus A_orig | Receptions | 4302 | 0.000 | 0.000 | 0.000 |
| A minus A_orig | Rush yards | 2190 | 0.001 | -0.000 | 0.003 |
| A minus A_orig | Pass yards | 591 | 0.008 | 0.003 | 0.013 |
| A minus A_orig | All | 7083 | 0.001 | 0.000 | 0.002 |

Receptions are identical because no league constant enters that model. Passing yards score about 0.008 Brier worse with honest constants, so full-sample constants made the original pilot look better than it would have been in real time.

## 3. Over/Under calibration
Pooled across the three thresholds, by market and spec (meanP = mean predicted P(Over); actual = realized Over rate; bias = meanP - actual). n = threshold-cases (3 per observation).

| mkt | spec | n | meanP | actual | bias | brier | logloss |
|---|---|---|---|---|---|---|---|
| Receptions | A_orig | 4302 | 0.448 | 0.437 | 0.011 | 0.221 | 0.635 |
| Receptions | A0 | 4302 | 0.448 | 0.437 | 0.011 | 0.221 | 0.635 |
| Receptions | A | 4302 | 0.448 | 0.437 | 0.011 | 0.221 | 0.635 |
| Receptions | B | 4302 | 0.447 | 0.437 | 0.010 | 0.222 | 0.637 |
| Receptions | C | 4302 | 0.447 | 0.437 | 0.010 | 0.222 | 0.637 |
| Rush yards | A_orig | 2190 | 0.376 | 0.386 | -0.010 | 0.230 | 0.651 |
| Rush yards | A0 | 2190 | 0.384 | 0.386 | -0.003 | 0.233 | 0.659 |
| Rush yards | A | 2190 | 0.382 | 0.386 | -0.004 | 0.231 | 0.654 |
| Rush yards | B | 2190 | 0.382 | 0.386 | -0.005 | 0.232 | 0.657 |
| Rush yards | C | 2190 | 0.382 | 0.386 | -0.005 | 0.232 | 0.656 |
| Pass yards | A_orig | 591 | 0.468 | 0.519 | -0.052 | 0.227 | 0.644 |
| Pass yards | A0 | 591 | 0.469 | 0.519 | -0.050 | 0.228 | 0.648 |
| Pass yards | A | 591 | 0.469 | 0.519 | -0.050 | 0.235 | 0.662 |
| Pass yards | B | 591 | 0.468 | 0.519 | -0.051 | 0.238 | 0.670 |
| Pass yards | C | 591 | 0.468 | 0.519 | -0.052 | 0.238 | 0.670 |

Same by threshold position, specs A, B, C (AUC is computed **within** a threshold, which is the meaningful discrimination measure):

| mkt | spec | thr | n | meanP | actual | bias | brier | auc |
|---|---|---|---|---|---|---|---|---|
| Receptions | A | L0-step | 1434 | 0.655 | 0.619 | 0.035 | 0.231 | 0.596 |
| Receptions | A | L0 (center) | 1434 | 0.446 | 0.440 | 0.006 | 0.243 | 0.570 |
| Receptions | A | L0+step | 1434 | 0.243 | 0.252 | -0.008 | 0.190 | 0.538 |
| Receptions | B | L0-step | 1434 | 0.652 | 0.619 | 0.033 | 0.231 | 0.594 |
| Receptions | B | L0 (center) | 1434 | 0.444 | 0.440 | 0.004 | 0.245 | 0.564 |
| Receptions | B | L0+step | 1434 | 0.243 | 0.252 | -0.009 | 0.191 | 0.537 |
| Receptions | C | L0-step | 1434 | 0.652 | 0.619 | 0.033 | 0.232 | 0.594 |
| Receptions | C | L0 (center) | 1434 | 0.444 | 0.440 | 0.004 | 0.245 | 0.564 |
| Receptions | C | L0+step | 1434 | 0.243 | 0.252 | -0.009 | 0.191 | 0.540 |
| Rush yards | A | L0-step | 730 | 0.475 | 0.456 | 0.018 | 0.245 | 0.570 |
| Rush yards | A | L0 (center) | 730 | 0.377 | 0.385 | -0.008 | 0.234 | 0.544 |
| Rush yards | A | L0+step | 730 | 0.294 | 0.318 | -0.024 | 0.215 | 0.554 |
| Rush yards | B | L0-step | 730 | 0.474 | 0.456 | 0.018 | 0.246 | 0.567 |
| Rush yards | B | L0 (center) | 730 | 0.377 | 0.385 | -0.008 | 0.235 | 0.544 |
| Rush yards | B | L0+step | 730 | 0.294 | 0.318 | -0.024 | 0.215 | 0.560 |
| Rush yards | C | L0-step | 730 | 0.474 | 0.456 | 0.018 | 0.246 | 0.565 |
| Rush yards | C | L0 (center) | 730 | 0.377 | 0.385 | -0.008 | 0.235 | 0.543 |
| Rush yards | C | L0+step | 730 | 0.294 | 0.318 | -0.024 | 0.215 | 0.562 |
| Pass yards | A | L0-step | 197 | 0.675 | 0.685 | -0.011 | 0.219 | 0.409 |
| Pass yards | A | L0 (center) | 197 | 0.460 | 0.523 | -0.063 | 0.253 | 0.518 |
| Pass yards | A | L0+step | 197 | 0.274 | 0.350 | -0.076 | 0.231 | 0.622 |
| Pass yards | B | L0-step | 197 | 0.671 | 0.685 | -0.014 | 0.221 | 0.459 |
| Pass yards | B | L0 (center) | 197 | 0.459 | 0.523 | -0.064 | 0.255 | 0.520 |
| Pass yards | B | L0+step | 197 | 0.275 | 0.350 | -0.075 | 0.238 | 0.489 |
| Pass yards | C | L0-step | 197 | 0.671 | 0.685 | -0.015 | 0.221 | 0.474 |
| Pass yards | C | L0 (center) | 197 | 0.458 | 0.523 | -0.065 | 0.255 | 0.521 |
| Pass yards | C | L0+step | 197 | 0.275 | 0.350 | -0.075 | 0.238 | 0.493 |

**Over-leaning vs Under-leaning predictions** (spec A; cases where the model's P(Over) is above or below 50%; meanP_side = mean model probability of the side it leans toward; gap = predicted minus realized hit rate, positive = overconfident):

| mkt | side | n | meanP_side | hit | gap |
|---|---|---|---|---|---|
| Receptions | Over-leaning (P>.5) | 1793 | 0.633 | 0.600 | 0.033 |
| Receptions | Under-leaning (P<.5) | 2509 | 0.684 | 0.680 | 0.005 |
| Rush yards | Over-leaning (P>.5) | 334 | 0.559 | 0.503 | 0.056 |
| Rush yards | Under-leaning (P<.5) | 1856 | 0.650 | 0.635 | 0.015 |
| Pass yards | Over-leaning (P>.5) | 197 | 0.675 | 0.685 | -0.011 |
| Pass yards | Under-leaning (P<.5) | 394 | 0.633 | 0.563 | 0.070 |
| All | Over-leaning (P>.5) | 2324 | 0.626 | 0.593 | 0.032 |
| All | Under-leaning (P<.5) | 4759 | 0.667 | 0.652 | 0.014 |

**Reliability by predicted probability** (spec A, pooled thresholds; bins with n < 30 are directional only):

| mkt | bin | n | meanP | actual |
|---|---|---|---|---|
| Receptions | [0.0, 0.1) | 39 | 0.093 | 0.179 |
| Receptions | [0.1, 0.2) | 367 | 0.157 | 0.210 |
| Receptions | [0.2, 0.3) | 718 | 0.252 | 0.277 |
| Receptions | [0.3, 0.4) | 729 | 0.349 | 0.324 |
| Receptions | [0.4, 0.5) | 656 | 0.451 | 0.434 |
| Receptions | [0.5, 0.6) | 756 | 0.551 | 0.520 |
| Receptions | [0.6, 0.7) | 604 | 0.646 | 0.618 |
| Receptions | [0.7, 0.8) | 340 | 0.741 | 0.712 |
| Receptions | [0.8, 0.9) | 93 | 0.823 | 0.731 |
| Rush yards | [0.1, 0.2) | 12 | 0.189 | 0.000 |
| Rush yards | [0.2, 0.3) | 411 | 0.271 | 0.243 |
| Rush yards | [0.3, 0.4) | 885 | 0.335 | 0.390 |
| Rush yards | [0.4, 0.5) | 548 | 0.437 | 0.425 |
| Rush yards | [0.5, 0.6) | 304 | 0.554 | 0.500 |
| Rush yards | [0.6, 0.7) | 30 | 0.606 | 0.533 |
| Pass yards | [0.2, 0.3) | 193 | 0.273 | 0.342 |
| Pass yards | [0.3, 0.4) | 4 | 0.306 | 0.750 |
| Pass yards | [0.4, 0.5) | 197 | 0.460 | 0.523 |
| Pass yards | [0.5, 0.6) | 1 | 0.568 | 1.000 |
| Pass yards | [0.6, 0.7) | 184 | 0.673 | 0.707 |
| Pass yards | [0.7, 0.8) | 12 | 0.704 | 0.333 |

**Reading.** The model is not systematically too Under-heavy for receptions or rushing: pooled bias is +1.1 and -0.4 points, and both Over- and Under-leaning predictions are overconfident by a few points. The overconfidence concentrates in the tails (predicted 80-90% receptions hit 73%; predicted under 10% hit 18%). Passing yards are different: the pilot underestimates Overs by about 5 points, and its Under-leaning predictions are 7 points overconfident (n = 394 threshold-cases from 197 QB-games).

## 4. PIT histograms and distributional diagnostics
Randomized probability-integral-transform values from each simulated distribution; a calibrated distribution gives a uniform histogram. Columns show the percentage of observations in each of 10 equal bins from 0-0.1 to 0.9-1.0 (uniform = 10 each). chi2_p is a chi-square test of uniformity (exploratory; observations are weakly dependent).

| mkt | spec | n | meanPIT | chi2_p | hist |
|---|---|---|---|---|---|
| Receptions | A_orig | 1434 | 0.494 | 0.031 | 12 10 10 9 9 9 9 9 10 12 |
| Receptions | A | 1434 | 0.494 | 0.031 | 12 10 10 9 9 9 9 9 10 12 |
| Receptions | B | 1434 | 0.496 | 0.003 | 12 11 10 10 8 10 9 9 10 12 |
| Receptions | C | 1434 | 0.496 | 0.012 | 12 11 10 9 9 10 9 9 9 12 |
| Rush yards | A_orig | 730 | 0.498 | 0.016 | 12 11 9 10 8 9 8 9 9 13 |
| Rush yards | A | 730 | 0.494 | 0.005 | 13 11 8 10 9 8 8 10 9 13 |
| Rush yards | B | 730 | 0.494 | 0.005 | 13 10 9 11 8 9 8 10 9 13 |
| Rush yards | C | 730 | 0.494 | 0.009 | 13 10 9 10 9 8 8 10 9 13 |
| Pass yards | A_orig | 197 | 0.518 | 0.197 | 11 9 9 6 8 10 13 15 10 9 |
| Pass yards | A | 197 | 0.518 | 0.014 | 12 9 10 4 9 10 10 17 12 8 |
| Pass yards | B | 197 | 0.519 | 0.115 | 11 11 7 8 6 14 10 14 13 9 |
| Pass yards | C | 197 | 0.519 | 0.045 | 10 12 6 8 6 14 9 15 12 9 |

U-shaped histograms (excess 0-0.1 and 0.9-1.0, about 12-13% each) for receptions and rushing mean the predictive distributions are **slightly too narrow**: realized outcomes land in the tails more often than the model implies. That fits the tail overconfidence in section 3. Passing-yardage PIT is noisier (n = 197) and less uniform with chronological constants than with full-sample constants.

Mean predicted vs realized outcome (units: receptions or yards):

| mkt | spec | n | mean_pred | mean_actual | MAE |
|---|---|---|---|---|---|
| Receptions | A_orig | 1434 | 2.766 | 2.709 | 1.534 |
| Receptions | A | 1434 | 2.766 | 2.709 | 1.534 |
| Receptions | B | 1434 | 2.760 | 2.709 | 1.538 |
| Receptions | C | 1434 | 2.759 | 2.709 | 1.538 |
| Rush yards | A_orig | 730 | 28.989 | 29.271 | 16.871 |
| Rush yards | A | 730 | 29.144 | 29.271 | 17.154 |
| Rush yards | B | 730 | 29.170 | 29.271 | 17.215 |
| Rush yards | C | 730 | 29.160 | 29.271 | 17.211 |
| Pass yards | A_orig | 197 | 213.319 | 211.411 | 63.676 |
| Pass yards | A | 197 | 213.741 | 211.411 | 65.550 |
| Pass yards | B | 197 | 213.405 | 211.411 | 65.270 |
| Pass yards | C | 197 | 213.267 | 211.411 | 65.302 |

Means are close to unbiased in every market (receptions 2.77 vs 2.71, rush yards 29.1 vs 29.3, pass yards 213.7 vs 211.4), so the issue is the spread and shape of the distribution, not the center.

## 5. Brier score and log loss
Pooled values are in the table in section 3. For reference, the Brier score of a predictor that only knows the threshold position (the realized Over rate at each of the three thresholds, in-sample, so a deliberately favorable benchmark) versus spec A:

| mkt | n_obs | n_threshold_cases | brier_model_A | brier_offset_base_rate | skill |
|---|---|---|---|---|---|
| Receptions | 1434 | 4302 | 0.221 | 0.224 | 0.009 |
| Rush yards | 730 | 2190 | 0.231 | 0.234 | 0.012 |
| Pass yards | 197 | 591 | 0.235 | 0.231 | -0.016 |

Skill (1 minus model Brier / benchmark Brier) is about +0.9% for receptions and +1.2% for rushing yards, and **-1.6% for passing yards (worse than the benchmark)**. So beyond the information already contained in where the threshold sits relative to the model's own mean, the probabilities add very little, and for passing yards they subtract. The benchmark uses realized Over rates in-sample, so it is favorable to the benchmark, but the conclusion is that the pilot's shape and spread assumptions add little scoring value here, which is consistent with the weak within-threshold AUCs.

## 6. Standardized-threshold sensitivity
The three threshold positions in section 3 are the sensitivity analysis. Calibration bias is small at the center and one step above (receptions -0.8 to +0.6 points; rush yards -2.4 to -0.8) and larger at the low threshold for receptions (+3.5 points: the model overstates P(Over) when the line is one catch below its mean). Passing yards under-predict Overs at the center (-6.3) and one step above (-7.6). Discrimination (within-threshold AUC) is 0.54-0.60 for receptions, 0.54-0.57 for rushing, and 0.41-0.62 for passing yards (n = 197 each, essentially no reliable ranking power at the low threshold).

Subgroups that matter for the LEAN archetypes (spec A; side = Under unless noted; **exploratory, defined after seeing the overall results, so not independent confirmation**; gap = predicted minus realized, positive = overconfident):

| group | spec | n | meanP_side | hit | gap | brier |
|---|---|---|---|---|---|---|
| Rec, tgtEW<2.5, all thresholds (Under side) | A | 1473 | 0.575 | 0.555 | 0.020 | 0.218 |
| Rec, tgtEW<2.5, P(Under)>=0.70 | A | 542 | 0.812 | 0.751 | 0.061 | 0.187 |
| Rec, tgtEW<2.5, line<=1.5, P(Under)>=0.70 | A | 235 | 0.779 | 0.706 | 0.073 | 0.210 |
| Rec, tgtEW 2.5-5, P(Under)>=0.70 | A | 400 | 0.771 | 0.725 | 0.046 | 0.202 |
| Rec, tgtEW>=5, P(Under)>=0.70 | A | 185 | 0.732 | 0.795 | -0.063 | 0.167 |
| Rec, RB, P(Under)>=0.55 | A | 518 | 0.720 | 0.745 | -0.025 | 0.194 |
| Rec, TE, P(Under)>=0.55 | A | 571 | 0.711 | 0.676 | 0.035 | 0.222 |
| Rush, QB, P(Under)>=0.70 | A | 90 | 0.724 | 0.644 | 0.079 | 0.237 |
| Rush, non-QB, P(Under)>=0.70 | A | 334 | 0.733 | 0.793 | -0.060 | 0.164 |
| Pass, P(Under)>=0.60 | A | 197 | 0.726 | 0.650 | 0.076 | 0.231 |
| Pass, P(Over)>=0.60 | A | 196 | 0.675 | 0.684 | -0.009 | 0.219 |

Overconfidence is largest for QB rushing Unders (+7.9 points, n = 90, 27 players), low-volume receiver Unders (+6.1, n = 542; +7.3 at lines of 1.5 or lower, n = 235) and passing-yardage Unders (+7.6, n = 197). The model is **underconfident** (gap about -6) for high-target receiver Unders and for non-QB rushing Unders, which means the stated edges there were understated, not overstated.

## 7. A/B/C specification comparison (no winner declared)
Paired Brier difference per spec comparison, 95% bootstrap interval resampling players (negative = second spec scored better; threshold-cases pooled):

| comparison | mkt | n | dBrier | ci_lo | ci_hi |
|---|---|---|---|---|---|
| A minus A_orig | Receptions | 4302 | 0.000 | 0.000 | 0.000 |
| A minus A_orig | Rush yards | 2190 | 0.001 | -0.000 | 0.003 |
| A minus A_orig | Pass yards | 591 | 0.008 | 0.003 | 0.013 |
| A minus A_orig | All | 7083 | 0.001 | 0.000 | 0.002 |
| A minus A0 | Receptions | 4302 | 0.000 | 0.000 | 0.000 |
| A minus A0 | Rush yards | 2190 | -0.002 | -0.005 | 0.000 |
| A minus A0 | Pass yards | 591 | 0.006 | -0.001 | 0.013 |
| A minus A0 | All | 7083 | -0.000 | -0.001 | 0.001 |
| B minus A | Receptions | 4302 | 0.001 | -0.000 | 0.002 |
| B minus A | Rush yards | 2190 | 0.001 | -0.001 | 0.004 |
| B minus A | Pass yards | 591 | 0.003 | -0.003 | 0.011 |
| B minus A | All | 7083 | 0.001 | 0.000 | 0.003 |
| C minus B | Receptions | 4302 | -0.000 | -0.000 | 0.000 |
| C minus B | Rush yards | 2190 | -0.000 | -0.000 | 0.000 |
| C minus B | Pass yards | 591 | 0.000 | -0.001 | 0.001 |
| C minus B | All | 7083 | -0.000 | -0.000 | 0.000 |
| C minus A | Receptions | 4302 | 0.001 | -0.000 | 0.002 |
| C minus A | Rush yards | 2190 | 0.001 | -0.001 | 0.003 |
| C minus A | Pass yards | 591 | 0.003 | -0.003 | 0.011 |
| C minus A | All | 7083 | 0.001 | 0.000 | 0.003 |

**Reading.** B minus A is about +0.001 (all markets, interval 0.000 to 0.003): adding my opponent adjustment to volume and catch rate did **not** improve out-of-sample scoring. C minus B is about 0.000: the game-script term moved probabilities very little (the estimated slope is small and changes sign for rushing across weeks, which means the multiplier was mostly close to 1). A minus A0 (does the pilot's existing 50% opponent efficiency adjustment for yardage help?) is -0.002 for rushing (interval -0.005 to 0.000) and +0.006 for passing (interval -0.001 to 0.013), so no clear benefit. **These are results for these specific, deliberately simple implementations with a fixed 50% shrink and no tuning; they do not show that opponent or game-script effects do not matter.** No specification is selected here. Adoption of any of them would need a separate validation period.

## 8. Five-LEAN survival analysis
Re-running the five pregame LEANs with the week-10 inputs (history through week 9; lines from the Lock 2 card) under each spec. Probability is for the pregame side, in %. BE = break-even implied by the quoted price. frozen = probability recorded in the Lock 2 card.

| prop | price | BE | frozen | A_orig | A0 | A | B | C | games |
|---|---|---|---|---|---|---|---|---|---|
| Bryce Young (CAR) U9.5 rush | -115 | 53.500 | 81.500 | 81.300 | 83.900 | 81.200 | 80.100 | 80.300 | 8 |
| Bijan Robinson (ATL) U3.5 rec | 125 | 44.400 | 58.000 | 58.000 | 58.000 | 58.000 | 57.500 | 57.200 | 9 |
| Kyle Pitts (ATL) U3.5 rec | 115 | 46.500 | 59.300 | 60.500 | 60.500 | 60.500 | 59.600 | 59.700 | 9 |
| Deion Burks (IND) U1.5 rec | 125 | 44.400 | 82.400 | 81.500 | 81.500 | 81.500 | 81.700 | 82.400 | 8 |
| Laquon Treadwell (IND) U2.5 rec | -160 | 61.500 | 75.700 | 75.500 | 75.500 | 75.500 | 76.000 | 76.200 | 9 |

Edge (probability minus break-even, points):

| prop | edge_A_orig | edge_A0 | edge_A | edge_B | edge_C |
|---|---|---|---|---|---|
| Bryce Young (CAR) U9.5 rush | 27.800 | 30.400 | 27.700 | 26.600 | 26.800 |
| Bijan Robinson (ATL) U3.5 rec | 13.600 | 13.600 | 13.600 | 13.000 | 12.700 |
| Kyle Pitts (ATL) U3.5 rec | 14.000 | 14.000 | 14.000 | 13.100 | 13.200 |
| Deion Burks (IND) U1.5 rec | 37.100 | 37.100 | 37.100 | 37.300 | 38.000 |
| Laquon Treadwell (IND) U2.5 rec | 13.900 | 13.900 | 13.900 | 14.500 | 14.700 |

All five keep the same side and a large positive gap under every specification (differences of at most about 3 points from the frozen number), so **the alternative specs do not change the picture**; the specs differ very little from each other for these players. Historical hit rates in analogous buckets from this audit (same market and position, similar model probability; Wilson 95% interval; BE = the price of the actual LEAN):

| bucket | n | players | meanP_under | hit | wilson95 | BE |
|---|---|---|---|---|---|---|
| Young: QB rush, P(Under) 0.70-0.90 | 90 | 27 | 72.400 | 64.400 | 54.1-73.6 | 53.500 |
| Bijan: RB rec, P(Under) 0.55-0.65 | 138 | 60 | 60.400 | 71.700 | 63.7-78.6 | 44.400 |
| Pitts: TE rec, P(Under) 0.55-0.65 | 178 | 54 | 60.200 | 61.800 | 54.5-68.6 | 46.500 |
| Burks: WR rec, tgtEW<2.5, line<=1.5, P(Under) 0.70-0.95 | 117 | 58 | 78.600 | 75.200 | 66.7-82.2 | 44.400 |
| Treadwell: WR rec, P(Under) 0.70-0.80 | 344 | 131 | 74.400 | 71.800 | 66.8-76.3 | 61.500 |

**Reading.** Historical hit rates in analogous buckets stay above the LEAN break-even prices, but the Young bucket is the weakest (lower bound 54.1% against BE 53.5%; model said 72.4%, realized 64.4%), consistent with the QB-rushing overconfidence in section 6. The Burks bucket realized 75.2% against a model 78.6%, still far above 44.4%. The Bijan bucket realized 71.7% against a model 60.4% (the model was underconfident). These are **calibration checks at standardized thresholds, not tests at sportsbook lines**: a LEAN is selected because the model disagrees with the market, and that selection (the market may know role or injury information the model lacks) is not tested here. So the audit gives no support for treating a 25-38 point stated edge as a real advantage of that size.

## 9. Sample-size and uncertainty assessment
- Observations by market: receptions 1434, rushing 730, passing 197 (each at 3 thresholds, so effective independent sample is the observation count, not the case count). Passing yards are the thinnest: all passing-yardage findings are directional.
- Week coverage: 7 weeks (3-9) of a single season; results can differ in other seasons or after role changes. Player counts in buckets: see the players column in section 8 (27 to 131 distinct players).
- Calibration bins with n < 30 (several extreme bins) are not interpretable. Subgroup tables contain many comparisons and were defined post hoc; treat gaps under about 4-5 points as noise.
- Monte Carlo error about 0.6 points per probability; bootstrap intervals resample players but not games.

## 10. Limitations and conclusions
**Limitations**
1. No historical sportsbook lines or prices, so profitability, closing-line value and the market-disagreement selection effect are untested.
2. Dispersion r and the position catch priors are original constants of undocumented origin; possible leakage there is unresolved (section 2).
3. Standardized thresholds come from the model's own mean (a calibration test around the model's center).
4. Specs B and C are single, simple implementations with fixed 50% shrink and no tuning; negative results do not generalize to the concepts.
5. Week 2 excluded; only weeks 3-9 of 2026; defined "active" as offense snaps > 0 (later-game injuries are not voided); QB kneel-downs excluded from the data but counted in official stats; no passing TD or receiving-yard audit (TDs and receiving yards are not modeled).
6. Subgroup analyses were defined after viewing overall results.

**Conclusions (for review; none applied)**
- Average calibration is acceptable for receptions and rushing yards, but scoring skill beyond the threshold position is only about 1% (negative for passing yards), so the probabilities carry little extra information; probabilities in the 80-90% range and below 10% should not be taken at face value (about 73% realized at 82% predicted for receptions).
- No evidence of a structural Under bias in receptions or rushing; passing yards show a real Under overstatement of about 7 points (directional, n = 197).
- The LEAN archetypes (low-volume receivers, QB rushing, pass-yardage Unders) are where the model's overconfidence is largest (about 6-8 points); the LEANs survive every spec but their stated probabilities are probably 5-8 points too high, and the size of the market disagreement should not be read as the size of an edge.
- Opponent and game-script adjustments, as implemented here, did not improve out-of-sample Brier. Any adoption needs an independent validation period.
- Possible follow-ups for independent review: obtain historical lines to test calibration at real prices; document how r and the catch priors were fit; test a variance/tail-widening specification on a **held-out** period; add a held-out week 10-12 prospective check.

Governance: NFL Player Prop Model v2.2 FROZEN. Nov 15 Lock 2 card FROZEN. Calibration research branch APPROVED. Model parameter changes NOT AUTHORIZED.
