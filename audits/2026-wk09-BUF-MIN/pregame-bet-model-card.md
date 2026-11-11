# NFL Bet Model v2.2 — BUF @ MIN (Week 9 MNF, Mon Nov 9 2026, 8:15 PM ET, U.S. Bank Stadium, dome)

Prepared pregame, Nov 9 2026, after a 7:38 PM ET clock check and before kickoff. Frozen pregame record: later line moves and results never rewrite it.
Architecture and weights unchanged: opp-adjusted efficiency 25 / matchup 25 / power rating 15 / market value 20 / turnover-ST regression 10 / injuries-weather-news 5.
Component outputs are qualitative with provenance. No 0-100 scores, per the standing no-false-precision rule.

## 1. Final classification (read this first)

| Market | Status | Why |
|---|---|---|
| Spread BUF -3 to -3.5 | **WATCH** | Direction BUF is supported by raw efficiency, TO regression and the FPI reference. It is fully priced. No edge shown, and no live price could be verified. |
| Moneyline | **INCOMPLETE** | Power rating and opponent adjustment were not completed, so no model win probability and no EV. |
| Total (43.5 to 46.5 across snapshots) | **INCOMPLETE** | No independent total projection built, and snapshots conflict by 3 points. No direction annotated, per the INCOMPLETE rule. |
| BET / LEAN | **None** | The standard needs a verified price, a model edge and confidence. Only the confidence side is partly met. |

The result is zero actionable bets. That is a valid output and not a target miss.

**Kill conditions for the spread WATCH.**
(a) A verified post-inactives price at BUF -4.5 or longer (the FPI reference) leaves no market value.
(b) A verified price moved toward MIN (about -2.5) means the OL downgrade was already priced, so the injury component gets a double-counting check before any promotion.
(c) A verified price is still required for any promotion.
These are my stated conditions, not calibrated thresholds.

## 2. Data-source and freshness audit

| Item | Result |
|---|---|
| GitHub repo `nicholascaruso1/nflverse-roster-download` | Public, cloned OK (HEAD 302b926, Nov 8 21:52 ET). It contains workflows and `scripts/build_scoring_event_ledger.py` only, with no data files. |
| Actions artifacts (13711131074, 13710095041, 13711444803, 13643886148, 13643140837) | **DATA-ACCESS GAP.** The GitHub API returned 403 for this session. None were downloaded. Run IDs and artifact IDs from the handoff are unverified. |
| Substitute | The public nflverse release files your workflows pull from: `pbp/play_by_play_2026.parquet`, `weekly_rosters/roster_weekly_2026.csv`, and nflverse `games.csv` for the schedule. These are the same upstream source but not the same snapshot as your artifacts. |
| 2026 PBP | 23,647 plays, 372 columns, weeks 1-9, 135 games, latest game date Nov 8 2026. Pregame-suitable. The BUF-MIN game is not in it. |
| BUF / MIN games in PBP | 7 each (BUF bye wk 7, MIN bye wk 6). |
| Weekly rosters 2026 | 22,285 rows, weeks 1-9. This is a status roster, not an active list. |
| Scoring/TD ledger | Not retrievable. TD attribution came from PBP fields. |
| Participation | **No 2026 file.** PBP lacks `offense_players`, `defense_players`, `n_offense`, `was_pressure` and `pass_rusher`. |

## 3. Missing-data report

- **Opponent-adjusted efficiency:** only raw EPA and success rate were computed. No schedule adjustment was run.
- **Power rating:** no independent rating was pulled. ESPN FPI is cited as a reference only.
- **Pressure rate:** unavailable (no pressure flag). Sack rate and QB-hit rate are used as labeled proxies, not pressure rate.
- **Special teams:** not computed.
- **Route and snap metrics:** unavailable (no 2026 participation).
- **Backup QB for BUF:** not pulled.
- **Market:** no sportsbook was accessible directly. Every number below is third-party-published and not verified live.
- **Lock 1:** no real pre-inactives snapshot with a timestamp exists. None is invented.

## 4. Market snapshot (all ET, Nov 9 unless noted; none verified at the book)

