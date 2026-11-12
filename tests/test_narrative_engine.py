import hashlib
import json
import os
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import nfl_script_narrative_engine as engine

FIXTURES = ROOT / "tests" / "fixtures"
CAR_TB = FIXTURES / "games_car_tb_2025.csv"
COLS = ["game_id", "season", "game_type", "week", "gameday", "gametime",
        "away_team", "away_score", "home_team", "home_score"]


def game(season, week, day, time, away, home, a, h, gtype="REG"):
    return {"game_id": f"{season}_{week:02d}_{away}_{home}", "season": season, "game_type": gtype,
            "week": week, "gameday": day, "gametime": time, "away_team": away, "away_score": a,
            "home_team": home, "home_score": h}


def write_games(path, rows, extra_cols=None):
    frame = pd.DataFrame(rows)
    for col, val in (extra_cols or {}).items():
        frame[col] = val
    frame.to_csv(path, index=False)
    return path


def run_engine(games, day, away, home, tmp, extra=None, ledger=True):
    argv = ["--games", str(games), "--date", day, "--away", away, "--home", home,
            "--output", str(Path(tmp) / "out")]
    argv += ["--ledger", str(Path(tmp) / "ledger.csv")] if ledger else ["--no-ledger"]
    argv += extra or []
    return engine.run(engine.build_parser().parse_args(argv))


def findings_by_id(findings, feature_id, team=None):
    return [f for f in findings if f["feature_id"] == feature_id and (team is None or f["team"] == team)]


class CipherTests(unittest.TestCase):
    def test_pythagorean_values(self):
        self.assertEqual(engine.ciphers("WASHINGTON")["pythagorean"], 49)
        self.assertEqual(engine.ciphers("GIANTS")["pythagorean"], 25)

    def test_ordinal_values(self):
        self.assertEqual(engine.ciphers("COMMANDERS")["ordinal"], 105)
        self.assertEqual(engine.ciphers("GIANTS")["ordinal"], 70)

    def test_reverse_ordinal_is_27_minus_ordinal_letters(self):
        for word in ("GIANTS", "COMMANDERS", "WASHINGTON"):
            c = engine.ciphers(word)
            self.assertEqual(c["ordinal"] + c["reverse_ordinal"], 27 * c["letters"])
        self.assertEqual(engine.ciphers("GIANTS")["reverse_ordinal"], 92)

    def test_record_uses_only_games_team_played(self):
        games = pd.DataFrame([
            {"away_team": "WAS", "home_team": "NYG", "away_score": 20, "home_score": 17},
            {"away_team": "DAL", "home_team": "PHI", "away_score": 10, "home_score": 24}])
        self.assertEqual(engine.team_record(games, "WAS")["record"], "1-0-0")
        self.assertEqual(engine.team_record(games, "NYG")["record"], "0-1-0")

    def test_digital_root(self):
        self.assertEqual(engine.digital_root(49), 4)
        self.assertEqual(engine.digital_root(25), 7)
        self.assertEqual(engine.digital_root(0), 0)


class JanuarySeasonRegressionTests(unittest.TestCase):
    """v1.0 used the calendar year as the season, so every January game was wrong."""

    def test_car_tb_2026_01_03_uses_2025_season_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            context, findings = run_engine(CAR_TB, "2026-01-03", "CAR", "TB", tmp)
        self.assertEqual(context["season"], 2025)
        self.assertEqual(context["season_source"], "nflverse_schedule")
        self.assertEqual(context["game_id"], "2025_18_CAR_TB")
        self.assertEqual(context["week"], 18)
        self.assertEqual(context["season_records_before_game"]["CAR"]["record"], "8-8-0")
        self.assertEqual(context["season_records_before_game"]["TB"]["record"], "7-9-0")
        self.assertNotEqual(context["season_records_before_game"]["CAR"]["record"], "0-0-0")

    def test_date_fallback_assigns_january_to_previous_season(self):
        self.assertEqual(engine.nfl_season_for_date(date(2026, 1, 3)), 2025)
        self.assertEqual(engine.nfl_season_for_date(date(2026, 2, 8)), 2025)
        self.assertEqual(engine.nfl_season_for_date(date(2025, 9, 7)), 2025)

    def test_roster_file_uses_nfl_season_not_calendar_year(self):
        with tempfile.TemporaryDirectory() as tmp:
            roster_dir = Path(tmp) / "rosters"
            roster_dir.mkdir()
            pd.DataFrame([{"season": 2025, "week": 18, "team": "TB", "status": "ACT", "full_name": "Commanders"}]
                         ).to_csv(roster_dir / "roster_weekly_2025.csv", index=False)
            context, _ = run_engine(CAR_TB, "2026-01-03", "CAR", "TB", tmp, ["--rosters", str(roster_dir)])
        self.assertEqual(context["roster_snapshot_week"], 18)


