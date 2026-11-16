# NFL Player Prop Model v2.2: Week 10 Sunday (Nov 15 2026) postmortem

**Classification:** FINAL postmortem, graded only against the FROZEN pregame cards (`week10-nfl-sun-ne-det-munich-prop-model-card`, `week10-nfl-sun-1pm-prop-model-card`, `week10-nfl-sun-4pm-prop-model-card`). No hindsight reconstruction; no pregame status, probability or threshold was altered. v2.2 and the pilot v0.1 are unchanged; no parameter change is proposed or authorized. Written Sun Nov 15 2026 about 9:15 PM ET. SNF PIT@CIN was in progress and is not covered.

## 1. Provenance and data
- Pregame cards: Munich locked about 9:28 AM ET, 1 PM about 12:55 PM, 4 PM about 3:30 PM (screenshot stamps in each card). Prices and pilot probabilities are as recorded there; pilot probabilities were computed after seeing prices.
- Results: nflverse play_by_play_2026 (downloaded about 8:56 PM ET Nov 15), derived per-player lines. Validated against the sports feed's official team totals: rush attempts/yards and receptions matched for all games except **DAL rush attempts (mine 25, feed 24; yards 96 both)**. Rushing includes QB scrambles and kneels, as official stats do. Provisional until stat corrections.
- Closing prices were not captured. **CLV is unscored** and no substitute is used.

## 2. Official LEAN record
**LEAN 4-4, VOID 1, PLAY none. Flat 1u: +0.19u** (2-0 on rushing Unders +1.74u; 2-4 on receiving Unders -1.55u).
- **Maye U27.5 rush = VOID.** The play log records "NE-10-D.Maye was injured during the play" on a Q1 sack (9:43); DeVito took every later snap. Pre-injury production (1 carry, 11 yards) is an observation only, outside the denominator.
- Rushing Unders are n=2 and are not evidence of strength.

### Official LEANs (and the VOID)
| Player | Prop | Price | Break-even | Pilot P(side) | Actual | Result | Units |
|---|---|---|---|---|---|---|---|
| Maye | rush U27.5 | -115 | 53.5% | 78.8% | 11 | VOID (injury exit) | - |
| Young | rush U9.5 | -115 | 53.5% | 81.5% | 1 | W | +0.87 |
| Bijan | rec U3.5 | +125 | 44.4% | 58.0% | 4 | L | -1.00 |
| Pitts | rec U3.5 | +115 | 46.5% | 59.3% | 4 | L | -1.00 |
| Burks | rec U1.5 | +125 | 44.4% | 82.4% | 0 | W | +1.25 |
| Treadwell | rec U2.5 | -160 | 61.5% | 75.7% | 3 | L | -1.00 |
| Mumpfield | rec U2.5 | -150 | 60.0% | 86.5% | 3 | L | -1.00 |
| Javonte Williams | rec U2.5 | +120 | 45.5% | 57.2% | 1 | W | +1.20 |
| Jeanty | rush U36.5 | -115 | 53.5% | 70.9% | 18 | W | +0.87 |

