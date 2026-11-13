# Stale-reference audit — revision 4 active files

Scope: revision 4 docs, F4 spec JSON, regenerated registry CSV/meta, registry builder, stopping-rule and permutation modules, simulation README, baseline report. Patterns: 106 structural / 25 empirical; Option A1/A3; 10.2-point MDE; season-week-only permutation; PENDING_PRE_FREEZE; left-closed / float digitize of d; old power/MDE (55-62%, ~13 points); B = 299 simulations; registry hash b714c780 as current.

Result: 18 matches; **0 ACTIVE-STALE**. Every other match is an explicit supersession/correction statement.

Intentionally unchanged historical records (append-only / point-in-time, not active definitions): `research_ledger/hypotheses_ledger.csv` original REGISTERED rows and `research_ledger/partition_manifest.csv` (registry b714c780… at build time), `reports/v1.1/v1.1_build_report.md`.

## ACTIVE-STALE items
- none

## All matches
| pattern | file:line | class | text |
|---|---|---|---|
| 106 structural / 25 empirical | docs/nfl_script_narrative_engine/TIER_B_DEFINITIONS_REV4.md:5 | HISTORICAL/CORRECTION NOTE | Supersedes the untestable-feature counts in earlier packages: **98 STRUCTURAL / 33 EMPIRICAL_ZERO** (not 106/25), derived with mathematical bounds (se |
| 106 structural / 25 empirical | docs/nfl_script_narrative_engine/TIER_B_DEFINITIONS_REV4.md:32 | HISTORICAL/CORRECTION NOTE | - Counts, with labels: 504 nominal; 98 structurally impossible (mathematical bounds); 33 empirical zeros (no regular-season match, not mathematically  |
| Option A1/A3 | docs/nfl_script_narrative_engine/F4_PROTOCOL_REV4.md:3 | HISTORICAL/CORRECTION NOTE | Status: registry NOT_FROZEN; coefficients PROVISIONAL; A2 is the SOLE stopping rule (A1/A3 retired). Supersedes review package 2 v1/v2 and the revisio |
| 10.2-point MDE | docs/nfl_script_narrative_engine/F4_PROTOCOL_REV4.md:44 | HISTORICAL/CORRECTION NOTE | Type I at alpha = 0.05 under 12 null models x comparator thresholds 10/20/40: 3.7%-5.1% (primary threshold 20: 3.7%-5.1%; maximum cell 5.1%, within on |
| PENDING_PRE_FREEZE | docs/nfl_script_narrative_engine/CHANGE_LOG_REV4.md:14 | HISTORICAL/CORRECTION NOTE | - tests/test_narrative_batch.py: one assertion (stopping rule no longer PENDING_PRE_FREEZE). |
| registry hash b714c780 as current | docs/nfl_script_narrative_engine/CHANGE_LOG_REV4.md:15 | HISTORICAL/CORRECTION NOTE | - reference/feature_registry_v1.1.csv + .meta.json: REGENERATED (520 rows; new column `testability`; F4 hypothesis text corrected; registry status tex |
| 106 structural / 25 empirical | docs/nfl_script_narrative_engine/CHANGE_LOG_REV4.md:22 | HISTORICAL/CORRECTION NOTE | - Untestable 106/25 -> 98/33. Option A1/A3 retired; A2 only. Power at 10 points 55-62% -> 64%; MDE about 12 points. d-bin edge convention aligned with |
| Option A1/A3 | docs/nfl_script_narrative_engine/CHANGE_LOG_REV4.md:22 | HISTORICAL/CORRECTION NOTE | - Untestable 106/25 -> 98/33. Option A1/A3 retired; A2 only. Power at 10 points 55-62% -> 64%; MDE about 12 points. d-bin edge convention aligned with |
| old power/MDE (55-62%, ~13 points) | docs/nfl_script_narrative_engine/CHANGE_LOG_REV4.md:22 | HISTORICAL/CORRECTION NOTE | - Untestable 106/25 -> 98/33. Option A1/A3 retired; A2 only. Power at 10 points 55-62% -> 64%; MDE about 12 points. d-bin edge convention aligned with |
| registry hash b714c780 as current | docs/nfl_script_narrative_engine/FREEZE_CHECKLIST_REV4.md:21 | HISTORICAL/CORRECTION NOTE | / 19 / Registry regeneration with approved statuses; SHA-256 recorded in meta and ledger / DONE in the PROPOSED diff: new registry sha 001718332501… ( |
| 106 structural / 25 empirical | docs/nfl_script_narrative_engine/FREEZE_CHECKLIST_REV4.md:29 | HISTORICAL/CORRECTION NOTE | 1. **Untestable counts:** rev 3 documents and the rev 2 checklist say 106/25. Superseded by 98/33; every document must carry the rev 4 numbers. Reason |
| Option A1/A3 | docs/nfl_script_narrative_engine/FREEZE_CHECKLIST_REV4.md:30 | HISTORICAL/CORRECTION NOTE | 2. **Option A wording:** package2_v2 §7 still describes A1/A2/A3 and recommends A1; superseded by A2 (rev 3 addendum, approved). Freeze text must use  |
| 10.2-point MDE | docs/nfl_script_narrative_engine/FREEZE_CHECKLIST_REV4.md:31 | HISTORICAL/CORRECTION NOTE | 3. **Power/MDE:** package2_v2 says ~55–62% at 10 points and MDE ~13/12; rev 4 gives 64% at 10 points, 79% at 12, MDE ≈ 12 at ~190 on-support. Use rev  |
| old power/MDE (55-62%, ~13 points) | docs/nfl_script_narrative_engine/FREEZE_CHECKLIST_REV4.md:31 | HISTORICAL/CORRECTION NOTE | 3. **Power/MDE:** package2_v2 says ~55–62% at 10 points and MDE ~13/12; rev 4 gives 64% at 10 points, 79% at 12, MDE ≈ 12 at ~190 on-support. Use rev  |
| left-closed / float digitize of d | docs/nfl_script_narrative_engine/FREEZE_CHECKLIST_REV4.md:43 | HISTORICAL/CORRECTION NOTE | 1. The first stopping-rule module (sha256 0dd88805…) binned d with floating-point `numpy.digitize` (left-closed); the approved text is right-closed. A |
| 106 structural / 25 empirical | docs/nfl_script_narrative_engine/V1_1_REVISION4_ADDENDUM.md:7 | HISTORICAL/CORRECTION NOTE | Result: **98 STRUCTURAL / 33 EMPIRICAL_ZERO** (was 106 / 25). The 8 reclassified features are all season_ties × {city, nickname} × {historical, curren |
| left-closed / float digitize of d | docs/nfl_script_narrative_engine/V1_1_REVISION4_ADDENDUM.md:51 | HISTORICAL/CORRECTION NOTE | - d-bin convention: an earlier module used floating-point left-closed binning; the module now follows the documented right-closed convention in exact  |
| left-closed / float digitize of d | simulations/f4_revision4/README.md:9 | HISTORICAL/CORRECTION NOTE | - `results/`: committed outputs. `results/SUPERSEDED_f4_stopping_rule_v1_digitize.py` is the first (float, left-closed) module, retained only for the  |
