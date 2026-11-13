# v1.1 Infrastructure (build only; no statistical validation)

v1.1 builds the data and governance machinery for historical discovery. **It makes no predictive or statistical claims and joins no outcomes.** Outcome-joined validation (v1.2), narrative scoring, TNF-dependent testing and First-TD integration are not part of v1.1.

## Components

| File | Purpose |
|---|---|
| `scripts/narrative_batch.py` | Batch runner: pregame feature tables as immutable Parquet partitions, plus `--verify` and `--parity` |
| `scripts/hashchain.py` | Generic append-only hash-chained CSV (manifest and hypotheses ledger) |
| `scripts/narrative_registry.py` | Deterministic feature registry, F4 specification, exposure attestation, hypotheses ledger |
| `scripts/narrative_data_audit.py` | PBP schema inspection and games-per-split reconciliation |
| `reference/feature_registry_v1.1.csv` / `.meta.json` | The registry (preregistration object) and its SHA-256. **Status: NOT_FROZEN** |
| `reference/confirmatory_specs/F4_MIRRORED_CURRENT_RECORDS.json` | Full specification of the only Tier A feature |
| `reference/exposure_attestation_v1.1.csv` | Exposure labels per feature per split |
| `research_ledger/hypotheses_ledger.csv` | Hash-chained list of registered hypotheses; failures are never deleted |
| `research_ledger/partition_manifest.csv` | Hash-chained manifest of every Parquet partition |
| `reports/v1.1/` | PBP schema report and games-per-split reconciliation |
| `derived/v1.1/` | Parquet partitions (gitignored; rebuilt deterministically and verified against the manifest) |

## Partitions (one per split)

- `team_game_features`: one row per team per completed game; pregame quantities, cipher values for city/nickname/full x historical/current, F1-F3 flags.
- `game_features`: one row per completed game; F4 mirrored-record flag (REG only) and F5 previous-meeting-tie flags (`rs`/`all`).
- `grid_flags`: the 504 Tier B exploratory flags (3 strings x 2 name bases x 6 cipher fields x 14 quantities).
- `roster_candidates_previous_week`: name-value matches against the opponent nickname using the **PREVIOUS_WEEK_ROSTER** proxy (status ACT, REG). Stores snapshot week, staleness, source file, SHA-256 and retrieval date.
- `roster_candidates_same_week_sensitivity`: separately labelled sensitivity set (`SAME_WEEK_SNAPSHOT_TIMING_UNVERIFIED`).
- `roster_coverage`: snapshot status per REG team-game, so a missing snapshot is distinguishable from "no match".

No partition contains scores, winners or any outcome column; the writer asserts this.

## Rules enforced by code and tests

- Pregame cutoff: `gameday < game date` (date level). Perturbing results on or after a date leaves earlier features byte-identical.
- Partitions are content-addressed (SHA-256 in the filename), written with exclusive-create, never overwritten. A correction creates a new version that records `supersedes_sha256`.
- Manifest and hypotheses ledger are append-only and hash-chained; edits, deletions and reordering are detected; appends to a broken chain are refused. `verify_manifest` also re-hashes every partition file.
- Registry is deterministic (no timestamps). Its hash is recorded in the manifest and ledger. It is **not frozen**; the freeze, with minimum sample, evaluation timing and stopping rule for F4, must be declared before any outcome-joined or prospective analysis.
- F4 is the only CONFIRMATORY feature. F1-F3, F5-F10 are DESCRIPTIVE_ONLY. TNF features are BLOCKED_TNF and excluded from the 504-feature multiplicity denominator.
- The roster proxy is never described as game-day active status.

## Commands

    python scripts/narrative_registry.py                 # regenerate registry files
    python scripts/narrative_registry.py --register --code-commit <sha>
    python scripts/narrative_registry.py --verify
    python scripts/narrative_batch.py --games games.csv --rosters rosters_dir --retrieved YYYY-MM-DD
    python scripts/narrative_batch.py --games games.csv --verify
    python scripts/narrative_batch.py --games games.csv --parity 200
    python scripts/narrative_data_audit.py --games games.csv --pbp-dir pbp --rosters rosters_dir --output reports/v1.1

Real-data tests: set `NFLVERSE_GAMES_CSV` (and optionally `NFLVERSE_ROSTERS_DIR`) and run `python -m unittest discover -s tests`.
