#!/usr/bin/env python3
"""Reproducibility audit for BUF @ MIN (2026 wk9) model reports.
Usage: python3 -I audit.py <dir with play_by_play_2026.parquet (or pbp_2026.parquet), roster_weekly_2026.csv, games.csv> <out_md>
Every figure in the original reports is regenerated from raw nflverse files here.
"""
import sys
import numpy as np
import pandas as pd

D, OUT = sys.argv[1], sys.argv[2]
import os
_pf = next((f for f in (f"{D}/play_by_play_2026.parquet", f"{D}/pbp_2026.parquet", f"{D}/play_by_play_2026.csv") if os.path.exists(f)), None)
if _pf is None:
    sys.exit("no PBP file found (play_by_play_2026.parquet / pbp_2026.parquet / play_by_play_2026.csv)")
# CSV fallback is a lossless export of the parquet (for environments without pyarrow); dtype lines in the schema table may differ
p = pd.read_csv(_pf, low_memory=False) if _pf.endswith(".csv") else pd.read_parquet(_pf)
ro = pd.read_csv(f"{D}/roster_weekly_2026.csv", low_memory=False)
out = []


def md(df, fmt=".3f"):
    return df.to_markdown(index=False, floatfmt=fmt) + "\n"


def h(s):
    out.append("\n" + s + "\n")


def para(s):
    out.append(s + "\n")


# ---------- filters -------------------------------------------------------
# Efficiency base: play_type in (pass, run) AND epa not null AND posteam not null.
base = p[p.play_type.isin(["pass", "run"]) & p.epa.notna() & p.posteam.notna()].copy()
TEAMS = ["BUF", "MIN"]
games = {}
for t in TEAMS:
    g = p[(p.home_team == t) | (p.away_team == t)][["game_id", "week", "home_team", "away_team"]].drop_duplicates()
    g["opp"] = np.where(g.home_team == t, g.away_team, g.home_team)
    games[t] = g.sort_values("week").reset_index(drop=True)


def mean_or_nan(s):
    return float(s.mean()) if len(s) else float("nan")


# ---------- 1. team efficiency -------------------------------------------
h("## 1. Team efficiency reconciliation")
para("**Filters (exact).** `season==2026`; `play_type in {pass, run}`; `epa` not null; `posteam` not null. "
     "Offense rows = filter + `posteam==TEAM`. Defense rows = filter + `defteam==TEAM`. "
     "Pass rows = `pass==1` (nflverse sets this on dropbacks: it includes sacks and QB scrambles). "
     "Rush rows = `rush==1` (designed runs only; scrambles are NOT in rush). "
     "Success rate = mean of `success`. All EPA/SR figures are plain per-play means over those rows, "
     "so the aggregate is a play-weighted mean of the per-game values. "
     "No opponent adjustment, no garbage-time or win-probability filter, no special-teams plays.")
sc = p[p.qb_scramble == 1].groupby(["play_type", "pass", "rush"]).size().reset_index(name="n")
para("Scramble row classification check (all 2026 plays with `qb_scramble==1`):")
out.append(md(sc, ".0f"))

