# v1.1 play-by-play schema inspection (outcome-blind)

Files inspected: 28 (seasons 1999-2026); total rows 1,303,450.

Required columns checked: game_id, season, week, season_type, posteam, defteam, play_id, play_type, desc, yards_gained, touchdown, td_team, td_player_id, td_player_name, total_home_score, total_away_score, game_date.

Player-outcome columns checked (needed by F8-F10 later; not joined in v1.1): complete_pass, pass_touchdown, rush_touchdown, receiver_player_id, receiver_player_name, receiving_yards, rusher_player_id, rusher_player_name.

## Seasons with missing columns

None.

## Per-season inventory (full table with SHA-256 in pbp_schema_inventory.csv)

|   season |   rows |   columns |   pbp_games |   schedule_completed_games |   in_schedule_not_pbp |   in_pbp_not_schedule |   td_player_id_null_pct |   receiver_id_null_pct |   receiver_ids_in_roster_pct |
|---------:|-------:|----------:|------------:|---------------------------:|----------------------:|----------------------:|------------------------:|-----------------------:|-----------------------------:|
|     1999 |  46136 |       372 |         258 |                        259 |                     1 |                     0 |                    0    |                   0    |                          nan |
|     2000 |  45491 |       372 |         257 |                        259 |                     2 |                     0 |                    0    |                   0    |                          nan |
|     2001 |  44969 |       372 |         259 |                        259 |                     0 |                     0 |                    0    |                   0    |                          nan |
|     2002 |  47355 |       372 |         267 |                        267 |                     0 |                     0 |                    0    |                   0    |                          100 |
|     2003 |  46811 |       372 |         267 |                        267 |                     0 |                     0 |                    0    |                   0    |                          100 |
|     2004 |  46705 |       372 |         267 |                        267 |                     0 |                     0 |                    0    |                   0    |                          100 |
|     2005 |  46823 |       372 |         267 |                        267 |                     0 |                     0 |                    0.08 |                   0    |                          100 |
|     2006 |  46299 |       372 |         267 |                        267 |                     0 |                     0 |                    0    |                   0    |                          100 |
|     2007 |  46266 |       372 |         267 |                        267 |                     0 |                     0 |                    0    |                   0    |                          100 |
|     2008 |  45917 |       372 |         267 |                        267 |                     0 |                     0 |                    0    |                   0    |                          100 |
|     2009 |  46519 |       372 |         267 |                        267 |                     0 |                     0 |                    0    |                   0    |                          100 |
|     2010 |  46892 |       372 |         267 |                        267 |                     0 |                     0 |                    0    |                   0    |                          100 |
|     2011 |  47448 |       372 |         267 |                        267 |                     0 |                     0 |                    0    |                   0    |                          100 |
|     2012 |  47834 |       372 |         267 |                        267 |                     0 |                     0 |                    0    |                   0.02 |                          100 |
|     2013 |  48158 |       372 |         267 |                        267 |                     0 |                     0 |                    0    |                   0    |                          100 |
|     2014 |  47629 |       372 |         267 |                        267 |                     0 |                     0 |                    0    |                   0    |                          100 |
|     2015 |  48122 |       372 |         267 |                        267 |                     0 |                     0 |                    0    |                   0    |                          100 |
|     2016 |  47651 |       372 |         267 |                        267 |                     0 |                     0 |                    0    |                   0    |                          100 |
|     2017 |  47245 |       372 |         267 |                        267 |                     0 |                     0 |                    0    |                   0    |                          100 |
|     2018 |  47109 |       372 |         267 |                        267 |                     0 |                     0 |                    0    |                   0    |                          100 |
|     2019 |  47260 |       372 |         267 |                        267 |                     0 |                     0 |                    0    |                   0    |                          100 |
|     2020 |  47705 |       372 |         269 |                        269 |                     0 |                     0 |                    0    |                   0    |                          100 |
|     2021 |  49922 |       372 |         285 |                        285 |                     0 |                     0 |                    0    |                   0    |                          100 |
|     2022 |  49434 |       372 |         284 |                        284 |                     0 |                     0 |                    0    |                   0    |                          100 |
|     2023 |  49665 |       372 |         285 |                        285 |                     0 |                     0 |                    0    |                   0    |                          100 |
|     2024 |  49492 |       372 |         285 |                        285 |                     0 |                     0 |                    0    |                   0    |                          100 |
|     2025 |  48771 |       372 |         285 |                        285 |                     0 |                     0 |                    0    |                   0    |                          100 |
|     2026 |  23822 |       372 |         136 |                        136 |                     0 |                     0 |                    0    |                   0    |                          100 |
