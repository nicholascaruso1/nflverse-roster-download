# Freeze checklist and consistency review — revision 4 (2026-11-13; updated for the proposed commit)
State: registry NOT_FROZEN · PR #3 open/unmerged · main untouched · no commits · no F4/validation/holdout/prospective outcome joins · outcome firewall intact for those partitions. (Clarification 2026-11-13: the separately authorized, restricted discovery baseline fit (`reference/baseline_fit/fit_baseline_discovery.py`) did join home_score/away_score for discovery non-F4 eligible regular-season games only; coefficients are PROVISIONAL.) This document does NOT request a freeze.

## A. Checklist dispositions (items 1–24 from rev 2, updated)
| # | Item | Disposition now |
|---|---|---|
| 1 | v1.1 infrastructure accepted in principle | DONE |
| 2–5 | 14 quantities; exposure labels; full current basis; rs/all | DONE (approved) |
| 6 | Untestable features | **UPDATED: 98 STRUCTURAL / 33 EMPIRICAL_ZERO (math bounds); CSV rev4 — PENDING-REVIEW of re-audit** |
| 7 | Equivalence classes / denominators | Approved in rev 3 review (counts 171/142/72/14) |
| 8 | Tier B minimum n = 30 | Approved (provisional) |
| 9 | Tier B outcome definition | Approved (operational definition only; no test authorized) |
| 10–12 | Home value; k=8 (+4/16 sensitivities); multiplicity | DONE (approved) |
| 13 | Null hypothesis and stratified permutation | Conditionally approved; extra validation now run (corrected-module rerun: Type I 3.7–5.1% across 12 nulls × 3 thresholds, R=5,000) — PENDING-REVIEW |
| 14 | On-support rule (≥1 F4, ≥20 non-F4) | Approved (provisional); sensitivities 10/40 run — PENDING-REVIEW |
| 15 | Refit rule | Frozen coefficients for prospective; discovery refit calibrated at ~20 seasons, corrected-module rerun (3.7–4.8%) — PENDING-REVIEW, discovery stays exploratory |
| 16 | Option A | A2 chosen (188 cumulative on-support); implemented and verified |
| 17 | Additional simulations | DONE (rev 4) |
| 18 | Authorization to fit baseline coefficients on non-F4 outcomes | GRANTED (restricted) and executed; see 18a |
| 18a | Discovery baseline fit (k=8, non-F4, 1999-2018) | DONE 2026-11-13: b0=0.3509, b1=3.896 PROVISIONAL (not frozen) |
| 19 | Registry regeneration with approved statuses; SHA-256 recorded in meta and ledger | DONE in the PROPOSED diff: new registry sha 001718332501… (was b714c780…), `testability` column 98/33/373, ledger REGISTRY_REVISED events appended; manifest rows unchanged (append-only; partitions registry-independent, rebuild check in CHANGE_LOG_REV4) |
| 20 | F4 spec JSON updated | DONE in the proposed diff (A2, H0, power, permutation spec) |
| 21–22 | Frozen coefficients recorded; NOT_FROZEN to FROZEN | NOT in this commit: coefficients provisional; status stays NOT_FROZEN |
| 23 | v1.2 outcome joins | PENDING-AUTH (not authorized) |
| 24 | PR #3 merge | Not authorized |
New items: 25 stopping-rule implementation verified on synthetic + real 2026 pregame data: **DONE / PASS** (threshold not reached; 0 on-support F4; empty support hash expected). 26 higher-precision power: DONE (MDE ≈ 12 pts). 27 Tier B test specification: separate, PENDING. 28 Protocol/spec text must be updated to A2 and the rev 4 numbers before any freeze (PENDING-BUILD).

