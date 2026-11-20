# WCF Player Milestone Engine v4.1 — Independent Audit, Part 2 (Priority Cases)

Created: Fri 2026-11-20, evening. Status: FROZEN (corrections go in an errata file). Follows `wcf-milestone-engine-audit-1-first-response.md` (saved in the project).
Rules in force: workbook NOT modified; no predictive validity inferred from the 14-case convenience sample; pregame and postgame evidence kept separate; no betting-model input; no subscription, paywall bypass, WCF contact or outside model/service. Retrieval date for all web sources: 2026-11-20.

Coverage statement. Fully rechecked this pass: Stevenson, Collins. Partly rechecked: Eagles–Giants (series count, venue), Panthers (game ordinal), Bears (Macdonald/Johnson ATS, interval arithmetic). Carried from the workbook and NOT yet rechecked: Eagles (NFC record, 67/68 wins, Sirianni, Milton DOB), Panthers (103 road wins, LaFleur 124/125, Love 26/27, Packers vs NFC South, Novak ATS, betting split), Bears (12-8 series, Macdonald DOB, Seattle 4-3, last win in Seattle).

## A. Rhamondre Stevenson (WCF post 10/22; target game at Chicago; pregame cutoff 2026-10-21)

Original WCF claims vs our reconstruction. The workbook's Historical Post Universe records the post's visible claims as: Chicago=35; Thursday=35; next TD #35; full name=257; Thursday Night Football=257; 257 days since last TD vs an NFC opponent. The cipher NAMES used by WCF are not recorded in the workbook; the "Reduction" labels are the reconstruction's, not WCF's.

### A1. Cipher calculations (A=1..Z=26; spaces ignored)
| Phrase | Ordinal | Reverse (A=26..Z=1) | Reduction (Pythagorean; letter values reduced to 1-9, summed) | Reverse Reduction (reverse values reduced letter-by-letter, summed) |
|---|---|---|---|---|
| Chicago | 46 | 143 | 37 | 35 |
| Thursday | 116 | 100 | 35 | 46 |
| Rhamondre Stevenson | 229 | 257 | 85 | 95 |
| Thursday Night Football | 257 | 310 | 95 | 112 |

Chicago detail: ordinal letter values C3 H8 I9 C3 A1 G7 O15; Reduction 3+8+9+3+1+7+6 = 37; reverse values 24,19,18,24,26,20,12 reduce to 6,1,9,6,8,2,3 = 35.
- ERROR (original → corrected → source): workbook "Chicago Reduction = 35" → Chicago Reduction = 37; 35 is the Reverse Reduction value → calculation above. Label status: Contradicted. "Chicago = 35" as a number: Reproduced under Reverse Reduction only.
- No single cipher produces both 35s (Chicago needs Reverse Reduction, Thursday needs Reduction). The two 257s also need different ciphers (name = Reverse; Thursday Night Football = Ordinal). So the four equalities use four different cipher conventions. Whether WCF named a cipher for each is not in the workbook.

### A2. "Next TD would be career #35" (cutoff 2026-10-21; regular season, rushing + receiving)
- NFL.com career table: rushing 2021-25 = 5+5+4+7+7 = 28; receiving 0+1+0+1+2 = 4; total 32. The page does not state scope; 2021-25 values match the workbook.
- NFL.com 2026 log: rushing TDs 10/4 at BUF and 10/11 vs LV; none 9/9, 9/20, 9/27. The 10/18 vs NYJ receiving column is blank; NBC Sports' 10/18 note says Stevenson was not targeted, so no receiving TD. Pregame 2026 = 2.
- Pregame regular-season total 34, so the target-game TD would be #35. Reproduced under regular-season-only counting.
- Postseason: NFL.com 2025 log shows a receiving TD on 2/8/2026 vs Seattle (the other three playoff games: 0 TD). Including it, pregame = 35 and the next TD would be #36.
- ERROR (workbook → corrected): the sheet's note and conclusion say #35 is "correct only when postseason is included". With postseason included the next TD is #36, so #35 holds only for regular-season-only counting (the Cross-Post Matrix wording is right; the sheet note is wrong). The sheet's ledger total rows are also mis-added: "regular season only 30 / 6 / 36" should read 30 rushing + 4 receiving = 34; "incl. postseason 30 / 7 / 37" should read 30 + 5 = 35.
- Status: Reproduced with scope qualification (regular season only).

