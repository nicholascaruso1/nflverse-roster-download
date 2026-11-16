# NFL Player Prop Model v2.2: Week 10 Sunday 1:00 PM ET slate (KC@ATL, JAX@TEN, CAR@NO, MIN@GB, BUF@NYJ, HOU@CLE, MIA@IND)

Prepared pregame, about 12:55 PM ET Sun Nov 15 2026, from Hard Rock-style app screenshots stamped 12:26-12:29 PM ET (app assumed to be Hard Rock, same as prior locks). Kept separate from the Bet Model. Architecture and weights unchanged. Statuses: PLAY / LEAN / WATCH / PASS / VOID. **This is a partial post-inactives card (Lock 2 state). No Lock 1 exists. Full official inactive lists were NOT retrieved for ATL, JAX, TEN, NO, GB or MIN (see section 3), so Opportunity and Scenario Confidence are capped at Medium.** The pilot v0.1 probabilities in section 6 were computed AFTER seeing these prices (not a blind pre-registration). One consolidated file by design (card and pilot probabilities together).

## 1. Result (read this first)
- **PLAY: none.** Nothing is Level A: the pilot method is unvalidated and no PLAY can come from it.
- **LEAN (5), all Level B, Data Quality Medium or better. Two more from the second batch (BUF@NYJ, HOU@CLE, MIA@IND, section 9): Deion Burks U1.5 rec (+125) and Laquon Treadwell U2.5 rec (-160), both IND WRs, one correlated cluster.**
  Original three:
  1. **Bryce Young (CAR) UNDER 9.5 rush yards (-115)**: independent of the others.
  2. **Bijan Robinson (ATL) UNDER 3.5 receptions (+125)** and 3. **Kyle Pitts (ATL) UNDER 3.5 receptions (+115)**: these two share one mechanism (ATL pass volume) and are **one correlated cluster**, never independent evidence.
- **WATCH (13):** London U5.5 rec, Worthy O2.5 rec, Penix U219.5 pass yds, Rice U5.5 rec (KC@ATL); Pollard O56.5 rush, Spears U10.5 rush, Lawrence U247.5 pass yds, Washington U4.5 rec (JAX@TEN); Shough U252.5 pass yds, Kamara O12.5 rush (CAR@NO); Jefferson U7.5 rec, Love U3.5 rush, Lloyd O12.5 rush (MIN@GB). Section 5 says why none was promoted.
- **PASS / Level C:** everything else screened (section 5). **No quantified TD edge** (no recorded pregame probability, Addendum B). Receiving-yard props are not modeled.
- **No parlay. No numeric joint probability.**
- Most of the board is Under-leaning in my pilot output. That is a property of the unvalidated method (no matchup or game-script term, Poisson and negative-binomial shapes) as much as of the market, which is why only 3 of roughly 70 modeled props were promoted and most numeric passes were held back by role flags.

## 2. Data and availability audit
- Usage and logs: my computation from nflverse 2026 play-by-play (weeks 1-10, 24,002 plays, downloaded about 12:30 PM ET; week 10 so far contains only WAS @ NYG and NE @ DET is not in the file yet). Snap counts (nflverse snap_counts_2026) define active weeks (offense snaps > 0). Rosters from nflverse roster_2026.
- Prices: screenshots, 12:26-12:29 PM ET, read by me. **Rows hidden behind the nav bar are unread:** Noah Gray (KC) receptions and receiving yards, Tony Pollard and Brian Thomas Jr. (receptions, JAX/TEN), Tommy Tremble (CAR) receptions, Myles Price (MIN) receptions, the TD boards below roughly +450 (KC@ATL), +425 (JAX@TEN), +300 (CAR@NO) and +475 (MIN@GB), and every defense, kicker and alt market.
- Game lines are NOT in these screenshots. Implied points use the Hard Rock 11:40 AM lines recorded in the Lock 2 Bet Model card (may have moved): KC -3 / 47 (KC 25.0, ATL 22.0); JAX -11.5 / 45.5 (JAX 28.5, TEN 17.0); NO -1.5 / 49 (NO 25.25, CAR 23.75); GB -2.5 / 42.5 (GB 22.5, MIN 20.0). Weather not checked.
- ff_opportunity for 2026 was not rechecked (Week 10 Lock 3 said it does not exist), so anytime TDs stay unpriced.
- Model omission that matters: QB kneel-downs are excluded from my rushing data but count in official stats. Kneels can only lower QB rush yardage, so they help the Young Under and hurt QB Overs.
- League inputs (weeks 1-10): 4.33 ypc (QB carries 5.56), 6.23 yds per pass attempt, pass TDs per point 0.0660.

## 3. Availability (V = verified on a Nov 15 2026 page, R = reported/designation, U = unverified)
- **KC:** RB Kenneth Walker III **OUT** (groin; V: CBS tracker, Yahoo, NFL.com); OT Jaylon Moore and DT Peter Woods **OUT** (V: CBS). CBS's Chiefs section lists no other out names, so Mahomes, Rice, Kelce and Worthy are assumed active (U). **WR Josh Downs is making his Chiefs debut (R: CBS video headline); all 9 of his 2026 games in my data are with IND (w1-9)**, so he has no KC sample. Isiah Pacheco appears on a third-party injured-reserve list (R).
- **ATL:** inactive list not retrieved (U). Penix, London, Pitts, Bijan, Dotson, Herbert assumed active because the book prices them.
- **JAX:** DT Jordan Davis and S Jessie Bates **OUT**, resting (V: Jaguars via Yahoo live blog). Full list not retrieved (U). **TEN:** RB Tyjae Spears was questionable and is **ACTIVE** (V: CBS). Full list not retrieved (U).
- **CAR:** NFL.com Sunday report lists RB Jonathon Brooks, OL Brady Christensen, LB Bobby Okereke and CB Mike Jackson OUT (R). **NO:** RB CJ Donaldson, OT Taliese Fuaga, C Erik McCoy, DL Christen Miller OUT (R, matches the Lock 2 card); **RB Travis Etienne Jr. is ACTIVE for the first time since Week 3** (V: Saints post via Bleacher Report/Yahoo); snap count unknown.
- **MIN:** WR Jordan Addison **inactive** (V: NFL.com, CBS); NFL.com's report also lists QB Kyler Murray, WR Jauan Jennings, TE T.J. Hockenson, LB Blake Cashman and DL Tyrion Ingram-Dawkins OUT (R, designations, not the 11:30 AM list). **Kirk Cousins set to start** (R, video headline). **GB:** RB Josh Jacobs **OUT** (V: CBS). Skyy Moore, Lukas Van Ness, RB Chris Brooks and Javon Bullard were questionable and **unresolved** in what I retrieved (U).

## 4. Team context (nflverse 2026, raw, not opponent-adjusted)
| | Off EPA/play | Def EPA/play allowed | Pass att/g | Rush att/g | Opp rush: ypc allowed | Opp pass: yds/att allowed |
|---|---|---|---|---|---|---|
| KC | +0.119 | -0.053 | 34.3 | 26.3 | 3.67 | 5.86 |
| ATL | -0.061 | 0.000 | 30.1 | 27.9 | 4.62 | 6.09 |
| JAX | +0.113 | -0.109 | 29.9 | 27.9 | 3.80 | 6.61 |
| TEN | -0.076 | +0.059 | 32.6 | 23.5 | 4.33 | 7.10 |
| CAR | +0.026 | +0.050 | 42.1 | 23.0 | 4.75 | 5.83 |
| NO | -0.028 | +0.056 | 40.9 | 25.0 | 4.79 | 6.83 |
| MIN | -0.151 | -0.168 | 30.8 | 24.9 | 4.39 | 4.92 |
| GB | +0.045 | -0.050 | 39.8 | 21.7 | 4.15 | 5.52 |