## B. Cross-document consistency findings (all RESOLVED in the revision 4 documents; see STALE_REFERENCE_AUDIT_REV4.md)
1. **Untestable counts:** rev 3 documents and the rev 2 checklist say 106/25. Superseded by 98/33; every document must carry the rev 4 numbers. Reason for change: 8 season_ties features. Nothing else moved.
2. **Option A wording:** package2_v2 §7 still describes A1/A2/A3 and recommends A1; superseded by A2 (rev 3 addendum, approved). Freeze text must use A2 only.
3. **Power/MDE:** package2_v2 says ~55–62% at 10 points and MDE ~13/12; rev 4 gives 64% at 10 points, 79% at 12, MDE ≈ 12 at ~190 on-support. Use rev 4 figures; earlier 10.2 stays withdrawn.
4. **Permutation B:** protocol specifies B=100,000; simulations used B=199 (Type I) for tractability. Permutation p-value validity does not depend on B, but the B=100,000 run itself has not been simulated end to end. Disclosed, not a discrepancy in the rule.
5. **Support threshold in rev 3 sims** was per-5-season fixed samples; rev 4 sims use the actual cumulative stopping design. Rev 4 results govern.
6. **Seasons-to-evaluation** (median ≈ 6, ≈ 2031) is approximate (weeks ÷ 18) in rev 4; rev 3's "5–6 seasons / 2030–2031" is consistent.
7. **Real data vs simulations:** real 2026 shows 33 F4 in 120 eligible games (27.5%), well above the long-run ~15% of all games; this is the known early-season effect (low games played makes mirrored records common) and is consistent with simulated F4 shares in early weeks; no outcomes involved. Zero supported strata so far is expected at n=120.
8. **Known limits to keep in the protocol text:** nulls are simulated stress scenarios, not a proof of exactness; estimand limited to on-support F4 games; M1 is under-powered for a 10-point effect (~64%).
9. **Provenance:** partition sha256 f178ca89… matches the manifest; stopping_rule sha256 0dd88805…; if f4_stopping_rule.py changes at all, the hash changes and the check must be rerun. Code now lives outside the repo (review_packages/sim); a freeze requires it to be committed with the registry (needs authorization).

## C. Open items before a freeze request can be made
(a) Commit authorization for the reviewed patch (registry regeneration included); (b) the freeze build: final coefficients + freeze metadata + FROZEN transition (separate authorization); (c) Tier B test specification, separately; (d) B = 100,000 is used only for execution checks and the future primary evaluation (see F4_PROTOCOL_REV4.md section 5 table).

## D. Deviation found and corrected during revision 4 (reported, not silent)
1. The first stopping-rule module (sha256 0dd88805…) binned d with floating-point `numpy.digitize` (left-closed); the approved text is right-closed. About 3% of equal-games-played games lie exactly on a bin edge (119/4,062 discovery; 23/837 validation; 16/632 holdout; 0/96 prospective); none is an F4 game. 
2. Corrected module: exact integer arithmetic, documented right-closed convention. Additionally, games with a team at 0 games played are now explicitly excluded from every stratum (previously the caller had to filter them; an unfiltered call would have counted week-1 games as comparators). Corrected module sha256 a487b2518c60e296… (full hash in the manifest).
3. Validation of the correction (all outcome-blind or simulated): exhaustive boundary tests over every (G ≤ 17, W, T) combination for both teams against a rational-arithmetic reference, with every edge exercised on exact equality and one step either side; old-vs-new comparison on the real partitions (binning_old_new_comparison.csv): F4 labels identical to the partition flag in all splits; games whose stratum changed: 68 discovery, 14 validation, 8 holdout, 0 prospective, none F4; on-support F4 sets and supported-strata counts IDENTICAL (discovery 728 / 18, validation 84 / 11, holdout 45 / 9, prospective 0 / 0); weekly cumulative stopping counts identical for 2026.
4. Re-run with the corrected module: full 12 × 3 Type I grid (R = 5,000), power cells (R = 4,000), 20-season discovery refit (R = 1,000 per null), real 2026 pregame check, one full-scale B = 100,000 arm. Maximum |new − old| Type I difference 1.0 point (Monte Carlo noise at SE ≈ 0.3); old results retained in results/SUPERSEDED_*.
