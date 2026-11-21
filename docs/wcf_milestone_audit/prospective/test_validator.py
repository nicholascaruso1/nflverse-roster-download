#!/usr/bin/env python3
"""Synthetic tests for validate_ledgers.py. Fictional rows only; no WCF data."""
import csv, subprocess, sys, tempfile, shutil, pathlib
here = pathlib.Path(__file__).parent
def base():
    return {
 "capture_log.csv": [dict(capture_id="C1", record_state="Observed", post_url="https://example.test/p", post_title="t", publication_timestamp_utc="2026-11-21T10:00:00Z", publication_timestamp_source="Page metadata", capture_timestamp_utc="2026-11-21T11:00:00Z", capture_method="manual", access_state="Public-full", media_preserved="Yes", media_paths="m/", kickoff_time_utc_of_earliest_game="2026-11-21T18:00:00Z", missing_items="", notes=""),
                     dict(capture_id="C2", record_state="Known but inaccessible", post_url="https://example.test/q", post_title="", publication_timestamp_utc="", publication_timestamp_source="None", capture_timestamp_utc="2026-11-21T11:05:00Z", capture_method="manual", access_state="Locked", media_preserved="No", media_paths="", kickoff_time_utc_of_earliest_game="", missing_items="all", notes="")],
 "selections_ledger.csv": [dict(selection_id="S1", capture_id="C1", player_or_team="P", game="G", market_stated="ATD", odds_stated="+100", eligibility="Eligible", duplicate_of_selection_id="", decode_disclosed="Yes", notes=""),
                           dict(selection_id="S2", capture_id="C1", player_or_team="Q", game="G", market_stated="ATD", odds_stated="", eligibility="Eligible", duplicate_of_selection_id="", decode_disclosed="No", notes="")],
 "claims_ledger.csv": [dict(claim_id="K1", capture_id="C1", selection_id="S1", claim_category="Gematria", exact_wording="w", slide_or_location="1", counting_scope="Regular", cutoff_date="", convention_cipher="Ordinal", convention_interval="", convention_home_definition="", convention_preselected_before_test="Yes", source_urls="", source_retrieval_date="", arithmetic_status="Reproduced", source_status="Reproduced", provenance_at_capture="Not established", claim_visible_in_preserved_source="Yes", game_player_unambiguous="Yes", preserved_evidence_path="", evidence_notes=""),
                       dict(claim_id="K2", capture_id="C1", selection_id="S1", claim_category="Statistical milestone", exact_wording="w2", slide_or_location="2", counting_scope="Regular", cutoff_date="", convention_cipher="", convention_interval="", convention_home_definition="", convention_preselected_before_test="Yes", source_urls="", source_retrieval_date="", arithmetic_status="Not yet tested", source_status="Not yet tested", provenance_at_capture="Established", claim_visible_in_preserved_source="Yes", game_player_unambiguous="Yes", preserved_evidence_path="evid/c1.png", evidence_notes="")],
 "provenance_amendments.csv": [dict(amendment_id="A1", claim_id="K1", amended_utc="2026-11-22T09:00:00Z", new_provenance_status="Established", basis_evidence_url_or_capture="https://example.test/e", evidence_publication_timestamp_utc="2026-11-21T12:00:00Z", evidence_retrieval_timestamp_utc="2026-11-22T08:00:00Z", evidence_first_located_utc="2026-11-22T07:00:00Z", evidence_known_at_capture="No", evidence_preserved_path="evid/a.png", evidence_is_postgame_material="No", claim_visible_in_evidence="Yes", game_player_unambiguous="Yes", original_classification_error_explanation="", reason="located")],
 "search_space_log.csv": [dict(frozen_id="F1", capture_id="C1", frozen_utc="2026-11-21T12:00:00Z", candidate_universe_description="u", conventions_available_scopes="3", conventions_available_intervals="2", conventions_available_ciphers="4", comparisons_attempted="2", comparisons_matched="1", nonselected_player_check_done="No", notes="")],
 "comparisons_ledger.csv": [dict(comparison_id="X1", frozen_id="F1", selection_id="S1", subject_player_or_team="P", statistic="TD", numerical_target="30", counting_scope="Regular", cutoff_date="", operation_type="Count", operation_detail="d", attempted="Yes", result_class="Match", notes=""),
                            dict(comparison_id="X2", frozen_id="F1", selection_id="S1", subject_player_or_team="P", statistic="TD", numerical_target="31", counting_scope="Combined", cutoff_date="", operation_type="Count", operation_detail="d", attempted="Yes", result_class="Nonmatch", notes="")],
 "outcomes_ledger.csv": [dict(outcome_id="O1", claim_id="K1", outcome_recorded_utc="2026-11-22T00:00:00Z", event_final="Yes", event_result="Occurred", event_accuracy_status="Event occurred", arithmetic_reproduction_status="Reproduced", provenance_at_capture_copied="Not established", outcome_source_urls="", outcome_source_retrieval_date="", notes="")],
 "source_coverage_log.csv": [dict(coverage_id="V1", noted_utc="2026-11-21T00:00:00Z", coverage_state="Not supplied", description="d", how_known="h", linked_capture_id="C1", notes="")]}
