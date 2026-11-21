#!/usr/bin/env python3
"""Build WCF Player Milestone Engine v4.2 DRAFT as a COPY of v4.1.
v4.1 is opened read-only and never written. Every edit is an exact-substring
replacement (or exact whole-cell replacement) asserted against the v4.1 value,
and logged to a new 'Audit Trail' sheet. Research artifact only."""
import openpyxl, shutil, sys, re, collections, datetime
from openpyxl.styles import Alignment, Font

SRC = "/mnt/user-data/uploads/94cec51f-WCF_Player_Milestone_Engine_v4.1.xlsx"
OUT = "/home/claude/out/WCF_Player_Milestone_Engine_v4.2_DRAFT.xlsx"

wb = openpyxl.load_workbook(SRC)
orig = openpyxl.load_workbook(SRC)  # untouched reference for diffing

# ---------- independent arithmetic checks (asserted before any edit) ----------
def ordv(c): return ord(c.upper()) - 64
def red(n):
    while n > 9: n = sum(int(d) for d in str(n))
    return n
def ordinal(s): return sum(ordv(c) for c in s if c.isalpha())
def reverse(s): return sum(27 - ordv(c) for c in s if c.isalpha())
def reduction(s): return sum(red(ordv(c)) for c in s if c.isalpha())
def revred(s): return sum(red(27 - ordv(c)) for c in s if c.isalpha())
assert (ordinal("Chicago"), reduction("Chicago"), revred("Chicago")) == (46, 37, 35)
assert reduction("Thursday") == 35
assert reverse("Rhamondre Stevenson") == 257 and ordinal("Thursday Night Football") == 257
# no single cipher gives both 35s
assert not (reduction("Chicago") == 35 and reduction("Thursday") == 35)
assert not (revred("Chicago") == 35 and revred("Thursday") == 35)

st = wb["Rhamondre Stevenson Reconstruction"]
rows = {r: (int(st.cell(r, 2).value), int(st.cell(r, 3).value)) for r in range(15, 22)}
reg = [rows[r] for r in (15, 16, 17, 18, 19, 21)]
reg_rush = sum(a for a, b in reg); reg_rec = sum(b for a, b in reg)
assert (reg_rush, reg_rec) == (30, 4), (reg_rush, reg_rec)   # 34 regular season pregame
assert rows[20] == (0, 1)                                    # postseason TD
assert (28, 4) == (sum(rows[r][0] for r in range(15, 20)), sum(rows[r][1] for r in range(15, 20)))

# ---------- Universe recount (asserted) ----------
h = wb["WCF Historical Post Universe"]
rel = collections.Counter()
for r in range(1, h.max_row + 1):
    v = h.cell(r, 4).value
    if v in ("Yes", "Possible") or (isinstance(v, str) and v.startswith("No")):
        rel["No" if v.startswith("No") else v] += 1
assert dict(rel) == {"Yes": 45, "Possible": 1, "No": 2}, rel

LOG = []   # (register, sheet, cell, v4.1 value, v4.2 value, reasoning, source+limitation, class)

def edit(rid, sheet, cell, old, new, reason, source, cls, whole=False):
    ws = wb[sheet]
    v41 = orig[sheet][cell].value
    cur = ws[cell].value
    prior = [i for i, l in enumerate(LOG) if l[1] == sheet and l[2] == cell]
    if not prior: assert cur == v41, f"cell already changed {sheet}!{cell}"
    if whole or old is None:
        if old is not None: assert str(cur) == old, f"whole-cell mismatch {sheet}!{cell}: {cur!r}"
        newv = type(cur)(new) if isinstance(cur, (int, float)) else new
    else:
        assert isinstance(cur, str) and cur.count(old) == 1, f"substring not unique/found {sheet}!{cell}: {old!r}"
        newv = cur.replace(old, new)
    ws[cell].value = newv
    ws[cell].alignment = Alignment(wrap_text=True, vertical="top")
    if prior:   # second edit to same cell: merge into one audit row (v4.1 value stays exact original)
        o = LOG[prior[0]]
        LOG[prior[0]] = (o[0] + " + " + rid, sheet, cell, v41, newv, o[5] + " | " + reason, o[6] + " || " + source, o[7] if o[7] == cls else o[7] + " / " + cls)
    else:
        LOG.append((rid, sheet, cell, v41, newv, reason, source, cls))

