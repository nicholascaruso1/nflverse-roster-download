# Week 10 (Sun Nov 15 2026) NFL Player Prop: source artifacts index

These four files are the evidence behind the Nov 15 prop postmortem (`docs/nfl_player_props/week10/week10-nfl-sun-prop-postmortem.md`, PR #5). They are stored here **unmodified**, so the postmortem and its underlying evidence can be reviewed independently.

**Governance statement.** This export is documentation only. It does not change any model parameter, pilot v0.1 probability, historical grade, or governance status. NFL Player Prop Model v2.2 remains FROZEN; the three pregame cards remain FROZEN; model parameter changes remain NOT AUTHORIZED.

## Classification

| Class | Meaning | Files |
|---|---|---|
| **FROZEN pregame record** | Prepared before kickoff; graded against, never edited or reconstructed after the fact | the three Week 10 cards |
| **RESEARCH (retrospective)** | Run after the 1:00 PM kickoffs on Nov 15 using weeks 1-10 data; walk-forward test of weeks 3-9; promotes, demotes or re-grades nothing | the calibration audit |

## Files

| # | Filename (original, preserved) | Class | Bytes | SHA-256 |
|---|---|---|---|---|
| 1 | `week10-nfl-sun-ne-det-munich-prop-model-card.md` | FROZEN pregame (NE @ DET, Munich, 9:30 AM ET; Lock 2 state, prepared about 9:28 AM ET) | 18715 | `403590f97426c6f89e9ccbeb37ac5502e55ede53054610a29b07973dfe78392f` |
| 2 | `week10-nfl-sun-1pm-prop-model-card.md` | FROZEN pregame (1:00 PM ET slate; prepared about 12:55 PM ET; includes section 9 addendum for BUF@NYJ, HOU@CLE, MIA@IND) | 45017 | `b4636f2a68e6152ef5281fa69ed4a0c32c85f46c9a96519440c20ec7ea6924b3` |
| 3 | `week10-nfl-sun-4pm-prop-model-card.md` | FROZEN pregame (4:05/4:25 PM ET slate; screenshots 3:05-3:08 PM ET; includes section 9 errata added 3:30 PM ET, original probabilities and statuses unchanged) | 34494 | `f986d26bc16414859753b798ab83c7ef0133b2f1aa337423d94a42f3cc0958e1` |
| 4 | `prop-model-v0.1-calibration-audit.md` | RESEARCH, retrospective (weeks 3-9 walk-forward calibration audit, v0.1 of the audit) | 28305 | `9265681b00c3896969d1eaa6a9aafc7ae401fd1382ad28a93173942742140c77` |

Notes on the frozen cards: the Munich card states that no Lock 1 exists and that its pilot probabilities were computed after seeing the prices. The 1 PM card says the same, with Opportunity and Scenario Confidence capped at Medium. The 4 PM card's errata section is part of the file as saved and is not an edit made during this export.

## Provenance

- **Origin:** each file is a document in the "Bet Screener" Claude Project, under the project paths `claude/<filename>`.
- **Chain of custody:** the files were downloaded from the Project by Nick and attached to the Claude session that built this PR. They were copied from those attachments into this directory with `cp`. No editor, formatter, line-ending conversion or regeneration touched them.
- **Filename changes:** the attachments arrived with an upload prefix (and `__1_` on the 1 PM card). Those were stripped back to the original project filenames above. File contents are unchanged by this.
- **What the hashes establish:** the SHA-256 values above were computed on the attachments as received and re-computed on the copies in this directory; all four pairs are identical. That proves a byte-for-byte copy of the downloaded files. **The Project's storage does not expose a hash for its own copy, so the hashes cannot be compared against the Project's stored original, only against what Nick downloaded.** Anyone who wants to confirm can re-download the same four Project docs and run `sha256sum`.
- **Provenance class under the archive standard:** VERIFIED-ORIGINAL as to the downloaded file; not independently hash-verified against the Project's internal store (see above).

## Verify

From this directory:

```
sha256sum *.md
```

and compare to the table above (`INDEX.md` itself is excluded from the table).