| Snapshot | Spread | Total | Moneyline |
|---|---|---|---|
| ESPN preview (DK odds), 6:46 AM | BUF -3 (-120); open -3 (-105) | 43.5; open 48.5 | BUF -175 / MIN +145 |
| DK Network article, 2:54 PM | BUF -3.5 (price not listed) | 45.5 | BUF -192 / MIN +160 |
| Covers (book unnamed), 3:04 PM | BUF -3.5 | 44.5 | implied 61% / 39% |
| SportsLine (book unnamed), 6:39 PM | BUF -3.5 | 45.5 | not listed |
| nflverse schedule row | BUF -3.5 | 45.5 | BUF -192 / MIN +160 (source and time unstated) |
| FanDuel Research, Nov 5 | BUF -3 (-120) | 45.5 (O -105 / U -115) | BUF -188 / MIN +158 |
| DraftKings via NBC, Nov 3 | BUF -3.5 (-102) | 46.5; open 48.5 | BUF -185 / MIN +154 |

**Observations**
- Direction of movement: the total fell from 48.5 to roughly 44-46 and the spread rose from -3 to -3.5. Murray's hamstring news (Nov 5) fits that.
- The newest numbers (3:04 and 6:39 PM) cluster at BUF -3.5 and 44.5-45.5.
- The 6:46 AM total of 43.5 conflicts with the later numbers. I can't tell which is stale.
- No post-inactives line was found.
- FPI reference (ESPN, 6:46 AM page): BUF by 4.5, 67.6%.
- RLM and ticket/money splits: not obtained, so RLM is unverified/unavailable. Line movement alone is not called sharp money.

## 5. Component outputs

All stats are computed from nflverse 2026 PBP, regular season, pass and run plays, 7 games per team.

| Raw efficiency | BUF | MIN | League |
|---|---|---|---|
| Off EPA/play | +0.173 | -0.096 | -0.001 |
| Off success rate | 49.0% | 37.3% | 43.4% |
| Off pass EPA / rush EPA | +0.291 / +0.022 | -0.016 / -0.206 | |
| Def EPA/play allowed | +0.063 | -0.169 | |
| Def pass EPA / rush EPA allowed | +0.140 / -0.077 | -0.207 / -0.116 | |
| 20+ yd pass rate | 13.3% | 8.6% | |
| Plays per game | 61.3 | 57.4 | |
| Sack rate taken / def sack rate | 5.4% / 5.1% | 9.0% / 10.6% | |
| Def QB-hit rate | 18.3% | 24.3% | |
| Turnovers (give / take / margin) | 11 / 9 / -2 | 5 / 12 / +7 | |

1. **Opponent-adjusted efficiency (25%): INCOMPLETE.** The raw read is BUF offense far ahead and MIN defense clearly better than BUF defense. That is not schedule-adjusted.
   - MIN QB sample: Murray 169 attempts at -0.121 EPA per attempt; Wentz 46 attempts at +0.120 with -7.8 CPOE, over 2 games. The Wentz sample is too small to treat as signal.
2. **Matchup-specific (25%): provisional MIN pass-rush vs BUF OL is the central tension.**
   - BUF pass offense (+0.291) meets MIN's best unit, a pass D at -0.207 EPA with a 10.6% sack rate.
   - Verified inactives remove LT Dawkins and LG Anderson. Replacements named by Buffalo Down are T Tylan Grable and G Austin Corbett (position mapping inferred by the article).
   - On the other side, MIN's rush offense (-0.206) meets BUF's rush D (-0.077).
   - MIN's offense is weak on every raw measure. BUF's defense is below average against the pass (+0.140).
3. **Power rating (15%): INCOMPLETE.** Not sourced.
4. **Market value (20%):** the market (-3 to -3.5) vs the FPI reference (-4.5) is about 1 to 1.5 points. That is small and inside any plausible noise band. The numeric noise band is uncalibrated, so no value signal is claimed.
5. **Turnover/ST regression (10%):** MIN's +7 margin is expected to regress against MIN. BUF's -2 is a mild regression toward positive. Direction: BUF, small samples. ST not computed.
6. **Injuries/weather/news (5%):** dome, so weather is neutral.
   - **MIN:** QB Murray out, and the Wentz start was announced Nov 5. That is already in the market, so no incremental adjustment (double-counting rule). Verified inactives: Murray, Jennings, Claiborne, S Jakobe Thomas, CB Chuck Demmings, DL Caleb Banks.
   - **BUF:** verified inactives are LT Dawkins, LG Anderson, DL Gaines, WR Skyler Bell, S Kilgore, OLB Danna.
   - The Dawkins/Anderson absence is incremental versus their "questionable" tags, so it is applied. I can't see whether the post-inactives market absorbed it.
   - Source conflict, not resolved: Buffalo Down says Shavers and Hancock are not activated from IR and Palmer is headed to IR. The Nov 7 team report lists Shavers and Hancock as questionable.