ORIG = {  # values printed in the original Bet Model report
    "BUF": dict(off_epa=.173, off_sr=.490, off_pass=.291, off_rush=.022, def_epa=.063, def_pass=.140, def_rush=-.077),
    "MIN": dict(off_epa=-.096, off_sr=.373, off_pass=-.016, off_rush=-.206, def_epa=-.169, def_pass=-.207, def_rush=-.116),
}
recon_rows = []
for t in TEAMS:
    rows = []
    for _, gm in games[t].iterrows():
        o = base[(base.game_id == gm.game_id) & (base.posteam == t)]
        d = base[(base.game_id == gm.game_id) & (base.defteam == t)]
        rows.append(dict(
            wk=int(gm.week), game_id=gm.game_id, opp=gm.opp,
            off_n=len(o), off_epa=mean_or_nan(o.epa), off_sr=mean_or_nan(o.success),
            off_pass_n=int((o["pass"] == 1).sum()), off_pass_epa=mean_or_nan(o[o["pass"] == 1].epa),
            off_rush_n=int((o["rush"] == 1).sum()), off_rush_epa=mean_or_nan(o[o["rush"] == 1].epa),
            def_n=len(d), def_epa=mean_or_nan(d.epa), def_sr=mean_or_nan(d.success),
            def_pass_epa=mean_or_nan(d[d["pass"] == 1].epa), def_rush_epa=mean_or_nan(d[d["rush"] == 1].epa)))
    gdf = pd.DataFrame(rows)
    h(f"### {t}: seven games")
    out.append(md(gdf))
    O = base[base.posteam == t]
    Dd = base[base.defteam == t]
    agg = dict(
        off_n=len(O), off_epa=O.epa.mean(), off_sr=O.success.mean(),
        off_pass=O[O["pass"] == 1].epa.mean(), off_rush=O[O["rush"] == 1].epa.mean(),
        def_n=len(Dd), def_epa=Dd.epa.mean(), def_sr=Dd.success.mean(),
        def_pass=Dd[Dd["pass"] == 1].epa.mean(), def_rush=Dd[Dd["rush"] == 1].epa.mean())
    wavg = dict(
        off_epa=np.average(gdf.off_epa, weights=gdf.off_n),
        off_sr=np.average(gdf.off_sr, weights=gdf.off_n),
        off_pass=np.average(gdf.off_pass_epa, weights=gdf.off_pass_n),
        off_rush=np.average(gdf.off_rush_epa, weights=gdf.off_rush_n),
        def_epa=np.average(gdf.def_epa, weights=gdf.def_n),
        def_sr=np.average(gdf.def_sr, weights=gdf.def_n))
    para(f"{t} pooled aggregate: off plays {agg['off_n']}, def plays {agg['def_n']}; "
         f"unweighted mean of the seven per-game off EPA values = {gdf.off_epa.mean():.3f} (NOT what the report used). "
         f"Play-weighted per-game mean = pooled value (max abs diff below).")
    for k, orig_k in [("off_epa", "off_epa"), ("off_sr", "off_sr"), ("off_pass", "off_pass"), ("off_rush", "off_rush"),
                      ("def_epa", "def_epa"), ("def_pass", "def_pass"), ("def_rush", "def_rush")]:
        pooled = agg[k]
        w = wavg.get(k, np.nan)
        recon_rows.append(dict(team=t, metric=k, original_report=ORIG[t][orig_k], recomputed_pooled=round(pooled, 3),
                               match=("yes" if abs(round(pooled, 3) - ORIG[t][orig_k]) < 0.0006 else "NO"),
                               weighted_per_game=(round(w, 3) if w == w else None)))
    # excluded-row accounting
    allrows = p[(p.home_team == t) | (p.away_team == t)]
    acc = dict(
        total_rows=len(allrows),
        play_type_not_pass_run=int((~allrows.play_type.isin(["pass", "run"])).sum()),
        pass_run_epa_null=int((allrows.play_type.isin(["pass", "run"]) & allrows.epa.isna()).sum()),
        pass_run_posteam_null=int((allrows.play_type.isin(["pass", "run"]) & allrows.posteam.isna()).sum()),
        kept_both_sides=int(allrows.index.isin(base.index).sum()),
        play_type_counts=allrows.play_type.value_counts(dropna=False).to_dict())
    para(f"{t} row accounting (all rows in the 7 games): {acc}")
    h(f"#### {t} other efficiency-adjacent figures in the report (same filters)")
    op = O[O["pass"] == 1]
    dp = Dd[Dd["pass"] == 1]
    para(f"20+ yd pass rate = share of `pass==1` offense rows with `yards_gained>=20`: {(op.yards_gained >= 20).sum()}/{len(op)} = {(op.yards_gained >= 20).mean():.3f}. "
         f"Plays per game = off rows / 7 = {len(O)}/7 = {len(O) / 7:.1f}. "
         f"Sack rate taken = mean(`sack`) over pass rows = {int(op.sack.sum())}/{len(op)} = {op.sack.mean():.3f}. "
         f"Def sack rate = {int(dp.sack.sum())}/{len(dp)} = {dp.sack.mean():.3f}.")
out.append("\n### Reconciliation: original report vs recomputed\n")
rec = pd.DataFrame(recon_rows)
out.append(md(rec))
para(f"League reference: off EPA {base.epa.mean():.3f}, SR {base.success.mean():.3f} over {len(base)} rows (both sides, all teams).")

