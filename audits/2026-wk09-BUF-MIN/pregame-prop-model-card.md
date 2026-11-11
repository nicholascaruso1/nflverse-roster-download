# NFL Player Prop Model v2.2 — BUF @ MIN (Week 9 MNF, Mon Nov 9 2026, 8:15 PM ET, dome)

Prepared pregame, Nov 9 2026, after a 7:38 PM ET clock check and before kickoff. Kept separate from the Bet Model report. No combined recommendation.
Architecture and weights unchanged. Official statuses: PLAY / LEAN / WATCH / PASS / VOID.

## 1. Result (read this first)

- **PLAY: none. LEAN: none.**
- Every line I found was published before the inactives, and none was verifiable at the book. The standard is not to recommend a prop without a verified current line and price, so nothing can be promoted.
- **WATCH (4):** Cook O18.5 carries, Wentz Under passing yards, Jefferson Under receiving yards, Kincaid Over receiving yards.
- **PASS:** everything else screened (list in section 5).
- **No Lock 1.** No timestamped pre-inactives snapshot of lines exists, so none is invented.
- **Lock 2 is partial.** Inactives are verified. Post-inactives prices are not.

## 2. Data-source and freshness audit

- Usage and game logs are computed by me from nflverse 2026 PBP (weeks 1-9, through Nov 8 2026; BUF and MIN 7 games each).
- GitHub Actions artifacts were inaccessible (API 403 for this session). I used the public nflverse equivalents.
- The scoring ledger was not retrievable. TDs came from PBP.
- **Participation does not exist for 2026.** Snap share, route participation, red-zone snap role and first-15-snap share are unavailable.
- Where "share" appears below it means share of targets or carries from PBP, not snaps.
- Rosters (weeks 1-9) were not needed beyond name and team validation.
- Scrambles: nflverse flags QB scrambles separately. Allen's rushing includes scramble rows. Other players use designed rushes (`rush == 1`).

## 3. Missing-data report

- Snap share, route participation, route-level and personnel-level data: unavailable.
- Pressure rate: unavailable. Sack and QB-hit rates are proxies.
- Opponent-adjusted usage: not run.
- Prop prices: no sportsbook accessed directly. All prices are third-party-published and stale relative to inactives.
- **Probabilities:** no per-prop model probability, no-vig price or fair odds was calculated (inputs incomplete), so no prop is Level A.
- Red-zone and goal-line inputs: partial (PBP red-zone and inside-5 counts only).

## 4. Verified availability (inactives)

- **BUF inactive:** WR Skyler Bell, S Jalon Kilgore, OLB Mike Danna, **LG Alec Anderson, LT Dion Dawkins**, DL Greg Gaines.
- **MIN inactive:** **QB Kyler Murray, WR Jauan Jennings, RB Demond Claiborne**, S Jakobe Thomas, CB Chuck Demmings, DL Caleb Banks.
- **Out, per the Nov 7 team report:** BUF WR Joshua Palmer.
- **Conflict, unresolved:** Buffalo Down says Palmer is headed to IR and Shavers and Hancock were not activated from IR. The Nov 7 report lists the latter two as questionable.
- **Implications:**
  - Wentz starts, with Max Brosmer as backup.
  - Jennings had 10 tracked targets (5.5% share, about 1.4 per game).
  - Palmer had 13 tracked targets (6.6% share, about 1.9 per game).
  - BUF's two inactive OL starters face MIN's 10.6% sack rate and 24.3% QB-hit rate (proxies).

## 5. Props, by status

Lines are as published, with source and time. All times ET, Nov 9. **None are verified live or post-inactives.**

### WATCH

