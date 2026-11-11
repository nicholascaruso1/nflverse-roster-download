# NFL Model Ledger — Audit Supplement: BUF @ MIN (Week 9 MNF, Mon Nov 9 2026)

**Status: AUDIT ONLY.** The original Bet Model report, Prop Model report and Lock 2 addendum are unchanged. No architecture, weight or classification was altered. Where the audit finds a label error or a weakened evidence statement, it is logged here as a finding and not applied to the frozen cards.
Everything below is regenerated from the raw nflverse files by one script (`audit.py`, delivered with this file), so any number can be re-run.

## 0. Ledger record

```yaml
run_id: 2026-wk09-MNF-BUF@MIN
audit_supplement: v2   # v2 = script review items R1-R4 applied (section 9); no numbers changed
audit_scope: team efficiency, player volume, Cook red zone, turnovers/QB-hit, provenance, completeness
original_classifications: frozen (unchanged)
wentz_under_status_lineage: {original_pregame_card: WATCH, lock2_addendum_post_inactives_HardRock_7:31PM: LEAN, audit_supplement: no status change}
data_inputs_pregame_only: true   # PBP through Nov 8 2026; no postgame data used
files:
  play_by_play_2026.parquet:  {sha256: 422f78930248c86facb6bae5489c612700a9d351504f82a479319af5f9600795, bytes: 10050821, rows: 23647, cols: 372, weeks: 1-9, games: 135, last_game_date: 2026-11-08}
  roster_weekly_2026.csv:     {sha256: 5cb8857be2f49be417627b63faa26b33431a53ea6cc8398d087bebeab61c520f, bytes: 7281670, rows: 22285, cols: 36, weeks: 1-9}
  nfldata_games.csv:          {sha256: fc4f1a6f0c19e166ac3bf0a81ca52695113fd7975d9314b794b93552e6e53fc6, bytes: 2189036, rows: 7548}
lock2_wentz_under_audit_annotation: "Lock 2 LEAN (215.5 at -115) stands as recorded and is not rewritten. Annotation: Murray full-game average is 200.8 (over 215.5 in 2 of 5), not 170.3; Wentz 133/143 yards = one relief game (wk1) + one full game (wk2). See D2."
audit_py_sha256: 7e181aa6f8d449bd09c532ebf120ba96cea47374b5b16ee6db0941506935102f
retrieved: 2026-11-09T19:30:41-05:00
github_actions_artifacts: INACCESSIBLE in the Claude session (see section 5)
independent_reproduction: {R6: closed, reviewer_run_of_v2.1_matches_author_run_except_dtype_label_line}
open_items: []
post_closure_notes: ["2026-11-10 D1 spike-filter sensitivity: Murray 154 -> 155 if spike counted, Wentz unchanged at 40, no other figure affected (section 10)"]
audit_status: CLOSED 2026-11-09 (R1-R8 resolved; R5 artifact check performed by reviewer)
artifact_checksums_verified_by_reviewer: {play_by_play_2026.parquet: match, roster_weekly_2026.csv: match}
reconciliation_result: efficiency PASS (14/14 figures); Cook red zone PASS (28/10); turnovers PASS (counts); QB-hit PASS (rates); player hit counts PASS; 6 labeling/evidence findings (D1-D6)
```

## Discrepancy log (read this first)

| ID | Where in the original reports | Finding | Severity | Effect on frozen classification |
|---|---|---|---|---|
| **D1** | Prop report (Wentz "23 attempts each") and Bet report ("Murray 169 attempts at -0.121 EPA per attempt; Wentz 46 attempts") | In this file `pass_attempt==1` is set on every sack row (635 of 635), so my "attempts" were **dropbacks**. Box-score attempts excluding sacks: Wentz 40 (20 + 20), Murray 154. EPA figures are EPA per **dropback**. Yardage totals are unaffected (Wentz 276, Murray 1,022). One unexplained gap: NFL.com's 23-of-39 for Wentz implies 39 attempts vs 40 here. No reported calculation used attempts as a denominator: the EPA means are taken over `pass==1` rows (dropbacks). | Medium (label error) | None applied. |
| **D2** | Prop report ("Murray averaged 170.3 yards per game"; "neither MIN QB averaged near 210") and Lock 2 addendum | The 170.3 includes Murray's week-1 appearance of **5 dropbacks, 18 yards** (Wentz relieved him). Across his five full-game outings (wks 3, 4, 5, 7, 8) he threw for 168, 247, 229, 150, 210 = **200.8 per game**, and was over 215.5 in **2 of 5**. Wentz: week 1 was 23 dropbacks in relief (133 yds), week 2 a full game (143 yds). | **Medium** (weakens an evidence sentence behind Wentz Under; status lineage: original pregame card = **WATCH**, Lock 2 addendum on post-inactives Hard Rock prices = **LEAN**, both frozen) | None applied. Recorded for the ledger. Wentz still went under 150 in both games, but that is a 2-game sample, one of them in relief. |
| **D3** | Prop report (Jefferson "5.9 targets per game") | 5.9 = 41 targets / 7 team games. Jefferson was inactive in week 4 (roster status `INA`), so per-game targets over his 6 games = 6.83. Yardage hit counts used 6 games and are correct (over 79.5 in 1 of 6; including the zero game would be 1 of 7). The 22% share is unaffected. | Low | None. |
| **D4** | Prop report (Cook "28 red-zone carries, 10 inside the 5") | Reproduced exactly with `yardline_100 <= 20` and `<= 5`. The "inside the 5" label should read "at or inside the 5" (strictly `< 5` = 6). One of the 28 is from exactly the 20 (strictly inside 20 = 27). | Low (label) | None. |
| **D5** | Bet report ("MIN takeaways 12, margin +7") | One of the 12 is a kickoff-return fumble (NO game, play 1938), a special-teams event. Scrimmage-only (pass/run) takeaways = 11, margin +6. BUF's counts are all pass/run. Two events (BUF-LAC play 3173; MIA-MIN play 1684) are reversed-on-challenge sacks with a fumble recovery recorded. | Low | None. |
| **D6** | Bet report / Lock 2 addendum (schedule line -3.5, total 45.5) | The 2026 schedule row came from nfldata `games.csv`, **not** from the schedule artifact (which exports 2002-2025 only) and not from the release the workflow downloads. The file changed after my retrieval (week-10 lines only; the BUF@MIN row is identical at the 8:01 PM ET recheck). | Low | None. |

No finding changes a recomputed figure in the efficiency, red-zone or QB-hit tables.

## Claim-by-claim reconciliation of the player figures

| Original claim | Recomputed | Status |
|---|---|---|
| Cook carries 13, 21, 24, 12, 25, 22, 21 (avg 19.7); 19+ in 5 of 7 | identical (section 2) | reproduced |
| Cook about 73% of BUF designed rushes | 138 / 188 = 0.734 | reproduced |
| Cook rush yards over 84.5 / 86.5 in 4 of 7 | 4 / 4 | reproduced |
| Cook 28 red-zone carries, 10 inside the 5 | 28 / 10 (6 strictly inside 5) | reproduced (D4) |
| Wentz 133 and 143 yards; under 150 both games | identical | reproduced (attempts mislabeled, D1) |
| Murray 1,022 yards, 170.3 per game | 1,022 / 6 = 170.3 | arithmetic reproduced (D2) |
| Jefferson yards 92, 55, 32, 79, 44, 33; 1 of 6 over 79.5; mean 55.8 | identical; week 4 inactive | reproduced (D3) |
| Hockenson at or under 4 receptions in 6 of 7; over 41.5 in 2 of 7 | identical | reproduced |
| Kincaid over 36.5 in 5 of 7; over 39.5 in 3 of 7 | identical | reproduced |
| Games excluded from any sample | Jefferson wk 4 (inactive per roster). BUF bye wk 7; MIN bye wk 6 (no game). Wentz zero-dropback weeks 3-8 are shown, not excluded. | documented |

Prop hit counts above treat all games with at least one target (or carry) as the sample, except where stated.


## 1. Team efficiency reconciliation

**Filters (exact).** `season==2026`; `play_type in {pass, run}`; `epa` not null; `posteam` not null. Offense rows = filter + `posteam==TEAM`. Defense rows = filter + `defteam==TEAM`. Pass rows = `pass==1` (nflverse sets this on dropbacks: it includes sacks and QB scrambles). Rush rows = `rush==1` (designed runs only; scrambles are NOT in rush). Success rate = mean of `success`. All EPA/SR figures are plain per-play means over those rows, so the aggregate is a play-weighted mean of the per-game values. No opponent adjustment, no garbage-time or win-probability filter, no special-teams plays.

Scramble row classification check (all 2026 plays with `qb_scramble==1`):

| play_type   |   pass |   rush |   n |
|:------------|-------:|-------:|----:|
| no_play     |      1 |      0 |  36 |
| run         |      1 |      0 | 488 |


### BUF: seven games

