#!/usr/bin/env python3
"""v1.1 batch discovery runner: pregame feature tables as immutable Parquet partitions.

What this does
- Builds, for every completed game 1999+, one row per team (team_game_features), one row per game
  (game_features), the 504-feature Tier B flag grid (grid_flags), and PREVIOUS_WEEK_ROSTER player
  candidates with coverage rows.
- Every value is a PREGAME value: only games with gameday strictly before the target game's date are used.
- NO outcome columns (scores, winners, results) are written. Outcome-joined analysis is out of scope for v1.1.
- Partitions are content-addressed (SHA-256 in the filename), never overwritten, and recorded in an
  append-only hash-chained manifest (research_ledger/partition_manifest.csv).
"""
from __future__ import annotations
import argparse, hashlib, io, json, random, sys
from datetime import date, datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hashchain
import nfl_script_narrative_engine as eng
import narrative_registry as reg

REPO_ROOT = eng.REPO_ROOT
SCHEMA_VERSION = "1.1.0"
DEFAULT_DERIVED = REPO_ROOT / "derived" / "v1.1"
DEFAULT_MANIFEST = REPO_ROOT / "research_ledger" / "partition_manifest.csv"
SPLIT_NAMES = [s[0] for s in eng.SPLITS]
FIELDS = reg.CIPHER_FIELDS
EXACT = reg.EXACT_FIELDS
KINDS = reg.STRING_KINDS
BASES = reg.BASES
FORBIDDEN_COLUMNS = {"away_score", "home_score", "score", "own_score", "opp_score", "result", "outcome", "winner",
                     "total", "game_total", "margin", "spread", "moneyline", "team_win", "home_win", "away_win"}

MANIFEST_FIELDS = ["manifest_row", "created_utc", "partition_name", "split", "relative_path", "sha256", "bytes", "rows",
                   "columns", "schema_version", "schema_sha256", "registry_sha256", "code_commit", "code_dirty",
                   "inputs_json", "supersedes_sha256", "notes", "prev_hash", "row_hash"]


class ImmutabilityError(Exception):
    pass


# --------------------------------------------------------------------------- pregame state
def _completed(raw):
    done = raw[raw.away_score.notna() & raw.home_score.notna()].copy()
    return done.sort_values(["gameday", "game_id"]).reset_index(drop=True)


def _long(done):
    rows = []
    for side, team, opp, own, other in (("away", "away_team", "home_team", "away_score", "home_score"),
                                         ("home", "home_team", "away_team", "home_score", "away_score")):
        part = done[["game_id", "season", "week", "gameday", "game_type", "weekday", "slot"]].copy()
        part["side"], part["franchise_id"], part["opponent_id"] = side, done[team].values, done[opp].values
        part["_res"] = np.sign(done[own].values - done[other].values).astype(int)  # internal only, never written
        rows.append(part)
    long = pd.concat(rows, ignore_index=True)
    return long.sort_values(["franchise_id", "gameday", "game_id"]).reset_index(drop=True)