# ---------- 2. player volume ----------------------------------------------
h("## 2. Player volume reconciliation (WATCH props, plus Kincaid who was WATCH in the original card)")
para("**Filters.** Team games = every game the team played in the 2026 PBP file (BUF 7: wks 1-6, 8; MIN 7: wks 1-5, 7, 8). "
     "Receiving: rows with `receiver_player_id` = player id and `play_type=='pass'` (target); reception = `complete_pass==1`; "
     "receiving yards = sum `receiving_yards`. Rushing: `rush==1` and `rusher_player_id` = player id (designed runs, scrambles excluded); "
     "yards = sum `rushing_yards`. Passing: `passer_player_id` = player id; **box-score attempt = `pass_attempt==1 & sack!=1`** (in this file `pass_attempt==1` is also set on sack rows, so the raw flag equals dropbacks); "
     "dropbacks = `pass==1` rows with that passer (includes sacks and scrambles). Zero-volume games are shown as zero if the player has any row for the team that season; "
     "whether a zero is a scratch or a non-involvement cannot be determined from PBP (no 2026 participation file).")


def pid(name, team, col):
    ids = p[(p[col.replace("_id", "_name")] == name) & (p.posteam == team)][col].dropna().unique()
    return list(ids)


def team_games(t):
    return list(games[t][["week", "game_id"]].itertuples(index=False, name=None))


def recv_log(name, team):
    ids = pid(name, team, "receiver_player_id")
    rows = []
    for wk, gid in team_games(team):
        x = p[(p.game_id == gid) & (p.posteam == team) & (p.play_type == "pass") & (p.receiver_player_id.isin(ids))]
        rows.append(dict(wk=wk, game_id=gid, tgt=len(x), rec=int(x.complete_pass.sum()), rec_yds=float(x.receiving_yards.sum())))
    return ids, pd.DataFrame(rows)


def rush_log(name, team):
    ids = pid(name, team, "rusher_player_id")
    rows = []
    for wk, gid in team_games(team):
        x = p[(p.game_id == gid) & (p.posteam == team) & (p.rush == 1) & (p.rusher_player_id.isin(ids))]
        rows.append(dict(wk=wk, game_id=gid, car=len(x), rush_yds=float(x.rushing_yards.sum())))
    return ids, pd.DataFrame(rows)


def pass_log(name, team):
    ids = pid(name, team, "passer_player_id")
    rows = []
    for wk, gid in team_games(team):
        x = p[(p.game_id == gid) & (p.posteam == team) & (p["pass"] == 1) & (p.passer_player_id.isin(ids))]
        a = x[x.pass_attempt == 1]
        rows.append(dict(wk=wk, game_id=gid, dropbacks=len(x), pass_attempt_flag=len(a),
                         att_excl_sacks=int(((x.pass_attempt == 1) & (x.sack != 1)).sum()), cmp=int(a.complete_pass.sum()),
                         pass_yds=float(x.passing_yards.sum()), sacks=int(x.sack.sum()), scrambles=int(x.qb_scramble.sum()),
                         ints=int(x.interception.sum())))
    return ids, pd.DataFrame(rows)


def roster_status(name_like, team, weeks):
    r = ro[(ro.team == team) & ro.full_name.str.contains(name_like, na=False) & ro.week.isin(weeks)]
    return r[["week", "full_name", "position", "status", "status_description_abbr"]].sort_values("week")


# Cook
ids, cook = rush_log("J.Cook", "BUF")
_, cook_r = recv_log("J.Cook", "BUF")
cook = cook.merge(cook_r[["wk", "tgt", "rec", "rec_yds"]], on="wk")
h("### James Cook (BUF)")
para(f"gsis ids matched for `J.Cook` as BUF rusher: {ids}")
out.append(md(cook, ".1f"))
n = len(cook)
para(f"Carries: sum {int(cook.car.sum())}, mean over {n} games = {cook.car.mean():.2f}; games with 19+ carries (threshold for O18.5) = {(cook.car >= 19).sum()} of {n}. "
     f"Rush yds: mean {cook.rush_yds.mean():.1f}; games over 84.5 = {(cook.rush_yds > 84.5).sum()}, over 86.5 = {(cook.rush_yds > 86.5).sum()} of {n}.")
