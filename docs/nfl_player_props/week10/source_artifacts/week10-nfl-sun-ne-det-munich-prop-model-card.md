# NFL Player Prop Model v2.2: NE @ DET (Week 10, Sun Nov 15 2026, 9:30 AM ET, Allianz Arena, Munich; DET is the designated home team)

Prepared pregame, about 9:28 AM ET (clock check 9:26 ET), after the 8:00 AM ET inactives, from Hard Rock-style app screenshots stamped 9:21 and 9:22 AM ET (app assumed to be Hard Rock, same as prior locks). Kept separate from the Bet Model. Architecture and weights unchanged. Statuses: PLAY / LEAN / WATCH / PASS / VOID. **This is a Lock 2-state card (post-inactives). No Lock 1 exists: no pre-inactives snapshot was captured.** The pilot v0.1 probabilities in section 6 were computed AFTER seeing these prices, so they are not a blind pre-registration. One consolidated file by design (card and pilot probabilities together).

## 1. Result (read this first)
- **PLAY: none.** Nothing is Level A: the pilot method is unvalidated and no PLAY can come from it.
- **LEAN (1): Drake Maye UNDER 27.5 rush yards (-115). Level B, Data Quality Medium.** Opportunity Confidence 70/100, Scenario Confidence Medium.
- **WATCH (4):** Kiner U31.5 rush yds (-115), Gibbs U4.5 rec (-140), A.J. Brown U4.5 rec (-150), Goff O0.5 rush yds (-120).
- **PASS / Level C:** everything else screened (section 5). **No quantified TD edge** (no recorded pregame probability, Addendum B). Receiving-yard props are not modeled (Level B/C at most, no probabilities).
- No parlay. No numeric joint probability.

## 2. Data and availability audit
- Usage and logs: my computation from nflverse 2026 play-by-play through week 10 (NE 9 games, DET 8 games; DET bye wk6; week 10 so far contains only WAS @ NYG). Snap counts (nflverse snap_counts_2026) define active weeks (offense snaps > 0). League rates use weeks 1-10 to date.
- Prices: screenshots, stamped 9:21-9:22 AM ET, read by me. The TD board's lower rows after Jared Goff (+1300) were hidden behind the nav bar and are unread. Game lines are NOT in the screenshots.
- Game lines (third-party, unverified, timing uncertain): DET -2.5, total 50.5-51 (BetMGM via SI: NE +2.5 / O51; Covers early lean page: DET -2.5 / 50.5). Other pages show DET -1.5 and 48.5-49.5 (DraftKings via statsniper, sportsgrid, TeamRankings), treated as older. Base implied points used: DET 26.5, NE 24.0. Weather not checked.
- Not rechecked today: whether ff_opportunity exists for 2026 (Week 10 Lock 3 said it does not), so anytime TDs stay unpriced.
- Model omission that matters for one prop: QB kneel-downs are excluded from my rushing data. Official stats count them, which lowers QB rush totals (affects Goff O0.5).

## 3. Verified availability (8:00 AM ET inactives)
- **NE inactive:** C/G Ben Brown (knee, ruled out Wed), CB Carlton Davis III (knee, ruled out Wed), OL Walter Rouse (concussion), S Brenden Schooler (hamstring), OT Dametrious Crownover, QB Behren Morton (emergency 3rd). **RB TreVeyon Henderson (illness) was ruled out Wed and is now on IR.**
- **NE active, were questionable:** **A.J. Brown** (ankle/knee; missed wks 8-9; limited all week), **Rhamondre Stevenson** (knee tendon, left wk9 in Q3; missed one practice, limited Thu/Fri). Also active: CB Charles Woods, G/C Greg Van Roten (activated from IR Saturday, expected to start LG), FB Reggie Gilliam.
- **DET inactive:** CB D.J. Reed, CB Keith Abney, LB Amen Ogbongbemiga, C Cade Mays, DT Mekhi Wingo, DE Ahmed Hassanein. S Kerby Joseph is out (did not travel, PUP).
- **DET active, were questionable:** WR Amon-Ra St. Brown (rib), RB Sione Vaki (ankle). Goff (chest, limited Wed) is not on the inactive list.
- Sources agree across Patriots.com, Lions.com, Yahoo/SB Nation, Boston Globe and AP.