def _pregame_team_state(long):
    """Cumulative pregame state per team-game using date < game date (strict, date-level)."""
    out = []
    for fid, g in long.groupby("franchise_id", sort=False):
        dates = np.array([np.datetime64(d, "D") for d in g.gameday])
        res, season = g._res.values, g.season.values.astype(int)
        reg = (g.game_type.values == "REG")
        thu = reg & (g.weekday.values == "Thursday")
        recs = []
        for i in range(len(g)):
            earlier = dates < dates[i]
            def last(mask):
                m = earlier & mask
                return dates[m].max() if m.any() else None
            sm = earlier & reg & (season == season[i])
            rec = {"q_season_wins": int((res[sm] == 1).sum()), "q_season_losses": int((res[sm] == -1).sum()),
                   "q_season_ties": int((res[sm] == 0).sum())}
            today = g.gameday.values[i]
            for name, mask in (("days_since_last_win_rs", reg & (res == 1)), ("days_since_last_loss_rs", reg & (res == -1)),
                               ("days_since_last_win_all", res == 1), ("days_since_last_loss_all", res == -1)):
                d = last(mask)
                rec["q_" + name] = None if d is None else int((dates[i] - d).astype("timedelta64[D]").astype(int))
            d = last(thu & (res == 1))
            if d is None:
                rec["q_days_since_last_thursday_win"] = rec["q_completed_months_since_last_thursday_win"] = None
            else:
                start = date.fromisoformat(str(d))
                em = eng.elapsed_months(start, today)
                rec["q_days_since_last_thursday_win"] = em["days"]
                rec["q_completed_months_since_last_thursday_win"] = em["completed_months"]
            recs.append(rec)
        out.append(pd.DataFrame(recs, index=g.index))
    return pd.concat(out).sort_index()


def _identity_columns(frame):
    cols = {}
    cache = {}
    for fid, season in set(zip(frame.franchise_id, frame.season.astype(int))):
        hist = eng.identity_for(fid, season)
        cur = eng.current_identity(fid)
        cache[(fid, season)] = {"historical": hist, "current": cur}
    rows = []
    for fid, season in zip(frame.franchise_id, frame.season.astype(int)):
        ids = cache[(fid, season)]
        row = {"hist_city": ids["historical"]["city"], "hist_nickname": ids["historical"]["nickname"],
               "hist_display_name": ids["historical"]["display_name"], "cur_city": ids["current"]["city"],
               "cur_nickname": ids["current"]["nickname"], "cur_display_name": ids["current"]["display_name"]}
        for basis in BASES:
            strings = eng.identity_strings(ids[basis])
            for kind in KINDS:
                values = eng.ciphers(strings[kind])
                for field in FIELDS:
                    row[f"nm_{basis}_{kind}_{field}"] = values[field]
        rows.append(row)
    return pd.DataFrame(rows, index=frame.index)


def _date_quantities(frame):
    days = [date.fromisoformat(str(d)) for d in frame.gameday]
    q = pd.DataFrame(index=frame.index)
    q["q_days_remaining"] = [(date(d.year, 12, 31) - d).days for d in days]
    sums = [sum(int(c) for c in d.strftime("%Y%m%d")) for d in days]
    q["q_date_digit_sum"] = sums
    q["q_date_digit_root"] = [eng.digital_root(s) for s in sums]
    q["q_weekday_number"] = [d.isoweekday() for d in days]
    q["q_schedule_week"] = frame.week.astype(int).values
    return q


def _qty_array(frame, qty):
    return pd.to_numeric(frame["q_" + qty], errors="coerce").to_numpy(dtype="float64")


def _digital_root_array(arr):
    out = np.zeros(len(arr), dtype="float64")
    valid = ~np.isnan(arr)
    v = np.abs(arr[valid]).astype(int)
    out[valid] = np.where(v == 0, 0, 1 + (v - 1) % 9)
    out[~valid] = np.nan
    return out


def grid_flag_frame(team_games, registry):
    """504 uint8 flags: exact => name value == quantity; root => root field == digital_root(quantity). Missing quantity => 0."""
    grid = registry[registry.tier == "B"]
    grid = grid[grid.status == "EXPLORATORY"]
    data = {}
    for r in grid.itertuples():
        name = team_games[f"nm_{r.name_basis}_{r.string_source}_{r.cipher_field}"].to_numpy(dtype="float64")
        qty = _qty_array(team_games, r.quantity)
        target = qty if r.match_type == "exact" else _digital_root_array(qty)
        with np.errstate(invalid="ignore"):
            flag = (name == target) & ~np.isnan(target)
        data[r.feature_id] = flag.astype("uint8")
    return pd.DataFrame(data, index=team_games.index)


