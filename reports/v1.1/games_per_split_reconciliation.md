# v1.1 games-per-split reconciliation (outcome-blind)

Schedule file SHA-256: `5ae004ff6d26b08109cbd7424127b0eaa89f59a4bed445229e8683e98d22c8d0`

Completed regular-season games only. Prospective = games after the 2025 season (2026 in progress).

## By split

| split       |   reg_completed |   team_game_rows |   ties |   playoff_games | seasons   |
|:------------|----------------:|-----------------:|-------:|----------------:|:----------|
| discovery   |            5096 |            10192 |      9 |             220 | 1999-2018 |
| validation  |            1055 |             2110 |      5 |              50 | 2019-2022 |
| holdout     |             816 |             1632 |      1 |              39 | 2023-2025 |
| prospective |             136 |              272 |      1 |               0 | 2026-2026 |

## Integrity checks

- identity_coverage_gaps: 0
- duplicate_game_ids: 0
- unscored_regular_season_games_before_last_completed_date: none
- team_game_rows_equal_twice_games: True

## Seasons whose completed count differs from a full schedule

|   season |   reg_completed |   expected_full_schedule |   difference |
|---------:|----------------:|-------------------------:|-------------:|
|     2022 |             271 |                      272 |           -1 |

Expected full schedule: 248 games through 2001, 256 for 2002-2020, 272 from 2021. Differences are reported, not corrected; any difference must be explained by nflverse data (e.g. a cancelled or unscored game) before the split is frozen.
