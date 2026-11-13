"""Tests for the shared F4 support / stopping-rule implementation (outcome-blind; no outcome data used)."""
import sys, unittest
from pathlib import Path
import numpy as np
from fractions import Fraction
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import f4_stopping_rule as SR

class StoppingRule(unittest.TestCase):
    def test_exact_edge_bins_right_closed(self):      # d = dW/20 at G=12; edges land in the LOWER bin ((-.15,-.05], (-.05,.05], ...)
        chk = {(12, 7, 10): 0, (12, 8, 10): 1, (12, 9, 10): 1, (12, 10, 10): 2, (12, 11, 10): 2, (12, 12, 10): 3, (12, 12, 9): 3, (12, 12, 8): 4}
        for (g, w, a), v in chk.items(): self.assertEqual(int(SR.dbin_exact(g, w, 0, a, 0)), v, (g, w, a))
    def test_unequal_games_played_has_no_stratum(self):
        self.assertEqual(int(SR.stratum_ids(5, 6, 3, 0, 3, 0)), -1)
    def test_zero_games_played_is_ineligible(self):      # week-1 games (G=0 for both teams) must never be comparators
        self.assertEqual(int(SR.stratum_ids(0, 0, 0, 0, 0, 0)), -1)
    def test_cumulative_matches_bruteforce_every_weekend(self):
        rng = np.random.default_rng(1); n = 600; G = rng.integers(1, 17, n); Wh = rng.integers(0, G + 1); Wa = rng.integers(0, G + 1); z = np.zeros(n, int)
        f4 = rng.random(n) < .08; ids = SR.stratum_ids(G, G.copy(), Wh, z, Wa, z); wk = np.sort(rng.integers(0, 60, n)); we = np.r_[np.where(np.diff(wk) != 0)[0], n - 1]
        cnt = SR.cumulative_on_support(ids, f4, we)
        for j, e in enumerate(we):
            sub = SR.on_support_mask(ids[:e + 1], f4[:e + 1]); self.assertEqual(int((sub & f4[:e + 1]).sum()), cnt[j])
        self.assertTrue((np.diff(cnt) >= 0).all())
    def test_first_week_reaching(self):
        self.assertEqual(SR.first_week_reaching([1, 5, 187, 188, 190]), 3); self.assertEqual(SR.first_week_reaching([1, 2]), -1)
    def test_support_hash_order_invariant_and_empty(self):
        ids = np.array([0, 0, 1, 1]); f4 = np.array([True, False, False, False]); gid = np.array(list("abcd"))
        self.assertEqual(SR.support_hash(gid, ids, f4), SR.support_hash(gid[::-1].copy(), ids[::-1], f4[::-1]))
        import hashlib; self.assertEqual(SR.support_hash(gid, ids, f4), hashlib.sha256(b"").hexdigest())   # nothing on support (<20 comparators) -> hash of empty list

class BinBoundaries(unittest.TestCase):
    """Right-closed d-bins: (-inf,-3/20] | (-3/20,-1/20] | (-1/20,1/20] | (1/20,3/20] | (3/20,inf), exact arithmetic."""
    EDGES = [Fraction(-3, 20), Fraction(-1, 20), Fraction(1, 20), Fraction(3, 20)]
    @staticmethod
    def ref_bin(G, Wh, Th, Wa, Ta):
        d = Fraction(2 * (Wh - Wa) + (Th - Ta), 2 * (G + 8)); return sum(1 for e in BinBoundaries.EDGES if d > e), d
    def cases(self):
        for G in range(1, 18):
            for Wh in range(G + 1):
                for Th in range(G - Wh + 1):
                    for Wa in range(G + 1):
                        for Ta in range(G - Wa + 1): yield G, Wh, Th, Wa, Ta
    def test_exhaustive_match_with_rational_reference(self):
        n = 0; eq_hits = {e: 0 for e in self.EDGES}; below = {e: 0 for e in self.EDGES}; above = {e: 0 for e in self.EDGES}
        for G, Wh, Th, Wa, Ta in self.cases():
            b, d = self.ref_bin(G, Wh, Th, Wa, Ta); self.assertEqual(int(SR.dbin_exact(G, Wh, Th, Wa, Ta)), b, (G, Wh, Th, Wa, Ta)); n += 1
            for e in self.EDGES:
                if d == e: eq_hits[e] += 1; self.assertEqual(b, self.EDGES.index(e))                 # exact equality -> LOWER bin (right-closed)
                elif d == e + Fraction(1, 2 * (G + 8)): above[e] += 1; self.assertEqual(b, self.EDGES.index(e) + 1)   # one step above -> upper bin
                elif d == e - Fraction(1, 2 * (G + 8)): below[e] += 1; self.assertEqual(b, self.EDGES.index(e))     # one step below -> lower bin
        self.assertGreater(n, 100000)
        for e in self.EDGES: self.assertTrue(eq_hits[e] > 0 and above[e] > 0 and below[e] > 0, e)       # every edge exercised on equality and both sides
    def test_float_digitize_would_misplace_some_edge_cases(self):    # documents WHY exact arithmetic is used
        wrong = 0
        for G, Wh, Th, Wa, Ta in self.cases():
            b, d = self.ref_bin(G, Wh, Th, Wa, Ta)
            if int(np.digitize(SR.shrunk_diff(Wh, Th, G, Wa, Ta, G), SR.EDGES)) != b: wrong += 1
        self.assertGreater(wrong, 0)
if __name__ == "__main__": unittest.main()
