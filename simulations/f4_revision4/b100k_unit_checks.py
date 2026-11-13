import sys, time, itertools; import paths
import numpy as np, f4_permutation_test as P, f4_stopping_rule as SR
rng = np.random.default_rng(5)
# (1) exact enumeration on a toy problem (2 strata) vs MC B=100k
v1 = rng.normal(size=7); v2 = rng.normal(size=6); ids = np.r_[np.zeros(7, int), np.ones(6, int)]; f4 = np.r_[[1,1,0,0,0,0,0],[1,0,0,0,0,0]].astype(bool); rt = np.r_[v1, v2]
class Z: pass
prep = {"groups": [v1, v2], "n1s": [2, 1], "c": 2 * v1.mean() + v2.mean()}; prep["t_obs"] = float(v1[:2].sum() + v2[:1].sum() - prep["c"])
ts = [v1[list(a)].sum() + v2[list(b)].sum() - prep["c"] for a in itertools.combinations(range(7), 2) for b in itertools.combinations(range(6), 1)]
pex = float((np.abs(ts) >= abs(prep["t_obs"]) - 1e-12).mean()); r = P.permutation_test(prep, 100000, 11)
print("exact enumeration p", round(pex, 5), "| MC(B=1e5) p", round(r["p"], 5), "| exact Var", round(float(np.var(ts)), 5), "MC var", round(r["tstar_sd"] ** 2, 5), "closed form", round(P.exact_null_variance(prep), 5))
# (2) reproducibility + observed statistic independent of seed/B
a = P.permutation_test(prep, 100000, 11); b = P.permutation_test(prep, 100000, 11); c = P.permutation_test(prep, 20000, 12)
print("same seed identical:", a["p"] == b["p"] and a["tstar_sd"] == b["tstar_sd"], "| t_obs invariant:", a["t_obs"] == c["t_obs"] == prep["t_obs"])