bt = p[(p.posteam == "BUF") & (p.rush == 1) & (p.play_type == "run") & p.rusher_player_id.notna() & p.rusher_player_name.notna()]
para(f"Share denominator used in the report: BUF `rush==1`, `play_type=='run'`, rusher id/name not null = {len(bt)} rows; Cook {int(cook.car.sum())} = {cook.car.sum() / len(bt):.3f}.")

# Wentz / Murray
h("### Carson Wentz and Kyler Murray (MIN) — passing")
for nm in ["C.Wentz", "K.Murray"]:
    ids, wl = pass_log(nm, "MIN")
    para(f"**{nm}** ids: {ids}")
    out.append(md(wl, ".1f"))
    wl2 = wl[wl.dropbacks > 0]
    para(f"{nm}: games with dropbacks = {len(wl2)} (weeks {list(wl2.wk)}); dropbacks {int(wl2.dropbacks.sum())}, `pass_attempt==1` rows {int(wl2.pass_attempt_flag.sum())}, "
         f"attempts excluding sacks {int(wl2.att_excl_sacks.sum())}, completions {int(wl2.cmp.sum())}, yards {wl2.pass_yds.sum():.0f}, sacks {int(wl2.sacks.sum())}, scrambles {int(wl2.scrambles.sum())}. "
         f"Yards per game over games with dropbacks = {wl2.pass_yds.mean():.1f}; dropbacks per game = {wl2.dropbacks.mean():.1f}; attempts excluding sacks per game = {wl2.att_excl_sacks.mean():.1f}. "
         f"**In this file `pass_attempt==1` is set on every sack row, so it equals dropbacks.** The original reports' 'attempts' (Wentz 23 per game, Murray 28.2 per game) are therefore DROPBACKS, not box-score attempts.")

# receivers
for nm, tm in [("J.Jefferson", "MIN"), ("T.Hockenson", "MIN"), ("D.Kincaid", "BUF")]:
    ids, rl = recv_log(nm, tm)
    h(f"### {nm} ({tm})")
    para(f"receiver ids: {ids}")
    out.append(md(rl, ".1f"))
    gp = rl[rl.tgt > 0]
    zero = rl[rl.tgt == 0]
    para(f"Games with at least one target: {len(gp)} of {len(rl)} team games. Zero-target team games: {list(zero.wk)}. "
         f"Targets/game = {gp.tgt.sum()}/{len(gp)} = {gp.tgt.mean():.2f} (report's tgt_pg used all {len(rl)} team games as denominator = {gp.tgt.sum() / len(rl):.2f}). "
         f"Rec yds mean over games with targets = {gp.rec_yds.mean():.1f}; over all team games (zeros included) = {rl.rec_yds.mean():.1f}.")
    if nm == "J.Jefferson":
        para(f"Over 79.5: {(gp.rec_yds > 79.5).sum()} of {len(gp)} (with-target games) / of {len(rl)} (all team games); over 80.5: {(gp.rec_yds > 80.5).sum()}. "
             f"Receptions >=7 (over 6.5): {(gp.rec >= 7).sum()} of {len(gp)}.")
        if len(zero):
            para("Roster status for the zero-target week(s):")
            out.append(md(roster_status("Jefferson", "MIN", list(zero.wk) + [w for w in rl.wk if w not in list(zero.wk)][:2])))
    if nm == "T.Hockenson":
        para(f"Receptions <=4 (Under 4.5): {(gp.rec <= 4).sum()} of {len(gp)}; receptions >=5: {(gp.rec >= 5).sum()}.")
    if nm == "D.Kincaid":
        para(f"Over 36.5: {(gp.rec_yds > 36.5).sum()} of {len(gp)}; over 39.5: {(gp.rec_yds > 39.5).sum()}.")