def named_flags(team_games):
    """F1-F3 per team-game: any of city/nickname/full exact Pythagorean (historical) equals the quantity."""
    cols = [f"nm_historical_{k}_pythagorean" for k in KINDS]
    names = team_games[cols].to_numpy(dtype="float64")
    out = {}
    for fid, qty in (("f1_name_eq_days_remaining", "days_remaining"),
                     ("f2_name_eq_days_since_loss_rs", "days_since_last_loss_rs"),
                     ("f2_name_eq_days_since_loss_all", "days_since_last_loss_all"),
                     ("f3_name_eq_days_since_win_rs", "days_since_last_win_rs"),
                     ("f3_name_eq_days_since_win_all", "days_since_last_win_all")):
        q = _qty_array(team_games, qty)[:, None]
        with np.errstate(invalid="ignore"):
            hit = (names == q).any(axis=1) & ~np.isnan(q[:, 0])
        out[fid] = hit.astype("uint8")
    return pd.DataFrame(out, index=team_games.index)


def build_tables(raw):
    """Return {'team_game_features','game_features','grid_flags'} DataFrames for all completed games."""
    done = _completed(raw)
    long = _long(done)
    state = _pregame_team_state(long)
    team = pd.concat([long.drop(columns=["_res"]), state], axis=1)
    team = pd.concat([team, _date_quantities(team), _identity_columns(team)], axis=1)
    team["split"] = [eng.split_for_season(int(s)) for s in team.season]
    team["gameday"] = team.gameday.astype(str)
    team = team.sort_values(["gameday", "game_id", "side"]).reset_index(drop=True)
    for col in [c for c in team.columns if c.startswith("q_")]:
        team[col] = pd.array(team[col], dtype="Int64")
    team = pd.concat([team, named_flags(team)], axis=1)
    registry = reg.build_registry()
    grid = grid_flag_frame(team, registry)
    grid.insert(0, "side", team.side.values)
    grid.insert(0, "franchise_id", team.franchise_id.values)
    grid.insert(0, "game_id", team.game_id.values)
    grid.insert(0, "split", team.split.values)

    # game-level: F4 mirrored records (REG only) and F5 previous meeting tied
    away = team[team.side == "away"].set_index("game_id")
    home = team[team.side == "home"].set_index("game_id")
    games = done[["game_id", "season", "week", "gameday", "game_type"]].copy()
    games["gameday"] = games.gameday.astype(str)
    games["split"] = [eng.split_for_season(int(s)) for s in games.season]
    games["away_id"] = games.game_id.map(away.franchise_id)
    games["home_id"] = games.game_id.map(home.franchise_id)
    for side, frame in (("away", away), ("home", home)):
        for part in ("wins", "losses", "ties"):
            games[f"{side}_season_{part}"] = games.game_id.map(frame["q_season_" + part]).astype("Int64")
    games["f4_eligible"] = (games.game_type == "REG").astype("uint8")
    aw, al, at = (games.away_season_wins, games.away_season_losses, games.away_season_ties)
    hw, hl, ht = (games.home_season_wins, games.home_season_losses, games.home_season_ties)
    mirrored = ((aw == hl) & (al == hw) & (at == ht) & ((aw + al + at) >= 1) & ((hw + hl + ht) >= 1))
    games["f4_mirrored_current_records"] = (mirrored.fillna(False) & (games.f4_eligible == 1)).astype("uint8")

    meetings, prev_rs, prev_all = {}, {}, {}
    # (previous meeting by franchise pair, strictly earlier date; same-day games added only after the day)
    pending_rs = []
    ordered = done.sort_values(["gameday", "game_id"])
    for day, chunk in ordered.groupby("gameday", sort=True):
        batch = []
        for r in chunk.itertuples():
            pair = frozenset((r.away_team, r.home_team))
            history = meetings.get(pair, [])
            hist_rs = [m for m in history if m[1] == "REG"]
            prev_all[r.game_id] = history[-1] if history else None
            prev_rs[r.game_id] = hist_rs[-1] if hist_rs else None
            batch.append((pair, (str(r.gameday), r.game_type, bool(r.away_score == r.home_score))))
        for pair, entry in batch:
            meetings.setdefault(pair, []).append(entry)
    games["prev_meeting_date_rs"] = games.game_id.map(lambda g: prev_rs[g][0] if prev_rs[g] else None)
    games["prev_meeting_date_all"] = games.game_id.map(lambda g: prev_all[g][0] if prev_all[g] else None)
    games["f5_prev_meeting_tied_rs"] = games.game_id.map(lambda g: int(bool(prev_rs[g][2])) if prev_rs[g] else 0).astype("uint8")
    games["f5_prev_meeting_tied_all"] = games.game_id.map(lambda g: int(bool(prev_all[g][2])) if prev_all[g] else 0).astype("uint8")
    games = games.sort_values(["gameday", "game_id"]).reset_index(drop=True)
    assert_no_outcome_columns(team), assert_no_outcome_columns(games), assert_no_outcome_columns(grid)
    return {"team_game_features": team, "game_features": games, "grid_flags": grid}