FC, SQ, PV, UC = "factual correction", "scope qualification", "provenance correction", "unresolved conflict"
S = "Rhamondre Stevenson Reconstruction"; M = "Cross-Post Methodology Matrix"; L = "Public WCF Claims Ledger"
C = "Nico Collins Reconstruction"; E = "Eagles Giants Reconstruction"; P = "Panthers Packers Reconstruction"
B = "Bears Seahawks Reconstruction"; MS = "DJ Moore Source Audit"; MR = "DJ Moore Reconstruction"
N = "Bo Nix Uploaded Slide Audit"; K = "Travis Kelce #87 Symbolic Audit"; CH = "Ja'Marr Chase Reconstruction"
U = "Universe Summary"

# ---- D-01 Stevenson cipher label ----
src1 = "Recomputed in audit-5 / v4.2 build script: Chicago Ordinal 46, Reduction 37, Reverse Reduction 35; Thursday Reduction 35; Stevenson Reverse 257; Thursday Night Football Ordinal 257. Arithmetic only; WCF's own cipher label for Chicago was not visible."
edit("D-01", S, "B7", None, "Chicago Reverse Reduction = 35 (Reduction = 37; Ordinal = 46).",
     "v4.1 labeled the 35 as Reduction; Reduction is 37. The value 35 reproduces under Reverse Reduction.", src1, FC, whole=True)
edit("D-01", S, "C7", "EXACT", "EXACT UNDER REVERSE REDUCTION (not Reduction)",
     "Status text qualified to the cipher under which the value reproduces. Linked to B7.", src1, SQ, whole=True)
edit("D-01", S, "D7", "Reduction cipher; A=1..Z=26, each letter reduced to 1–9.",
     "Reverse Reduction cipher; reverse A=26..Z=1, each letter's reverse value reduced to 1–9, then summed.",
     "Convention cell must match B7. Linked to B7.", src1, FC, whole=True)
edit("D-01", M, "H15", "Chicago Reduction 35", "Chicago Reverse Reduction 35",
     "Same cipher-label error propagated to the matrix.", src1, FC)
edit("D-01", S, "A37", "WCF's ciphers reproduce exactly.",
     "WCF's cipher values reproduce, but not under one cipher: Chicago = 35 under Reverse Reduction (Reduction is 37); Thursday = 35 under Reduction; Stevenson = 257 under Reverse; Thursday Night Football = 257 under Ordinal. No single cipher yields both 35s.",
     "Replaces 'reproduce exactly' with per-cipher statement. Linked to D-01 and D-04.", src1, SQ)

# ---- D-04 Stevenson TD scope ----
src4 = "NFL.com season career table (28 rushing + 4 receiving through 2025), NFL.com 2026 log (rushing TDs Oct. 4, Oct. 11), Feb. 8, 2026 postseason receiving TD. Ledger sums recomputed in build script from rows 15–21."
edit("D-04", S, "A26",
     "Add the Feb. 8, 2026 postseason receiving TD and the Oct. 4/11, 2026 regular-season rushing TDs = 35 total across regular season + postseason before the Oct. 22 game. Therefore WCF's #35 is correct only when postseason TDs are included. If strictly regular-season only, the pregame total is 34 and the Oct. 22 TD would be #35.",
     "Add the Oct. 4/11, 2026 regular-season rushing TDs = 34 regular-season TDs before the Oct. 22 game, so the Oct. 22 TD would be regular-season #35 (WCF's #35 reproduces under regular-season-only counting). If the Feb. 8, 2026 postseason receiving TD is also counted, the combined pregame total is 35 and the Oct. 22 TD would be #36 (WCF's #35 does not reproduce under that convention).",
     "v4.1 reversed the scope: #35 holds for regular-season-only (34 pregame), not for regular season + postseason (35 pregame, next #36).", src4, FC)
edit("D-04", S, "A37",
     "The 35th-career-TD milestone is supported if the count includes the Feb. 8, 2026 postseason touchdown; under regular-season-only counting the target touchdown would also be #35.",
     "The #35 milestone reproduces under regular-season-only counting (34 pregame); if the Feb. 8, 2026 postseason touchdown is included, the pregame total is 35 and the target touchdown would be #36.",
     "Same reversed-scope error as A26. Second edit to this cell (first edit is D-01).", src4, FC)
edit("D-04", S, "E23", "See note below: career total #35 depends on whether NFL career stat total includes postseason.",
     "Under this combined count the pregame total is 35, so the Oct. 22 TD would be #36, not #35. See note below.",
     "Linked cell carrying the same reversed-scope claim.", src4, FC)
