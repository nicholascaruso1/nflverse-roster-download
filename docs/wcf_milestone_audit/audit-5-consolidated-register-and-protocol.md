# WCF Milestone Engine v4.1 — Part 5 (rev. 2): Consolidated Disagreement Register (D-01 to D-15) and Proposed Audit Protocol

Written Fri 2026-11-20. DRAFT rev. 2 for review (rev. 1 is commit 19d5958 on this branch). Revision log: register wording refined for D-02, D-06, D-07, D-09, D-12, D-14, D-15 per reviewer comments; protocol adds convention pre-selection, independence definition, frozen search space and comparison counting; stop/go table replaced (20% threshold removed); Section C adds three requirements and the independent Universe Summary recount; Part 3 inputs partly archived. No finding was reversed. Research artifact only; separate from all betting models, the Narrative Engine and the registry. v4.1 workbook, Parts 1–4 and errata-3 are untouched. Where Part 1 and Part 2 word an entry differently, Part 2 supersedes (Part 1 originals are preserved in `audit-1-first-response.md`). Nothing here recommends a bet or builds a predictive method.

## A. How to read the register

Each entry carries three separate statuses, because they answer different questions:

- **Arithmetic**: does the stated number follow from the stated inputs and convention?
- **Source**: are the inputs themselves verified by retrievable sources, and how many?
- **Pregame provenance**: is it established that the claim was published before the event (original WCF post, user-supplied screenshot, or workbook transcription only)?

Source rows are dated transcriptions (page-to-text summarizer), not raw-HTML archives. Archived as dated CSV transcriptions: Hurts and Chase game rows (`data/nfl_com_extracts_2026-11-20.csv`); Nix and Kelce game rows, the Kelce career table and the Moore career table (`data/nfl_com_extracts_part3_2026-11-20.csv`). **Not archived:** Moore's game-by-game opponent lists (only the auditor's per-season AFC counts, flagged unverified; the 2019/2020 pages returned no rows), and all Collins, Stevenson, Eagles, Panthers and Bears inputs.

## B. Register

Provenance key: **PUB** = public Patreon text/slides as transcribed in the workbook (page not reopened by me); **IG** = user-supplied Instagram screenshots, seen only through the workbook; **USR** = user-supplied claim, no public post located; **ARCH** = archive capture of a page that could not be reopened.