class FranchiseAliasTests(unittest.TestCase):
    def test_era_codes_map_to_franchise(self):
        self.assertEqual(engine.to_franchise("OAK"), "LV")
        self.assertEqual(engine.to_franchise("LV"), "LV")
        self.assertEqual(engine.to_franchise("SD"), "LAC")
        self.assertEqual(engine.to_franchise("STL"), "LA")
        self.assertEqual(engine.to_franchise("LAR"), "LA")

    def test_legacy_roster_codes_map_to_franchise(self):
        for raw, expected in (("ARZ", "ARI"), ("BLT", "BAL"), ("CLV", "CLE"), ("HST", "HOU"), ("SL", "LA")):
            self.assertEqual(engine.to_franchise(raw), expected)

    def test_unknown_code_raises(self):
        with self.assertRaises(ValueError):
            engine.to_franchise("XXX")

    def test_history_is_continuous_across_relocation(self):
        rows = [game(2018, 3, "2018-09-23", "16:25", "OAK", "KC", 10, 20),
                game(2021, 3, "2021-09-26", "16:25", "LV", "KC", 31, 28),
                game(2021, 5, "2021-10-10", "13:00", "KC", "LV", 14, 17)]
        with tempfile.TemporaryDirectory() as tmp:
            path = write_games(Path(tmp) / "g.csv", rows)
            frame = engine.load_games(path, date(2022, 1, 1))
            self.assertEqual(engine.team_record(frame, "LV")["record"], "2-1-0")
            context, _ = run_engine(path, "2022-09-11", "OAK", "KC", tmp)
        self.assertEqual(context["head_to_head"]["games"], 3)
        self.assertEqual(context["away"], "LV")

    def test_san_diego_and_st_louis_history_kept(self):
        rows = [game(2010, 1, "2010-09-12", "13:00", "SD", "KC", 21, 14),
                game(2010, 2, "2010-09-19", "13:00", "STL", "OAK", 13, 16),
                game(2020, 1, "2020-09-13", "13:00", "LAC", "KC", 20, 23),
                game(2020, 2, "2020-09-20", "13:00", "LA", "LV", 30, 17)]
        with tempfile.TemporaryDirectory() as tmp:
            frame = engine.load_games(write_games(Path(tmp) / "g.csv", rows), date(2021, 1, 1))
        self.assertEqual(engine.team_record(frame, "LAC")["record"], "1-1-0")
        self.assertEqual(engine.team_record(frame, "LA")["record"], "1-1-0")

    def test_real_schedule_codes_all_have_identity_eras(self):
        table = engine.identities()
        self.assertEqual(len(table.franchise_id.unique()), 32)
        self.assertIn(("LV", "OAK"), set(zip(table.franchise_id, table.code)))


