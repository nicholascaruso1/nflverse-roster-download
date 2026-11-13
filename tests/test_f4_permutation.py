"""Tests for the full-scale F4 stratified residual permutation implementation (synthetic residuals only; no outcomes)."""
import sys, itertools, unittest
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import f4_permutation_test as P

def toy():
    rng = np.random.default_rng(5); v1 = rng.normal(size=7); v2 = rng.normal(size=6)
    prep = {"groups": [v1, v2], "n1s": [2, 1], "c": 2 * v1.mean() + v2.mean()}; prep["t_obs"] = float(v1[:2].sum() + v2[:1].sum() - prep["c"]); return prep, v1, v2

class Permutation(unittest.TestCase):
    def test_matches_exact_enumeration(self):
        prep, v1, v2 = toy()
        ts = np.array([v1[list(a)].sum() + v2[list(b)].sum() - prep["c"] for a in itertools.combinations(range(7), 2) for b in itertools.combinations(range(6), 1)])
        pex = float((np.abs(ts) >= abs(prep["t_obs"]) - 1e-12).mean()); r = P.permutation_test(prep, 100_000, 11)
        self.assertLess(abs(r["p"] - pex), 4 * np.sqrt(pex * (1 - pex) / 100_000)); self.assertAlmostEqual(r["tstar_sd"] ** 2, float(ts.var()), delta=0.05)
        self.assertAlmostEqual(P.exact_null_variance(prep), float(ts.var()), places=9)
    def test_reproducible_and_observed_statistic_invariant(self):
        prep, _, _ = toy(); a = P.permutation_test(prep, 20_000, 3); b = P.permutation_test(prep, 20_000, 3); c = P.permutation_test(prep, 10_000, 4)
        self.assertEqual((a["p"], a["tstar_sd"]), (b["p"], b["tstar_sd"])); self.assertEqual(a["t_obs"], c["t_obs"]); self.assertEqual(a["t_obs"], prep["t_obs"])
        self.assertNotEqual(a["tstar_sd"], c["tstar_sd"])
    def test_prepare_support_and_none_when_unsupported(self):
        ids = np.r_[np.zeros(30, int), np.ones(5, int)]; f4 = np.r_[[True] * 3, [False] * 27, [True] * 2, [False] * 3]; rt = np.arange(35, dtype=float)
        prep = P.prepare(rt, ids, f4, 20); self.assertEqual((prep["n_strata"], prep["n_on_support_f4"]), (1, 3))
        self.assertIsNone(P.prepare(rt, ids, np.zeros(35, bool), 20))
if __name__ == "__main__": unittest.main()
