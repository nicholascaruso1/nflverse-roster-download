#!/usr/bin/env python3
"""Structural validator for Part 7 ledgers (v0.4). Checks records are internally consistent.
It CANNOT verify that evidence is authentic, complete, newly discovered or predictive.
Never crashes on malformed rows: problems are reported as errors. Research artifact only."""
import csv, sys, pathlib, re
from datetime import datetime
d = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "ledgers")
HDR = {
 "capture_log.csv": "capture_id,record_state,post_url,post_title,publication_timestamp_utc,publication_timestamp_source,capture_timestamp_utc,capture_method,access_state,media_preserved,media_paths,kickoff_time_utc_of_earliest_game,missing_items,notes",
 "selections_ledger.csv": "selection_id,capture_id,player_or_team,game,market_stated,odds_stated,eligibility,duplicate_of_selection_id,decode_disclosed,notes",
 "claims_ledger.csv": "claim_id,capture_id,selection_id,claim_category,exact_wording,slide_or_location,counting_scope,cutoff_date,convention_cipher,convention_interval,convention_home_definition,convention_preselected_before_test,source_urls,source_retrieval_date,arithmetic_status,source_status,provenance_at_capture,claim_visible_in_preserved_source,game_player_unambiguous,preserved_evidence_path,evidence_notes",
 "provenance_amendments.csv": "amendment_id,claim_id,amended_utc,new_provenance_status,basis_evidence_url_or_capture,evidence_publication_timestamp_utc,evidence_retrieval_timestamp_utc,evidence_first_located_utc,evidence_known_at_capture,evidence_preserved_path,evidence_is_postgame_material,claim_visible_in_evidence,game_player_unambiguous,original_classification_error_explanation,reason",
 "search_space_log.csv": "frozen_id,capture_id,frozen_utc,candidate_universe_description,conventions_available_scopes,conventions_available_intervals,conventions_available_ciphers,comparisons_attempted,comparisons_matched,nonselected_player_check_done,notes",
 "comparisons_ledger.csv": "comparison_id,frozen_id,selection_id,subject_player_or_team,statistic,numerical_target,counting_scope,cutoff_date,operation_type,operation_detail,attempted,result_class,notes",
 "outcomes_ledger.csv": "outcome_id,claim_id,outcome_recorded_utc,event_final,event_result,event_accuracy_status,arithmetic_reproduction_status,provenance_at_capture_copied,outcome_source_urls,outcome_source_retrieval_date,notes",
 "source_coverage_log.csv": "coverage_id,noted_utc,coverage_state,description,how_known,linked_capture_id,notes",
}
err = []
def E(m): err.append(m)
TS = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?(\.\d+)?(Z|\+00:00)$")
def ts(x):
    x = (x or "").strip()
    if not TS.match(x): return None
    try: return datetime.fromisoformat(x.replace("Z", "+00:00"))
    except Exception: return None
def load(n):
    p = d / n
    if not p.exists(): E(f"{n}: file missing"); return []
    try:
        with open(p, newline="", encoding="utf-8") as f:
            rd = csv.DictReader(f)
            if ",".join(rd.fieldnames or []) != HDR[n]: E(f"{n}: header does not match v0.4 template"); return []
            out = []
            for i, r in enumerate(rd, 2):
                if None in r or None in r.values(): E(f"{n} line {i}: wrong number of columns"); continue
                out.append({k: (v or "").strip() for k, v in r.items()})
            return out
    except Exception as ex: E(f"{n}: unreadable ({ex.__class__.__name__})"); return []
def idcheck(rows, n, key):
    seen = set()
    for r in rows:
        k = r[key]
        if not k: E(f"{n}: empty {key}")
        elif k in seen: E(f"{n}: duplicate {key} {k}")
        seen.add(k)
    return seen
def enum(r, f, allowed, tag, req=True):
    v = r[f]
    if v == "" and not req: return
    if v not in allowed: E(f"{tag}: {f} {v!r} not allowed")
def utc(r, f, tag, req=False):
    v = r[f]
    if v == "":
        if req: E(f"{tag}: {f} required")
    elif not ts(v): E(f"{tag}: {f} must be ISO UTC with Z or +00:00")