edit("D-04", S, "C22", "6", "4", "Receiving TD total in the regular-season-only ledger row: 0+1+0+1+2+0 = 4, not 6.", src4, FC, whole=True)
edit("D-04", S, "D22", "36", "34", "Total = 30 rushing + 4 receiving = 34 (matches the sheet's own B9 and E22 text).", src4, FC, whole=True)
edit("D-04", S, "C23", "7", "5", "Combined-row receiving TDs: 4 regular season + 1 postseason = 5.", src4, FC, whole=True)
edit("D-04", S, "D23", "37", "35", "Combined total = 30 rushing + 5 receiving = 35 (matches E23 text).", src4, FC, whole=True)

# ---- D-02 Collins DOB ----
src2 = "ESPN, Ourlads, Wikipedia, Pro-Football-Reference list 3/19/1999: four citations, independence not established; official Texans bio not retrieved. 2026-11-19 to 2027-03-19 = 120 calendar days (arithmetic verified)."
edit("D-02", "DOB Verification", "C2", "Not verified in official bio during this pass",
     "Not verified in official bio during this pass. v4.2 note: DOB 3/19/1999 appears in four public citations (ESPN, Ourlads, Wikipedia, Pro-Football-Reference); independence not established; official Texans bio not retrieved.",
     "Sheets conflict (B9 states DOB; this sheet says not verified): both retained, provenance stated.", src2, PV, whole=True)
edit("D-02", C, "B9", "difference = 120 days",
     "difference = 120 days (arithmetic reproduces given this DOB; DOB itself rests on four public citations, independence not established, no official bio)",
     "Arithmetic status separated from source status.", src2, SQ)
edit("D-02", C, "D9", "birthday source verified by Football Database",
     "v4.1 text: 'birthday source verified by Football Database.' v4.2: that verification is not independently established; see DOB Verification C2.",
     "v4.1 'verified' wording conflicts with DOB Verification sheet. Original wording preserved inside the new text.", src2, PV)

# ---- D-03 Collins home appearances ----
src3 = "NFL.com situational splits (regular season 7, 4, 9, 6, 7 + 3 in 2026 = 36). 2023/2024 postseason home appearances not verified."
edit("D-03", C, "A39", "this is the convention required to reproduce the claim.",
     "this is the convention required to reproduce the claim. Regular-season count of 36 reproduces (7+4+9+6+7+3 per NFL.com situational splits); the +2 postseason home appearances (2023, 2024) were not verified, so the 39th is conditional on both the convention and an unverified postseason count.",
     "Scope qualification; arithmetic, source and convention statuses separated.", src3, SQ)
edit("D-03", M, "G8", "39th career home appearance only if postseason included",
     "39th career home appearance only if postseason included; regular-season 36 reproduces, +2 postseason unverified",
     "Linked to A39.", src3, SQ)

# ---- D-05 Eagles–Giants meetings ----
src5 = "Giants.com/NFL capsules 182 (regular season); sportsbrackets 184 (regular season); Wikipedia mirrors 185 (early 2024); current Wikipedia total 190. Inclusion rules and cutoffs differ or are unstated; none ranked."
edit("D-05", E, "B13", "and whether postseason games are included.",
     "and whether postseason games are included. Four public counts are preserved without ranking: 182 (Giants.com/NFL capsules, regular season), 184 (sportsbrackets, regular season), 185 (Wikipedia mirrors, early 2024), 190 (current Wikipedia total).", "Adds the four counts.", src5, UC)
edit("D-05", E, "D13", "WCF says 184 all-time; official NFL pregame source confirms 182 regular-season meetings.",
     "WCF says 184 all-time; the NFL/Giants pregame source gives 182 regular-season meetings, while another public source (sportsbrackets) also lists 184 regular-season meetings. WCF's 184 is therefore not refuted.",
     "v4.1 implied 184 was contradicted; it is not.", src5, UC)
edit("D-05", E, "A36", "is not reconciled with the NFL's official pregame figure of 182 regular-season meetings;",
     "is not reconciled with the NFL's official pregame figure of 182 regular-season meetings (public sources give 182, 184, 185 and 190; 184 not refuted);",
     "Linked to B13/D13.", src5, UC)
edit("D-05", L, "G12", "WCF's 184/185 count not reconciled;", "WCF's 184/185 count not reconciled (public sources give 182, 184, 185, 190; not refuted);", "Linked.", src5, UC)
edit("D-05", M, "L14", "WCF 184/185 count unreconciled;", "WCF 184/185 count unreconciled (sources give 182/184/185/190; not refuted);", "Linked.", src5, UC)

# ---- D-06 Panthers ordinal ----
src6 = "CBS/NFL.com schedule: weeks 1–7 = 107 games, so Panthers–Packers is the reconstructed 108th. 103 is the 27th prime (arithmetic fact)."
edit("D-06", P, "D8", "Do not silently accept 103 as a verified game ordinal.",
     "Do not silently accept 103 as a verified game ordinal. 103 is the 27th prime, preserved as a separate numerical coincidence, not a game count.",
     "Keeps the coincidence separate from the contradicted count.", src6, SQ)