|   wk | game_id         | opp   |   off_n |   off_epa |   off_sr |   off_pass_n |   off_pass_epa |   off_rush_n |   off_rush_epa |   def_n |   def_epa |   def_sr |   def_pass_epa |   def_rush_epa |
|-----:|:----------------|:------|--------:|----------:|---------:|-------------:|---------------:|-------------:|---------------:|--------:|----------:|---------:|---------------:|---------------:|
|    1 | 2026_01_BUF_HOU | HOU   |      52 |     0.229 |    0.404 |           33 |          0.513 |           19 |         -0.263 |      73 |     0.069 |    0.466 |          0.097 |          0.030 |
|    2 | 2026_02_DET_BUF | DET   |      66 |     0.435 |    0.576 |           38 |          0.548 |           28 |          0.281 |      62 |     0.232 |    0.484 |          0.414 |         -0.211 |
|    3 | 2026_03_LAC_BUF | LAC   |      62 |    -0.021 |    0.500 |           31 |         -0.112 |           31 |          0.070 |      64 |    -0.071 |    0.469 |         -0.167 |          0.068 |
|    4 | 2026_04_NE_BUF  | NE    |      55 |     0.099 |    0.400 |           36 |          0.074 |           19 |          0.147 |      72 |     0.191 |    0.514 |          0.370 |         -0.075 |
|    5 | 2026_05_BUF_LA  | LA    |      58 |     0.291 |    0.552 |           29 |          0.692 |           29 |         -0.110 |      79 |     0.231 |    0.481 |          0.330 |         -0.012 |
|    6 | 2026_06_BUF_LV  | LV    |      61 |     0.171 |    0.475 |           36 |          0.282 |           25 |          0.011 |      61 |     0.095 |    0.426 |          0.280 |         -0.285 |
|    8 | 2026_08_BAL_BUF | BAL   |      75 |     0.027 |    0.493 |           38 |          0.077 |           37 |         -0.024 |      48 |    -0.497 |    0.333 |         -0.659 |         -0.201 |

BUF pooled aggregate: off plays 429, def plays 459; unweighted mean of the seven per-game off EPA values = 0.176 (NOT what the report used). Play-weighted per-game mean = pooled value (max abs diff below).

BUF row accounting (all rows in the 7 games): {'total_rows': 1268, 'play_type_not_pass_run': 380, 'pass_run_epa_null': 0, 'pass_run_posteam_null': 0, 'kept_both_sides': 888, 'play_type_counts': {'pass': 507, 'run': 381, 'no_play': 134, 'kickoff': 86, 'extra_point': 43, 'punt': 39, nan: 36, 'field_goal': 29, 'qb_kneel': 13}}


#### BUF other efficiency-adjacent figures in the report (same filters)

20+ yd pass rate = share of `pass==1` offense rows with `yards_gained>=20`: 32/241 = 0.133. Plays per game = off rows / 7 = 429/7 = 61.3. Sack rate taken = mean(`sack`) over pass rows = 13/241 = 0.054. Def sack rate = 15/295 = 0.051.


### MIN: seven games

|   wk | game_id         | opp   |   off_n |   off_epa |   off_sr |   off_pass_n |   off_pass_epa |   off_rush_n |   off_rush_epa |   def_n |   def_epa |   def_sr |   def_pass_epa |   def_rush_epa |
|-----:|:----------------|:------|--------:|----------:|---------:|-------------:|---------------:|-------------:|---------------:|--------:|----------:|---------:|---------------:|---------------:|
|    1 | 2026_01_GB_MIN  | GB    |      59 |    -0.020 |    0.356 |           31 |          0.075 |           28 |         -0.125 |      67 |    -0.175 |    0.388 |         -0.059 |         -0.429 |
|    2 | 2026_02_MIN_CHI | CHI   |      51 |    -0.078 |    0.333 |           24 |          0.005 |           27 |         -0.151 |      69 |    -0.125 |    0.319 |         -0.026 |         -0.271 |
|    3 | 2026_03_MIN_TB  | TB    |      55 |    -0.264 |    0.236 |           34 |         -0.304 |           21 |         -0.199 |      64 |    -0.246 |    0.266 |         -0.231 |         -0.284 |
|    4 | 2026_04_MIA_MIN | MIA   |      69 |    -0.047 |    0.391 |           43 |         -0.018 |           26 |         -0.094 |      37 |    -0.204 |    0.351 |         -0.530 |          0.180 |
|    5 | 2026_05_MIN_NO  | NO    |      64 |    -0.104 |    0.453 |           38 |          0.075 |           26 |         -0.367 |      43 |    -0.351 |    0.349 |         -0.459 |         -0.185 |
|    7 | 2026_07_IND_MIN | IND   |      54 |    -0.081 |    0.370 |           29 |          0.087 |           25 |         -0.275 |      59 |    -0.112 |    0.441 |         -0.278 |          0.028 |
|    8 | 2026_08_MIN_DET | DET   |      50 |    -0.092 |    0.460 |           34 |         -0.012 |           16 |         -0.262 |      67 |    -0.047 |    0.478 |         -0.144 |          0.028 |

MIN pooled aggregate: off plays 402, def plays 406; unweighted mean of the seven per-game off EPA values = -0.098 (NOT what the report used). Play-weighted per-game mean = pooled value (max abs diff below).

MIN row accounting (all rows in the 7 games): {'total_rows': 1159, 'play_type_not_pass_run': 351, 'pass_run_epa_null': 0, 'pass_run_posteam_null': 0, 'kept_both_sides': 808, 'play_type_counts': {'pass': 442, 'run': 366, 'no_play': 120, 'punt': 66, 'kickoff': 61, nan: 35, 'field_goal': 35, 'extra_point': 18, 'qb_kneel': 14, 'qb_spike': 2}}


#### MIN other efficiency-adjacent figures in the report (same filters)

20+ yd pass rate = share of `pass==1` offense rows with `yards_gained>=20`: 20/233 = 0.086. Plays per game = off rows / 7 = 402/7 = 57.4. Sack rate taken = mean(`sack`) over pass rows = 21/233 = 0.090. Def sack rate = 25/235 = 0.106.


### Reconciliation: original report vs recomputed

| team   | metric   |   original_report |   recomputed_pooled | match   |   weighted_per_game |
|:-------|:---------|------------------:|--------------------:|:--------|--------------------:|
| BUF    | off_epa  |             0.173 |               0.173 | yes     |               0.173 |
| BUF    | off_sr   |             0.490 |               0.490 | yes     |               0.490 |
| BUF    | off_pass |             0.291 |               0.291 | yes     |               0.291 |
| BUF    | off_rush |             0.022 |               0.022 | yes     |               0.022 |
| BUF    | def_epa  |             0.063 |               0.063 | yes     |               0.063 |
| BUF    | def_pass |             0.140 |               0.140 | yes     |             nan     |
| BUF    | def_rush |            -0.077 |              -0.077 | yes     |             nan     |
| MIN    | off_epa  |            -0.096 |              -0.096 | yes     |              -0.096 |
| MIN    | off_sr   |             0.373 |               0.373 | yes     |               0.373 |
| MIN    | off_pass |            -0.016 |              -0.016 | yes     |              -0.016 |
| MIN    | off_rush |            -0.206 |              -0.206 | yes     |              -0.206 |
| MIN    | def_epa  |            -0.169 |              -0.169 | yes     |              -0.169 |
| MIN    | def_pass |            -0.207 |              -0.207 | yes     |             nan     |
| MIN    | def_rush |            -0.116 |              -0.116 | yes     |             nan     |

League reference: off EPA -0.001, SR 0.434 over 16617 rows (both sides, all teams).


## 2. Player volume reconciliation (WATCH props, plus Kincaid who was WATCH in the original card)

**Filters.** Team games = every game the team played in the 2026 PBP file (BUF 7: wks 1-6, 8; MIN 7: wks 1-5, 7, 8). Receiving: rows with `receiver_player_id` = player id and `play_type=='pass'` (target); reception = `complete_pass==1`; receiving yards = sum `receiving_yards`. Rushing: `rush==1` and `rusher_player_id` = player id (designed runs, scrambles excluded); yards = sum `rushing_yards`. Passing: `passer_player_id` = player id; **box-score attempt = `pass_attempt==1 & sack!=1`** (in this file `pass_attempt==1` is also set on sack rows, so the raw flag equals dropbacks); dropbacks = `pass==1` rows with that passer (includes sacks and scrambles). Zero-volume games are shown as zero if the player has any row for the team that season; whether a zero is a scratch or a non-involvement cannot be determined from PBP (no 2026 participation file).


### James Cook (BUF)

gsis ids matched for `J.Cook` as BUF rusher: ['00-0037248']

|   wk | game_id         |   car |   rush_yds |   tgt |   rec |   rec_yds |
|-----:|:----------------|------:|-----------:|------:|------:|----------:|
|    1 | 2026_01_BUF_HOU |    13 |       57.0 |     4 |     3 |      12.0 |
|    2 | 2026_02_DET_BUF |    21 |      135.0 |     3 |     1 |       4.0 |
|    3 | 2026_03_LAC_BUF |    24 |      154.0 |     1 |     0 |       0.0 |
|    4 | 2026_04_NE_BUF  |    12 |       75.0 |     2 |     2 |       8.0 |
|    5 | 2026_05_BUF_LA  |    25 |      111.0 |     1 |     1 |       7.0 |
|    6 | 2026_06_BUF_LV  |    22 |       95.0 |     3 |     3 |      58.0 |
|    8 | 2026_08_BAL_BUF |    21 |       80.0 |     3 |     2 |      21.0 |

Carries: sum 138, mean over 7 games = 19.71; games with 19+ carries (threshold for O18.5) = 5 of 7. Rush yds: mean 101.0; games over 84.5 = 4, over 86.5 = 4 of 7.

Share denominator used in the report: BUF `rush==1`, `play_type=='run'`, rusher id/name not null = 188 rows; Cook 138 = 0.734.


### Carson Wentz and Kyler Murray (MIN) — passing

**C.Wentz** ids: ['00-0032950']

