"""Outcome-blind Type I / power simulation for the F4 test (no real outcomes used).

The real schedule STRUCTURE (who plays whom in which week, 2021-2025 REG) is reused; every result is simulated
from a latent-strength null model in which F4 status has NO effect beyond team strength (records are only noisy proxies).
"""
import sys, json, time, os
import numpy as np, pandas as pd
import paths
import nfl_script_narrative_engine as eng
import f4_stopping_rule as SR

K = 8
EDGES = np.array([-0.15, -0.05, 0.05, 0.15])
def gclass(g): return np.digitize(g, [3, 5, 9])           # 1-2,3-4,5-8,9+
def dbin(d): return np.digitize(d, EDGES)                  # 5 bins

raw = eng.read_schedule(paths.games_csv())
sched = raw[(raw.game_type == "REG") & raw.season.between(2021, 2025)].sort_values(["season", "week", "gameday", "game_id"])
teams = sorted(set(sched.home_team) | set(sched.away_team)); tix = {t: i for i, t in enumerate(teams)}
SEASONS = sorted(sched.season.unique())
WEEKS = {s: [(w, sched[(sched.season == s) & (sched.week == w)]) for w in sorted(sched[sched.season == s].week.unique())] for s in SEASONS}

def logistic(x): return 1 / (1 + np.exp(-x))

def simulate(R, theta_sd, hfa, tie_p, delta, rng, mode='latent'):
    """Return dict of arrays (R, N) for eligible games across the 5 seasons, plus fixed vectors."""
    cols = {k: [] for k in ["Wh", "Lh", "Th", "Wa", "La", "Ta", "h", "f4"]}
    sw_id, gh, ga = [], [], []
    swc = 0
    for s in SEASONS:
        theta = rng.normal(0, theta_sd, (R, len(teams)))
        W = np.zeros((R, len(teams))); L = W.copy(); T = W.copy()
        for w, g in WEEKS[s]:
            hi = np.array([tix[t] for t in g.home_team]); ai = np.array([tix[t] for t in g.away_team])
            Wh, Lh, Th, Wa, La, Ta = W[:, hi], L[:, hi], T[:, hi], W[:, ai], L[:, ai], T[:, ai]
            Gh, Ga = Wh + Lh + Th, Wa + La + Ta
            elig = (Gh >= 1) & (Ga >= 1)
            f4 = elig & (Wa == Lh) & (La == Wh) & (Ta == Th)
            if mode == 'latent':
                p = logistic(hfa + theta[:, hi] - theta[:, ai])
            else:  # records-only stress nulls: outcome depends on records ONLY through d and games played; F4 has no extra effect
                dd = (Wh + .5 * Th + K / 2) / (Gh + K) - (Wa + .5 * Ta + K / 2) / (Ga + K)
                if mode == 'gslope':      # slope in d grows with games played (early records are weaker signals)
                    p = logistic(hfa + np.where(Gh <= 4, 1.5, np.where(Gh <= 8, 3.5, 6.0)) * dd)
                elif mode == 'cubic':     # nonlinear in d
                    p = logistic(hfa + 2.0 * dd + 40.0 * dd ** 3)
                elif mode == 'eqbonus':   # equal-games-played matchups (all F4 games) have a slightly different home edge; no F4 effect
                    p = logistic(hfa + 3.0 * dd + 0.25 * (Gh == Ga))
                elif mode == 'eqbonus_big':
                    p = logistic(hfa + 3.0 * dd + 1.2 * (Gh == Ga))
                elif mode == 'levelgap':  # depends on unequal games played (post-bye) and a small level effect
                    p = logistic(hfa + 3.0 * dd + 0.6 * (Gh - Ga))
            p = np.where(f4, np.clip(p + delta, 0, 1), p)
            u1, u2 = rng.random(p.shape), rng.random(p.shape)
            tie = u1 < tie_p; win = (~tie) & (u2 < p)
            h = np.where(tie, 0.5, np.where(win, 1.0, 0.0))
            for a, b in (("Wh", Wh), ("Lh", Lh), ("Th", Th), ("Wa", Wa), ("La", La), ("Ta", Ta), ("h", h), ("f4", f4)):
                cols[a].append(b)
            sw_id += [swc] * len(hi); swc += 1
            gh.append(Gh[0]); ga.append(Ga[0])
            W[:, hi] += win; L[:, hi] += (~win) & (~tie); T[:, hi] += tie
            L[:, ai] += win; W[:, ai] += (~win) & (~tie); T[:, ai] += tie
    out = {k: np.concatenate(v, axis=1) for k, v in cols.items()}
    out["sw"] = np.array(sw_id); out["Gh"] = np.concatenate(gh); out["Ga"] = np.concatenate(ga)
    keep = (out["Gh"] >= 1) & (out["Ga"] >= 1)   # eligibility is schedule-determined, same for all replicates
    for k in out: out[k] = out[k][..., keep] if out[k].ndim == 2 or k in ("sw", "Gh", "Ga") else out[k]
    return out