# ---- D-07 Bears ATS ----
src7 = "WCF slide 3: 2–6 ATS; NBC Sports pregame trends (10/29/2026 9:30 PM): Seattle 8–6–2 ATS as home favorite. Windows, venue filters and favorite/underdog definitions of both figures unknown. NFC 3–7 split: no public source found."
edit("D-07", B, "B20", "NBC Sports' pregame trend table reports Seattle 8–6–2 ATS as a home favorite with Macdonald.",
     "NBC Sports' pregame trend table (10/29/2026 9:30 PM) reports Seattle 8–6–2 ATS as a home favorite with Macdonald. Date windows, venue filters and favorite/underdog definitions of both figures are unknown, so the comparison is not normalized: 2–6 is unverified, not disproved.",
     "Both figures retained with their windows.", src7, UC)
edit("D-07", M, "L21", "Macdonald home-favorite 2-6 conflicts with NBC 8-6-2;",
     "Macdonald home-favorite 2-6 (WCF) vs NBC 8-6-2 (10/29/2026): windows/definitions unaligned, 2-6 unverified not disproved;", "Linked.", src7, UC)
edit("D-07", L, "G25", "Macdonald 2-6 home-favorite conflicts with NBC 8-6-2;",
     "Macdonald 2-6 home-favorite (WCF) vs NBC 8-6-2 (10/29/2026): windows/definitions unaligned, 2-6 unverified not disproved;", "Linked.", src7, UC)

# ---- D-08/D-09/D-10 Collins postgame ----
src8 = "NFL.com log shows W 26–3 for both the 10/11 and 11/19/2026 games (anomaly). Box score not opened; PFR box score request denied and not retried. Undated NFL.com 42-yard highlight is not corroboration."
edit("D-08", C, "D43", "Houston won 26–3.",
     "NFL.com log lists W 26–3 for Houston, but the same 26–3 appears for both Oct. 11 and Nov. 19, 2026. Final score unconfirmed (box score not opened).",
     "Score stays unconfirmed per register.", src8, UC, whole=True)
edit("D-08", C, "D44", "NFL final individual statistics and game recap confirm the score.",
     "v4.1 text: 'NFL final individual statistics and game recap confirm the score.' v4.2: the score is not independently confirmed; see D43.",
     "Linked cell asserted score confirmation; D-08 keeps it unconfirmed. Original wording preserved.", src8, UC, whole=True)
edit("D-09", C, "B44", "1 receiving TD.",
     "1 receiving TD. (Receiving TD reproduced from NFL.com log; the 42-yard length and Q2 timing are not independently confirmed.)",
     "Length unconfirmed per register D-09.", src8, UC)
edit("D-09", C, "C44", "OFFICIALLY VERIFIED",
     "TD EVENT REPRODUCED (NFL.com log); 42-YARD LENGTH UNCONFIRMED",
     "'OFFICIALLY VERIFIED' not supported for the 42-yard detail.", src8, UC, whole=True)
edit("D-09", C, "D49", "Scoring table identifies Nico Collins 42-yard pass from C.J. Stroud.",
     "Scoring table identifies Nico Collins 42-yard pass from C.J. Stroud. [v4.2: this entry was not independently retrieved in the audit; 42-yard length unconfirmed (D-09).]",
     "Source cell annotated, original retained.", src8, UC, whole=True)
src10 = "No timestamped pre-kickoff WCF record exists in the workbook or the thread. Event accuracy (#30 TD) is reproduced separately from NFL.com game log."
edit("D-10", C, "C45", "HIT",
     "EVENT OCCURRED (#30 under regular-season receiving-TD scope); PRE-GAME PROVENANCE NOT ESTABLISHED — 'HIT' label withdrawn",
     "A hit requires a pregame-timestamped record; none exists here.", src10, PV, whole=True)
edit("D-10", M, "K8", "Reconstructed with definition caveat",
     "Reconstructed with definition caveat; pregame provenance not established", "Linked.", src10, PV, whole=True)
edit("D-10", "Read Me", "B57", "confirms the pregame #30 career regular-season receiving TD milestone forecast. Classified as a hit for this event; no global methodology validation implied.",
     "shows a receiving TD (NFL.com log) that is the #30 career regular-season receiving TD under the stated scope; the 42-yard length is unconfirmed (D-09) and whether the #30 claim was recorded before kickoff is not established (D-10), so it is not classified as a hit. No methodology validation implied.",
     "Provenance wording; removes 'confirms ... forecast' and 'hit'.", src10, PV)
