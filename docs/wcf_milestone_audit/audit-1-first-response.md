# WCF Player Milestone Engine v4.1 — Independent Audit, Part 1 (First Response)

Created: Fri 2026-11-20. Status: FROZEN (corrections go in an errata file, not edits).
Scope: methodology audit of a research artifact. Not ground truth. No betting-model input, no picks, no direction. Separate from the NFL/CFB betting models and the Script & Narrative Engine. No WCF purchase, no paywall access, no contact, nothing sent to another service.

## 1. Workbook inspected
Yes. All 38 sheets were dumped to text and read in full. Nothing was modified.

Sheets: Read Me; Rhamondre Stevenson Reconstruction; WCF Historical Post Universe; Oct 25 Promo Audit; Oct 5 Free Play Audit; Universe Summary; Cross-Post Methodology Matrix; Eagles Giants; Brian Thomas Jr Source Audit; Bo Nix Uploaded Slide Audit; Ja'Marr Chase; Bo Nix Source Audit; Cole Kmet Symbolic; Jalen Hurts; Nico Collins; Public WCF Claims Ledger; Opponent History; StatMuse Query Templates; Player Query Queue; Interpretation Rules; Eligibility Audit; Source Log; DOB Verification; Expanded Query Queue; Pregame Candidate Status; Home Appearances; Query Execution Log; Career Home Audit; Injury Home Reconciliation; Career Home Count Verification; Audit Closure Status; Pat Freiermuth; Panthers Packers; CeeDee Lamb; DJ Moore Source Audit; DJ Moore Reconstruction; Travis Kelce #87; Bears Seahawks.

Cases (14): Stevenson (10/22), Collins (11/19, user-supplied), Chase (11/1), Hurts (10/11), Nix (10/15, two sheets), Moore (10/4, two sheets), Kmet (10/11), Kelce #87 (10/17-18), Eagles +3.5 (11/8), Panthers +3.5 (10/29), Bears +3.5 (11/2), Brian Thomas Jr (11/5), Freiermuth (10/1), Lamb (10/8).
Archive ledger: 48 entries (Public 11, Locked 25, Mixed 12; the Public/Locked/Mixed counts overlap the "Sitemap-listed" rows).
The Collins-engine sheets (Opponent History through Audit Closure, ~12 sheets) are a candidate-universe build for the 11/19 game, not WCF claims.

## 2. Three most consequential methodological risks
R1. Counting-convention freedom. The workbook switches scope per claim: regular season vs postseason vs combined; elapsed vs inclusive days; receiving vs rushing vs total TDs; games played vs team home dates. A claim "reproduces" if any defensible convention matches. Examples: Stevenson #35 (table and matrix disagree on scope), Moore 44 (regular-season only; 45 with playoffs), Bears 4y44w4d (inclusive only), Nix 19 days (18 elapsed), Kelce 87 (receiving+rushing only; 84 receiving-only), Collins home game #39 (postseason included) vs #37 (excluded). Without a declared convention per feature before the fact, the match rate is not interpretable.
R2. No denominator. 14 convenience cases, drawn from public posts whose decodes were recoverable. 25+ locked posts are unobserved, so nothing can be said about hits, misses or base rates. "Reproduced" means WCF's arithmetic checks out, not that the method predicts. Mechanism counts use "at least one component reproduced".
R3. Hindsight and unstable sources. The Collins case was added in v4.1 after the outcome and is user-supplied; the workbook has no archived, timestamped pregame claim for it. Several inputs are live or stale pages (StatMuse crawled months ago; NFL.com pages that now include the target game). Pregame values must be rebuilt from dated rows only, and the workbook itself says some are not frozen.

## 3. Collins #30 independent check (retrieved 2026-11-20)
Sources: NFL.com career stats page; NFL.com 2026 game log; ESPN/CBS/PFR recap of 11/30/2025; ABC13/Fox/KSAT/ESPN reports on 2025 playoffs. PFR player page returned a stale partial table (2021-23 only) and was not used. The PFR 11/19/2026 box score fetch was blocked by the tool's permission rule, so it was not retried or bypassed.