cap, sel, cl, am, ss, cmp_, out, cov = (load(n) for n in HDR)
YN = {"Yes","No"}; PROV = {"Established","Not established","Not applicable"}
STAT = {"Reproduced","Reproduced with scope qualification","Partially reproduced","Contradicted","Unsupported","Symbolic association only","Missing/inaccessible","Not yet tested"}
CATS = {"Statistical milestone","Calendar/elapsed interval","Birthday interval","Opponent-specific interval","Career/home game count","Gematria","Symbolic jersey/history","Football rationale","Missing decode","Selection only"}
SCOPE = {"Regular","Postseason","Combined","Not stated"}
OBS_ACC = {"Public-full","Public-partial","User-supplied"}; INACC = {"Locked","Inaccessible"}
# capture log
capids = idcheck(cap, "capture_log", "capture_id"); capd = {r["capture_id"]: r for r in cap}
for r in cap:
    t = f"capture {r['capture_id']}"
    enum(r, "record_state", {"Observed","Known but inaccessible"}, t)
    if r["record_state"] == "Observed": enum(r, "access_state", OBS_ACC, t)
    elif r["record_state"] == "Known but inaccessible": enum(r, "access_state", INACC, t)
    else: E(f"{t}: Not observed/Not supplied belong in source_coverage_log, not capture_log") if r["record_state"] in ("Not observed","Not supplied") else None
    if not r["post_url"]: E(f"{t}: post_url required")
    utc(r, "capture_timestamp_utc", t, True); utc(r, "publication_timestamp_utc", t); utc(r, "kickoff_time_utc_of_earliest_game", t)
    enum(r, "publication_timestamp_source", {"Page metadata","User screenshot","None"}, t)
    if r["publication_timestamp_source"] == "None" and r["publication_timestamp_utc"]: E(f"{t}: timestamp present but source is None")
    if r["publication_timestamp_source"] in ("Page metadata","User screenshot") and not r["publication_timestamp_utc"]: E(f"{t}: source named but timestamp empty")
# selections
selids = idcheck(sel, "selections_ledger", "selection_id"); seld = {r["selection_id"]: r for r in sel}
for r in sel:
    t = f"selection {r['selection_id']}"
    if r["capture_id"] not in capids: E(f"{t}: unknown capture_id")
    enum(r, "eligibility", {"Eligible","Duplicate","Ineligible"}, t); enum(r, "decode_disclosed", {"Yes","Partial","No"}, t)
    if r["eligibility"] == "Eligible":
        if not (r["player_or_team"] and r["game"] and r["market_stated"]): E(f"{t}: Eligible needs player_or_team, game and market_stated")
        if capd.get(r["capture_id"], {}).get("record_state") != "Observed": E(f"{t}: Eligible requires an Observed capture")
        if r["duplicate_of_selection_id"]: E(f"{t}: Eligible cannot name duplicate_of")
    if r["eligibility"] == "Duplicate":
        o = seld.get(r["duplicate_of_selection_id"])
        if not o or o["eligibility"] != "Eligible" or o["capture_id"] == r["capture_id"]: E(f"{t}: Duplicate must name an Eligible selection from a different capture")
        else:
            oc, dc = ts(capd.get(o["capture_id"], {}).get("capture_timestamp_utc")), ts(capd.get(r["capture_id"], {}).get("capture_timestamp_utc"))
            if not (oc and dc and oc < dc): E(f"{t}: the original selection's capture must precede the duplicate's capture")
            norm = lambda x: " ".join(x.lower().split())
            if any(norm(o[f]) != norm(r[f]) for f in ("player_or_team","game","market_stated")): E(f"{t}: Duplicate must match the original on player_or_team, game and market_stated (normalized text); if identity is only semantic, mark Ineligible and note it for manual review")
# claims
clids = idcheck(cl, "claims_ledger", "claim_id"); cld = {r["claim_id"]: r for r in cl}
def est_ok(pub, retr, kick, vis, unamb, path):
    return bool(ts(pub) and ts(kick) and ts(pub) < ts(kick) and ts(retr) and vis == "Yes" and unamb == "Yes" and path)