## 4. Team context (nflverse 2026, raw, not opponent-adjusted)
| | Off EPA/play | Pass / rush EPA | Def EPA/play allowed | Pass / rush allowed | Opp pass att/g, yds/g, ypa | Opp rush att/g, yds/g, ypc |
|---|---|---|---|---|---|---|
| NE | +0.041 | +0.098 / -0.029 | +0.043 | +0.138 / -0.091 | 34.8, 250.7, 7.21 | 23.6, 89.6, 3.80 |
| DET | +0.102 | +0.222 / -0.054 | +0.080 | +0.149 / -0.053 | 43.0, 283.1, 6.58 | 20.5, 80.2, 3.91 |
- Both pass defenses are poor by EPA; both rush defenses are good by EPA. Team rush attempts per game: NE 27.2, DET 28.0; pass attempts per game: NE 33.6, DET 36.6. League: 4.08 ypc, 6.59 ypa.
- **Scenario branches (qualitative, no probabilities):** (A) favored-to-trail team controls anyway: low; (B) competitive/balanced: most likely; (C) DET dominates: moderate; (D) low-scoring, suppressed volume: low (total about 50). Volume direction: both pass volumes are supported by the total; NE rush volume falls if NE trails. Lead-creation tag: pass-driven (both teams).
- Neutral-site international game on a 9:30 AM ET kickoff, with NE traveling a day early; no model adjustment for either.

## 5. Props by status
**Lines:** screenshots 9:21-9:22 AM ET. Break-even = the raw implied probability of the quoted price (same convention as prior cards).

### LEAN
| Prop | Line / price | Evidence | DQ | Level | Opp. / Scenario Conf. |
|---|---|---|---|---|---|
| **Drake Maye UNDER rush yards** | U27.5 -115 (BE 53.5%) | Rush yds by game (9): 47, 20, 18, 56, 29, 25, 26, 8, 3. **Under 6 of 9**, mean 25.8, median 25. Carries: 7, 2, 4, 6, 4, 3, 4, 5, 1; EW mean 3.5, ypc 4.97 (incl. scrambles). 5+ carries in 3 of 9 games. DET allowed QBs 3.6 carries and 23.0 yds per game. Pilot P(Under) 78.8% on the designed-run yardage distribution; with a scramble-inclusive league QB distribution (QB ypc 5.29, 16% of carries 10+) P(Under) is 79%, 72% and 64% at 3.5, 4.2 and 5.0 expected carries. Edge stays above +10 pts at every one of those. | Medium | B | Opp. **70/100** (starter, role stable, carries trending down); Scenario **Medium** |

**Threshold recorded (Addendum B):** Over needs about 5.5 carries at 4.97 ypc, or one 20+ yard scramble.
**Kill conditions (my stated conditions, not calibrated):** line moves to 24.5 or lower, or price moves to -130 or worse (edge priced out); NE trailing script that raises scramble volume (not controllable pregame). QB injury to either side changes the prop (see section 7).