| Claim | Independent finding | Status |
|---|---|---|
| 29 regular-season receiving TDs through 11/18 | NFL.com career: 1+2+8+7+6 through 2025 = 24; 2026 log TD rows dated 9/13 (1), 10/4 (2), 11/8 (1), 11/15 (1) = 5 before 11/19; total 29. NFL.com career total 30 includes 11/19 | Reproduced (regular-season receiving only) |
| 11/19 TD is the 30th | Log: 11/19 vs Colts, 3 rec, 58 yds, 1 TD, W 26-3. 30th under receiving-only scope | Reproduced with scope qualification |
| Collins also has a 7-yd RUSHING TD at IND (11/30/2025) | Confirmed by PFR/ESPN recap; so "total TD" scope would give a different count | Scope item, consistent with workbook's opponent table |
| 42-yard length | Not seen in any retrieved source (log shows yards per game only) | Missing / not independently confirmed |
| Day 323; 42 days left; 120 days to 3/19/2027 | Recomputed by script: 323; 42 (Dec 31 minus 11/19, target date excluded); 120 | Reproduced (convention: remaining days exclude the date itself) |
| DOB 1999-03-19 | Not verified by me in this part. The workbook's own DOB Verification sheet lists Collins DOB as "not verified" and says not to freeze the 120-day interval (see Part 2, which finds public support for 3/19/1999) | Unsupported / internal contradiction |
| 36 regular-season home appearances pregame, +2 postseason; 11/19 = #39 (or #37) | 2026 part (3: 9/13 Bills, 10/4 Cowboys, 10/25 Giants; games 9/20 and 9/27 show no stats) is consistent with the NFL.com log. 2021-25 splits (7+4+9+6+7) not verified in this part (see Part 2). Postseason: 2025 playoff games were both away (WC at PIT, divisional at NE), so 2025 adds 0 home; the 2 postseason home games (2023, 2024 wild cards) are not verified. Existing StatMuse snapshots (33 / 35) are stale and differ in scope | Partially reproduced; scope-dependent |
| Houston won 26-3 | NFL.com log shows W 26-3. Same score is shown for 10/11 at Titans, which is suspicious and unresolved | Reproduced from one source; data-quality flag |

Classification: the event (30th regular-season receiving TD, 11/19) occurred on the sources checked. The pregame side cannot be verified from the workbook: the original Collins claim has no archived timestamp. So it counts as a successful event prediction conditional on the researcher's own pre-game record, which has not been seen. One event gives no predictive validity, strategy profit or statistical significance. Nothing in the postgame row was used to build the pregame baseline; the 29 comes from rows dated 11/18 or earlier.

## 4. Cipher and date recomputation
32 distinct cipher claims recalculated under the workbook's stated conventions (Ordinal; Reduction = Pythagorean; Reverse; Reverse Reduction letter-by-letter; Sumerian = 6 x ordinal): 31 reproduce. One mismatch:
- Stevenson sheet "Chicago Reduction 35": Chicago = 37 under Reduction (C3 H8 I9 C3 A1 G7 O6). 35 is the Reverse Reduction value. Either the workbook's label or WCF's label is wrong; the original slide label was not checked here. (Thursday Reduction 35 reproduces.)
Dates: 305/60/120/42 (Chase), 49 (Eagles), 65/707=101wk (Hurts), 294=42wk; Nix rushing interval 18 elapsed (not 19), 259=37wk (Moore), 129 and 1,772 days (Bears), 50 (Panthers), 103 = 27th prime, 666 = T36, Thursday #42 (Oct 15). All reproduce under the stated convention. Collins: see section 3.
A test line "Touchdown Reduction 39" in the checking script was a test error (the claim is Reverse Reduction); it reproduces.

## 5. First five claims to audit in detail
1. Stevenson: "Chicago 35" label; scope for "#35 TD" (workbook table vs matrix conflict); "257 days" (256 elapsed / 257 inclusive).
2. Collins: home-game count (36 + 2) from season-level splits, including the 2026 no-stat rows and the DOB contradiction.
3. Eagles-Giants: 184/185 all-time meetings vs NFL's 182 regular-season meetings; slide 1 MetLife vs Lincoln Financial Field.
4. Panthers: "103rd game" vs 107 prior games; "26 losses vs NFC South" unverified; "11-7 all-time" omits postseason.
5. Bears: Macdonald 2-6 ATS home favorite (WCF) vs 8-6-2 (NBC); 4y44w4d requires inclusive count.
Queued next: Moore 44 vs 45 scope and AFC-game count; Nix 42 home points on a road game; Kelce 87 scope; Freiermuth/Lamb/Nix source audits; Oct 4 Updated Free Play attribution; Oct 25 promo media; Oct 5 MLB control.

## 6. Disagreement register (initial; superseded where Part 2 changes an entry)
D-01 Stevenson Chicago: workbook "Reduction 35"; recalculated Reduction 37, Reverse Reduction 35.
D-02 Collins DOB: Collins sheet uses 1999-03-19; DOB Verification sheet says not verified. Not resolved.
D-03 Collins home count: workbook 36+2; only the 2026 portion supported so far.
D-04 Stevenson #35: table says 35 pregame including postseason; matrix says regular-season only. Not resolved.
D-05 Eagles-Giants meetings: WCF 184 vs NFL 182 (regular season). Preserved both.
D-06 Panthers game ordinal: WCF 103rd vs 108th by full-schedule count.
D-07 Macdonald ATS: WCF 2-6 vs NBC 8-6-2. Preserved both.
D-08 NFL.com log: 26-3 shown for both 10/11 and 11/19. Unresolved.
No workbook classification was changed.

## Sources
NFL.com career stats (nfl.com/players/nico-collins/stats/career) and 2026 log (.../stats/logs/2026/), retrieved 2026-11-20; PFR box score 202511300clt; ESPN recap gameId 401772787; ABC13 / Fox Sports / KSAT reports of the Jan 12, 2026 wild card at Pittsburgh and the divisional loss at New England.