for r in cl:
    t = f"claim {r['claim_id']}"; c = capd.get(r["capture_id"])
    if not c: E(f"{t}: unknown capture_id"); continue
    if c["record_state"] != "Observed": E(f"{t}: claim rows require an Observed capture (inaccessible content stays Missing; no claim is inferred)")
    if r["selection_id"] and r["selection_id"] not in selids: E(f"{t}: unknown selection_id")
    if r["selection_id"] and seld[r["selection_id"]]["capture_id"] != r["capture_id"]: E(f"{t}: selection belongs to a different capture")
    if not r["exact_wording"]: E(f"{t}: exact_wording required")
    enum(r, "claim_category", CATS, t); enum(r, "counting_scope", SCOPE, t); enum(r, "provenance_at_capture", PROV, t)
    enum(r, "arithmetic_status", STAT, t); enum(r, "source_status", STAT, t); enum(r, "convention_preselected_before_test", YN, t)
    enum(r, "claim_visible_in_preserved_source", YN, t, False); enum(r, "game_player_unambiguous", YN, t, False)
    if r["provenance_at_capture"] == "Established" and not est_ok(c["publication_timestamp_utc"], c["capture_timestamp_utc"], c["kickoff_time_utc_of_earliest_game"], r["claim_visible_in_preserved_source"], r["game_player_unambiguous"], r["preserved_evidence_path"]):
        E(f"{t}: Established at capture needs pre-kickoff publication timestamp, capture timestamp, claim visible, unambiguous game/player, and a preserved evidence path (a URL alone is not enough)")
# amendments
amids = idcheck(am, "provenance_amendments", "amendment_id"); last = {}
for a in am:
    t = f"amendment {a['amendment_id']}"; c = cld.get(a["claim_id"])
    if not c: E(f"{t}: unknown claim_id"); continue
    enum(a, "new_provenance_status", PROV, t)
    for f in ("amended_utc","evidence_retrieval_timestamp_utc"): utc(a, f, t, True)
    for f in ("evidence_publication_timestamp_utc","evidence_first_located_utc"): utc(a, f, t)
    if not a["basis_evidence_url_or_capture"] or not a["reason"]: E(f"{t}: every amendment (including downgrades) needs basis_evidence_url_or_capture and reason")
    when, prev = ts(a["amended_utc"]), last.get(a["claim_id"])
    if when:
        if prev and when <= prev: E(f"{t}: amended_utc must be strictly later than the previous amendment for this claim (ties/out-of-order rejected)")
        last[a["claim_id"]] = max(when, prev) if prev else when
        cc = ts(capd[c["capture_id"]]["capture_timestamp_utc"])
        if cc and when < cc: E(f"{t}: amendment predates the claim's capture")
    fl_, rt_, am_ = ts(a["evidence_first_located_utc"]), ts(a["evidence_retrieval_timestamp_utc"]), ts(a["amended_utc"])
    if fl_ and rt_ and fl_ > rt_: E(f"{t}: evidence_first_located_utc is after evidence_retrieval_timestamp_utc")
    if rt_ and am_ and rt_ > am_: E(f"{t}: evidence retrieved after the amendment was recorded")
    if a["new_provenance_status"] == "Established":
        k = capd[c["capture_id"]]["kickoff_time_utc_of_earliest_game"]
        enum(a, "evidence_is_postgame_material", YN, t); enum(a, "evidence_known_at_capture", YN, t)
        if a["evidence_is_postgame_material"] == "Yes": E(f"{t}: postgame material can never establish provenance")
        if not est_ok(a["evidence_publication_timestamp_utc"], a["evidence_retrieval_timestamp_utc"], k, a["claim_visible_in_evidence"], a["game_player_unambiguous"], a["evidence_preserved_path"]):
            E(f"{t}: upgrade needs pre-kickoff evidence publication timestamp, retrieval timestamp, claim visible, unambiguous game/player and a preserved evidence path")
        if a["evidence_known_at_capture"] != "No": E(f"{t}: upgrade must rest on evidence not known at capture")
        fl, cc = ts(a["evidence_first_located_utc"]), ts(capd[c["capture_id"]]["capture_timestamp_utc"])
        if not fl or (cc and fl <= cc): E(f"{t}: evidence_first_located_utc must be after the claim's capture timestamp")
        if c["provenance_at_capture"] == "Not applicable" and not a["original_classification_error_explanation"]:
            E(f"{t}: Not applicable -> Established needs original_classification_error_explanation")
# search space and comparisons
ssids = idcheck(ss, "search_space_log", "frozen_id"); ssd = {r["frozen_id"]: r for r in ss}
for r in ss:
    t = f"search_space {r['frozen_id']}"
    if r["capture_id"] not in capids: E(f"{t}: unknown capture_id")
    utc(r, "frozen_utc", t, True); enum(r, "nonselected_player_check_done", YN, t)
    if not r["candidate_universe_description"]: E(f"{t}: candidate_universe_description required")
    a_, m_ = r["comparisons_attempted"], r["comparisons_matched"]
    if not (a_.isdigit() and m_.isdigit()): E(f"{t}: comparisons_attempted/matched must be nonnegative integers")
    elif int(m_) > int(a_): E(f"{t}: matched exceeds attempted")
