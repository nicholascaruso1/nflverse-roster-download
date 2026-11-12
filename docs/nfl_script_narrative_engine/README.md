# NFL Script & Narrative Engine v1.0

A reproducible, pregame-only research module for NFL gematria, numerology, calendar relationships, franchise records, head-to-head history, scoreline frequencies, and optional active-roster name matches. It is a research tool, **not a betting model**.

## Scope

- A1Z26 ordinal and digital root.
- Reverse ordinal and digital root.
- Pythagorean sum and digital root (A=1 through I=9 repeating).
- Separate city, nickname, and full-team identity values.
- Current-season records, mirrored records, Thursday records, and Thursday-night kickoff-time proxies.
- Head-to-head history and previous-meeting ties.
- Calendar-day calculations and elapsed time since the last win/loss.
- Historical exact-score and total-score frequencies.
- Optional player-name screening using the latest available weekly roster at or before the target week.
- Frozen JSON context, CSV findings ledger, and Markdown report.

## Run

Install dependency: pandas.

Example:

    python -m pip install pandas
    python scripts/nfl_script_narrative_engine.py --games data/games.csv --date 2026-11-12 --away WAS --home NYG --week 10 --rosters data/rosters --claimed-away-tnf-record 3-9 --claimed-home-tnf-record 4-8 --output output/WAS_NYG_2026-11-12

The schedule CSV must contain game_id, season, game_type, week, gameday, gametime, away_team, away_score, home_team, and home_score. Weekly roster files should be named roster_weekly_YYYY.csv.

## Outputs

- frozen_context.json: inputs, cutoff, data scope, records, cipher values, base rates, roster snapshot and governance.
- findings.csv: normalized findings ledger.
- report.md: readable audit.

## Governance

1. The historical cutoff is exclusive of the target game date.
2. No odds, market prices, splits, or market-implied probabilities are used.
3. City, nickname, and full-team identity are separate strings and must not be substituted.
4. Digital roots are secondary matches, not full-value matches.
5. Cipher transformations are mathematically dependent; multiple hits are not independent confirmations.
6. Both teams receive competing narrative treatment. The engine does not choose a winner based on match count.
7. Days remaining is December 31 minus the target date, excluding the target date.
8. Thursday kickoff-time proxies are not official branded Thursday Night Football records.
9. Weekly roster snapshots are not official game-day inactive lists.
10. Historical rates are descriptive and in-sample, not validated predictive probabilities. Predictive claims require preregistered features and chronological holdout testing.

## Tests

    python -m unittest discover -s tests -v

No finding should be added to the NFL Bet Model or treated as a betting edge without independent prospective validation.
