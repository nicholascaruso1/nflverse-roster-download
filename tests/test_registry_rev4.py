"""Revision 4 registry tests: 98/33 classification encoded, corrected F4 hypothesis, append-only ledger lineage, NOT_FROZEN."""
import json, sys, unittest
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "scripts"))
import narrative_registry as reg, hashchain

class RegistryRev4(unittest.TestCase):
    def setUp(self): self.f = reg.build_registry()
    def test_testability_counts(self):
        g = self.f[(self.f.tier == "B") & (self.f.status == "EXPLORATORY")]
        self.assertEqual(len(g), 504); c = g.testability.value_counts().to_dict()
        self.assertEqual((c[reg.STRUCTURAL], c[reg.EMPIRICAL_ZERO], c[reg.TESTABLE]), (98, 33, 373))
        self.assertTrue((self.f[self.f.tier != "B"].testability == reg.NOT_APPLICABLE).all())
    def test_classification_file_matches_registry_and_math_rule(self):
        cls = pd.read_csv(reg.UNTESTABLE_CSV); self.assertEqual(len(cls), 131); self.assertTrue(set(cls.feature_id) <= set(self.f.feature_id))
        self.assertEqual(cls.zero_class_rev4.value_counts().to_dict(), {"STRUCTURAL": 98, "EMPIRICAL_ZERO": 33})
        # no days_since / months_since feature may ever be structural (no mathematical upper bound)
        unb = cls[cls.quantity.str.startswith(("days_since", "completed_months"))]; self.assertFalse((unb.zero_class_rev4 == "STRUCTURAL").any())
        # the eight season_ties features reclassified in revision 4
        self.assertEqual(int(((cls.quantity == "season_ties") & cls.changed_from_rev3).sum()), 8)
    def test_f4_hypothesis_corrected_and_confirmatory_unique(self):
        r = self.f[self.f.feature_id == "F4_MIRRORED_CURRENT_RECORDS"].iloc[0]
        self.assertNotIn("season-week permutation", r.hypothesis); self.assertIn("exchangeable", r.hypothesis); self.assertIn("A2", r.hypothesis)
        self.assertEqual(list(self.f[self.f.status == "CONFIRMATORY"].feature_id), ["F4_MIRRORED_CURRENT_RECORDS"])
    def test_registry_files_match_code_and_not_frozen(self):
        meta = json.loads(reg.REGISTRY_META.read_text()); self.assertEqual(meta["sha256"], reg.registry_sha256(self.f)); self.assertTrue(meta["freeze_status"].startswith("NOT_FROZEN"))
        self.assertEqual(meta["untestable_classification_sha256"], reg.untestable_csv_sha256()); self.assertEqual(reg.REGISTRY_CSV.read_bytes(), reg.registry_csv_bytes(self.f))
    def test_ledger_lineage_append_only(self):
        ok, n, head, errors = hashchain.verify(reg.HYPOTHESES_LEDGER, reg.LEDGER_FIELDS, "hypothesis_row"); self.assertTrue(ok, errors)
        rows = hashchain.read_rows(reg.HYPOTHESES_LEDGER); rev = [r for r in rows if r["event_type"] == "REGISTRY_REVISED"]
        self.assertEqual({r["feature_id"] for r in rev}, {"F4_MIRRORED_CURRENT_RECORDS", "TIER_B_EXPLORATORY_GRID"})
        self.assertTrue(all(r["registry_sha256"] == reg.registry_sha256(self.f) for r in rev))
        orig = [r for r in rows if r["event_type"] == "REGISTERED"]; self.assertEqual(len(orig), 14)
        self.assertTrue(all(r["registry_sha256"].startswith("b714c780") for r in orig))      # original rows never rewritten
        self.assertTrue(all("b714c780" in r["statement"] for r in rev))                      # lineage to the superseded registry hash
if __name__ == "__main__": unittest.main()
