# Discovery baseline fit (k=8), non-F4 only — authorized, restricted

Registry NOT_FROZEN; no commits; no F4/validation/holdout/prospective outcomes read; no F4 test run. Coefficients are candidate frozen inputs, pending commit/freeze authorization.

```json
{
 "run_utc": "2026-11-13T13:05:14.932893+00:00",
 "k_shrinkage": 8,
 "sample": {
  "discovery_partition_rows": 5316,
  "REG_rows": 5096,
  "excluded_not_eligible_(a_team_has_0_games)": 321,
  "excluded_F4_games": 766,
  "fit_sample_rows": 4009
 },
 "ties_in_fit_sample": 7,
 "seasons": [
  1999,
  2018
 ],
 "coefficients": {
  "b0_intercept": 0.35086712927793096,
  "b1_d": 3.8959057735807017
 },
 "std_err_robust_season_week_clustered": [
  0.031926616647934766,
  0.22892441898751226
 ],
 "irls_iterations": 6,
 "converged": true,
 "diagnostics": {
  "mean_h": 0.5770765777001746,
  "mean_fitted": 0.5770765777001746,
  "logloss": 0.6433521029347784,
  "logloss_intercept_only": 0.6812180723717304,
  "d_min_max": [
   -0.5263157894736842,
   0.5909090909090909
  ]
 },
 "hashes": {
  "discovery_game_features_partition_sha256": "fe053ea802067ab7cd14c23a5ea650897330b4a137846628cbe72249770ede0e",
  "outcome_source_sha256_games.csv": "5ae004ff6d26b08109cbd7424127b0eaa89f59a4bed445229e8683e98d22c8d0",
  "stopping_rule_module_sha256": "0dd88805a4c7f87aa466c75d5bbf64e4e6984b5b0f584e6f4a53428708c201ad",
  "fit_script_sha256": "431af77e65c96cbd0feac3ee0c2144af3497063f6421c168410555c15ffebafc",
  "fit_sample_game_id_list_sha256": "544781d6ae6d9d776c6f8c623de18f5b289d4f52a8b84b25e503ec94498ca3a2"
 },
 "outcome_scope": "home_score,away_score for discovery non-F4 eligible REG games only; no F4, validation, holdout or prospective outcomes read; no F4 test run"
}```

Calibration by decile of d (fit sample only):
|   dec |   n |   mean_d |   mean_h |   mean_fit |
|------:|----:|---------:|---------:|-----------:|
|     0 | 402 |  -0.274  |   0.3321 |     0.3305 |
|     1 | 402 |  -0.1611 |   0.4428 |     0.4314 |
|     2 | 416 |  -0.1022 |   0.4868 |     0.4882 |
|     3 | 392 |  -0.0588 |   0.5485 |     0.5304 |
|     4 | 746 |  -0.0049 |   0.5791 |     0.5821 |
|     5 |  53 |   0.0262 |   0.6038 |     0.6114 |
|     6 | 402 |   0.0535 |   0.6281 |     0.6362 |
|     7 | 399 |   0.0987 |   0.6541 |     0.6759 |
|     8 | 410 |   0.1544 |   0.7073 |     0.7213 |
|     9 | 387 |   0.2652 |   0.8191 |     0.7968 |

Note: k=4/16 sensitivity coefficients were NOT fitted (not within the stated authorization).