**v2.2 layers**
- **Offensive Ceiling Index:** BUF high (pass EPA, 20+ yd rate, plays per game). MIN low. It is used for totals, team totals and props, not as a standalone signal.
- **Total-specific divergence:** not built. Recorded game totals so far: BUF games 67 / 72 / 40 / 55 / 71 / 63 / 46 (avg 59.1) and MIN games 61 / 12 / 39 / 25 / 36 / 26 / 34 (avg 33.3). Pace and finishing drives were not modeled.
- **Opportunity Confidence and Scenario Confidence (game-level):** Medium for BUF's offense carrying the game, Low for the total, per the missing inputs.
- **Scenario branches, rough relative likelihood (qualitative, not a probability):**
  - (A) favorite trails but controls: low
  - (B) competitive and balanced: most likely
  - (C) BUF dominates: moderate, helped by the Wentz uncertainty but dented by the OL absences
  - (D) low-scoring and suppressed: moderate, supported by MIN's 33.3 avg game total
- **QB Injury Volatility:** the pregame QB change is already realized. An in-game injury to either QB would move both teams' remaining props. MIN's backup is Max Brosmer (NFL.com). BUF's backup was not pulled.

## 6. Matchup summary and market conclusions

- The raw data supports Buffalo as the better team. The price already says so.
- The one new fact since the line posted is two BUF OL starters inactive against the NFL's most pressure-prone unit in this sample (10.6% sack rate, 24.3% QB-hit rate). It cuts against laying the points and is not yet confirmed in the price.
- No verified price means no BET or LEAN.

## 7. Conditional parlay candidates

None built. Parlay construction needs recorded per-leg probabilities and a stated correlation assumption, and neither exists. Structural note only: BUF side plus BUF-offense props share one environment, so they are positively correlated. A MIN-side pass-volume prop and MIN-side rushing props are negatively correlated through run/pass share.

## 8. Confidence and data-quality ratings

- Spread: Data Quality **Medium** (efficiency from sourced PBP, power rating missing, price unverified). Scenario Confidence **Medium**.
- Moneyline: **Low**.
- Total: **Low**.

## 9. Governance notes

- No weights, components or features changed. No gematria, numerology, jersey-number or birthday inputs were used.
- Every efficiency figure was computed by me from nflverse 2026 PBP. Market figures are third-party-published and unverified. Inactives are verified from the Vikings' site (5:45 PM ET) and Buffalo Down (7:16 PM ET).

## Sources

- [Covers game page](https://www.covers.com/nfl/bills-vs-vikings-prediction-picks-nov-9-2026)
- [FanDuel Research](https://fanduel.com/research/bills-vs-vikings-predictions-odds-picks-best-bets-for-nfl-week-9-monday-night-football-2026)
- [NBC Sports](https://www.nbcsports.com/betting/nfl/news/bills-vs-vikings-odds-expert-picks-team-and-player-news-betting-trends-and-stats)
- [ESPN preview](https://www.espn.com/espn/betting/story/_/id/50413261/nfl-week-9-odds-betting-preview-bills-vikings-prop-tips)
- [DK Network props](https://dknetwork.draftkings.com/2026/11/09/bills-at-vikings-nfl-player-prop-bets-for-monday-night-football/)
- [SportsLine](https://www.sportsline.com/insiders/bills-vs-vikings-odds-line-time-proven-computer-model-reveals-picks-for-2026-nfl-week-9-monday-night-football-matchup/)
- [Vikings.com injury report](https://www.vikings.com/news/bills-injury-report-week-9-2026-nfl-season)
- [Vikings.com inactives](https://www.vikings.com/news/inactives-buffalo-bills-week-9-2026)
- [Buffalo Down inactives](https://buffalowdown.com/buffalo-bills-vs-minnesota-vikings-inactives-bills-missing-multiple-ol-starters-01m5mmq6cjs9)
- [NFL.com, Wentz start](https://www.nfl.com/news/vikings-to-start-carson-wentz-vs-bills-kyler-murray-hamstring)
- nflverse releases: https://github.com/nflverse/nflverse-data
