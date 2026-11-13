"""v1.1 acceptance tests: batch runner, immutable partitions, manifest, registry, hypotheses ledger."""
import csv
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import hashchain
import narrative_batch as nb
import narrative_registry as reg
import nfl_script_narrative_engine as eng

CAR_TB = ROOT / "tests" / "fixtures" / "games_car_tb_2025.csv"
REAL_GAMES = os.environ.get("NFLVERSE_GAMES_CSV")
REAL_ROSTERS = os.environ.get("NFLVERSE_ROSTERS_DIR")
COLS = ["game_id", "season", "game_type", "week", "gameday", "gametime",
        "away_team", "away_score", "home_team", "home_score"]


def mini_league(scores=None):
    """Four teams, six weeks, one game per pair slot; deterministic scores unless overridden."""
    teams = ["NYG", "WAS", "DAL", "PHI"]
    rows, day = [], pd.Timestamp("2024-09-08")
    pairings = [("NYG", "WAS", "DAL", "PHI"), ("WAS", "DAL", "PHI", "NYG"), ("DAL", "NYG", "WAS", "PHI")]
    n = 0
    for week in range(1, 7):
        a1, h1, a2, h2 = pairings[(week - 1) % 3]
        for a, h in ((a1, h1), (a2, h2)):
            n += 1
            sa, sh = (17 + (n * 3) % 11, 20 + (n * 5) % 13)
            if scores and (week, a, h) in scores: sa, sh = scores[(week, a, h)]
            wd = day + pd.Timedelta(days=7 * (week - 1))
            rows.append({"game_id": f"2024_{week:02d}_{a}_{h}", "season": 2024, "game_type": "REG", "week": week,
                         "gameday": wd.strftime("%Y-%m-%d"), "gametime": "13:00", "away_team": a, "away_score": float(sa),
                         "home_team": h, "home_score": float(sh)})
    return pd.DataFrame(rows, columns=COLS)


def write_csv(path, frame):
    frame.to_csv(path, index=False)
    return path


class TableTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def tables(self, frame):
        return nb.build_tables(eng.read_schedule(write_csv(self.dir / "g.csv", frame)))

    def test_coverage_two_rows_per_completed_game_and_unscored_excluded(self):
        frame = mini_league()
        frame.loc[frame.index[-1], ["away_score", "home_score"]] = None  # future unplayed game
        raw = eng.read_schedule(write_csv(self.dir / "g.csv", frame))
        t = nb.build_tables(raw)
        cov = nb.coverage_report(raw, t)
        self.assertEqual(cov["completed_games"], len(frame) - 1)
        self.assertEqual(cov["team_game_rows"], 2 * (len(frame) - 1))
        self.assertEqual(cov["games_without_exactly_two_rows"], 0)
        self.assertEqual(cov["identity_coverage_gaps"], 0)
        self.assertEqual(cov["grid_flag_columns"], 504)

    def test_no_outcome_columns_in_any_table(self):
        for name, table in self.tables(mini_league()).items():
            self.assertTrue(nb.assert_no_outcome_columns(table), name)
            self.assertFalse(set(table.columns) & nb.FORBIDDEN_COLUMNS, name)
        with self.assertRaises(AssertionError):
            nb.assert_no_outcome_columns(pd.DataFrame({"home_score": [1]}))

    def test_no_leakage_perturbing_results_on_or_after_a_date_keeps_earlier_features_identical(self):
        base = mini_league()
        cut = "2024-10-06"  # week 5
        changed = base.copy()
        late = changed.gameday >= cut
        changed.loc[late, "away_score"] = changed.loc[late, "away_score"] + 13
        changed.loc[late, "home_score"] = 3.0
        a = self.tables(base)
        b = self.tables(changed)
        for name in ("team_game_features", "game_features", "grid_flags"):
            left, right = a[name], b[name]
            gid_dates = dict(zip(a["game_features"].game_id, a["game_features"].gameday))
            keep_ids = [g for g, d in gid_dates.items() if d <= cut]  # includes games ON the cut date (their pregame state)
            l = left[left.game_id.isin(keep_ids)].reset_index(drop=True)
            r = right[right.game_id.isin(keep_ids)].reset_index(drop=True)
            pd.testing.assert_frame_equal(l, r, check_dtype=True, obj=name)
        # and the perturbation really did change later pregame state
        later = lambda t: t["team_game_features"][t["team_game_features"].gameday > cut].q_season_wins.tolist()
        self.assertNotEqual(later(a), later(b))

    def test_same_day_results_are_excluded(self):
        # NYG plays week 1 and week 2 on different dates; a result on the same date must never count.
        t = self.tables(mini_league())["team_game_features"]
        w1 = t[(t.week == 1) & (t.franchise_id == "NYG")].iloc[0]
        self.assertEqual((w1.q_season_wins, w1.q_season_losses, w1.q_season_ties), (0, 0, 0))
        self.assertTrue(pd.isna(w1.q_days_since_last_win_rs))
        w2 = t[(t.week == 2) & (t.franchise_id == "NYG")].iloc[0]
        self.assertEqual(w2.q_season_wins + w2.q_season_losses + w2.q_season_ties, 1)

    def test_january_game_keeps_season_and_calendar_year_separate(self):
        raw = eng.read_schedule(CAR_TB)
        t = nb.build_tables(raw)["team_game_features"]
        row = t[(t.game_id == "2025_18_CAR_TB") & (t.franchise_id == "CAR")].iloc[0]
        self.assertEqual(int(row.season), 2025)
        self.assertEqual(row.gameday, "2026-01-03")
        self.assertEqual((int(row.q_season_wins), int(row.q_season_losses), int(row.q_season_ties)), (8, 8, 0))
        self.assertEqual(int(row.q_days_remaining), 362)  # December 31, 2026 minus January 3, 2026

    def test_f4_requires_mirrored_records_with_at_least_one_game_each(self):
        g = self.tables(mini_league())["game_features"]
        wk1 = g[g.week == 1]
        self.assertEqual(int(wk1.f4_mirrored_current_records.sum()), 0)  # 0-0-0 vs 0-0-0 is suppressed
        mirrored = g[g.f4_mirrored_current_records == 1]
        for r in mirrored.itertuples():
            self.assertEqual((r.away_season_wins, r.away_season_losses, r.away_season_ties),
                             (r.home_season_losses, r.home_season_wins, r.home_season_ties))
            self.assertGreaterEqual(r.away_season_wins + r.away_season_losses + r.away_season_ties, 1)

    def test_f5_previous_meeting_tie_uses_strictly_earlier_meeting(self):
        frame = mini_league()
        frame = pd.concat([frame, pd.DataFrame([
            {"game_id": "2025_01_WAS_NYG", "season": 2025, "game_type": "REG", "week": 1, "gameday": "2025-09-07",
             "gametime": "13:00", "away_team": "WAS", "away_score": 20.0, "home_team": "NYG", "home_score": 20.0},
            {"game_id": "2025_10_NYG_WAS", "season": 2025, "game_type": "REG", "week": 10, "gameday": "2025-11-09",
             "gametime": "13:00", "away_team": "NYG", "away_score": 10.0, "home_team": "WAS", "home_score": 17.0}])],
            ignore_index=True)
        g = self.tables(frame)["game_features"].set_index("game_id")
        self.assertEqual(int(g.loc["2025_10_NYG_WAS", "f5_prev_meeting_tied_rs"]), 1)
        self.assertEqual(int(g.loc["2025_01_WAS_NYG", "f5_prev_meeting_tied_rs"]), 0)  # the tie itself is not its own prior

    def test_grid_flags_exact_vs_root_are_separate_features(self):
        registry = reg.build_registry()
        row = {c: 0 for c in [f"nm_{b}_{k}_{f}" for b in nb.BASES for k in nb.KINDS for f in nb.FIELDS]}
        row.update({"nm_historical_city_pythagorean": 89, "nm_historical_city_pythagorean_root": 8,
                    "q_days_remaining": 89, "q_weekday_number": 7})
        for q in reg.QUANTITIES:
            row.setdefault("q_" + q, pd.NA)
        row["q_days_remaining"] = 89
        frame = pd.DataFrame([row]).astype({c: "float64" for c in row if c.startswith("nm_")})
        for q in [c for c in frame.columns if c.startswith("q_")]:
            frame[q] = pd.array(frame[q], dtype="Int64")
        flags = nb.grid_flag_frame(frame, registry)
        self.assertEqual(flags.shape[1], 504)
        self.assertEqual(int(flags["B__city__historical__pythagorean__days_remaining"].iloc[0]), 1)   # exact 89 == 89
        self.assertEqual(int(flags["B__city__historical__pythagorean_root__days_remaining"].iloc[0]), 1)  # root 8 == dr(89)=8
        self.assertEqual(int(flags["B__city__historical__ordinal__days_remaining"].iloc[0]), 0)
        self.assertEqual(int(flags["B__city__current__pythagorean__days_remaining"].iloc[0]), 0)
        self.assertEqual(int(flags["B__city__historical__pythagorean__days_since_last_win_rs"].iloc[0]), 0)  # missing quantity => 0

    def test_named_flags_f1_any_kind_exact_pythagorean(self):
        t = self.tables(mini_league())["team_game_features"]
        row = t.iloc[0]
        expected = int(any(row[f"nm_historical_{k}_pythagorean"] == row.q_days_remaining for k in nb.KINDS))
        self.assertEqual(int(row.f1_name_eq_days_remaining), expected)


class PartitionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.raw = eng.read_schedule(write_csv(self.dir / "g.csv", mini_league()))
        self.tables = nb.build_tables(self.raw)
        self.reg_sha = reg.registry_sha256()
        self.code = {"git_commit": "testcommit", "working_tree_dirty": False}

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, frame, derived, manifest, name="game_features", split="discovery"):
        return nb.write_partition(frame, name, split, derived, manifest, self.reg_sha, {"x": 1}, "t", self.code)

    def split_frame(self):
        g = self.tables["game_features"]
        return g[g.split == "holdout"].reset_index(drop=True) if (g.split == "holdout").any() else g.reset_index(drop=True)

    def test_determinism_two_builds_identical_hashes(self):
        again = nb.build_tables(self.raw)
        for name in self.tables:
            a, _ = nb.parquet_bytes(self.tables[name])
            b, _ = nb.parquet_bytes(again[name])
            self.assertEqual(a, b, name)
        d1, d2 = self.dir / "d1", self.dir / "d2"
        r1 = self.write(self.split_frame(), d1, d1 / "m.csv")
        r2 = self.write(self.split_frame(), d2, d2 / "m.csv")
        self.assertEqual(r1["sha256"], r2["sha256"])
        self.assertIn(r1["sha256"], r1["path"].name)  # content-addressed filename

    def test_immutability_rewrite_is_noop_and_never_overwrites(self):
        d, m = self.dir / "d", self.dir / "m.csv"
        first = self.write(self.split_frame(), d, m)
        self.assertEqual(first["status"], "created")
        mtime = first["path"].stat().st_mtime_ns
        again = self.write(self.split_frame(), d, m)
        self.assertEqual(again["status"], "exists_identical")
        self.assertEqual(again["manifest"], "already_recorded")
        self.assertEqual(first["path"].stat().st_mtime_ns, mtime)
        self.assertEqual(len(hashchain.read_rows(m)), 1)

    def test_corrected_content_creates_new_versioned_partition_with_supersedes_link(self):
        d, m = self.dir / "d", self.dir / "m.csv"
        a = self.write(self.split_frame(), d, m)
        changed = self.split_frame().copy()
        changed.loc[0, "week"] = 99
        b = self.write(changed, d, m)
        self.assertNotEqual(a["sha256"], b["sha256"])
        self.assertTrue(a["path"].exists() and b["path"].exists())  # old version kept
        rows = hashchain.read_rows(m)
        self.assertEqual(rows[1]["supersedes_sha256"], a["sha256"])
        ok, n, _, errors = nb.verify_manifest(m, d)
        self.assertTrue(ok, errors)

    def test_partition_tampering_is_detected(self):
        d, m = self.dir / "d", self.dir / "m.csv"
        res = self.write(self.split_frame(), d, m)
        with open(res["path"], "ab") as handle:
            handle.write(b"x")
        ok, _, _, errors = nb.verify_manifest(m, d)
        self.assertFalse(ok)
        self.assertTrue(any("altered" in e for e in errors))
        with self.assertRaises(nb.ImmutabilityError):
            self.write(self.split_frame(), d, m)  # existing file no longer matches its content-addressed name

    def test_partition_deletion_is_detected(self):
        d, m = self.dir / "d", self.dir / "m.csv"
        res = self.write(self.split_frame(), d, m)
        res["path"].unlink()
        ok, _, _, errors = nb.verify_manifest(m, d)
        self.assertFalse(ok)
        self.assertTrue(any("missing" in e for e in errors))

    def test_manifest_row_edit_delete_and_reorder_break_the_chain(self):
        d, m = self.dir / "d", self.dir / "m.csv"
        self.write(self.split_frame(), d, m)
        self.write(self.tables["team_game_features"].query("split == 'holdout'").reset_index(drop=True)
                   if (self.tables["team_game_features"].split == "holdout").any() else self.tables["team_game_features"],
                   d, m, name="team_game_features")
        ok, n, _, _ = nb.verify_manifest(m, d)
        self.assertTrue(ok); self.assertEqual(n, 2)
        original = m.read_text()
        lines = original.splitlines()
        m.write_text(original.replace("testcommit", "forgedcommit", 1))
        self.assertFalse(nb.verify_manifest(m, d)[0])
        m.write_text("\n".join([lines[0], lines[2], lines[1]]) + "\n")  # reorder
        self.assertFalse(nb.verify_manifest(m, d)[0])
        m.write_text("\n".join([lines[0], lines[2]]) + "\n")  # delete first row
        self.assertFalse(nb.verify_manifest(m, d)[0])
        m.write_text(original)
        self.assertTrue(nb.verify_manifest(m, d)[0])

    def test_append_refuses_to_extend_a_broken_chain(self):
        d, m = self.dir / "d", self.dir / "m.csv"
        self.write(self.split_frame(), d, m)
        m.write_text(m.read_text().replace("testcommit", "forged", 1))
        other = self.split_frame().copy(); other.loc[0, "week"] = 77
        with self.assertRaises(hashchain.ChainError):
            self.write(other, d, m)

    def test_manifest_records_required_provenance(self):
        d, m = self.dir / "d", self.dir / "m.csv"
        self.write(self.split_frame(), d, m)
        row = hashchain.read_rows(m)[0]
        for field in ("sha256", "schema_version", "schema_sha256", "rows", "registry_sha256", "code_commit", "inputs_json"):
            self.assertTrue(row[field] != "", field)
        self.assertEqual(row["registry_sha256"], self.reg_sha)


class RosterProxyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        frame = mini_league()
        frame["season"] = 2010
        frame["game_id"] = frame.game_id.str.replace("2024", "2010")
        frame["gameday"] = (pd.to_datetime(frame.gameday) - pd.DateOffset(years=14)).dt.strftime("%Y-%m-%d")
        self.raw = eng.read_schedule(write_csv(self.dir / "g.csv", frame))
        self.team = nb.build_tables(self.raw)["team_game_features"]
        rows = []
        for week in range(1, 7):
            for team in ("NYG", "WAS", "DAL", "PHI"):
                rows.append({"season": 2010, "team": team, "status": "ACT", "full_name": f"Filler{week}{team}", "gsis_id": f"00-{week}{team}",
                             "week": week, "game_type": "REG"})
        # target nickname for WAS opponents in 2010 is REDSKINS; plant matching player names on NYG and an inactive one
        rows += [{"season": 2010, "team": "NYG", "status": "ACT", "full_name": "Redskins", "gsis_id": "00-MATCH", "week": 3, "game_type": "REG"},
                 {"season": 2010, "team": "NYG", "status": "RES", "full_name": "Redskins", "gsis_id": "00-INACT", "week": 3, "game_type": "REG"},
                 {"season": 2010, "team": "NYG", "status": "ACT", "full_name": "Redskins", "gsis_id": "00-POST", "week": 3, "game_type": "CON"}]
        self.rost = self.dir / "rosters"; self.rost.mkdir()
        pd.DataFrame(rows).to_csv(self.rost / "roster_weekly_2010.csv", index=False)

    def tearDown(self):
        self.tmp.cleanup()

    def test_previous_week_proxy_labels_staleness_and_week_one(self):
        out = nb.build_player_tables(self.team, self.rost, "2026-11-12")
        prev, same, cov = (out["roster_candidates_previous_week"], out["roster_candidates_same_week_sensitivity"], out["roster_coverage"])
        # NYG plays WAS in week 3? find NYG-vs-WAS games and check the roster used the PRIOR week
        self.assertTrue((prev.roster_label == "PREVIOUS_WEEK_ROSTER").all())
        self.assertTrue((same.roster_label == "SAME_WEEK_SNAPSHOT_TIMING_UNVERIFIED").all())
        self.assertTrue((prev.staleness_weeks >= 1).all())
        self.assertTrue((same.staleness_weeks == 0).all())
        self.assertTrue((prev.retrieval_date == "2026-11-12").all())
        self.assertTrue(prev.roster_source_sha256.str.len().eq(64).all())
        # inactive and non-REG roster rows never become candidates
        self.assertFalse(prev.gsis_id.isin(["00-INACT", "00-POST"]).any())
        self.assertFalse(same.gsis_id.isin(["00-INACT", "00-POST"]).any())
        # week 1 has no prior-week snapshot and says so explicitly
        wk1 = cov[(cov.week == 1) & (cov.roster_label == "PREVIOUS_WEEK_ROSTER")]
        self.assertTrue((wk1.snapshot_status == "NO_PRIOR_WEEK_SNAPSHOT").all())
        ok = cov[cov.snapshot_status == "OK"]
        self.assertTrue((ok.snapshot_week == ok.week - ok.staleness_weeks).all())
        self.assertFalse(prev.drop_duplicates("game_id").game_id.isin(wk1.game_id).all())

    def test_match_available_only_when_snapshot_exists_before_the_game(self):
        out = nb.build_player_tables(self.team, self.rost, "2026-11-12")
        prev, same = out["roster_candidates_previous_week"], out["roster_candidates_same_week_sensitivity"]
        planted_prev = prev[prev.gsis_id == "00-MATCH"]
        planted_same = same[same.gsis_id == "00-MATCH"]
        # the planted week-3 snapshot can serve week >= 4 games as previous-week proxy, and week-3 games as same-week only
        self.assertTrue((planted_prev.week >= 4).all())
        self.assertTrue((planted_same.week == 3).all())

    def test_player_tables_contain_no_outcome_columns(self):
        for name, table in nb.build_player_tables(self.team, self.rost, "2026-11-12").items():
            self.assertTrue(nb.assert_no_outcome_columns(table), name)


