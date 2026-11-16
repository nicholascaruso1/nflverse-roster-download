# NFL Player Prop Model v2.2: Week 10 Sunday 4:05/4:25 PM ET slate (SEA@LV, LAR@ARI, SF@DAL)

Prepared pregame, Sun Nov 15 2026, from Hard Rock-style app screenshots stamped 3:05-3:08 PM ET (app assumed to be Hard Rock, same as prior locks). Kept separate from the Bet Model. Architecture and weights unchanged (v2.2 frozen; the approved calibration branch changed no parameters). Statuses: PLAY / LEAN / WATCH / PASS / VOID. **Full official inactive lists were NOT retrieved for any of the six teams (see section 3), and SEA@LV and LAR@ARI each have a quarterback with little or no sample (SF@DAL does not: Purdy 8 starts, Prescott 9), so Opportunity and Scenario Confidence are capped at Medium.** The pilot v0.1 probabilities in section 6 were computed AFTER seeing these prices (not a blind pre-registration). One consolidated file by design (card and pilot probabilities together).

## 1. Result (read this first)
- **PLAY: none.** Nothing is Level A: the pilot method is unvalidated and no PLAY can come from it.
- **LEAN (3), all Level B, Data Quality Medium or better:**
  1. **Konata Mumpfield (LAR) UNDER 2.5 receptions (-150)**
  2. **Javonte Williams (DAL) UNDER 2.5 receptions (+120)**
  3. **Ashton Jeanty (LV) UNDER 36.5 rush yards (-115)**
  They do not share a mechanism, but all three sit inside games where one team is a clear underdog or a shootout is priced (SF@DAL total 55.5), so a script that forces extra volume would hurt each in its own way (section 7).
- **WATCH (17; corrected from 14, see Errata):** Higbee U3.5 rec, Parkinson U3.5 rec, Atwell U2.5 rec, Davis Allen U1.5 rec, Corum U58.5 rush, Stafford O209.5 pass yds (LAR@ARI); Higgins U2.5 rec, Virgil U2.5 rec, Fehoko U1.5 rec, Knight U33.5 rush (ARI); Horton O0.5 rec, Mayer O2.5 rec, Nailor O1.5 rec, Charbonnet U63.5 rush, Lock U5.5 rush (SEA@LV); Prescott U1.5 pass TD, Spann-Ford U2.5 rec (SF@DAL). Section 5 says why none was promoted.
- **PASS / Level C:** everything else screened, including every prop for **Carson Beck (ARI)** and **Fernando Mendoza (LV)** (no NFL sample), **Keenan Allen (SF)** (no 49ers sample). **No quantified TD edge** (no recorded pregame probability, Addendum B). Receiving-yard props are not modeled.
- **No parlay. No numeric joint probability.**
- **Calibration caveat (source: `claude/prop-model-v0.1-calibration-audit.md`; the subgroup gaps were defined after viewing overall results, so they are exploratory, not validated findings):** the audit found the pilot overconfident by about 5 to 8 points on low-volume receiver Unders, QB rush Unders and pass-yard Unders. Mumpfield's Under is the only LEAN in that family. Its pilot 86.5% is shown unadjusted; a 5 to 8 point haircut still leaves it well above the 60.0% break-even. Higbee was held to WATCH partly because the same haircut leaves his stability margin near zero.
- Most of the board is Under-leaning in my pilot output. That is a property of the unvalidated method (no matchup or game-script term, Poisson and negative-binomial shapes) as much as of the market. Only 3 of about 70 modeled props were promoted.

## 2. Data and availability audit
- Usage and logs: my computation from nflverse 2026 play-by-play (weeks 1-10, 24,002 plays; week 10 holds only WAS @ NYG). Snap counts (nflverse snap_counts_2026) define active weeks (offense snaps > 0 or recorded involvement). Rosters from nflverse roster_2026 (week 10 status field). **Only games with the player's CURRENT team are used**, so a player's earlier-team games never enter his sample.
- Prices: screenshots, 3:05-3:08 PM ET (19 images: touchdowns, passing, rushing, receiving, receptions boards), read by me. Any row hidden behind the nav bar, plus defense, kicker and alt-line markets, is unread.
- **Game lines are NOT in these screenshots.** Implied points use the Hard Rock 11:40 AM lines from the Lock 2 Bet Model card (may have moved): SEA -6.5 / 40.5 (SEA 23.5, LV 17.0); LAR -9 (-115) / 38.5 (LAR 23.75, ARI 14.75); SF -4 / 55.5 (SF 29.75, DAL 25.75). Weather not checked.
- Model definitions, same as the Week 10 1 PM card: league 2026 ypc 4.33 (QB carries 5.56), 6.23 yds per pass attempt (dropbacks including sacks, sack yards netted), pass TDs per point 0.0660. **Disclosed definition gap:** books settle passing yards gross of sack yardage, so my net-of-sacks distribution understates yards slightly. A diagnostic gross-yardage run (not used for statuses) is in the workspace and did not change any LEAN. QB kneel-downs are excluded from my rushing data but count in official stats; kneels only lower QB rush yardage.
- Validation: the new script reproduced the earlier card on Young U9.5 rush (carEW 0.78, ypc 5.80, adj 1.053, P(Over) 18.6% vs 18.5%) and Penix U219.5 pass (attEW 30.0, ypa 6.55, adj 0.971, 32.0% vs 32.0%). Bijan U3.5 rec (57.7% vs 58.0%) and Pitts U3.5 rec (58.8% vs 59.3%) agree within simulation noise.