class HistoricalIdentityTests(unittest.TestCase):
    def test_washington_name_eras(self):
        self.assertEqual(engine.identity_for("WAS", 2019)["nickname"], "Redskins")
        self.assertEqual(engine.identity_for("WAS", 2021)["nickname"], "Football Team")
        self.assertEqual(engine.identity_for("WAS", 2022)["nickname"], "Commanders")

    def test_relocation_cities(self):
        self.assertEqual(engine.identity_for("LV", 2019)["city"], "Oakland")
        self.assertEqual(engine.identity_for("LV", 2020)["city"], "Las Vegas")
        self.assertEqual(engine.identity_for("LAC", 2016)["city"], "San Diego")
        self.assertEqual(engine.identity_for("LAC", 2017)["city"], "Los Angeles")
        self.assertEqual(engine.identity_for("LA", 2015)["city"], "St. Louis")
        self.assertEqual(engine.identity_for("LA", 2016)["city"], "Los Angeles")

    def test_historical_primary_and_current_separate(self):
        rows = [game(2015, 1, "2015-09-13", "13:00", "OAK", "KC", 10, 20)]
        with tempfile.TemporaryDirectory() as tmp:
            path = write_games(Path(tmp) / "g.csv", rows)
            context, findings = run_engine(path, "2015-09-20", "OAK", "KC", tmp)
        lv = context["team_ciphers"]["LV"]
        self.assertEqual(lv["historical"]["city"], "Oakland")
        self.assertEqual(lv["current"]["city"], "Las Vegas")
        self.assertFalse(lv["current_equals_historical"])
        hist = [f for f in findings if f["feature_id"] == "gematria.city.ordinal" and f["team"] == "LV" and f["name_basis"] == "historical"]
        cur = [f for f in findings if f["feature_id"] == "gematria.city.ordinal" and f["team"] == "LV" and f["name_basis"] == "current"]
        self.assertEqual(int(hist[0]["value"]), engine.ciphers("OAKLAND")["ordinal"])
        self.assertEqual(int(cur[0]["value"]), engine.ciphers("LAS VEGAS")["ordinal"])
        self.assertNotEqual(hist[0]["value"], cur[0]["value"])
        kc = [f for f in findings if f["team"] == "KC" and f["name_basis"] == "current"]
        self.assertEqual(kc, [])

    def test_commanders_era_game_uses_historical_redskins_value(self):
        rows = [game(2010, 1, "2010-09-12", "13:00", "WAS", "DAL", 13, 7)]
        with tempfile.TemporaryDirectory() as tmp:
            context, _ = run_engine(write_games(Path(tmp) / "g.csv", rows), "2010-09-19", "WAS", "DAL", tmp)
        self.assertEqual(context["team_ciphers"]["WAS"]["historical"]["nickname"], "Redskins")
        self.assertEqual(context["team_ciphers"]["WAS"]["current"]["nickname"], "Commanders")


class SanFranciscoTests(unittest.TestCase):
    def test_display_name_keeps_49ers_and_ciphers_are_consistent(self):
        sf = engine.identity_for("SF", 2024)
        self.assertEqual(sf["display_name"], "San Francisco 49ers")
        strings = engine.identity_strings(sf)
        full = engine.ciphers(strings["full_identity"])
        parts = engine.ciphers(strings["city"])["ordinal"] + engine.ciphers(strings["nickname"])["ordinal"]
        self.assertEqual(full["ordinal"], parts)
        self.assertEqual(engine.letters(strings["nickname"]), "FORTYNINERS")


class CalendarMonthTests(unittest.TestCase):
    def test_boundaries_vs_completed_months(self):
        em = engine.elapsed_months(date(2022, 10, 13), date(2026, 11, 12))
        self.assertEqual(em, {"days": 1491, "month_boundaries": 49, "completed_months": 48})

    def test_exact_month_anniversary_is_completed(self):
        em = engine.elapsed_months(date(2022, 10, 12), date(2026, 11, 12))
        self.assertEqual(em["completed_months"], 49)
        self.assertEqual(em["month_boundaries"], 49)

    def test_engine_reports_both_separately(self):
        rows = [game(2022, 6, "2022-10-13", "20:15", "WAS", "CHI", 12, 7),
                game(2026, 9, "2026-11-05", "20:15", "NYG", "DAL", 10, 17)]
        with tempfile.TemporaryDirectory() as tmp:
            _, findings = run_engine(write_games(Path(tmp) / "g.csv", rows), "2026-11-12", "WAS", "NYG", tmp)
        boundary = findings_by_id(findings, "calendar.month_boundaries_since_last_thursday_win", "WAS")[0]
        completed = findings_by_id(findings, "calendar.completed_months_since_last_thursday_win", "WAS")[0]
        self.assertEqual((boundary["value"], completed["value"]), ("49", "48"))


class MirroredRecordTests(unittest.TestCase):
    def test_zero_zero_not_mirrored(self):
        zero = {"wins": 0, "losses": 0, "ties": 0, "games": 0}
        self.assertFalse(engine.mirrored(zero, zero))

    def test_true_mirror_detected(self):
        a = engine.team_record(pd.DataFrame([{"away_team": "A", "home_team": "B", "away_score": 1, "home_score": 0}]), "A")
        b = engine.team_record(pd.DataFrame([{"away_team": "A", "home_team": "B", "away_score": 1, "home_score": 0}]), "B")
        self.assertTrue(engine.mirrored(a, b))

    def test_week1_run_has_no_mirrored_finding(self):
        rows = [game(2024, 1, "2024-09-08", "13:00", "NE", "CIN", 16, 10)]
        with tempfile.TemporaryDirectory() as tmp:
            context, findings = run_engine(write_games(Path(tmp) / "g.csv", rows), "2025-09-07", "DAL", "PHI", tmp)
        self.assertEqual(findings_by_id(findings, "records.mirrored_current_season"), [])
        self.assertEqual(context["season_records_before_game"]["DAL"]["record"], "0-0-0")