| Prop | Line / price (source, time) | Evidence (nflverse PBP, 2026) | Data Quality | Level | Opp. / Scenario Confidence |
|---|---|---|---|---|---|
| **James Cook Over 18.5 rush attempts** | O18.5 -112 (ESPN/DK, 6:46 AM) | Carries by game: 13, 21, 24, 12, 25, 22, 21 (avg 19.7); 5 of 7 at 19 or more. About 73% of BUF's tracked designed rushes. 28 red-zone carries, 10 inside the 5. **Threshold: 19 carries.** | Medium | B | Opp. **High-ish**; Scenario **Medium** |
| **Carson Wentz Under passing yards** | 209.5 (-113/-111, ESPN/DK 6:46 AM); 214.5 O at -115 (Hard Rock article, 5:00 PM); 210.5 Under cited without price | Wentz: 2 games, 23 attempts each, 133 and 143 yards (PBP), under 150 both times. Murray averaged 170.3 yards per game. Neither MIN QB averaged near 210. Counter: MIN is a home underdog, BUF's defense allows +0.140 EPA/pass, and the 2-game sample is thin. | Low-Medium | B | Opp. **Medium**; Scenario **Medium** |
| **Justin Jefferson Under receiving yards** | 79.5 (-111/-113, ESPN/DK 6:46 AM); 78.5 O at -112 (DK Network, 2:54 PM); 69.5 (Kalshi, 3:20 PM) | Yards by game (6 games): 92, 55, 32, 79, 44, 33. **Over 79.5: 1 of 6.** 5.9 targets per game, 22% share. Jennings out redistributes about 1.4 targets per game. Counter: Wentz uncertainty is two-sided, and Jefferson is the top target by share. | Medium | B | Opp. **Medium**; Scenario **Low-Medium** |
| **Dalton Kincaid Over receiving yards** | 36.5 (-111/-113, ESPN/DK 6:46 AM); 39.5 (Kalshi, 3:20 PM) | Yards by game: 130, 95, 38, 7, 7, 38, 86. **Over 36.5: 5 of 7.** 5.1 targets per game, 18% share. Palmer out frees about 1.9 targets per game. Counter: BUF's OL is down two starters, which hurts Allen and the passing game. | Medium | B | Opp. **Medium**; Scenario **Medium** |

Why WATCH and not LEAN:
- No verified price.
- No calculated probability or fair price.
- No score-state or opponent adjustment.

**Kill conditions** (a verified price is required for any promotion):
- **Cook carries:** BUF falls behind early (script branch A).
- **Wentz Under:** a verified line moves to 200 or lower, or he throws more than about 30 times.
- **Jefferson Under:** a verified line moves to 70 or lower.
- **Kincaid Over:** a verified line moves to 40 or higher.
These are my stated conditions, not calibrated thresholds.

### PASS (screened, no verified edge)

| Prop | Line (source) | Reason |
|---|---|---|
| Josh Allen pass yards | 238.5 (-112/-112, ESPN/DK); 224.5 Kalshi | 5 of 7 games over 238.5 (334, 248, 204, 253, 210, 255, 289), but MIN pass D is -0.207 EPA allowed and BUF's OL is down two starters. Signals conflict, no direction. |
| Josh Allen rush yards | 31.5 (-116/-109, ESPN/DK); 29.5 Kalshi | Weekly 23, 69, 22, 4, 121, 1, 30. Over 31.5 in 2 of 7 (mean 38.6, median 23). High variance, no edge shown. |
| Cook rush yards | 84.5 (-110/-114) | 57, 135, 154, 75, 111, 95, 80, so 4 of 7 over. No edge beyond the carries thesis, and efficiency is a separate question. |
| Aaron Jones rush yards | 32.5 (-111/-113) | 40, 105, 58, 94, 113, 26, 22, so 5 of 7 over. His role is shifting (Mason 38 carries in 3 games). Role uncertainty, Low Opportunity Confidence. |
| Jordan Mason rush yards | 47.5 (-113/-111) | 3 games of data, role unstable. |
| Hockenson receiving yards | 41.5 (-115/-109) | Over in 2 of 7 (119, 58). High variance, one outlier game. |
| Addison receiving yards | 40.5 (-115/-109) | Over in 3 of 6. No lean. |
| Shakir receiving yards | 40.5 (-109/-115) | Over in 3 of 7. No lean. |
| Moore receiving yards | 47.5 (-113/-111) | 4 games only (100, 67, 11, 82). Shoulder limited on the report, small sample. |
| Coleman receiving yards | 28.5 (-110/-114) | Over in 4 of 7, wildly variable. No lean. |
| Wentz interceptions | O0.5 -120 (DK Network) | 0 INT in 46 attempts. No lean. |
| Allen / Wentz passing TDs | 1.5 (+143/-183, +120/-153; ESPN/DK) | No per-prop probability. |
| Anytime TDs (Cook -110, Allen -120, Jefferson +150, Hockenson +210, Addison +260, Moore +275, Kincaid +275, Shakir +300, Coleman +425, Mason +210, Jones +270; ESPN/DK 6:46 AM) | | **No legitimate recorded pregame probability, so no quantified TD edge, per Addendum B.** TD props stay Level B at best, so there is no official TD PLAY. |

