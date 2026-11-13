import sys, time, resource, json; import paths
import numpy as np, f4_type1_sim as S, f4_stopping_rule as SR, f4_rev4_sim as V, f4_permutation_test as P
rng = np.random.default_rng(99); seasons = [S.SEASONS[i % 5] for i in range(10)]
o = V.simulate2(1, seasons, .6, .2, .003, 0., rng, "latent"); d = S.features(o); sw = o["sw"]; we = np.r_[np.where(np.diff(sw) != 0)[0], len(sw) - 1]
f4 = o["f4"][0]; ids = SR.stratum_ids(o["Gh"], o["Ga"], o["Wh"][0], o["Th"][0], o["Wa"][0], o["Ta"][0]); cnt = SR.cumulative_on_support(ids, f4, we); j = SR.first_week_reaching(cnt); e = we[j] + 1
rt = P.centred_residuals(o["h"][0][:e], d[0][:e], sw[:e], 0.35086712927793096, 3.8959057735807017); prep = P.prepare(rt, ids[:e], f4[:e]); t_before = prep["t_obs"]
t0 = time.time(); a = P.permutation_test(prep, 100000, 424242, keep=True); t1 = time.time(); b = P.permutation_test(prep, 100000, 424242, keep=True); c = P.permutation_test(prep, 100000, 424243)
sup_before = (prep["n_on_support_f4"], prep["n_strata"], prep["strata"])
out = {"identical_p_same_seed": a["p"] == b["p"], "identical_full_T*_vector_same_seed": bool(np.array_equal(a["tstar"], b["tstar"])), "p_seed_424242": a["p"], "p_seed_424243": c["p"], "p_difference_within_MC": abs(a["p"] - c["p"]) < 5 * np.sqrt(.25 / 1e5) * 1.0 + 0.01,
       "t_obs_unchanged_by_permutation_runs": prep["t_obs"] == t_before == a["t_obs"], "support_unchanged": sup_before == (prep["n_on_support_f4"], prep["n_strata"], prep["strata"]), "seconds_per_100k": round(t1 - t0, 2),
       "tstar_quantiles_1_25_50_75_99": np.percentile(a["tstar"], [1, 25, 50, 75, 99]).round(4).tolist(), "tstar_sd": a["tstar_sd"], "exact_sd": float(np.sqrt(P.exact_null_variance(prep))), "peak_rss_MB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024}
out = {k: (bool(v) if isinstance(v, (np.bool_, bool)) else v) for k, v in out.items()}; print(json.dumps(out)); open(paths.OUT / "b100k_repro_check.json", "w").write(json.dumps(out, indent=1))