def features(o):
    Gh, Ga = o["Gh"], o["Ga"]
    swh = (o["Wh"] + .5 * o["Th"] + K / 2) / (Gh + K); swa = (o["Wa"] + .5 * o["Ta"] + K / 2) / (Ga + K)
    return swh - swa

def fit_frac_logit(d, h, mask, iters=25):
    """Fractional-response logistic via Newton/IRLS on [1, d] using rows where mask."""
    X = np.stack([np.ones_like(d[mask]), d[mask]], 1); y = h[mask]; b = np.zeros(2)
    for _ in range(iters):
        mu = logistic(X @ b); Wt = mu * (1 - mu)
        b = b + np.linalg.solve(X.T @ (X * Wt[:, None]) + 1e-9 * np.eye(2), X.T @ (y - mu))
    return b

def strata_ids(o, d, f4rep, r):
    """Revision 4: exact integer, right-closed d-bins via the shared module (the earlier float digitize version is superseded)."""
    return SR.stratum_ids(o["Gh"], o["Ga"], o["Wh"][r], o["Th"][r], o["Wa"][r], o["Ta"][r])

def perm_p(stat_vals, ids, f4, B, rng, tol_n=20):
    """Stratified permutation p for T = sum over F4 of rtil, centred by the stratum means. Strata need >=1 F4 and >=tol_n non-F4."""
    keep = ids >= 0
    u, inv = np.unique(ids[keep], return_inverse=True)
    N = np.bincount(inv); n1 = np.bincount(inv, weights=f4[keep].astype(float)).astype(int)
    ok = (n1 >= 1) & (N - n1 >= tol_n)
    if ok.sum() == 0: return np.nan, 0
    sel = np.zeros(len(ids), bool); idx = np.where(keep)[0]; sel[idx] = ok[inv]
    vals, lab, sid = stat_vals[sel], f4[sel], np.unique(ids[sel], return_inverse=True)[1]
    ns = np.bincount(sid); n1s = np.bincount(sid, weights=lab.astype(float)).astype(int)
    c = (n1s / ns * np.bincount(sid, weights=vals)).sum()          # null mean of the sum
    t_obs = vals[lab].sum() - c
    order = np.argsort(sid, kind="stable"); starts = np.concatenate([[0], np.cumsum(ns)[:-1]])
    rank_pick = np.zeros((B, len(vals)), bool)
    keys = rng.random((B, len(vals)))
    for s_i in range(len(ns)):
        cols = order[starts[s_i]:starts[s_i] + ns[s_i]]
        ranks = np.argsort(np.argsort(keys[:, cols], axis=1), axis=1)
        rank_pick[:, cols] = ranks < n1s[s_i]
    tstar = rank_pick @ vals - c
    return (1 + (np.abs(tstar) >= abs(t_obs) - 1e-12).sum()) / (1 + B), int(lab.sum())

