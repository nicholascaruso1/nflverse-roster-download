# WCF Milestone Engine v4.1 — Part 6: Cell-level reconciliation map (read-only; no workbook changes)

Written Fri 2026-11-20. DRAFT. Source: `WCF_Player_Milestone_Engine_v4.1.xlsx` (38 sheets) opened read-only. Nothing was edited; original values are preserved here for the audit trail. Candidate-cell list (199 hits, pattern-matched, so some are false positives): `data/v4.1_reconciliation_cell_map.csv`. Proposed changes are text for review, not applied.

## 1. Workbook-wide finding

v4.1 contains **zero formula cells**. Every count, total and status is typed text. So "checking formulas" is not possible; each total must be recalculated from source rows and re-typed, and every summary cell can silently drift from its source sheet (as the Universe Summary has).

## 2. Primary target cells by register ID

| ID | Sheet!cell (v4.1 current value) | Proposed correction (original kept in an audit-trail column) |
|---|---|---|
| D-01 | Rhamondre Stevenson Reconstruction!B7 ("Chicago Reduction = 35; Ordinal 46"); Public WCF Claims Ledger!C19; Cross-Post Methodology Matrix!H15 | Reduction 37; Reverse Reduction 35; keep WCF's stated "35" as the claim |
| D-02 | Nico Collins Reconstruction!B9, D28 (uses 1999-03-19); **DOB Verification!C2–C8 say "Not verified"; F2 says "Do not freeze 120-day interval until DOB verified from official source"** | Internal inconsistency inside v4.1. Keep 1999-03-19 with "four citations, independence not established; official bio not retrieved" |
| D-03 | Nico Collins Reconstruction!A10, A39; Matrix!G8 | 36 regular-season reproduced; postseason +2 unverified |
| D-04 | Stevenson sheet!A9, B9, E23, A26, A37; Ledger!G19; Matrix!C15, L15. **A37 says the 35th-TD milestone "is supported if the count includes the Feb. 8 postseason TD"; E23 sums 32 + 1 + 2 = 35 as the pregame total** | Regular-season pregame 34, next #35; combined pregame 35, next #36. A37's direction is reversed |
| D-05 | Eagles Giants Reconstruction!A13, B13, D13, A36; Ledger!C12, E12, G12; Matrix!F14, L14 | Preserve 182/184/185/190; no single number |
| D-06 | Panthers Packers Reconstruction!A8, D8 (already says "do not silently accept 103"); Ledger!G21; Matrix!D17 | Reconstructed ordinal 108th; 103 only as separate coincidence |
| D-07 | Bears Seahawks Reconstruction!A20, B20; Matrix!L21; Ledger!G25 | Keep 2–6 unverified and 8–6–2 as unaligned conflicting source; add windows |
| D-08 | Nico Collins Reconstruction!D43 ("Houston won 26–3") | Add duplicated 26–3 NFL.com anomaly; box score unreconciled |
| D-09 | Nico Collins Reconstruction!B44 ("42-yard receiving touchdown … OFFICIALLY VERIFIED"), D49 | Length unconfirmed; "OFFICIALLY VERIFIED" in C44 is stronger than my evidence. Exclude unrelated 42-yard catch-and-run |
| D-10 | Nico Collins Reconstruction!C45 ("HIT"); Matrix!K8; Read Me!B57 | Replace with "Event reproduced; pregame provenance not established" |
| D-11 | DJ Moore Source Audit!A8–D8, B16; DJ Moore Reconstruction!C9; Matrix!C19 ("postseason-inclusive baseline is 45, so next would be #46") | 46 combined; next #47; keep 1/18 TD single-source limitation |
| D-12 | **Bo Nix Uploaded Slide Audit!B3 ("Denver Broncos at Seattle Seahawks")**, C10, D10, E10; Matrix!G11; Ledger!G9 | Venue Denver. B3 is a workbook-authored header, not a WCF quote, so the Seattle error originates in the workbook, not in the slide transcription. 36 conditional on definition |
| D-13 | Travis Kelce #87 Symbolic Audit!B12, D12, B17; Matrix!H20, L20; Ledger!G24 (and Ledger!C24 for the 13-pick card) | 2 rushing through 2025; 86 under receiving-plus-rushing |
| D-14 | Kelce sheet!D12 ("postseason … 20"), B17 | Add 2014-item separate possibility, with cutoff stated for each source |
| D-15 | Ja'Marr Chase Reconstruction!A18 ("42 prior home games; target is #43"), D18, D29, A35 ("all … reproducible") | 42nd–43rd unresolved; A35's "all reproducible" must be softened |
| Moore AFC | DJ Moore Reconstruction!C8; Source Audit!B7, D7; Matrix!F19, D22, D28, D29 | Keep provisional ±1 everywhere; do not count as reproduced in summaries |

## 3. Candidate new register item (for ChatGPT to number)

**Proposed D-16 — Universe Summary counts** (Universe Summary!B4–B8, typed text):

| Cell | v4.1 | Recount from the Historical Post Universe rows |
|---|---|---|
| B4 | "NFL-related archive entries recorded: 48" | 48 rows, but relevance is 45 Yes / 1 Possible / 2 No, so not all 48 are NFL-related |
| B5 | Public 11 | 17 rows marked Public; 12 NFL posts with an identifiable selection |
| B6 | Locked 25 | 26 |
| B7 | 12 unresolved | 5 |
| B8 | Yes 45 / Possible 2 / No 1 | 45 / 1 / 2 |

Definitions to freeze are those ChatGPT proposed (total, relevance, locked, public, unresolved, public NFL selections). The 12 selections are an archive classification, not 12 verified decodes or predictions. 10/5 stays No; 10/4 updated stays its own record, not merged with Moore.

## 4. Other cells worth review before v4.2

- Stevenson!A37 and Collins!C45 contain scope/status wording stronger or reversed relative to the evidence (above).
- Collins!C44 "OFFICIALLY VERIFIED" is a postgame-sheet label; keep postgame content separate from pregame claims.
- Matrix!K8 ("Reconstructed with definition caveat") should read "event reproduced; provenance not established".
- Read Me update log entries should append rather than overwrite; add a v4.2 entry per change with old value, new value, calculation, source.

## 5. Next

1. ChatGPT confirms the D-16 number and definitions and the cell list above (it can use the CSV in place of uploading v4.1, or Nick can upload the workbook).
2. Apply changes to a **copy** (v4.2) with an audit-trail sheet (old value / new value / calculation / source / register ID).
3. Recompute every typed total from source sheets and diff against v4.1.
