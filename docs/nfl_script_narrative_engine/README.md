# NFL Script & Narrative Engine v1.0.1

A reproducible, pregame-only research module for NFL gematria, numerology, calendar relationships, franchise records, head-to-head history, scoreline frequencies, and optional active-roster name matches. It is a research tool, **not a betting model**.

v1.0.1 is a **correctness and data-integrity patch** of v1.0 (no new research features). It fixes the defects found in the v1.0 technical audit so that historical backtesting (v1.1+) is built on reliable identities, seasons and provenance.

## What changed in v1.0.1

| Audit issue | Correction |
|---|---|
| January games used calendar year as season | Season comes from the NFL schedule row (fallback: Jan/Feb → previous season). Roster files use the NFL season. Permanent fixture: 2025 Wk 18 CAR @ TB (2026-01-03). |
| OAK/SD/STL rejected; relocated franchises lost history | `reference/team_identity_eras.csv`; era/legacy codes (OAK, SD, STL, LAR, ARZ, BLT, CLV, HST, SL, ...) map to a continuous `franchise_id`. |
| Historical names | Historical city/nickname is **primary**; current city/nickname is a separate comparison (`name_basis = current`, emitted only when it differs). Never substituted silently. |
| Month arithmetic | Exact days, **month boundaries**, and **completed months** are separate features. |
| Week-1 "mirrored 0-0-0" | Mirrored records require >= 1 game each. |
| San Francisco "49ers" | Cipher strings use the spelled-out nickname (`Forty Niners`); full identity is always `city + nickname`, so city/nickname/full are consistent. Display name keeps "49ers". |
| Thursday/TNF classification | All-Thursday, Thursday excl. Thanksgiving, Thursday evening proxy, Thanksgiving, Sunday/Monday night proxies are separate and labelled as schedule-derived. **Branded TNF counts only from the verified TNF table** (`reference/tnf_broadcast_games.csv`, currently empty). |
| Provenance | Every run records SHA-256, size, source URL, retrieval date (or "unknown"), schema hash and coverage for each input; code commit, dirty flag, script hash, Python/pandas versions; data cutoff. |
| Ledger | Append-only, hash-chained `findings_ledger.csv` with stable `game_id`, `feature_id`, `family_id`, UTC observation timestamp, split label. Tampering or row deletion is detected by `--verify-ledger`. |
| Market data separation | The schedule loader is a column whitelist; market columns are never read. |
| Ties / outcomes | `win_pct = (W + 0.5*T)/G`; predictive outcomes are `HOME_WIN`, `AWAY_WIN`, `TIE` (ties never folded into W/L). |
| Validation periods | Discovery 1999-2018, Validation 2019-2022, Holdout 2023-2025, Prospective 2026+. Each ledger row carries its `split`. |

## Run

Install dependency: pandas.

    python -m pip install pandas
    python scripts/nfl_script_narrative_engine.py --games data/games.csv --date 2026-11-12 --away WAS --home NYG --rosters data --claimed-away-tnf-record 3-9 --claimed-home-tnf-record 4-8 --ledger research_ledger/findings_ledger.csv --output output/WAS_NYG_2026-11-12

Add `--no-ledger` for a dry run. Verify a ledger: `python scripts/nfl_script_narrative_engine.py --verify-ledger research_ledger/findings_ledger.csv`.

Optional provenance arguments: `--games-source-url`, `--games-retrieved YYYY-MM-DD`, `--rosters-source-url`, `--rosters-retrieved`.

The schedule CSV must contain game_id, season, game_type, week, gameday, gametime, away_team, away_score, home_team, and home_score. Weekly roster files are named `roster_weekly_YYYY.csv` (YYYY = NFL season) and are looked up directly under `--rosters`.

## Outputs

- `frozen_context.json`: inputs, provenance, cutoff, identities, records, cipher values (historical and current), base rates, roster snapshot, governance.
- `findings.csv`: normalized findings with `feature_id`, `family_id`, `team`, `name_basis`, `match_type`, `data_quality`.
- `report.md`: readable audit.
- Ledger rows (append-only): see `LEDGER_FIELDS` in the script.

## Governance

1. The historical cutoff is exclusive of the target game date.
2. No odds, market prices, splits, or market-implied probabilities are used or loaded.
3. City, nickname, and full-team identity are separate strings and must not be substituted. Historical identity is primary; current identity is a separate comparison.
4. Digital roots are secondary matches, not full-value matches.
5. Cipher transformations are mathematically dependent; they share a `family_id` and multiple hits are not independent confirmations.
6. Both teams receive competing narrative treatment. The engine does not choose a winner based on match count.
7. Days remaining is December 31 of the target's calendar year minus the target date, excluding the target date.
8. Thursday kickoff-time proxies are not branded Thursday Night Football records. Branded TNF requires the verified table.
9. Weekly roster snapshots are not official game-day inactive lists, and their freeze time is unverified.
10. Historical rates are descriptive and in-sample, not validated predictive probabilities. Predictive claims require preregistered features and chronological holdout testing; do not tune against the holdout period.
11. The ledger is append-only. Failed hypotheses and original timestamps are preserved.

## Known limitations (unchanged by v1.0.1)

- Streaks, head-to-head and "days since" use regular-season games only (playoffs excluded).
- The pregame cutoff is date-level; earlier same-day kickoffs are excluded.
- Branded TNF data must still be sourced and verified (official NFL media guides / broadcast records).
- v1.0.1 evaluates one game per run; batch discovery is v1.1.

## Tests

    python -m unittest discover -s tests -v

Optional real-data golden test: `NFLVERSE_GAMES_CSV=/path/to/games.csv python -m unittest discover -s tests -v`.

No finding should be added to the NFL Bet Model or treated as a betting edge without independent prospective validation.
