"""Discovery-style procedure (in-sample baseline refit inside every permutation) at ~20-season size. Simulated outcomes only."""
import sys, json, os, time
import numpy as np
import f4_type1_sim as S, f4_refit_sim as RF, f4_rev4_sim as V
import paths
R, B = int(sys.argv[1]), int(sys.argv[2]); mode_list = sys.argv[3].split(","); SEED = 20261130; rng = np.random.default_rng(SEED)
for mode in mode_list:
    sd = {"lat060": .60}.get(mode, 0.0); m = "latent" if mode.startswith("lat") else mode; hfa = 0.20 if mode == "lat060" else 0.15
    seasons = [S.SEASONS[i % 5] for i in range(20)]; t0 = time.time(); ps = []; nf = []
    for c in range(0, R, 50):
        o = V.simulate2(min(50, R - c), seasons, sd, hfa, 0.003, 0.0, rng, m); d_all = S.features(o)
        for r in range(o["h"].shape[0]):
            ids = S.strata_ids(o, d_all[r], o["f4"][r], r); nf.append(int(o["f4"][r].sum()))
            p = RF.refit_test(o["h"][r], d_all[r], o["f4"][r], o["sw"], ids, B, rng)
            if not np.isnan(p): ps.append(p)
    a = np.array(ps); rate = float((a < .05).mean())
    rec = {"null": mode, "n_games": int(o["h"].shape[1]), "mean_F4": float(np.mean(nf)), "R": len(a), "B": B, "refit_type1": rate, "mc_se": float(np.sqrt(rate * (1 - rate) / len(a))), "secs": round(time.time() - t0)}
    print(json.dumps(rec), flush=True); open(paths.OUT / "refit20.jsonl", "a").write(json.dumps(rec) + "\n")
