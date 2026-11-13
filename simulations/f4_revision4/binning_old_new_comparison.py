"""Outcome-blind comparison of the superseded float-digitize binning vs the exact right-closed binning on real pregame partitions
(F4 labels, stratum assignments, support counts). No outcome data."""
import glob, hashlib, importlib.util, json
import numpy as np, pandas as pd
import paths, f4_stopping_rule as NEW
spec = importlib.util.spec_from_file_location("old", str(paths.HERE / "results" / "SUPERSEDED_f4_stopping_rule_v1_digitize.py")); OLD = importlib.util.module_from_spec(spec); spec.loader.exec_module(OLD)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest(); rows = []
for sp in ("discovery", "validation", "holdout", "prospective"):
    f = glob.glob(f"{paths.DERIVED}/game_features/*{sp}*.parquet")[0]; g = pd.read_parquet(f); g = g[g.game_type == "REG"].sort_values(["season", "week", "gameday", "game_id"]).reset_index(drop=True)
    Wh, Lh, Th, Wa, La, Ta = (g[c].to_numpy(int) for c in ["home_season_wins", "home_season_losses", "home_season_ties", "away_season_wins", "away_season_losses", "away_season_ties"])
    Gh, Ga = Wh + Lh + Th, Wa + La + Ta; el = (Gh >= 1) & (Ga >= 1); f4 = el & (Wa == Lh) & (La == Wh) & (Ta == Th)
    assert (f4 == g.f4_mirrored_current_records.to_numpy(bool)).all()
    Wh, Lh, Th, Wa, La, Ta, Gh, Ga, f4 = (x[el] for x in (Wh, Lh, Th, Wa, La, Ta, Gh, Ga, f4)); g = g[el].reset_index(drop=True); el = np.ones(len(g), bool)   # eligible games only (both teams >= 1 completed game)
    d = NEW.shrunk_diff(Wh, Th, Gh, Wa, Ta, Ga); io = OLD.stratum_ids(Gh, Ga, d); inew = NEW.stratum_ids(Gh, Ga, Wh, Th, Wa, Ta)
    # support is evaluated per evaluation sample; here pooled sample = the whole split (and per season for the historical splits as 5-season-like checks are not needed)
    so, sn = OLD.on_support_mask(io, f4) & f4, NEW.on_support_mask(inew, f4) & f4
    n1o, n0o = OLD.stratum_counts(io, f4); n1n, n0n = NEW.stratum_counts(inew, f4)
    rows.append({"split": sp, "REG_games": len(g), "eligible_equalG": int((el & (Gh == Ga)).sum()), "F4_labels": int(f4.sum()), "F4_labels_match_partition_flag": True,
                 "games_with_changed_stratum": int((io != inew).sum()), "F4_games_with_changed_stratum": int(((io != inew) & f4).sum()), "on_support_F4_old": int(so.sum()), "on_support_F4_new": int(sn.sum()),
                 "supported_strata_old": int(OLD.supported(n1o, n0o).sum()), "supported_strata_new": int(NEW.supported(n1n, n0n).sum()), "on_support_F4_set_identical": bool((so == sn).all()), "partition_sha256": sha(f)})
    if sp == "prospective":
        wk = g.week.to_numpy(); we = np.array([np.where(wk == w)[0].max() for w in sorted(set(wk))]); co = OLD.cumulative_on_support(io, f4, we); cn = NEW.cumulative_on_support(inew, f4, we)
        rows[-1]["weekly_cumulative_on_support_identical"] = bool((co == cn).all())
df = pd.DataFrame(rows); print(df.drop(columns="partition_sha256").to_string(index=False))
df.to_csv(paths.OUT / "binning_old_new_comparison.csv", index=False)
json.dump({"old_module_sha256": sha(str(paths.HERE / "results" / "SUPERSEDED_f4_stopping_rule_v1_digitize.py")), "new_module_sha256": sha(NEW.__file__)}, open(paths.OUT / "binning_old_new_module_hashes.json", "w"), indent=1)