def run(label, theta_sd, hfa, tie_p, delta, R, B, rng, coefs, mode='latent'):
    o = simulate(R, theta_sd, hfa, tie_p, delta, rng, mode); d = features(o)
    res = {"M0_seasonweek_perm": [], "M1_stratified_perm": [], "M2_model_z": [], "n_f4": [], "n_f4_on_support": []}
    for r in range(R):
        e = logistic(coefs[0] + coefs[1] * d[r]); resid = o["h"][r] - e
        sw = o["sw"]; cen = resid - (np.bincount(sw, weights=resid) / np.bincount(sw))[sw]
        f4 = o["f4"][r]
        res["n_f4"].append(int(f4.sum()))
        if f4.sum() < 5:
            for k in ("M0_seasonweek_perm", "M1_stratified_perm", "M2_model_z"): res[k].append(np.nan)
            res["n_f4_on_support"].append(0); continue
        p0, _ = perm_p(cen, sw, f4, B, rng, tol_n=1)
        ids = strata_ids(o, d[r], f4, r)
        p1, n_os = perm_p(cen, ids, f4, B, rng)
        from math import erf, sqrt
        z = (o["h"][r][f4] - e[f4]).sum() / np.sqrt((e[f4] * (1 - e[f4])).sum())
        p2 = 2 * (1 - 0.5 * (1 + erf(abs(z) / sqrt(2))))
        res["M0_seasonweek_perm"].append(p0); res["M1_stratified_perm"].append(p1); res["M2_model_z"].append(p2); res["n_f4_on_support"].append(n_os)
    out = {"label": label, "delta": delta, "R": R, "B": B, "mean_n_f4": float(np.mean(res["n_f4"])), "mean_n_f4_on_support": float(np.mean(res["n_f4_on_support"]))}
    for k in ("M0_seasonweek_perm", "M1_stratified_perm", "M2_model_z"):
        a = np.array(res[k]); a = a[~np.isnan(a)]
        out[k] = {"reject_rate_alpha05": float((a < 0.05).mean()), "mc_se": float(np.sqrt((a < .05).mean() * (1 - (a < .05).mean()) / len(a)))}
    return out

if __name__ == "__main__":
    R, B = int(sys.argv[1]), int(sys.argv[2])
    SEED = int(os.environ.get('SEED', 20261112)); rng = np.random.default_rng(SEED)
    DGPS = [("moderate_spread_hfa15", 0.35, 0.15, 0.003, 'latent'), ("wide_spread_hfa20", 0.60, 0.20, 0.003, 'latent'), ("very_wide_spread_hfa25", 0.85, 0.25, 0.003, 'latent'),
            ("STRESS_gslope", 0, 0.15, 0.003, 'gslope'), ("STRESS_cubic", 0, 0.15, 0.003, 'cubic'), ("STRESS_unequalG", 0, 0.15, 0.003, 'levelgap'), ("STRESS_equalG_bonus", 0, 0.15, 0.003, 'eqbonus'), ("STRESS_equalG_bonus_large", 0, 0.15, 0.003, 'eqbonus_big')]
    if os.environ.get("OUT_SUFFIX"): pass
    if len(sys.argv) > 3: DGPS = [x for x in DGPS if x[0] == sys.argv[3]]
    allres = []
    for name, sd, hfa, tp, mode in DGPS:
        tr = simulate(8, sd, hfa, tp, 0.0, rng, mode); dtr = features(tr)
        coefs = fit_frac_logit(dtr.ravel(), tr["h"].ravel(), (~tr["f4"]).ravel())
        for delta in ((0.0,) if os.environ.get('TYPEI_ONLY') else (0.0, 0.10)):
            t0 = time.time()
            res = run(name, sd, hfa, tp, delta, R, B, rng, coefs, mode); res["frozen_coefs"] = coefs.tolist(); allres.append(res)
            print(json.dumps(res), flush=True); print("  secs", round(time.time() - t0), file=sys.stderr)
    json.dump(allres, open(str(paths.OUT / "f4_type1_sim_results") + os.environ.get("OUT_SUFFIX", "") + ("_" + sys.argv[3] if len(sys.argv) > 3 else "") + ".json", "w"), indent=2)
