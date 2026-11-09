#!/usr/bin/env python3
"""Build a reproducible NFL scoring-event ledger and TD jersey-number join."""
from pathlib import Path
import pandas as pd

PBP_DIR = Path("pbp")
ROSTER_DIR = Path("rosters")
OUT = Path("output")
OUT.mkdir(exist_ok=True)

required = {
    "game_id", "season", "week", "posteam", "defteam", "play_id",
    "play_type", "desc", "touchdown", "td_team", "td_player_id",
    "td_player_name", "field_goal_result", "extra_point_result",
    "two_point_conv_result", "safety", "game_date"
}
pbp_frames = []
schema_rows = []

for path in sorted(PBP_DIR.glob("play_by_play_*.parquet")):
    df = pd.read_parquet(path)
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"{path.name} missing required columns: {sorted(missing)}")
    df["source_season_file"] = path.name
    schema_rows.append({
        "season_file": path.name, "rows": len(df), "columns": len(df.columns),
        "has_game_type": "game_type" in df.columns
    })
    pbp_frames.append(df)

pbp = pd.concat(pbp_frames, ignore_index=True)
pbp["touchdown"] = pd.to_numeric(pbp["touchdown"], errors="coerce").fillna(0).astype(int)
pbp["safety"] = pd.to_numeric(pbp["safety"], errors="coerce").fillna(0).astype(int)

def norm(v):
    if pd.isna(v):
        return ""
    return str(v).strip().lower()

# Preserve all scoring-play classes; player attribution is meaningful primarily for TDs.
td = pbp[pbp["touchdown"].eq(1)].copy()
td["event_type"] = "TOUCHDOWN"
td["scoring_team"] = td["td_team"].where(td["td_team"].notna() & td["td_team"].ne(""), td["posteam"])

fg = pbp[pbp["field_goal_result"].astype("string").str.lower().eq("made")].copy()
fg["event_type"] = "FIELD_GOAL"
fg["scoring_team"] = fg["posteam"]

safety = pbp[pbp["safety"].eq(1)].copy()
safety["event_type"] = "SAFETY"
safety["scoring_team"] = safety["defteam"]

xp = pbp[pbp["extra_point_result"].astype("string").str.lower().isin(["good", "made", "successful"])].copy()
xp["event_type"] = "EXTRA_POINT"
xp["scoring_team"] = xp["posteam"]

two = pbp[pbp["two_point_conv_result"].astype("string").str.lower().isin(["success", "successful", "good"])].copy()
two["event_type"] = "TWO_POINT_CONVERSION"
two["scoring_team"] = two["posteam"]

cols = ["game_id", "season", "week", "game_date", "play_id", "event_type",
        "scoring_team", "posteam", "defteam", "td_player_id", "td_player_name",
        "desc", "source_season_file"]
events = pd.concat([x.reindex(columns=cols) for x in [td, fg, safety, xp, two]], ignore_index=True)
events = events.reset_index(drop=True)
events["play_id"] = pd.to_numeric(events["play_id"], errors="coerce")
events = events.sort_values(["game_id", "play_id", "event_type"], kind="stable")
events["is_first_td"] = False
td_idx = events.index[events["event_type"].eq("TOUCHDOWN")]
first_td_idx = events.loc[td_idx].groupby("game_id", sort=False)["play_id"].idxmin()
events.loc[first_td_idx, "is_first_td"] = True

# Load historical weekly rosters and resolve GSIS player ID + game-week + team.
roster_paths = sorted(ROSTER_DIR.glob("roster_weekly_*.csv"))
if not roster_paths:
    raise SystemExit("No weekly roster CSVs found")
rosters = pd.concat([pd.read_csv(p, low_memory=False) for p in roster_paths], ignore_index=True)
for c in ["season", "week"]:
    rosters[c] = pd.to_numeric(rosters[c], errors="coerce")
rosters["gsis_id"] = rosters["gsis_id"].astype("string").str.strip()
rosters["jersey_number"] = rosters["jersey_number"].astype("string").str.strip()

td_events = events["event_type"].eq("TOUCHDOWN")
td_join = events.loc[td_events].copy()
td_join["gsis_id"] = td_join["td_player_id"].astype("string").str.strip()
roster_key = rosters[["season", "week", "team", "gsis_id", "jersey_number",
                      "position", "full_name", "status"]].dropna(subset=["gsis_id"]).copy()

# Historical nflverse team-code aliases. Normalize both sources to current-style codes.
team_aliases = {
    "ARZ": "ARI", "BLT": "BAL", "CLV": "CLE", "HST": "HOU",
    "JAC": "JAX", "SD": "LAC", "OAK": "LV", "SL": "LA"
}
roster_key["team_norm"] = roster_key["team"].astype("string").replace(team_aliases)
roster_key = roster_key.drop_duplicates(["season", "week", "team_norm", "gsis_id"], keep="last")
td_join["scoring_team_norm"] = td_join["scoring_team"].astype("string").replace(team_aliases)
joined = td_join.merge(roster_key, on=["season", "week", "gsis_id"], how="left", suffixes=("", "_roster"))
joined["team_match"] = joined["scoring_team_norm"].eq(joined["team_norm"])
joined["jersey_join_status"] = "MATCHED"
joined.loc[joined["td_player_id"].isna() | joined["td_player_id"].astype("string").str.strip().eq(""), "jersey_join_status"] = "NO_PLAYER_ID"
joined.loc[joined["td_player_id"].notna() & joined["team"].isna(), "jersey_join_status"] = "UNMATCHED_ROSTER"
joined.loc[joined["team"].notna() & ~joined["team_match"], "jersey_join_status"] = "TEAM_MISMATCH"

# When multiple roster entries exist, prefer exact team match, then available jersey number.
joined = joined.sort_values(["game_id", "play_id", "team_match"], ascending=[True, True, False], kind="stable")
joined = joined.drop_duplicates(["game_id", "play_id"], keep="first")

events.to_csv(OUT / "scoring_event_ledger.csv", index=False)
joined.to_csv(OUT / "touchdown_player_jersey_join.csv", index=False)
pd.DataFrame(schema_rows).to_csv(OUT / "pbp_schema_manifest.csv", index=False)

summary = {
    "pbp_seasons": len(schema_rows),
    "pbp_rows": int(sum(x["rows"] for x in schema_rows)),
    "scoring_events": int(len(events)),
    "touchdowns": int(len(td)),
    "first_td_games": int(events.loc[events["is_first_td"], "game_id"].nunique()),
    "td_with_player_id": int(td["td_player_id"].notna().sum()),
    "td_jersey_matched": int(joined["jersey_join_status"].eq("MATCHED").sum()),
    "td_no_player_id": int(joined["jersey_join_status"].eq("NO_PLAYER_ID").sum()),
    "td_unmatched_roster": int(joined["jersey_join_status"].eq("UNMATCHED_ROSTER").sum()),
    "td_team_mismatch": int(joined["jersey_join_status"].eq("TEAM_MISMATCH").sum()),
}
pd.Series(summary, name="value").to_csv(OUT / "build_summary.csv", header=True)
print(pd.Series(summary).to_string())