edit("D-10", C, "B46", "The central career receiving-TD milestone forecast occurred in the target game.",
     "The #30 career receiving-TD milestone event occurred in the target game; whether it was recorded before kickoff is not established (D-10).", "Linked wording.", src10, PV, whole=True)
edit("D-10", C, "D46", "This verifies the event forecast for this single case.",
     "This reproduces the event for this single case (pregame provenance not established).", "Linked wording.", src10, PV)

# ---- D-11 Moore ----
src11 = "NFL.com 2025 game log lists two postseason receiving TDs: 1/10/2026 vs GB (AP/Tribune/ESPN corroborate) and 1/18/2026 vs LAR (NFL.com log only). 44 regular + 2 postseason = 46; next #47."
edit("D-11", MS, "D8", "If postseason is included, his Jan. 18, 2026 playoff TD raises the pregame total to 45, so the next combined regular-season + postseason TD would be #46.",
     "If postseason is included, his two 2025-season playoff TDs (Jan. 10 and Jan. 18, 2026) raise the pregame total to 46, so the next combined regular-season + postseason TD would be #47.", "45/#46 → 46/#47.", src11, FC)
edit("D-11", MS, "B16", "combined regular season + postseason baseline is 45 because the Jan. 18 playoff TD is included.",
     "combined regular season + postseason baseline is 46 because two playoff TDs (Jan. 10 and Jan. 18, 2026) are included.", "Linked.", src11, FC)
edit("D-11", MR, "C9", "Including the Jan. 18, 2026 postseason receiving TD, combined baseline = 45.",
     "Including the two postseason receiving TDs (Jan. 10 vs GB and Jan. 18, 2026 vs LAR), combined baseline = 46 (next would be #47).", "45 → 46.", src11, FC)
edit("D-11", M, "C19", "postseason-inclusive baseline is 45, so next would be #46", "postseason-inclusive baseline is 46, so next would be #47", "Linked.", src11, FC)

# ---- Moore AFC count (unresolved ±1) ----
srcA = "2019/2020 DJ Moore game-log refetch returned an unrendered template; AFC counts hand-transcribed and flagged unverified (errata-3, nfl_com_extracts_part3 CSV)."
edit("D-11b", MR, "C8", "before treating exact count as fully verified.",
     "before treating exact count as fully verified. v4.2: unresolved ±1 (2019/2020 logs not re-retrieved; AFC counts hand-transcribed).", "Unresolved, not decided.", srcA, UC)
edit("D-11b", M, "F19", "(count audit pending)", "(count audit pending; unresolved ±1)", "Linked.", srcA, UC)

# ---- D-12 Nix venue ----
src12 = "Venue: Empower Field at Mile High, Denver — seahawks.com, denverbroncos.com, Fox Sports event info, ticket listings; NFL.com row shows no '@'. The 36 home points are conditional on the stated definition (6 home rushing TDs × 6); other scoring not checked. 36 + 6 = 42 (arithmetic)."
edit("D-12", N, "B3", "Denver Broncos at Seattle Seahawks", "Seattle Seahawks at Denver Broncos", "Header venue reversed in v4.1.", src12, FC)
edit("D-12", N, "C10", "The target game is at Seattle, away from Denver. A touchdown in this game cannot increase Nix's home-points total.",
     "The target game was at Denver (home for Nix). A touchdown (6 points) would take 36 career home points to 42; the 36 is conditional on the stated definition (home rushing TDs only) and was not independently verified for other scoring.",
     "v4.1 location error withdrawn.", src12, FC, whole=True)
edit("D-12", N, "D10", "INTERNAL LOGIC CONFLICT", "REPRODUCED — CONDITIONAL ON POINTS DEFINITION (36 + 6 = 42)",
     "Conflict arose from the wrong venue.", src12, FC, whole=True)
edit("D-12", N, "E10", "This is a material location/definition issue. Do not mark the claimed 42 home points as a valid pregame milestone for this road game.",
     "v4.1 venue error corrected (home game). Remaining issue: the definition of 'home points' and the source of the 36 are not established in the slides.",
     "Withdraws the invalid-milestone instruction.", src12, SQ, whole=True)
edit("D-12", N, "A18", "the 42-home-points claim conflicts with the game being played away at Seattle;",
     "the 42-home-points claim reproduces at the home game in Denver conditional on the points definition (v4.1 incorrectly placed the game at Seattle);", "Linked.", src12, FC)
edit("D-12", M, "G11", "42nd career game; home-points claim conflicts with game being at Seattle",
     "42nd career game; game at Denver (home); 42 home-points claim reproduces (36+6) conditional on the points definition", "Linked.", src12, FC, whole=True)
