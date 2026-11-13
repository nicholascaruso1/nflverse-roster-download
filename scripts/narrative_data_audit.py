#!/usr/bin/env python3
"""v1.1 data audits: games-per-split reconciliation and play-by-play schema inspection.

Outcome-blind: these reports count games, columns and identifier coverage. They never
join features to winners, scores-by-feature or any other research outcome.
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nfl_script_narrative_engine as engine

# Regular-season games per full schedule (31 teams x 16 / 2 = 248 through 2001; 256 through 2020; 272 from 2021).
def expected_regular_games(season):
    return 248 if season <= 2001 else (256 if season <= 2020 else 272)

PBP_REQUIRED = ["game_id", "season", "week", "season_type", "posteam", "defteam", "play_id", "play_type",
                "desc", "yards_gained", "touchdown", "td_team", "td_player_id", "td_player_name",
                "total_home_score", "total_away_score", "game_date"]
PBP_PLAYER_OUTCOME = ["complete_pass", "pass_touchdown", "rush_touchdown", "receiver_player_id",
                      "receiver_player_name", "receiving_yards", "rusher_player_id", "rusher_player_name"]


def reconcile_splits(games_path):
    raw = engine.read_schedule(games_path)
    done = raw[raw.away_score.notna() & raw.home_score.notna()]
    reg = done[done.game_type.eq("REG")]
    rows = []
    for season, grp in reg.groupby("season"):
        season = int(season)
        ties = int((grp.away_score == grp.home_score).sum())
        rows.append({"season": season, "split": engine.split_for_season(season), "reg_completed": len(grp),
                     "expected_full_schedule": expected_regular_games(season),
                     "difference": len(grp) - expected_regular_games(season),
                     "team_game_rows": 2 * len(grp), "ties": ties,
                     "playoff_games": int(((done.season == season) & ~done.game_type.eq("REG")).sum()),
                     "first_gameday": str(grp.gameday.min()), "last_gameday": str(grp.gameday.max())})
    table = pd.DataFrame(rows)
    by_split = (table.groupby("split")[["reg_completed", "team_game_rows", "ties", "playoff_games"]].sum()
                .reindex(["discovery", "validation", "holdout", "prospective"]))
    by_split["seasons"] = table.groupby("split").season.agg(lambda s: f"{s.min()}-{s.max()}")
    last_done = done.gameday.max()
    unscored = raw[raw.game_type.eq("REG") & (raw.gameday < last_done) & (raw.away_score.isna() | raw.home_score.isna())]
    checks = {"identity_coverage_gaps": engine.identity_coverage_gaps(done),
              "duplicate_game_ids": int(done.game_id.duplicated().sum()),
              "unscored_regular_season_games_before_last_completed_date": ", ".join(
                  f"{r.game_id} ({r.gameday})" for r in unscored.itertuples()) or "none",
              "team_game_rows_equal_twice_games": bool((table.team_game_rows == 2 * table.reg_completed).all())}
    return table, by_split, checks


def sha256_file(path):
    return engine.sha256_file(Path(path))


def inspect_pbp(pbp_dir, games_path, roster_dir=None):
    import pyarrow.parquet as pq
    raw = engine.read_schedule(games_path)
    done = raw[raw.away_score.notna() & raw.home_score.notna()]
    sched_ids = {int(s): set(g.game_id) for s, g in done.groupby("season")}
    rows = []
    for path in sorted(Path(pbp_dir).glob("play_by_play_*.parquet")):
        season = int(path.stem.rsplit("_", 1)[-1])
        meta = pq.ParquetFile(path)
        names = set(meta.schema_arrow.names)
        missing_req = sorted(set(PBP_REQUIRED) - names)
        missing_out = sorted(set(PBP_PLAYER_OUTCOME) - names)
        use = [c for c in ("game_id", "season_type", "touchdown", "td_player_id", "complete_pass",
                           "receiver_player_id", "receiving_yards", "rush_touchdown", "pass_touchdown",
                           "rusher_player_id") if c in names]
        frame = pd.read_parquet(path, columns=use)
        games = set(frame.game_id.dropna())
        reg_sched = {g for g in sched_ids.get(season, set())}
        row = {"season": season, "file": path.name, "bytes": path.stat().st_size, "sha256": sha256_file(path),
               "rows": int(meta.metadata.num_rows), "columns": int(meta.metadata.num_columns),
               "missing_required": ";".join(missing_req), "missing_player_outcome_cols": ";".join(missing_out),
               "pbp_games": len(games), "schedule_completed_games": len(reg_sched),
               "in_schedule_not_pbp": len(reg_sched - games), "in_pbp_not_schedule": len(games - reg_sched)}
        if "touchdown" in frame and "td_player_id" in frame:
            td = frame[frame.touchdown == 1]
            row["td_plays"] = len(td)
            row["td_player_id_null_pct"] = round(100 * td.td_player_id.isna().mean(), 2) if len(td) else None
        if "complete_pass" in frame and "receiver_player_id" in frame:
            cp = frame[frame.complete_pass == 1]
            row["completions"] = len(cp)
            row["receiver_id_null_pct"] = round(100 * cp.receiver_player_id.isna().mean(), 2) if len(cp) else None
        if roster_dir and (Path(roster_dir) / f"roster_weekly_{season}.csv").exists() and "receiver_player_id" in frame:
            roster = pd.read_csv(Path(roster_dir) / f"roster_weekly_{season}.csv", usecols=["gsis_id"], low_memory=False)
            ids = set(frame.receiver_player_id.dropna())
            row["receiver_ids"] = len(ids)
            row["receiver_ids_in_roster_pct"] = round(100 * len(ids & set(roster.gsis_id.dropna())) / len(ids), 1) if ids else None
        elif roster_dir:
            row["roster_file"] = "absent"
        rows.append(row)
    return pd.DataFrame(rows)


def write_reports(out_dir, games_path, pbp_dir=None, roster_dir=None):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    table, by_split, checks = reconcile_splits(games_path)
    table.to_csv(out / "games_per_season_reconciliation.csv", index=False)
    lines = ["# v1.1 games-per-split reconciliation (outcome-blind)", "",
             f"Schedule file SHA-256: `{sha256_file(games_path)}`", "",
             "Completed regular-season games only. Prospective = games after the 2025 season (2026 in progress).", "",
             "## By split", "", by_split.to_markdown(), "", "## Integrity checks", "",
             "\n".join(f"- {k}: {v}" for k, v in checks.items()), "",
             "## Seasons whose completed count differs from a full schedule", ""]
    off = table[(table.difference != 0) & (table.split != "prospective")]
    lines += ["None." if off.empty else off[["season", "reg_completed", "expected_full_schedule", "difference"]].to_markdown(index=False)]
    lines += ["", "Expected full schedule: 248 games through 2001, 256 for 2002-2020, 272 from 2021. "
              "Differences are reported, not corrected; any difference must be explained by nflverse data (e.g. a cancelled or "
              "unscored game) before the split is frozen.", ""]
    (out / "games_per_split_reconciliation.md").write_text("\n".join(lines))
    if pbp_dir:
        pbp = inspect_pbp(pbp_dir, games_path, roster_dir)
        pbp.to_csv(out / "pbp_schema_inventory.csv", index=False)
        bad = pbp[(pbp.missing_required != "") | (pbp.missing_player_outcome_cols != "")]
        text = ["# v1.1 play-by-play schema inspection (outcome-blind)", "",
                f"Files inspected: {len(pbp)} (seasons {pbp.season.min()}-{pbp.season.max()}); total rows {int(pbp.rows.sum()):,}.", "",
                "Required columns checked: " + ", ".join(PBP_REQUIRED) + ".", "",
                "Player-outcome columns checked (needed by F8-F10 later; not joined in v1.1): " + ", ".join(PBP_PLAYER_OUTCOME) + ".", "",
                "## Seasons with missing columns", ""]
        text += ["None." if bad.empty else bad[["season", "missing_required", "missing_player_outcome_cols"]].to_markdown(index=False)]
        cols = [c for c in ("season", "rows", "columns", "pbp_games", "schedule_completed_games", "in_schedule_not_pbp",
                            "in_pbp_not_schedule", "td_player_id_null_pct", "receiver_id_null_pct",
                            "receiver_ids_in_roster_pct") if c in pbp.columns]
        text += ["", "## Per-season inventory (full table with SHA-256 in pbp_schema_inventory.csv)", "", pbp[cols].to_markdown(index=False), ""]
        (out / "pbp_schema_report.md").write_text("\n".join(text))
    return table, by_split, checks


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--games", type=Path, required=True)
    p.add_argument("--pbp-dir", type=Path)
    p.add_argument("--rosters", type=Path)
    p.add_argument("--output", type=Path, default=Path("reports/v1.1"))
    a = p.parse_args()
    table, by_split, checks = write_reports(a.output, a.games, a.pbp_dir, a.rosters)
    print(by_split.to_string()); print(checks)

if __name__ == "__main__":
    main()