## 3. Availability and quarterbacks (V = verified on a dated 2026 page, R = reported/roster status, U = unverified)
- **SEA:** **Drew Lock starts for a second straight game, replacing injured Sam Darnold (ribs/quad)** (V: Fox Sports preview). Lock's 2026 sample is 3 games (23, 27, 28 attempts), so SEA's passing props rest on a thin QB sample and SEA receivers' historical targets mostly came from Darnold. nflverse roster status lists no skill-position names beyond depth-chart reserves for SEA (R); game-day inactive list not retrieved (U). Zach Charbonnet has only 2 games in the sample (wk8 and wk9).
- **LV:** **Kirk Cousins was traded to Minnesota; rookie Fernando Mendoza makes his first career NFL start** (V: Fox Sports preview). His only 2026 NFL snaps are 8 pass attempts and 1 carry in week 5. All LV receivers' history comes with Cousins (g=9 at QB). Inactive list not retrieved (U).
- **LAR:** Puka Nacua and Davante Adams are on reserve in the nflverse roster file (R), and the WR corps (Atwell, Mumpfield, Daniels) has been in place since week 2, so their sample reflects the current room. TE Terrance Ferguson is on reserve (R). Stafford has started all 9 games. Inactive list not retrieved (U).
- **ARI:** **Rookie Carson Beck starts** (V: Arizona Sports, Fox Sports); Jacoby Brissett was traded to Baltimore and Gardner Minshew suffered a season-ending elbow injury (V: Fox Sports). **Beck has no regular-season NFL snaps**, so all ARI passing-game numbers come from three different QBs (Brissett w1-8, Minshew w8-9). RB James Conner, Trey Benson and Jeremiyah Love, WRs Michael Wilson, Kendrick Bourne and Jalen Brooks are on reserve (R). Inactive list not retrieved (U).
- **SF:** **Keenan Allen has 0 games with SF in my data**; all 8 of his 2026 games were with IND (weeks 1-9). WR Ricky Pearsall, Christian Kirk and Brandon Aiyuk are on reserve or not active (R). Purdy has started all 8 games he played. Inactive list not retrieved (U).
- **DAL:** Dak Prescott has started all 9 games. Full inactive list not retrieved (U).
- Search note: most retrieved inactive pages were from earlier seasons and were discarded; nothing from them is used.

## 4. Team context (nflverse 2026, raw, not opponent-adjusted)
| | Off EPA/play | Def EPA/play allowed | Pass att/g | Rush att/g | Opp rush: ypc allowed | Opp pass: yds/att allowed |
|---|---|---|---|---|---|---|
| SEA | -0.044 | -0.099 | 33.9 | 28.0 | 3.56 | 4.68 |
| LV | -0.010 | +0.094 | 36.9 | 23.6 | 5.31 | 7.07 |
| LA | +0.044 | -0.114 | 39.8 | 26.0 | 3.96 | 5.82 |
| ARI | -0.036 | +0.075 | 41.9 | 24.8 | 4.33 | 7.00 |
| SF | +0.178 | -0.075 | 30.2 | 28.0 | 3.45 | 5.80 |
| DAL | +0.097 | +0.091 | 38.9 | 25.7 | 5.16 | 6.58 |

**Scenario branches (qualitative, no probabilities).** Branches: (A) favored-to-trail team controls anyway, (B) competitive/balanced, (C) favored-narrative team dominates, (D) low-scoring, suppressed volume.
- **SEA @ LV (SEA -6.5, total 40.5):** C and D most likely, B moderate, A low. Volume: both offenses are led by backup or first-time QBs; LV rush volume likely falls if it trails, LV pass volume rises but with an unproven QB. Tag: defensive-turnover (SEA), clock-control rushing (SEA with a lead).
- **LAR @ ARI (LAR -9, total 38.5):** C most likely, D moderate, B low, A low. Volume: LAR rush volume up with a lead, LAR pass volume down; ARI's volume is the least predictable on the board (third QB in three weeks, rookie, thin RB room). Tag: clock-control rushing (LAR).
- **SF @ DAL (SF -4, total 55.5):** B most likely, C moderate, A moderate, D low. This is the highest total on the board, so both pass volumes and RB targets carry upside risk for Unders. Tag: pass-driven (both).

## 5. Props by status
**Lines:** screenshots 3:05-3:08 PM ET. Break-even (BE) = raw implied probability of the quoted price. Edge = model probability of the side minus BE, in points.

