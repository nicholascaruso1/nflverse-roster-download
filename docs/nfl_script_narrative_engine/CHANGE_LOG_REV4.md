# Change log — revision 4 (2026-11-13)
Against the v1.1 infrastructure at commit 0851b41. Registry NOT_FROZEN.

## Added
- scripts/f4_stopping_rule.py: shared support / A2 stopping-rule implementation (exact integer d-bins).
- scripts/f4_permutation_test.py: full-scale (B = 100,000) stratified residual permutation, blocked and seeded.
- tests/test_f4_stopping_rule.py, tests/test_f4_permutation.py.
- reference/untestable_features_v1.1_rev4.csv: 98 STRUCTURAL / 33 EMPIRICAL_ZERO (mathematical bounds).
- reference/baseline_fit/*: provisional discovery baseline (b0 = 0.3509, b1 = 3.896), fit script, calibration, report.
- simulations/f4_revision4/*: simulation code, seeds, results, README.
- docs: F4_PROTOCOL_REV4.md, TIER_B_DEFINITIONS_REV4.md, V1_1_REVISION4_ADDENDUM.md, FREEZE_CHECKLIST_REV4.md, this log.
## Modified
- scripts/narrative_registry.py (f4_spec only) and reference/confirmatory_specs/F4_MIRRORED_CURRENT_RECORDS.json: hypothesis/H0 wording, comparison baseline (season-week-only permutation retired), minimum n and power (A2), promotion criteria (REVISED, needs review), stopping rule A2, registry_status NOT_FROZEN, provisional coefficients pointer, permutation spec.
- tests/test_narrative_batch.py: one assertion (stopping rule no longer PENDING_PRE_FREEZE).
- reference/feature_registry_v1.1.csv + .meta.json: REGENERATED (520 rows; new column `testability`; F4 hypothesis text corrected; registry status text still NOT_FROZEN). New registry sha256 0017183325012b9237b31b047b81346504dd7e24b316ca4748096c82eadd29c6; superseded sha256 b714c780891f656121a7945d8d3a14c8d5b84d9bdccaf7a0b42ca581117775aa. Grid `status` stays EXPLORATORY for all 504 grid features (ids retained, grid flag partitions unchanged); `testability` = {98 STRUCTURALLY_UNTESTABLE, 33 EMPIRICAL_ZERO_UNTESTABLE_IN_REG_SAMPLE, 373 TESTABLE_SUBJECT_TO_SAMPLE_MINIMUM, NOT_APPLICABLE for the remaining rows}. Meta records the classification file sha256, per-sample denominator rule and the A2 note.
- research_ledger/hypotheses_ledger.csv: APPEND-ONLY, 2 new REGISTRY_REVISED events (F4; Tier B grid) bound to the new registry sha and citing the superseded sha; the original 14 REGISTERED rows are untouched; chain verifies (16 rows).
- scripts/narrative_registry.py: `testability`, `untestable_classes()`, `revise_hypotheses()`, `--revise`, corrected F4 row text, updated multiplicity note.
- tests/test_registry_rev4.py (new): classification counts, F4 hypothesis, registry/meta consistency, ledger lineage.
## Unchanged
- research_ledger/partition_manifest.csv (24 rows) and all partitions: append-only record of what was built; partitions do not depend on registry content. Rebuild check under the new registry: the 12 team_game_features / game_features / grid_flags partitions are byte-identical to the committed manifest hashes; the 6 roster-derived partitions could not be compared in this environment (the historical roster directory is not available here) but the roster builders take no registry input. main and PR #3 history.
## Corrections to earlier statements
- Untestable 106/25 -> 98/33. Option A1/A3 retired; A2 only. Power at 10 points 55-62% -> 64%; MDE about 12 points. d-bin edge convention aligned with the documented right-closed rule (see checklist section D).
