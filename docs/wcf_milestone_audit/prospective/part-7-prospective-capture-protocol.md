# WCF Audit — Part 7: Prospective Post Capture and Claim-Level Evidence Logging

Protocol version: **P7 v0.3 DRAFT** (2026-11-20). Status: for review; nothing has been captured under it yet.
Research artifact only. Separate from the NFL/CFB betting models, the Script & Narrative Engine and the registry. Nothing here recommends a bet, and no ledger row is an input to any model.
v4.2 (commit 0196732), v4.1 and Parts 1–6 are **not modified** by this part. New observations never edit historical findings; they live only in `prospective/`.

Version history:
- v0.1 DRAFT — initial protocol and empty ledger templates.
- v0.2 DRAFT — after ChatGPT review: (1) immutable capture-time provenance plus dated evidence-based amendments; (2) record-state taxonomy, so a post missing from the conversation is never a claim record; (3) exact Established-provenance requirements; (4) outcomes reference the immutable capture-time status. Part 5 stop/go table unchanged.
- v0.3 DRAFT — after ChatGPT review of commit 7e640ad (v0.2 stays available in git history): explicit pilot-count rule via a new selections ledger; comparison-level ledger; validator now covers all ledgers, requires UTC-with-offset timestamps, never crashes on bad input, enforces amendment ordering, newly-located-evidence fields and preserved-evidence paths; automated synthetic test suite.

## 1. Scope and hard limits

- Public WCF posts and user-supplied screenshots only. No subscription, no bypassing paid or locked content, no contact with WCF, no private material, no sending the work to another model or service, no inference of hidden slides or Instagram/premium content. Missing stays missing.
- Capture is event-driven: it happens when Nick supplies a post or screenshot, or asks for a public page to be fetched. This session does not monitor feeds on its own.
- **Record states.** Only two states create a specific post record (`capture_log.csv`): **Observed** (a specific post or selection was located) and **Known but inaccessible** (a specific post is known to exist but its content cannot be retrieved; the page error is logged, not worked around). The other two states — **Not observed** (no specific post located) and **Not supplied** (a known post has not been provided for audit) — go only in `source_coverage_log.csv` as source-coverage notes. They are never invented claim records, never nonmatches, and never part of a claim denominator. A post cannot become "Missing" merely because it was not supplied in a conversation.

## 2. Capture procedure (per post)

1. Record the post in `capture_log.csv`: URL, title, publication timestamp **and where it came from** (page metadata, user screenshot, none), capture timestamp (UTC, taken at the moment of capture), capture method, access state.
2. Preserve the post as supplied: screenshots/media files byte-for-byte under `prospective/media/<capture_id>/`, with a SHA-256 list. Dated text transcriptions are labeled as transcriptions, not raw HTML.
3. Record every slide or section expected but not seen under `missing_items` (e.g., "slide 4/4 not supplied").
4. Record the earliest relevant kickoff time. A capture made after kickoff or after the result establishes nothing about pregame provenance by itself.
5. Freeze the search space (`search_space_log.csv`) **before** any outcome is looked at.

## 3. Claim-level ledger

One row per distinct claim or selection in `claims_ledger.csv`. Categories are never merged (list in `ledgers/VALID_VALUES.md`): the stated selection, each numerical rationale, each cipher, each football rationale and each implied milestone are separate rows. A selection with no disclosed decode is still a row (category "Selection only" or "Missing decode").

Each row carries the Part 5 fields: exact wording; counting scope (Regular / Postseason / Combined / Not stated); cutoff date; cipher, interval (elapsed vs inclusive) and home-definition conventions; source URLs and retrieval dates; and the **three separate statuses** — arithmetic, source, pregame provenance. No single score per post or per case, and no pooling of exact, approximate, symbolic, missing and contradicted components.

**Convention pre-selection:** `convention_*` fields are filled from what the post states, before testing, and `convention_preselected_before_test` records that. A match found only after trying other scopes, intervals or ciphers is labeled exploratory and may not be marked Reproduced under the primary convention.

Arithmetic and source verification may use data dated before the claim cutoff only. Any unresolved game-count discrepancy blocks "Reproduced" for that claim (Part 5 STOP rule).

## 4. Pregame provenance: immutable at capture, amendable by evidence