### WATCH (not promoted)
| Prop | Line / price | Evidence | Why not LEAN |
|---|---|---|---|
| Corey Kiner U31.5 rush | U -115 (BE 53.5%) | Yards (9): 11, 0, 18, 0, 52, 57, 13, 38, 55; Under 5 of 9, but Over **3 of the last 4**. Carries 6, 2, 6, 0, 6, 11, 4, 7, 8; EW 6.3 at 4.39 ypc. Pilot P(U) 66.1%, +12.6, min +2.0 (last-2 check). | **Role-shift flag:** Henderson is on IR (out indefinitely) and Stevenson is playing through a knee tendon issue after leaving wk9 in Q3. If Stevenson is limited, Kiner's carries rise. Threshold: Over needs about 7-8 carries at 4.4 ypc. |
| Jahmyr Gibbs U4.5 rec | U -140 (BE 58.3%); O +110 | Rec (8): 5, 6, 7, 4, 5, 5, 2, 0; **Over 5 of 8**. Targets 5, 8, 8, 7, 6, 6, 4, 1. Pilot P(U) 69.8%, +11.4, min +2.4, driven by the last two games (EW targets 4.7). | The edge rests on a two-game target collapse against a season Over rate of 5 of 8; trend, not a verified role change. The Under is already priced at 58.3%. Threshold: Over needs about 6-7 targets at a .76 catch rate. |
| A.J. Brown U4.5 rec | U -150 (BE 60.0%); O +115 | 3 games played: rec 3, 3, 3 on 4, 10, 6 targets (snaps 31, 52, 49); 9 rec / 101 yds total. Pilot P(U) 70.8%, +10.8, min +1.7. | **Data Quality Low** (n=3) and returning from ankle/knee after two missed games and limited practice. Direction is consistent with a snap-managed return, but nothing here verifies it. |
| Jared Goff O0.5 rush yds | O -120 / U -110 (BE 54.5%) | Rush yds (8): 2, 7, 8, 0, 1, 0, 2, 7; Over 6 of 8. Carries 2, 3, 2, 0, 1, 1, 1, 2. Pilot P(O) 63.6%, +9.1, min +4.0. | **Kneel-downs are excluded from my data but count in official stats** (a late-lead kneel can pull the total to 0 or below). Settlement-rule risk makes the number unreliable. |

### PASS / Level C (screened, no verified edge)
| Prop | Line | Reason |
|---|---|---|
| Efton Chism III O0.5 rec | O -180 / U +135 | Pilot P(O) 92.5% (+28.2, min +24.5) **is not trusted**: with A.J. Brown active (wk6, wk7) Chism had 1 target each (0 and 1 rec, 42 and 34 snaps). His two 5-target games (wk8-9) came with Brown out (Hollins was also out in wk8 and back in wk9). Brown and Hollins are both active today. Role-shift flag. |
| Mack Hollins O2.5 rec | O -135 / U +105 | Over 4 of 5 (4, 2, 6, 3, 3 rec). Pilot P(O) 65.5%, +8.0, **min -1.1**. Only wk1 had him active with Brown (5 targets). Returning role with Brown back is unverified. |
| Jameson Williams U3.5 rec | O -130 / U +100 | Rec 4, 2, 4, 6, 2, 5, 4, 1 (Over 4 of 8). Pilot P(U) 59.7%, +9.7, **min +0.7** (fails). |
| A. St. Brown rec 7.5 | O -110 / U -120 | Over 5 of 8 (10, 9, 4, 8, 6, 9, 7, 8); targets 14, 13, 8, 11, 11, 11, 8, 10. Pilot Under +4.1 but **min -8.1**; rib injury, active. No edge. |
| LaPorta rec 4.5 | O +125 / U -160 | Pilot Under +2.7, min -7.5. Under already priced. |
| Douglas 3.5, Henry 3.5, Stevenson 2.5, Raridon 2.5, TeSlaa 1.5 rec | see section 6 | No base edge above +4.5 and all fail the stability check (min edges -12.4 to -4.3). Stevenson rec Over 7 of 9 (5, 1, 3, 3, 3, 0, 5, 3, 3), but the price is -115 both ways and his usage today is knee-limited, so the model's 51% shows no edge. |
| Gibbs rush 90.5 | -115/-115 | P(O) 52.7%, -0.8. Yards (8): 156, 52, 99, 46, 151, 116, 153, 74 (Over 5 of 8) on 15-29 carries. Near fair. |
| Stevenson rush 39.5 | -115/-115 | P(U) 52.2%, -1.3. Yards (9): 51, 43, 22, 47, 64, 36, 22, 82, 32; Over 5 of 9. Knee limits usage; carries 18, 6, 7, 13, 13, 14, 6, 19, 6. Near fair. |
| Vaki rush 12.5 | -115/-115 | +1.9 base, min -5.8. |
| Goff pass 268.5 / Maye pass 264.5 | -115/-115 | Pilot Unders +7.0 / +7.2 but **min -8.8 / -8.9** (volume +15%). Goff Over 5 of 8, Maye Over 4 of 9. Both Unders also fight a total near 50. |
| Goff pass TD 1.5 | O -195 / U +145 | Pilot Under +7.0, **min -0.5**; Poisson unvalidated. Goff 2+ TD in 5 of 8 games. |
| Maye pass TD 1.5 | O -175 / U +135 | Pilot Under +10.5, min +3.1 passes the numeric gate, but Poisson gives P(2+) 47% and Maye had 2+ TD in **6 of 9 games**. Week 8 postmortem already flagged Poisson tail risk for QBs; not used. |
| **Anytime TD / 2+ TD (all)** | Gibbs -275, St. Brown -145, Stevenson +115, A.J. Brown +175, LaPorta +200, J. Williams +220, Henry +230, Kiner +300, Douglas +300, Hollins +300, Maye +325, Raridon +350, TeSlaa +425, Vaki +500, Chism +600, K. Williams +800, Larison +800, B. Wright +900, Goff +1300; 2+ TD Gibbs +190, St. Brown +400, Stevenson +600 | **No legitimate recorded pregame probability, so no quantified TD edge.** TD props stay Level B at best, no official TD PLAY (Addendum B). |
| Receiving yards (all) | St. Brown 84.5, J. Williams 57.5, A.J. Brown 51.5 (O -120 / U -110), LaPorta 42.5, Douglas 40.5, Henry 38.5, Hollins 35.5, Gibbs 32.5, Raridon 26.5, Stevenson 18.5, TeSlaa 15.5, Chism 5.5; all -115/-115 unless noted | **Not modeled in the pilot, Level C.** Season Over counts for reference only, no direction: St. Brown 3/8, J. Williams 3/8, A.J. Brown 0/3, LaPorta 5/8, Douglas 4/9, Henry 5/9, Hollins 4/5, Gibbs 3/8, Raridon 4/8, Stevenson 5/9, TeSlaa 3/8, Chism 5/6. |
| Not on the board or not read | | Kyle Williams (TD board only, +800), Larison TD, Wright, defense, kicker, longest-reception and alt lines. Coverage sweep: top-3 targets, primary and secondary RB, TE and QB screened for both teams. |