# ---------- 3. Cook red zone ---------------------------------------------
h("## 3. James Cook red-zone audit")
cids = pid("J.Cook", "BUF", "rusher_player_id")
cr = p[(p.posteam == "BUF") & (p.rusher_player_id.isin(cids))]
cr_rush = cr[cr.rush == 1]
rz = cr_rush[cr_rush.yardline_100 <= 20]
i5 = cr_rush[cr_rush.yardline_100 <= 5]
para(f"**Definition used in the original report:** `yardline_100 <= 20` (red zone) and `yardline_100 <= 5` (labeled 'inside the 5'; this actually includes carries from exactly the 5-yard line). "
     f"Filter: `posteam=='BUF'`, `rush==1`, `rusher_player_id` = Cook's id {cids} (player-specific). Recomputed: red-zone carries = {len(rz)}, at-or-inside-5 = {len(i5)}. "
     f"Strictly inside the 5 (`yardline_100 < 5`) = {int((cr_rush.yardline_100 < 5).sum())}; strictly inside the 20 (`<20`) = {int((cr_rush.yardline_100 < 20).sum())}; "
     f"goal-to-go carries = {int((cr_rush.goal_to_go == 1).sum())}.")
team_rz = p[(p.posteam == "BUF") & (p.rush == 1) & (p.yardline_100 <= 20)]
team_rz5 = p[(p.posteam == "BUF") & (p.rush == 1) & (p.yardline_100 <= 5)]
para(f"Team-level comparison (raw `rush==1` flag count, no play_type or rusher-id restriction; may include penalty-nullified `no_play` rows with null rusher id): red-zone rush rows = {len(team_rz)}, at-or-inside-5 = {len(team_rz5)}. "
     f"Cook's {len(rz)}/{len(i5)} are therefore a subset of team totals, i.e. player-specific, not team-level. "
     f"Breakdown of team red-zone rushes by rusher: {team_rz.rusher_player_name.value_counts(dropna=False).to_dict()}.")
h("### Data-hygiene checks")
bufrun = p[(p.posteam == "BUF") & (p.rush == 1)]
dups_all = int(p.duplicated(subset=["game_id", "play_id"]).sum())
dups_buf = int(p[(p.home_team == "BUF") | (p.away_team == "BUF")].duplicated(subset=["game_id", "play_id"]).sum())
para(f"- Duplicate `(game_id, play_id)` rows: whole 2026 file = {dups_all}; BUF games = {dups_buf}.\n"
     f"- BUF `rush==1` rows with null `rusher_player_id` = {int(bufrun.rusher_player_id.isna().sum())} of {len(bufrun)}; null `rusher_player_name` = {int(bufrun.rusher_player_name.isna().sum())}.\n"
     f"- `qb_kneel==1` among BUF rush==1 rows = {int((bufrun.qb_kneel == 1).sum())}; kneels by anyone, BUF offense = {int(((p.posteam == 'BUF') & (p.qb_kneel == 1)).sum())}; "
     f"Cook rows with `qb_kneel==1` = {int((cr_rush.qb_kneel == 1).sum())}. (Kneel-downs carry the QB's rusher id and `rush==1` is 0 on them in nflverse; they are therefore not in these counts.)\n"
     f"- Cook rows with `rush==1` and `play_type=='no_play'` (penalty-nullified) = {int((cr_rush.play_type == 'no_play').sum())}; `rush==1` and `play_type=='run'` = {int((cr_rush.play_type == 'run').sum())}. "
     f"Original carry totals used `rush==1` without a play_type filter; the two agree if the no_play count is 0.\n"
     f"- Cook rush rows total (all field positions) = {len(cr_rush)}; with `fumble_lost==1` = {int((cr_rush.fumble_lost == 1).sum())}.")
kn = p[p.qb_kneel == 1]
sk = p[p.sack == 1]
nul = bufrun[bufrun.rusher_player_id.isna()]
para(f"- Verified flag semantics (whole 2026 file): `qb_kneel==1` rows = {len(kn)}, all with `rush==0`, `play_type=='qb_kneel'`, and non-null rusher id ({int(kn.rusher_player_id.notna().sum())}); so kneels never enter `rush==1` counts. "
     f"`sack==1` rows = {len(sk)}, all with `pass==1` and `pass_attempt==1` (pass_attempt includes sacks). "
     f"BUF `rush==1` rows with null `rusher_player_id` = {len(nul)}; all have play_type {nul.play_type.value_counts().to_dict()} (penalty-nullified plays) and null `rusher_player_name`; "
     f"they are excluded from every player count and from the 188-row share denominator by the `play_type=='run'` / non-null id filters, which is the intended treatment. "
     f"The `rusher` text field names: {nul.rusher.value_counts().to_dict()}.")