### A3. "257 days since last TD vs an NFC opponent"
- 2026 NFC opponents before 10/22: only SEA on 9/9 (0 TD). Last prior TD vs NFC = receiving TD vs SEA on 2/8/2026.
- 2/8/2026 to 10/22/2026 = 256 days elapsed; 257 only counting both endpoints. Status: Reproduced only under inclusive counting.

Postgame (kept separate, not used above): the NFL.com log lists receiving TDs on 10/22 and 11/8. No claim about the 10/22 outcome is made here.

## B. Nico Collins (target IND @ HOU 11/19; pregame cutoff 2026-11-18)

### B1. Event accuracy (postgame; separate)
- NFL.com 2026 log row 11/19 vs Colts: W 26-3, 3 rec, 58 yds, 1 TD. 2026 receiving TD dates: 9/13 (1), 10/4 (2), 11/8 (1), 11/15 (1), 11/19 (1). NFL.com career total 30 including 11/19.
- Under the pregame definition (regular-season receiving TDs) the 11/19 TD is #30. Event Reproduced.
- Open on the postgame side: (i) the 42-yard TD length is not confirmed; an NFL.com highlight titled "Nico Collins bursts downfield via 42-yard catch and run late in first half" describes a play that set up field position before halftime, i.e. not a touchdown (the video is undated and may be another game). (ii) NFL.com shows W 26-3 for both 10/11 at TEN and 11/19. (iii) The PFR box score could not be opened (tool permission denied; not retried).
- Status: TD event Reproduced; length 42 yards Unsupported/Unconfirmed; score entry flagged for data quality.

### B2. Pregame baseline (rows dated on or before 2026-11-18 only)
| Claim | Convention | Calculation | Primary source | Status |
|---|---|---|---|---|
| 29 regular-season receiving TDs | Regular season, receiving only, through 11/18 | 1+2+8+7+6 = 24 through 2025; 2026 rows 9/13 (1), 10/4 (2), 11/8 (1), 11/15 (1) = 5; total 29 | NFL.com career + 2026 log | Reproduced. The workbook's PFR cross-check could not be reproduced (PFR page returned a stale partial table) |
| Scope note | Receiving vs total TDs | Collins also has a 7-yard rushing TD at IND on 11/30/2025 | PFR box score 202511300clt; ESPN/AP recap | Total-TD scope would give 30 pregame |
| Day 323 | Day of year of target date | 11/19/2026 = day 323 | calendar | Reproduced |
| 42 days remaining | Dec 31 minus target date; target excluded | 365 − 323 = 42 | calendar | Reproduced |
| 120 days to birthday | Elapsed days 11/19/2026 to 3/19/2027 | 30+31+31+28 = 120 | calendar; DOB 3/19/1999 per ESPN bio, Ourlads, Wikipedia, PFR | Reproduced. Workbook inconsistency: its DOB Verification sheet says Collins DOB is unverified and not to be frozen, while the Collins sheet uses it; the Football Database page it cites returned no name or DOB when retrieved. Official Texans bio not retrieved |
| 36 regular-season home appearances | Games played in home games | NFL.com situational: 2021 7; 2022 4; 2023 9; 2024 6; 2025 7 = 33; 2026 (log: 9/13 BUF, 10/4 DAL, 10/25 NYG; 9/20 CIN and 9/27 at IND show no stats) 3; total 36 | NFL.com situational 2021-25; 2026 log | Reproduced |
| +2 postseason home appearances | Playoff games played at Houston | 2023 WC vs CLE and 2024 WC vs LAC assumed played; 2025 playoff games both away (WC at PIT, divisional at NE) | ABC13/ESPN for 2025; 2023-24 not checked | Partially reproduced: 2025 adds 0 (confirmed); 2023/2024 participation unverified |
| 11/19 = home game #39 or #37 | #39 needs postseason; #37 regular season only | 36+2+1 = 39; 36+1 = 37 | derived | Scope-dependent; both preserved |