class ThursdayTnfTests(unittest.TestCase):
    def test_slot_classification(self):
        self.assertEqual(engine.classify_slot(date(2025, 11, 27), "20:20"), "thanksgiving")
        self.assertEqual(engine.classify_slot(date(2025, 11, 27), "13:00"), "thanksgiving")
        self.assertEqual(engine.classify_slot(date(2025, 10, 9), "20:15"), "thursday_evening_proxy")
        self.assertEqual(engine.classify_slot(date(2025, 10, 9), "13:00"), "thursday_other")
        self.assertEqual(engine.classify_slot(date(2025, 10, 12), "20:20"), "sunday_night_proxy")
        self.assertEqual(engine.classify_slot(date(2025, 10, 13), "20:15"), "monday_night_proxy")
        self.assertEqual(engine.classify_slot(date(2025, 10, 12), "13:00"), "other")

    def _rows(self):
        return [game(2024, 6, "2024-10-10", "20:15", "SF", "SEA", 36, 24),
                game(2024, 12, "2024-11-28", "20:20", "SF", "GB", 10, 38),
                game(2024, 14, "2024-12-05", "20:15", "SF", "LA", 6, 12)]

    def test_no_branded_tnf_without_verified_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            context, findings = run_engine(write_games(Path(tmp) / "g.csv", self._rows()), "2025-10-02", "SF", "SEA", tmp,
                                           ["--claimed-away-tnf-record", "3-9"])
        tnf = findings_by_id(findings, "schedule.branded_tnf_verified_record", "SF")[0]
        self.assertTrue(tnf["value"].startswith("unavailable"))
        proxy = findings_by_id(findings, "schedule.thursday_evening_proxy_record", "SF")[0]
        self.assertEqual(proxy["value"], "1-1-0")
        self.assertEqual(proxy["data_quality"], "schedule_proxy_not_tnf")
        thanks = findings_by_id(findings, "schedule.thanksgiving_record", "SF")[0]
        self.assertEqual(thanks["value"], "0-1-0")
        claim = findings_by_id(findings, "claim_audit.external_tnf_record", "SF")[0]
        self.assertIn("unavailable", claim["value"])
        self.assertEqual(claim["data_quality"], "external_claim_unverified")

    def test_verified_table_rows_counted_unverified_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            table = Path(tmp) / "tnf.csv"
            base = {"season": 2024, "week": 6, "gameday": "2024-10-10", "away_team": "SF", "home_team": "SEA",
                    "network": "Prime Video", "tnf_brand_status": "branded_tnf",
                    "source_url": "https://example.test/src", "verification_status": "verified"}
            pd.DataFrame([
                {**base, "game_id": "2024_06_SF_SEA"},
                {**base, "game_id": "2024_14_SF_LA", "verification_status": "candidate_unverified"},
                {**base, "game_id": "2024_12_SF_GB", "source_url": ""}]).to_csv(table, index=False)
            context, findings = run_engine(write_games(Path(tmp) / "g.csv", self._rows()), "2025-10-02", "SF", "SEA", tmp,
                                           ["--tnf-table", str(table)])
        self.assertEqual(context["tnf_table"]["verified_rows"], 1)
        rec = findings_by_id(findings, "schedule.branded_tnf_verified_record", "SF")[0]
        self.assertEqual(rec["value"], "1-0-0")
        self.assertEqual(rec["data_quality"], "verified_external_table")


