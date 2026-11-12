# NFL Script & Narrative Engine v1.0.1 — WAS @ NYG

**Target:** 2026-11-12 | **Season:** 2026 | **Week:** 10 | **Split:** prospective | **Frozen:** 2026-11-12T18:59:06-05:00
**Game ID:** 2026_10_WAS_NYG (nflverse_schedule) | **Code:** cbafc6af5a19

## Governance
- Pregame cutoff excludes target-date and later results.
- Descriptive research only; no betting recommendation.
- Branded TNF is counted only from the verified TNF table; Thursday/kickoff proxies are labelled proxies.
- Historical team identity is primary; current identity is a separate comparison.
- Cipher variants share a family_id and are not independent confirmations.

## Team identities (historical primary)
- WAS: Washington Commanders (WAS); current: Washington Commanders (same)
- NYG: New York Giants (NYG); current: New York Giants (same)

## Current records
- WAS: 2-5-1
- NYG: 5-2-1

## Findings (gematria values are in findings.csv / ledger)
| Category | Finding | Value | Caveat |
|---|---|---|---|
| records | Mirrored current-season records | WAS 2-5-1 / NYG 5-2-1 | Descriptive symmetry; not a winner prediction. |
| records | WAS current-season record | 2-5-1 | Regular season games before target date. |
| records | WAS current-season win pct | 0.312 | (W + 0.5*T)/G. |
| records | NYG current-season record | 5-2-1 | Regular season games before target date. |
| records | NYG current-season win pct | 0.688 | (W + 0.5*T)/G. |
| schedule_records | WAS all-Thursday record | 7-14-0 | Every Thursday regular-season game; not branded TNF. |
| schedule_records | WAS Thursday (excl. Thanksgiving) record | 4-10-0 | Not branded TNF. |
| schedule_records | WAS Thursday >=7 PM ET proxy record (excl. Thanksgiving) | 3-9-0 | Schedule-time proxy only; NOT a TNF record (includes pre-2006 and kickoff-night games). |
| schedule_records | WAS Thanksgiving Thursday record | 3-4-0 | Thanksgiving games are not branded TNF. |
| schedule_records | WAS Sunday >=7 PM ET proxy record | 13-14-0 | Schedule-time proxy; not a verified package label. |
| schedule_records | WAS Monday >=7 PM ET proxy record | 6-20-0 | Schedule-time proxy; not a verified package label. |
| schedule_records | WAS branded TNF record (verified table) | unavailable: no verified branded-TNF table | Branded TNF is never inferred from Thursday or kickoff times. |
| calendar | WAS days since last Thursday win | 1491 | Last qualifying Thursday win: 2022-10-13. |
| calendar | WAS calendar-month boundaries since last Thursday win | 49 | Last qualifying Thursday win: 2022-10-13. Counts month boundaries crossed, not completed months. |
| calendar | WAS completed calendar months since last Thursday win | 48 | Last qualifying Thursday win: 2022-10-13. |
| schedule_records | NYG all-Thursday record | 5-13-0 | Every Thursday regular-season game; not branded TNF. |
| schedule_records | NYG Thursday (excl. Thanksgiving) record | 5-9-0 | Not branded TNF. |
| schedule_records | NYG Thursday >=7 PM ET proxy record (excl. Thanksgiving) | 5-9-0 | Schedule-time proxy only; NOT a TNF record (includes pre-2006 and kickoff-night games). |
| schedule_records | NYG Thanksgiving Thursday record | 0-4-0 | Thanksgiving games are not branded TNF. |
| schedule_records | NYG Sunday >=7 PM ET proxy record | 18-27-0 | Schedule-time proxy; not a verified package label. |
| schedule_records | NYG Monday >=7 PM ET proxy record | 12-21-0 | Schedule-time proxy; not a verified package label. |
| schedule_records | NYG branded TNF record (verified table) | unavailable: no verified branded-TNF table | Branded TNF is never inferred from Thursday or kickoff times. |
| calendar | NYG days since last Thursday win | 399 | Last qualifying Thursday win: 2025-10-09. |
| calendar | NYG calendar-month boundaries since last Thursday win | 13 | Last qualifying Thursday win: 2025-10-09. Counts month boundaries crossed, not completed months. |
| calendar | NYG completed calendar months since last Thursday win | 13 | Last qualifying Thursday win: 2025-10-09. |
| head_to_head | Previous meeting was tied | 27-27 on 2026-10-11 | Historical context only; not a rematch prediction. |
| calendar | Days remaining in calendar year, excluding game date | 49 | December 31 of the target's calendar year minus target date. |
| calendar | Date digit sum | 15 | Date format YYYYMMDD. |
| calendar | Date digital root | 6 | Date format YYYYMMDD. |
| calendar | Weekday number | 4 | ISO weekday: Monday=1 through Sunday=7. |
| calendar | Weekday digital root | 4 | ISO weekday: Monday=1 through Sunday=7. |
| base_rates | Historical exact 27-27 frequency | 3/7103 (0.042%) | Completed regular-season games in supplied schedule file; in-sample. |
| base_rates | Historical total-54 frequency | 145/7103 (2.041%) | Completed regular-season games; descriptive only. |
| streaks | Days since WAS last win | 11 | Last regular-season win: 2026-11-01; target date excluded; playoffs excluded. |
| streaks | Days since WAS last loss | 4 | Last regular-season loss: 2026-11-08; target date excluded; playoffs excluded. |
| streaks | Days since NYG last win | 4 | Last regular-season win: 2026-11-08; target date excluded; playoffs excluded. |
| streaks | Days since NYG last loss | 25 | Last regular-season loss: 2026-10-18; target date excluded; playoffs excluded. |
| player_names | Jon Runyan matches COMMANDERS | pythagorean | Name-value match only; no player-performance inference. Systems listed are dependent (one family). |
| player_names | Basil Okoye matches COMMANDERS | pythagorean | Name-value match only; no player-performance inference. Systems listed are dependent (one family). |
| player_names | Malik Nabers matches COMMANDERS | ordinal,pythagorean | Name-value match only; no player-performance inference. Systems listed are dependent (one family). |
| player_names | Abdul Carter matches COMMANDERS | ordinal,pythagorean | Name-value match only; no player-performance inference. Systems listed are dependent (one family). |
| claim_audit | WAS external TNF claim vs verified TNF table | claimed 3-9; verified unavailable (no verified branded-TNF table) | Unverified until a verified table exists. Thursday >=7 PM proxy for context only: 3-9-0 (not TNF). |
| claim_audit | NYG external TNF claim vs verified TNF table | claimed 4-8; verified unavailable (no verified branded-TNF table) | Unverified until a verified table exists. Thursday >=7 PM proxy for context only: 5-9-0 (not TNF). |

## Gematria (exact values; roots are secondary)
| Team | Basis | String | Ordinal | Ord root | Reverse | Rev root | Pyth | Pyth root |
|---|---|---|---|---|---|---|---|---|
| WAS | historical | WASHINGTON | 130 | 4 | 140 | 5 | 49 | 4 |
| WAS | historical | COMMANDERS | 105 | 6 | 165 | 3 | 42 | 6 |
| WAS | historical | WASHINGTON COMMANDERS | 235 | 1 | 305 | 8 | 91 | 1 |
| NYG | historical | NEW YORK | 111 | 3 | 78 | 6 | 39 | 3 |
| NYG | historical | GIANTS | 70 | 7 | 92 | 2 | 25 | 7 |
| NYG | historical | NEW YORK GIANTS | 181 | 1 | 170 | 8 | 64 | 1 |

## Interpretation
Do not select the narrative with the most matches. Report both sides.
Historical frequencies are descriptive and in-sample, not predictive.
Predictive evaluation requires preregistration and chronological holdout testing.
