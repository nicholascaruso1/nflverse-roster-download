"""Single shared implementation of the F4 support / stopping rule (outcome-blind: uses only pregame fields + F4 flag).

Used BOTH by the simulations and (unchanged) by the prospective pipeline. No outcome column is accepted anywhere here.
Strata: equal-games-played games only; home games-played class {1-2,3-4,5-8,9+} x shrunk-record difference bin (edges -.15,-.05,.05,.15) = 20.
On-support stratum (evaluation sample, pooled over all season-weeks so far): >=1 F4 game AND >= TOL non-F4 games.
Stopping rule A2: evaluate ONCE, at the end of the first regular-season week at which the CUMULATIVE count of on-support F4 games >= TARGET,
recomputing support from scratch on all games to date at every week-end.
"""
import hashlib
import numpy as np

K = 8; EDGES = np.array([-0.15, -0.05, 0.05, 0.15]); GCUTS = [3, 5, 9]; NSTRATA = 20; TARGET = 188; TOL = 20

def shrunk_diff(Wh, Th, Gh, Wa, Ta, Ga):
    return (Wh + .5 * Th + K / 2) / (Gh + K) - (Wa + .5 * Ta + K / 2) / (Ga + K)

def stratum_ids(Gh, Ga, d):
    """-1 when games played differ (never supported); else gclass*5 + dbin in 0..19."""
    return np.where(Gh == Ga, np.digitize(Gh, GCUTS) * 5 + np.digitize(d, EDGES), -1)

def stratum_counts(ids, f4):
    ok = ids >= 0
    n1 = np.bincount(ids[ok], weights=f4[ok].astype(float), minlength=NSTRATA).astype(int)
    N = np.bincount(ids[ok], minlength=NSTRATA)
    return n1, N - n1

def supported(n1, n0, tol=TOL):
    return (n1 >= 1) & (n0 >= tol)

def on_support_mask(ids, f4, tol=TOL):
    n1, n0 = stratum_counts(ids, f4); sup = supported(n1, n0, tol)
    return (ids >= 0) & sup[np.where(ids >= 0, ids, 0)]

def cumulative_on_support(ids, f4, week_end_idx, tol=TOL):
    """Cumulative on-support F4 count at each week end (index = last game of the week, inclusive). Recomputed from cumulative stratum counts."""
    n = len(ids); oh = np.zeros((n, NSTRATA)); ok = ids >= 0; oh[np.where(ok)[0], ids[ok]] = 1
    c1 = np.cumsum(oh * f4[:, None], axis=0)[week_end_idx]; c0 = np.cumsum(oh * (~f4)[:, None], axis=0)[week_end_idx]
    return (c1 * ((c1 >= 1) & (c0 >= tol))).sum(1).astype(int)

def first_week_reaching(counts, target=TARGET):
    hit = np.where(np.asarray(counts) >= target)[0]
    return int(hit[0]) if len(hit) else -1

def support_hash(game_ids, ids, f4, tol=TOL):
    """SHA-256 over the sorted ids of on-support games (F4 and comparators) -- computed and stored BEFORE any outcome is joined."""
    m = on_support_mask(ids, f4, tol)
    return hashlib.sha256("\n".join(sorted(map(str, np.asarray(game_ids)[m]))).encode()).hexdigest()

if __name__ == "__main__":      # self-tests on synthetic data
    rng = np.random.default_rng(1)
    n = 600; Gh = rng.integers(1, 17, n); d = rng.normal(0, .12, n); f4 = rng.random(n) < .08
    ids = stratum_ids(Gh, Gh.copy(), d); wk = np.sort(rng.integers(0, 60, n)); we = np.r_[np.where(np.diff(wk) != 0)[0], n - 1]
    cnt = cumulative_on_support(ids, f4, we)
    # brute-force recomputation at every week end
    for j, e in enumerate(we):
        sub = on_support_mask(ids[:e + 1], f4[:e + 1]); assert int((sub & f4[:e + 1]).sum()) == cnt[j], j
    assert (np.diff(cnt) >= -999).all()
    # support can only be gained, never lost, as games accumulate (n1,n0 monotone) -> counts non-decreasing
    assert (np.diff(cnt) >= 0).all()
    assert first_week_reaching([1, 5, 187, 188, 190]) == 3 and first_week_reaching([1, 2]) == -1
    h1 = support_hash(np.arange(n), ids, f4); assert h1 == support_hash(np.arange(n)[::-1].copy(), ids[::-1], f4[::-1])  # order-invariant
    print("self-tests OK; final cumulative on-support:", cnt[-1], "of", int(f4.sum()), "F4; hash", h1[:16])