cols = ["game_id", "play_id", "rusher_player_id", "qtr", "down", "ydstogo", "yardline_100", "goal_to_go",
        "rushing_yards", "rush_touchdown", "qb_kneel", "play_type"]
rzp = rz[cols].sort_values(["game_id", "play_id"]).copy()
rzp["at_or_inside_5"] = np.where(rzp.yardline_100 <= 5, "Y", "")
h(f"### Underlying play records: Cook red-zone carries ({len(rzp)} rows)")
out.append(md(rzp, ".0f"))
para(f"Per-game red-zone carries: {rz.groupby('game_id').size().to_dict()}. Red-zone rush yards {rz.rushing_yards.sum():.0f}, rush TDs {int(rz.rush_touchdown.sum())}; "
     f"at-or-inside-5 yards {i5.rushing_yards.sum():.0f}, TDs {int(i5.rush_touchdown.sum())}.")

# ---------- 4. turnovers & QB hits ---------------------------------------
h("## 4. Turnover and QB-hit reconciliation")
para("**Definition used in the original report.** Giveaway = a row with `posteam==TEAM` and (`interception==1` or `fumble_lost==1`). "
     "Takeaway = a row with `defteam==TEAM` and the same flags. NO play_type filter was applied (so special-teams and any other row types are included), "
     "and each play is counted once even if it has both flags. Listed below event by event.")
tocols = ["game_id", "play_id", "qtr", "posteam", "defteam", "play_type", "interception", "fumble_lost", "desc"]
for t in TEAMS:
    g = p[(p.home_team == t) | (p.away_team == t)]
    ev = g[(g.interception == 1) | (g.fumble_lost == 1)].copy()
    ev["side"] = np.where(ev.posteam == t, "GIVEAWAY", "TAKEAWAY")
    ev["desc"] = ev["desc"].astype(str).str.slice(0, 110)
    ev = ev.sort_values(["side", "game_id", "play_id"])
    h(f"### {t} turnover events")
    gv = (ev.side == "GIVEAWAY").sum()
    tk = (ev.side == "TAKEAWAY").sum()
    para(f"Giveaways {gv}, takeaways {tk}, margin {tk - gv:+d}. Of these, rows with play_type not in {{pass, run}}: {int((~ev.play_type.isin(['pass','run'])).sum())}; "
         f"rows with both flags: {int(((ev.interception == 1) & (ev.fumble_lost == 1)).sum())}. "
         f"Interceptions thrown by {t}: {int(((ev.side=='GIVEAWAY')&(ev.interception==1)).sum())}; fumbles lost by {t}: {int(((ev.side=='GIVEAWAY')&(ev.fumble_lost==1)).sum())}.")
    out.append(md(ev[["side"] + tocols], ".0f"))
h("### Fumble-event verification (recovering team recorded in the file)")
fe = p[(p.fumble_lost == 1) & (((p.home_team.isin(TEAMS)) | (p.away_team.isin(TEAMS))))].copy()
fe = fe[fe.posteam.isin(TEAMS) | fe.defteam.isin(TEAMS)]
fe["fumbled_by_team"] = fe.fumbled_1_team
fe["recovered_by_team"] = fe.fumble_recovery_1_team
fe["recovery_is_opponent_of_fumbler"] = np.where(fe.fumbled_by_team.notna() & fe.recovered_by_team.notna(),
                                                 np.where(fe.fumbled_by_team != fe.recovered_by_team, "yes", "NO"), "n/a (null field)")
para("For each `fumble_lost==1` event involving BUF or MIN: the fumbling team (`fumbled_1_team`) and recovering team (`fumble_recovery_1_team`) fields. "
     "A fumble is a genuine turnover only if recovery team differs from fumbling team. Rows with null fields need manual review.")
out.append(md(fe[["game_id", "play_id", "play_type", "posteam", "fumbled_by_team", "recovered_by_team", "recovery_is_opponent_of_fumbler"]].sort_values(["game_id", "play_id"]), ".0f"))
flag_ids = [("2026_03_LAC_BUF", 3173), ("2026_04_MIA_MIN", 1684), ("2026_03_LAC_BUF", 63)]
for gid, pid_ in flag_ids:
    r = p[(p.game_id == gid) & (p.play_id == pid_)]
    if len(r):
        para(f"Full description, {gid} play {pid_}: {r.iloc[0].desc}")