### LEAN
| Prop | Line / price | Evidence | DQ | Level | Opp. / Scenario Conf. |
|---|---|---|---|---|---|
| **Konata Mumpfield (LAR) UNDER receptions** | U2.5 -150 (BE 60.0%) | Rec (last 8): 1, 4, 1, 0, 2, 1, 0, 2; **Under 7 of 8**. Targets 2, 8, 3, 0, 3, 2, 2, 2 (the 8 came in week 3 on 63 snaps). Snaps 43, 63, 23, 6, 27, 31, 27, 33. tgtEW 2.3, catch .53 (WR prior .62, shrunk). Pilot P(Under) 86.5%, edge +26.5, **min +21.8** (vol +15%). Stress: 77.4% at +30% targets, 70.9% at +50%, 55.7% at +100%; **breaks even near +80% target volume.** Over needs 3 catches, about 5 targets at his catch rate. | Medium | B | Opp. **60/100** (LAR inactives unverified, ARI QB unknown, which could change LAR's pass volume either way); Scenario **Medium** |
| **Javonte Williams (DAL) UNDER receptions** | U2.5 +120 (BE 45.5%) | Rec (8): 3, 2, 5, 2, 2, 0, 1, 4; **Under 5 of 8**. Targets 4, 3, 5, 3, 2, 0, 2, 5; snaps 44-58 every week; carries 11-25. tgtEW 3.0, catch .81 (RB prior .78). Pilot P(Under) 57.2%, edge +11.8, **min +2.5** (last-2 mean). Stress: 41.3% at +30% targets (BE 45.5%), so **breaks even near +20% target volume**; Over needs 3 catches, about 4 targets. Weakest of the three: the 55.5 total and DAL as a 4-point underdog both push toward more targets. | High | B | Opp. **65/100**; Scenario **Medium** |
| **Ashton Jeanty (LV) UNDER rush yds** | U36.5 -115 (BE 53.5%) | Rush yds (8): 48, 56, 58, 27, 22, 15, 9, 25; **Under 5 of 8, all of the last 5 at 27 or fewer.** Carries 21, 19, 15, 10, 10, 8, 2, 6; snaps 51, 59, 56, 32, 38, 49, 25, 32. carEW 9.2, ypc 3.53 (shrunk toward 4.33), SEA allows x0.911 (adjustment). Pilot P(Under) 70.9%, edge +17.4, **min +9.2** (vol +15%). Stress: 44.4% at +50% carries, so **breaks even near +35% carries (about 12 to 13 carries).** LV is a 6.5-point underdog, which points to fewer carries. | Medium | B | Opp. **55/100** (first Mendoza start, LV usage declined from 21 carries to 6 over 8 weeks; Michael Washington O25.5 rush fails the gate at min -0.4); Scenario **Medium** |

**Thresholds recorded (Addendum B):** Mumpfield Over needs 3 receptions; Williams Over needs 3 receptions; Jeanty Over needs 37+ rush yards.
**Cluster note:** the Williams Under shares a script risk with the whole SF@DAL game (DAL trailing, SF pushing a 55.5 total); Mumpfield and Jeanty are in different games. No two LEANs are evidence for each other.
**Kill conditions (my stated conditions, not calibrated):** Mumpfield: any LAR WR1/WR2 or TE inactive that raises his role, Stafford out, or price worse than -175. Williams: price worse than +100, a DAL WR or TE inactive that changes target distribution, or a Prescott injury. Jeanty: Michael Washington inactive (raises Jeanty's share), Mendoza out of the game early (changes script), or price worse than -135. A QB injury to either side in any game changes remaining props for both teams (section 7).

### WATCH (not promoted)
| Prop | Line / price | Pilot (base / min edge) | Why not LEAN |
|---|---|---|---|
| Tyler Higbee U3.5 rec (LAR) | U +100 (BE 50.0%) | P(U) 64.6%, +14.6 / +6.1 | **Model and history disagree:** Under 3.5 in only 4 of 8 (rec 0, 8, 5, 5, 4, 2, 1, 1; targets 0, 11, 6, 6, 4, 3, 2, 5), though the last three are down. Breaks even near +30% targets. After the approved 5-8 point calibration haircut the stability margin is about 0. |
| Colby Parkinson U3.5 rec (LAR) | U -110 (BE 52.4%) | P(U) 65.9%, +13.6 / **-3.4** | Fails last-2 check. |
| Tutu Atwell U2.5 rec (LAR) | U -140 (BE 58.3%) | P(U) 78.9%, +20.5 / **-5.6** | Fails last-2 check; g=6. |
| Davis Allen U1.5 rec (LAR) | U -135 (BE 57.4%) | P(U) 64.6%, +7.2 / +0.7 | Fails stability. Rec (8): 1, 2, 0, 2, 0, 4, 2, 0. |
| Blake Corum U58.5 rush (LAR) | U -115 | P(U) 66.0%, +12.5 / +3.0 | **Model and history disagree:** yards 79, 15, 14, 19, 42, 93, 73, 58; Over in 3 of 8, **two of the last three at 73 and 93**, carries 9, 17, 11, 11 in the last four. LAR -9 favors rushing volume late. |
| Matthew Stafford O209.5 pass yds (LAR) | O -120 (BE 54.5%) | P(O) 68.4%, +13.9 / **-2.9** | Fails stability (vol -15%); the LAR -9 script points to fewer attempts. |
| Elijah Higgins U2.5 rec (ARI) | U -120 (BE 54.5%) | P(U) 63.9%, +9.3 / +1.6 | **ARI quarterback change (Beck, no sample)**; targets 0, 3, 2, 3, 3, 3, 4, 2 came from other QBs. |
| Reggie Virgil U2.5 rec (ARI) | U -160 (BE 61.5%) | P(U) 89.9%, +28.4 / +20.8 | **Role-shift flag and QB change:** g=5, snaps 13, 3, 3, 38, 18, targets 5, 0, 0, 2, 4. |
| Simi Fehoko U1.5 rec (ARI) | U -165 (BE 62.3%) | P(U) 96.4%, +34.1 / +25.2 | **Role-shift flag:** snaps 6, 6, 3, 6, 7, then 40 and 26; targets only 0, 0, 0, 0, 0, 1, 1. Usage regime changed two weeks ago and the QB changed again. |
| Bam Knight U33.5 rush (ARI) | U -115 | P(U) 73.2%, +19.7 / +12.4 | **Role-shift flag:** g=6 with carries 0, 2, 1, 15, 7, 3 and snaps 3-6 until week 6; no wk9 data point; QB change; Conner, Benson and Love on reserve (R). |
| Tory Horton O0.5 rec (SEA) | O -220 (BE 68.8%) | P(O) 78.9%, +10.2 / +5.0 | **Model and history disagree:** rec 0, 3, 1, 0, 1, 0, 3, 2 gives Over 0.5 in 5 of 8 (62.5%) against a 68.8% price; Lock is the QB. |
| Michael Mayer O2.5 rec (LV) | O -145 (BE 59.2%) | P(O) 71.3%, +12.1 / +2.5 | **LV quarterback change (Mendoza).** Over 7 of 8 but all with Cousins. |
| Jalen Nailor O1.5 rec (LV) | O +110 (BE 47.6%) | P(O) 57.1%, +9.5 / +1.8 | **LV quarterback change.** Over 4 of 8 (rec 3, 1, 1, 0, 1, 2, 4, 2). |
| Zach Charbonnet U63.5 rush (SEA) | U -115 | P(U) 64.5%, +11.0 / +2.1 | **g=2** (week 8: 6 carries, 23 snaps; week 9: 16 carries, 38 snaps) after missing weeks 1-7; role and workload unknown. Jadarian Price carried 10, 13, 5, 10, 9 in his 5 games. |
| Drew Lock U5.5 rush (SEA) | U -115 | P(U) 60.2%, +6.7 / +2.1 | **g=3**, QB rush Under (calibration caveat: overconfident 5-8 points). |
| Dak Prescott U1.5 pass TD (DAL) | U +145 (BE 40.8%) | P(U) 49.4%, +8.5 / **+1.1** | Narrowly fails min +1.5; the Poisson pass-TD method is unvalidated and the 55.5 total is the highest on the board. |
| Brevyn Spann-Ford U2.5 rec (DAL) | U +110 (BE 47.6%) | P(U) 65.7%, +18.1 / **-0.3** | Fails last-2 check. |

### PASS / Level C (screened, no verified edge or no valid sample)
| Prop | Line | Reason |
|---|---|---|
| **Carson Beck (ARI) all props** | pass 175.5, TD 0.5, rush 10.5 | **No NFL regular-season sample.** Pass TD output of 62.2% is points-only (Poisson), not a QB model. Level C. |
| **Fernando Mendoza (LV) all props** | pass 183.5, TD 0.5, rush 15.5 | **g=1** (8 attempts, 1 carry). Pilot outputs (Under 99.9% pass yds, 90.8% rush) are sample artifacts. Level C. |
| **Keenan Allen (SF) O2.5 rec** | 2.5 | **No SF games**; the IND sample is not used. Level C. |
| **CJ Daniels (LAR) U1.5 rec; Jadarian Price (SEA) O1.5 rec** | see table | Daniels: g=3 with 1-3 snaps per game and 0 targets, pilot 100% is an artifact. Price: base +9.1 but min +1.3 and a 5-game, injury-gapped sample. |
| Duvernay (ARI), Allgeier (ARI) | see table | Duvernay g=2; Allgeier O2.5 rec +6.0 / -3.6, rush O34.5 +4.2 / -6.0. |
| McBride O6.5 rec (ARI) | O -105 | +6.7 / -9.9, fails stability; QB change. |
| Bowers, Tucker, Jeanty rec, Washington rush, Bech (LV) | see table | Bowers O5.5 +7.8 / -5.0; Tucker O2.5 +17.4 / -4.0 (last-2); Jeanty O4.5 rec +5.0 / -6.9; Washington O25.5 rush +9.4 / -0.4; Bech base -0.9. |
| Kupp, Shaheed, JSN, Barner (SEA) | see table | Base edges +3.6, +3.4, +0.4 and negative; none reach the gate. |
| Kyren Williams, McCaffrey, Kittle, Deebo, Lamb, Pickens, Flournoy, Juszczyk, Watkins, D. Robinson | see table | Base edge below +4.0 or min edge negative. Kyren O2.5 rec +3.2 / -30.1; Lamb O7.5 rec +8.8 / -5.7; Deebo U3.5 rec +11.0 / +0.5 (g=5, fails stability). |
| Purdy and Prescott pass yards | U260.5 / U270.5 | +9.7 / -4.9 and +12.7 / -2.5: fail stability; pass-yard Unders carry the 5-8 point calibration caveat. |
| Pass TD props (Lock, Stafford, Purdy) | see table | Poisson unvalidated; base edges +0.4, -2.9, -0.5. |
| Rush props with base edge under +4.0 | see table | Kyren, Stafford, McCaffrey, Black, Purdy, Deebo, J. Williams rush, Prescott rush: no edge or negative min. |
| **Anytime TD / 2+ TD (all)** | not reproduced | **No legitimate recorded pregame probability, so no quantified TD edge.** TD props stay Level B at best, no official TD PLAY (Addendum B). |
| Receiving yards (all) | not modeled | **Not modeled in the pilot, Level C.** |
| Not on the board or not read | | Rows hidden behind the nav bar, defense, kicker, longest-reception and alt lines. **Coverage sweep:** top-2 targets, primary and secondary RB, TE and QB screened for all six teams except the unread rows. |

## 6. Pilot v0.1 recorded probabilities (unvalidated; recorded after seeing prices)
**Method (identical to the Week 10 1 PM card):** volume = negative binomial with exponentially weighted mean (half-life 3 games) over weeks with offense snaps or recorded involvement for the CURRENT team, zeros included; dispersion r: targets 13.5, carries 8.1, attempts 26.3 (carried over). Receptions = Binomial(targets, catch rate shrunk to position prior with 15 pseudo-targets: WR .62, TE .72, RB .78). Rush and pass yards: per-play yardage drawn from the league 2026 empirical distribution, scaled to the player's ypc/ypa shrunk to league (50 carries / 100 attempts; QB carries shrunk to league QB 5.56), 50% opponent adjustment from raw allowed rates; 40,000 sims; no game-script adjustment. Pass TD = Poisson with lambda = 0.0660 x implied points. Anytime TDs and receiving yards are not priced. Perturbations: volume +/-15%, dispersion x0.5 / x2, last-2-games mean, catch prior 5 / 30 (rec), no opponent adjustment (yards), league QB carry distribution (QB rush), lambda +/-15% and total -3 / +3 (pass TD; the table's lam-15 and lam+15 labels cover the lambda perturbations). Min edge is the worst perturbation for the base best side. **Proposed gate (mine, not governance-approved):** LEAN-eligible only if base edge >= +4.0 pts, min edge >= +1.5, Data Quality >= Medium and no role-shift flag. Stress tests in section 5 (target/carry multipliers) were added after seeing the output and are disclosed as such. Quarterback-change and calibration flags (sections 1 and 3) were applied as analyst judgment on top of the gate.

| Player | Market | Line | O / U price | Model P(Over) | Best side | P(best) | Break-even | Base edge (pts) | Min edge across perturbations | Inputs |
|---|---|---|---|---|---|---|---|---|---|---|
| Trey McBride (ARI) | receptions | 6.5 | -105 / -125 | 57.9% | Over | 57.9% | 51.2% | +6.7 | -9.9 (last2) | tgtEW 9.8 catch 0.77 g=9 |
| Elijah Higgins (ARI) | receptions | 2.5 | -110 / -120 | 36.1% | Under | 63.9% | 54.5% | +9.3 | +1.6 (vol+15) | tgtEW 2.6 catch 0.82 g=9 |
| Reggie Virgil (ARI) | receptions | 2.5 | +125 / -160 | 10.1% | Under | 89.9% | 61.5% | +28.4 | +20.8 (last2) | tgtEW 2.3 catch 0.47 g=5 |
| Tyler Allgeier (ARI) | receptions | 2.5 | +135 / -185 | 48.6% | Over | 48.6% | 42.6% | +6.0 | -3.6 (vol-15) | tgtEW 3.1 catch 0.87 g=9 |
| Bam Knight (ARI) | receptions | 1.5 | -110 / -120 | 42.3% | Under | 57.7% | 54.5% | +3.2 | -24.6 (last2) | tgtEW 2.0 catch 0.74 g=6 |
| Devin Duvernay (ARI) | receptions | 1.5 | +115 / -150 | 39.9% | Under | 60.1% | 60.0% | +0.1 | -6.6 (vol+15) | tgtEW 2.0 catch 0.70 g=2 |
| Simi Fehoko (ARI) | receptions | 1.5 | +125 / -165 | 3.6% | Under | 96.4% | 62.3% | +34.1 | +25.2 (last2) | tgtEW 0.5 catch 0.61 g=7 |
| Tyler Allgeier (ARI) | rush yds | 34.5 | -120 / -110 | 58.8% | Over | 58.8% | 54.5% | +4.2 | -6.0 (vol-15) | carEW 11.2 ypc 4.21 adj x0.957 g=9 |
| Bam Knight (ARI) | rush yds | 33.5 | -115 / -115 | 26.8% | Under | 73.2% | 53.5% | +19.7 | +12.4 (vol+15) | carEW 5.3 ypc 4.93 adj x0.957 g=6 |
| Carson Beck (ARI) | rush yds | 10.5 | -120 / -110 | n/a | n/a | n/a | n/a | n/a | n/a | no usable sample, Level C |
| Carson Beck (ARI) | pass yds | 175.5 | n/a / n/a | n/a | n/a | n/a | n/a | n/a | n/a | no usable sample, Level C |
| Carson Beck (ARI) | pass TD | 0.5 | -155 / +120 | 62.2% | Over | 62.2% | 60.8% | +1.4 | -4.5 (lam-15) | lambda 0.97 (14.75 pts) g=0 |
| Tyler Higbee (LA) | receptions | 3.5 | -130 / +100 | 35.4% | Under | 64.6% | 50.0% | +14.6 | +6.1 (vol+15) | tgtEW 4.2 catch 0.72 g=9 |
| Colby Parkinson (LA) | receptions | 3.5 | -120 / -110 | 34.1% | Under | 65.9% | 52.4% | +13.6 | -3.4 (last2) | tgtEW 3.9 catch 0.76 g=7 |
| Kyren Williams (LA) | receptions | 2.5 | -160 / +125 | 64.7% | Over | 64.7% | 61.5% | +3.2 | -30.1 (last2) | tgtEW 4.5 catch 0.78 g=9 |
| Tutu Atwell (LA) | receptions | 2.5 | +110 / -140 | 21.1% | Under | 78.9% | 58.3% | +20.5 | -5.6 (last2) | tgtEW 2.7 catch 0.58 g=6 |
| Konata Mumpfield (LA) | receptions | 2.5 | +115 / -150 | 13.5% | Under | 86.5% | 60.0% | +26.5 | +21.8 (vol+15) | tgtEW 2.3 catch 0.53 g=9 |
| Davis Allen (LA) | receptions | 1.5 | +105 / -135 | 35.4% | Under | 64.6% | 57.4% | +7.2 | +0.7 (vol+15) | tgtEW 1.7 catch 0.74 g=9 |
| CJ Daniels (LA) | receptions | 1.5 | +120 / -155 | 0.0% | Under | 100.0% | 60.8% | +39.2 | +39.2 (base) | tgtEW 0.0 catch 0.62 g=3 |
| Blake Corum (LA) | receptions | 1.5 | +130 / -170 | 35.0% | Under | 65.0% | 63.0% | +2.0 | -4.2 (vol+15) | tgtEW 1.8 catch 0.68 g=9 |
| Kyren Williams (LA) | rush yds | 66.5 | -115 / -115 | 44.6% | Under | 55.4% | 53.5% | +1.9 | -8.5 (vol+15) | carEW 14.6 ypc 4.57 adj x1.000 g=9 |
| Blake Corum (LA) | rush yds | 58.5 | -115 / -115 | 34.0% | Under | 66.0% | 53.5% | +12.5 | +3.0 (vol+15) | carEW 10.4 ypc 4.88 adj x1.000 g=9 |
| Matthew Stafford (LA) | rush yds | 0.5 | +135 / -180 | 37.1% | Under | 62.9% | 64.3% | -1.4 | -5.2 (vol+15) | carEW 0.6 ypc 5.35 adj x1.000 g=9 |
| Matthew Stafford (LA) | pass yds | 209.5 | -120 / -110 | 68.4% | Over | 68.4% | 54.5% | +13.9 | -2.9 (vol-15) | attEW 38.4 ypa 6.37 adj x1.062 g=9 |
| Matthew Stafford (LA) | pass TD | 1.5 | +100 / -130 | 46.4% | Under | 53.6% | 56.5% | -2.9 | -10.3 (lam+15) | lambda 1.57 (23.75 pts) g=9 |
| Brock Bowers (LV) | receptions | 5.5 | -105 / -125 | 59.0% | Over | 59.0% | 51.2% | +7.8 | -5.0 (vol-15) | tgtEW 9.3 catch 0.70 g=7 |
| Ashton Jeanty (LV) | receptions | 4.5 | +125 / -160 | 49.5% | Over | 49.5% | 44.4% | +5.0 | -6.9 (vol-15) | tgtEW 6.2 catch 0.77 g=9 |
| Michael Mayer (LV) | receptions | 2.5 | -145 / +110 | 71.3% | Over | 71.3% | 59.2% | +12.1 | +2.5 (vol-15) | tgtEW 4.8 catch 0.82 g=9 |
| Tre Tucker (LV) | receptions | 2.5 | -110 / -120 | 69.8% | Over | 69.8% | 52.4% | +17.4 | -4.0 (last2) | tgtEW 6.5 catch 0.60 g=9 |
| Jalen Nailor (LV) | receptions | 1.5 | +110 / -140 | 57.1% | Over | 57.1% | 47.6% | +9.5 | +1.8 (vol-15) | tgtEW 3.7 catch 0.54 g=8 |
| Jack Bech (LV) | receptions | 0.5 | -190 / +140 | 59.2% | Under | 40.8% | 41.7% | -0.9 | -5.4 (vol+15) | tgtEW 1.4 catch 0.67 g=5 |
| Ashton Jeanty (LV) | rush yds | 36.5 | -115 / -115 | 29.1% | Under | 70.9% | 53.5% | +17.4 | +9.2 (vol+15) | carEW 9.2 ypc 3.53 adj x0.911 g=9 |
| Michael Washington (LV) | rush yds | 25.5 | -110 / -120 | 61.7% | Over | 61.7% | 52.4% | +9.4 | -0.4 (vol-15) | carEW 9.5 ypc 4.06 adj x0.911 g=9 |
| Fernando Mendoza (LV) | rush yds | 15.5 | -120 / -110 | 9.2% | Under | 90.8% | 52.4% | +38.4 | +36.5 (vol+15) | carEW 1.0 ypc 5.50 adj x0.911 g=1 |
| Fernando Mendoza (LV) | pass yds | 183.5 | -115 / -115 | 0.1% | Under | 99.9% | 53.5% | +46.4 | +46.2 (noopp) | attEW 8.0 ypa 6.21 adj x0.876 g=1 |
| Fernando Mendoza (LV) | pass TD | 0.5 | -230 / +165 | 67.4% | Over | 67.4% | 69.7% | -2.3 | -8.2 (lam-15) | lambda 1.12 (17.00 pts) g=1 |
| Jaxon Smith-Njigba (SEA) | receptions | 7.5 | +105 / -135 | 49.2% | Over | 49.2% | 48.8% | +0.4 | -13.8 (vol-15) | tgtEW 11.0 catch 0.70 g=9 |
| Cooper Kupp (SEA) | receptions | 1.5 | -185 / +140 | 68.5% | Over | 68.5% | 64.9% | +3.6 | -4.4 (vol-15) | tgtEW 3.9 catch 0.64 g=9 |
| Rashid Shaheed (SEA) | receptions | 1.5 | -185 / +140 | 68.3% | Over | 68.3% | 64.9% | +3.4 | -4.5 (vol-15) | tgtEW 4.4 catch 0.56 g=7 |
| Tory Horton (SEA) | receptions | 0.5 | -220 / +160 | 78.9% | Over | 78.9% | 68.8% | +10.2 | +5.0 (vol-15) | tgtEW 2.9 catch 0.57 g=8 |
| AJ Barner (SEA) | receptions | 2.5 | -125 / -105 | 52.0% | Under | 48.0% | 51.2% | -3.2 | -11.6 (vol+15) | tgtEW 4.4 catch 0.64 g=9 |
| Zach Charbonnet (SEA) | receptions | 1.5 | -145 / +110 | 61.1% | Over | 61.1% | 59.2% | +1.9 | -6.2 (vol-15) | tgtEW 2.9 catch 0.75 g=2 |
| Jadarian Price (SEA) | receptions | 1.5 | -130 / +100 | 65.7% | Over | 65.7% | 56.5% | +9.1 | +1.3 (vol-15) | tgtEW 3.3 catch 0.72 g=5 |
| Zach Charbonnet (SEA) | rush yds | 63.5 | -115 / -115 | 35.5% | Under | 64.5% | 53.5% | +11.0 | +2.1 (vol+15) | carEW 11.6 ypc 4.40 adj x1.113 g=2 |
| Jadarian Price (SEA) | rush yds | 41.5 | -115 / -115 | 41.7% | Under | 58.3% | 53.5% | +4.8 | -4.1 (vol+15) | carEW 9.2 ypc 4.00 adj x1.113 g=5 |
| Drew Lock (SEA) | rush yds | 5.5 | -115 / -115 | 39.8% | Under | 60.2% | 53.5% | +6.7 | +2.1 (vol+15) | carEW 1.1 ypc 5.84 adj x1.113 g=3 |
| Drew Lock (SEA) | pass yds | 198.5 | -115 / -115 | 41.6% | Under | 58.4% | 53.5% | +4.9 | -8.4 (vol+15) | attEW 26.4 ypa 6.73 adj x1.068 g=3 |
| Drew Lock (SEA) | pass TD | 1.5 | +120 / -155 | 45.9% | Over | 45.9% | 45.5% | +0.4 | -7.5 (lam-15) | lambda 1.55 (23.50 pts) g=3 |
| CeeDee Lamb (DAL) | receptions | 7.5 | +115 / -145 | 55.3% | Over | 55.3% | 46.5% | +8.8 | -5.7 (vol-15) | tgtEW 13.0 catch 0.64 g=9 |
| George Pickens (DAL) | receptions | 4.5 | -105 / -125 | 47.2% | Under | 52.8% | 55.6% | -2.8 | -13.0 (vol+15) | tgtEW 7.4 catch 0.63 g=8 |
| Ryan Flournoy (DAL) | receptions | 3.5 | +115 / -150 | 38.6% | Under | 61.4% | 60.0% | +1.4 | -7.7 (vol+15) | tgtEW 4.8 catch 0.67 g=9 |
| Javonte Williams (DAL) | receptions | 2.5 | -155 / +120 | 42.8% | Under | 57.2% | 45.5% | +11.8 | +2.5 (last2) | tgtEW 3.0 catch 0.81 g=9 |
| Brevyn Spann-Ford (DAL) | receptions | 2.5 | -145 / +110 | 34.3% | Under | 65.7% | 47.6% | +18.1 | -0.3 (last2) | tgtEW 2.9 catch 0.72 g=9 |
| Javonte Williams (DAL) | rush yds | 60.5 | -115 / -115 | 54.8% | Over | 54.8% | 53.5% | +1.3 | -11.1 (vol-15) | carEW 18.9 ypc 4.14 adj x0.898 g=9 |
| Dak Prescott (DAL) | rush yds | 9.5 | -115 / -115 | 46.7% | Under | 53.3% | 53.5% | -0.1 | -14.4 (last2) | carEW 2.5 ypc 5.23 adj x0.898 g=9 |
| Dak Prescott (DAL) | pass yds | 270.5 | -115 / -115 | 33.8% | Under | 66.2% | 53.5% | +12.7 | -2.5 (vol+15) | attEW 38.1 ypa 6.52 adj x0.965 g=9 |
| Dak Prescott (DAL) | pass TD | 1.5 | -195 / +145 | 50.6% | Under | 49.4% | 40.8% | +8.5 | +1.1 (lam+15) | lambda 1.70 (25.75 pts) g=9 |
| George Kittle (SF) | receptions | 5.5 | +120 / -155 | 40.6% | Under | 59.4% | 60.8% | -1.3 | -14.1 (last2) | tgtEW 7.2 catch 0.72 g=8 |
| Christian McCaffrey (SF) | receptions | 4.5 | +115 / -145 | 44.0% | Over | 44.0% | 46.5% | -2.5 | -13.7 (vol-15) | tgtEW 5.5 catch 0.80 g=8 |
| Deebo Samuel (SF) | receptions | 3.5 | +115 / -145 | 29.9% | Under | 70.1% | 59.2% | +11.0 | +0.5 (last2) | tgtEW 3.8 catch 0.72 g=5 |
| Keenan Allen (SF) | receptions | 2.5 | +110 / -140 | n/a | n/a | n/a | n/a | n/a | n/a | no usable sample, Level C |
| Demarcus Robinson (SF) | receptions | 2.5 | +120 / -160 | 41.0% | Under | 59.0% | 61.5% | -2.5 | -11.2 (vol+15) | tgtEW 3.4 catch 0.69 g=3 |
| Jordan Watkins (SF) | receptions | 1.5 | +105 / -135 | 54.8% | Over | 54.8% | 48.8% | +6.0 | -2.3 (vol-15) | tgtEW 2.8 catch 0.69 g=6 |
| Kyle Juszczyk (SF) | receptions | 0.5 | -220 / +155 | 67.9% | Over | 67.9% | 68.8% | -0.9 | -6.6 (vol-15) | tgtEW 1.6 catch 0.76 g=7 |
| Christian McCaffrey (SF) | rush yds | 63.5 | -115 / -115 | 45.0% | Under | 55.0% | 53.5% | +1.5 | -8.0 (vol+15) | carEW 13.3 ypc 4.43 adj x1.096 g=8 |
| Kaelon Black (SF) | rush yds | 36.5 | -115 / -115 | 52.9% | Over | 52.9% | 53.5% | -0.6 | -11.0 (vol-15) | carEW 9.0 ypc 4.40 adj x1.096 g=8 |
| Brock Purdy (SF) | rush yds | 21.5 | -115 / -115 | 54.2% | Over | 54.2% | 53.5% | +0.8 | -7.8 (vol-15) | carEW 4.5 ypc 5.76 adj x1.096 g=8 |
| Deebo Samuel (SF) | rush yds | 6.5 | -115 / -115 | 49.4% | Under | 50.6% | 53.5% | -2.9 | -12.6 (last2) | carEW 2.0 ypc 4.99 adj x1.096 g=5 |
| Brock Purdy (SF) | pass yds | 260.5 | -115 / -115 | 36.9% | Under | 63.1% | 53.5% | +9.7 | -4.9 (vol+15) | attEW 30.9 ypa 7.47 adj x1.028 g=8 |
| Brock Purdy (SF) | pass TD | 2.5 | +160 / -225 | 31.3% | Under | 68.7% | 69.2% | -0.5 | -8.5 (lam+15) | lambda 1.96 (29.75 pts) g=8 |

**Gate result:**
- Numeric gate passes (base >= +4.0 and min >= +1.5) but not promoted: Higbee U3.5 rec, Higgins U2.5 rec, Virgil U2.5 rec, Fehoko U1.5 rec, Horton O0.5 rec, Mayer O2.5 rec, Nailor O1.5 rec, Corum U58.5 rush, Knight U33.5 rush, Charbonnet U63.5 rush, Lock U5.5 rush, Jeanty (promoted), Mumpfield (promoted), Williams (promoted), Daniels, Mendoza (Level C).
- **Of those, only three clear the full review with Data Quality >= Medium, no role-shift flag, no QB-change flag and agreement with history: Mumpfield U2.5 rec, Javonte Williams U2.5 rec, Jeanty U36.5 rush.** The rest fail on QB change (all ARI and LV receivers, Mayer, Nailor, Higgins, Virgil, Fehoko, Knight), role-shift flags (Fehoko, Virgil, Knight, Charbonnet), sample size (Daniels, Mendoza, Lock, Beck, Allen) or model-versus-history disagreement (Higbee, Corum, Horton).
- **Known tail issue:** QB carries use the league empirical distribution in the base run; the QB-distribution perturbation is included in min edge for the QB rush rows.

## 7. Correlation and QB injury volatility
- Structural only, no numeric joint probability. **No two LEANs are in the same game.** Within the WATCH list, the LAR receiver Unders (Higbee, Parkinson, Atwell, Allen, Mumpfield) share LAR pass volume and the ARI receiver Unders share ARI pass volume; they would lose together if a game turns into a shootout.
- Mumpfield U2.5 and Corum U58.5 (WATCH) are partly opposed in script terms: a LAR lead raises Corum's carries and lowers Mumpfield's targets. No parlay is authorized.
- QB injury volatility: SEA (backup-level Lock), LV (rookie first start) and ARI (rookie first start) each carry a materially higher chance of an in-game QB change than a normal slate. A QB leaving in any of these games changes both teams' remaining props. The Jeanty Under is not injury-censored (VOID) by a Mendoza exit, but its script assumption would change.

## 8. Governance
- No weights, components or features changed. No gematria, numerology, jersey-number or birthday inputs used.
- Frozen pregame record. Postgame results are graded against it only, with no hindsight reconstruction. The pilot probabilities add no PLAY or LEAN of their own; official statuses above come from the V2.2 card and Level B review.
- Closing prices are not captured here; CLV unscored unless later screenshots are added.
- Open items for the ledger: full inactive lists for all six teams, game lines after 11:40 AM, and weather were not verified before this lock. The net-of-sacks passing-yard definition remains an open modeling decision.

## Sources
- [Fox Sports: Raiders give Fernando Mendoza the keys (first start vs SEA, Lock subbing for injured Darnold, Beck starting for ARI)](https://www.foxsports.com/stories/nfl/fernando-mendoza-raiders-rams-puka-nacua)
- [Arizona Sports: Carson Beck named the Cardinals' starter against Rams](https://arizonasports.com/nfl/arizona-cardinals/carson-beck-named-the-cardinals-starter-against-rams)
- Week 10 Bet Model Lock 2 card (project doc `claude/week10-nfl-sun-bet-model-card-lock2.md`) for Hard Rock 11:40 AM lines
- nflverse releases: https://github.com/nflverse/nflverse-data (play_by_play_2026, snap_counts_2026, roster_2026, downloaded Nov 15 2026)

## 9. Errata (added 3:30 PM ET after outside review; original probabilities and statuses unchanged)
1. **WATCH count:** the Result section said 14; the list and table contain 17 (LAR@ARI 6, ARI 4, SEA@LV 5, SF@DAL 2). 17 is correct.
2. **QB-sample statement:** the opening said all three games had a thin QB sample. Only SEA@LV (Lock g=3, Mendoza g=1) and LAR@ARI (Beck none; Stafford is fine, so the uncertainty is the ARI side) qualify. SF@DAL does not.
3. **Game lines (both sources preserved):** (a) **Used in the recorded card:** Hard Rock 11:40 AM ET lines from the Lock 2 Bet Model card: SEA -6.5 / 40.5, LAR -9 / 38.5, SF -4 / 55.5. (b) **Later screenshot, per outside reviewer (timestamp not known to me; I did not have the image):** SEA -6.5 / 40.5, LAR -10 / 38.5, SF -4 / 55. Implied points (b): LAR 24.25, ARI 14.25, SF 29.5, DAL 25.5 (vs 23.75, 14.75, 29.75, 25.75 used). Effect on scenario text: LAR is a slightly larger favorite, which marginally strengthens the "LAR leads, fewer LAR pass attempts" branch (C) and the SF@DAL total is 0.5 lower, so the shootout concern for the Williams Under is very slightly smaller. Only pass-TD probabilities use implied points, and no LEAN does. Reference recompute on (b), not replacing the recorded table: Prescott P(Over 1.5 TD) 50.1% (recorded 50.6%), Stafford 47.5%, Beck 61.0%, Purdy P(Over 2.5) 30.9%. No status changes.
4. **Mumpfield probability, three labeled tiers (none is a validated calibrated probability):** raw pilot 86.5%; exploratory 5-8 point haircut (the audit's 6.1-point gap for tgtEW<2.5, P(Under)>=0.70, n = 542) gives about 78.5-81.5%; the audit's realized hit rate in that bucket was 75.1% (n = 542, model said 81.2%), which is the source of the 75% figure (not extra shrinkage I added). Break-even 60.0%. Audit source: `claude/prop-model-v0.1-calibration-audit.md` section 6, subgroups defined after seeing results (exploratory); section 8 states that a 25-38 point stated edge should not be read as a real edge of that size. The audit's RB reception Unders (gap -2.5) and non-QB rush Unders (gap -6.0, underconfident) show no overconfidence, so no haircut is applied to the Williams or Jeanty Unders.