def assert_no_outcome_columns(frame):
    bad = sorted(c for c in frame.columns if c.lower() in FORBIDDEN_COLUMNS)
    if bad:
        raise AssertionError(f"outcome column(s) present in a feature partition: {bad}")
    return True


# ----------------------------------------------------------------------- roster candidates
def _roster_files(roster_dir):
    return {int(p.stem.split("_")[-1]): p for p in Path(roster_dir).glob("roster_weekly_*.csv")}


def build_player_tables(team_games, roster_dir, retrieved):
    """PREVIOUS_WEEK_ROSTER candidates (primary) and same-week sensitivity candidates for REG games.

    Rows are name-value matches between a player's full name and the OPPONENT's nickname. Never described as
    game-day active status. No outcomes are joined.
    """
    files = _roster_files(roster_dir)
    mapping = eng.code_to_franchise()
    regs = team_games[(team_games.game_type == "REG") & (team_games.season >= 2002)]
    primary, sensitivity, coverage = [], [], []
    for season, games in regs.groupby("season"):
        path = files.get(int(season))
        if path is None:
            for r in games.itertuples():
                coverage.append(_cov_row(r, "PREVIOUS_WEEK_ROSTER", None, None, 0, "NO_ROSTER_FILE", None, retrieved))
            continue
        roster = pd.read_csv(path, low_memory=False)
        sha = eng.sha256_file(path)
        roster["week"] = pd.to_numeric(roster.week, errors="coerce")
        roster = roster[roster.game_type.astype(str).eq("REG") & roster.status.astype(str).str.upper().eq("ACT")].copy()
        roster["team_fid"] = roster.team.map(lambda c: mapping.get(eng.normalize_code(c)) if pd.notna(c) else None)
        roster = roster[roster.full_name.notna() & roster.team_fid.notna()]
        cache = {}
        for r in games.itertuples():
            weeks = sorted(roster.loc[roster.team_fid == r.franchise_id, "week"].dropna().astype(int).unique())
            prior = [w for w in weeks if w < int(r.week)]
            snap = prior[-1] if prior else None
            same = int(r.week) if int(r.week) in weeks else None
            for label, snapshot, sink in (("PREVIOUS_WEEK_ROSTER", snap, primary),
                                          ("SAME_WEEK_SNAPSHOT_TIMING_UNVERIFIED", same, sensitivity)):
                if snapshot is None:
                    if label == "PREVIOUS_WEEK_ROSTER":
                        coverage.append(_cov_row(r, label, None, None, 0, "NO_PRIOR_WEEK_SNAPSHOT", path.name, retrieved, sha))
                    continue
                key = (r.franchise_id, snapshot)
                if key not in cache:
                    cache[key] = roster[(roster.team_fid == r.franchise_id) & (roster.week == snapshot)][["gsis_id", "full_name"]]
                players = cache[key]
                opp = eng.identity_for(r.opponent_id, int(r.season))
                opp_cur = eng.current_identity(r.opponent_id)
                nick_bases = [("historical", opp["nickname"])]
                if opp_cur["nickname"] != opp["nickname"]:
                    nick_bases.append(("current", opp_cur["nickname"]))
                if label == "PREVIOUS_WEEK_ROSTER":
                    coverage.append(_cov_row(r, label, snapshot, int(r.week) - snapshot, len(players), "OK", path.name, retrieved, sha))
                for basis, nick in nick_bases:
                    target = eng.ciphers(nick)
                    for p in players.itertuples():
                        cv = eng.ciphers(p.full_name)
                        exact = [f for f in EXACT if cv[f] == target[f]]
                        roots = [f for f in ("ordinal_root", "reverse_root", "pythagorean_root") if cv[f] == target[f]]
                        if exact or roots:
                            sink.append({"game_id": r.game_id, "season": int(r.season), "week": int(r.week), "split": r.split,
                                         "franchise_id": r.franchise_id, "opponent_id": r.opponent_id,
                                         "gsis_id": p.gsis_id if pd.notna(p.gsis_id) else "", "player_name": p.full_name,
                                         "opponent_nickname_basis": basis, "opponent_nickname": nick.upper(),
                                         "exact_systems": ",".join(exact), "root_systems": ",".join(roots),
                                         "roster_label": label, "snapshot_week": snapshot,
                                         "staleness_weeks": int(r.week) - snapshot, "roster_source_file": path.name,
                                         "roster_source_sha256": sha, "retrieval_date": retrieved})
    cols = ["game_id", "season", "week", "split", "franchise_id", "opponent_id", "gsis_id", "player_name",
            "opponent_nickname_basis", "opponent_nickname", "exact_systems", "root_systems", "roster_label",
            "snapshot_week", "staleness_weeks", "roster_source_file", "roster_source_sha256", "retrieval_date"]
    p1 = pd.DataFrame(primary, columns=cols)
    p2 = pd.DataFrame(sensitivity, columns=cols)
    cov = pd.DataFrame(coverage, columns=["game_id", "season", "week", "split", "franchise_id", "roster_label",
                                          "snapshot_week", "staleness_weeks", "active_players", "snapshot_status",
                                          "roster_source_file", "roster_source_sha256", "retrieval_date"])
    for f in (p1, p2, cov):
        for c in ("snapshot_week", "staleness_weeks"):
            if c in f: f[c] = pd.array(f[c], dtype="Int64")
    for f in (p1, p2):
        f.sort_values(["game_id", "franchise_id", "opponent_nickname_basis", "gsis_id", "player_name"], inplace=True)
        f.reset_index(drop=True, inplace=True)
    cov = cov.sort_values(["game_id", "franchise_id"]).reset_index(drop=True)
    return {"roster_candidates_previous_week": p1, "roster_candidates_same_week_sensitivity": p2, "roster_coverage": cov}


