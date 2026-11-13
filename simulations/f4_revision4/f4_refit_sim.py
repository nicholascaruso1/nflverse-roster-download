"""Calibration of the DISCOVERY-style procedure (in-sample baseline, refit inside every permutation). Simulated outcomes only."""
import sys, json, os, time
import numpy as np
import f4_type1_sim as S

def batched_fit(d, h, w, iters=8):
    """Weighted fractional-logit IRLS for B weight vectors at once. w: (B,N) in {0,1}."""
    B = w.shape[0]; b0 = np.zeros(B); b1 = np.zeros(B)
    for _ in range(iters):
        mu = S.logistic(b0[:, None] + b1[:, None] * d[None, :]); Wt = mu * (1 - mu) * w
        S0, S1, S2 = Wt.sum(1), (Wt * d).sum(1), (Wt * d * d).sum(1)
        g0, g1 = (w * (h - mu)).sum(1), (w * (h - mu) * d).sum(1)
        det = S0 * S2 - S1 ** 2 + 1e-12
        b0 = b0 + (S2 * g0 - S1 * g1) / det; b1 = b1 + (-S1 * g0 + S0 * g1) / det
    return b0, b1

def centred(resid, starts):
    """Subtract season-week means; games are stored in season-week order so reduceat applies. resid: (B,N)."""
    sums = np.add.reduceat(resid, starts, axis=-1); cnt = np.diff(np.append(starts, resid.shape[-1]))
    return resid - np.repeat(sums / cnt, cnt, axis=-1)

def refit_test(h, d, f4, sw, ids, B, rng, tol_n=20):
    keep = ids >= 0
    u, inv = np.unique(ids[keep], return_inverse=True)
    N = np.bincount(inv); n1 = np.bincount(inv, weights=f4[keep].astype(float)).astype(int)
    ok = (n1 >= 1) & (N - n1 >= tol_n)
    if ok.sum() == 0: return np.nan
    supp = np.zeros(len(ids), bool); supp[np.where(keep)[0]] = ok[inv]
    sid = np.full(len(ids), -1); sid[supp] = np.unique(ids[supp], return_inverse=True)[1]
    ns = np.bincount(sid[supp]); n1s = np.bincount(sid[supp], weights=f4[supp].astype(float)).astype(int)
    onehot = np.zeros((len(ids), len(ns))); onehot[np.where(supp)[0], sid[supp]] = 1
    starts = np.r_[0, np.where(np.diff(sw) != 0)[0] + 1]
    def stat(labels):                      # labels: (B',N) bool, True = F4 (real or pseudo); fit excludes labelled games
        b0, b1 = batched_fit(d, h, (~labels).astype(float))
        r = h[None, :] - S.logistic(b0[:, None] + b1[:, None] * d[None, :])
        r = centred(r, starts)
        c = ((r @ onehot) / ns * n1s).sum(1)                       # null mean of the sum under label permutation
        return (r * (labels & supp)).sum(1) - c
    t_obs = stat(f4[None, :].copy())[0]
    labels = np.tile(f4, (B, 1))             # off-support games keep their real label (they stay excluded from / included in the fit)
    keys = rng.random((B, len(ids)))
    for s_i in range(len(ns)):
        cols = np.where(sid == s_i)[0]
        ranks = np.argsort(np.argsort(keys[:, cols], axis=1), axis=1)
        labels[:, cols] = ranks < n1s[s_i]
    tstar = stat(labels)
    return (1 + (np.abs(tstar) >= abs(t_obs) - 1e-12).sum()) / (1 + B)

if __name__ == "__main__":
    R, B = int(sys.argv[1]), int(sys.argv[2]); SEED = int(os.environ.get("SEED", 20261114)); rng = np.random.default_rng(SEED)
    nulls = [("latent_sd0.60_edge0.20", 0.60, 0.20, 'latent'), ("STRESS_gslope", 0, 0.15, 'gslope'), ("STRESS_equalG_bonus_large", 0, 0.15, 'eqbonus_big')]
    res = []
    for name, sd, hfa, mode in nulls:
        t0 = time.time()
        o = S.simulate(R, sd, hfa, 0.003, 0.0, rng, mode); d_all = S.features(o)
        ps = []
        for r in range(R):
            ids = S.strata_ids(o, d_all[r], o["f4"][r], r)
            p = refit_test(o["h"][r], d_all[r], o["f4"][r], o["sw"], ids, B, rng)
            if not np.isnan(p): ps.append(p)
        a = np.array(ps); rate = float((a < 0.05).mean())
        res.append({"null": name, "R": len(a), "B": B, "seed": SEED, "refit_in_each_permutation_type1": rate, "mc_se": float(np.sqrt(rate * (1 - rate) / len(a)))})
        print(json.dumps(res[-1]), "secs", round(time.time() - t0), flush=True)
    json.dump(res, open(str(S.paths.OUT / "f4_refit_sim_results.json"), "w"), indent=2)