## 6. Pilot v0.1 recorded probabilities (unvalidated; recorded after seeing prices)
**Method (identical to Week 8 and Week 10 Lock 3):** volume = negative binomial with exponentially weighted mean (half-life 3 games) over weeks with offense snaps, zeros included; dispersion r: targets 13.5, carries 8.1, attempts 26.3 (carried over). Receptions = Binomial(targets, catch rate shrunk to position prior with 15 pseudo-targets: WR .62, TE .72, RB .78). Rush and pass yards: per-play yardage drawn from the league 2026 empirical distribution, scaled to the player's ypc/ypa shrunk to league (50 carries / 100 attempts), 50% opponent adjustment from raw allowed rates; 40,000 sims; no game-script adjustment. Pass TD = Poisson with lambda = 0.0660 (league pass TD per point, weeks 1-10) x implied points (DET 26.5, NE 24.0, from the unverified total 50.5 and DET -2.5). Anytime TDs and receiving yards are not priced. Perturbations: volume +/-15%, dispersion x0.5 / x2, last-2-games mean, catch prior 5 / 30 (rec), no opponent adjustment (yards), lambda +/-15% and total 46.5 / 53 (pass TD). **Proposed gate (mine, not governance-approved):** LEAN-eligible only if base edge >= +4.0 pts, min edge >= +1.5, Data Quality >= Medium and no role-shift flag.

