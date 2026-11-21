# WCF Milestone Engine v4.1 — Independent Audit, Part 4: Hurts, Chase, and remaining Patreon records

Retrieved Fri 2026-11-20. Research artifact only; separate from all betting models, the Narrative Engine and the registry. v4.1, Parts 1–3 and errata-3 untouched. Register continues from D-14 (D-01 to D-14 retained, not renumbered). No new errata to my own earlier reports were found in this pass.

Evidence standard (new, per reviewer note): the NFL.com extracts used here are archived in `data/nfl_com_extracts_2026-11-20.csv` (116 rows, Hurts and Chase game rows) and the recompute is in `scripts/hurts_chase_checks.py`. Limitation: pages were read through a page-to-text summarizer, not saved as raw HTML, so the CSV is a transcription. Parts 3 inputs (Moore, Nix, Kelce) are still not archived as CSV.

Postgame hygiene: the Hurts and Chase logs also showed rows after each post's cutoff (including each target game). None were used to build or repair a pregame claim. Post-cutoff rows appear only where stated.

## 0. Access limits (nothing bypassed)

Fetching the public Patreon pages (10/1 Freiermuth, 10/4 Updated Free Play, 10/8 Lamb, 11/5 Thomas Jr.) failed with a client error from this environment; nothing was retrieved. I did not try alternate routes. Locked posts remain Missing/inaccessible, not nonmatches. So for those records I could only verify facts that are checkable elsewhere; I could not inspect any image or caption.

## 1. Jalen Hurts — Oct 11 (TD +200, 2U)

| Claim | Status | Calculation / source |
|---|---|---|
| Next regular-season rushing TD would be #65 | **Reproduced** | NFL.com career table: 3+10+13+15+14+8+1 = 64 (2020–2026). The only 2026 rushing TD before 10/11 is 9/28 @CHI. Career table is regular season only: 2024 rows sum to 14 (matches table) and the 5 postseason rushing TDs that year are excluded. Postseason-inclusive count is higher and was not computed for all years. |
| 101 weeks since last rushing TD vs Jacksonville | **Reproduced** | Last JAX rushing TD 11/3/2024 (1 TD). 11/3/2024 → 10/11/2026 = 707 days = 101.0 weeks. I did not retrieve a full game list vs JAX; no 2025 Eagles–Jaguars game is shown in the 2024/2026 logs, so "last" is consistent but not exhaustively checked. |
| 65 days after birthday | **Reproduced, DOB not re-fetched** | DOB 8/7/1998 taken from the workbook's team-bio citation; 8/7/2026 → 10/11/2026 = 65 days. |
| United Kingdom = 65 (Reduction); Philadelphia = 65 (Reduction), 101 (Ordinal) | **Reproduced** | Script: UK Red 65; Philadelphia Red 65, Ord 101. |

## 2. Ja'Marr Chase — Nov 1 (TD −115, 1U)

| Claim | Status | Calculation / source |
|---|---|---|
| 60th regular-season career TD (59 pregame) | **Reproduced** | 2021–25: 13+9+7+17+8 = 54 (season logs agree with the career table). 2026 before 11/1: @HOU 2, @PIT 1, @MIA 1, @BAL 1 = 5. Total 59; no rushing TDs. |
| 42 days since last TD vs AFC South | **Reproduced** | 9/20 @HOU → 11/1 = 42 days; 10/4 vs JAX had 0. |
| 43 weeks since last home TD | **Reproduced** | 1/4/2026 vs CLE → 11/1 = 301 days = 43.0 weeks; home 2026 games before 11/1 (9/13 TB, 10/4 JAX) had 0. |
| 120 days to next birthday | **Reproduced, DOB not re-fetched** | 3/1/2000 per workbook; 11/1/2026 → 3/1/2027 = 120. |
| 43rd regular-season home game | **Partially reproduced — D-15** | Home rows in NFL.com logs 2021–25: 9, 7, 9, 8, 8 = 41 listed. 2022 has 4 rows with no stats (GP 12), one of them home (PAN): 40 played. 2023 shows 17 rows against GP 16 on the career table, so one 2023 row may be a non-appearance: 39–40 played. Plus 2026 home games TB and JAX = 2. Titans 11/1 is the **42nd–43rd** home game. The workbook's 43 uses a StatMuse snapshot of 40 through 2025 (not re-fetched). |
| Ciphers: Touchdown = 42 (Reduction) / 120 (Reverse); Chase = 43 (Reduction); Titans = 43 and Football = 43 (Reverse Reduction) | **Reproduced** | Script: Touchdown Red 42, Reverse 120; Ja'Marr Chase Red 43; Titans RevRed 43; Football RevRed 43. |

## 3. Records not independently audited here

| Record | Status |
|---|---|
| Cole Kmet 10/11 (#85 / Ditka / #89) | Jersey/history facts rest on workbook-cited team pages; not re-fetched. Symbolic association; no measurable rule. |
| Brian Thomas Jr. 11/5 | Football rationale (short week, Baltimore blitz, production decline) not re-audited; Instagram decode Missing. Patreon page not retrievable now. |
| Pat Freiermuth 10/1 | Selection and jersey #88 only; decode Missing; page not retrievable now. |
| CeeDee Lamb 10/8 | Selection only; no decode; page not retrievable now. |
| 10/4 Updated Free Play attribution | Unresolved; not retrievable now. Do not assume duplicate, replacement or distinct pick. |
| 10/25 promo (five 403 images) and 10/5 MLB control | Unchanged from the workbook; promotional / control only; no selection added. |
| Locked NFL cards and Inner Circle posts | Missing/inaccessible; not nonmatches. |

## 4. Register additions

| ID | Claim (exact) | Workbook | Finding | Calculation | Status |
|---|---|---|---|---|---|
| D-15 | Chase "43rd regular-season home game" | Reconstructed using 40 home games through 2025 (StatMuse) | 42nd–43rd; depends on whether one 2023 row (17 rows vs GP 16) and the 2022 non-appearance rows count | 2021–25 home rows 41 → 39–40 played, + 2 in 2026, + 1 target | Unresolved ±1, provisional |

D-01 to D-14 unchanged.

## 5. What this does and doesn't show

Two more cases whose stated statistics and ciphers reproduce (Hurts fully; Chase except the home-game count, which is provisional). This is still a convenience sample with no denominator: no count of how many other players or intervals produced equally clean matches, and no way from here to see the picks that came without a disclosed number. Reproduction means the arithmetic is right, not that it predicts anything. No hit rate or recommendation follows.

## 6. Still open before reconciliation

- Retrieve Patreon pages or user-supplied images for 10/1, 10/4 updated, 10/8, 11/5 if Nick can supply screenshots (only public material).
- Resolve ±1 counts (Moore AFC games, Chase home games) using archived raw NFL.com extracts or a second game-by-game source.
- Consolidated register D-01 to D-15, then the fixed protocol, then reconcile against the workbook.
