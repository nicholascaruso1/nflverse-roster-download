# Tier B definitions and denominators — revision 4 (consolidated)

Status: registry NOT_FROZEN. **The Tier B outcome TEST is NOT specified or approved** (null hypothesis, comparator construction, home/away and strength treatment, inferential procedure, multiplicity implementation all pending). Nothing here authorizes a Tier B outcome test.

Supersedes the untestable-feature counts in earlier packages: **98 STRUCTURAL / 33 EMPIRICAL_ZERO** (not 106/25), derived with mathematical bounds (see `reference/untestable_features_v1.1_rev4.csv`, columns zero_class_rev3 vs zero_class_rev4). A feature is STRUCTURAL only if every possible name value (all eras, both bases) is disjoint from the mathematically feasible set of the quantity; the six days_since / months_since quantities have no mathematical upper bound and can never be structural. The 8 reclassified features are season_ties x {city,nickname} x {historical,current} x {pythagorean, reverse_root}.

Counts: 504 nominal; 98 structural; 33 empirical-zero (regular-season sample 1999-2026, re-evaluated as seasons are added; never described as impossible); 373 with at least one regular-season match; 223 distinct observed flag columns (equivalence classes), NOT independent hypotheses.

## A. The 14 quantities (approved; unchanged; from review package 1 v2)
## 1. The 14 quantities (APPROVED as defined; unchanged)

| # | quantity | definition (unchanged from revision 1) |
|---|---|---|
| 1 | days_remaining | Dec 31 of the game's **calendar** year minus game date (game date excluded) |
| 2 | date_digit_sum | digit sum of YYYYMMDD |
| 3 | date_digit_root | digital root of #2 |
| 4 | weekday_number | ISO weekday, Mon=1..Sun=7 |
| 5 | schedule_week | nflverse `week`, including postseason numbering that overlaps late regular-season weeks |
| 6-8 | season_wins / losses / ties | regular-season record in the same NFL season before the date; full regular-season record for postseason games |
| 9-10 | days_since_last_win_rs / loss_rs | regular-season results only; franchise-continuous across relocations |
| 11-12 | days_since_last_win_all / loss_all | postseason results included |
| 13 | days_since_last_thursday_win | all regular-season Thursday wins incl. Thanksgiving; **not** branded TNF |
| 14 | completed_months_since_last_thursday_win | completed calendar months, no month-end clipping |

Unchanged: date-level pregame cutoff (`gameday <` game date), missing quantity => flag 0 (quantity column stays null), units, left-censoring of 1999-2000.


## B. Wording corrections, denominator rule and outcome observation rule (from revision 3; approved as operational definitions)
## 1. Wording corrections

- **223 is the number of distinct observed flag columns** among the 373 features with at least one regular-season match (regular-season scope, 1999-2026). It is **not** the number of independent hypotheses and must not be described as such. Features with identical flags are merged because duplicates add no information; distinct flags can still be strongly dependent.
- Counts, with labels: 504 nominal; 98 structurally impossible (mathematical bounds); 33 empirical zeros (no regular-season match, not mathematically excluded; status scoped to the regular-season sample through 2026) [revision 4 correction of the 106/25 in revision 3]; 373 with at least one regular-season match; 223 equivalence classes among those 373.
- Status for the 25 is scoped: `EMPIRICAL_ZERO_UNTESTABLE_IN_REG_SAMPLE` applies to the regular-season sample 1999-2026 and is re-evaluated when seasons are added. It is never described as "impossible" or as a null result.

## 2. Tier B denominator rule (exact)

For each evaluated sample (discovery, validation, holdout, or a prospective evaluation), separately:

1. Compute team-game flags for every non-untestable feature in the regular-season games of that sample (pregame data only).
2. Form **equivalence classes**: features whose team-game flag columns are identical in that sample are one class.
3. For each class compute **n_one** = number of games in which exactly one of the two teams qualifies (the game-level unit; section 3).
4. A class is **testable** in that sample if n_one >= 30. Members of a class have identical flags, hence identical n_one (verified: 0 inconsistent classes in all four samples), so applying the threshold before or after deduplication gives the same result.
5. m = number of testable classes in that sample. BH and max-T use m; no other count.
6. Testability is **per sample**: a class may be testable in discovery and not in holdout (class membership and counts differ by sample).

Outcome-blind results (regular-season games):

| Sample | games | nonzero features | classes | classes with n_one >= 30 (m) | features with n_one >= 30 |
|---|---|---|---|---|---|
| Discovery 1999-2018 | 5,096 | 364 | 217 | **171** | 274 |
| Validation 2019-2022 | 1,055 | 333 | 188 | **142** | 234 |
| Holdout 2023-2025 | 816 | 332 | 109 | **72** | 234 |
| Prospective 2026 (136 games so far) | 136 | 278 | 88 | **14** | 50 |

Correction to revision 2: its prospective figure (28) used team-game counts; on the exactly-one-team **game** basis it is 14. Historical splits are unchanged because the two bases give the same classes there.

## 3. Tier B game-level outcome observation rule (approved as an operational definition ONLY; the test is NOT approved)

Unit: **game**, per feature.

| Game status for a feature | Treatment |
|---|---|
| Exactly one team qualifies | primary observation; outcome = that team's win value (win 1, tie 0.5, loss 0); the tie count is also kept |
| Both teams qualify | excluded from the primary comparison; counted and reported per feature; **no separate hypothesis** is registered for them |
| Neither team qualifies | not in the qualifying group |

The both-team rule is fixed now, before any Tier B outcome is seen. Large both-team counts exist (for example, 254 discovery features have at least one both-team game), so the tally is reported with every result. The Tier B baseline (expected win value for the qualifying team from the same frozen strength model, home or away role accounted for) and the Tier B null/permutation design will be specified in a separate package; **none of the Tier B test statistic is defined here**, and no Tier B test may run before that package is approved.