|   wk | game_id         |   dropbacks |   pass_attempt_flag |   att_excl_sacks |   cmp |   pass_yds |   sacks |   scrambles |   ints |
|-----:|:----------------|------------:|--------------------:|-----------------:|------:|-----------:|--------:|------------:|-------:|
|    1 | 2026_01_GB_MIN  |          23 |                  23 |               20 |    12 |      133.0 |       3 |           0 |      0 |
|    2 | 2026_02_MIN_CHI |          23 |                  23 |               20 |    11 |      143.0 |       3 |           0 |      0 |
|    3 | 2026_03_MIN_TB  |           0 |                   0 |                0 |     0 |        0.0 |       0 |           0 |      0 |
|    4 | 2026_04_MIA_MIN |           0 |                   0 |                0 |     0 |        0.0 |       0 |           0 |      0 |
|    5 | 2026_05_MIN_NO  |           0 |                   0 |                0 |     0 |        0.0 |       0 |           0 |      0 |
|    7 | 2026_07_IND_MIN |           0 |                   0 |                0 |     0 |        0.0 |       0 |           0 |      0 |
|    8 | 2026_08_MIN_DET |           0 |                   0 |                0 |     0 |        0.0 |       0 |           0 |      0 |

C.Wentz: games with dropbacks = 2 (weeks [1, 2]); dropbacks 46, `pass_attempt==1` rows 46, attempts excluding sacks 40, completions 23, yards 276, sacks 6, scrambles 0. Yards per game over games with dropbacks = 138.0; dropbacks per game = 23.0; attempts excluding sacks per game = 20.0. **In this file `pass_attempt==1` is set on every sack row, so it equals dropbacks.** The original reports' 'attempts' (Wentz 23 per game, Murray 28.2 per game) are therefore DROPBACKS, not box-score attempts.

**K.Murray** ids: ['00-0035228']

|   wk | game_id         |   dropbacks |   pass_attempt_flag |   att_excl_sacks |   cmp |   pass_yds |   sacks |   scrambles |   ints |
|-----:|:----------------|------------:|--------------------:|-----------------:|------:|-----------:|--------:|------------:|-------:|
|    1 | 2026_01_GB_MIN  |           5 |                   5 |                5 |     3 |       18.0 |       0 |           0 |      1 |
|    2 | 2026_02_MIN_CHI |           0 |                   0 |                0 |     0 |        0.0 |       0 |           0 |      0 |
|    3 | 2026_03_MIN_TB  |          32 |                  32 |               29 |    15 |      168.0 |       3 |           0 |      1 |
|    4 | 2026_04_MIA_MIN |          41 |                  41 |               37 |    27 |      247.0 |       4 |           0 |      0 |
|    5 | 2026_05_MIN_NO  |          31 |                  31 |               29 |    24 |      229.0 |       2 |           0 |      0 |
|    7 | 2026_07_IND_MIN |          27 |                  27 |               24 |    14 |      150.0 |       3 |           0 |      0 |
|    8 | 2026_08_MIN_DET |          33 |                  33 |               30 |    17 |      210.0 |       3 |           0 |      1 |

K.Murray: games with dropbacks = 6 (weeks [1, 3, 4, 5, 7, 8]); dropbacks 169, `pass_attempt==1` rows 169, attempts excluding sacks 154, completions 100, yards 1022, sacks 15, scrambles 0. Yards per game over games with dropbacks = 170.3; dropbacks per game = 28.2; attempts excluding sacks per game = 25.7. **In this file `pass_attempt==1` is set on every sack row, so it equals dropbacks.** The original reports' 'attempts' (Wentz 23 per game, Murray 28.2 per game) are therefore DROPBACKS, not box-score attempts.


### J.Jefferson (MIN)

receiver ids: ['00-0036322']

|   wk | game_id         |   tgt |   rec |   rec_yds |
|-----:|:----------------|------:|------:|----------:|
|    1 | 2026_01_GB_MIN  |    10 |     8 |      92.0 |
|    2 | 2026_02_MIN_CHI |     6 |     3 |      55.0 |
|    3 | 2026_03_MIN_TB  |     2 |     2 |      32.0 |
|    4 | 2026_04_MIA_MIN |     0 |     0 |       0.0 |
|    5 | 2026_05_MIN_NO  |     7 |     6 |      79.0 |
|    7 | 2026_07_IND_MIN |     7 |     4 |      44.0 |
|    8 | 2026_08_MIN_DET |     9 |     5 |      33.0 |