def _cov_row(r, label, snapshot, staleness, n, status, fname, retrieved, sha=None):
    return {"game_id": r.game_id, "season": int(r.season), "week": int(r.week), "split": r.split,
            "franchise_id": r.franchise_id, "roster_label": label, "snapshot_week": snapshot, "staleness_weeks": staleness,
            "active_players": n, "snapshot_status": status, "roster_source_file": fname or "",
            "roster_source_sha256": sha or "", "retrieval_date": retrieved}


# --------------------------------------------------------------------------- partitions
def schema_hash(table):
    return hashlib.sha256("\n".join(f"{f.name}:{f.type}" for f in table.schema).encode()).hexdigest()


def parquet_bytes(frame):
    table = pa.Table.from_pandas(frame, preserve_index=False).replace_schema_metadata(None)
    buf = io.BytesIO()
    pq.write_table(table, buf, compression="zstd", use_dictionary=True, write_statistics=True)
    return buf.getvalue(), table


def write_partition(frame, name, split, derived_dir, manifest_path, registry_sha, inputs, notes="", code=None):
    """Write an immutable content-addressed partition and append its manifest row. Never overwrites."""
    derived_dir = Path(derived_dir)
    data, table = parquet_bytes(frame)
    sha = hashlib.sha256(data).hexdigest()
    rel = Path(name) / f"{name}__{split}__{sha}.parquet"
    path = derived_dir / rel
    if path.exists():
        if eng.sha256_file(path) != sha:
            raise ImmutabilityError(f"existing partition content differs from its name: {path}")
        status = "exists_identical"
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "xb") as handle:  # 'x' refuses to overwrite
            handle.write(data)
        status = "created"
    rows = hashchain.read_rows(manifest_path)
    same = [r for r in rows if r["partition_name"] == name and r["split"] == split]
    if any(r["sha256"] == sha for r in same):
        return {"status": status, "path": path, "sha256": sha, "manifest": "already_recorded"}
    code = code or eng.code_provenance()
    row = {"created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "partition_name": name, "split": split,
           "relative_path": rel.as_posix(), "sha256": sha, "bytes": len(data), "rows": len(frame), "columns": len(frame.columns),
           "schema_version": SCHEMA_VERSION, "schema_sha256": schema_hash(table), "registry_sha256": registry_sha,
           "code_commit": code["git_commit"], "code_dirty": code["working_tree_dirty"],
           "inputs_json": json.dumps(inputs, sort_keys=True), "supersedes_sha256": same[-1]["sha256"] if same else "",
           "notes": notes}
    hashchain.append(manifest_path, MANIFEST_FIELDS, "manifest_row", [row])
    return {"status": status, "path": path, "sha256": sha, "manifest": "appended"}