| ID | Case | Exact claim at issue | Workbook value | Finding (original → corrected, with basis) | Arithmetic | Source | Provenance |
|---|---|---|---|---|---|---|---|
| D-01 | Stevenson | "Chicago = 35" (Reduction) | Reduction 35 | Reduction 37; Reverse Reduction 35. No single cipher yields both 35s (Chicago, Thursday) or both 257s | Workbook label wrong; corrected value reproduces | Computed from ciphers' stated conventions | PUB |
| D-02 | Collins | DOB for "120 days to next birthday" | Sheets conflict (1999-03-19 vs "not verified") | 3/19/1999 appears on ESPN, Ourlads, Wikipedia, PFR; these are four citations, not demonstrated independent sources (Wikipedia may repeat another); official Texans bio not retrieved | Reproduces given that DOB | 4 citations, independence not established; no official bio | USR |
| D-03 | Collins | 39th home appearance (36 + 2 + …) | 36 + 2 | Regular-season 36 reproduced (NFL.com situational splits: 7, 4, 9, 6, 7 + 3 in 2026); postseason +2 not verified for 2023/2024 | Reproduces for regular season | 1 source; postseason unverified | USR |
| D-04 | Stevenson | "Next TD = #35" | Notes say correct only with postseason; ledger totals 36/37 | #35 holds only for regular-season-only (34 pregame). With the 2/8 postseason TD the next is #36. Ledger totals should read 34/35 | Scope-dependent | NFL game logs | PUB |
| D-05 | Eagles | Eagles–Giants meeting count 184 | 184 | Conflict preserved: 182 (Giants.com, regular season), 184 (sportsbrackets, regular season), 185 (Wikipedia mirrors, early 2024), 190 (current Wikipedia total). WCF 184 not refuted | Not computable until definition fixed | Four sources disagree | PUB |
| D-06 | Panthers | "103rd game" | 103rd | Contradicted under the full chronological regular-season count: weeks 1–7 = 107 games (CBS), so Panthers–Packers is the reconstructed 108th. 103 is the 27th prime, preserved as a separate numerical coincidence, not a count | Count contradicted | CBS schedule | PUB |
| D-07 | Bears | Macdonald ATS 2–6 | 2–6 | Source conflict, comparison not normalized: NBC (10/29/2026 9:30 PM) shows 8–6–2; date windows, venue filters and favorite/underdog definitions of both figures are unknown; NFC 3–7 split has no public source found. The 2–6 claim is unverified, not disproved. Workbook must keep both figures with their windows, not replace 2–6 with 8–6–2 | Cannot compare: windows differ | 2 sources, unaligned | PUB |
| D-08 | Collins | Result of 10/11 vs 11/19 games | — | NFL.com log shows W 26–3 for both dates; PFR box score not opened | n/a | Source anomaly | USR |
| D-09 | Collins | 42-yard TD length | 42 yards | Unconfirmed. The undated NFL.com highlight of a 42-yard catch-and-run is not corroboration and is not to be used as such | Unverifiable | PFR box score request denied; not retried | USR |
| D-10 | Collins | Event recorded before kickoff | "Hit" | Provenance NOT ESTABLISHED: no timestamped pre-kickoff WCF record in the workbook or this thread. Event accuracy (#30 TD) is a separate, reproduced question | n/a | n/a | **Not established** |
| D-11 | Moore | Postseason-inclusive baseline "45, next #46" | 45 | 46, next #47: 44 regular + 2 postseason TDs (1/10 and 1/18/2026) | Corrected value reproduces | 1/10 TD: AP/Tribune/ESPN; 1/18 TD: NFL.com log only | IG |
| D-12 | Nix | "Target game at Seattle … internal logic conflict" | Road game; home-points claim invalid | Game at Empower Field, Denver. The 36 home points are conditional on the stated definition: 6 home rushing TDs × 6; other scoring (2-pt, kicking, other TD types) was not checked | Reproduces | Venue: 4+ pages | IG |
| D-13 | Kelce | "82 receiving + 3 rushing through 2025 + 2 = 87" | 87 | 2 rushing through 2025 (2019, 2021); total 86 under the workbook's own definition. NFL.com career rushing "3" includes the 11/8/2026 TD (post-cutoff); that is a candidate explanation, not established | Contradicted as stated | NFL.com logs, StatMuse, RotoWire | ARCH |
| D-14 | Kelce | Career TD total, source conflict | 87 | Compare at one cutoff (10/18/2026) and one definition: StatMuse 85 through 2025 (82 rec + 2 rush + one 2014 "RET TD") + 2 = 87; offensive TDs only = 86. Wikipedia's 86 total is stamped "as of Week 9 2026" (a later cutoff, after the 11/8 rushing TD) and does not obviously use the same definition. The 2014 item is unverified. This is a separate, unverified route to 87, not evidence that the workbook's 82 + 3 + 2 decomposition was right | Scope- and cutoff-dependent | Two sources, different cutoffs; item unverified | ARCH |
| D-15 | Chase | "43rd regular-season home game" | 43 (uses StatMuse 40 through 2025) | Unresolved: 42nd–43rd: NFL.com home rows 41, minus 2022 non-appearance rows and one possible 2023 non-appearance (17 rows vs GP 16) = 39–40 played, +2 in 2026, +1 target | Unresolved ±1; blocked from "reproduced" until rows reconcile to games played | NFL.com rows vs StatMuse snapshot | PUB |

### Items kept at claim level, not register disagreements

- **Hurts** (Part 4): #65 reproduced for regular-season rushing TDs only (64 pregame); the 5 postseason rushing TDs in 2024 change a combined count, not this one. 707 days = 101 weeks: *date arithmetic reproduced*; *that this was his last Jacksonville rushing TD is consistent with retrieved evidence, not exhaustively verified*. DOB inherited from workbook.
- **Moore** AFC count (38 before target, 39th): arithmetic fine; inputs hand-transcribed, 2019 shows 16 rows vs GP 15, 2019/2020 re-fetch returned no rows. Provisional ±1.
- **Nix** 18 elapsed vs 19 inclusive days: agrees with workbook; WCF's other intervals use elapsed days. Slide 4/4 missing.
- **Public Patreon records** (10/1, 10/4 updated, 10/8, 11/5, 10/25, 10/5) and all locked posts: Missing/inaccessible or unresolved; not nonmatches; no selection inferred.
- **Ciphers**: 31 of 32 originally checked reproduce; the exception is D-01.

## C. Reconciliation targets against v4.1 (no edits made)

Workbook cells that this register would change, for review before any new version: Stevenson Chicago label (D-01) and ledger totals (D-04); Collins DOB/home-count notes (D-02, D-03) and the Collins "Hit" provenance wording (D-10); Panthers game ordinal (D-06); Moore baseline row 211 (D-11); Nix Slide Audit rows 203/309 (D-12); Kelce rows 212, 503, 1019–1025 (D-13, D-14); Chase home-game row (D-15); Moore/Chase "pending/count audit" notes. Universe Summary counts (48 entries; 11 public; 25 locked; 12 unresolved) were not independently recounted.

Added requirements: (1) D-07 keeps the differing ATS windows and definitions beside both figures. (2) D-14 corrects the cutoff and scope description, not only the displayed total. (3) D-15 and the Moore AFC count keep explicit unresolved status in both the case sheet and the summary; neither is counted as fully reproduced.

**Universe Summary independent recount** (Historical Post Universe sheet rows, parsed from the workbook dump; one row's columns shifted because its title contains the field delimiter, corrected by hand):

| Item | Summary says | Recount from rows |
|---|---|---|
| Total entries | 48 | 48 (agrees) |
| NFL relevance Yes / Possible / No | 45 / 2 / 1 | 45 / 1 / 2 (10/5 was reclassified to No in its own audit sheet; summary not updated) |
| Locked | 25 | 26 by the Access status column |
| Public (any relevance) | "11 explicitly marked Public" | 17 rows marked Public; 12 are NFL posts with an identifiable selection (Eagles, Brian Thomas Jr., Bears, Chase, Panthers, Stevenson, Nix, Kmet, Hurts, Lamb, Moore, Freiermuth); the others are the Kelce follow-up, the 10/25 promo, the 10/4 image-only update, and two non-NFL posts |
| Sitemap-listed / unresolved | 12 | 5 (11/13, 10/30, 10/28, 10/11 TD card, 10/23 recording); 26 + 17 + 5 = 48 |

None of the Summary counts should be carried into v4.2 until ChatGPT confirms the definitions; the Locked, Public and unresolved figures do not reproduce.

## D. Proposed audit protocol v0 (for review; not a prediction method)

Purpose: a fixed evidence standard for auditing any numerology/milestone claim made by a public source. It is defined from audit failures (scope drift, off-by-one counts, source conflicts), not from which cases matched, and it is not to be tuned on new outcomes. It makes no claim about edge and feeds no betting model.

**Claim record (required fields):** exact wording and publication timestamp; claim category (never merged: statistical milestone; calendar/elapsed interval; birthday interval; opponent-specific interval; career/home game count; gematria; symbolic jersey/history; football rationale; missing decode); counting scope (regular, postseason, combined); cutoff date; convention (cipher name, elapsed vs inclusive); source URLs, retrieval date, and dated transcription or CSV; three statuses (arithmetic, source, pregame provenance).

**Convention pre-selection (new):** the counting scope, interval convention and cipher method for a claim must be chosen before the claim is tested, from what the source states. A match found only after trying alternative scopes, intervals or ciphers is exploratory and cannot be labeled reproduced under the primary convention.

**Fixed conventions:** elapsed days by default, inclusive reported alongside; every count stated as regular / postseason / combined; "home" defined per claim as team-home or player's-team-home; cipher conventions as listed in Part 1; counts of games must reconcile row-by-row to games played, and any mismatch (e.g., 16 rows vs GP 15) blocks "reproduced"; birthdays need two independent sources, meaning sources with different underlying records (e.g., an official team bio and a league database), not two sites repeating one biography; a blank row is not proof of a non-appearance and an extra row is not proof of a game played.

**Evidence rules:** reproduction of arithmetic is never promoted to confirmation of provenance; postgame data may be used to validate stats only if dated before the claim cutoff; contradictory sources are kept, not chosen between; locked or inaccessible content stays Missing; one numerical match is not causation.

**Denominator and search-space rules (required before any prevalence statement):** freeze the candidate universe and the complete set of numerical operations searched (players, ciphers, date intervals, counting scopes) before outcomes are evaluated; record the number of attempted comparisons, not only the matches; log every selection, including those with no disclosed decode; enumerate for each decode how many conventions and intervals were available (so chance-match rates can be estimated); record for non-selected players in the same games whether equivalent numbers existed; record pregame timestamps at publication.

**Stop/go criteria (rev. 2):**

| Stage | Requirement |
|---|---|
| GO: prospective logging | Every selection has a timestamped pregame record, a complete claim record, and a frozen convention and search space. |
| GO: pilot completion | At least 100 prospectively logged selections, including selections with no disclosed decode. A completeness checkpoint only, not validation or significance. |
| GO: prevalence analysis | Candidate universe, decode availability, search space, missingness and comparison procedure fully specified, with a prespecified analysis that accounts for multiple comparisons. Sample size set by the hypothesis, outcome, expected effect and design, not a round number. |
| STOP: individual claim | Any unresolved game-count discrepancy blocks a "reproduced" label for that claim, regardless of how many other claims reconcile. |
| STOP: sample | Pregame provenance is missing for a material portion of the sample, or the candidate universe cannot be reconstructed. |
| NEVER GO | No transfer into betting models, the registry, the Narrative Engine or staking decisions. No paid or private content required. |

The earlier 20%-unresolved threshold is removed. The unresolved proportion is reported only as a descriptive data-quality statistic.

## E. Suggested sequence

1. Review this register and the three-status columns.
2. Archive remaining publicly available source material as dated transcriptions (Moore game rows, Collins, Chase 2022–23 detail, Stevenson, Eagles, Panthers, Bears); do not pursue paid or private content.
3. Resolve D-05, D-07, D-09, D-14, D-15 where public sources allow; leave the rest open.
4. Reconcile each workbook change against the register, preserving original values and an audit trail; confirm Universe Summary definitions; only then draft v4.2.
