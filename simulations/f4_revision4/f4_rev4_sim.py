"""Revision-4 outcome-blind simulations of the FINAL F4 design (A2 stopping rule, stratified residual permutation, frozen coefficients).
Real 2021-2025 schedule structure reused cyclically; ALL outcomes simulated. Usage: f4_rev4_sim.py MODE TOL R B DELTA [NSEASONS] [SEED]"""
import sys, json, time, os
import numpy as np
import paths
import f4_type1_sim as S
import f4_stopping_rule as SR

K = S.K; logistic = S.logistic
def simulate2(R, seasons, theta_sd, hfa, tie_p, delta, rng, mode):
    teams, tix, WEEKS = S.teams, S.tix, S.WEEKS
    cols = {k: [] for k in ["Wh", "Lh", "Th", "Wa", "La", "Ta", "h", "f4"]}; sw_id, gh, ga = [], [], []; swc = 0
    for si, s in enumerate(seasons):
        theta = rng.normal(0, theta_sd, (R, len(teams)))
        tre = rng.normal(0, 0.4, (R, len(teams)))                       # team random effects for 'teamre'
        sshift = rng.normal(0, 0.3, (R, 1))                              # season-level home-edge shift for 'seasonshift'
        W = np.zeros((R, len(teams))); L = W.copy(); T = W.copy()
        for w, g in S.WEEKS[s]:
            hi = np.array([tix[t] for t in g.home_team]); ai = np.array([tix[t] for t in g.away_team])
            Wh, Lh, Th, Wa, La, Ta = W[:, hi], L[:, hi], T[:, hi], W[:, ai], L[:, ai], T[:, ai]
            Gh, Ga = Wh + Lh + Th, Wa + La + Ta
            elig = (Gh >= 1) & (Ga >= 1); f4 = elig & (Wa == Lh) & (La == Wh) & (Ta == Th)
            dd = (Wh + .5 * Th + K / 2) / (Gh + K) - (Wa + .5 * Ta + K / 2) / (Ga + K)
            if mode == 'latent': p = logistic(hfa + theta[:, hi] - theta[:, ai])
            elif mode == 'gslope': p = logistic(hfa + np.where(Gh <= 4, 1.5, np.where(Gh <= 8, 3.5, 6.0)) * dd)
            elif mode == 'cubic': p = logistic(hfa + 2.0 * dd + 40.0 * dd ** 3)
            elif mode == 'eqbonus': p = logistic(hfa + 3.0 * dd + 0.25 * (Gh == Ga))
            elif mode == 'eqbonus_big': p = logistic(hfa + 3.0 * dd + 1.2 * (Gh == Ga))
            elif mode == 'levelgap': p = logistic(hfa + 3.0 * dd + 0.6 * (Gh - Ga))
            elif mode == 'weekshock':     # per season-week common logit shock AND per-week signal-scale heterogeneity (residual variance differs by week)
                shock = rng.normal(0, 0.30, (R, 1)); scale = np.exp(rng.normal(0, 0.5, (R, 1)))
                p = logistic(hfa + shock + 3.0 * scale * dd)
            elif mode == 'teamre':        # records signal + persistent team effects (repeated team participation not captured by records)
                p = logistic(hfa + 3.0 * dd + tre[:, hi] - tre[:, ai])
            elif mode == 'seasonshift':   # season-level home-edge drift
                p = logistic(hfa + sshift + 3.0 * dd)
            elif mode == 'combo':         # all of the above, moderate
                shock = rng.normal(0, 0.20, (R, 1)); scale = np.exp(rng.normal(0, 0.35, (R, 1)))
                p = logistic(hfa + sshift + shock + 3.0 * scale * dd + 0.5 * (tre[:, hi] - tre[:, ai]) + 0.25 * (Gh == Ga))
            p = np.where(f4, np.clip(p + delta, 0, 1), p)
            u1, u2 = rng.random(p.shape), rng.random(p.shape); tie = u1 < tie_p; win = (~tie) & (u2 < p)
            h = np.where(tie, 0.5, np.where(win, 1.0, 0.0))
            for a, b in (("Wh", Wh), ("Lh", Lh), ("Th", Th), ("Wa", Wa), ("La", La), ("Ta", Ta), ("h", h), ("f4", f4)): cols[a].append(b)
            sw_id += [swc] * len(hi); swc += 1; gh.append(Gh[0]); ga.append(Ga[0])
            W[:, hi] += win; L[:, hi] += (~win) & (~tie); T[:, hi] += tie
            L[:, ai] += win; W[:, ai] += (~win) & (~tie); T[:, ai] += tie
    out = {k: np.concatenate(v, axis=1) for k, v in cols.items()}
    out["sw"] = np.array(sw_id); out["Gh"] = np.concatenate(gh); out["Ga"] = np.concatenate(ga)
    keep = (out["Gh"] >= 1) & (out["Ga"] >= 1)
    for k in out: out[k] = out[k][..., keep]
    return out