def verify_manifest(manifest_path, derived_dir):
    """Chain integrity plus re-hash of every referenced partition file."""
    ok, n, head, errors = hashchain.verify(manifest_path, MANIFEST_FIELDS, "manifest_row")
    errors = list(errors)
    for r in hashchain.read_rows(manifest_path):
        path = Path(derived_dir) / r["relative_path"]
        if not path.exists():
            errors.append(f"missing partition {r['relative_path']}")
        elif eng.sha256_file(path) != r["sha256"]:
            errors.append(f"partition altered {r['relative_path']}")
    return (not errors), n, head, errors


# -------------------------------------------------------------------------------- parity
def parity_check(games_path, n=200, seed=11, tolerance_report=20, include_rare=True):
    """Compare batch features with the v1.0.1 single-game engine for n random completed REG games."""
    from types import SimpleNamespace
    import tempfile
    raw = eng.read_schedule(games_path)
    tables = build_tables(raw)
    team = tables["team_game_features"].set_index(["game_id", "side"])
    games = tables["game_features"].set_index("game_id")
    pool = games[games.game_type == "REG"].index.tolist()
    rng = random.Random(seed)
    sample = rng.sample(pool, min(n, len(pool)))
    if include_rare:  # rare events are almost never hit by a random sample, so force them in
        rare = games[(games.f5_prev_meeting_tied_rs == 1) & (games.game_type == "REG")].index.tolist()
        mirrored = games[(games.f4_mirrored_current_records == 1)].index.tolist()
        sample = list(dict.fromkeys(sample + rare + rng.sample(mirrored, min(40, len(mirrored)))))
    original = eng.read_schedule
    eng.read_schedule = lambda path: raw.copy()
    mismatches, compared = [], 0
    try:
        for gid in sample:
            g = raw[raw.game_id == gid].iloc[0]
            with tempfile.TemporaryDirectory() as tmp:
                ctx, findings = eng.run(SimpleNamespace(date=str(g.gameday), away=g.away_team, home=g.home_team, week=None,
                                                        games=games_path, rosters=None, output=Path(tmp), no_ledger=True))
            by = {(f["feature_id"], f["team"], f["name_basis"] if f["category"] == "gematria" else ""): f["value"] for f in findings}
            def expect(label, key, mine, basis=""):
                nonlocal compared
                compared += 1
                theirs = by.get((key[0], key[1], basis))
                if mine is None or (isinstance(mine, float) and np.isnan(mine)) or mine is pd.NA:
                    if theirs is not None: mismatches.append((gid, label, theirs, None))
                elif theirs is None or str(theirs) != str(mine):
                    mismatches.append((gid, label, theirs, mine))
            for side in ("away", "home"):
                t = team.loc[(gid, side)]
                fid = t.franchise_id
                rec = f"{t.q_season_wins}-{t.q_season_losses}-{t.q_season_ties}"
                expect(f"{side} record", ("records.current_season_record", fid), rec)
                expect(f"{side} days_since_win", ("streaks.days_since_last_win", fid), None if pd.isna(t.q_days_since_last_win_rs) else int(t.q_days_since_last_win_rs))
                expect(f"{side} days_since_loss", ("streaks.days_since_last_loss", fid), None if pd.isna(t.q_days_since_last_loss_rs) else int(t.q_days_since_last_loss_rs))
                expect(f"{side} thu_days", ("calendar.days_since_last_thursday_win", fid), None if pd.isna(t.q_days_since_last_thursday_win) else int(t.q_days_since_last_thursday_win))
                expect(f"{side} thu_months", ("calendar.completed_months_since_last_thursday_win", fid), None if pd.isna(t.q_completed_months_since_last_thursday_win) else int(t.q_completed_months_since_last_thursday_win))
                for kind in KINDS:
                    for field in FIELDS:
                        expect(f"{side} {kind} {field}", (f"gematria.{kind}.{field}", fid), int(t[f"nm_historical_{kind}_{field}"]), "historical")
                if t.cur_nickname != t.hist_nickname or t.cur_city != t.hist_city:
                    for kind in KINDS:
                        for field in FIELDS:
                            expect(f"{side} current {kind} {field}", (f"gematria.{kind}.{field}", fid), int(t[f"nm_current_{kind}_{field}"]), "current")
            t = team.loc[(gid, "away")]
            for key, col in (("calendar.days_remaining_in_year", "q_days_remaining"), ("calendar.date_digit_sum", "q_date_digit_sum"),
                             ("calendar.date_digit_root", "q_date_digit_root"), ("calendar.weekday_number", "q_weekday_number")):
                expect(key, (key, ""), int(t[col]))
            g_row = games.loc[gid]
            compared += 2
            if (("records.mirrored_current_season", "", "") in by) != bool(g_row.f4_mirrored_current_records):
                mismatches.append((gid, "mirrored", ("records.mirrored_current_season", "", "") in by, int(g_row.f4_mirrored_current_records)))
            if (("head_to_head.previous_meeting_tied", "", "") in by) != bool(g_row.f5_prev_meeting_tied_rs):
                mismatches.append((gid, "prev_tied", ("head_to_head.previous_meeting_tied", "", "") in by, int(g_row.f5_prev_meeting_tied_rs)))
    finally:
        eng.read_schedule = original
    return {"games_sampled": len(sample), "values_compared": compared, "mismatches": len(mismatches),
            "first_mismatches": mismatches[:tolerance_report]}


