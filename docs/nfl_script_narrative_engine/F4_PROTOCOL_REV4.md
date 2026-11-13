# F4 protocol — revision 4 (authoritative consolidated text)

Status: registry NOT_FROZEN; coefficients PROVISIONAL; A2 is the SOLE stopping rule (A1/A3 retired). Supersedes review package 2 v1/v2 and the revision 3 addendum where they differ. Simulations use simulated outcomes only; they show calibration under the tested data-generating processes, not exchangeability under every real-world misspecification.

## 0. Binning convention (revision 4 clarification)
d-bins are right-closed: `<= -0.15 | (-0.15, -0.05] | (-0.05, 0.05] | (0.05, 0.15] | > 0.15`, evaluated in exact integer arithmetic (for equal games played G: d = (2(Wh-Wa)+(Th-Ta)) / (2(G+8)); compare 20*numerator with e*denominator, e in {-3,-1,1,3}). Games-played classes {1-2, 3-4, 5-8, 9+}. Implementation: `scripts/f4_stopping_rule.py`.

## 1. Exact algorithm (sections 4-5 of the revision 3 addendum, retained)
## 4. F4 test: exact algorithm (primary, frozen-coefficient evaluation)

**Inputs (all fixed before outcomes are joined):** list of eligible games in the evaluation sample (regular-season, both teams with >= 1 completed game) with pregame records W, L, T for each team, game id, season-week id; frozen k = 8 and coefficients (b0, b1); B = 100,000 and a recorded seed. Outcomes h (home 1, tie 0.5, away 0) are joined only at step 1.

1. For each eligible game g: `sw_team = (W + 0.5T + 4) / (G + 8)`; `d_g = sw_home - sw_away`; `e_g = logistic(b0 + b1*d_g)`; `r_g = h_g - e_g`.
2. **Season-week centring:** for each season-week w, `rt_g = r_g - mean(r over ALL eligible games in w)`. No F4 label is used here.
3. **Strata:** equal-G eligible games (G_home = G_away) only. Stratum = (games-played class of the home team in {1-2, 3-4, 5-8, 9+}) x (d-bin in {<= -0.15, (-0.15, -0.05], (-0.05, 0.05], (0.05, 0.15], > 0.15}). Unequal-G games have no stratum and only enter step 2.
4. **Support (outcome-blind):** for each stratum s, N_s = equal-G eligible games in s, n1_s = F4 games in s. s is **supported** iff n1_s >= 1 and N_s - n1_s >= 20. All other F4 games are off-support.
5. n1 = sum of n1_s over supported strata. `c = sum over supported s of n1_s * mean(rt over all N_s games in s)`.
6. **Observed statistic:** `T_obs = sum of rt_g over supported F4 games - c`. Reported effect = T_obs / n1 in home-win-probability points.
7. **Permutations, b = 1..B:** inside each supported stratum, choose n1_s of its N_s games uniformly at random without replacement and call them pseudo-F4. **Held fixed:** coefficients, e, r, rt, strata, N_s, n1_s, c. **Varies:** which games carry the label. `T*_b = sum of rt_g over pseudo-F4 games - c`. Nothing is refit, because the coefficients are frozen and centring does not use labels.
8. `p = (1 + #{b : |T*_b| >= |T_obs|}) / (1 + B)`. Reject H0 if p < 0.05 (two-sided).
9. **Always also reported:** n1 and n off-support (overall and by stratum), the descriptive mean h and mean residual of off-support F4 games (non-inferential), ties as a separate count with an exact interval, k = 4 and k = 16 results, the model-based z-test, and the achieved MDE.

**Discovery (in-sample) version:** steps 1-8, except that in step 1 the baseline is fitted on the non-F4 eligible games of the sample, and **inside every permutation** the fit is repeated excluding the games carrying that permutation's labels (off-support F4 games keep their real label and stay excluded), then r, rt, c and T* are recomputed from that fit. Implemented in `f4_refit_sim.py`.

## 5. On-support definition (answers to your five questions)

| Question | Rule |
|---|---|
| Comparators counted before or after other exclusions? | After removing games with either team at 0 completed games and after restricting to equal-G games; before any other exclusion. The count is non-F4 equal-G eligible games in the stratum. |
| Applied within each season-week? | No. Strata pool all season-weeks in the evaluation sample. Season-week enters only through centring. |
| Entirely outcome-blind? | Yes. It uses pregame records only. The supported-stratum list and the list of on-support games are computed and hashed **before** outcomes are joined. |
| How are unsupported F4 games reported? | Counts by stratum and overall, plus descriptive mean h and mean residual with intervals, labelled non-inferential. They are never part of the confirmatory claim. |
| Is the primary effect limited to on-support games? | **Yes, explicitly.** The estimand is the effect among F4 games with sufficient comparison support. The report must say so in the first sentence of the result. |

The 20-comparator threshold is a design choice, not tuned. Sensitivity at 10 and 40 comparators is proposed as non-primary but has **not** been simulated. The 20-comparator threshold stays **unapproved** until you decide.

