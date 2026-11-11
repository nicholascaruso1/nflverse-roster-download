#!/usr/bin/env python3
"""Week 9 BUF@MIN postmortem: regenerates every postgame figure from the postgame nflverse PBP.
Usage: python3 -I postmortem.py <path to play_by_play_2026.parquet or .csv>
Pregame/Lock 2 records are NOT read here; they are frozen documents. This only computes results."""
import sys
import pandas as pd

f = sys.argv[1]
p = pd.read_csv(f, low_memory=False) if f.endswith(".csv") else pd.read_parquet(f)
g = p[p.game_id == "2026_09_BUF_MIN"].copy()
print("rows", len(g), "dup (game_id,play_id)", int(g.duplicated(["game_id", "play_id"]).sum()))
print("final home MIN / away BUF:", int(g.home_score.iloc[0]), int(g.away_score.iloc[0]), "total", int(g.total.iloc[0]), "result(home-away)", int(g.result.iloc[0]))

pa = g[g["pass"] == 1]
print("\n== Passing (dropbacks include sacks; attempts = pass_attempt==1 & sack!=1) ==")
for (t, n), x in pa.groupby(["posteam", "passer_player_name"]):
    allrows = g[(g.passer_player_name == n) & (g.posteam == t)]
    att = int(((allrows.pass_attempt == 1) & (allrows.sack != 1)).sum())  # includes qb_spike rows (pass==0, pass_attempt==1), as the official box does
    print(f"{t} {n}: dropbacks {len(x)}, att {att}, cmp {int(x.complete_pass.sum())}, yds {x.passing_yards.sum():.0f}, "
          f"sacks {int(x.sack.sum())}, int {int(x.interception.sum())}, td {int(x.pass_touchdown.sum())}")

print("\n== Rushing (rush==1 designed runs) ==")
ru = g[g.rush == 1]
print(ru.groupby(["posteam", "rusher_player_name"]).agg(car=("rush", "size"), yds=("rushing_yards", "sum"), td=("rush_touchdown", "sum")).to_string())
al = g[(g.rusher_player_name == "J.Allen") & (g.qb_kneel != 1)]
print("Allen rush yards incl. scrambles (kneels excluded):", al.rushing_yards.sum(), "on", len(al), "carries")
buf = g[(g.posteam == "BUF")]
print("BUF team rush reconciliation: designed", int((buf.rush == 1).sum()), "+ kneels", int((buf.qb_kneel == 1).sum()),
      "+ scrambles", int((buf.qb_scramble == 1).sum()), "(official team box: 44 rush plays)")
c = ru[ru.rusher_player_name == "J.Cook"]
print("Cook red zone (<=20):", int((c.yardline_100 <= 20).sum()), " at/inside 5 (<=5):", int((c.yardline_100 <= 5).sum()))

print("\n== Receiving (play_type=='pass', receiver id present) ==")
re = g[(g.play_type == "pass") & g.receiver_player_name.notna()]
print(re.groupby(["posteam", "receiver_player_name"]).agg(tgt=("pass", "size"), rec=("complete_pass", "sum"), yds=("receiving_yards", "sum"), td=("pass_touchdown", "sum")).to_string())

print("\n== Team efficiency, same filters as the audit (pass/run, epa not null, posteam not null) ==")
b = g[g.play_type.isin(["pass", "run"]) & g.epa.notna() & g.posteam.notna()]
for t in ["BUF", "MIN"]:
    o = b[b.posteam == t]
    pp, rr = o[o["pass"] == 1], o[o.rush == 1]
    print(f"{t} offense: n {len(o)}, EPA/play {o.epa.mean():.3f}, SR {o.success.mean():.3f}, pass EPA {pp.epa.mean():.3f}, rush EPA {rr.epa.mean():.3f}, "
          f"sacks taken {int(o.sack.sum())}/{len(pp)} dropbacks, QB hits taken {int(pp.qb_hit.sum())}/{len(pp)} = {pp.qb_hit.mean():.3f}")

print("\n== Turnovers (interception==1 or fumble_lost==1, no play_type filter) ==")
to = g[(g.interception == 1) | (g.fumble_lost == 1)]
print(to[["qtr", "posteam", "play_type", "interception", "fumble_lost", "desc"]].to_string())

print("\n== Score by drive context ==")
print(g.groupby("qtr")[["total_home_score", "total_away_score"]].max())

print("\n== QB changes (MIN) ==")
m = g[(g.posteam == "MIN") & (g["pass"] == 1)]
print(m.groupby(["passer_player_name", "qtr"]).size().unstack(fill_value=0))
last_w = m[m.passer_player_name == "C.Wentz"].iloc[-1]
first_b = m[m.passer_player_name == "M.Brosmer"].iloc[0]
print("Wentz last dropback: Q%d, %d s left;  Brosmer first dropback: Q%d, %d s left, score diff (MIN) %s"
      % (last_w.qtr, last_w.game_seconds_remaining, first_b.qtr, first_b.game_seconds_remaining, first_b.score_differential))
inj = g[g.desc.str.contains("injur", case=False, na=False) & g.desc.str.contains("Wentz|Brosmer", na=False)]
print("PBP injury text naming Wentz/Brosmer:", len(inj))