### WATCH, diagnostic only (never counted in the official record)
| Player | Prop | Price | Break-even | Pilot P(side) | Actual | Result | Units |
|---|---|---|---|---|---|---|---|
| Kiner | rush U31.5 | -115 | 53.5% | 66.1% | 25 | W | +0.87 |
| Gibbs | rec U4.5 | -140 | 58.3% | 69.8% | 7 | L | -1.00 |
| A.J. Brown | rec U4.5 | -150 | 60.0% | 70.8% | 2 | W | +0.67 |
| Goff | rush O0.5 | -120 | 54.5% | 63.6% | 3 | W | +0.83 |
| London | rec U5.5 | -105 | 51.2% | 64.5% | 6 | L | -1.00 |
| Worthy | rec O2.5 | -135 | 57.4% | 73.4% | 0 | L | -1.00 |
| Penix | pyds U219.5 | -115 | 53.5% | 68.0% | 286 | L | -1.00 |
| Rice | rec U5.5 | -125 | 55.6% | 74.0% | 5 | W | +0.80 |
| Pollard | rush O56.5 | -115 | 53.5% | 67.1% | 33 | L | -1.00 |
| Spears | rush U10.5 | -120 | 54.5% | 63.9% | 28 | L | -1.00 |
| Lawrence | pyds U247.5 | -115 | 53.5% | 62.8% | 352 | L | -1.00 |
| Washington | rec U4.5 | -150 | 60.0% | 69.2% | 7 | L | -1.00 |
| Shough | pyds U252.5 | -115 | 53.5% | 69.9% | 187 | W | +0.87 |
| Kamara | rush O12.5 | -120 | 54.5% | 73.0% | 4 | L | -1.00 |
| Jefferson | rec U7.5 | -145 | 59.2% | 84.8% | 9 | L | -1.00 |
| Love | rush U3.5 | -110 | 52.4% | 65.9% | 0 | W | +0.91 |
| Lloyd | rush O12.5 | -120 | 54.5% | 68.4% | 13 | W | +0.83 |
| B.Allen | rush O31.5 | -120 | 54.5% | 83.8% | 40 | W | +0.83 |
| K.Coleman | rec U1.5 | -105 | 51.2% | 68.3% | 1 | W | +0.95 |
| J.Taylor | rush U71.5 | -115 | 53.5% | 64.0% | 83 | L | -1.00 |
| Mitchell | rec O2.5 | -130 | 56.5% | 67.1% | 3 | W | +0.77 |
| Boston | rec O2.5 | -175 | 63.6% | 73.2% | 1 | L | -1.00 |
| Higbee | rec U3.5 | +100 | 50.0% | 64.6% | 3 | W | +1.00 |
| Parkinson | rec U3.5 | -110 | 52.4% | 65.9% | 2 | W | +0.91 |
| Atwell | rec U2.5 | -140 | 58.3% | 78.9% | 1 | W | +0.71 |
| Davis Allen | rec U1.5 | -135 | 57.4% | 64.6% | 1 | W | +0.74 |
| Corum | rush U58.5 | -115 | 53.5% | 66.0% | 100 | L | -1.00 |
| Stafford | pyds O209.5 | -120 | 54.5% | 68.4% | 249 | W | +0.83 |
| Higgins | rec U2.5 | -120 | 54.5% | 63.9% | 0 | UNVERIFIED, excluded | - |
| Virgil | rec U2.5 | -160 | 61.5% | 89.9% | 0 | UNVERIFIED, excluded | - |
| Fehoko | rec U1.5 | -165 | 62.3% | 96.4% | 1 | W | +0.61 |
| Bam Knight | rush U33.5 | -115 | 53.5% | 73.2% | 19 | W | +0.87 |
| Horton | rec O0.5 | -220 | 68.8% | 78.9% | 0 | UNVERIFIED, excluded | - |
| Mayer | rec O2.5 | -145 | 59.2% | 71.3% | 2 | L | -1.00 |
| Nailor | rec O1.5 | +110 | 47.6% | 57.1% | 1 | L | -1.00 |
| Charbonnet | rush U63.5 | -115 | 53.5% | 64.5% | 94 | L | -1.00 |
| Lock | rush U5.5 | -115 | 53.5% | 60.2% | 20 | L | -1.00 |
| Prescott | ptd U1.5 | +145 | 40.8% | 49.4% | 5 | L | -1.00 |
| Spann-Ford | rec U2.5 | +110 | 47.6% | 65.7% | 1 | W | +1.10 |

### PASS, diagnostic only
| Player | Prop | Price | Break-even | Pilot P(side) | Actual | Result | Units |
|---|---|---|---|---|---|---|---|
| Chism | rec O0.5 | -180 | 64.3% | 92.5% | 0 | L | -1.00 |
| Hollins | rec O2.5 | -135 | 57.4% | 65.5% | 5 | W | +0.74 |

Higgins, Virgil (ARI) and Horton (SEA) have no recorded plays and their active status is unverified (the week 10 snap file is not populated); they are excluded from every tally. WATCH tallies below use the 36 graded props.