cids = idcheck(cmp_, "comparisons_ledger", "comparison_id"); cnt = {}
for r in cmp_:
    t = f"comparison {r['comparison_id']}"
    if r["frozen_id"] not in ssids: E(f"{t}: unknown frozen_id")
    if r["selection_id"] and r["selection_id"] not in selids: E(f"{t}: unknown selection_id")
    elif r["selection_id"] and r["frozen_id"] in ssd and seld[r["selection_id"]]["capture_id"] != ssd[r["frozen_id"]]["capture_id"]:
        E(f"{t}: selection belongs to a different capture than the frozen search-space record")
    enum(r, "operation_type", {"Cipher","Date interval","Count","Other"}, t); enum(r, "attempted", YN, t); enum(r, "counting_scope", SCOPE, t)
    for f in ("subject_player_or_team","statistic","numerical_target","operation_detail"):
        if not r[f]: E(f"{t}: {f} required")
    if r["attempted"] == "Yes":
        enum(r, "result_class", {"Match","Nonmatch","Not computable"}, t)
        c_ = cnt.setdefault(r["frozen_id"], [0, 0]); c_[0] += 1; c_[1] += r["result_class"] == "Match"
    elif r["result_class"]: E(f"{t}: result_class must be empty when attempted = No")
for fid, s_ in ssd.items():
    a_, m_ = cnt.get(fid, (0, 0))
    if s_["comparisons_attempted"].isdigit() and s_["comparisons_matched"].isdigit() and (int(s_["comparisons_attempted"]), int(s_["comparisons_matched"])) != (a_, m_):
        E(f"search_space {fid}: aggregate counts ({s_['comparisons_attempted']}/{s_['comparisons_matched']}) do not equal comparison rows ({a_}/{m_})")
frozen_for = {}
for r in ss:
    if ts(r["frozen_utc"]): frozen_for.setdefault(r["capture_id"], []).append(ts(r["frozen_utc"]))
# outcomes
oids = idcheck(out, "outcomes_ledger", "outcome_id")
for r in out:
    t = f"outcome {r['outcome_id']}"; c = cld.get(r["claim_id"])
    if not c: E(f"{t}: unknown claim_id"); continue
    enum(r, "event_result", {"Occurred","Did not occur","Void/postponed","Unresolved"}, t)
    enum(r, "event_accuracy_status", {"Event occurred","Event did not occur","Unresolved","Void/postponed"}, t)
    if {"Occurred":"Event occurred","Did not occur":"Event did not occur","Unresolved":"Unresolved","Void/postponed":"Void/postponed"}.get(r["event_result"]) != r["event_accuracy_status"]:
        E(f"{t}: event_result {r['event_result']!r} is inconsistent with event_accuracy_status {r['event_accuracy_status']!r}")
    enum(r, "arithmetic_reproduction_status", STAT, t); utc(r, "outcome_recorded_utc", t, True)
    if r["provenance_at_capture_copied"] != c["provenance_at_capture"]: E(f"{t}: must reference the immutable provenance_at_capture (amendments never rewrite outcome records)")
    fz, ot = frozen_for.get(c["capture_id"]), ts(r["outcome_recorded_utc"])
    if not fz: E(f"{t}: no frozen search-space record for this claim's capture before its outcome")
    elif ot and not any(f < ot for f in fz): E(f"{t}: outcome recorded before the search space was frozen")
# coverage
idcheck(cov, "source_coverage_log", "coverage_id")
for r in cov:
    t = f"coverage {r['coverage_id']}"
    enum(r, "coverage_state", {"Not observed","Not supplied"}, t); utc(r, "noted_utc", t, True)
    if not r["description"]: E(f"{t}: description required")
    if r["linked_capture_id"] and r["linked_capture_id"] not in capids: E(f"{t}: unknown linked_capture_id")
# pilot count: unique Eligible selections from Observed captures; claim rows never counted
pilot = sum(1 for r in sel if r["eligibility"] == "Eligible" and capd.get(r["capture_id"], {}).get("record_state") == "Observed")
print(f"capture {len(cap)} | selections {len(sel)} | claims {len(cl)} | amendments {len(am)} | comparisons {len(cmp_)} | outcomes {len(out)} | coverage {len(cov)}")
print(f"pilot count (unique Eligible selections; completeness checkpoint only, target 100): {pilot}")
print(f"errors {len(err)}")
for e in err: print(" -", e)
sys.exit(1 if err else 0)
