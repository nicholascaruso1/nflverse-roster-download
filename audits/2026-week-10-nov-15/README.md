# Week 10 NFL, Sun Nov 15 2026: player-prop archive (4:05/4:25 PM slate)

Status: **archive of frozen pregame records. Do not edit files in `pregame/`; add corrections as new files.**
Model: NFL Player Prop Model v2.2 (frozen); pilot v0.1 probabilities (unvalidated, computed after seeing prices).

## Contents
| Path | What it is | Integrity |
|---|---|---|
| `pregame/4pm-prop-model-card_original-as-first-saved.md` | The 4 PM card (SEA@LV, LAR@ARI, SF@DAL) as first saved to the Bet Screener Project at about 3:25 PM ET | **Regenerated** from the committed generator, not copied from the stored file. Verified two ways: its SHA-256 (`023a997b...`) equals the version id the Project returned when this card was first saved, and re-applying the three later in-line edits to it reproduces the pre-errata text of the final file |
| `pregame/4pm-prop-model-card_with-errata-1.md` | Same card after the 3:30-3:40 PM ET corrections: WATCH count 14 to 17, QB-sample wording, calibration source label, new section 9 Errata (both game-line sources preserved) | Exact copy of the Project doc `claude/week10-nfl-sun-4pm-prop-model-card.md` as of the last save; its SHA-256 (`f986d26b...`) equals the Project's version id for that save |
| `calibration/prop-model-v0.1-calibration-audit_resaved-copy.md` | Walk-forward calibration audit reviewed by ChatGPT | **Re-saved copy** of the Project doc (text transferred by me, 28,305 bytes); the Project original `claude/prop-model-v0.1-calibration-audit.md` governs on any difference |
| `provenance/code/` | Scripts that produced the pilot probabilities and the card | Exact copies |
| `provenance/pilot_v0.1_board_output_4pm.csv` | Per-prop pilot output (all perturbation-derived fields except per-game histories) | Generated from the run that produced the card |
| `SHA256SUMS` | Checksums of every file here | |

## Classification (archive standard: FROZEN / FINAL / RESEARCH / SUPERSEDED / RECONSTRUCTED)
| File | Classification | Provenance |
|---|---|---|
| `pregame/4pm-prop-model-card_original-as-first-saved.md` | **RECONSTRUCTED** (hash-verified) | **Regenerated from the committed generator, not copied from a stored original.** Its SHA-256 equals the version id the Project returned when the original was saved, so the text is believed identical, but the stored original itself was not available to copy. |
| `pregame/4pm-prop-model-card_with-errata-1.md` | FINAL (exact copy of the Project doc at last save) | Contains the original card plus three in-line corrections and an Errata section; not the pre-errata original |
| `calibration/prop-model-v0.1-calibration-audit_resaved-copy.md` | RESEARCH, **re-saved copy** | Text transferred by me; the Project original governs |
| `provenance/code/*`, `provenance/pilot_v0.1_board_output_4pm.csv` | RESEARCH, exact copies of workspace files | |

No file in this directory is a verified byte-exact copy of an originally stored FROZEN file. That status requires the original Project documents (pending ZIP).

## Not included yet (needs exact bytes, not retyping)
The 1 PM prop card and the Lock 2 Bet Model card exist only in the Project. They will be added once an exact copy is available.

## Rules
Frozen files are immutable. Postgame grading goes in `postgame/` as separate files. Calibration research never changes v2.2. Corrections are new files with their own date. Lines used by the card: Hard Rock 11:40 AM ET (Lock 2 card); a later screenshot with different lines (LAR -10, SF total 55) is recorded in the card's Errata item 3 and was not seen by me directly.

## Data not committed
nflverse parquet inputs (play_by_play_2026, snap_counts_2026, roster_2026; downloaded Nov 15 2026 about 12:30 PM ET) are public releases and were not copied here.
