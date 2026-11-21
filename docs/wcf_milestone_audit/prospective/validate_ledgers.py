#!/usr/bin/env python3
"""Structural validator for Part 7 ledgers (v0.2). Checks required fields, allowed values, links,
Established-provenance requirements, amendment rules, and that outcomes reference the immutable
capture-time provenance. Evaluates no claim. Research artifact only."""
import csv, sys, pathlib
from datetime import datetime
d = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "ledgers")
def rows(n): return list(csv.DictReader(open(d / n, newline="")))
def ts(x):
    try: return datetime.fromisoformat(x.strip().replace("Z", "+00:00"))
    except Exception: return None
REC = {"Observed","Known but inaccessible"}; COV = {"Not observed","Not supplied"}
ACC = {"Public-full","Public-partial","User-supplied","Locked","Inaccessible"}
PROV = {"Established","Not established","Not applicable"}; YN = {"Yes","No"}
STAT = {"Reproduced","Reproduced with scope qualification","Partially reproduced","Contradicted","Unsupported","Symbolic association only","Missing/inaccessible","Not yet tested"}
SCOPE = {"Regular","Postseason","Combined","Not stated"}; RES = {"Occurred","Did not occur","Void/postponed","Unresolved"}
err = []
cap, cl, am, out, cov = (rows(n) for n in ("capture_log.csv","claims_ledger.csv","provenance_amendments.csv","outcomes_ledger.csv","source_coverage_log.csv"))
capd = {r["capture_id"]: r for r in cap}
if len(capd) != len(cap): err.append("duplicate capture_id")
for r in cap:
    i = r["capture_id"]
    for f in ("capture_id","record_state","capture_timestamp_utc","access_state"):
        if not r[f]: err.append(f"capture {i}: empty {f}")
    if r["record_state"] not in REC: err.append(f"capture {i}: record_state must be Observed or Known but inaccessible (Not observed/Not supplied belong in source_coverage_log)")
    if r["access_state"] not in ACC: err.append(f"capture {i}: bad access_state")
for r in cov:
    if r["coverage_state"] not in COV: err.append(f"coverage {r['coverage_id']}: bad coverage_state")
def established_ok(pub, retr_or_cap, kickoff, visible, unamb, path_or_url):
    return all([ts(pub) and kickoff and ts(kickoff) and ts(pub) < ts(kickoff), ts(retr_or_cap), visible == "Yes", unamb == "Yes", path_or_url])
cld = {}
for r in cl:
    i = r["claim_id"]
    if i in cld: err.append(f"duplicate claim_id {i}")
    cld[i] = r
    c = capd.get(r["capture_id"])
    if not c: err.append(f"claim {i}: unknown capture_id"); continue
    for f in ("claim_id","claim_category","exact_wording","counting_scope","provenance_at_capture"):
        if not r[f]: err.append(f"claim {i}: empty {f}")
    if r["counting_scope"] not in SCOPE: err.append(f"claim {i}: bad counting_scope")
    for f in ("arithmetic_status","source_status"):
        if r[f] not in STAT: err.append(f"claim {i}: bad {f}")
    if r["provenance_at_capture"] not in PROV: err.append(f"claim {i}: bad provenance_at_capture")
    if r["provenance_at_capture"] == "Established" and not established_ok(c["publication_timestamp_utc"], c["capture_timestamp_utc"], c["kickoff_time_utc_of_earliest_game"], r["claim_visible_in_preserved_source"], r["game_player_unambiguous"], r["preserved_evidence_path"] or r["source_urls"]):
        err.append(f"claim {i}: Established at capture requires pre-kickoff publication timestamp, capture timestamp, claim visible in preserved source, unambiguous game/player, and preserved evidence/source")
seen = set()
for a in am:
    i = a["amendment_id"]
    if i in seen: err.append(f"duplicate amendment_id {i}")
    seen.add(i)
    c = cld.get(a["claim_id"])
    if not c: err.append(f"amendment {i}: unknown claim_id"); continue
    if a["new_provenance_status"] not in PROV: err.append(f"amendment {i}: bad new_provenance_status")
    if not ts(a["amended_utc"]) or not a["reason"]: err.append(f"amendment {i}: needs amended_utc and reason")
    if a["new_provenance_status"] == "Established":
        k = capd[c["capture_id"]]["kickoff_time_utc_of_earliest_game"]
        if a["evidence_is_postgame_material"] != "No": err.append(f"amendment {i}: postgame material can never establish provenance")
        elif not established_ok(a["evidence_publication_timestamp_utc"], a["evidence_retrieval_timestamp_utc"], k, a["claim_visible_in_evidence"], a["game_player_unambiguous"], a["evidence_preserved_path"] or a["basis_evidence_url_or_capture"]):
            err.append(f"amendment {i}: upgrade needs newly located evidence with pre-kickoff publication timestamp, retrieval timestamp, claim visible, unambiguous game/player, preserved evidence")
for r in out:
    c = cld.get(r["claim_id"])
    if not c: err.append(f"outcome {r['outcome_id']}: unknown claim_id"); continue
    if r["event_result"] not in RES: err.append(f"outcome {r['outcome_id']}: bad event_result")
    if r["provenance_at_capture_copied"] != c["provenance_at_capture"]:
        err.append(f"outcome {r['outcome_id']}: must reference the immutable provenance_at_capture (amendments never rewrite outcome records)")
print(f"capture {len(cap)} | claims {len(cl)} | amendments {len(am)} | outcomes {len(out)} | coverage {len(cov)} | errors {len(err)}")
for e in err: print(" -", e)
sys.exit(1 if err else 0)