## 3. Receiving Under losses: opportunity versus conversion
Pregame EW targets (from the cards) vs actual, for the four losing LEANs: Bijan 4.3 vs 5, Pitts 4.8 vs 5, Treadwell 2.9 vs 3, Mumpfield 2.3 vs 4 (total 14.3 expected, 17 actual). Modeled catch rates .78, .69, .58, .53.
- Expected receptions at pregame targets: 9.6. At actual targets: 11.2. Actual: 14 (82% conversion).
- **Roughly 1.6 catches of the 4.4 miss came from extra targets (opportunity, mostly Mumpfield +1.7), and roughly 2.8 from conversion.** Both mechanisms contributed; conversion was larger. The approximately 1.9-catch standard deviation is an unadjusted independent-Bernoulli approximation using the four modeled catch rates and actual target counts. The 2.8-catch conversion residual is therefore about 1.5 approximate standard deviations; this is descriptive, not a formal significance test, and does not account for dependence among players sharing game environments.
- For the eight graded LEANs (excluding the Maye VOID), realized receptions were below the recorded Over threshold on the six losing/winning Under selections except Bijan, who landed exactly on the threshold. This is a directional classification against the reception threshold, **not** a claim that target counts were predicted exactly. Outcomes were 4-4; Maye was VOID.
- Subgroup note: all six receiving Unders (2-4) averaged pilot P 69.8% vs 33% realized (about 7% under the pilot's own probabilities, n=6 with two correlated pairs, effective n about 4). The audit's warning (`prop-model-v0.1-calibration-audit`, weeks 3-9) made this archetype a pre-specified concern, so today is an out-of-sample data point for it.

## 4. Calibration (diagnostic; pilot is unvalidated)
| Population | n | Avg pilot P | Hit rate |
|---|---|---|---|
| LEAN (graded) | 8 | 71.4% | 50% |
| WATCH (graded) | 36 | 68.8% | 50% |
| Combined | 44 | 69.3% | 50% |
Brier 0.275 (flat 50% forecast: 0.250). Buckets: P<65%: 4/14 (29%); 65-80%: 14/24 (58%); >80%: 4/6 (67%). Higher stated probabilities hit more often, but at lower rates than stated. Caveats: the 44 are same-game correlated (not 44 experiments); the props are selected where the pilot disagrees with the market; probabilities were computed after prices. Do not read this as an adjustment factor.

## 5. Held-back and PASS diagnostics
- Props held back for role-shift or QB-change flags (14): 6-8, -3.04u diagnostic. Jefferson U7.5 (flagged: breaks even near 11 targets) got 13 targets, 9 rec. Chism O0.5 (PASS, pilot 92.5%, role-shift flag) got 1 target, 0 rec.
- ARI Unders (Fehoko, Bam Knight) won; LV Overs (Mayer, Nailor) lost, consistent with the QB-change flag but n is small.
- PASS and WATCH outcomes are never wins or losses in the official record.

## 6. Same-game exposure
KC won 35-13; Penix threw 43 non-sack passes (card failure case: 40+). Bijan U3.5 and Pitts U3.5 (official LEANs, one cluster) lost; London U5.5 and Penix U219.5 (WATCH, same mechanism) also lost. **Only two of those four were official positions.** The card treated Bijan/Pitts as one cluster and held London to WATCH for that reason. This is a position-sizing and exposure question for anyone staking the board, not a failure of the Conditional Parlay Engine (no parlay was built). IND cluster (Burks W, Treadwell L) split.

## 7. Scenario branches
Qualitative only: **no branch probabilities were recorded pregame, so branch calibration cannot be scored retrospectively.** Top-ranked branch matched in 5 of 8 games with a branch list (JAX@TEN, CAR@NO, SEA@LV, LAR@ARI, SF@DAL). KC@ATL and NE@DET went to the "moderate" branch (C); MIN@GB (underdog dominated 30-10, branch A rated low) was a miss. Any future scenario calibration requires recording branch probabilities before kickoff.

## 8. Research items (no model change)
1. Low-volume receiving Under calibration, using the existing weeks 3-9 walk-forward dataset plus today as one new out-of-sample day (the cumulative ledger is not needed and is not complete).
2. Opportunity versus conversion decomposition, using recorded pregame EW targets and catch priors per prop.
3. Same-game cluster exposure reporting (count of positions per mechanism) on cards.
4. Record branch probabilities pregame, then evaluate.
Not done and not authorized: lowering Under probabilities, changing gates, re-grading Mumpfield or any LEAN, extending the cumulative ledger (last on-file entry 2026-10-06: PLAY 1-1, LEAN 4-3; later weeks need versioned reconstruction from cards).

## 9. Cross-check notes (ChatGPT review of this audit)
Agreed: 4-4 with one VOID, rushing vs receiving split, no parameter change, CLV unscored, keep PASS/WATCH out of the record. Corrected: the player is **Laquon** Treadwell; no 70% confidence threshold exists in v2.2 or the pilot (the pilot's proposed, not governance-approved, LEAN gate is base edge at least +4.0, min edge at least +1.5, DQ at least Medium, no role-shift flag); "rushing-prop performance: strong" overstates n=2; branch probabilities were never recorded; the opportunity-versus-conversion question is answered from the cards in section 3 rather than needing retrieval.

## 10. Cross-check outcome and governance (recorded Sun Nov 15 2026, about 9:10 PM ET)
ChatGPT confirmed all five corrections in section 9. **It could not retrieve this file, so its agreement rests on the corrections as summarized in chat, not an independent read of the document.**
- **Carried forward as research conclusions:** (1) of the 4.4-catch shortfall, about 1.6 came from extra targets and 2.8 from conversion; (2) the +4.0 / +1.5 gate is a pilot proposal, not approved v2.2 governance, and no 70% threshold exists; (3) scenario calibration is a data-collection gap, not a measured failure; (4) the Atlanta result is two official LEAN losses plus two WATCH losses, a correlated-outcome observation, not a Conditional Parlay Engine failure; (5) rushing Unders 2-0 is n=2.
- **Revised research priorities:** 1) monitor low-volume receiving Under calibration; 2) keep target-volume and conversion error measured separately; 3) record scenario branch probabilities pregame; 4) improve same-game exposure reporting; 5) keep LEAN, WATCH and PASS results strictly separate.
- **Nov 15 is one additional out-of-sample observation** for the Weeks 3-9 walk-forward audit, not a new discovery exercise. A historical-ledger research protocol is not needed.
- **Governance decision:** no change to NFL Player Prop Model v2.2, no retroactive grading changes, no new probability thresholds approved. This postmortem is preserved as a completed audit with research observations, not a model revision.