**Scenario branches (qualitative, no probabilities).** Branches: (A) favored-to-trail team controls anyway, (B) competitive/balanced, (C) favored-narrative team dominates, (D) low-scoring, suppressed volume.
- **KC @ ATL:** B most likely, C moderate, A and D low. Volume: ATL pass volume rises if it trails (the sensitivity that matters for the ATL Under cluster); KC without Walker leans pass. Lead-creation tag: pass-driven.
- **JAX @ TEN (JAX -11.5):** C most likely, B moderate, D moderate (total 45.5), A low. Volume: JAX rush volume up, TEN carries down and TEN pass volume up if trailing. Tag: clock-control rushing (JAX), pass-driven (TEN, trailing).
- **CAR @ NO:** B most likely; D low to moderate; A and C low. Volume: both pass-heavy (CAR 42.1 and NO 40.9 attempts per game). Tag: pass-driven.
- **MIN @ GB:** B and D most likely (total 42.5 is the lowest on the board), C low-moderate, A low. Volume: MIN pass volume and target distribution are uncertain (first Cousins game, three pass catchers out); GB pass-heavy (39.8 att/g, rush EPA -0.255). Tag: pass-driven (GB), defensive-turnover (MIN) at best.

## 5. Props by status
**Lines:** screenshots 12:26-12:29 PM ET. Break-even (BE) = raw implied probability of the quoted price (same convention as prior cards). Edge = model probability of the side minus BE, in points.

### LEAN
| Prop | Line / price | Evidence | DQ | Level | Opp. / Scenario Conf. |
|---|---|---|---|---|---|
| **Bryce Young UNDER rush yds** | U9.5 -115 (BE 53.5%) | Rush yds by game (8): 10, 6, 0, 7, 8, 9, 0, 13. **Under 7 of 8.** Carries 2, 1, 0, 1, 1, 1, 0, 1; EW mean 0.8, ypc 5.80 (shrunk toward league QB 5.56), NO allows 4.79 ypc (x1.053 adj). Pilot P(Under) 81.5%, edge +28.1, **min +25.1** (vol +15%). Stress: still 72.0% at 1.5x carries, 62.9% at 2.0x (+9.4 edge), breaks even only near 2.5x (47.4% at 3.0x). Scramble-tail check run (league QB carry distribution): included in min edge. | High | B | Opp. **80/100** (starter, role stable, carries flat at 0-2); Scenario **Medium** |
| **Bijan Robinson UNDER receptions** | U3.5 +125 (BE 44.4%) | Rec (last 8): 3, 2, 1, 4, 2, 5, 0, 6; **Over 3 of 8**. Targets 4, 2, 2, 7, 2, 5, 1, 7; EW 4.3, catch .78 (RB prior .78). Pilot P(Under) 58.0%, edge +13.6, **min +4.3** (vol +15%). Stress: 68.2% at -15% volume, 48.7% at +15%, 40.3% at +30%; **breaks even near +20% target volume.** | Medium | B | Opp. **65/100** (ATL inactives unverified); Scenario **Medium** |
| **Kyle Pitts UNDER receptions** | U3.5 +115 (BE 46.5%) | Rec (last 8): 1, 1, 3, 5, 5, 5, 2, 3; **Over 3 of 8**. Targets 3, 2, 3, 6, 7, 5, 5, 5; EW 4.8, catch .69 (TE prior .72). Pilot P(Under) 59.3%, edge +12.8, **min +3.5** (vol +15%). Stress: 69.1% at -15%, 50.1% at +15%, 41.4% at +30%; **breaks even near +20% target volume.** | Medium | B | Opp. **65/100** (ATL inactives unverified); Scenario **Medium** |

**Thresholds recorded (Addendum B):** Young Over needs 10+ rush yards, about 2 carries or one 10+ yard scramble. Bijan Over needs 4 receptions, about 5 to 6 targets at his catch rate. Pitts Over needs 4 receptions, about 6 targets at his catch rate.
**Cluster note:** the Bijan and Pitts Unders fail together if ATL trails and Penix throws 40+ (Penix attempts this year: 25, 21, 35, 38, 33, 24, 31). Both also sit on a market that prices the Overs at -165 and -150. The market gap is large (model Over 42% and 41%), so the divergence layer is an audit trigger here, not confirmation.
**Kill conditions (my stated conditions, not calibrated):** any ATL skill-position inactive that raises Bijan or Pitts volume (London, Dotson, Herbert, Penix), or Bijan/Pitts price worse than +105/+100. For Young: a CAR QB injury (backup would change the prop) or price worse than -135. A QB injury to either side changes remaining props for both teams (section 7).

### WATCH (not promoted)
| Prop | Line / price | Pilot (base / min edge) | Why not LEAN |
|---|---|---|---|
| London U5.5 rec (ATL) | U -105 (BE 51.2%) | P(U) 64.5%, +13.3 / +2.6 | Passes the numeric gate; **held back as the third prop on the same ATL pass-volume mechanism** (analyst judgment, not a governance rule). Rec (8): 4, 9, 5, 7, 4, 7, 1, 5; Under 5 of 8. |
| Worthy O2.5 rec (KC) | O -135 (BE 57.4%) | P(O) 73.4%, +16.0 / +6.7 | **Role-shift flag:** Downs debuts, Walker out, Rice back (2 games since return). Over 7 of 8 games. Stress: 64.2% at -15% targets, 52.7% at -30% (BE 57.4%). |
| Penix U219.5 pass yds (ATL) | U -115 | P(U) 68.0%, +14.5 / **+0.2** | Fails the stability gate (vol +15%). Under 219.5 in only 3 of 7 (pass yds 256, 223, 240, 225, 213, 125, 162), so history does not back the model. |
| Rice U5.5 rec (KC) | U -125 (BE 55.6%) | P(U) 74.0%, +18.5 / **-0.7** | Fails last-2 check (8 and 7 targets since return); Downs flag. |
| Pollard O56.5 rush (TEN) | O -115 | P(O) 67.1%, +13.6 / +1.8 | **Role-shift flag:** carries 25 and 21 in wk7-8 came while Spears had 0 snaps; Spears is active today. TEN is an 11.5-point underdog. Stress: 55.3% at -15% carries, 46.5% at -25% (BE 53.5%). Over needs about 14-15 carries. |
| Spears U10.5 rush (TEN) | U -120 (BE 54.5%) | P(U) 63.9%, +9.3 / +3.8 | Returning from knee, snaps 11-34, unknown workload; g=6, last game wk6. |
| Lawrence U247.5 pass yds (JAX) | U -115 | P(U) 62.8%, +9.3 / -4.8 | Fails stability. JAX -11.5 supports fewer attempts but the Under is not stable to volume +15%. Under in 6 of 8. |
| Washington U4.5 rec (JAX) | U -150 (BE 60.0%) | P(U) 69.2%, +9.2 / **+0.3** | Fails stability; targets 6, 12, 5, 3, 9, 11, 2, 7. |
| Shough U252.5 pass yds (NO) | U -115 | P(U) 69.9%, +16.4 / **+1.0** | Fails stability (vol +15%). **History disagrees with the model:** Over 252.5 in 5 of 8 (pass yds 410, 252, 255, 286, 96, 144, 278, 265); attempts 62, 37, 44, 50, 26, 30, 40, 40. |
| Kamara O12.5 rush (NO) | O -120 (BE 54.5%) | P(O) 73.0%, +18.5 / +10.3 | **Role-shift flag: Etienne Jr. returns** (3 games all year, hamstring). Stress: 59.2% at 0.75x carries, 43.7% at 0.55x. |
| Jefferson U7.5 rec (MIN) | U -145 (BE 59.2%) | P(U) 84.8%, +25.6 / +11.7 | **Role-shift flag (largest on the board):** Addison, Jennings, Hockenson out and Cousins' first MIN game. Stress: Under 71.2% at 10 targets, 56.1% at 12, 42.6% at 14; **breaks even near 11 targets** (EW 8.0, last game 11). Rec (7): 8, 3, 2, 6, 4, 5, 3. |
| Love U3.5 rush (GB) | O -120 / U -110 (BE 52.4%) | P(U) 65.9%, +13.5 / +9.6 | **Model and history disagree:** Over 3.5 in 4 of 8 (0, 0, 4, 6, 14, 0, 0, 13 yds) vs model P(Over) 34%. |
| Lloyd O12.5 rush (GB) | O -120 | P(O) 68.4%, +13.8 / **-3.7** | Role shift: Jacobs out, Brooks unresolved; Lloyd had no snaps in wk9 and 3 carries in wk8. |