# --------------------------------------------------------------------------------- build
def coverage_report(raw, tables):
    done = _completed(raw)
    team = tables["team_game_features"]
    per_game = team.groupby("game_id").size()
    gaps = eng.identity_coverage_gaps(done)
    return {"completed_games": int(len(done)), "team_game_rows": int(len(team)),
            "games_without_exactly_two_rows": int((per_game != 2).sum()),
            "games_missing_from_team_table": int(len(set(done.game_id) - set(team.game_id))),
            "identity_coverage_gaps": int(gaps), "grid_flag_columns": int(len(tables["grid_flags"].columns) - 4),
            "game_rows": int(len(tables["game_features"]))}


def build_all(games_path, roster_dir, retrieved, derived_dir=DEFAULT_DERIVED, manifest_path=DEFAULT_MANIFEST,
              games_source_url=None, rosters_source_url=None):
    raw = eng.read_schedule(games_path)
    tables = build_tables(raw)
    cov = coverage_report(raw, tables)
    registry_sha = reg.registry_sha256()
    inputs = {"schedule": eng.input_provenance(games_path, "schedule", games_source_url, eng.GAMES_DEFAULT_SOURCE, retrieved),
              "identity_table": eng.input_provenance(eng.IDENTITY_PATH, "team_identity_eras")}
    for k in ("path", "file_mtime_utc"):
        for v in inputs.values(): v.pop(k, None)
    results = []
    all_tables = dict(tables)
    if roster_dir:
        all_tables.update(build_player_tables(tables["team_game_features"], roster_dir, retrieved))
        roster_files = _roster_files(roster_dir)
        inputs["rosters"] = {"role": "weekly_roster", "retrieved_date": retrieved,
                             "source_url": rosters_source_url or eng.ROSTER_DEFAULT_SOURCE,
                             "files": {str(s): {"basename": p.name, "sha256": eng.sha256_file(p)} for s, p in sorted(roster_files.items())},
                             "label": "PREVIOUS_WEEK_ROSTER proxy; previous-week roster as retrieved on the retrieval date; not game-day active status"}
    code = eng.code_provenance()
    notes = {"team_game_features": "Pregame values only; no outcome columns.", "game_features": "F4 mirrored records and F5 previous-meeting tie flags; pregame only.",
             "grid_flags": "504 Tier B exploratory flags; hypothesis-generating only.",
             "roster_candidates_previous_week": "PREVIOUS_WEEK_ROSTER proxy name-match candidates; no outcomes joined.",
             "roster_candidates_same_week_sensitivity": "SENSITIVITY ONLY: same-week snapshot, timing unverified.",
             "roster_coverage": "Snapshot week, staleness and status per REG team-game."}
    for name, frame in all_tables.items():
        for split in SPLIT_NAMES:
            part = frame[frame.split == split]
            if part.empty: continue
            res = write_partition(part.reset_index(drop=True), name, split, derived_dir, manifest_path, registry_sha, inputs, notes[name], code)
            results.append({"partition": name, "split": split, "rows": len(part), **{k: str(v) for k, v in res.items()}})
    return {"coverage": cov, "partitions": results, "registry_sha256": registry_sha}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--games", type=Path, required=True)
    p.add_argument("--rosters", type=Path, help="directory of roster_weekly_YYYY.csv files")
    p.add_argument("--retrieved", default="unknown", help="retrieval date for the input files (YYYY-MM-DD)")
    p.add_argument("--derived-dir", type=Path, default=DEFAULT_DERIVED)
    p.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    p.add_argument("--verify", action="store_true", help="verify manifest chain and partition hashes only")
    p.add_argument("--parity", type=int, default=0, help="run parity check against the v1.0.1 engine on N random games")
    a = p.parse_args()
    if a.verify:
        ok, n, head, errors = verify_manifest(a.manifest, a.derived_dir)
        print(json.dumps({"ok": ok, "rows": n, "head": head, "errors": errors}, indent=2)); sys.exit(0 if ok else 1)
    if a.parity:
        out = parity_check(a.games, a.parity)
        print(json.dumps(out, indent=2, default=str)); sys.exit(0 if out["mismatches"] == 0 else 1)
    out = build_all(a.games, a.rosters, a.retrieved, a.derived_dir, a.manifest)
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