edit("D-12", L, "G9", "42 home points conflicts with road game;", "42 home points reproduces at Denver home game conditional on points definition (v4.1 venue error corrected);", "Linked.", src12, FC)

# ---- D-13 / D-14 Kelce ----
src13 = "NFL.com game logs 2019 (12/8 @NE), 2021 (11/21 DAL), 2026; StatMuse total 2 rushing; RotoWire 'second career rushing TD' (2021). NFL.com career page shows 3 only if it includes the 11/8/2026 vs NYJ rushing TD (post-cutoff) — candidate explanation, not established. StatMuse 85 through 2025 includes one unverified 2014 'RET TD'; Wikipedia 86 is stamped as of Week 9 2026."
edit("D-13", K, "B10", "3 regular-season rushing TDs through 2025.", "2 regular-season rushing TDs through 2025 (2019, 2021). NFL.com's career page shows 3 only if it includes the 11/8/2026 rushing TD (post-cutoff); that is a candidate explanation, not established.", "Count correction.", src13, FC)
edit("D-13", K, "B12", "82 receiving + 3 rushing through 2025 = 85; add 2 receiving TDs in 2026 = 87 total regular-season TDs through October 18.",
     "82 receiving + 2 rushing through 2025 = 84; add 2 receiving TDs in 2026 = 86 total regular-season TDs through October 18. v4.1 stated 3 rushing and 87.", "82+2+2 = 86.", src13, FC, whole=True)
edit("D-13", K, "C12", "EXACT UNDER REGULAR-SEASON TOTAL-TD DEFINITION", "NOT REPRODUCED UNDER REGULAR-SEASON TOTAL-TD DEFINITION (86, not 87)", "Linked status.", src13, FC, whole=True)
edit("D-13", K, "D12", "The 87 requires adding receiving and rushing TDs and excluding postseason. Receiving-only total is 84.",
     "Adding regular-season receiving and rushing TDs through October 18 gives 86, not 87. Receiving-only total is 84. A route to 87 exists only via StatMuse's all-TD count (82 receiving + 2 rushing + one 2014 'RET TD' = 85 through 2025, plus 2), and that 2014 item is unverified (D-14); Wikipedia's 86 is stamped as of Week 9 2026, a later cutoff.",
     "D-13 and D-14 together; both routes preserved.", src13, UC)
edit("D-14", K, "B17", "The numerical coincidence reproduces under one explicit scope: Kelce's regular-season receiving + rushing touchdowns through October 18, 2026 total 87, matching his jersey number. It does not reproduce as receiving-only (84), and postseason inclusion changes the total. This is a verified symbolic association, not a demonstrated predictive method.",
     "The numerical coincidence does not reproduce under the workbook's stated decomposition: regular-season receiving + rushing touchdowns through October 18, 2026 total 86. A route to 87 exists only through StatMuse's all-TD count including an unverified 2014 non-offensive TD. It does not reproduce as receiving-only (84), and postseason inclusion changes the total. This is an unverified symbolic association, not a demonstrated predictive method.",
     "'Verified' withdrawn.", src13, UC, whole=True)
edit("D-13", M, "H20", "Career regular-season TDs = 87 (82 receiving + 3 rushing through 2025, plus 2 receiving in 2026)",
     "Career regular-season receiving + rushing TDs = 86 (82 receiving + 2 rushing through 2025, plus 2 receiving in 2026); WCF's 87 reproduces only via an unverified StatMuse count (D-14)", "Linked.", src13, FC, whole=True)
edit("D-13", M, "L20", "87 depends on combined regular-season TD scope;", "87 not reproduced under combined regular-season scope (86);", "Linked.", src13, FC)
edit("D-13", M, "K20", "Symbolic association reproduced; no predictive test", "Symbolic association not reproduced under workbook decomposition (86); 87 only via unverified StatMuse route; no predictive test", "Linked status.", src13, UC, whole=True)
edit("D-13", L, "G24", "87 = 82 receiving + 3 rushing through 2025 + 2 receiving in 2026;", "82 receiving + 2 rushing through 2025 + 2 receiving in 2026 = 86 (WCF 87 reproduces only via unverified StatMuse count, D-14);", "Linked.", src13, FC)
edit("D-13", L, "D24", "SYMBOLIC ASSOCIATION VERIFIED UNDER REGULAR-SEASON TOTAL-TD SCOPE; PAID CARD INACCESSIBLE",
     "SYMBOLIC ASSOCIATION NOT REPRODUCED UNDER WORKBOOK DECOMPOSITION (86); 87 ONLY VIA UNVERIFIED STATMUSE ROUTE; PAID CARD INACCESSIBLE", "Linked classification.", src13, UC, whole=True)