h("### Defensive QB-hit rate (and sack rate): exact definition")
for t in TEAMS:
    Dd = base[base.defteam == t]
    dp = Dd[Dd["pass"] == 1]
    n_all = len(dp)
    n_nan = int(dp.qb_hit.isna().sum())
    num = float(dp.qb_hit.sum())
    att_only = dp[dp.pass_attempt == 1]
    para(f"**{t} defense.** Denominator = opponent offense rows with `defteam=='{t}'`, `play_type in {{pass,run}}`, `epa` not null, `pass==1` "
         f"(all dropbacks: attempts + sacks + scrambles) = {n_all} rows. Numerator = sum of `qb_hit` = {num:.0f}. `qb_hit` null in {n_nan} of those rows; "
         f"pandas `mean()` skips nulls, so the reported rate = {num:.0f} / {n_all - n_nan} = {num / (n_all - n_nan):.3f} "
         f"(rate treating nulls as 0 over all {n_all} = {num / n_all:.3f}). Sack rate = sum(`sack`) {int(dp.sack.sum())} / {n_all} = {dp.sack.mean():.3f}. "
         f"Sensitivity: QB hits over attempts only ({len(att_only)} rows) = {att_only.qb_hit.sum():.0f}/{att_only.qb_hit.notna().sum()} = {att_only.qb_hit.mean():.3f}. "
         f"`qb_hit` is a play-level flag (it includes sacks and hits on throws); it is not a pressure flag and was never relabeled as pressure rate. "
         f"No 2026 pressure field exists in this file (`was_pressure` absent).")

# ---------- 5. provenance --------------------------------------------------
h("## 5. Data provenance (from the files actually used)")
sch = pd.DataFrame({"column": p.columns, "dtype": [str(x) for x in p.dtypes]})
para(f"`play_by_play_2026.parquet`: {len(p):,} rows x {p.shape[1]} columns; seasons {sorted(p.season.unique().tolist())}; "
     f"season_type {p.season_type.value_counts().to_dict()}; weeks {sorted(int(x) for x in p.week.unique())}; games {p.game_id.nunique()}; "
     f"game_date min {p.game_date.min()} max {p.game_date.max()}.")
para(f"`roster_weekly_2026.csv`: {len(ro):,} rows x {ro.shape[1]} columns; seasons {sorted(ro.season.unique().tolist())}; weeks {sorted(int(x) for x in ro.week.unique())}. "
     f"Columns: {', '.join(ro.columns)}.")
needed = ["epa", "success", "pass", "rush", "sack", "qb_hit", "qb_scramble", "qb_kneel", "interception", "fumble_lost", "yardline_100",
          "goal_to_go", "rusher_player_id", "receiver_player_id", "passer_player_id", "pass_attempt", "complete_pass", "receiving_yards",
          "rushing_yards", "passing_yards", "was_pressure", "offense_players", "defense_players", "n_offense", "pass_rusher", "xpass", "cpoe", "wp"]
chk = pd.DataFrame({"column": needed, "in_file": [c in p.columns for c in needed],
                    "non_null_share": [round(float(p[c].notna().mean()), 3) if c in p.columns else None for c in needed]})
para("Columns used or requested, presence and non-null share (full 2026 file):")
out.append(md(chk))
para("Full PBP schema (name:dtype), all columns:")
out.append("```\n" + ", ".join(f"{a}:{b}" for a, b in zip(sch.column, sch.dtype)) + "\n```\n")

h("## 8. Schedule row (games.csv)")
_g = pd.read_csv(f"{D}/games.csv", low_memory=False)
_r = _g[(_g.season == 2026) & (_g.week == 9) & (_g.home_team == "MIN") & (_g.away_team == "BUF")]
para(f"games.csv rows {len(_g)}; 2026 rows {int((_g.season == 2026).sum())}. BUF@MIN wk9 row (spread_line, total_line, moneylines as in file):")
out.append(md(_r[[c for c in ["game_id", "gameday", "gametime", "spread_line", "total_line", "home_moneyline", "away_moneyline", "roof"] if c in _r.columns]], ".1f"))

open(OUT, "w").write("\n".join(out))
print("wrote", OUT, "chars", sum(len(x) for x in out))