- `provenance_at_capture` (claims ledger) is the immutable record of what was established when the claim was first logged. It is never edited.
- The **current provenance assessment** is the latest row for that claim in `provenance_amendments.csv` (append-only, dated). An amendment may downgrade or upgrade, and records the exact basis: evidence URL or capture, its publication timestamp, its retrieval timestamp, preserved evidence path, and the reason.
- **Established** (at capture or by amendment) requires all of: the exact claim or selection visible in the preserved pregame source; a verifiable publication timestamp before kickoff; a source URL or the original user-supplied capture; capture/retrieval timestamp with preserved evidence; and no material ambiguity about the game or player. A timestamped post that does not expose the claim cannot establish provenance for it.
- An upgrade requires **newly located** evidence that itself independently establishes the claim existed before kickoff. Postgame material can never establish pregame provenance, and the validator rejects an upgrade whose evidence is flagged as postgame.

## 5. Outcomes are separate records

After the event, add rows to `outcomes_ledger.csv`; never edit the claim row's wording, conventions or `provenance_at_capture`. Each outcome row records `provenance_at_capture_copied`, which must equal the claim's immutable capture-time value; later amendments live only in the amendments ledger and never rewrite an outcome record. Three questions stay separate: did the event occur (event accuracy), does the arithmetic reproduce (arithmetic reproduction), and was the claim observable before kickoff (provenance). Event occurrence never upgrades provenance or arithmetic status, and a failed event never removes a claim. Losses, nonmatches, voids, unresolved outcomes, locked/missing posts and no-decode selections all stay in the ledgers. A locked or inaccessible post is a Known-but-inaccessible record, not a nonmatch; an unsupplied or unobserved post is a coverage note only.

## 6. Denominator and search-space record

`search_space_log.csv` (per captured post, frozen **before** any outcome is recorded; the validator rejects an outcome with no earlier freeze): candidate universe description; scopes, intervals and ciphers available; aggregate comparisons attempted and matched; whether equivalent numbers were checked for non-selected players in the same games.

`comparisons_ledger.csv` lists each comparison operation: subject, statistic, numerical target, scope, cutoff, operation type and detail, whether it was attempted, and the result class (Match / Nonmatch / Not computable). Aggregate counts in the search-space log must equal the comparison rows, so a later auditor can reconstruct which comparisons were made. Counts are descriptive data-quality items.

## 7. Pilot checkpoint

**Counting rule.** The unit is the **unique eligible selection** (`selections_ledger.csv`), never a claim row. One selection with several rationales (several claim rows) counts once; a post with several selections adds one row per selection; a selection with no disclosed decode counts (`decode_disclosed` = No); a selection repeated in a later post is marked Duplicate pointing to the first Eligible one and is not counted again; a post with no identifiable selection has no selection row and is not counted. A selection is Eligible only if it comes from an Observed capture and names the player/team, game and market. The validator prints the pilot count from this rule.

Uses the Part 5 rev. 2 stop/go table unchanged. The first **100 prospectively logged selections** (including no-decode selections) are a completeness and process checkpoint — not validation, not a significance test, and no hit rate is computed from them. Prevalence analysis requires its own prespecified design and multiple-comparison handling. Unresolved proportion is reported only as a descriptive statistic. NEVER GO: no transfer into betting models, the registry, the Narrative Engine or staking decisions.

At 100 selections, report only: counts by access state, provenance status, claim category and status; number of attempted comparisons; missingness. Nothing else.

## 8. Files

- `ledgers/capture_log.csv`, `selections_ledger.csv`, `claims_ledger.csv`, `comparisons_ledger.csv`, `provenance_amendments.csv`, `outcomes_ledger.csv`, `source_coverage_log.csv`, `search_space_log.csv` — empty templates (headers only).
- `ledgers/VALID_VALUES.md` — allowed values.
- `validate_ledgers.py` — structural checks only (required fields, allowed values, links, Established-provenance requirements, amendment rules, outcome/capture-time-provenance consistency). It evaluates no claim.

## 9. Known limitations

**Amendment rules.** The current assessment is the latest amendment by `amended_utc`; ties and out-of-order entries are rejected. Every amendment, including a downgrade, needs a basis and reason. An upgrade to Established needs evidence flagged not known at capture and first located after the capture timestamp, a retrieval timestamp and a preserved evidence path (a URL alone is not enough); Not applicable → Established also needs a written explanation of why the original classification was wrong. All `*_utc` fields must be ISO UTC with Z or +00:00.

Provenance can only be Established when the preserved source shows the claim and a pre-kickoff timestamp; Patreon page fetches failed earlier in this audit, so many posts may be Not established. Capture depends on Nick supplying material, and the source-coverage log is how that dependence stays visible. No sample from this protocol can be treated as complete unless the capture frame is itself documented. The validator checks structure only: a clean run means the records are internally consistent, not that the evidence is authentic, complete, newly discovered or predictive. `test_validator.py` runs synthetic tests (fictional rows only).