class ProvenanceTests(unittest.TestCase):
    def test_hashes_coverage_and_code_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            context, _ = run_engine(CAR_TB, "2026-01-03", "CAR", "TB", tmp)
        sched = context["provenance"]["inputs"][0]
        self.assertEqual(sched["sha256"], hashlib.sha256(CAR_TB.read_bytes()).hexdigest())
        self.assertEqual(sched["role"], "schedule")
        self.assertEqual(sched["coverage"]["season_min"], 2025)
        self.assertEqual(sched["schema_columns"], 10)
        self.assertIn("retrieved_date", sched)
        self.assertIn("source_url", sched)
        code = context["provenance"]["code"]
        self.assertEqual(code["engine_version"], "1.0.1")
        self.assertTrue(len(code["git_commit"]) == 40 or code["git_commit"] == "unknown")
        self.assertEqual(len(code["script_sha256"]), 64)
        roles = {i["role"] for i in context["provenance"]["inputs"]}
        self.assertIn("team_identity_eras", roles)
        self.assertEqual(context["data_cutoff"]["target_date_exclusive"], "2026-01-03")
        self.assertEqual(context["data_cutoff"]["last_game_included"], "2025-12-28")

    def test_market_columns_are_never_loaded(self):
        rows = [game(2024, 1, "2024-09-08", "13:00", "NE", "CIN", 16, 10)]
        with tempfile.TemporaryDirectory() as tmp:
            path = write_games(Path(tmp) / "g.csv", rows, {"spread_line": 3.5, "home_moneyline": -150, "total_line": 41})
            frame = engine.read_schedule(path)
        for col in ("spread_line", "home_moneyline", "total_line"):
            self.assertNotIn(col, frame.columns)

    def test_roster_input_hashed_and_legacy_codes_mapped(self):
        rows = [game(2005, 1, "2005-09-11", "13:00", "STL", "SF", 10, 20),
                game(2005, 3, "2005-09-25", "13:00", "STL", "SEA", None, None)]
        with tempfile.TemporaryDirectory() as tmp:
            games = write_games(Path(tmp) / "g.csv", rows)
            roster_dir = Path(tmp) / "r"
            roster_dir.mkdir()
            roster_file = roster_dir / "roster_weekly_2005.csv"
            pd.DataFrame([{"season": 2005, "week": 3, "team": "SL", "status": "ACT", "full_name": "Seahawks"},
                          {"season": 2005, "week": 3, "team": "ARZ", "status": "ACT", "full_name": "Someone"}]
                         ).to_csv(roster_file, index=False)
            context, findings = run_engine(games, "2005-09-25", "STL", "SEA", tmp, ["--rosters", str(roster_dir)])
            digest = hashlib.sha256(roster_file.read_bytes()).hexdigest()
        self.assertEqual(context["roster_unmapped_team_codes"], [])
        names = [m["player"] for m in context["player_name_matches"] if m["exact_systems"]]
        self.assertEqual(names, ["Seahawks"])
        self.assertEqual(context["player_name_matches"][0]["team"], "LA")
        roster_in = [i for i in context["provenance"]["inputs"] if i["role"] == "weekly_roster"][0]
        self.assertEqual(roster_in["sha256"], digest)