# ---- D-15 Chase ----
src15 = "NFL.com logs 2021–25 list 41 home rows; 2022 has 4 no-stat rows (GP 12), one home; 2023 shows 17 rows vs GP 16. → 39–40 played through 2025, +2 in 2026, Titans 11/1 is the 42nd–43rd. StatMuse snapshot of 40 through 2025 not re-fetched."
edit("D-15", CH, "B18", "Tennessee game would be #43.",
     "Tennessee game would be #43. v4.2: unresolved ±1 — NFL.com home rows 2021–25 give 39–40 played through 2025 (41 listed, minus 2022 non-appearance rows and one possible 2023 non-appearance), +2 in 2026, so the Titans game is the 42nd–43rd.", "Unresolved, not decided.", src15, UC)
edit("D-15", CH, "C18", "RECONSTRUCTED — REGULAR SEASON", "UNRESOLVED ±1 (42nd–43rd) — REGULAR SEASON", "Status linked to B18.", src15, UC, whole=True)
edit("D-15", CH, "D18", "Excludes postseason.", "Excludes postseason. The StatMuse 40 is not reconciled to NFL.com rows (see B18).", "Linked.", src15, UC)
edit("D-15", CH, "D29", "40 regular-season home games in career at 2025-season snapshot",
     "40 regular-season home games in career at 2025-season snapshot (not reconciled to NFL.com rows; D-15)", "Linked.", src15, UC, whole=True)
edit("D-15", CH, "A35", "All visible Ja'Marr Chase slide claims are reproducible under the stated conventions. The 59-to-60 career TD count, date intervals, and ciphers match. The 43rd home-game count reconstructs using regular-season appearances only.",
     "Most visible Ja'Marr Chase slide claims reproduce under the stated conventions. The 59-to-60 career TD count, date intervals, and ciphers match. The 43rd home-game count reconstructs only from the StatMuse 40-through-2025 snapshot; NFL.com game-log rows give the 42nd–43rd (unresolved ±1, D-15).",
     "Summary overstated reproducibility.", src15, UC)
edit("D-15", M, "G12", "43rd regular-season home game", "43rd regular-season home game (WCF); reconstructed 42nd–43rd, unresolved ±1 (D-15)", "Linked.", src15, UC, whole=True)

# ---- ChatGPT review round 2 (approved adjustments) ----
srcR="ChatGPT review of v4.2 draft (relayed by Nick, 2026-11-20); register D-10, D-11b, D-12, D-15."
edit("D-10", C, "C46", "SUCCESSFUL EVENT PREDICTION", "EVENT OCCURRED; PREGAME PROVENANCE NOT ESTABLISHED", "C46 and B47 contradicted D-10.", src10, PV, whole=True)
edit("D-10", C, "B47", "All milestone inputs were defined before the November 19 game.",
     "The timestamped pregame WCF record was not located; the reconstruction used a pre-Nov. 19 cutoff, but pregame provenance of the claim is not established (D-10).", "Provenance statement.", src10, PV, whole=True)
edit("D-11b", M, "G19", "39th career AFC game; home TD interval",
     "38 prior AFC games, provisional ±1; target would be #39 if the count holds. Home TD interval separately reproduced.", "Unqualified exact ordinal removed.", srcA, UC, whole=True)
edit("D-12", M, "K11", "Partial reconstruction with internal discrepancies",
     "Partial reconstruction; home-points claim reproduced conditionally; elapsed-day count mismatch (18 vs 19) and missing slide 4 remain; 42nd-game denominator not independently audited", "Status wording only; Partial kept.", src12, SQ, whole=True)
m=wb[M]; r=m.max_row+1
m.cell(r,1).value="v4.2 note on case-count tables"
m.cell(r,2).value="The mechanism tables count cases where a feature family is present, not whether each specific count is verified. Chase (ordinal unresolved 42nd–43rd) and DJ Moore (AFC count unresolved ±1) remain counted as feature-present; claim-level status is in each reconstruction sheet."
for c_ in (1,2): m.cell(r,c_).alignment=Alignment(wrap_text=True,vertical="top")
LOG.append(("D-15/D-11b",M,f"A{r}:B{r}","(empty row)",m.cell(r,2).value,"Feature presence vs claim-level verification.",srcR,SQ))