class RegistryTests(unittest.TestCase):
    def test_registry_is_reproducible_and_matches_committed_files(self):
        a, b = reg.build_registry(), reg.build_registry()
        self.assertEqual(reg.registry_sha256(a), reg.registry_sha256(b))
        self.assertEqual(reg.REGISTRY_CSV.read_bytes(), reg.registry_csv_bytes(a))
        meta = json.loads(reg.REGISTRY_META.read_text())
        self.assertEqual(meta["sha256"], reg.registry_sha256(a))
        self.assertTrue(meta["freeze_status"].startswith("NOT_FROZEN"))
        self.assertEqual(a.feature_id.is_unique, True)

    def test_f4_is_the_only_confirmatory_feature_with_full_spec(self):
        frame = reg.build_registry()
        conf = frame[frame.status == "CONFIRMATORY"]
        self.assertEqual(list(conf.feature_id), ["F4_MIRRORED_CURRENT_RECORDS"])
        self.assertEqual(list(frame[frame.tier == "A"].feature_id), ["F4_MIRRORED_CURRENT_RECORDS"])
        spec = json.loads(reg.F4_SPEC.read_text())
        for key in ("operational_definition", "unit", "denominator", "expected_prevalence", "hypothesis", "direction",
                    "primary_outcome", "tie_treatment", "comparison_baseline", "minimum_qualifying_n",
                    "multiplicity_correction", "promotion_criteria", "exposure", "stopping_rule", "testing_sequence"):
            self.assertIn(key, spec)
        self.assertEqual(spec["primary_outcome"], ["HOME_WIN", "AWAY_WIN", "TIE"])
        self.assertTrue(spec["stopping_rule"].startswith("A2:") and "188" in spec["stopping_rule"]); self.assertEqual(spec["registry_status"], "NOT_FROZEN")

    def test_approved_statuses_and_exposure_labels(self):
        f = reg.build_registry().set_index("feature_id")
        for fid in f.index[f.family_id.isin(["F1", "F2", "F3", "F5", "F6", "F7"])]:
            self.assertEqual(f.loc[fid, "status"], "DESCRIPTIVE_ONLY", fid)
        for fid in f.index[f.family_id.isin(["F8", "F9", "F10"])]:
            self.assertTrue(f.loc[fid, "status"].startswith("DESCRIPTIVE_ONLY"), fid)
            self.assertEqual(f.loc[fid, "exposure_holdout"], reg.NONE_EST)
        for fid in f.index[f.family_id.isin(["F1", "F2", "F3", "F4", "F5"])]:
            self.assertEqual((f.loc[fid, "exposure_discovery"], f.loc[fid, "exposure_validation"], f.loc[fid, "exposure_holdout"]),
                             (reg.DISCOVERY, reg.AWAITING, reg.PREV), fid)
        for fid in f.index[f.family_id.isin(["F6", "F7"])]:
            self.assertEqual({f.loc[fid, "exposure_discovery"], f.loc[fid, "exposure_validation"], f.loc[fid, "exposure_holdout"]},
                             {reg.PREV}, fid)
            self.assertEqual(f.loc[fid, "requires"], "OUTCOME_SCORE")
        self.assertTrue((f.exposure_prospective == reg.PROSPECTIVE).all())

    def test_grid_size_and_tnf_blocking(self):
        frame = reg.build_registry()
        grid = frame[(frame.tier == "B") & (frame.status == "EXPLORATORY")]
        self.assertEqual(len(grid), 3 * 2 * 6 * 14)
        self.assertEqual(len(grid), 504)
        self.assertEqual(set(frame[frame.status == "BLOCKED_TNF"].feature_id),
                         {"TNF_RECORD_VERIFIED", "TNF_COMPLETED_MONTHS_SINCE_LAST_TNF_WIN", "TNF_DAYS_SINCE_LAST_TNF_WIN"})
        self.assertEqual(reg.registry_meta(frame)["exploratory_grid_size"], 504)
        # exact and root matches are different features; cipher variants of one string share a family
        a = grid[grid.feature_id == "B__city__historical__pythagorean__days_remaining"].iloc[0]
        b = grid[grid.feature_id == "B__city__historical__pythagorean_root__days_remaining"].iloc[0]
        self.assertEqual((a.match_type, b.match_type), ("exact", "root"))
        self.assertEqual(a.family_id, b.family_id)

    def test_hypotheses_ledger_register_is_idempotent_and_tamper_evident(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "h.csv"
            frame = reg.build_registry()
            first = reg.register_hypotheses(frame, ledger, "c0ffee")
            self.assertEqual(first["appended"], 14)
            second = reg.register_hypotheses(frame, ledger, "c0ffee")
            self.assertEqual(second["appended"], 0)
            ok, n, _, errors = hashchain.verify(ledger, reg.LEDGER_FIELDS, "hypothesis_row")
            self.assertTrue(ok, errors); self.assertEqual(n, 14)
            ledger.write_text(ledger.read_text().replace("NOT_TESTED", "SIGNIFICANT", 1))
            self.assertFalse(hashchain.verify(ledger, reg.LEDGER_FIELDS, "hypothesis_row")[0])

    def test_committed_hypotheses_ledger_verifies(self):
        ok, n, _, errors = hashchain.verify(reg.HYPOTHESES_LEDGER, reg.LEDGER_FIELDS, "hypothesis_row")
        self.assertTrue(ok, errors)
        self.assertGreaterEqual(n, 14)


@unittest.skipUnless(REAL_GAMES and Path(REAL_GAMES).exists(), "set NFLVERSE_GAMES_CSV to run real-data acceptance tests")
class RealDataAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = eng.read_schedule(REAL_GAMES)
        cls.tables = nb.build_tables(cls.raw)

    def test_coverage_reconciles_to_schedule(self):
        cov = nb.coverage_report(self.raw, self.tables)
        self.assertEqual(cov["team_game_rows"], 2 * cov["completed_games"])
        self.assertEqual(cov["games_without_exactly_two_rows"], 0)
        self.assertEqual(cov["games_missing_from_team_table"], 0)
        self.assertEqual(cov["identity_coverage_gaps"], 0)

    def test_split_counts_match_reconciliation(self):
        g = self.tables["game_features"]
        reg_games = g[g.game_type == "REG"]
        counts = reg_games.groupby("split").size().to_dict()
        self.assertEqual(counts["discovery"], 5096)
        self.assertEqual(counts["validation"], 1055)
        self.assertEqual(counts["holdout"], 816)

    def test_f4_prevalence_matches_approved_outcome_blind_counts(self):
        g = self.tables["game_features"]
        counts = g[g.game_type == "REG"].groupby("split").f4_mirrored_current_records.sum().to_dict()
        self.assertEqual((counts["discovery"], counts["validation"], counts["holdout"]), (766, 154, 117))

    def test_parity_with_v101_engine_200_random_plus_rare_games(self):
        out = nb.parity_check(REAL_GAMES, 200)
        self.assertEqual(out["mismatches"], 0, out["first_mismatches"])
        self.assertGreaterEqual(out["games_sampled"], 200)


if __name__ == "__main__":
    unittest.main()