| Player | Market | Line | O / U price | Model P(Over) | Best side | P(best) | Break-even | Base edge (pts) | Min edge across perturbations | Inputs |
|---|---|---|---|---|---|---|---|---|---|---|
| Amon-Ra St. Brown | receptions | 7.5 | -110 / -120 | 41.4% | Under | 58.6% | 54.5% | +4.1 | -8.1 (vol+15) | tgtEW 10.2 catch 0.70 g=8 |
| Jahmyr Gibbs | receptions | 4.5 | +110 / -140 | 30.2% | Under | 69.8% | 58.3% | +11.4 | +2.4 (vol+15) | tgtEW 4.7 catch 0.76 g=8 |
| A.J. Brown | receptions | 4.5 | +115 / -150 | 29.2% | Under | 70.8% | 60.0% | +10.8 | +1.7 (vol+15) | tgtEW 6.8 catch 0.52 g=3 |
| Sam LaPorta | receptions | 4.5 | +125 / -160 | 35.7% | Under | 64.3% | 61.5% | +2.7 | -7.5 (vol+15) | tgtEW 5.5 catch 0.72 g=8 |
| Jameson Williams | receptions | 3.5 | -130 / +100 | 40.3% | Under | 59.7% | 50.0% | +9.7 | +0.7 (vol+15) | tgtEW 5.3 catch 0.61 g=8 |
| DeMario Douglas | receptions | 3.5 | +100 / -130 | 48.1% | Over | 48.1% | 50.0% | -1.9 | -12.4 (vol-15) | tgtEW 5.6 catch 0.66 g=9 |
| Hunter Henry | receptions | 3.5 | +105 / -135 | 42.6% | Under | 57.4% | 57.4% | +0.0 | -9.6 (vol+15) | tgtEW 4.1 catch 0.82 g=9 |
| Mack Hollins | receptions | 2.5 | -135 / +105 | 65.5% | Over | 65.5% | 57.4% | +8.0 | -1.1 (vol-15) | tgtEW 5.4 catch 0.67 g=5 |
| Rhamondre Stevenson | receptions | 2.5 | -115 / -115 | 51.0% | Over | 51.0% | 53.5% | -2.5 | -12.1 (vol-15) | tgtEW 3.5 catch 0.80 g=9 |
| Eli Raridon | receptions | 2.5 | +135 / -185 | 47.0% | Over | 47.0% | 42.6% | +4.5 | -4.5 (vol-15) | tgtEW 4.0 catch 0.65 g=8 |
| Isaac TeSlaa | receptions | 1.5 | +120 / -160 | 36.1% | Under | 63.9% | 61.5% | +2.3 | -4.3 (vol+15) | tgtEW 2.4 catch 0.53 g=8 |
| Efton Chism III | receptions | 0.5 | -180 / +135 | 92.5% | Over | 92.5% | 64.3% | +28.2 | +24.5 (vol-15) | tgtEW 3.8 catch 0.74 g=6 |
| Jahmyr Gibbs | rush yds | 90.5 | -115 / -115 | 52.7% | Over | 52.7% | 53.5% | -0.8 | -13.9 (vol-15) | carEW 22.5 ypc 4.45 g=8 |
| Rhamondre Stevenson | rush yds | 39.5 | -115 / -115 | 47.8% | Under | 52.2% | 53.5% | -1.3 | -11.0 (vol+15) | carEW 11.1 ypc 3.89 g=9 |
| Corey Kiner | rush yds | 31.5 | -115 / -115 | 33.9% | Under | 66.1% | 53.5% | +12.6 | +2.0 (last2) | carEW 6.3 ypc 4.39 g=9 |
| Drake Maye | rush yds | 27.5 | -115 / -115 | 21.2% | Under | 78.8% | 53.5% | +25.3 | +20.0 (vol+15) | carEW 3.5 ypc 4.97 g=9 |
| Sione Vaki | rush yds | 12.5 | -115 / -115 | 55.4% | Over | 55.4% | 53.5% | +1.9 | -5.8 (vol-15) | carEW 4.4 ypc 4.09 g=8 |
| Jared Goff | rush yds | 0.5 | -120 / -110 | 63.6% | Over | 63.6% | 54.5% | +9.1 | +4.0 (vol-15) | carEW 1.4 ypc 3.60 g=8 |
| Jared Goff | pass yds | 268.5 | -115 / -115 | 39.5% | Under | 60.5% | 53.5% | +7.0 | -8.8 (vol+15) | attEW 33.9 ypa 7.46 g=8 |
| Drake Maye | pass yds | 264.5 | -115 / -115 | 39.3% | Under | 60.7% | 53.5% | +7.2 | -8.9 (vol+15) | attEW 33.2 ypa 7.48 g=9 |
| Jared Goff | pass TD | 1.5 | -195 / +145 | 52.2% | Under | 47.8% | 40.8% | +7.0 | -0.5 (lam+15) | lambda 1.75 (26.50 pts) |
| Drake Maye | pass TD | 1.5 | -175 / +135 | 47.0% | Under | 53.0% | 42.6% | +10.5 | +3.1 (lam+15) | lambda 1.58 (24.00 pts) |

