# Allowed values (Part 7 ledgers, v0.5)

All fields named `*_utc` must be ISO-8601 with an explicit `Z` or `+00:00` offset (e.g. 2026-11-21T18:00:00Z).

- record_state (capture_log): Observed | Known but inaccessible. Observed requires access_state Public-full | Public-partial | User-supplied. Known but inaccessible requires Locked | Inaccessible.
- publication_timestamp_source: Page metadata | User screenshot | None (None requires an empty publication timestamp; a timestamp requires a source other than None).
- coverage_state (source_coverage_log; never claim records): Not observed | Not supplied
- eligibility (selections_ledger): Eligible | Duplicate | Ineligible. Eligible needs player_or_team, game and market_stated and an Observed capture. Duplicate needs duplicate_of_selection_id naming an Eligible selection from an EARLIER capture, matching on player_or_team, game and market_stated (normalized text), and the duplicate's own capture must be Observed; claims may reference only Eligible selections; semantic-only identity is Ineligible with a manual-review note.
- decode_disclosed: Yes | Partial | No
- provenance_at_capture / new_provenance_status: Established | Not established | Not applicable
- Yes/No fields: convention_preselected_before_test, claim_visible_in_preserved_source, game_player_unambiguous, evidence_is_postgame_material, evidence_known_at_capture, nonselected_player_check_done, attempted
- claim_category (never merged): Statistical milestone | Calendar/elapsed interval | Birthday interval | Opponent-specific interval | Career/home game count | Gematria | Symbolic jersey/history | Football rationale | Missing decode | Selection only
- counting_scope: Regular | Postseason | Combined | Not stated
- arithmetic_status / source_status / arithmetic_reproduction_status: Reproduced | Reproduced with scope qualification | Partially reproduced | Contradicted | Unsupported | Symbolic association only | Missing/inaccessible | Not yet tested
- event_result: Occurred | Did not occur | Void/postponed | Unresolved
- event_accuracy_status: Event occurred | Event did not occur | Unresolved | Void/postponed. Must map one-to-one from event_result (Occurred / Did not occur / Unresolved / Void/postponed); a void or postponed game is never recorded as an occurrence or non-occurrence.
- operation_type (comparisons_ledger): Cipher | Date interval | Count | Other
- result_class (comparisons_ledger): Match | Nonmatch | Not computable (required when attempted = Yes; empty when attempted = No)

Established provenance (at capture or by amendment) requires ALL of: exact claim visible in the preserved pregame source; verifiable publication timestamp before kickoff; a recorded capture/retrieval timestamp AND a preserved evidence path (a URL alone is not enough); no material ambiguity about game or player. Postgame material can never establish it. An upgrade also needs evidence_known_at_capture = No and evidence_first_located_utc later than the claim's capture timestamp; Not applicable -> Established needs original_classification_error_explanation.
