"""Frozen-algorithm implementation of the F4 stratified residual permutation test (full scale, B = 100,000 in the protocol).

Algorithm (all inputs fixed before outcomes are joined except h):
 1. residual r = h - logistic(b0 + b1*d) with FROZEN (b0, b1); centre r by season-week mean over ALL eligible games to date -> r~.
 2. strata ids (f4_stopping_rule.stratum_ids); on-support strata: >=1 F4 and >= TOL non-F4 games (pooled to date).
 3. T = sum of r~ over on-support F4 games - c,  c = sum_s n1_s * mean_s(r~).
 4. Null: within each supported stratum choose n1_s of N_s games uniformly at random as 'F4' (label permutation). T* analogous.
 5. p = (1 + #{|T*| >= |T|}) / (1 + B), two-sided. Reproducible: block b (size BLOCK) uses default_rng(SeedSequence(seed).spawn(nblocks)[b]).
Implementation: T* = sum_s [sum of the first n1_s entries of a random permutation of r~ in stratum s] - c  (identical distribution to relabelling).
"""
import numpy as np
import f4_stopping_rule as SR
BLOCK = 5000
logistic = lambda x: 1 / (1 + np.exp(-x))

def centred_residuals(h, d, sw, b0, b1):
    r = h - logistic(b0 + b1 * d); return r - (np.bincount(sw, weights=r) / np.maximum(np.bincount(sw), 1))[sw]

def prepare(rt, ids, f4, tol=SR.TOL):
    """Deterministic (no RNG, no outcome beyond rt). Returns support selection, observed statistic, counts."""
    ok = ids >= 0; n1, n0 = SR.stratum_counts(ids, f4); sup = SR.supported(n1, n0, tol)
    if not sup.any(): return None
    sel = ok & sup[np.where(ok, ids, 0)]; strata = [s for s in range(SR.NSTRATA) if sup[s]]
    groups = [rt[sel & (ids == s)] for s in strata]; n1s = [int(n1[s]) for s in strata]
    c = sum(n * v.mean() for n, v in zip(n1s, groups)); t_obs = float(rt[sel & f4].sum() - c)
    return {"groups": groups, "n1s": n1s, "c": float(c), "t_obs": t_obs, "n_on_support_f4": int((sel & f4).sum()), "n_strata": len(strata),
            "eff_size": float(sum(n * (len(v) - n) / len(v) for n, v in zip(n1s, groups))), "strata": strata}

def tstar_block(prep, size, rng):
    t = np.zeros(size)
    for v, n in zip(prep["groups"], prep["n1s"]):
        M = np.tile(v, (size, 1)); rng.permuted(M, axis=1, out=M); t += M[:, :n].sum(1)
    return t - prep["c"]

def permutation_test(prep, B=100_000, seed=0, keep=False):
    nb = -(-B // BLOCK); seeds = np.random.SeedSequence(seed).spawn(nb); cnt = 0; s1 = s2 = 0.0; allt = [] if keep else None; tq = []
    for b in range(nb):
        size = min(BLOCK, B - b * BLOCK); t = tstar_block(prep, size, np.random.default_rng(seeds[b]))
        cnt += int((np.abs(t) >= abs(prep["t_obs"]) - 1e-12).sum()); s1 += t.sum(); s2 += (t * t).sum()
        if keep: allt.append(t)
    mean = s1 / B; var = s2 / B - mean ** 2
    out = {"p": (1 + cnt) / (1 + B), "B": B, "seed": seed, "tstar_mean": mean, "tstar_sd": float(np.sqrt(var)), "t_obs": prep["t_obs"]}
    if keep: out["tstar"] = np.concatenate(allt)
    return out

def exact_null_variance(prep):
    """Closed-form Var(T*) under sampling without replacement: sum_s n1 (N-n1)/N * s2_s,  s2_s = sample variance of r~ in stratum s."""
    return float(sum(n * (len(v) - n) / len(v) * v.var(ddof=1) for v, n in zip(prep["groups"], prep["n1s"])))