### PASS / Level C (screened, no verified edge or no valid sample)
| Prop | Line | Reason |
|---|---|---|
| **Emmett Johnson (KC) U3.5 rec -135 / U73.5 rush** | rec 3.5, rush 73.5 | Pilot Unders (88.9% / 99.5%) are **artifacts**: he has been RB2 (0-8 carries, 13-25 snaps). With Walker out he is the lead for the first time, so no sample exists. Level C. |
| **Josh Downs (KC) O2.5 rec +115** | 2.5 | Pilot O 65.0% is from his 9 IND games. No KC sample. Level C. |
| **Bartholomew (MIN) U3.5 rec, Yurosek U1.5 rec** | 3.5 / 1.5 | Pilot Unders (98.4% / 90.3%) are artifacts of TE3 usage (EW 1.1 and 0.7 targets) with Hockenson out. Level C. |
| **Aaron Jones (MIN) O28.5 rush / U2.5 rec; Mason (MIN) U46.5 rush / U1.5 rec** | see table | Jones carries 8, 5, 5 over wk7-9 vs 12-25 early (min -29.2); Mason has 4 games. MIN backfield with a new QB and no Hockenson. Level C. |
| **Cousins (MIN) all props** | pass 229.5, TD 1.5, rush 1.5 | **All 9 of his 2026 games are with LV**; no MIN offense sample. Pass yds edge +0.3. Rush O1.5 pilot +14.4 is not trusted: model 66% vs Over 4 of 8, plus the kneel omission. Level C. |
| **Etienne Jr. O30.5 rush; Estime O24.5 rush; T. Etienne U7.5 rush** | 30.5 / 24.5 / 7.5 | Etienne: g=3 (last played wk3), hamstring return. Estime: g=2, both as the fill-in lead (83% is an artifact). Level C. |
| **Tyson (NO) U4.5 rec; Herbert (ATL) U9.5 rush; Dike (TEN) U2.5 rec** | see table | g=1, g=3, and a single role game (wk8: 6 targets, 63 snaps). Pilot edges (+12.8, +10.4, +31.9) are sample artifacts. Level C. |
| Waller O2.5 rec (CAR) | O -115 | Pilot Over +7.6 but min -2.3, and he cleared 3 catches in only 3 of 8 games (w9: 10 targets, 8 rec). |
| Coker U4.5, Olave O5.5, McMillan O5.5, Hubbard O3.5, Vele O3.5, J. Johnson U2.5, Kamara O2.5 rec (CAR/NO) | see table | No edge above +7.4 survives (min edges -2.7 to -12.2). Kamara O2.5 rec +9.2 base, **min -0.0**, same Etienne flag as his rush prop. |
| Kelce, Dotson, Bijan rush U84.5, Pitts/London other lines, Mahomes rush/pass yds/pass TD, Penix rush/TD | see table | Base edges at or below +4.1 and/or min edges negative. Kelce O4.5: model Over 41.8% (-2.7). Mahomes U243.5 +2.6 / -12.6. |
| Meyers, Strange, Helm, Ayomanor, Robinson, Tuten, C. Rodriguez, Ward, Lawrence rush/TD, Hubbard rush, Young pass/TD, Shough rush/TD | see table | No edge or fails the stability check. Pass TD props: Poisson is unvalidated and Young reached 2+ TD in 5 of 8, Love in 8 of 9, so the pilot's pass-TD Unders are not used. |
| Golden O5.5 rec (GB) | O +105 | +7.4 / -5.9 (vol -15%). Targets EW 10.7, catch .58. Near fair. |
| Watson, Kraft, S. Williams, Love pass/TD, K. Johnson rush, Brooks rush | see table | No edge or min fails. Love Over 254.5 in 7 of 9 and Love 2+ TD in 8 of 9 (against the pilot's Under). Brooks: 4 games, ankle-questionable. |
| **Anytime TD / 2+ TD (all)** | KC@ATL: Bijan -225, E. Johnson -175, London +145, Rice +170, Kelce +200, Pitts +240, Worthy +300, Downs +325, Dotson +400, Mahomes +450; JAX@TEN: Tuten -115, Pollard +120, Washington +125, C. Rodriguez +160, Meyers +230, Strange +240, Lawrence +300, Robinson +300, Dike +425, Ayomanor +425; CAR@NO: Hubbard -160, McMillan +130, Olave +150, Etienne +170, Coker +210, Tyson +230, Estime +275, J. Johnson +275, Shough +275, Kamara +300; MIN@GB: Jefferson +125, Watson +140, Golden +165, Mason +220, K. Johnson +220, Kraft +220, A. Jones +250, Bartholomew +350, Brooks +400 | **No legitimate recorded pregame probability, so no quantified TD edge.** TD props stay Level B at best, no official TD PLAY (Addendum B). |
| Receiving yards (all) | London 71.5, Rice 56.5, Kelce 48.5, Pitts 37.5, Bijan 28.5, Dotson 28.5, Worthy 27.5, E. Johnson 26.5, Downs 22.5 (KC@ATL); Washington 61.5, Meyers 41.5, Robinson 38.5, Strange 35.5, Dike 30.5, Helm 26.5, Ayomanor 26.5, Tuten 13.5, Spears 12.5 (JAX@TEN); Olave 74.5, McMillan 66.5, Coker 52.5, Tyson 43.5, Vele 29.5, Waller 29.5, J. Johnson 24.5, Hubbard 19.5, Tremble 15.5 (CAR@NO); Jefferson 90.5, Watson 75.5, Golden 70.5, Kraft 36.5, Bartholomew 23.5, Price 21.5, S. Williams 19.5, Felton 19.5, A. Jones 11.5 (MIN@GB) | **Not modeled in the pilot, Level C.** |
| Not on the board or not read | | Noah Gray, Pollard, Brian Thomas Jr., Tremble, Price receptions; Gray and Ridley receiving yards; hidden TD rows; defense, kicker, longest-reception, alt lines. **Coverage sweep:** top-2 targets, primary and secondary RB, TE and QB screened for all eight teams, except the unread rows above. |

## 6. Pilot v0.1 recorded probabilities (unvalidated; recorded after seeing prices)
**Method (identical to Week 8 and Week 10 cards):** volume = negative binomial with exponentially weighted mean (half-life 3 games) over weeks with offense snaps or recorded involvement, zeros included; dispersion r: targets 13.5, carries 8.1, attempts 26.3 (carried over). Receptions = Binomial(targets, catch rate shrunk to position prior with 15 pseudo-targets: WR .62, TE .72, RB .78). Rush and pass yards: per-play yardage drawn from the league 2026 empirical distribution, scaled to the player's ypc/ypa shrunk to league (50 carries / 100 attempts; QB carries shrunk to league QB 5.56), 50% opponent adjustment from raw allowed rates; 40,000 sims; no game-script adjustment. Pass TD = Poisson with lambda = 0.0660 x implied points. Anytime TDs and receiving yards are not priced. Perturbations: volume +/-15%, dispersion x0.5 / x2, last-2-games mean, catch prior 5 / 30 (rec), no opponent adjustment (yards), league QB carry distribution (QB rush), lambda +/-15% and total -3 / +3 (pass TD). Min edge is the worst perturbation for the base best side. **Proposed gate (mine, not governance-approved):** LEAN-eligible only if base edge >= +4.0 pts, min edge >= +1.5, Data Quality >= Medium and no role-shift flag. Stress tests in section 5 (target/carry multipliers) were added after seeing the output and are disclosed as such.

| Player | Market | Line | O / U price | Model P(Over) | Best side | P(best) | Break-even | Base edge (pts) | Min edge across perturbations | Inputs |
|---|---|---|---|---|---|---|---|---|---|---|
| Drake London (ATL) | receptions | 5.5 | -125 / -105 | 35.5% | Under | 64.5% | 51.2% | +13.3 | +2.6 (vol+15) | tgtEW 7.4 catch 0.65 g=9 |
| Rashee Rice (KC) | receptions | 5.5 | -105 / -125 | 26.0% | Under | 74.0% | 55.6% | +18.5 | -0.7 (last2) | tgtEW 5.7 catch 0.73 g=6 |
| Travis Kelce (KC) | receptions | 4.5 | +125 / -160 | 41.8% | Over | 41.8% | 44.4% | -2.7 | -14.0 (vol-15) | tgtEW 6.1 catch 0.70 g=8 |
| Bijan Robinson (ATL) | receptions | 3.5 | -165 / +125 | 41.9% | Under | 58.0% | 44.4% | +13.6 | +4.3 (vol+15) | tgtEW 4.3 catch 0.78 g=9 |
| Kyle Pitts (ATL) | receptions | 3.5 | -150 / +115 | 40.7% | Under | 59.3% | 46.5% | +12.8 | +3.5 (vol+15) | tgtEW 4.8 catch 0.69 g=9 |
| Emmett Johnson (KC) | receptions | 3.5 | +105 / -135 | 11.1% | Under | 88.9% | 57.4% | +31.4 | +26.2 (last2) | tgtEW 2.1 catch 0.83 g=8 |
| Xavier Worthy (KC) | receptions | 2.5 | -135 / +105 | 73.4% | Over | 73.4% | 57.4% | +16.0 | +6.7 (vol-15) | tgtEW 6.0 catch 0.68 g=8 |
| Josh Downs (KC) | receptions | 2.5 | +115 / -150 | 65.0% | Over | 65.0% | 46.5% | +18.5 | +8.5 (vol-15) | tgtEW 6.0 catch 0.59 g=9 |
| Jahan Dotson (ATL) | receptions | 1.5 | -185 / +135 | 54.7% | Under | 45.3% | 42.6% | +2.7 | -4.2 (vol+15) | tgtEW 3.5 catch 0.54 g=9 |
| Bijan Robinson (ATL) | rush yds | 84.5 | -115 / -115 | 44.0% | Under | 56.0% | 53.5% | +2.5 | -8.2 (vol+15) | carEW 18.3 ypc 5.01 adj x0.924 g=9 |
| Emmett Johnson (KC) | rush yds | 73.5 | -115 / -115 | 0.5% | Under | 99.5% | 53.5% | +46.0 | +45.8 (last2) | carEW 3.0 ypc 4.31 adj x1.034 g=8 |
| Patrick Mahomes (KC) | rush yds | 9.5 | -115 / -115 | 42.4% | Under | 57.6% | 53.5% | +4.1 | -1.9 (vol+15) | carEW 2.0 ypc 5.53 adj x1.034 g=8 |
| Khalil Herbert (ATL) | rush yds | 9.5 | -110 / -120 | 35.1% | Under | 64.9% | 54.5% | +10.4 | +5.1 (vol+15) | carEW 2.2 ypc 4.29 adj x0.924 g=3 |
| Michael Penix (ATL) | rush yds | 7.5 | -115 / -115 | 54.3% | Over | 54.3% | 53.5% | +0.8 | -5.9 (vol-15) | carEW 2.5 ypc 5.55 adj x0.924 g=7 |
| Patrick Mahomes (KC) | pass yds | 243.5 | -115 / -115 | 43.9% | Under | 56.1% | 53.5% | +2.6 | -12.6 (vol+15) | attEW 34.7 ypa 6.94 adj x0.989 g=8 |
| Michael Penix (ATL) | pass yds | 219.5 | -115 / -115 | 32.0% | Under | 68.0% | 53.5% | +14.5 | +0.2 (vol+15) | attEW 30.0 ypa 6.55 adj x0.971 g=7 |
| Patrick Mahomes (KC) | pass TD | 1.5 | -145 / +110 | 49.2% | Under | 50.8% | 47.6% | +3.1 | -4.4 (lam+15) | lambda 1.65 (25.00 pts) |
| Michael Penix (ATL) | pass TD | 1.5 | +115 / -155 | 42.5% | Under | 57.5% | 60.8% | -3.2 | -10.6 (lam+15) | lambda 1.45 (22.00 pts) |
| Bhayshul Tuten (JAX) | rush yds | 68.5 | -115 / -115 | 38.5% | Under | 61.5% | 53.5% | +8.0 | -2.5 (vol+15) | carEW 14.9 ypc 4.29 adj x1.000 g=8 |
| Tony Pollard (TEN) | rush yds | 56.5 | -115 / -115 | 67.1% | Over | 67.1% | 53.5% | +13.6 | +1.8 (vol-15) | carEW 18.7 ypc 4.43 adj x0.939 g=8 |
| Chris Rodriguez (JAX) | rush yds | 31.5 | -115 / -115 | 41.1% | Under | 58.9% | 53.5% | +5.4 | -2.6 (vol+15) | carEW 7.4 ypc 4.23 adj x1.000 g=8 |
| Cam Ward (TEN) | rush yds | 10.5 | -110 / -120 | 56.3% | Over | 56.3% | 52.4% | +3.9 | -3.3 (vol-15) | carEW 3.4 ypc 5.21 adj x0.939 g=8 |
| Tyjae Spears (TEN) | rush yds | 10.5 | -110 / -120 | 36.1% | Under | 63.9% | 54.5% | +9.3 | +3.8 (vol+15) | carEW 2.5 ypc 4.15 adj x0.939 g=6 |
| Trevor Lawrence (JAX) | rush yds | 8.5 | -120 / -110 | 43.4% | Under | 56.6% | 52.4% | +4.3 | -1.3 (vol+15) | carEW 1.9 ypc 5.38 adj x1.000 g=8 |
| Trevor Lawrence (JAX) | pass yds | 247.5 | -115 / -115 | 37.2% | Under | 62.8% | 53.5% | +9.3 | -4.8 (vol+15) | attEW 28.9 ypa 7.29 adj x1.070 g=8 |
| Cam Ward (TEN) | pass yds | 201.5 | -115 / -115 | 41.7% | Under | 58.3% | 53.5% | +4.9 | -10.4 (vol+15) | attEW 33.7 ypa 5.56 adj x1.031 g=8 |
| Trevor Lawrence (JAX) | pass TD | 1.5 | -210 / +145 | 56.3% | Under | 43.7% | 40.8% | +2.8 | -4.4 (lam+15) | lambda 1.88 (28.50 pts) |
| Cam Ward (TEN) | pass TD | 0.5 | -230 / +165 | 67.9% | Over | 67.9% | 69.7% | -1.8 | -7.9 (lam-15) | lambda 1.12 (17.00 pts) |
| Wan'Dale Robinson (TEN) | receptions | 4.5 | -135 / +105 | 44.3% | Under | 55.7% | 48.8% | +6.9 | -3.6 (vol+15) | tgtEW 6.5 catch 0.68 g=8 |
| Parker Washington (JAX) | receptions | 4.5 | +115 / -150 | 30.8% | Under | 69.2% | 60.0% | +9.2 | +0.3 (vol+15) | tgtEW 6.6 catch 0.55 g=8 |
| Jakobi Meyers (JAX) | receptions | 3.5 | +100 / -130 | 45.1% | Under | 54.9% | 56.5% | -1.6 | -10.9 (vol+15) | tgtEW 5.1 catch 0.68 g=8 |
| Brenton Strange (JAX) | receptions | 3.5 | +120 / -155 | 43.4% | Over | 43.4% | 45.5% | -2.0 | -37.1 (last2) | tgtEW 4.4 catch 0.78 g=8 |
| Gunnar Helm (TEN) | receptions | 2.5 | -170 / +125 | 47.5% | Under | 52.5% | 44.4% | +8.0 | -22.0 (last2) | tgtEW 3.9 catch 0.68 g=8 |
| Chimere Dike (TEN) | receptions | 2.5 | -145 / +115 | 21.5% | Under | 78.5% | 46.5% | +31.9 | +16.8 (last2) | tgtEW 2.2 catch 0.72 g=8 |
| Elic Ayomanor (TEN) | receptions | 2.5 | +120 / -150 | 34.1% | Under | 65.9% | 60.0% | +5.9 | -20.7 (last2) | tgtEW 3.8 catch 0.54 g=8 |
| Tyjae Spears (TEN) | receptions | 2.5 | +130 / -170 | 44.1% | Over | 44.1% | 43.5% | +0.7 | -8.8 (vol-15) | tgtEW 3.0 catch 0.83 g=6 |
| Bhayshul Tuten (JAX) | receptions | 1.5 | -145 / +115 | 47.4% | Under | 52.6% | 46.5% | +6.1 | -1.0 (vol+15) | tgtEW 1.9 catch 0.86 g=8 |
| Chuba Hubbard (CAR) | rush yds | 80.5 | -115 / -115 | 46.4% | Under | 53.6% | 53.5% | +0.1 | -10.8 (vol+15) | carEW 17.3 ypc 4.54 adj x1.053 g=8 |
| Travis Etienne (NO) | rush yds | 30.5 | -120 / -110 | 66.4% | Over | 66.4% | 54.5% | +11.9 | +2.0 (vol-15) | carEW 10.3 ypc 4.31 adj x1.048 g=3 |
| Audric Estime (NO) | rush yds | 24.5 | -110 / -120 | 83.0% | Over | 83.0% | 52.4% | +30.7 | +23.2 (vol-15) | carEW 12.3 ypc 4.15 adj x1.048 g=2 |
| Tyler Shough (NO) | rush yds | 17.5 | -110 / -120 | 55.2% | Over | 55.2% | 52.4% | +2.8 | -5.6 (vol-15) | carEW 4.4 ypc 5.47 adj x1.048 g=8 |
| Alvin Kamara (NO) | rush yds | 12.5 | -120 / -110 | 73.0% | Over | 73.0% | 54.5% | +18.5 | +10.3 (vol-15) | carEW 6.3 ypc 3.85 adj x1.048 g=7 |
| Bryce Young (CAR) | rush yds | 9.5 | -115 / -115 | 18.5% | Under | 81.5% | 53.5% | +28.1 | +25.1 (vol+15) | carEW 0.8 ypc 5.80 adj x1.053 g=8 |
| Trevor Etienne (CAR) | rush yds | 7.5 | -120 / -110 | 49.2% | Under | 50.8% | 52.4% | -1.6 | -7.3 (vol+15) | carEW 2.4 ypc 3.86 adj x1.053 g=4 |
| Tyler Shough (NO) | pass yds | 252.5 | -115 / -115 | 30.1% | Under | 69.9% | 53.5% | +16.4 | +1.0 (vol+15) | attEW 38.8 ypa 5.78 adj x0.968 g=8 |
| Bryce Young (CAR) | pass yds | 251.5 | -115 / -115 | 53.9% | Over | 53.9% | 53.5% | +0.4 | -17.5 (vol-15) | attEW 41.5 ypa 6.17 adj x1.048 g=8 |
| Bryce Young (CAR) | pass TD | 1.5 | -140 / +110 | 46.5% | Under | 53.5% | 47.6% | +5.9 | -1.5 (lam+15) | lambda 1.57 (23.75 pts) |
| Tyler Shough (NO) | pass TD | 1.5 | -140 / +110 | 49.8% | Under | 50.2% | 47.6% | +2.6 | -5.0 (lam+15) | lambda 1.67 (25.25 pts) |
| Chris Olave (NO) | receptions | 5.5 | -140 / +110 | 61.9% | Over | 61.9% | 58.3% | +3.5 | -9.5 (vol-15) | tgtEW 10.1 catch 0.67 g=8 |
| Tetairoa McMillan (CAR) | receptions | 5.5 | +120 / -155 | 45.9% | Over | 45.9% | 45.5% | +0.5 | -12.2 (vol-15) | tgtEW 8.6 catch 0.64 g=8 |
| Jalen Coker (CAR) | receptions | 4.5 | -105 / -125 | 37.1% | Under | 62.9% | 55.6% | +7.4 | -2.7 (vol+15) | tgtEW 6.3 catch 0.63 g=7 |
| Jordyn Tyson (NO) | receptions | 4.5 | +125 / -160 | 25.7% | Under | 74.3% | 61.5% | +12.8 | +4.1 (vol+15) | tgtEW 5.0 catch 0.67 g=1 |
| Chuba Hubbard (CAR) | receptions | 3.5 | +105 / -135 | 49.5% | Over | 49.5% | 48.8% | +0.7 | -9.5 (vol-15) | tgtEW 4.6 catch 0.82 g=8 |
| Devaughn Vele (NO) | receptions | 3.5 | +115 / -150 | 51.3% | Over | 51.3% | 46.5% | +4.8 | -11.6 (last2) | tgtEW 5.8 catch 0.66 g=8 |
| Juwan Johnson (NO) | receptions | 2.5 | -150 / +115 | 52.5% | Under | 47.5% | 46.5% | +1.0 | -7.6 (vol+15) | tgtEW 4.0 catch 0.72 g=8 |
| Alvin Kamara (NO) | receptions | 2.5 | -135 / +110 | 66.7% | Over | 66.7% | 57.4% | +9.2 | -0.0 (vol-15) | tgtEW 4.5 catch 0.80 g=7 |
| Darren Waller (CAR) | receptions | 2.5 | -115 / -115 | 61.0% | Over | 61.0% | 53.5% | +7.6 | -2.3 (vol-15) | tgtEW 4.9 catch 0.68 g=8 |
| Jordan Love (GB) | pass yds | 254.5 | -115 / -115 | 39.5% | Under | 60.5% | 53.5% | +7.0 | -8.8 (vol+15) | attEW 38.9 ypa 6.86 adj x0.895 g=9 |
| Kirk Cousins (MIN) | pass yds | 229.5 | -115 / -115 | 46.2% | Under | 53.8% | 53.5% | +0.3 | -15.1 (vol+15) | attEW 35.5 ypa 6.85 adj x0.943 g=9 |
| Jordan Love (GB) | pass TD | 1.5 | -125 / -105 | 43.6% | Under | 56.4% | 51.2% | +5.1 | -2.2 (lam+15) | lambda 1.48 (22.50 pts) |
| Kirk Cousins (MIN) | pass TD | 1.5 | +135 / -175 | 38.3% | Under | 61.7% | 63.6% | -1.9 | -8.5 (lam+15) | lambda 1.32 (20.00 pts) |
| Jordan Mason (MIN) | rush yds | 46.5 | -115 / -115 | 35.3% | Under | 64.7% | 53.5% | +11.2 | +1.3 (vol+15) | carEW 10.0 ypc 4.24 adj x0.979 g=4 |
| Kaleb Johnson (GB) | rush yds | 29.5 | -115 / -115 | 45.7% | Under | 54.3% | 53.5% | +0.8 | -7.3 (vol+15) | carEW 7.5 ypc 4.22 adj x1.006 g=6 |
| Aaron Jones (MIN) | rush yds | 28.5 | -115 / -115 | 72.4% | Over | 72.4% | 53.5% | +18.9 | -29.2 (last2) | carEW 11.7 ypc 4.18 adj x0.979 g=8 |
| Chris Brooks (GB) | rush yds | 15.5 | -115 / -115 | 37.6% | Under | 62.4% | 53.5% | +8.9 | +2.4 (vol+15) | carEW 3.4 ypc 4.41 adj x1.006 g=4 |
| MarShawn Lloyd (GB) | rush yds | 12.5 | -120 / -110 | 68.4% | Over | 68.4% | 54.5% | +13.8 | -3.7 (last2) | carEW 6.3 ypc 3.42 adj x1.006 g=8 |
| Jordan Love (GB) | rush yds | 3.5 | -120 / -110 | 34.1% | Under | 65.9% | 52.4% | +13.5 | +9.6 (vol+15) | carEW 0.7 ypc 5.52 adj x1.006 g=9 |
| Kirk Cousins (MIN) | rush yds | 1.5 | -105 / -125 | 65.7% | Over | 65.7% | 51.2% | +14.4 | +8.9 (vol-15) | carEW 1.7 ypc 4.80 adj x0.979 g=9 |
| Justin Jefferson (MIN) | receptions | 7.5 | +115 / -145 | 15.2% | Under | 84.8% | 59.2% | +25.6 | +11.7 (last2) | tgtEW 8.0 catch 0.61 g=7 |
| Matthew Golden (GB) | receptions | 5.5 | +105 / -135 | 56.2% | Over | 56.2% | 48.8% | +7.4 | -5.9 (vol-15) | tgtEW 10.7 catch 0.58 g=9 |
| Christian Watson (GB) | receptions | 4.5 | -145 / +110 | 59.0% | Over | 59.0% | 59.2% | -0.2 | -11.6 (vol-15) | tgtEW 8.3 catch 0.66 g=9 |
| Tucker Kraft (GB) | receptions | 3.5 | -155 / +120 | 51.1% | Under | 48.9% | 45.5% | +3.5 | -6.3 (vol+15) | tgtEW 5.5 catch 0.70 g=9 |
| Gavin Bartholomew (MIN) | receptions | 3.5 | +125 / -165 | 1.6% | Under | 98.4% | 62.3% | +36.2 | +35.4 (vol+15) | tgtEW 1.1 catch 0.77 g=6 |
| Savion Williams (GB) | receptions | 2.5 | +130 / -180 | 40.8% | Over | 40.8% | 43.5% | -2.7 | -11.5 (vol-15) | tgtEW 3.2 catch 0.72 g=4 |
| Aaron Jones (MIN) | receptions | 2.5 | +140 / -185 | 27.8% | Under | 72.2% | 64.9% | +7.3 | +0.2 (vol+15) | tgtEW 2.4 catch 0.75 g=8 |
| Jordan Mason (MIN) | receptions | 1.5 | +135 / -180 | 26.3% | Under | 73.7% | 64.3% | +9.5 | +4.3 (vol+15) | tgtEW 1.5 catch 0.69 g=4 |
| Ben Yurosek (MIN) | receptions | 1.5 | +115 / -150 | 9.7% | Under | 90.3% | 60.0% | +30.3 | +23.9 (last2) | tgtEW 0.7 catch 0.71 g=4 |

**Gate result:**
- Numeric gate passes (base >= +4.0 and min >= +1.5): London U5.5 rec, Bijan U3.5 rec, Pitts U3.5 rec, Worthy O2.5 rec, Downs O2.5 rec, E. Johnson U3.5 rec and U73.5 rush, Herbert U9.5 rush, Pollard O56.5 rush, Spears U10.5 rush, Dike U2.5 rec, Etienne Jr. O30.5 rush, Estime O24.5 rush, Kamara O12.5 rush and O2.5-rec (rec fails at min -0.0), Young U9.5 rush, Tyson U4.5 rec, Mason U1.5 rec and U46.5-rush (rush fails at +1.3), Love U3.5 rush, Cousins O1.5 rush, Jefferson U7.5 rec, Bartholomew U3.5 rec, Yurosek U1.5 rec, Brooks U15.5 rush.
- **Of those, only three clear the full gate with Data Quality >= Medium, no role-shift flag and agreement with history: Young U9.5 rush, Bijan U3.5 rec, Pitts U3.5 rec.** London passes numerically and was held to WATCH for cluster concentration (analyst judgment). The rest fail on role-shift flags (Worthy, Pollard, Spears, Kamara, Jefferson, Lloyd, Mason, Brooks), sample size (Downs, E. Johnson, Herbert, Dike, Etienne Jr., Estime, Tyson, Bartholomew, Yurosek), model-vs-history disagreement (Love, Cousins) or QB change (Cousins).
- **Known tail issue:** QB carries use the league empirical distribution in the base run; the QB-distribution perturbation addresses the Young prop (included in min edge).

## 7. Correlation and QB injury volatility
- Structural only, no numeric joint probability. **Bijan U3.5 rec and Pitts U3.5 rec share ATL pass volume (positive correlation: both lose if ATL trails and Penix throws a lot).** London U5.5 and Penix U219.5 (both WATCH) share the same mechanism. Young U9.5 rush is independent of the ATL pair. No parlay is authorized.
- QB injury volatility: a QB leaving in any of these games changes both teams' remaining props. The Young LEAN is injury-censored (VOID) only if Young himself leaves early. A CAR QB change would make the prop an unmodeled one.

## 8. Governance
- No weights, components or features changed. No gematria, numerology, jersey-number or birthday inputs used.
- Frozen pregame record. Postgame results are graded against it only, with no hindsight reconstruction. The pilot probabilities add no PLAY or LEAN of their own; official statuses above come from the V2.2 card and Level B review.
- Closing prices are not captured here; CLV unscored unless later screenshots are added.
- Open items for the ledger: full ATL, JAX, TEN, NO, GB and MIN inactive lists, and game lines after 11:40 AM, were not verified before this lock.

## 9. Addendum: the other three 1:00 PM games (BUF @ NYJ, HOU @ CLE, MIA @ IND)
Screenshots stamped 12:31-12:35 PM ET (read by me). Game lines are the Hard Rock 11:40 AM numbers from the Lock 2 card (may have moved): BUF -8 / 51 (BUF 29.5, NYJ 21.5); HOU -3.5 / 40.5 (HOU 22.0, CLE 18.5); IND -4 / 37.5 (IND 20.75, MIA 16.75). Same pilot v0.1 method and gate as section 6, run about 12:50 PM ET, so it is **less than 10 minutes of review before kickoff**. Hidden rows unread: Mason Taylor (NYJ) receptions and receiving yards, Woody Marks and Ollie Gordon receptions, TD board tails.

**Availability (Lock 2 card, not re-verified):** NYJ inactive: Brownlee, Lynn, Patrick, Wallace, Woods; G. Wilson cleared (V). HOU: Hunter and M. Harrison Jr. OUT, Anderson Jr. active (V); full list not retrieved. CLE: Boston active; Watson set to start (R). IND OUT: Travis, Rhodes, Alie-Cox, Tillery, Davis-Gaither, Carlies (V per Lock 2). MIA: Willis on IR, **rookie Kyle McCord makes his first start (R); he has no 2026 NFL sample in my data**, so his rush, pass and TD props are Level C and unmodeled.

### New LEANs (both Level B, Data Quality Medium, IND wide receivers)
| Prop | Line / price | Evidence | Opp. / Scenario Conf. |
|---|---|---|---|
| **Deion Burks (IND) UNDER receptions** | U1.5 **+125** (BE 44.4%) | Rec by game (8): 0, 0, 1, 0, 2, 1, 1, 1; **Under 7 of 8**. Targets 0, 0, 2, 2, 2, 1, 1, 1; offense snaps 3-19; tgtEW 1.2. Pilot P(Under) 82.4%, edge +37.9, **min +33.8** (vol +15%). Over needs 2 catches, about 3 or more targets. | Opp. **60/100** (IND inactives incl. possible WR "Travis" unverified); Scenario **Medium** |
| **Laquon Treadwell (IND) UNDER receptions** | U2.5 **-160** (BE 61.5%) | Rec (8): 3, 1, 5, 2, 2, 2, 1, 0; **Under 6 of 8**. Targets 3, 1, 6, 8, 5, 2, 2, 1 (falling: 2, 2, 1 in last 3). Pilot P(Under) 75.7%, edge +14.1, **min +8.0**. Over needs 3 catches, about 5 targets. Price is steep. | Opp. **60/100**; Scenario **Medium** |

**Cluster note:** Burks and Treadwell Unders share one mechanism (IND pass volume and target share among WRs); both lose together if IND chases and Jones throws 45+ or a WR2/WR3 gets injured. Burks has the better price and a lower threshold. **Kill conditions (mine, uncalibrated):** any IND WR OUT on the 1 PM list (raises both roles), Burks price worse than +105, Treadwell worse than -185, or Daniel Jones out.

### WATCH (not promoted)
- **Braelon Allen (NYJ) O31.5 rush -120:** pilot +29.2 / +21.3, but **role-shift flag**: his 14-24 carry games (w4-8) came while Breece Hall was out; Hall returned w9 (15c, 27 snaps) and Allen had 8c. Hall U53.5 rush is 50.3% and fails.
- **Kevin Coleman Jr. (MIA) U1.5 rec -105:** pilot +17.1 / +11.0, rec 0, 0, 1, 1, 3, 0, 3, 0, but first McCord start changes MIA target distribution; role-shift flag.
- **Jonathan Taylor (IND) U71.5 rush:** +10.5 base but min +0.1 (vol +15%). **Mitchell O2.5 rec (NYJ), Boston O2.5 rec (CLE):** min +0.6 each, fail stability.

### PASS / Level C
- **Level C (no sample):** McCord (all props), Anthony Gould U1.5 rec (g=2, 1 snap per game, pilot +50 is an artifact), Dylan Sampson CLE (g=3), Tank Dell (g=2 for HOU).
- **Fail the gate (min edge negative or base under +4):** every other modeled prop, including Josh Allen and Geno Smith passing yards and TDs, Cook O92.5 (+2.8), Wilson, Shakir, Moore, Kincaid, Kayshon, Collins, Concepcion, Warren, Washington, Douglas, Dulcich, Marks U62.5 (+8.4 / -11.3), Stroud pass, Watson pass and rush, Daniel Jones pass, rush and TD (O1.5 +180: +4.1 / -3.0).
- **TDs:** no quantified TD edge. Boards read: BUF@NYJ Cook -165, Allen -165, Hall +120, B. Allen +180, Kincaid +200, Moore +200, Shakir +210, Wilson +220, Coleman +275, Cooper +350; HOU@CLE Marks +130, Collins +165, Judkins +165, Schultz +250, Boston +260, Fannin +260, Concepcion +275, Dell +325, Hutchinson +350; MIA@IND Taylor -115, Gordon +105, Warren +200, Treadwell +300, McGowan +300, Washington +325, Douglas +350, Dulcich +450, Burks +475, Gould +525. Receiving yards not modeled.

### Pilot v0.1 recorded probabilities (computed after seeing the prices)
| Player | Market | Line | O / U price | Model P(Over) | Best side | P(best) | Break-even | Base edge | Min edge | Inputs |
|---|---|---|---|---|---|---|---|---|---|---|
| Garrett Wilson (NYJ) | receptions | 5.5 | +105 / -140 | 43.3% | Under | 56.7% | 58.3% | -1.7 | -12.6 (vol+15) | tgtEW 8.0 catch 0.67 g=8 |
| Khalil Shakir (BUF) | receptions | 3.5 | -140 / +105 | 47.5% | Under | 52.5% | 48.8% | +3.8 | -5.5 (vol+15) | tgtEW 5.1 catch 0.71 g=8 |
| DJ Moore (BUF) | receptions | 3.5 | -110 / -120 | 39.2% | Under | 60.8% | 54.5% | +6.3 | -3.5 (vol+15) | tgtEW 5.3 catch 0.60 g=6 |
| Dalton Kincaid (BUF) | receptions | 3.5 | -105 / -125 | 46.0% | Under | 54.0% | 55.6% | -1.5 | -10.9 (vol+15) | tgtEW 4.6 catch 0.77 g=8 |
| Omar Cooper Jr. (NYJ) | receptions | 3.5 | +105 / -130 | 55.5% | Over | 55.5% | 48.8% | +6.7 | -4.0 (vol-15) | tgtEW 5.4 catch 0.75 g=5 |
| Adonai Mitchell (NYJ) | receptions | 2.5 | -130 / +100 | 67.1% | Over | 67.1% | 56.5% | +10.6 | +0.6 (vol-15) | tgtEW 7.0 catch 0.52 g=5 |
| Breece Hall (NYJ) | receptions | 2.5 | -105 / -125 | 57.1% | Over | 57.1% | 51.2% | +5.9 | -4.1 (vol-15) | tgtEW 3.6 catch 0.85 g=4 |
| Kenyon Sadiq (NYJ) | receptions | 2.5 | +110 / -140 | 36.2% | Under | 63.8% | 58.3% | +5.5 | -2.3 (vol+15) | tgtEW 3.1 catch 0.69 g=9 |
| Keon Coleman (BUF) | receptions | 2.5 | +115 / -155 | 55.8% | Over | 55.8% | 46.5% | +9.3 | -0.2 (vol-15) | tgtEW 4.5 catch 0.67 g=8 |
| James Cook (BUF) | rush yds | 92.5 | -115 / -115 | 56.3% | Over | 56.3% | 53.5% | +2.8 | -9.8 (vol-15) | carEW 23.1 ypc 4.71 adj x0.996 g=8 |
| Breece Hall (NYJ) | rush yds | 53.5 | -115 / -115 | 49.7% | Under | 50.3% | 53.5% | -3.2 | -13.2 (vol+15) | carEW 15.9 ypc 3.80 adj x0.957 g=4 |
| Braelon Allen (NYJ) | rush yds | 31.5 | -120 / -110 | 83.8% | Over | 83.8% | 54.5% | +29.2 | +21.3 (vol-15) | carEW 14.5 ypc 4.79 adj x0.957 g=9 |
| Josh Allen (BUF) | rush yds | 28.5 | -110 / -120 | 49.1% | Over | 49.1% | 52.4% | -3.2 | -12.1 (vol-15) | carEW 6.1 ypc 5.61 adj x0.996 g=8 |
| Geno Smith (NYJ) | rush yds | 5.5 | -115 / -115 | 43.7% | Under | 56.3% | 53.5% | +2.8 | -2.1 (vol+15) | carEW 1.4 ypc 5.06 adj x0.957 g=9 |
| Josh Allen (BUF) | pass yds | 237.5 | -115 / -115 | 43.5% | Under | 56.5% | 53.5% | +3.0 | -11.8 (vol+15) | attEW 32.4 ypa 7.20 adj x0.989 g=8 |
| Geno Smith (NYJ) | pass yds | 224.5 | -115 / -115 | 37.1% | Under | 62.9% | 53.5% | +9.4 | -5.6 (vol+15) | attEW 33.7 ypa 6.19 adj x0.985 g=9 |
| Josh Allen (BUF) | pass TD | 1.5 | -165 / +130 | 58.1% | Under | 41.9% | 43.5% | -1.6 | -8.8 (lam+15) | lambda 1.95 (29.50 pts) |
| Geno Smith (NYJ) | pass TD | 1.5 | +145 / -195 | 41.3% | Over | 41.3% | 40.8% | +0.5 | -6.7 (lam-15) | lambda 1.42 (21.50 pts) |
| KC Concepcion (CLE) | receptions | 4.5 | +100 / -130 | 37.1% | Under | 62.9% | 56.5% | +6.4 | -3.8 (vol+15) | tgtEW 6.0 catch 0.66 g=9 |
| Nico Collins (HOU) | receptions | 4.5 | +100 / -135 | 36.8% | Under | 63.2% | 57.4% | +5.7 | -4.3 (vol+15) | tgtEW 5.8 catch 0.69 g=6 |
| Harold Fannin Jr. (CLE) | receptions | 3.5 | -160 / +125 | 58.8% | Over | 58.8% | 61.5% | -2.8 | -13.7 (vol-15) | tgtEW 6.1 catch 0.70 g=9 |
| Dylan Sampson (CLE) | receptions | 3.5 | +105 / -135 | 60.3% | Over | 60.3% | 48.8% | +11.5 | +0.3 (vol-15) | tgtEW 5.9 catch 0.74 g=3 |
| Dalton Schultz (HOU) | receptions | 3.5 | +120 / -165 | 51.7% | Over | 51.7% | 45.5% | +6.2 | -4.4 (vol-15) | tgtEW 5.2 catch 0.74 g=8 |
| Denzel Boston (CLE) | receptions | 2.5 | -175 / +130 | 73.2% | Over | 73.2% | 63.6% | +9.6 | +0.6 (vol-15) | tgtEW 7.4 catch 0.55 g=9 |
| Xavier Hutchinson (HOU) | receptions | 2.5 | -165 / +125 | 54.0% | Under | 46.0% | 44.4% | +1.6 | -6.9 (vol+15) | tgtEW 5.3 catch 0.55 g=8 |
| Tank Dell (HOU) | receptions | 2.5 | -150 / +115 | 57.9% | Over | 57.9% | 60.0% | -2.1 | -11.6 (vol-15) | tgtEW 5.5 catch 0.57 g=2 |
| Kayshon Boutte (HOU) | receptions | 1.5 | -155 / +120 | 66.4% | Over | 66.4% | 60.8% | +5.6 | -2.7 (vol-15) | tgtEW 3.6 catch 0.66 g=8 |
| Woody Marks (HOU) | rush yds | 62.5 | -115 / -115 | 38.1% | Under | 61.9% | 53.5% | +8.4 | -11.3 (last2) | carEW 14.1 ypc 3.84 adj x1.061 g=8 |
| Quinshon Judkins (CLE) | rush yds | 43.5 | -115 / -115 | 54.6% | Over | 54.6% | 53.5% | +1.1 | -10.3 (vol-15) | carEW 14.5 ypc 3.62 adj x0.964 g=8 |
| Deshaun Watson (CLE) | rush yds | 21.5 | -120 / -110 | 46.1% | Under | 53.9% | 52.4% | +1.5 | -6.0 (vol+15) | carEW 4.8 ypc 5.34 adj x0.964 g=8 |
| Dylan Sampson (CLE) | rush yds | 18.5 | -115 / -115 | 49.9% | Under | 50.1% | 53.5% | -3.4 | -11.4 (vol+15) | carEW 5.2 ypc 4.45 adj x0.964 g=3 |
| C.J. Stroud (HOU) | rush yds | 8.5 | -120 / -110 | 49.2% | Under | 50.8% | 52.4% | -1.6 | -6.7 (vol+15) | carEW 2.2 ypc 5.58 adj x1.061 g=8 |
| C.J. Stroud (HOU) | pass yds | 245.5 | -115 / -115 | 41.2% | Under | 58.8% | 53.5% | +5.3 | -9.6 (vol+15) | attEW 34.9 ypa 7.03 adj x0.952 g=8 |
| Deshaun Watson (CLE) | pass yds | 208.5 | -115 / -115 | 53.0% | Over | 53.0% | 53.5% | -0.5 | -17.3 (vol-15) | attEW 37.6 ypa 5.90 adj x0.998 g=8 |
| C.J. Stroud (HOU) | pass TD | 1.5 | -120 / -110 | 42.5% | Under | 57.5% | 52.4% | +5.2 | -2.2 (lam+15) | lambda 1.45 (22.00 pts) |
| Deshaun Watson (CLE) | pass TD | 1.5 | +180 / -250 | 34.6% | Over | 34.6% | 35.7% | -1.1 | -7.6 (lam-15) | lambda 1.22 (18.50 pts) |
| Tyler Warren (IND) | receptions | 5.5 | -135 / +105 | 47.6% | Under | 52.4% | 48.8% | +3.6 | -7.4 (vol+15) | tgtEW 7.9 catch 0.72 g=7 |
| Malik Washington (MIA) | receptions | 3.5 | -110 / -120 | 46.0% | Under | 54.0% | 54.5% | -0.6 | -10.4 (vol+15) | tgtEW 5.3 catch 0.67 g=8 |
| Caleb Douglas (MIA) | receptions | 3.5 | +100 / -130 | 51.5% | Over | 51.5% | 50.0% | +1.5 | -9.1 (vol-15) | tgtEW 5.7 catch 0.67 g=5 |
| Greg Dulcich (MIA) | receptions | 3.5 | +100 / -130 | 39.9% | Under | 60.1% | 56.5% | +3.6 | -5.5 (last2) | tgtEW 4.3 catch 0.74 g=8 |
| Jonathan Taylor (IND) | receptions | 3.5 | +105 / -135 | 37.8% | Under | 62.2% | 57.4% | +4.8 | -6.3 (last2) | tgtEW 4.2 catch 0.74 g=9 |
| Laquon Treadwell (IND) | receptions | 2.5 | +120 / -160 | 24.3% | Under | 75.7% | 61.5% | +14.1 | +8.0 (vol+15) | tgtEW 2.9 catch 0.58 g=9 |
| Anthony Gould (IND) | receptions | 1.5 | -165 / +125 | 5.3% | Under | 94.7% | 44.4% | +50.2 | +48.8 (vol+15) | tgtEW 0.6 catch 0.64 g=2 |
| Deion Burks (IND) | receptions | 1.5 | -160 / +125 | 17.6% | Under | 82.4% | 44.4% | +37.9 | +33.8 (vol+15) | tgtEW 1.2 catch 0.64 g=8 |
| Kevin Coleman Jr. (MIA) | receptions | 1.5 | -125 / -105 | 31.7% | Under | 68.3% | 51.2% | +17.1 | +11.0 (vol+15) | tgtEW 2.4 catch 0.48 g=8 |
| Ollie Gordon II (MIA) | rush yds | 74.5 | -115 / -115 | 45.1% | Under | 54.9% | 53.5% | +1.4 | -9.0 (vol+15) | carEW 16.0 ypc 4.33 adj x1.095 g=8 |
| Jonathan Taylor (IND) | rush yds | 71.5 | -115 / -115 | 36.0% | Under | 64.0% | 53.5% | +10.5 | +0.1 (vol+15) | carEW 15.8 ypc 4.13 adj x0.980 g=9 |
| Seth McGowan (IND) | rush yds | 25.5 | -115 / -115 | 41.5% | Under | 58.5% | 53.5% | +5.0 | -2.9 (vol+15) | carEW 5.7 ypc 4.56 adj x0.980 g=9 |
| Jaylen Wright (MIA) | rush yds | 11.5 | -115 / -115 | 52.4% | Over | 52.4% | 53.5% | -1.1 | -8.9 (vol-15) | carEW 3.9 ypc 3.58 adj x1.095 g=6 |
| Daniel Jones (IND) | rush yds | 8.5 | -110 / -120 | 58.2% | Over | 58.2% | 52.4% | +5.8 | -1.1 (vol-15) | carEW 3.0 ypc 4.90 adj x0.980 g=9 |
| Daniel Jones (IND) | pass yds | 184.5 | -115 / -115 | 55.1% | Over | 55.1% | 53.5% | +1.6 | -15.4 (vol-15) | attEW 35.6 ypa 5.15 adj x1.091 g=9 |
| Daniel Jones (IND) | pass TD | 1.5 | +180 / -250 | 39.8% | Over | 39.8% | 35.7% | +4.1 | -3.0 (lam-15) | lambda 1.37 (20.75 pts) |

## Sources
- [CBS Sports Week 10 inactives tracker](https://www.cbssports.com/nfl/news/nfl-week-10-inactives-injury-tracker-latest-news-updates/live/)
- [Yahoo Sports Week 10 live blog](https://sports.yahoo.com/nfl/live/nfl-scores-news-live-updates-week-10-schedule-inactives-highlights-stats-where-to-watch-141718993.html)
- [NFL.com Week 10 injury report](https://www.nfl.com/news/nfl-week-10-injury-report-2026-season)
- [NFL.com Sunday pregame injuries](https://www.nfl.com/news/week-10-injuries-sunday-pregame-2026-nfl-season)
- [Bleacher Report Week 10 live blog](https://bleacherreport.com/liveblogs/25533407-nfl-week-10-live-fantasy-football-start-em-sit-em-lineup-advice-and-latest-injury-updates)
- Week 10 Bet Model Lock 2 card (project doc) for Hard Rock 11:40 AM lines and NO/KC inactives
- nflverse releases: https://github.com/nflverse/nflverse-data (play_by_play_2026, snap_counts_2026, roster_2026, downloaded Nov 15 2026 about 12:30 PM ET)