Games with at least one target: 6 of 7 team games. Zero-target team games: [4]. Targets/game = 41/6 = 6.83 (report's tgt_pg used all 7 team games as denominator = 5.86). Rec yds mean over games with targets = 55.8; over all team games (zeros included) = 47.9.

Over 79.5: 1 of 6 (with-target games) / of 7 (all team games); over 80.5: 1. Receptions >=7 (over 6.5): 1 of 6.

Roster status for the zero-target week(s):

|   week | full_name        | position   | status   | status_description_abbr   |
|-------:|:-----------------|:-----------|:---------|:--------------------------|
|      1 | Jermar Jefferson | RB         | CUT      | W03                       |
|      1 | Justin Jefferson | WR         | ACT      | A01                       |
|      2 | Justin Jefferson | WR         | ACT      | A01                       |
|      4 | Justin Jefferson | WR         | INA      | A01                       |


### T.Hockenson (MIN)

receiver ids: ['00-0035229']

|   wk | game_id         |   tgt |   rec |   rec_yds |
|-----:|:----------------|------:|------:|----------:|
|    1 | 2026_01_GB_MIN  |     5 |     4 |      36.0 |
|    2 | 2026_02_MIN_CHI |     4 |     3 |      29.0 |
|    3 | 2026_03_MIN_TB  |     4 |     2 |      11.0 |
|    4 | 2026_04_MIA_MIN |    13 |    13 |     119.0 |
|    5 | 2026_05_MIN_NO  |     1 |     1 |       7.0 |
|    7 | 2026_07_IND_MIN |     5 |     4 |      35.0 |
|    8 | 2026_08_MIN_DET |     5 |     4 |      58.0 |

Games with at least one target: 7 of 7 team games. Zero-target team games: []. Targets/game = 37/7 = 5.29 (report's tgt_pg used all 7 team games as denominator = 5.29). Rec yds mean over games with targets = 42.1; over all team games (zeros included) = 42.1.

Receptions <=4 (Under 4.5): 6 of 7; receptions >=5: 1.


### D.Kincaid (BUF)

receiver ids: ['00-0038933']

|   wk | game_id         |   tgt |   rec |   rec_yds |
|-----:|:----------------|------:|------:|----------:|
|    1 | 2026_01_BUF_HOU |     6 |     5 |     130.0 |
|    2 | 2026_02_DET_BUF |     8 |     7 |      95.0 |
|    3 | 2026_03_LAC_BUF |     3 |     2 |      38.0 |
|    4 | 2026_04_NE_BUF  |     2 |     1 |       7.0 |
|    5 | 2026_05_BUF_LA  |     3 |     1 |       7.0 |
|    6 | 2026_06_BUF_LV  |     8 |     7 |      38.0 |
|    8 | 2026_08_BAL_BUF |     6 |     4 |      86.0 |

Games with at least one target: 7 of 7 team games. Zero-target team games: []. Targets/game = 36/7 = 5.14 (report's tgt_pg used all 7 team games as denominator = 5.14). Rec yds mean over games with targets = 57.3; over all team games (zeros included) = 57.3.

Over 36.5: 5 of 7; over 39.5: 3.


## 3. James Cook red-zone audit

**Definition used in the original report:** `yardline_100 <= 20` (red zone) and `yardline_100 <= 5` (labeled 'inside the 5'; this actually includes carries from exactly the 5-yard line). Filter: `posteam=='BUF'`, `rush==1`, `rusher_player_id` = Cook's id ['00-0037248'] (player-specific). Recomputed: red-zone carries = 28, at-or-inside-5 = 10. Strictly inside the 5 (`yardline_100 < 5`) = 6; strictly inside the 20 (`<20`) = 27; goal-to-go carries = 14.

Team-level comparison (raw `rush==1` flag count, no play_type or rusher-id restriction; may include penalty-nullified `no_play` rows with null rusher id): red-zone rush rows = 46, at-or-inside-5 = 21. Cook's 28/10 are therefore a subset of team totals, i.e. player-specific, not team-level. Breakdown of team red-zone rushes by rusher: {'J.Cook': 28, 'J.Allen': 13, 'T.Johnson': 3, nan: 1, 'D.Moore': 1}.


### Data-hygiene checks

- Duplicate `(game_id, play_id)` rows: whole 2026 file = 0; BUF games = 0.
- BUF `rush==1` rows with null `rusher_player_id` = 7 of 195; null `rusher_player_name` = 7.
- `qb_kneel==1` among BUF rush==1 rows = 0; kneels by anyone, BUF offense = 10; Cook rows with `qb_kneel==1` = 0. (Kneel-downs carry the QB's rusher id and `rush==1` is 0 on them in nflverse; they are therefore not in these counts.)
- Cook rows with `rush==1` and `play_type=='no_play'` (penalty-nullified) = 0; `rush==1` and `play_type=='run'` = 138. Original carry totals used `rush==1` without a play_type filter; the two agree if the no_play count is 0.
- Cook rush rows total (all field positions) = 138; with `fumble_lost==1` = 2.

- Verified flag semantics (whole 2026 file): `qb_kneel==1` rows = 201, all with `rush==0`, `play_type=='qb_kneel'`, and non-null rusher id (201); so kneels never enter `rush==1` counts. `sack==1` rows = 635, all with `pass==1` and `pass_attempt==1` (pass_attempt includes sacks). BUF `rush==1` rows with null `rusher_player_id` = 7; all have play_type {'no_play': 7} (penalty-nullified plays) and null `rusher_player_name`; they are excluded from every player count and from the 188-row share denominator by the `play_type=='run'` / non-null id filters, which is the intended treatment. The `rusher` text field names: {'J.Cook': 5, 'J.Allen': 1, 'R.Davis': 1}.


### Underlying play records: Cook red-zone carries (28 rows)

| game_id         |   play_id | rusher_player_id   |   qtr |   down |   ydstogo |   yardline_100 |   goal_to_go |   rushing_yards |   rush_touchdown |   qb_kneel | play_type   | at_or_inside_5   |
|:----------------|----------:|:-------------------|------:|-------:|----------:|---------------:|-------------:|----------------:|-----------------:|-----------:|:------------|:-----------------|
| 2026_01_BUF_HOU |      2832 | 00-0037248         |     3 |      1 |        10 |             16 |            0 |               3 |                0 |          0 | run         |                  |
| 2026_01_BUF_HOU |      3413 | 00-0037248         |     4 |      1 |        10 |             20 |            0 |               3 |                0 |          0 | run         |                  |
| 2026_02_DET_BUF |      1117 | 00-0037248         |     2 |      1 |         2 |              2 |            1 |               1 |                0 |          0 | run         | Y                |
| 2026_02_DET_BUF |      1653 | 00-0037248         |     2 |      1 |        10 |             13 |            0 |               7 |                0 |          0 | run         |                  |
| 2026_02_DET_BUF |      3102 | 00-0037248         |     3 |      1 |         6 |              6 |            1 |               2 |                0 |          0 | run         |                  |
| 2026_02_DET_BUF |      4101 | 00-0037248         |     4 |      1 |         1 |              1 |            1 |               1 |                1 |          0 | run         | Y                |
| 2026_03_LAC_BUF |      3707 | 00-0037248         |     4 |      1 |        10 |             16 |            0 |              11 |                0 |          0 | run         |                  |
| 2026_03_LAC_BUF |      3729 | 00-0037248         |     4 |      1 |         5 |              5 |            1 |               4 |                0 |          0 | run         | Y                |
| 2026_03_LAC_BUF |      4151 | 00-0037248         |     4 |      1 |         3 |              3 |            1 |               3 |                1 |          0 | run         | Y                |
| 2026_04_NE_BUF  |       855 | 00-0037248         |     1 |      1 |        10 |             19 |            0 |              -1 |                0 |          0 | run         |                  |
| 2026_04_NE_BUF  |       967 | 00-0037248         |     2 |      1 |         8 |              8 |            1 |               8 |                1 |          0 | run         |                  |
| 2026_04_NE_BUF  |      1766 | 00-0037248         |     2 |      1 |         6 |              6 |            1 |               0 |                0 |          0 | run         |                  |
| 2026_04_NE_BUF  |      1926 | 00-0037248         |     2 |      1 |         5 |              6 |            0 |               4 |                0 |          0 | run         |                  |
| 2026_05_BUF_LA  |       745 | 00-0037248         |     1 |      1 |        10 |             12 |            0 |               1 |                0 |          0 | run         |                  |
| 2026_05_BUF_LA  |      1453 | 00-0037248         |     2 |      1 |        10 |             17 |            0 |              17 |                1 |          0 | run         |                  |
| 2026_05_BUF_LA  |      3017 | 00-0037248         |     3 |      1 |         2 |              2 |            1 |              -5 |                0 |          0 | run         | Y                |
| 2026_05_BUF_LA  |      4094 | 00-0037248         |     4 |      1 |         5 |              5 |            1 |               0 |                0 |          0 | run         | Y                |
| 2026_05_BUF_LA  |      4123 | 00-0037248         |     4 |      2 |         5 |              5 |            1 |               5 |                1 |          0 | run         | Y                |
| 2026_06_BUF_LV  |       691 | 00-0037248         |     1 |      1 |        10 |             19 |            0 |               2 |                0 |          0 | run         |                  |
| 2026_06_BUF_LV  |      1255 | 00-0037248         |     2 |      1 |        10 |             13 |            0 |               4 |                0 |          0 | run         |                  |
| 2026_06_BUF_LV  |      2638 | 00-0037248         |     3 |      1 |        10 |             14 |            0 |               2 |                0 |          0 | run         |                  |
| 2026_06_BUF_LV  |      3854 | 00-0037248         |     4 |      1 |         3 |              3 |            1 |               3 |                1 |          0 | run         | Y                |
| 2026_08_BAL_BUF |      1374 | 00-0037248         |     2 |      2 |         5 |             15 |            0 |               2 |                0 |          0 | run         |                  |
| 2026_08_BAL_BUF |      1396 | 00-0037248         |     2 |      3 |         3 |             13 |            0 |               2 |                0 |          0 | run         |                  |
| 2026_08_BAL_BUF |      1425 | 00-0037248         |     2 |      4 |         1 |             11 |            0 |               1 |                0 |          0 | run         |                  |
| 2026_08_BAL_BUF |      1449 | 00-0037248         |     2 |      1 |        10 |             10 |            1 |               3 |                0 |          0 | run         |                  |
| 2026_08_BAL_BUF |      1538 | 00-0037248         |     2 |      2 |         3 |              3 |            1 |               2 |                0 |          0 | run         | Y                |
| 2026_08_BAL_BUF |      3064 | 00-0037248         |     3 |      2 |         5 |              5 |            1 |               5 |                1 |          0 | run         | Y                |

Per-game red-zone carries: {'2026_01_BUF_HOU': 2, '2026_02_DET_BUF': 4, '2026_03_LAC_BUF': 3, '2026_04_NE_BUF': 4, '2026_05_BUF_LA': 5, '2026_06_BUF_LV': 4, '2026_08_BAL_BUF': 6}. Red-zone rush yards 90, rush TDs 7; at-or-inside-5 yards 19, TDs 5.


## 4. Turnover and QB-hit reconciliation

**Definition used in the original report.** Giveaway = a row with `posteam==TEAM` and (`interception==1` or `fumble_lost==1`). Takeaway = a row with `defteam==TEAM` and the same flags. NO play_type filter was applied (so special-teams and any other row types are included), and each play is counted once even if it has both flags. Listed below event by event.


### BUF turnover events

Giveaways 11, takeaways 9, margin -2. Of these, rows with play_type not in {pass, run}: 0; rows with both flags: 0. Interceptions thrown by BUF: 5; fumbles lost by BUF: 6.

| side     | game_id         |   play_id |   qtr | posteam   | defteam   | play_type   |   interception |   fumble_lost | desc                                                                                                           |
|:---------|:----------------|----------:|------:|:----------|:----------|:------------|---------------:|--------------:|:---------------------------------------------------------------------------------------------------------------|
| GIVEAWAY | 2026_03_LAC_BUF |        63 |     1 | BUF       | LAC       | run         |              0 |             1 | (14:53) 4-J.Cook up the middle to BUF 47 for 4 yards (92-J.Eboigbe). FUMBLES (92-J.Eboigbe), RECOVERED by LAC- |
| GIVEAWAY | 2026_03_LAC_BUF |       793 |     1 | BUF       | LAC       | pass        |              1 |             0 | (3:31) (Shotgun) 17-J.Allen pass short middle intended for 2-D.Moore INTERCEPTED by 22-G.Smith at BUF 44. 22-G |
| GIVEAWAY | 2026_03_LAC_BUF |      1029 |     2 | BUF       | LAC       | pass        |              1 |             0 | (15:00) 17-J.Allen pass deep left intended for 2-D.Moore INTERCEPTED by 22-G.Smith at LAC 10. 22-G.Smith to LA |
| GIVEAWAY | 2026_03_LAC_BUF |      2861 |     3 | BUF       | LAC       | pass        |              0 |             1 | (4:00) (Shotgun) 17-J.Allen pass short middle to 86-D.Kincaid to LAC 24 for 24 yards (4-T.Still; 22-G.Smith).  |
| GIVEAWAY | 2026_03_LAC_BUF |      3173 |     4 | BUF       | LAC       | pass        |              0 |             1 | (15:00) (Shotgun) 17-J.Allen sacked at BUF 28 for -6 yards (52-K.Mack). Los Angeles Chargers challenged the pa |
| GIVEAWAY | 2026_04_NE_BUF  |      2179 |     2 | BUF       | NE        | pass        |              0 |             1 | (:23) (Shotgun) 17-J.Allen pass short middle to 10-K.Shakir to NE 39 for 8 yards (14-R.Spillane). FUMBLES (14- |
| GIVEAWAY | 2026_04_NE_BUF  |      4424 |     4 | BUF       | NE        | pass        |              1 |             0 | (1:14) (Shotgun) 17-J.Allen pass deep left intended for 5-J.Palmer INTERCEPTED by 4-C.Woodson at NE 19. 4-C.Wo |
| GIVEAWAY | 2026_05_BUF_LA  |      1955 |     2 | BUF       | LA        | pass        |              1 |             0 | (:37) (Shotgun) 17-J.Allen pass deep right intended for 0-K.Coleman INTERCEPTED by 35-J.Watson at LA 40. 35-J. |
| GIVEAWAY | 2026_05_BUF_LA  |      4604 |     5 | BUF       | LA        | run         |              0 |             1 | (8:00) 4-J.Cook up the middle to LA 22 for no gain (53-N.Landman). FUMBLES (53-N.Landman), RECOVERED by LA-99- |
| GIVEAWAY | 2026_08_BAL_BUF |       851 |     1 | BUF       | BAL       | pass        |              1 |             0 | (4:17) 17-J.Allen pass short middle intended for 85-J.Hawes INTERCEPTED by 96-B.Washington at BUF 17. 96-B.Was |
| GIVEAWAY | 2026_08_BAL_BUF |      2126 |     2 | BUF       | BAL       | pass        |              0 |             1 | (2:00) (Shotgun) 17-J.Allen pass short middle to 2-D.Moore to BAL 20 for 19 yards (24-M.Starks; 0-R.Smith). Th |
| TAKEAWAY | 2026_01_BUF_HOU |       313 |     1 | HOU       | BUF       | pass        |              0 |             1 | (9:40) (Shotgun) 7-C.Stroud sacked at HOU 29 for -5 yards (15-G.Rousseau). FUMBLES (15-G.Rousseau) [15-G.Rouss |
| TAKEAWAY | 2026_01_BUF_HOU |      4486 |     4 | HOU       | BUF       | pass        |              0 |             1 | (:16) (Shotgun) 7-C.Stroud sacked at BUF 28 for -10 yards (15-G.Rousseau). FUMBLES (15-G.Rousseau) [15-G.Rouss |
| TAKEAWAY | 2026_03_LAC_BUF |      3306 |     4 | LAC       | BUF       | pass        |              1 |             0 | (13:38) (Shotgun) 10-J.Herbert pass deep middle intended for 13-M.Valdes-Scantling INTERCEPTED by 22-C.Gardner |
| TAKEAWAY | 2026_04_NE_BUF  |      1208 |     2 | NE        | BUF       | pass        |              0 |             1 | (10:14) (Shotgun) 10-D.Maye sacked at BUF 30 for -7 yards (sack split by 99-T.Parker and 91-E.Oliver). FUMBLES |
| TAKEAWAY | 2026_04_NE_BUF  |      2220 |     2 | NE        | BUF       | pass        |              1 |             0 | (:16) (Shotgun) 10-D.Maye pass short left intended for 87-R.Doubs INTERCEPTED by 23-D.Alford at NE 46. 23-D.Al |
| TAKEAWAY | 2026_06_BUF_LV  |      2457 |     3 | LV        | BUF       | pass        |              1 |             0 | (9:00) (Shotgun) 8-K.Cousins pass short middle intended for 87-M.Mayer INTERCEPTED by 42-D.Williams at LV 32.  |
| TAKEAWAY | 2026_08_BAL_BUF |      1322 |     2 | BAL       | BUF       | pass        |              0 |             1 | (14:10) (Shotgun) 5-T.Huntley sacked at BAL 33 for -7 yards (24-C.Bishop). FUMBLES (24-C.Bishop) [24-C.Bishop] |
| TAKEAWAY | 2026_08_BAL_BUF |      2315 |     2 | BAL       | BUF       | pass        |              1 |             0 | (1:21) (Shotgun) 12-J.Fagnano pass short left intended for 4-Z.Flowers INTERCEPTED by 21-D.Igbinosun (25-G.Sto |
| TAKEAWAY | 2026_08_BAL_BUF |      4458 |     4 | BAL       | BUF       | run         |              0 |             1 | (2:38) 12-J.Fagnano FUMBLES (Aborted) at BUF 48, RECOVERED by BUF-42-D.Williams at BUF 47.                     |


### MIN turnover events

Giveaways 5, takeaways 12, margin +7. Of these, rows with play_type not in {pass, run}: 1; rows with both flags: 0. Interceptions thrown by MIN: 3; fumbles lost by MIN: 2.

| side     | game_id         |   play_id |   qtr | posteam   | defteam   | play_type   |   interception |   fumble_lost | desc                                                                                                           |
|:---------|:----------------|----------:|------:|:----------|:----------|:------------|---------------:|--------------:|:---------------------------------------------------------------------------------------------------------------|
| GIVEAWAY | 2026_01_GB_MIN  |        78 |     1 | MIN       | GB        | pass        |              1 |             0 | (14:23) (Shotgun) 1-K.Murray pass deep right intended for 14-J.Jennings INTERCEPTED by 25-K.Nixon [44-Z.Frankl |
| GIVEAWAY | 2026_03_MIN_TB  |      2682 |     3 | MIN       | TB        | pass        |              1 |             0 | (8:41) (Shotgun) 1-K.Murray pass short middle intended for 3-J.Addison INTERCEPTED by 91-A.Robinson (50-V.Vea) |
| GIVEAWAY | 2026_05_MIN_NO  |       740 |     1 | MIN       | NO        | run         |              0 |             1 | (:50) (Shotgun) 33-A.Jones up the middle to NO 7 for 3 yards (97-K.Boyd). FUMBLES (97-K.Boyd), RECOVERED by NO |
| GIVEAWAY | 2026_05_MIN_NO  |      2643 |     3 | MIN       | NO        | pass        |              0 |             1 | (2:49) (Shotgun) 1-K.Murray pass short left to 4-M.Price to NO 12 for 7 yards (22-M.Emerson; 20-P.Werner). FUM |
| GIVEAWAY | 2026_08_MIN_DET |      1919 |     2 | MIN       | DET       | pass        |              1 |             0 | (1:51) 1-K.Murray pass short left intended for 3-J.Addison INTERCEPTED by 4-D.Reed [93-T.Lacy] at DET 38. 4-D. |
| TAKEAWAY | 2026_01_GB_MIN  |      3754 |     4 | GB        | MIN       | pass        |              0 |             1 | (5:01) (Shotgun) 10-J.Love sacked at GB 11 for -12 yards (sack split by 43-A.Van Ginkel and 51-B.Cashman). FUM |
| TAKEAWAY | 2026_01_GB_MIN  |      3877 |     4 | GB        | MIN       | pass        |              1 |             0 | (4:21) (No Huddle, Shotgun) 10-J.Love pass short middle intended for 9-C.Watson INTERCEPTED by 23-J.Pierre (22 |
| TAKEAWAY | 2026_02_MIN_CHI |       860 |     1 | CHI       | MIN       | pass        |              1 |             0 | (1:47) (Shotgun) 18-C.Williams pass deep middle intended for 10-L.Burden INTERCEPTED by 7-B.Murphy [29-Jac.Tho |
| TAKEAWAY | 2026_02_MIN_CHI |      2383 |     3 | CHI       | MIN       | run         |              0 |             1 | (9:42) 4-D.Swift right tackle to MIN 1 for no gain (61-J.Redmond; 0-I.Pace). FUMBLES (61-J.Redmond), RECOVERED |
| TAKEAWAY | 2026_03_MIN_TB  |      4171 |     4 | TB        | MIN       | pass        |              1 |             0 | (1:54) (Shotgun) 6-B.Mayfield pass short right intended for 1-K.Gainwell INTERCEPTED by 43-A.Van Ginkel [51-B. |
| TAKEAWAY | 2026_03_MIN_TB  |      4453 |     4 | TB        | MIN       | pass        |              1 |             0 | (:08) (Shotgun) 10-J.Daniels pass deep right INTERCEPTED by 2-I.Rodgers at MIN 3. 2-I.Rodgers to MIN 3 for no  |
| TAKEAWAY | 2026_04_MIA_MIN |      1684 |     2 | MIA       | MIN       | pass        |              0 |             1 | (5:50) (Shotgun) 2-M.Willis pass incomplete short left to 5-J.Wright. Minnesota challenged the incomplete pass |
| TAKEAWAY | 2026_05_MIN_NO  |      1938 |     3 | NO        | MIN       | kickoff     |              0 |             1 | 16-W.Reichard kicks 59 yards from MIN 35 to NO 6. 38-J.Price to NO 29 for 23 yards (41-J.Golday). FUMBLES (41- |
| TAKEAWAY | 2026_05_MIN_NO  |      2351 |     3 | NO        | MIN       | pass        |              1 |             0 | (7:45) (Shotgun) 6-T.Shough pass short right intended for 18-B.Lance INTERCEPTED by 7-B.Murphy at MIN 49. 7-B. |
| TAKEAWAY | 2026_05_MIN_NO  |      3730 |     4 | NO        | MIN       | pass        |              1 |             0 | (2:56) (No Huddle, Shotgun) 6-T.Shough pass deep left intended for 12-C.Olave INTERCEPTED by 7-B.Murphy at MIN |
| TAKEAWAY | 2026_07_IND_MIN |      3709 |     4 | IND       | MIN       | pass        |              1 |             0 | (1:15) (No Huddle, Shotgun) 17-D.Jones pass short right intended for 86-W.Mallory INTERCEPTED by 22-H.Smith at |
| TAKEAWAY | 2026_08_MIN_DET |      1221 |     2 | DET       | MIN       | pass        |              1 |             0 | (12:56) (Shotgun) 16-J.Goff pass short left intended for 1-J.Williams INTERCEPTED by 23-J.Pierre at MIN 46. 23 |


### Fumble-event verification (recovering team recorded in the file)

For each `fumble_lost==1` event involving BUF or MIN: the fumbling team (`fumbled_1_team`) and recovering team (`fumble_recovery_1_team`) fields. A fumble is a genuine turnover only if recovery team differs from fumbling team. Rows with null fields need manual review.

| game_id         |   play_id | play_type   | posteam   | fumbled_by_team   | recovered_by_team   | recovery_is_opponent_of_fumbler   |
|:----------------|----------:|:------------|:----------|:------------------|:--------------------|:----------------------------------|
| 2026_01_BUF_HOU |       313 | pass        | HOU       | HOU               | BUF                 | yes                               |
| 2026_01_BUF_HOU |      4486 | pass        | HOU       | HOU               | BUF                 | yes                               |
| 2026_01_GB_MIN  |      3754 | pass        | GB        | GB                | MIN                 | yes                               |
| 2026_02_MIN_CHI |      2383 | run         | CHI       | CHI               | MIN                 | yes                               |
| 2026_03_LAC_BUF |        63 | run         | BUF       | BUF               | LAC                 | yes                               |
| 2026_03_LAC_BUF |      2861 | pass        | BUF       | BUF               | LAC                 | yes                               |
| 2026_03_LAC_BUF |      3173 | pass        | BUF       | BUF               | LAC                 | yes                               |
| 2026_04_MIA_MIN |      1684 | pass        | MIA       | MIA               | MIN                 | yes                               |
| 2026_04_NE_BUF  |      1208 | pass        | NE        | NE                | BUF                 | yes                               |
| 2026_04_NE_BUF  |      2179 | pass        | BUF       | BUF               | NE                  | yes                               |
| 2026_05_BUF_LA  |      4604 | run         | BUF       | BUF               | LA                  | yes                               |
| 2026_05_MIN_NO  |       740 | run         | MIN       | MIN               | NO                  | yes                               |
| 2026_05_MIN_NO  |      1938 | kickoff     | NO        | NO                | MIN                 | yes                               |
| 2026_05_MIN_NO  |      2643 | pass        | MIN       | MIN               | NO                  | yes                               |
| 2026_08_BAL_BUF |      1322 | pass        | BAL       | BAL               | BUF                 | yes                               |
| 2026_08_BAL_BUF |      2126 | pass        | BUF       | BUF               | BAL                 | yes                               |
| 2026_08_BAL_BUF |      4458 | run         | BAL       | BAL               | BUF                 | yes                               |

Full description, 2026_03_LAC_BUF play 3173: (15:00) (Shotgun) 17-J.Allen sacked at BUF 28 for -6 yards (52-K.Mack). Los Angeles Chargers challenged the passer was down by contact ruling, and the play was REVERSED. (Shotgun) 17-J.Allen sacked at BUF 28 for -6 yards (52-K.Mack). FUMBLES (52-K.Mack) [52-K.Mack], RECOVERED by LAC-0-D.Henley at BUF 28. Fumble Forced by 0-D.Henley.

Full description, 2026_04_MIA_MIN play 1684: (5:50) (Shotgun) 2-M.Willis pass incomplete short left to 5-J.Wright. Minnesota challenged the incomplete pass ruling, and the play was REVERSED. (Shotgun) 2-M.Willis sacked at MIA 39 for -9 yards (15-D.Turner). FUMBLES (15-D.Turner), RECOVERED by MIN-51-B.Cashman at 50.

Full description, 2026_03_LAC_BUF play 63: (14:53) 4-J.Cook up the middle to BUF 47 for 4 yards (92-J.Eboigbe). FUMBLES (92-J.Eboigbe), RECOVERED by LAC-0-D.Henley at BUF 47.


### Defensive QB-hit rate (and sack rate): exact definition

**BUF defense.** Denominator = opponent offense rows with `defteam=='BUF'`, `play_type in {pass,run}`, `epa` not null, `pass==1` (all dropbacks: attempts + sacks + scrambles) = 295 rows. Numerator = sum of `qb_hit` = 54. `qb_hit` null in 0 of those rows; pandas `mean()` skips nulls, so the reported rate = 54 / 295 = 0.183 (rate treating nulls as 0 over all 295 = 0.183). Sack rate = sum(`sack`) 15 / 295 = 0.051. Sensitivity: QB hits over attempts only (285 rows) = 54/285 = 0.189. `qb_hit` is a play-level flag (it includes sacks and hits on throws); it is not a pressure flag and was never relabeled as pressure rate. No 2026 pressure field exists in this file (`was_pressure` absent).

**MIN defense.** Denominator = opponent offense rows with `defteam=='MIN'`, `play_type in {pass,run}`, `epa` not null, `pass==1` (all dropbacks: attempts + sacks + scrambles) = 235 rows. Numerator = sum of `qb_hit` = 57. `qb_hit` null in 0 of those rows; pandas `mean()` skips nulls, so the reported rate = 57 / 235 = 0.243 (rate treating nulls as 0 over all 235 = 0.243). Sack rate = sum(`sack`) 25 / 235 = 0.106. Sensitivity: QB hits over attempts only (227 rows) = 57/227 = 0.251. `qb_hit` is a play-level flag (it includes sacks and hits on throws); it is not a pressure flag and was never relabeled as pressure rate. No 2026 pressure field exists in this file (`was_pressure` absent).


## 5. Data provenance (from the files actually used)

`play_by_play_2026.parquet`: 23,647 rows x 372 columns; seasons [2026]; season_type {'REG': 23647}; weeks [1, 2, 3, 4, 5, 6, 7, 8, 9]; games 135; game_date min 2026-09-09 max 2026-11-08.

`roster_weekly_2026.csv`: 22,285 rows x 36 columns; seasons [2026]; weeks [1, 2, 3, 4, 5, 6, 7, 8, 9]. Columns: season, team, position, depth_chart_position, jersey_number, status, full_name, first_name, last_name, birth_date, height, weight, college, gsis_id, espn_id, sportradar_id, yahoo_id, rotowire_id, pff_id, pfr_id, fantasy_data_id, sleeper_id, years_exp, headshot_url, ngs_position, week, game_type, status_description_abbr, football_name, esb_id, gsis_it_id, smart_id, entry_year, rookie_year, draft_club, draft_number.

Columns used or requested, presence and non-null share (full 2026 file):

| column             | in_file   |   non_null_share |
|:-------------------|:----------|-----------------:|
| epa                | True      |            0.989 |
| success            | True      |            0.989 |
| pass               | True      |            1.000 |
| rush               | True      |            1.000 |
| sack               | True      |            0.970 |
| qb_hit             | True      |            0.970 |
| qb_scramble        | True      |            1.000 |
| qb_kneel           | True      |            1.000 |
| interception       | True      |            0.970 |
| fumble_lost        | True      |            0.970 |
| yardline_100       | True      |            0.928 |
| goal_to_go         | True      |            1.000 |
| rusher_player_id   | True      |            0.308 |
| receiver_player_id | True      |            0.361 |
| passer_player_id   | True      |            0.406 |
| pass_attempt       | True      |            0.970 |
| complete_pass      | True      |            0.970 |
| receiving_yards    | True      |            0.241 |
| rushing_yards      | True      |            0.307 |
| passing_yards      | True      |            0.241 |
| was_pressure       | False     |          nan     |
| offense_players    | False     |          nan     |
| defense_players    | False     |          nan     |
| n_offense          | False     |          nan     |
| pass_rusher        | False     |          nan     |
| xpass              | True      |            0.761 |
| cpoe               | True      |            0.358 |
| wp                 | True      |            0.994 |

Full PBP schema (name:dtype), all columns:

```
play_id:float64, game_id:str, old_game_id:str, home_team:str, away_team:str, season_type:str, week:int32, posteam:str, posteam_type:str, defteam:str, side_of_field:str, yardline_100:float64, game_date:str, quarter_seconds_remaining:float64, half_seconds_remaining:float64, game_seconds_remaining:float64, game_half:str, quarter_end:float64, drive:float64, sp:float64, qtr:float64, down:float64, goal_to_go:float64, time:str, yrdln:str, ydstogo:float64, ydsnet:float64, desc:str, play_type:str, yards_gained:float64, shotgun:float64, no_huddle:float64, qb_dropback:float64, qb_kneel:float64, qb_spike:float64, qb_scramble:float64, pass_length:str, pass_location:str, air_yards:float64, yards_after_catch:float64, run_location:str, run_gap:str, field_goal_result:str, kick_distance:float64, extra_point_result:str, two_point_conv_result:str, home_timeouts_remaining:float64, away_timeouts_remaining:float64, timeout:float64, timeout_team:str, td_team:str, td_player_name:str, td_player_id:str, posteam_timeouts_remaining:float64, defteam_timeouts_remaining:float64, total_home_score:float64, total_away_score:float64, posteam_score:float64, defteam_score:float64, score_differential:float64, posteam_score_post:float64, defteam_score_post:float64, score_differential_post:float64, no_score_prob:float64, opp_fg_prob:float64, opp_safety_prob:float64, opp_td_prob:float64, fg_prob:float64, safety_prob:float64, td_prob:float64, extra_point_prob:float64, two_point_conversion_prob:float64, ep:float64, epa:float64, total_home_epa:float64, total_away_epa:float64, total_home_rush_epa:float64, total_away_rush_epa:float64, total_home_pass_epa:float64, total_away_pass_epa:float64, air_epa:float64, yac_epa:float64, comp_air_epa:float64, comp_yac_epa:float64, total_home_comp_air_epa:float64, total_away_comp_air_epa:float64, total_home_comp_yac_epa:float64, total_away_comp_yac_epa:float64, total_home_raw_air_epa:float64, total_away_raw_air_epa:float64, total_home_raw_yac_epa:float64, total_away_raw_yac_epa:float64, wp:float64, def_wp:float64, home_wp:float64, away_wp:float64, wpa:float64, vegas_wpa:float64, vegas_home_wpa:float64, home_wp_post:float64, away_wp_post:float64, vegas_wp:float64, vegas_home_wp:float64, total_home_rush_wpa:float64, total_away_rush_wpa:float64, total_home_pass_wpa:float64, total_away_pass_wpa:float64, air_wpa:float64, yac_wpa:float64, comp_air_wpa:float64, comp_yac_wpa:float64, total_home_comp_air_wpa:float64, total_away_comp_air_wpa:float64, total_home_comp_yac_wpa:float64, total_away_comp_yac_wpa:float64, total_home_raw_air_wpa:float64, total_away_raw_air_wpa:float64, total_home_raw_yac_wpa:float64, total_away_raw_yac_wpa:float64, punt_blocked:float64, first_down_rush:float64, first_down_pass:float64, first_down_penalty:float64, third_down_converted:float64, third_down_failed:float64, fourth_down_converted:float64, fourth_down_failed:float64, incomplete_pass:float64, touchback:float64, interception:float64, punt_inside_twenty:float64, punt_in_endzone:float64, punt_out_of_bounds:float64, punt_downed:float64, punt_fair_catch:float64, kickoff_inside_twenty:float64, kickoff_in_endzone:float64, kickoff_out_of_bounds:float64, kickoff_downed:float64, kickoff_fair_catch:float64, fumble_forced:float64, fumble_not_forced:float64, fumble_out_of_bounds:float64, solo_tackle:float64, safety:float64, penalty:float64, tackled_for_loss:float64, fumble_lost:float64, own_kickoff_recovery:float64, own_kickoff_recovery_td:float64, qb_hit:float64, rush_attempt:float64, pass_attempt:float64, sack:float64, touchdown:float64, pass_touchdown:float64, rush_touchdown:float64, return_touchdown:float64, extra_point_attempt:float64, two_point_attempt:float64, field_goal_attempt:float64, kickoff_attempt:float64, punt_attempt:float64, fumble:float64, complete_pass:float64, assist_tackle:float64, lateral_reception:float64, lateral_rush:float64, lateral_return:float64, lateral_recovery:float64, passer_player_id:str, passer_player_name:str, passing_yards:float64, receiver_player_id:str, receiver_player_name:str, receiving_yards:float64, rusher_player_id:str, rusher_player_name:str, rushing_yards:float64, lateral_receiver_player_id:str, lateral_receiver_player_name:str, lateral_receiving_yards:float64, lateral_rusher_player_id:str, lateral_rusher_player_name:str, lateral_rushing_yards:float64, lateral_sack_player_id:str, lateral_sack_player_name:str, interception_player_id:str, interception_player_name:str, lateral_interception_player_id:str, lateral_interception_player_name:str, punt_returner_player_id:str, punt_returner_player_name:str, lateral_punt_returner_player_id:str, lateral_punt_returner_player_name:str, kickoff_returner_player_name:str, kickoff_returner_player_id:str, lateral_kickoff_returner_player_id:str, lateral_kickoff_returner_player_name:str, punter_player_id:str, punter_player_name:str, kicker_player_name:str, kicker_player_id:str, own_kickoff_recovery_player_id:str, own_kickoff_recovery_player_name:str, blocked_player_id:str, blocked_player_name:str, tackle_for_loss_1_player_id:str, tackle_for_loss_1_player_name:str, tackle_for_loss_2_player_id:str, tackle_for_loss_2_player_name:str, qb_hit_1_player_id:str, qb_hit_1_player_name:str, qb_hit_2_player_id:str, qb_hit_2_player_name:str, forced_fumble_player_1_team:str, forced_fumble_player_1_player_id:str, forced_fumble_player_1_player_name:str, forced_fumble_player_2_team:str, forced_fumble_player_2_player_id:str, forced_fumble_player_2_player_name:str, solo_tackle_1_team:str, solo_tackle_2_team:str, solo_tackle_1_player_id:str, solo_tackle_2_player_id:str, solo_tackle_1_player_name:str, solo_tackle_2_player_name:str, assist_tackle_1_player_id:str, assist_tackle_1_player_name:str, assist_tackle_1_team:str, assist_tackle_2_player_id:str, assist_tackle_2_player_name:str, assist_tackle_2_team:str, assist_tackle_3_player_id:str, assist_tackle_3_player_name:str, assist_tackle_3_team:str, assist_tackle_4_player_id:str, assist_tackle_4_player_name:str, assist_tackle_4_team:str, tackle_with_assist:float64, tackle_with_assist_1_player_id:str, tackle_with_assist_1_player_name:str, tackle_with_assist_1_team:str, tackle_with_assist_2_player_id:str, tackle_with_assist_2_player_name:str, tackle_with_assist_2_team:str, pass_defense_1_player_id:str, pass_defense_1_player_name:str, pass_defense_2_player_id:str, pass_defense_2_player_name:str, fumbled_1_team:str, fumbled_1_player_id:str, fumbled_1_player_name:str, fumbled_2_player_id:str, fumbled_2_player_name:str, fumbled_2_team:str, fumble_recovery_1_team:str, fumble_recovery_1_yards:float64, fumble_recovery_1_player_id:str, fumble_recovery_1_player_name:str, fumble_recovery_2_team:str, fumble_recovery_2_yards:float64, fumble_recovery_2_player_id:str, fumble_recovery_2_player_name:str, sack_player_id:str, sack_player_name:str, half_sack_1_player_id:str, half_sack_1_player_name:str, half_sack_2_player_id:str, half_sack_2_player_name:str, return_team:str, return_yards:float64, penalty_team:str, penalty_player_id:str, penalty_player_name:str, penalty_yards:float64, replay_or_challenge:float64, replay_or_challenge_result:str, penalty_type:str, defensive_two_point_attempt:float64, defensive_two_point_conv:float64, defensive_extra_point_attempt:float64, defensive_extra_point_conv:float64, safety_player_name:str, safety_player_id:str, season:int32, cp:float64, cpoe:float64, series:float64, series_success:float64, series_result:str, order_sequence:float64, start_time:str, time_of_day:str, stadium:str, weather:str, nfl_api_id:str, play_clock:str, play_deleted:float64, play_type_nfl:str, special_teams_play:float64, st_play_type:str, end_clock_time:str, end_yard_line:str, fixed_drive:float64, fixed_drive_result:str, drive_real_start_time:str, drive_play_count:float64, drive_time_of_possession:str, drive_first_downs:float64, drive_inside20:float64, drive_ended_with_score:float64, drive_quarter_start:float64, drive_quarter_end:float64, drive_yards_penalized:float64, drive_start_transition:str, drive_end_transition:str, drive_game_clock_start:str, drive_game_clock_end:str, drive_start_yard_line:str, drive_end_yard_line:str, drive_play_id_started:float64, drive_play_id_ended:float64, away_score:int32, home_score:int32, location:str, result:int32, total:int32, spread_line:float64, total_line:float64, div_game:int32, roof:str, surface:str, temp:float64, wind:float64, home_coach:str, away_coach:str, stadium_id:str, game_stadium:str, aborted_play:float64, success:float64, passer:str, passer_jersey_number:float64, rusher:str, rusher_jersey_number:float64, receiver:str, receiver_jersey_number:float64, pass:float64, rush:float64, first_down:float64, special:float64, play:float64, passer_id:str, rusher_id:str, receiver_id:str, name:str, jersey_number:float64, id:str, fantasy_player_name:str, fantasy_player_id:str, fantasy:str, fantasy_id:str, out_of_bounds:float64, home_opening_kickoff:float64, qb_epa:float64, xyac_epa:float64, xyac_mean_yardage:float64, xyac_median_yardage:float64, xyac_success:float64, xyac_fd:float64, xpass:float64, pass_oe:float64
```


## 8. Schedule row (games.csv)

games.csv rows 7548; 2026 rows 272. BUF@MIN wk9 row (spread_line, total_line, moneylines as in file):

| game_id         | gameday    | gametime   |   spread_line |   total_line |   home_moneyline |   away_moneyline | roof   |
|:----------------|:-----------|:-----------|--------------:|-------------:|-----------------:|-----------------:|:-------|
| 2026_09_BUF_MIN | 2026-11-09 | 20:15      |          -3.5 |         45.5 |            160.0 |           -192.0 | dome   |

### 5 (continued). Files, timestamps and differences from the GitHub Actions artifacts

| Item | Used in this audit | Handoff artifact | Difference / status |
|---|---|---|---|
| Play-by-play | `https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.parquet`; retrieved 2026-11-09 19:30:41 ET; release `Last-Modified` 2026-11-09 19:48:29 GMT (2:48 PM ET), unchanged at the 19:57 ET recheck; 10,050,821 bytes | Artifact 13711131074, run 42699154336, reported as built 4:05 PM ET | **Not retrievable by the author; byte identity later confirmed by the reviewer (R5).** Same upstream URL (the workflow's `curl` line). The release was last modified before the 4:05 PM build and was unchanged afterward, so the artifact copy should be byte-identical, and the reviewer's later check of `SHA256SUMS.txt` confirms it (section 9, R5). Original method: compare `play_by_play_2026.parquet` against `pbp/SHA256SUMS.txt` inside the artifact. The artifact also holds 1999-2025 and `manifest.csv`, which I did not fetch. |
| Weekly rosters | `.../releases/download/weekly_rosters/roster_weekly_2026.csv`; same retrieval time; release `Last-Modified` 2026-11-09 17:34:23 GMT (12:34 PM ET); 7,281,670 bytes | Artifact 13710095041, run 42696340691, reported 3:47 PM ET | Not retrievable. Same upstream file; the artifact wraps 2002-2026 in a `.tar.gz` with `manifest.csv` and `SHA256SUMS.txt`. Same verification route. |
| Schedule / lines | nfldata `games.csv` (raw.githubusercontent), 7,548 rows, 2026 rows 272 | Artifact 13643140837, run 42544692899, coverage 2002-2025 | **Different source and different coverage.** The workflow downloads `releases/download/schedules/games.csv` and exports `games_2002_2025.csv`, so the artifact has no 2026 rows. The 2026 schedule and lines in my reports are not from the artifact. |
| Scoring / TD ledger | not used | Artifact 13711444803, run 42702775512 | Not retrievable. Built from PBP by `scripts/build_scoring_event_ledger.py`; TDs here come from PBP fields. |
| Participation | not used | Artifact 13643886148, 2016-2025 | No 2026 coverage; no participation, snap or route inputs exist for this season. |
| Repository | `nicholascaruso1/nflverse-roster-download`, anonymous git clone, HEAD `302b926d5fb36c73a19709be852260eea72ea2b6`, committed 2026-11-08 21:52 ET | | Public. Contains six workflows and one script; no data files. |

**Artifacts were inaccessible in this Claude session.** The GitHub API returned HTTP 403 ("GitHub access to this repository is not enabled for this session"). `add_repo` reported read-only anonymous git access, which covers clones but not Actions artifacts. No artifact was downloaded, listed or inspected, and the run IDs and artifact IDs in the handoff are unverified.

Schema and coverage for the PBP and roster files are in the generated tables above (all 372 PBP columns with dtypes are listed). Columns absent from the 2026 PBP: `was_pressure`, `offense_players`, `defense_players`, `n_offense`, `pass_rusher`.

## 6. Model completeness

The Bet Model produced no calibrated projection (no fair spread, fair total or win probability). The Prop Model produced no per-prop probability, no-vig price or fair odds, and no prop is Level A. Nothing below was created retrospectively. Break-even percentages quoted in the Lock 2 addendum are arithmetic on posted prices, not model probabilities.

| Bet Model component | Weight | Status | What exists / what is missing |
|---|---|---|---|
| Opponent-adjusted efficiency | 25% | **Partial** | Raw EPA/play and success rate reconciled above. No opponent adjustment, no garbage-time filter. |
| Matchup-specific | 25% | **Partial** | Raw pass/rush EPA splits, sack rate and QB-hit rate (dropback denominator). No pressure rate, route, personnel or participation data. |
| Power rating | 15% | **Unavailable** | No independent rating was sourced. FPI appears only as a reference and is not a component. |
| Market value | 20% | **Partial** | Third-party snapshots and Nick's Hard Rock screenshots exist. No model number, so no model-vs-market edge was computed. |
| Turnover / ST regression | 10% | **Partial** | Turnover counts and margin only. Special teams not computed. No regression formula applied; the direction is qualitative. |
| Injuries / weather / news | 5% | **Partial** | Inactives verified (dome, so weather neutral). The impact of the OL and receiver absences was not quantified. |

| v2.2 layer | Status |
|---|---|
| Offensive Ceiling Index | Partial: descriptive inputs only, no index computed |
| Opportunity Confidence | Partial: qualitative bands; 0-100 not assigned (route/snap inputs unavailable) |
| Scenario Confidence | Partial: qualitative branch ordering, no probabilities |
| Conditional Parlay Engine | Not run (no per-leg probabilities) |
| QB Injury Volatility | Partial: qualitative |
| Lock 1 | Unavailable (no timestamped pre-inactives snapshot) |
| Lock 2 | Partial: inactives verified; Hard Rock prices supplied by Nick at 7:31 PM (props) and 7:53 PM (game); Cook carries line not visible |

## 7. Reproduction

1. Download `play_by_play_2026.parquet` and `roster_weekly_2026.csv` from the nflverse release URLs above, and `games.csv` from nfldata, and compare SHA-256 with the ledger record (or with `SHA256SUMS.txt` in the artifacts).
2. Put them in one folder. The script accepts either `play_by_play_2026.parquet` or `pbp_2026.parquet` as the PBP filename. Run `python3 -I audit.py <folder> audit_data.md`.
3. Every table and count in sections 1-5 and 8 is regenerated, including the BUF@MIN schedule row from `games.csv` (section 8). The narrative in sections 0, 5 (continued), 6 and 9 is hand-written.

Python 3 with pandas, pyarrow and tabulate; the script is deterministic.

**Final status: AUDIT CLOSED 2026-11-09. R1-R8 resolved; D1-D6 remain recorded findings; no frozen classification changed.**

## 9. Review log (code review of audit.py v1, SHA-256 6af0bf75...b875; v2 was a57e36c6...0e04; current is v2.1)

| # | Review item | Disposition in v2 of the script/supplement |
|---|---|---|
| R1 | Filename mismatch (`pbp_2026.parquet` vs `play_by_play_2026.parquet`) | Fixed: script accepts either name; step 2 above states it. |
| R2 | Section 2 text said `pass_attempt==1` excludes sacks | Fixed: text now says box-score attempt = `pass_attempt==1 & sack!=1` and that the raw flag equals dropbacks in this file. No number changed. |
| R3 | Team red-zone comparison broader than the player count | Fixed: described as a raw `rush==1` flag count with no play_type or rusher-id restriction (46 / 21 includes 1 null-rusher row). Cook's 28 / 10 is unaffected. |
| R4 | Script never read `games.csv` | Fixed: section 8 now loads it and prints the BUF@MIN row (spread -3.5, total 45.5, ML -192 / +160, dome). The Hard Rock lines are from Nick's screenshots and are not reproducible by script. |
| R5 | Artifact byte identity unverified | **Closed 2026-11-09 ~8:44 PM ET (reviewer, not the author).** Reviewer retrieved both GitHub Actions artifacts and read `SHA256SUMS.txt`: `play_by_play_2026.parquet` = 422f78930248c86facb6bae5489c612700a9d351504f82a479319af5f9600795 and `roster_weekly_2026.csv` = 5cb8857be2f49be417627b63faa26b33431a53ea6cc8398d087bebeab61c520f, both identical to the release files used in this audit. Artifact ZIP digests (per GitHub metadata): PBP 531858c8055ab5420a161e585e6d6cdeece6f20352c5ddd00592526431cca22e; roster 5278c98541614c37ed3a2f64bc3a069b367e271a33c1d268d88bc4ef886641df. The author never had artifact access; this closure rests on the reviewer's report. |
| R6 | Numerical outputs not independently verified by the reviewer | **Closed 2026-11-09 ~8:40 PM ET.** Reviewer ran audit.py v2.1 (SHA-256 7e181aa6...5102f) on the hash-verified CSV export, roster and games files (exit 0). Reviewer output (53,449 bytes, SHA-256 aa1f9d023112e4a71e9b15808e036a147f093e2eff68d9b059ecd0da0f0b379d) was diffed line by line against the author run on the same inputs (o_csv.md, 53,023 bytes, SHA-256 daa2bdc5...ba40): one differing line, the schema dtype list (`object` vs `str`, a pandas-version label). Every table and count is identical. |
| R7 | Lock 2 addendum not yet reviewed | **Closed.** Reviewer received and reviewed the addendum (`week9-nfl-mnf-buf-min-lock2-addendum.md`) and confirmed the official Lock 2 record is Wentz Under 215.5 (-115) LEAN, with the original pregame WATCH preserved. The D2 annotation (Murray 200.8, Wentz relief game) is carried in the ledger record. |

| R8 | Reviewer environment lacked pyarrow, so R6 could not run | Script v2.1 also reads `play_by_play_2026.csv`, a lossless `to_csv` export of the parquet (SHA-256 dfcaa3c8e1963726d1a0c3be240c990d3d098d121fcd1ccfd87af5a8922c911f). Output on CSV vs parquet is identical except the dtype notation in the schema line (e.g. `week:int64` vs `int32`). **Closed:** reviewer ran v2.1 on the CSV export (see R6). |

audit.py v2.1 SHA-256: 7e181aa6f8d449bd09c532ebf120ba96cea47374b5b16ee6db0941506935102f

## 10. Post-closure note: D1 spike-filter sensitivity (2026-11-10)

Raised during the Week 9 postmortem: `qb_spike` rows carry `pass_attempt==1` but `pass==0`, so the audit's `pass==1` attempt filter omits them while an official box score counts a spike as an attempt. Checked with `spike_check.py` on the pregame PBP (SHA-256 422f7893...0795); output in `spike_check_output.txt`.

| Item | Result |
|---|---|
| Spike rows inside the audit EPA/SR filter (`play_type` in pass/run) | 0 of 51 in the file. **No efficiency, EPA, success-rate, yardage or QB-hit figure changes.** |
| Wentz (weeks 1-2) | 0 spikes. Attempts excluding sacks stay **40** (20 + 20). D1's open 39-vs-40 gap against NFL.com is **not** explained by spikes. |
| Murray (weeks 1, 3, 4, 5, 7, 8) | 1 spike (week 5, 0 yards). Attempts excluding sacks are **154** under the audit filter and **155** with the spike counted. Per-game attempts 25.7 becomes 25.8. |

Disposition: a counting-convention sensitivity of one attempt for Murray, with no effect on any reconciliation result, finding severity or frozen classification. **Audit status stays CLOSED.** `audit.py` v2.1 (SHA-256 7e181aa6...5102f) is unchanged so the reviewer-verified hash still applies; the sensitivity is documented here and in `spike_check.py` instead. D1's "Murray 154" should be read as "154 on the `pass==1` filter; 155 if the week-5 spike is counted". The frozen reports are not rewritten.