### B3. Evidence provenance (was the claim recorded before kickoff?)
- Available record: Nick's earliest message in this thread is 11/19 around 9:28 AM (a gematria card for the game). The first mention of WCF or Collins is the 11/20 5:20 PM handoff, which says "the user reports that the WCF gematria decode hit". There is no pre-kickoff message, screenshot, post URL or timestamp for the original WCF Collins decode in this thread or in the workbook.
- The Collins sheet says "four WCF claims" (30th TD, 42 days, 120 days, 39th home game) but, unlike the Chase and Eagles sheets, gives no source URL or image for what WCF actually said and no timestamp. The Read Me lists the sheet under 2026-11-19 and the postgame addition as v4.1 afterwards; that order is suggestive, not proof of pre-kickoff creation. A +105 price appears only in the handoff table.
- The sheet cannot show whether the four components came from WCF or were chosen after the fact.
- Conclusion: evidence provenance NOT ESTABLISHED. The #30 milestone event occurred, so it counts as a successful event prediction if the original record is dated before kickoff. What would establish it, to be supplied by Nick and not obtained by me: the original WCF post or screenshot with its timestamp, and the timestamp of the ChatGPT conversation that produced the pregame Collins reconstruction. One event does not establish predictive validity.

## C. Eagles–Giants (WCF 11/8; cutoff 2026-11-07)
Checked this pass:
- Series count. Giants.com Week 9 preview: "In regular season play, the teams have met 182 times." Its record text as retrieved (87-93-2, "led by the Eagles") is internally inconsistent, so only the 182 is used. Other public figures, all preserved: sportsbrackets.net (2026-09-06) regular season 94-88-2 = 184, postseason Eagles 3-2; Wikipedia mirrors (early 2024) 94-89-2 = 185 meetings; current Wikipedia 190 total (97-91-2 all-time; regular season 94-89-2; postseason 3-2); Giants.com in January 2023 called that week's game the 182nd meeting. The 2023 and 2026 Giants.com "182" cannot describe the same convention, since several meetings occurred between. WCF's "184 previous / 185th" matches the sportsbrackets regular-season total (94+88+2 = 184). Status: Contradicted by one source, supported by another; UNRECONCILED. Do not call 184 verified or refuted.
- Venue. The Eagles were the home team on 11/8 (sportsbrackets schedule; Wikipedia lists Lincoln Financial Field as the Eagles' stadium). The slide-1 MetLife image remains a graphic error, as the workbook states.
- Ciphers: Eagles Ordinal 49; Giants Reduction 25; Catholicism Ordinal 112, Reduction 49, Reverse 185, Reverse Reduction 68; New York Sumerian = 6 x 111 = 666; 666 = 36x37/2. All Reproduced under the stated conventions. 9/20 to 11/8 = 49 days elapsed.

## D. Panthers–Packers (WCF 10/29; cutoff 2026-10-28)
- "103rd game of the season": CBS 2026 schedule listing: Weeks 1-4 have 16 games each, Week 5 15, Week 6 14, Week 7 14 = 107 games before the Week 8 Thursday opener, so Panthers–Packers is the 108th. 103 is the Ordinal value of "Jesuits". Status: Contradicted under full-schedule counting; WCF's counting rule is undisclosed.
- "Jesuits = 103 / 50": Ordinal 103 reproduces; 9/9 to 10/29 = 50 elapsed (51 if 9/9 is day 1); 103 is the 27th prime.
- Wisconsin Ordinal 125, Reduction 44, Reverse 118: Reproduced.
- Not rechecked this pass: Packers 11-7 / 12-7, LaFleur 125th, Panthers 102 road wins, Love 26 losses, 26 losses vs NFC South, Novak 71.4%, betting split.

## E. Bears–Seahawks (WCF 11/2; cutoff 2026-11-01)
- Macdonald ATS. NBC Sports (published 10/29/2026, 9:30 PM; spells "McDonald"): Seahawks as home favorite 8-6-2 ATS (13-3 SU); no NFC-opponent split in the article; window not defined. WCF: 2-6 (25.0%) as home favorite and 3-7 vs NFC. Status: 2-6 Contradicted by NBC on its stated basis; 3-7 Unsupported. A different window or line source could explain it, which the public text cannot test. Both preserved.
- Ben Johnson: NBC 8-4 ATS as underdog (4-4 as road underdog; no non-division split in NBC). The 14-3 non-division figure is from the workbook's SI/Kacsmar citation and was not rechecked.
- Intervals: 6/26/2026 to 11/2/2026 = 129 days; 12/26/2021 to 11/2/2026 = 1,772 days = 4 years (1,461 days) + 311 days = 44 weeks 3 days; WCF's "4y44w4d" needs inclusive counting.
- Ciphers: Seahawks Reverse 129; Seattle Reverse 107; Seattle Reverse Reduction 44. Reproduced.

## F. Cross-case observations (no hit rate calculated)
1. Cipher choice: in Stevenson, four equalities need four different ciphers. Five ciphers applied to every word and phrase give each one five numbers to match against many candidate targets.
2. Scope choice: Stevenson #35 (regular season only), Moore 44 (regular season only), Collins #39 (postseason included), Kelce 87 (rushing + receiving only). One decode style does not use one scope.
3. Date choice: elapsed in Chase, Eagles and Hurts; inclusive in Stevenson (257) and Bears (4y44w4d); Nix 19 implies both endpoints.
4. Denominator: still missing is how often the same patterns appear for players never selected, for selections that missed, and across the unobserved locked posts, plus how many candidate combinations existed per decode. Required before any inference.

## G. Disagreement register (additions and changes; workbook unchanged)
D-01 Stevenson Chicago label: workbook Reduction 35 → Reduction 37; 35 = Reverse Reduction.
D-02 Collins DOB: workbook sheets conflict; 3/19/1999 supported by ESPN, Ourlads, Wikipedia, PFR; official Texans bio not retrieved.
D-03 Collins home count: regular-season 36 Reproduced (NFL.com); postseason +2 unverified for 2023/2024.
D-04 Stevenson #35: workbook note "correct only with postseason" → #35 only regular-season-only; with postseason the next TD is #36; ledger totals 36/37 → 34/35.
D-05 Eagles–Giants meetings: 182 (Giants.com 2026) vs 184 (sportsbrackets regular season) vs 185 (Wikipedia mirrors, early 2024) vs 190 (current Wikipedia total). Unreconciled; WCF 184 not refuted.
D-06 Panthers "103rd game": CBS schedule count gives 107 prior games.
D-07 Macdonald ATS: WCF 2-6 vs NBC 8-6-2; NFC 3-7 has no public source found.
D-08 NFL.com log shows 26-3 for both 10/11 and 11/19; PFR box score not opened.
D-09 Collins 42-yard TD: unconfirmed; an undated NFL.com highlight calls a 42-yard catch-and-run a first-half field-position play.
D-10 Collins provenance: no pre-kickoff timestamped WCF record in this thread or the workbook.

## H. Next in the agreed order
Moore (44 vs 45 scope, 38 AFC games, 37 weeks), Nix (42 home points on a road game, 19 vs 18 days, career game 42), Kelce (87 scope); then the unresolved Patreon records; then claim-by-claim reconciliation against the ChatGPT workbook; then the frozen protocol.

## Sources (retrieved 2026-11-20)
NFL.com: players/nico-collins/stats/career, /stats/logs/2026/, /stats/situational/2021-2025; players/rhamondre-stevenson/stats/career, /stats/logs/2026/, /stats/logs/2025/. ESPN, Ourlads, Wikipedia, PFR for Collins DOB. PFR boxscore 202511300clt; ESPN recap gameId 401772787. NBC Sports fantasy note 2026-10-18 (Stevenson vs Jets). Giants.com Week 9 stats preview; sportsbrackets.net Eagles–Giants series pages; Wikipedia Eagles–Giants rivalry. CBS Sports 2026 schedule article. NBC Sports Bears–Seahawks betting trends (10/29/2026). ABC13, Fox Sports, ESPN on the 2025 Texans playoffs. NFL.com highlight "Nico Collins bursts downfield via 42-yard catch and run late in first half".