**Gate result:** 
- Numeric gate passes: Gibbs U4.5 rec, A.J. Brown U4.5 rec, Kiner U31.5 rush, Maye U27.5 rush, Goff O0.5 rush, Chism O0.5 rec, Maye U1.5 pass TD.
- Of those, only Maye U27.5 rush clears the full gate (no role-shift flag, Data Quality Medium, stable under the scramble-tail check). Gibbs fails on trend-dependence (flag), A.J. Brown on Data Quality Low, Kiner and Chism on role-shift flags, Goff on the kneel omission, Maye pass TD on the unvalidated Poisson.
- **Known tail issue:** QB scrambles use a designed-run yardage distribution in the base run, which understates the tail. The Maye sensitivity above addresses it for the LEAN; the Goff 0.5 line is not sensitive to it.

## 7. Correlation and QB injury volatility
- Structural only, no numeric joint probability. Kiner Under rush and Stevenson props share the NE backfield (cannibalization: Kiner's carries rise if Stevenson is limited). Maye Under rush yards moves against a NE trailing script. No parlay.
- QB injury volatility: Maye or Goff leaving would change both teams' remaining props. Maye's backup QB is not verified (Morton is the emergency third). The Maye LEAN is injury-censored (VOID) only if Maye himself leaves early; a Goff injury does not void it.

## 8. Governance
- No weights, components or features changed. No gematria, numerology, jersey-number or birthday inputs used.
- Frozen pregame record. Postgame results are graded against it only, with no hindsight reconstruction. The pilot probabilities add no PLAY or LEAN of their own; official statuses above come from the V2.2 card and Level B review.
- Closing prices are not captured here; CLV unscored unless later screenshots are added.

## Sources
- [Patriots.com inactives](https://www.patriots.com/news/week-10-inactives-patriots-vs-lions)
- [Patriots.com inactives analysis](https://www.patriots.com/news/inactives-analysis-patriots-wr-a-j-brown-rb-rhamondre-stevenson-officially-active-for-sunday-s-game-vs-lions-in-munich)
- [Lions.com inactives](https://www.detroitlions.com/news/inactives-lions-vs-patriots-stbrown-vaki-cisco)
- [Yahoo/SB Nation inactives](https://sports.yahoo.com/articles/patriots-vs-lions-inactives-j-130730724.html)
- [AP via WPRI](https://www.wpri.com/sports/patriots-new-england-nation/brown-stevenson-active-for-patriots-against-lions-in-munich/)
- [Boston Globe live blog](https://www.bostonglobe.com/2026/11/15/sports/patriots-lions-live-updates-munich/)
- [Patriots.com Wed injury report](https://www.patriots.com/news/week-10-injury-report-patriots-at-lions)
- [Boston Globe, Stevenson](https://www.bostonglobe.com/2026/11/10/sports/rhamondre-stevenson-knee-injury/)
- [SI/BetMGM odds](https://www.si.com/betting/patriots-vs-lions-prediction-odds-spread-injuries-trends-for-nfl-week-10-2026)
- [Covers early odds](https://www.covers.com/nfl/patriots-vs-lions-prediction-picks-odds-early-leans-week-10-2026)
- nflverse releases: https://github.com/nflverse/nflverse-data (play_by_play_2026, snap_counts_2026, downloaded Nov 15 2026 about 9:22 AM ET)
