"""AUTHORIZED, RESTRICTED outcome-touching step: baseline fit on DISCOVERY (1999-2018) NON-F4 regular-season games only.
Outcome fields joined: home_score, away_score (to form h: home win 1 / tie .5 / loss 0) for the selected non-F4 game ids ONLY.
No F4 outcome is read. No validation/holdout/prospective outcome is read. No F4 test is run."""
import sys, glob, hashlib, json, datetime as dt
import numpy as np, pandas as pd
import os; from pathlib import Path
REPO = str(Path(os.environ.get("NFL_REPO_ROOT", Path(__file__).resolve().parents[2])).resolve()); sys.path.insert(0, REPO + "/scripts"); import f4_stopping_rule as SR
GAMES = os.environ["NFLVERSE_GAMES_CSV"]   # REQUIRED: authorized outcome source (home_score, away_score for discovery non-F4 games only)
OUTDIR = Path(os.environ.get("F4_OUT_DIR", Path(__file__).resolve().parent)); OUTDIR.mkdir(parents=True, exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
pf = glob.glob(os.environ.get("NFL_DERIVED_DIR", REPO + "/derived/v1.1") + "/game_features/*discovery*.parquet"); assert len(pf) == 1; pf = pf[0]
g = pd.read_parquet(pf); assert set(g.split) == {"discovery"} and g.season.between(1999, 2018).all()
n_all = len(g); g = g[g.game_type == "REG"]; n_reg = len(g)
Wh, Lh, Th, Wa, La, Ta = (g[c].to_numpy(int) for c in ["home_season_wins", "home_season_losses", "home_season_ties", "away_season_wins", "away_season_losses", "away_season_ties"])
Gh, Ga = Wh + Lh + Th, Wa + La + Ta; elig = (Gh >= 1) & (Ga >= 1); f4 = elig & (Wa == Lh) & (La == Wh) & (Ta == Th)
assert (f4 == g.f4_mirrored_current_records.to_numpy(bool)).all()
sel = elig & ~f4; gs = g[sel].copy(); gs["d"] = SR.shrunk_diff(Wh[sel], Th[sel], Gh[sel], Wa[sel], Ta[sel], Ga[sel])
excl = {"discovery_partition_rows": n_all, "REG_rows": n_reg, "excluded_not_eligible_(a_team_has_0_games)": int((~elig).sum()), "excluded_F4_games": int(f4.sum()), "fit_sample_rows": int(sel.sum())}
ids = set(gs.game_id)                                           # outcomes read ONLY for these ids
o = pd.read_csv(GAMES, usecols=["game_id", "home_score", "away_score"]); o = o[o.game_id.isin(ids)]
assert not (o.game_id.isin(g[f4].game_id)).any() and len(o) == len(gs)
gs = gs.merge(o, on="game_id"); assert gs.home_score.notna().all() and gs.away_score.notna().all()
gs["h"] = np.where(gs.home_score > gs.away_score, 1.0, np.where(gs.home_score == gs.away_score, 0.5, 0.0))
d, h = gs.d.to_numpy(), gs.h.to_numpy(); X = np.c_[np.ones_like(d), d]; b = np.zeros(2); L = lambda x: 1 / (1 + np.exp(-x))
for it in range(100):
    mu = L(X @ b); Wt = mu * (1 - mu); step = np.linalg.solve(X.T @ (X * Wt[:, None]), X.T @ (h - mu)); b = b + step
    if np.abs(step).max() < 1e-12: break
mu = L(X @ b); Wt = mu * (1 - mu); bread = np.linalg.inv(X.T @ (X * Wt[:, None]))
sw = (gs.season.astype(str) + "_" + gs.week.astype(str)).to_numpy(); sc = X * (h - mu)[:, None]
meat = sum(np.outer(sc[sw == k].sum(0), sc[sw == k].sum(0)) for k in np.unique(sw)); rob = np.sqrt(np.diag(bread @ meat @ bread))
ll = -np.mean(h * np.log(mu) + (1 - h) * np.log(1 - mu)); ll0 = -np.mean(h * np.log(h.mean()) + (1 - h) * np.log(1 - h.mean()))
gs["fit"] = mu; gs["dec"] = pd.qcut(gs.d, 10, labels=False, duplicates="drop"); cal = gs.groupby("dec").agg(n=("h", "size"), mean_d=("d", "mean"), mean_h=("h", "mean"), mean_fit=("fit", "mean")).round(4)
out = {"run_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "k_shrinkage": SR.K, "sample": excl, "ties_in_fit_sample": int((h == 0.5).sum()), "seasons": [int(gs.season.min()), int(gs.season.max())],
       "coefficients": {"b0_intercept": float(b[0]), "b1_d": float(b[1])}, "std_err_robust_season_week_clustered": rob.tolist(), "irls_iterations": it + 1, "converged": bool(np.abs(step).max() < 1e-12),
       "diagnostics": {"mean_h": float(h.mean()), "mean_fitted": float(mu.mean()), "logloss": float(ll), "logloss_intercept_only": float(ll0), "d_min_max": [float(d.min()), float(d.max())]},
       "hashes": {"discovery_game_features_partition_sha256": sha(pf), "outcome_source_sha256_games.csv": sha(GAMES), "stopping_rule_module_sha256": sha(SR.__file__), "fit_script_sha256": sha(__file__),
                  "fit_sample_game_id_list_sha256": hashlib.sha256("\n".join(sorted(gs.game_id)).encode()).hexdigest()},
       "outcome_scope": "home_score,away_score for discovery non-F4 eligible REG games only; no F4, validation, holdout or prospective outcomes read; no F4 test run"}
json.dump(out, open(OUTDIR / "baseline_coefficients_k8.json", "w"), indent=1); cal.to_csv(OUTDIR / "calibration_deciles.csv")
print(json.dumps(out, indent=1)); print(cal)