# ---- D-16 Universe Summary ----
src16 = "Independent recount from the 'WCF Historical Post Universe' sheet in audit-5 (Universe Summary recount): 48 records; Public 17 (12 with an identifiable NFL selection); Locked 26; unresolved 5; NFL relevance 45 Yes / 1 Possible / 2 No (the Yes/Possible/No split re-asserted in the build script). Archive classification only; no result or hit-rate implication."
edit("D-16", U, "B4", "NFL-related archive entries recorded: 48 total entries, including",
     "48 total archive records, including", "Label said NFL-related for all 48; 3 are Possible/No.", src16, FC)
edit("D-16", U, "B5", "Entries explicitly marked Public: 11.", "Entries explicitly marked Public: 17 (archive classification only). The 12 with an identifiable NFL selection are listed on a separate line below.", "11 → 17.", src16, FC)
edit("D-16", U, "B6", "Entries explicitly marked Locked: 25.", "Entries explicitly marked Locked: 26.", "25 → 26.", src16, FC)
edit("D-16", U, "B7", "Remaining access states: 12 entries are", "Remaining access states: 5 entries are", "12 → 5.", src16, FC)
edit("D-16", U, "B8", "Possible: 2. No (non-NFL control): 1.", "Possible: 1. No: 2.", "2/1 → 1/2.", src16, FC)

# new row on Universe Summary (append; no existing cell moved)
u = wb[U]
r = u.max_row + 1
u.cell(r, 1).value = "Public posts with an identifiable NFL selection (separate line, v4.2)"
u.cell(r, 2).value = "12 (Eagles, Brian Thomas Jr., Bears, Chase, Panthers, Stevenson, Nix, Kmet, Hurts, Lamb, Moore, Freiermuth). Archive classification only; does not imply a decode was visible or any result."
for c in (1, 2): u.cell(r, c).alignment = Alignment(wrap_text=True, vertical="top")
LOG.append(("D-16", U, f"A{r}:B{r}", "(empty row)", u.cell(r, 2).value, "New line; no existing cell shifted.", src16, FC))

# ---- Read Me log row ----
rm = wb["Read Me"]
rr = rm.max_row + 1
rm.cell(rr, 1).value = "v4.2 DRAFT update"
rm.cell(rr, 2).value = ("Draft created as a copy of v4.1 (SHA-256 79bd35461e320bc7b4533b9d69bd8fc79b1d470636c6015f1a390b8709611580). "
                        "Applies the approved correction register D-01 to D-16; every changed cell is listed in the 'Audit Trail' sheet with v4.1 value, v4.2 value, reasoning, source/limitation and classification. "
                        "Original WCF claims are preserved; no unrelated content was changed. Research artifact only; not connected to any betting model.")
for c in (1, 2): rm.cell(rr, c).alignment = Alignment(wrap_text=True, vertical="top")
LOG.append(("—", "Read Me", f"A{rr}:B{rr}", "(empty row)", rm.cell(rr, 2).value, "Version note.", "—", "provenance correction"))

# ---- split paired-cell log entries into one row per cell ----
_new=[]
for e in LOG:
    if ":" in e[2]:
        sh=e[1]; a,b=e[2].split(":")
        for cc in (a,b):
            _new.append((e[0],sh,cc,"(empty cell)",wb[sh][cc].value,e[5],e[6],e[7]))
    else: _new.append(e)
LOG[:]=_new

# ---- Audit Trail sheet ----
at = wb.create_sheet("Audit Trail")
hdr = ["#", "Register ID", "Sheet", "Cell", "v4.1 value (exact)", "v4.2 value (exact)", "Calculation / reasoning", "Supporting source and limitation", "Change classification"]
at.append(hdr)
for i, e in enumerate(LOG, 1):
    at.append([i, e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7]])
for c in at[1]: c.font = Font(bold=True)
for col, w in zip("ABCDEFGHI", (5, 10, 30, 10, 60, 60, 45, 60, 22)): at.column_dimensions[col].width = w
for row in at.iter_rows(min_row=2):
    for c in row: c.alignment = Alignment(wrap_text=True, vertical="top")
at.freeze_panes = "A2"

import os; os.makedirs("/home/claude/out", exist_ok=True)
wb.save(OUT)

# ---------- diff verification: only logged cells differ ----------
chk = openpyxl.load_workbook(OUT)
logged = {(e[1], e[2]) for e in LOG}
bad = 0
for ws in orig:
    for row in ws.iter_rows():
        for c in row:
            n = chk[ws.title][c.coordinate].value
            if n != c.value and (ws.title, c.coordinate) not in logged:
                bad += 1; print("UNLOGGED CHANGE", ws.title, c.coordinate)
print("edits logged:", len(LOG), "| unlogged changes:", bad)
print("sheets:", len(orig.sheetnames), "->", len(chk.sheetnames))