### Not screened

- Backup RBs and TEs beyond Knox, plus defense and kicker props. Coverage sweep (top-2 targets, primary rusher, secondary RB, relevant TE, QB) is complete for both teams except Mason, Johnson and Davis beyond the lines above.

## 6. Matchup and game environment

- **Dome.** Spread BUF -3 to -3.5, total 43.5 to 46.5 (unverified, see the Bet Model report for the snapshot table).
- **Scenario branches (qualitative, not probabilities):**
  - (A) BUF trails but controls: low
  - (B) competitive and balanced: most likely
  - (C) BUF dominates: moderate
  - (D) low-scoring and suppressed: moderate
- **Per-team volume direction:** BUF run volume is supported when ahead. MIN pass volume rises if trailing.
- **How the lead is expected to be created (research tag):** BUF clock-control rushing and defensive turnovers if C. A balanced pass-driven game if B.
- **OL / front:** BUF is down LT Dawkins and LG Anderson against MIN's sack rate of 10.6% and QB-hit rate of 24.3% (proxies). BUF's rush D is -0.077 EPA allowed and MIN's rush offense is -0.206.
- **RB efficiency and opportunity (v2.2):** BUF's run game can gain carries if the offense sustains drives, while receiving work for Cook (17 targets in 7 games) can fall. Modeled as separate markets.

## 7. QB Injury Volatility

The pregame QB change (Murray to Wentz) is realized. In-game injury to either QB changes both teams' remaining props. MIN's backup is Max Brosmer. BUF's backup was not pulled.

## 8. Conditional parlay candidates

None. No leg has a recorded pregame probability or a verified price, and no correlation assumption was established. Structural note only: Wentz Under yards and Jefferson Under yards share the same pass-volume mechanism and are positively correlated. Cook carries and Allen props share the BUF game script. Kincaid Over and Allen pass props share Allen's performance. No numeric joint probability was calculated.

## 9. Governance notes

- No weights, components or features changed. No gematria, numerology, jersey-number or birthday inputs were used.
- This is a frozen pregame record. Postgame results will be graded against it only. VOID rules apply to injury-censored props.

## Sources

- [ESPN preview (DK lines, props)](https://www.espn.com/espn/betting/story/_/id/50413261/nfl-week-9-odds-betting-preview-bills-vikings-prop-tips)
- [DK Network props](https://dknetwork.draftkings.com/2026/11/09/bills-at-vikings-nfl-player-prop-bets-for-monday-night-football/)
- [Hard Rock props article](https://www.hardrock.bet/news/bills-vs-vikings-best-player-props-and-prop-bets-for-mnf-at-u-s-bank-stadium/)
- [Covers prop projections (Kalshi)](https://www.covers.com/nfl/bills-vs-vikings-player-props-computer-projections-week-9-2026)
- [Vikings.com injury report](https://www.vikings.com/news/bills-injury-report-week-9-2026-nfl-season)
- [Vikings.com inactives](https://www.vikings.com/news/inactives-buffalo-bills-week-9-2026)
- [Buffalo Down inactives](https://buffalowdown.com/buffalo-bills-vs-minnesota-vikings-inactives-bills-missing-multiple-ol-starters-01m5mmq6cjs9)
- [NFL.com, Wentz start](https://www.nfl.com/news/vikings-to-start-carson-wentz-vs-bills-kyler-murray-hamstring)
- nflverse releases: https://github.com/nflverse/nflverse-data