def perm2(vals, ids, f4, B, rng, tol):
    """Stratified residual permutation (same as S.perm_p) returning p, n_on_support_F4, n_supported_strata, effective size."""
    keep = ids >= 0; u, inv = np.unique(ids[keep], return_inverse=True)
    N = np.bincount(inv); n1 = np.bincount(inv, weights=f4[keep].astype(float)).astype(int); ok = (n1 >= 1) & (N - n1 >= tol)
    if ok.sum() == 0: return np.nan, 0, 0, 0.0
    sel = np.zeros(len(ids), bool); sel[np.where(keep)[0]] = ok[inv]
    v, lab, sid = vals[sel], f4[sel], np.unique(ids[sel], return_inverse=True)[1]
    ns = np.bincount(sid); n1s = np.bincount(sid, weights=lab.astype(float)).astype(int)
    c = (n1s / ns * np.bincount(sid, weights=v)).sum(); t_obs = v[lab].sum() - c
    order = np.argsort(sid, kind="stable"); starts = np.concatenate([[0], np.cumsum(ns)[:-1]])
    pick = np.zeros((B, len(v)), bool); keys = rng.random((B, len(v)))
    for s_i in range(len(ns)):
        cc = order[starts[s_i]:starts[s_i] + ns[s_i]]
        pick[:, cc] = np.argsort(np.argsort(keys[:, cc], axis=1), axis=1) < n1s[s_i]
    ts = pick @ v - c
    return (1 + (np.abs(ts) >= abs(t_obs) - 1e-12).sum()) / (1 + B), int(lab.sum()), int(len(ns)), float((n1s * (ns - n1s) / ns).sum())

def main():
    mode, tol, R, B, delta = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5])
    nseas = int(sys.argv[6]) if len(sys.argv) > 6 else 10; SEED = int(sys.argv[7]) if len(sys.argv) > 7 else 20261120
    sd = {"lat035": .35, "lat060": .60, "lat085": .85}.get(mode, 0.0); m = "latent" if mode.startswith("lat") else mode
    hfa = 0.20 if mode == "lat060" else 0.15
    rng = np.random.default_rng(SEED + 7919 * hash(mode) % 100000 * 0 + tol + int(delta * 1000) + sum(map(ord, mode)))
    seasons = [S.SEASONS[i % 5] for i in range(nseas)]
    tr = simulate2(8, S.SEASONS, sd, hfa, 0.003, 0.0, rng, m); dtr = S.features(tr)
    coefs = S.fit_frac_logit(dtr.ravel(), tr["h"].ravel(), (~tr["f4"]).ravel())     # frozen from a SEPARATE simulated training set
    t0 = time.time(); rec = []
    CH = 400
    for c0 in range(0, R, CH):
        r_ = min(CH, R - c0); o = simulate2(r_, seasons, sd, hfa, 0.003, delta, rng, m); d = S.features(o)
        sw = o["sw"]; we = np.r_[np.where(np.diff(sw) != 0)[0], len(sw) - 1]
        for r in range(r_):
            f4 = o["f4"][r]; ids = SR.stratum_ids(o["Gh"], o["Ga"], o["Wh"][r], o["Th"][r], o["Wa"][r], o["Ta"][r])
            cnt = SR.cumulative_on_support(ids, f4, we, tol); j = SR.first_week_reaching(cnt, SR.TARGET)
            if j < 0: rec.append((np.nan, np.nan, 0, 0, 0, 0.0, int(f4.sum()), int(cnt[-1]))); continue
            e = we[j] + 1; hh = o["h"][r][:e]; dd = d[r][:e]; ss = sw[:e]
            res = hh - logistic(coefs[0] + coefs[1] * dd); cen = res - (np.bincount(ss, weights=res) / np.bincount(ss))[ss]
            p, nos, nst, eff = perm2(cen, ids[:e], f4[:e], B, rng, tol)
            rec.append((p, j, nos, nst, int(ss[-1] + 1), eff, int(f4[:e].sum()), int(cnt[j])))
    a = np.array(rec, float); reached = ~np.isnan(a[:, 0]); p = a[reached, 0]
    rej = float((p < 0.05).mean()) if len(p) else np.nan
    seasons_to = np.ceil(a[reached, 4] / 18.0)  # season-weeks elapsed -> seasons (approx; weeks/season ~ 17-18)
    out = {"mode": mode, "tol": tol, "R": R, "B": B, "delta": delta, "n_seasons_simulated": nseas, "coefs": coefs.tolist(),
           "frac_reached_188": float(reached.mean()), "reject_rate": rej, "mc_se": float(np.sqrt(rej * (1 - rej) / max(1, len(p)))) if len(p) else None,
           "on_support_F4_at_eval_mean": float(a[reached, 2].mean()), "on_support_F4_at_eval_p5_p50_p95": np.percentile(a[reached, 2], [5, 50, 95]).tolist(),
           "supported_strata_mean": float(a[reached, 3].mean()), "supported_strata_min_p5_p50_p95_max": [float(a[reached, 3].min())] + np.percentile(a[reached, 3], [5, 50, 95]).tolist() + [float(a[reached, 3].max())],
           "effective_size_mean": float(a[reached, 5].mean()), "effective_size_p5_p50_p95": np.percentile(a[reached, 5], [5, 50, 95]).tolist(),
           "total_F4_at_eval_mean": float(a[reached, 6].mean()), "seasons_to_eval_p5_p50_p95": np.percentile(seasons_to, [5, 50, 95]).tolist() if len(p) else None,
           "secs": round(time.time() - t0)}
    print(json.dumps(out), flush=True)
    open(os.environ.get("OUTFILE", paths.OUT / "results.jsonl"), "a").write(json.dumps(out) + "\n")

if __name__ == "__main__": main()
