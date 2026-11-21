# Allowed values (Part 7 ledgers, v0.2)

- record_state (capture_log; only these two create a specific post record): Observed | Known but inaccessible
- coverage_state (source_coverage_log; NOT claim records, never counted as nonmatches): Not observed | Not supplied
- access_state: Public-full | Public-partial | User-supplied | Locked | Inaccessible
- provenance_at_capture / new_provenance_status: Established | Not established | Not applicable
- claim_visible_in_preserved_source, game_player_unambiguous, evidence_is_postgame_material: Yes | No
- claim_category (never merged): Statistical milestone | Calendar/elapsed interval | Birthday interval | Opponent-specific interval | Career/home game count | Gematria | Symbolic jersey/history | Football rationale | Missing decode | Selection only
- counting_scope: Regular | Postseason | Combined | Not stated
- arithmetic_status / source_status: Reproduced | Reproduced with scope qualification | Partially reproduced | Contradicted | Unsupported | Symbolic association only | Missing/inaccessible | Not yet tested
- event_result: Occurred | Did not occur | Void/postponed | Unresolved
- event_accuracy_status: Event occurred | Event did not occur | Unresolved

Established provenance (at capture or by amendment) requires ALL of: exact claim visible in the preserved pregame source; verifiable publication timestamp before kickoff; source URL or original user capture; capture/retrieval timestamp and preserved evidence; no material ambiguity about game or player. Postgame material can never establish it.
