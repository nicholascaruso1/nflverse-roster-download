# audits/

Permanent record of each game the Bet Model and Player Prop Model were run on: the frozen pregame decisions, the audit that checks the numbers, and the postmortem that grades the result. These folders are records. Nothing in the data pipeline reads them, and the weekly workflows are not triggered by changes here.

## Folder layout

One folder per game: `audits/<season>-wk<NN>-<AWAY>-<HOME>/`, for example `2026-wk09-BUF-MIN/`.

| File | What it is |
|---|---|
| `pregame-bet-model-card.md` | Frozen Bet Model card. Never edited after the game starts. |
| `pregame-prop-model-card.md` | Frozen Player Prop Model card. Never edited after the game starts. |
| `lock2-addendum.md` | Frozen Lock 2 record (post-inactives prices and re-grades), if one exists. |
| `NFL_Audit_Supplement_...md`, `audit.py` | Reproducibility audit and the script that regenerates its numbers. |
| `week<NN>-postmortem.md`, `postmortem.py` | Result graded against the frozen records, and the script that regenerates it. |
| `checksums.txt` | SHA-256 of every input (with source URL and retrieval time), script, frozen record and output. |
| other scripts and outputs | Sensitivity checks, reviewer outputs, reference outputs. |

## Rules

1. **Frozen means frozen.** Pregame cards and Lock addenda are copied in unchanged. Corrections go in the audit or postmortem as findings, never as edits to the frozen file.
2. **Hashes, not data.** Record the SHA-256, source URL and retrieval time of every input in `checksums.txt`. Do not commit large raw data files to git. Git keeps every version forever, so weekly data copies would bloat the repo.
3. **Postgame data is separate.** Pregame inputs and postgame inputs get separate rows and hashes, so a pregame record is never rebuilt from postgame data.
4. **No model changes here.** Architecture and weights are not stored or changed in this folder. Proposed model changes are listed in a postmortem as research candidates only.

## Where raw inputs live

Hashes prove a file is the same file but cannot bring it back. nflverse release files are overwritten as a season goes on, and Actions artifacts expire. To keep an input retrievable, archive it as an asset on a GitHub Release (2 GB per file) at season end or when an audit needs it, and record the release link and hash in `checksums.txt`.

**Current status:** no Release archive has been created yet. For `2026-wk09-BUF-MIN`, the one exact pregame input needed to re-run `audit.py` without the parquet library is committed in that folder as `play_by_play_2026.csv.zip` (about 10 MB). Do not remove it from git until a durable copy exists elsewhere and its hash matches `checksums.txt`.

## Reproducing an audit

1. Put the inputs listed in `checksums.txt` in one folder (the script accepts `play_by_play_2026.parquet`, `pbp_2026.parquet` or `play_by_play_2026.csv`) and confirm the hashes match.
2. `python3 -I audit.py <folder> out.md` (needs pandas, tabulate; pyarrow only for parquet).
3. Diff `out.md` against the reference output in the folder.