class LedgerTests(unittest.TestCase):
    def test_append_only_chain_and_stable_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "ledger.csv"
            c1, f1 = run_engine(CAR_TB, "2026-01-03", "CAR", "TB", tmp)
            first_bytes = ledger.read_bytes()
            ok, n1, head1, errors = engine.verify_ledger(ledger)
            self.assertTrue(ok, errors)
            self.assertEqual(n1, len(f1))
            c2, f2 = run_engine(CAR_TB, "2026-01-03", "CAR", "TB", tmp)
            second_bytes = ledger.read_bytes()
            self.assertTrue(second_bytes.startswith(first_bytes))
            ok, n2, head2, _ = engine.verify_ledger(ledger)
            self.assertTrue(ok)
            self.assertEqual(n2, n1 + len(f2))
            self.assertNotEqual(head1, head2)
            frame = pd.read_csv(ledger, dtype=str, keep_default_na=False)
            self.assertEqual(list(frame.columns), engine.LEDGER_FIELDS)
            self.assertEqual(set(frame.game_id), {"2025_18_CAR_TB"})
            self.assertEqual(set(frame.game_id_source), {"nflverse_schedule"})
            self.assertEqual(set(frame.split), {"holdout"})
            ids1 = list(frame.feature_id[:n1])
            ids2 = list(frame.feature_id[n1:])
            self.assertEqual(ids1, ids2)
            self.assertEqual(len(set(frame.run_id)), 2)
            self.assertTrue(all(frame.observed_at_utc[:n1] == c1["observed_at_utc"]))
            self.assertTrue((frame.feature_id != "").all() and (frame.family_id != "").all())

    def test_tampering_is_detected_and_blocks_append(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "ledger.csv"
            run_engine(CAR_TB, "2026-01-03", "CAR", "TB", tmp)
            text = ledger.read_text()
            ledger.write_text(text.replace("8-8-0", "9-7-0", 1))
            ok, _, _, errors = engine.verify_ledger(ledger)
            self.assertFalse(ok)
            self.assertTrue(any("row_hash mismatch" in e for e in errors))
            with self.assertRaises(engine.LedgerError):
                run_engine(CAR_TB, "2026-01-03", "CAR", "TB", tmp)

    def test_deleting_a_row_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "ledger.csv"
            run_engine(CAR_TB, "2026-01-03", "CAR", "TB", tmp)
            lines = ledger.read_text().splitlines()
            del lines[3]
            ledger.write_text("\n".join(lines) + "\n")
            self.assertFalse(engine.verify_ledger(ledger)[0])

    def test_dry_run_writes_no_ledger(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_engine(CAR_TB, "2026-01-03", "CAR", "TB", tmp, ledger=False)
            self.assertFalse((Path(tmp) / "ledger.csv").exists())

    def test_family_ids_group_cipher_variants(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, findings = run_engine(CAR_TB, "2026-01-03", "CAR", "TB", tmp)
        fam = {f["family_id"] for f in findings if f["feature_id"].startswith("gematria.nickname.") and f["team"] == "CAR"}
        self.assertEqual(fam, {"gematria.CAR.historical.nickname"})


class NoLeakageTests(unittest.TestCase):
    def test_target_and_later_results_do_not_change_findings(self):
        base = pd.read_csv(CAR_TB)
        altered = base.copy()
        mask = altered.gameday >= "2026-01-03"
        altered.loc[mask, "home_score"] = 99
        altered.loc[mask, "away_score"] = 0
        with tempfile.TemporaryDirectory() as tmp:
            alt_path = Path(tmp) / "alt.csv"
            altered.to_csv(alt_path, index=False)
            _, f_base = run_engine(CAR_TB, "2026-01-03", "CAR", "TB", Path(tmp) / "a", ledger=False)
            _, f_alt = run_engine(alt_path, "2026-01-03", "CAR", "TB", Path(tmp) / "b", ledger=False)
        self.assertEqual(f_base, f_alt)


class OutcomeAndSplitTests(unittest.TestCase):
    def test_three_outcomes(self):
        self.assertEqual(engine.game_outcome(27, 20), "HOME_WIN")
        self.assertEqual(engine.game_outcome(20, 27), "AWAY_WIN")
        self.assertEqual(engine.game_outcome(27, 27), "TIE")

    def test_win_pct_counts_tie_as_half(self):
        self.assertAlmostEqual(engine.win_pct({"wins": 2, "losses": 5, "ties": 1}), 2.5 / 8)
        self.assertAlmostEqual(engine.win_pct({"wins": 0, "losses": 0, "ties": 1}), 0.5)
        self.assertIsNone(engine.win_pct({"wins": 0, "losses": 0, "ties": 0}))

    def test_team_record_win_pct_field(self):
        frame = pd.DataFrame([{"away_team": "A", "home_team": "B", "away_score": 7, "home_score": 7}])
        self.assertEqual(engine.team_record(frame, "A")["win_pct"], 0.5)

    def test_split_boundaries(self):
        expected = {1999: "discovery", 2018: "discovery", 2019: "validation", 2022: "validation",
                    2023: "holdout", 2025: "holdout", 2026: "prospective", 2027: "prospective"}
        for season, name in expected.items():
            self.assertEqual(engine.split_for_season(season), name)


@unittest.skipUnless(os.environ.get("NFLVERSE_GAMES_CSV"), "set NFLVERSE_GAMES_CSV to run the real-data golden test")
class RealDataGoldenTest(unittest.TestCase):
    def test_was_nyg_2026_11_12(self):
        with tempfile.TemporaryDirectory() as tmp:
            context, findings = run_engine(os.environ["NFLVERSE_GAMES_CSV"], "2026-11-12", "WAS", "NYG", tmp)
        self.assertEqual(context["season_records_before_game"]["WAS"]["record"], "2-5-1")
        self.assertEqual(context["season_records_before_game"]["NYG"]["record"], "5-2-1")
        self.assertEqual(findings_by_id(findings, "calendar.days_remaining_in_year")[0]["value"], "49")
        self.assertEqual(findings_by_id(findings, "calendar.completed_months_since_last_thursday_win", "WAS")[0]["value"], "48")
        self.assertEqual(findings_by_id(findings, "streaks.days_since_last_loss", "NYG")[0]["value"], "25")
        self.assertEqual(context["data_scope"]["identity_coverage_gaps"], 0)


if __name__ == "__main__":
    unittest.main()