def run(data):
    t = pathlib.Path(tempfile.mkdtemp())
    hdr = (here / "ledgers")
    for n, rows in data.items():
        cols = next(csv.reader(open(hdr / n)))
        with open(t / n, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); [w.writerow(r) for r in rows]
    p = subprocess.run([sys.executable, "-I", str(here / "validate_ledgers.py"), str(t)], capture_output=True, text=True)
    shutil.rmtree(t); return p
def mut(fn):
    d = base(); fn(d); return d
CASES = [
 ("valid scenario passes, pilot count 2 (not 3 claim rows)", lambda d: None, None),
 ("naive timestamp", lambda d: d["capture_log.csv"][0].update(capture_timestamp_utc="2026-11-21T11:00:00"), "ISO UTC"),
 ("garbage timestamp", lambda d: d["search_space_log.csv"][0].update(frozen_utc="tomorrow"), "ISO UTC"),
 ("duplicate selection id", lambda d: d["selections_ledger.csv"][1].update(selection_id="S1"), "duplicate selection_id"),
 ("duplicate outcome id", lambda d: d["outcomes_ledger.csv"].append(dict(d["outcomes_ledger.csv"][0])), "duplicate outcome_id"),
 ("not supplied as capture record", lambda d: d["capture_log.csv"][1].update(record_state="Not supplied"), "not allowed"),
 ("inaccessible recorded Public-full", lambda d: d["capture_log.csv"][1].update(access_state="Public-full"), "access_state"),
 ("timestamp with source None", lambda d: d["capture_log.csv"][1].update(publication_timestamp_utc="2026-11-21T10:00:00Z"), "source is None"),
 ("claim/selection from different capture", lambda d: d["claims_ledger.csv"][0].update(capture_id="C2"), "different capture"),
 ("bad claim category", lambda d: d["claims_ledger.csv"][0].update(claim_category="Vibes"), "claim_category"),
 ("bad preselected flag", lambda d: d["claims_ledger.csv"][0].update(convention_preselected_before_test="Maybe"), "convention_preselected"),
 ("Established at capture with URL only", lambda d: d["claims_ledger.csv"][1].update(preserved_evidence_path="", source_urls="https://x"), "preserved evidence path"),
 ("Established at capture after kickoff", lambda d: d["capture_log.csv"][0].update(publication_timestamp_utc="2026-11-21T19:00:00Z"), "pre-kickoff"),
 ("upgrade on postgame evidence", lambda d: d["provenance_amendments.csv"][0].update(evidence_is_postgame_material="Yes"), "postgame"),
 ("upgrade on evidence known at capture", lambda d: d["provenance_amendments.csv"][0].update(evidence_known_at_capture="Yes"), "not known at capture"),
 ("upgrade evidence located before capture", lambda d: d["provenance_amendments.csv"][0].update(evidence_first_located_utc="2026-11-21T10:30:00Z"), "after the claim's capture"),
 ("upgrade without preserved path", lambda d: d["provenance_amendments.csv"][0].update(evidence_preserved_path=""), "preserved evidence path"),
 ("downgrade without basis", lambda d: d["provenance_amendments.csv"].append(dict(d["provenance_amendments.csv"][0], amendment_id="A2", claim_id="K2", new_provenance_status="Not established", basis_evidence_url_or_capture="", amended_utc="2026-11-23T00:00:00Z")), "needs basis"),
 ("amendment tie", lambda d: d["provenance_amendments.csv"].append(dict(d["provenance_amendments.csv"][0], amendment_id="A2")), "strictly later"),
 ("Not applicable upgrade without explanation", lambda d: (d["claims_ledger.csv"][0].update(provenance_at_capture="Not applicable"), d["outcomes_ledger.csv"][0].update(provenance_at_capture_copied="Not applicable")), "original_classification_error_explanation"),
 ("outcome rewrites capture-time provenance", lambda d: d["outcomes_ledger.csv"][0].update(provenance_at_capture_copied="Established"), "immutable"),
 ("bad outcome status values", lambda d: d["outcomes_ledger.csv"][0].update(event_accuracy_status="Hit", arithmetic_reproduction_status="Yes"), "event_accuracy_status"),
 ("outcome before freeze", lambda d: d["outcomes_ledger.csv"][0].update(outcome_recorded_utc="2026-11-21T11:30:00Z"), "before the search space was frozen"),
 ("matched > attempted", lambda d: d["search_space_log.csv"][0].update(comparisons_matched="3"), "matched exceeds attempted"),
 ("non-integer counts", lambda d: d["search_space_log.csv"][0].update(comparisons_attempted="-1"), "nonnegative integers"),
 ("aggregate != comparison rows", lambda d: d["search_space_log.csv"][0].update(comparisons_attempted="5"), "do not equal comparison rows"),
 ("result_class with attempted No", lambda d: d["comparisons_ledger.csv"][0].update(attempted="No"), "must be empty"),
 ("coverage links unknown capture", lambda d: d["source_coverage_log.csv"][0].update(linked_capture_id="C9"), "unknown linked_capture_id"),
 ("duplicate selection names non-eligible", lambda d: d["selections_ledger.csv"][1].update(eligibility="Duplicate", duplicate_of_selection_id="S1"), "different capture"),
 ("zero-row aggregate mismatch", lambda d: (d["comparisons_ledger.csv"].clear(), None), "do not equal comparison rows (0/0)"),
 ("comparison selection from other capture", lambda d: (d["capture_log.csv"].append(dict(d["capture_log.csv"][0], capture_id="C3", capture_timestamp_utc="2026-11-21T11:10:00Z")), d["selections_ledger.csv"].append(dict(d["selections_ledger.csv"][0], selection_id="S9", capture_id="C3")), d["comparisons_ledger.csv"][0].update(selection_id="S9")), "different capture than the frozen"),
 ("claim on inaccessible capture", lambda d: d["claims_ledger.csv"][0].update(capture_id="C2", selection_id=""), "require an Observed capture"),
 ("duplicate original not earlier", lambda d: (d["capture_log.csv"].append(dict(d["capture_log.csv"][0], capture_id="C3", capture_timestamp_utc="2026-11-21T10:30:00Z")), d["selections_ledger.csv"].append(dict(d["selections_ledger.csv"][0], selection_id="S9", capture_id="C3", eligibility="Duplicate", duplicate_of_selection_id="S1"))), "must precede"),
 ("duplicate identity mismatch", lambda d: (d["capture_log.csv"].append(dict(d["capture_log.csv"][0], capture_id="C3", capture_timestamp_utc="2026-11-21T12:10:00Z")), d["selections_ledger.csv"].append(dict(d["selections_ledger.csv"][0], selection_id="S9", capture_id="C3", eligibility="Duplicate", duplicate_of_selection_id="S1", player_or_team="Other"))), "must match the original"),
 ("valid duplicate passes and is not counted", lambda d: (d["capture_log.csv"].append(dict(d["capture_log.csv"][0], capture_id="C3", capture_timestamp_utc="2026-11-21T12:10:00Z")), d["selections_ledger.csv"].append(dict(d["selections_ledger.csv"][0], selection_id="S9", capture_id="C3", eligibility="Duplicate", duplicate_of_selection_id="S1", player_or_team=" p "))), "target 100): 2"),
 ("contradictory outcome fields", lambda d: d["outcomes_ledger.csv"][0].update(event_result="Did not occur"), "inconsistent"),
 ("void mapped to occurred", lambda d: d["outcomes_ledger.csv"][0].update(event_result="Void/postponed"), "inconsistent"),
 ("evidence located after retrieval", lambda d: d["provenance_amendments.csv"][0].update(evidence_first_located_utc="2026-11-22T08:30:00Z"), "after evidence_retrieval"),
 ("evidence retrieved after amendment", lambda d: d["provenance_amendments.csv"][0].update(evidence_retrieval_timestamp_utc="2026-11-22T10:00:00Z"), "retrieved after the amendment"),
]
bad = 0
for name, fn, expect in CASES:
    p = run(mut(fn))
    if expect is None:
        ok = p.returncode == 0 and "target 100): 2" in p.stdout
    elif expect.startswith("target"):
        ok = p.returncode == 0 and expect in p.stdout
    else:
        ok = p.returncode == 1 and expect in p.stdout
    print(("PASS " if ok else "FAIL ") + name)
    if not ok: bad += 1; print(p.stdout[-600:], p.stderr[-300:])
# malformed file must not crash
t = pathlib.Path(tempfile.mkdtemp()); shutil.copytree(here / "ledgers", t / "l"); (t / "l" / "claims_ledger.csv").write_text("not,a,valid,header\n1,2\n")
p = subprocess.run([sys.executable, "-I", str(here / "validate_ledgers.py"), str(t / "l")], capture_output=True, text=True)
ok = p.returncode == 1 and "Traceback" not in p.stderr; print(("PASS " if ok else "FAIL ") + "malformed file handled without crash"); bad += not ok
print(f"{len(CASES)+1} tests, {bad} failures"); sys.exit(1 if bad else 0)
