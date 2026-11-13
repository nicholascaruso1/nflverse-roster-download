#!/usr/bin/env python3
"""v1.1 feature registry, exposure labels, F4 confirmatory spec and hypotheses ledger.

The registry is the preregistration object. It is generated deterministically (no timestamps),
hashed, and recorded with a NOT_FROZEN status: the formal freeze must be declared before any
outcome-joined or prospective analysis (v1.2). Nothing here reads outcomes.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hashchain

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_VERSION = "1.1.0"
REGISTRY_CSV = REPO_ROOT / "reference" / "feature_registry_v1.1.csv"
REGISTRY_META = REPO_ROOT / "reference" / "feature_registry_v1.1.meta.json"
EXPOSURE_CSV = REPO_ROOT / "reference" / "exposure_attestation_v1.1.csv"
F4_SPEC = REPO_ROOT / "reference" / "confirmatory_specs" / "F4_MIRRORED_CURRENT_RECORDS.json"
HYPOTHESES_LEDGER = REPO_ROOT / "research_ledger" / "hypotheses_ledger.csv"

STRING_KINDS = ("city", "nickname", "full_identity")
BASES = ("historical", "current")
CIPHER_FIELDS = ("ordinal", "ordinal_root", "reverse_ordinal", "reverse_root", "pythagorean", "pythagorean_root")
EXACT_FIELDS = ("ordinal", "reverse_ordinal", "pythagorean")
# Pregame quantities compared against name values in the exploratory (Tier B) grid.
QUANTITIES = ("days_remaining", "date_digit_sum", "date_digit_root", "weekday_number", "schedule_week",
              "season_wins", "season_losses", "season_ties",
              "days_since_last_win_rs", "days_since_last_loss_rs", "days_since_last_win_all",
              "days_since_last_loss_all", "days_since_last_thursday_win", "completed_months_since_last_thursday_win")
# Grid quantities that were raised in earlier work (days remaining / days since win-loss with the Pythagorean value).
EXPOSED_QUANTITIES = {"days_remaining", "days_since_last_win_rs", "days_since_last_loss_rs",
                      "days_since_last_win_all", "days_since_last_loss_all"}

REGISTRY_COLUMNS = ["feature_id", "family_id", "tier", "status", "scope", "unit", "string_source", "name_basis",
                    "cipher_field", "match_type", "quantity", "definition", "hypothesis", "primary_outcome",
                    "requires", "exposure_discovery", "exposure_validation", "exposure_holdout",
                    "exposure_prospective", "data_quality", "notes"]

AWAITING = "NO_CLEAN_ATTESTATION"
PREV = "PREVIOUSLY_EXPOSED"
NONE_EST = "NO_OUTCOME_EXPOSURE_ESTABLISHED"
PROSPECTIVE = "PROSPECTIVE_AFTER_FREEZE"
DISCOVERY = "DISCOVERY"


def _row(**kw):
    base = {c: "" for c in REGISTRY_COLUMNS}
    base.update(kw)
    return base


def named_features():
    """F1-F10 with the statuses and exposure labels approved on 2026-11-12."""
    exp_1_5 = dict(exposure_discovery=DISCOVERY, exposure_validation=AWAITING, exposure_holdout=PREV,
                   exposure_prospective=PROSPECTIVE)
    exp_6_7 = dict(exposure_discovery=PREV, exposure_validation=PREV, exposure_holdout=PREV,
                   exposure_prospective=PROSPECTIVE)
    exp_8_10 = dict(exposure_discovery=NONE_EST, exposure_validation=NONE_EST, exposure_holdout=NONE_EST,
                    exposure_prospective=PROSPECTIVE)
    desc = "DESCRIPTIVE_ONLY"
    pyth = "any of city/nickname/full exact Pythagorean value (historical names)"
    rows = [
        _row(feature_id="F1_NAME_EQ_DAYS_REMAINING", family_id="F1", tier="named", status=desc, scope="n/a",
             unit="team_game", string_source="city|nickname|full_identity", name_basis="historical",
             cipher_field="pythagorean", match_type="exact", quantity="days_remaining",
             definition=f"{pyth} equals days remaining in the calendar year (Dec 31 minus game date, excluding game date).",
             hypothesis="none (descriptive only; no significance test)", primary_outcome="not_defined",
             data_quality="computed", notes="~4.3-4.5% of games have exactly one side qualifying; MDE too large for confirmatory use.", **exp_1_5),
        _row(feature_id="F2_NAME_EQ_DAYS_SINCE_LOSS_RS", family_id="F2", tier="named", status=desc, scope="rs",
             unit="team_game", string_source="city|nickname|full_identity", name_basis="historical",
             cipher_field="pythagorean", match_type="exact", quantity="days_since_last_loss_rs",
             definition=f"{pyth} equals days since the team's last regular-season loss.",
             hypothesis="none (descriptive only)", primary_outcome="not_defined", data_quality="official_schedule_result",
             notes="~1.6-2.9% prevalence.", **exp_1_5),
        _row(feature_id="F2_NAME_EQ_DAYS_SINCE_LOSS_ALL", family_id="F2", tier="named", status=desc, scope="all",
             unit="team_game", string_source="city|nickname|full_identity", name_basis="historical",
             cipher_field="pythagorean", match_type="exact", quantity="days_since_last_loss_all",
             definition=f"{pyth} equals days since the team's last loss including playoffs.",
             hypothesis="none (descriptive only)", primary_outcome="not_defined", data_quality="official_schedule_result",
             notes="Playoff-inclusive variant; never mixed with the rs variant.", **exp_1_5),
        _row(feature_id="F3_NAME_EQ_DAYS_SINCE_WIN_RS", family_id="F3", tier="named", status=desc, scope="rs",
             unit="team_game", string_source="city|nickname|full_identity", name_basis="historical",
             cipher_field="pythagorean", match_type="exact", quantity="days_since_last_win_rs",
             definition=f"{pyth} equals days since the team's last regular-season win.",
             hypothesis="none (descriptive only)", primary_outcome="not_defined", data_quality="official_schedule_result",
             notes="~1.5-3.4% prevalence.", **exp_1_5),
        _row(feature_id="F3_NAME_EQ_DAYS_SINCE_WIN_ALL", family_id="F3", tier="named", status=desc, scope="all",
             unit="team_game", string_source="city|nickname|full_identity", name_basis="historical",
             cipher_field="pythagorean", match_type="exact", quantity="days_since_last_win_all",
             definition=f"{pyth} equals days since the team's last win including playoffs.",
             hypothesis="none (descriptive only)", primary_outcome="not_defined", data_quality="official_schedule_result",
             notes="Playoff-inclusive variant.", **exp_1_5),
        _row(feature_id="F4_MIRRORED_CURRENT_RECORDS", family_id="F4", tier="A", status="CONFIRMATORY", scope="rs",
             unit="game", string_source="n/a", name_basis="n/a", cipher_field="n/a", match_type="record",
             quantity="current_season_records",
             definition="Before kickoff the two teams have mirrored regular-season records: away wins = home losses, away losses = home wins, ties equal; both teams must have played at least one game.",
             hypothesis="Mirrored-record matchups have a HOME_WIN/AWAY_WIN/TIE distribution different from the season-week permutation baseline after prior-record adjustment. Nondirectional.",
             primary_outcome="HOME_WIN|AWAY_WIN|TIE", data_quality="official_schedule_result",
             notes="Only approved Tier A feature. Approved for preregistration, not evidence of an effect. See confirmatory_specs/F4_MIRRORED_CURRENT_RECORDS.json.",
             **exp_1_5),
        _row(feature_id="F5_PREVIOUS_MEETING_TIED_RS", family_id="F5", tier="named", status=desc, scope="rs", unit="game",
             string_source="n/a", name_basis="n/a", cipher_field="n/a", match_type="record", quantity="previous_meeting",
             definition="The most recent regular-season meeting of the two franchises (any prior season) ended tied.",
             hypothesis="none (descriptive only)", primary_outcome="not_defined", data_quality="official_schedule_result",
             notes="Extremely small qualifying sample (2-8 games per split).", **exp_1_5),
        _row(feature_id="F5_PREVIOUS_MEETING_TIED_ALL", family_id="F5", tier="named", status=desc, scope="all", unit="game",
             string_source="n/a", name_basis="n/a", cipher_field="n/a", match_type="record", quantity="previous_meeting",
             definition="The most recent meeting including playoffs ended tied.",
             hypothesis="none (descriptive only)", primary_outcome="not_defined", data_quality="official_schedule_result",
             notes="Playoff-inclusive variant.", **exp_1_5),
        _row(feature_id="F6_NAME_EQ_OWN_FINAL_SCORE", family_id="F6", tier="named", status=desc, scope="rs", unit="team_game",
             string_source="city|nickname|full_identity", name_basis="historical", cipher_field="pythagorean",
             match_type="exact", quantity="own_final_score",
             definition="Name value equals the team's own final score.", hypothesis="none (descriptive only)",
             primary_outcome="not_defined", requires="OUTCOME_SCORE", data_quality="official_schedule_result",
             notes="Outcome-defined: NOT computed in v1.1. Aggregate scoreline frequencies were already computed over all splits.", **exp_6_7),
        _row(feature_id="F7_GAME_TOTAL_EQ_54", family_id="F7", tier="named", status=desc, scope="rs", unit="game",
             string_source="n/a", name_basis="n/a", cipher_field="n/a", match_type="record", quantity="game_total",
             definition="Combined final score equals 54.", hypothesis="none (descriptive only)", primary_outcome="not_defined",
             requires="OUTCOME_SCORE", data_quality="official_schedule_result",
             notes="Outcome-defined: NOT computed in v1.1. Aggregate frequency already computed over all splits.", **exp_6_7),
        _row(feature_id="F8_PLAYER_MATCH_TD_RATE", family_id="F8", tier="named", status=desc + "_PENDING_PREVALENCE_AND_POWER",
             scope="rs", unit="player_game", string_source="player full_name vs opponent nickname", name_basis="historical",
             cipher_field="ordinal|reverse_ordinal|pythagorean", match_type="exact", quantity="player_touchdowns",
             definition="Player on the PREVIOUS_WEEK_ROSTER proxy whose exact name value equals the opponent nickname value; outcome would be touchdowns vs the player's own pregame baseline.",
             hypothesis="none (descriptive only)", primary_outcome="not_defined", requires="PBP;ROSTER_PROXY",
             data_quality="roster_proxy_not_game_day_active", notes="v1.1 builds candidate matches only; no outcome join.", **exp_8_10),
        _row(feature_id="F9_PLAYER_MATCH_RECEPTIONS_YARDS", family_id="F9", tier="named",
             status=desc + "_PENDING_PREVALENCE_AND_POWER", scope="rs", unit="player_game",
             string_source="player full_name vs opponent nickname", name_basis="historical",
             cipher_field="ordinal|reverse_ordinal|pythagorean", match_type="exact", quantity="receptions_receiving_yards",
             definition="Same candidate set as F8; outcomes would be receptions and receiving yards vs own pregame baseline.",
             hypothesis="none (descriptive only)", primary_outcome="not_defined", requires="PBP;ROSTER_PROXY",
             data_quality="roster_proxy_not_game_day_active", notes="No outcome join in v1.1.", **exp_8_10),
        _row(feature_id="F10_PLAYER_MATCH_TEAM_WIN", family_id="F10", tier="named",
             status=desc + "_PENDING_PREVALENCE_AND_POWER", scope="rs", unit="game",
             string_source="player full_name vs opponent nickname", name_basis="historical",
             cipher_field="ordinal|reverse_ordinal|pythagorean", match_type="exact", quantity="team_win",
             definition="At least one candidate player match on the team's PREVIOUS_WEEK_ROSTER proxy; outcome would be team win.",
             hypothesis="none (descriptive only)", primary_outcome="not_defined", requires="ROSTER_PROXY",
             data_quality="roster_proxy_not_game_day_active", notes="Needs prevalence and independent-sample review before any reconsideration.", **exp_8_10),
    ]
    return rows


def tnf_blocked_features():
    blocked = []
    for fid, qty, definition in (
            ("TNF_RECORD_VERIFIED", "tnf_record", "Team record in verified branded-TNF games (broadcast_category = CORE_TNF)."),
            ("TNF_COMPLETED_MONTHS_SINCE_LAST_TNF_WIN", "completed_months_since_last_tnf_win",
             "Completed calendar months since the team's last verified branded-TNF win."),
            ("TNF_DAYS_SINCE_LAST_TNF_WIN", "days_since_last_tnf_win", "Days since the team's last verified branded-TNF win.")):
        blocked.append(_row(feature_id=fid, family_id="TNF", tier="B", status="BLOCKED_TNF", scope="rs", unit="team_game",
                            match_type="record", quantity=qty, definition=definition, hypothesis="none (blocked)",
                            primary_outcome="not_defined", requires="VERIFIED_TNF_TABLE",
                            exposure_discovery=NONE_EST, exposure_validation=NONE_EST, exposure_holdout=NONE_EST,
                            exposure_prospective=PROSPECTIVE, data_quality="unavailable",
                            notes="Excluded from computation and multiplicity denominators until the verified table is populated."))
    return blocked


def grid_features():
    rows = []
    for kind in STRING_KINDS:
        for basis in BASES:
            for field in CIPHER_FIELDS:
                for qty in QUANTITIES:
                    exact = field in EXACT_FIELDS
                    exposed = exact and field == "pythagorean" and basis == "historical" and qty in EXPOSED_QUANTITIES
                    scope = "all" if qty.endswith("_all") else ("rs" if qty.endswith("_rs") else "n/a")
                    rows.append(_row(
                        feature_id=f"B__{kind}__{basis}__{field}__{qty}", family_id=f"FAM__{kind}__{basis}__{qty}",
                        tier="B", status="EXPLORATORY", scope=scope, unit="team_game", string_source=kind,
                        name_basis=basis, cipher_field=field, match_type="exact" if exact else "root", quantity=qty,
                        definition=(f"{basis} {kind} {field} equals {qty}" if exact else
                                    f"{basis} {kind} {field} equals digital_root({qty})"),
                        hypothesis="none (exploratory; hypothesis-generating only)", primary_outcome="not_defined",
                        exposure_discovery=DISCOVERY, exposure_validation=NONE_EST,
                        exposure_holdout=PREV if exposed else NONE_EST, exposure_prospective=PROSPECTIVE,
                        data_quality="computed",
                        notes="Raised in earlier work; conservative PREVIOUSLY_EXPOSED label." if exposed else
                              "Unattested: no outcome exposure established in the project record."))
    return rows


def build_registry():
    frame = pd.DataFrame(named_features() + tnf_blocked_features() + grid_features(), columns=REGISTRY_COLUMNS)
    return frame.sort_values(["tier", "feature_id"], key=lambda s: s.map(lambda v: (0 if v == "A" else 1 if v == "named" else 2 if v == "B" else 3) if s.name == "tier" else v)).reset_index(drop=True)


def registry_csv_bytes(frame):
    return frame.to_csv(index=False, lineterminator="\n").encode("utf-8")


def registry_sha256(frame=None):
    frame = build_registry() if frame is None else frame
    return hashlib.sha256(registry_csv_bytes(frame)).hexdigest()


def registry_meta(frame):
    grid = frame[frame.tier == "B"]
    active_grid = grid[grid.status == "EXPLORATORY"]
    return {"registry_version": REGISTRY_VERSION, "sha256": registry_sha256(frame), "rows": int(len(frame)),
            "freeze_status": "NOT_FROZEN (v1.1 build; the freeze, with this hash, must be declared before any "
                             "outcome-joined analysis or prospective evaluation)",
            "confirmatory_features": sorted(frame[frame.status == "CONFIRMATORY"].feature_id),
            "descriptive_only_features": sorted(frame[frame.status.str.startswith("DESCRIPTIVE_ONLY")].feature_id),
            "blocked_tnf_features": sorted(frame[frame.status == "BLOCKED_TNF"].feature_id),
            "exploratory_grid_size": int(len(active_grid)),
            "exploratory_family_count": int(active_grid.family_id.nunique()),
            "grid_dimensions": {"string_kinds": list(STRING_KINDS), "name_bases": list(BASES),
                                "cipher_fields": list(CIPHER_FIELDS), "quantities": list(QUANTITIES)},
            "multiplicity_denominator_note": "Denominator for any exploratory test is exploratory_grid_size (all features), "
                                             "never the number of features someone noticed."}


def f4_spec():
    return {
        "feature_id": "F4_MIRRORED_CURRENT_RECORDS", "tier": "A", "status": "CONFIRMATORY",
        "approval": "Approved for preregistration only by Nick on 2026-11-12 (governance review). Not evidence of an effect.",
        "operational_definition": "Before kickoff, the two teams have mirrored regular-season records: away wins equal home losses, away losses equal home wins, and ties are equal; both teams have >= 1 completed regular-season game.",
        "unit": "game",
        "denominator": "All eligible completed regular-season games with valid pregame records",
        "expected_prevalence": {"discovery_1999_2018": "15.0%", "validation_2019_2022": "14.6%", "holdout_2023_2025": "14.3%",
                                "basis": "outcome-blind counts from Revision 1 of the v1.1 plan"},
        "hypothesis": "Mirrored-record matchups have an outcome distribution different from the prespecified season-week permutation baseline after prior-record adjustment.",
        "direction": "Nondirectional; no team is selected by the feature",
        "primary_outcome": ["HOME_WIN", "AWAY_WIN", "TIE"],
        "tie_treatment": "Report ties separately; use 0.5 only when calculating win percentage",
        "comparison_baseline": "Season-week permutation null plus prior-record-strength adjustment",
        "minimum_qualifying_n": "No universal cutoff; actual power and MDE must be calculated and reported before testing. Expected validation count about 154.",
        "multiplicity_correction": "BH across the registered grid, max-T for the feature family, Holm across Tier A",
        "promotion_criteria": "Must pass the preregistered validation test after multiplicity correction and then succeed in one clean prospective confirmation.",
        "exposure": {"discovery_1999_2018": DISCOVERY, "validation_2019_2022": AWAITING,
                     "holdout_2023_2025": PREV, "prospective_2026_onward": PROSPECTIVE},
        "testing_sequence": ["1999-2018 discovery and exploratory development",
                             "2019-2022 validation with exposure status documented",
                             "freeze registry and its hash before any prospective outcome analysis",
                             "2023-2025 previously exposed: descriptive evidence only",
                             "2026 onward: prospective confirmation, one prespecified evaluation after the minimum sample/power requirement is reached"],
        "stopping_rule": "PENDING_PRE_FREEZE: minimum sample, evaluation timing and stopping rule must be written here and frozen before any prospective outcome analysis. No repeated significance peeking.",
        "data_quality": "High, subject to schedule and pregame-record reconciliation",
        "data_requirements": "Schedule results only (pregame records); no player or TNF data",
    }


def exposure_attestation(frame):
    rows = []
    notes = {
        "named": "Conservative governance classification relayed by Nick from the 2026-11-12 review; not a claim that prior outcome-linked tests occurred.",
        "A": "Same as named (F4).",
        "B": "Unattested default; features overlapping the F1-F3 quantities with the Pythagorean value are labelled PREVIOUSLY_EXPOSED for 2023-2025.",
    }
    scoreline = ("Aggregate scoreline frequencies were computed over 1999-2026 regular-season games, including 2023-2025, "
                 "in the v1.0.1 engine output and the v1.0 audit; labelled exposed across all historical splits.")
    for r in frame.itertuples():
        if r.tier not in ("A", "named", "B") or r.status == "BLOCKED_TNF":
            continue
        if r.tier == "B" and r.exposure_holdout == NONE_EST:
            continue  # unattested grid default is summarised by the registry meta, not row by row
        basis = scoreline if r.family_id in ("F6", "F7") else notes[r.tier]
        for split in ("discovery", "validation", "holdout", "prospective"):
            rows.append({"feature_id": r.feature_id, "split": split, "label": getattr(r, f"exposure_{split}"),
                         "basis": basis, "attested_by": "Nick (relayed governance review, 2026-11-12) with Claude session record"})
    return pd.DataFrame(rows)


LEDGER_FIELDS = ["hypothesis_row", "event_ts_utc", "event_type", "feature_id", "tier", "status", "exposure_discovery",
                 "exposure_validation", "exposure_holdout", "exposure_prospective", "statement", "registry_sha256",
                 "code_commit", "approval_ref", "result", "prev_hash", "row_hash"]


def register_hypotheses(frame, ledger_path=HYPOTHESES_LEDGER, code_commit="unknown"):
    """Append REGISTERED events for features not yet on the ledger. Existing rows are never changed."""
    existing = {r["feature_id"] for r in hashchain.read_rows(ledger_path) if r["event_type"] == "REGISTERED"}
    sha = registry_sha256(frame)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rows, skipped = [], []
    for r in frame[frame.tier.isin(["A", "named"])].itertuples():
        if r.feature_id in existing:
            skipped.append(r.feature_id); continue
        rows.append({"event_ts_utc": now, "event_type": "REGISTERED", "feature_id": r.feature_id, "tier": r.tier,
                     "status": r.status, "exposure_discovery": r.exposure_discovery,
                     "exposure_validation": r.exposure_validation, "exposure_holdout": r.exposure_holdout,
                     "exposure_prospective": r.exposure_prospective, "statement": r.definition + " | " + r.hypothesis,
                     "registry_sha256": sha, "code_commit": code_commit,
                     "approval_ref": "v1.1 governance approval 2026-11-12", "result": "NOT_TESTED"})
    if "TIER_B_EXPLORATORY_GRID" not in existing:
        meta = registry_meta(frame)
        rows.append({"event_ts_utc": now, "event_type": "REGISTERED", "feature_id": "TIER_B_EXPLORATORY_GRID", "tier": "B",
                     "status": "EXPLORATORY", "exposure_discovery": DISCOVERY, "exposure_validation": NONE_EST,
                     "exposure_holdout": NONE_EST, "exposure_prospective": PROSPECTIVE,
                     "statement": f"Exploratory grid of {meta['exploratory_grid_size']} features in {meta['exploratory_family_count']} families; hypothesis-generating only; no promotion without confirmation on unseen data.",
                     "registry_sha256": sha, "code_commit": code_commit,
                     "approval_ref": "v1.1 governance approval 2026-11-12", "result": "NOT_TESTED"})
    total, head = hashchain.append(ledger_path, LEDGER_FIELDS, "hypothesis_row", rows) if rows else (len(hashchain.read_rows(ledger_path)), None)
    return {"appended": len(rows), "skipped_existing": len(skipped), "total_rows": total, "chain_head": head}


def write_registry_files():
    frame = build_registry()
    REGISTRY_CSV.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_CSV.write_bytes(registry_csv_bytes(frame))
    REGISTRY_META.write_text(json.dumps(registry_meta(frame), indent=2, sort_keys=True) + "\n")
    F4_SPEC.parent.mkdir(parents=True, exist_ok=True)
    F4_SPEC.write_text(json.dumps(f4_spec(), indent=2) + "\n")
    exposure_attestation(frame).to_csv(EXPOSURE_CSV, index=False, lineterminator="\n")
    return frame


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--register", action="store_true", help="also append REGISTERED events to the hypotheses ledger")
    p.add_argument("--code-commit", default="unknown")
    p.add_argument("--verify", action="store_true", help="verify registry files and hypotheses ledger")
    a = p.parse_args()
    if a.verify:
        frame = build_registry()
        ok_csv = REGISTRY_CSV.exists() and REGISTRY_CSV.read_bytes() == registry_csv_bytes(frame)
        meta = json.loads(REGISTRY_META.read_text()) if REGISTRY_META.exists() else {}
        ok_meta = meta.get("sha256") == registry_sha256(frame)
        ok, n, head, errors = hashchain.verify(HYPOTHESES_LEDGER, LEDGER_FIELDS, "hypothesis_row")
        print(json.dumps({"registry_csv_matches_code": ok_csv, "registry_meta_hash_matches": ok_meta,
                          "hypotheses_ledger_ok": ok, "hypotheses_rows": n, "errors": errors}, indent=2))
        sys.exit(0 if (ok_csv and ok_meta and ok) else 1)
    frame = write_registry_files()
    print("registry rows:", len(frame), "sha256:", registry_sha256(frame))
    if a.register:
        print(register_hypotheses(frame, code_commit=a.code_commit))

if __name__ == "__main__":
    main()
