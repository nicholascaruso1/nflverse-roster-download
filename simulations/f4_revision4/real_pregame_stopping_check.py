"""Outcome-blind infrastructure check of f4_stopping_rule.py on the REAL 2026 prospective pregame partition. Reads game_features only
(records + f4 flag; no outcome columns exist in it). Not an evaluation."""
import sys, glob, hashlib, json, datetime as dt
import numpy as np, pandas as pd
import paths; import f4_stopping_rule as SR
REPO = str(paths.REPO)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
pf = glob.glob(f"{paths.DERIVED}/game_features/*prospective*.parquet"); assert len(pf) == 1; pf = pf[0]
man = pd.read_csv(f"{REPO}/research_ledger/partition_manifest.csv"); mrow = man[man.relative_path.str.endswith(pf.split("/")[-1])]
g = pd.read_parquet(pf); FORBID = {"home_score", "away_score", "result", "total", "winner", "home_win", "outcome"}
assert not (FORBID & set(c.lower() for c in g.columns)), "outcome column present"
g = g[(g.game_type == "REG") & (g.season == 2026)].sort_values(["week", "gameday", "game_id"]).reset_index(drop=True)
Wh, Lh, Th, Wa, La, Ta = (g[c].to_numpy(int) for c in ["home_season_wins", "home_season_losses", "home_season_ties", "away_season_wins", "away_season_losses", "away_season_ties"])
Gh, Ga = Wh + Lh + Th, Wa + La + Ta
elig = (Gh >= 1) & (Ga >= 1)
f4 = elig & (Wa == Lh) & (La == Wh) & (Ta == Th)
assert (f4 == g.f4_mirrored_current_records.to_numpy(bool)).all(), "F4 flag mismatch vs partition"
g, Wh, Lh, Th, Wa, La, Ta, Gh, Ga, f4 = [x[elig] if not isinstance(x, pd.DataFrame) else x[elig].reset_index(drop=True) for x in (g, Wh, Lh, Th, Wa, La, Ta, Gh, Ga, f4)]
ids = SR.stratum_ids(Gh, Ga, Wh, Th, Wa, Ta)
wk = g.week.to_numpy(); weeks = sorted(set(wk)); we = np.array([np.where(wk == w)[0].max() for w in weeks])
cnt = SR.cumulative_on_support(ids, f4, we, SR.TOL)
# INDEPENDENT brute force (pandas, no module functions): at each week-end recompute everything from scratch
from fractions import Fraction
def brute(upto_week, tol=20):     # independent: exact rational arithmetic, documented right-closed bins, plain pandas
    dd = [Fraction(int(2*(a-b)+(c-e)), int(2*(G+8))) for a, b, c, e, G in zip(Wh, Wa, Th, Ta, Gh)]
    cuts = [Fraction(-3, 20), Fraction(-1, 20), Fraction(1, 20), Fraction(3, 20)]
    db = [sum(1 for c in cuts if x > c) for x in dd]
    s = pd.DataFrame({"w": wk, "f4": f4, "isq": Gh == Ga, "gc": np.select([Gh < 3, Gh < 5, Gh < 9], [0, 1, 2], 3), "db": db}); s = s[(s.w <= upto_week) & s.isq]
    t = s.groupby(["gc", "db"]).f4.agg(n1="sum", n="size"); t["n0"] = t.n - t.n1; ok = t[(t.n1 >= 1) & (t.n0 >= tol)]
    return int(ok.n1.sum()), len(ok)
rows = []
for j, w in enumerate(weeks):
    b, nb = brute(w); n1, n0 = SR.stratum_counts(ids[:we[j] + 1], f4[:we[j] + 1]); ns = int(SR.supported(n1, n0).sum())
    rows.append({"week": int(w), "games_to_date": int(we[j] + 1), "eligible_games_wk": int((wk == w).sum()), "F4_to_date": int(f4[:we[j] + 1].sum()), "on_support_F4_cum": int(cnt[j]),
                 "supported_strata": ns, "brute_on_support": b, "brute_strata": nb, "match": (b == cnt[j]) and (nb == ns), "status": "AT/ABOVE 188" if cnt[j] >= 188 else "below 188"})
df = pd.DataFrame(rows); print(df.to_string(index=False))
j = SR.first_week_reaching(cnt); sup_hash = SR.support_hash(g.game_id.to_numpy(), ids, f4)
prov = {"run_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "partition_file": pf.split("/")[-1], "partition_sha256_computed": sha(pf), "partition_sha256_manifest": mrow.sha256.iloc[0] if len(mrow) else None,
        "stopping_rule_sha256": sha(SR.__file__), "check_script_sha256": sha(__file__), "eligible_weeks": [int(w) for w in weeks],
        "n_eligible_games": int(len(g)), "n_F4": int(f4.sum()), "first_crossing": None if j < 0 else int(weeks[j]), "all_match": bool(df.match.all()), "support_hash_current_support_list": sup_hash,
        "latest_gameday_in_partition": str(g.gameday.max()), "outcome_columns_loaded": False}
print(json.dumps(prov, indent=1)); df.to_csv(paths.OUT / "real_pregame_stopping_check.csv", index=False); json.dump(prov, open(paths.OUT / "real_pregame_stopping_check_provenance.json", "w"), indent=1)
