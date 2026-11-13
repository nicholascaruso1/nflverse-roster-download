"""Full-scale (B=100,000) execution/calibration check on SIMULATED outcomes only. Usage: b100k_calibration.py MODE COEFS(sim|real) R SEED"""
import sys, json, time, warnings; import paths
import numpy as np, f4_type1_sim as S, f4_stopping_rule as SR, f4_rev4_sim as V, f4_permutation_test as P
warnings.simplefilter("error", RuntimeWarning)  # numerical warnings must surface
mode, cm, R, SEED = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]); B = 100_000; tol = 20
sd = {"lat060": .60}.get(mode, 0.0); m = "latent" if mode.startswith("lat") else mode; hfa = .20 if mode == "lat060" else .15
rng = np.random.default_rng(SEED); seasons = [S.SEASONS[i % 5] for i in range(10)]
tr = V.simulate2(8, S.SEASONS, sd, hfa, .003, 0., rng, m); b = S.fit_frac_logit(S.features(tr).ravel(), tr["h"].ravel(), (~tr["f4"]).ravel())
if cm == "real": b = np.array([0.35086712927793096, 3.8959057735807017])
o = V.simulate2(R, seasons, sd, hfa, .003, 0., rng, m); d = S.features(o); sw = o["sw"]; we = np.r_[np.where(np.diff(sw) != 0)[0], len(sw) - 1]
rec = []; t0 = time.time(); fails = []
for r in range(R):
    f4 = o["f4"][r]; ids = SR.stratum_ids(o["Gh"], o["Ga"], o["Wh"][r], o["Th"][r], o["Wa"][r], o["Ta"][r]); cnt = SR.cumulative_on_support(ids, f4, we, tol); j = SR.first_week_reaching(cnt)
    if j < 0: fails.append(r); continue
    e = we[j] + 1; rt = P.centred_residuals(o["h"][r][:e], d[r][:e], sw[:e], b[0], b[1]); prep = P.prepare(rt, ids[:e], f4[:e], tol)
    res = P.permutation_test(prep, B, SEED * 1000 + r)
    # consistency with the (independent) B=199 implementation used in the simulations: support, strata, effective size must be identical
    _, nos, nst, eff = V.perm2(rt, ids[:e], f4[:e], 199, np.random.default_rng(1), tol)
    rec.append((res["p"], res["tstar_sd"] / np.sqrt(P.exact_null_variance(prep)), res["tstar_mean"], prep["n_on_support_f4"] == nos and prep["n_strata"] == nst and abs(prep["eff_size"] - eff) < 1e-9, prep["n_on_support_f4"]))
a = np.array(rec, float); p = a[:, 0]; rej = float((p < .05).mean())
out = {"mode": mode, "coefs": cm, "b": b.tolist(), "R": len(p), "B": B, "seed": SEED, "not_reached": len(fails), "reject_rate_alpha05": rej, "mc_se": float(np.sqrt(rej * (1 - rej) / len(p))),
       "p_deciles": np.percentile(p, [10, 20, 30, 40, 50, 60, 70, 80, 90]).round(3).tolist(), "p_min": float(p.min()), "frac_p_lt_0.10": float((p < .10).mean()),
       "tstar_sd_over_exact_sd_mean_min_max": [float(a[:, 1].mean()), float(a[:, 1].min()), float(a[:, 1].max())], "tstar_mean_abs_max": float(np.abs(a[:, 2]).max()),
       "support_consistency_with_B199_impl_all": bool(a[:, 3].all()), "on_support_F4_mean": float(a[:, 4].mean()), "secs_total": round(time.time() - t0), "secs_per_test": round((time.time() - t0) / len(p), 2), "numerical_warnings": 0}
print(json.dumps(out), flush=True); open(paths.OUT / "b100k_results.jsonl", "a").write(json.dumps(out) + "\n")