## 2. Stopping rule A2 (sole rule)
One evaluation, at the end of the first regular-season week at which the CUMULATIVE count of on-support F4 games reaches 188. Support is recomputed from scratch on all prospective games to date at every week-end (`cumulative_on_support`); the support list is SHA-256 hashed before any outcome is joined; the evaluation week and cumulative sample are then immutable. No interim outcome analysis. Real 2026 pregame check (weeks 2-9, 120 eligible games, 33 F4): 0 on-support F4 games, 0 supported strata, threshold not reached; independent recomputation matched at every week-end (`simulations/f4_revision4/results/real_pregame_stopping_check*`).

## 3. Frozen-coefficient baseline
k = 8. Coefficients are fitted ONCE on discovery (1999-2018) non-F4 eligible regular-season games (4,009 games; 766 F4 and 321 week-1 games excluded): b0 = 0.3509, b1 = 3.896 (robust SE 0.032, 0.229). PROVISIONAL until the freeze. The discovery refit procedure (baseline refit inside every permutation) is exploratory only and non-confirmatory.

## 4. Simulation evidence (simulated outcomes; corrected module; R = 5,000 per cell; B = 199)
Type I at alpha = 0.05 under 12 null models x comparator thresholds 10/20/40: 3.7%-5.1% (primary threshold 20: 3.7%-5.1%; maximum cell 5.1%, within one MC SE of 5%). Stress nulls: week-level shock and signal-scale heterogeneity, team random effects, season-level home-edge shift, combined null. At threshold 20 the evaluation lands at about 190 on-support F4 games (95th pct about 209), 12-18 supported strata (median 16), effective size about 143, about 6 seasons (5-7). Discovery refit at about 20 seasons (N = 5,116, R = 1,000): lat060: 3.7%; gslope: 4.1%; eqbonus_big: 4.7%; combo: 4.3%; weekshock: 4.8%. Power: latent SD0.60, threshold 20: 8 pts 44.4%; 10 pts 63.5%; 12 pts 80.1%; 14 pts 91.2%. 10 pts at threshold 10 / 40: 61.2% / 70.2%; latent SD0.35: 63.6%; combined null: 67.5%. **80%-power MDE about 12 points**; a 10-point effect remains under-powered. Earlier 10.2-point figure withdrawn. Full tables: V1_1_REVISION4_ADDENDUM.md sections 2-5.

## 5. Permutation counts by procedure (do not conflate)
| Procedure | Permutations B |
|---|---|
| Type I and power simulation grid (R = 5,000 / 4,000 per cell) | 199 |
| Discovery-refit calibration (R = 1,000 per null) | 199 |
| Full-scale execution / calibration checks (3 arms x 1,500 evaluations) | 100,000 |
| Future primary F4 evaluation | 100,000 |

## 5a. Full-scale execution check (B = 100,000)
Implementation `scripts/f4_permutation_test.py` (T* = per-stratum sum of the first n1_s entries of a random permutation of centred residuals, minus c; 5,000-permutation blocks, per-block `SeedSequence.spawn` seeds), validated by simulation with SIMULATED outcomes only, B = 100,000, final A2 design, threshold 20, frozen coefficients, R = 1,500 evaluations per arm:

| Arm | Coefficients | Rejection at 0.05 (MC SE) | p deciles 10..90% | sd(T*)/exact sd (mean, min, max) |
|---|---|---|---|---|
| latent SD 0.60 | simulated-training | 4.80% (0.55) | .10 .19 .31 .43 .52 .61 .71 .82 .91 | 1.0000, 0.993, 1.009 |
| latent SD 0.60 | REAL provisional (0.3509, 3.896) | 5.07% (0.57) | .11 .20 .32 .41 .49 .59 .69 .80 .90 | 1.0000, 0.992, 1.007 |
| combined stress | simulated-training | 4.93% (0.56) | .10 .19 .27 .39 .48 .59 .68 .79 .89 | 1.0000, 0.993, 1.007 |

Checks: observed statistic and support identical regardless of seed/B/run order; same seed reproduces the entire T* vector exactly and the same p; different seeds give p within Monte Carlo error (0.08359 vs 0.08345 on one evaluation); the permutation null variance matches the closed-form without-replacement variance (ratio 1.000); mean |mean(T*)| <= 0.064; support (on-support F4 count, supported strata, effective size) agrees with the independent B = 199 implementation in 100% of 4,500 evaluations; 0 numerical warnings (RuntimeWarnings were promoted to errors); all 4,500 evaluations reached the 188 threshold within 10 simulated seasons; seeds 20261201-20261203 (evaluation r uses seed*1000 + r). All three arms were re-run with the FINAL module (sha256 a487b251…55b7) and the parameterized scripts and reproduced the earlier arms bit-for-bit (identical rejection rates, p-value deciles and variance ratios), confirming that the binning correction and the ineligible-game guard do not alter these results. Runtime 1.3 s per full B = 100,000 test, peak memory about 140 MB. Exact-enumeration check on a 2-stratum toy problem: exact p 0.0794 vs Monte Carlo 0.0801. Limits: this validates the full-scale implementation and its computational behaviour under simulated nulls; it does not establish exchangeability for real data, and the simulated evaluations used the schedule structure of 2021-2025 repeated.

## 6. Limitations and disclosures
Estimand = on-support F4 games only; off-support F4 reported descriptively and non-inferentially. Nulls are simulated stress scenarios. The 12 x 3 Type I grid and the 20-season refit simulation predate the d-bin fix (re-checked on a subset, see section 4). Confirmatory evaluation not started; Tier B test not specified.
