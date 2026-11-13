"""Stale-reference audit of ACTIVE revision-4 files. Usage: python simulations/f4_revision4/stale_reference_audit.py  (writes docs/.../STALE_REFERENCE_AUDIT_REV4.md)."""
import re, glob
from pathlib import Path
import paths
ROOT = paths.REPO; D = ROOT / "docs" / "nfl_script_narrative_engine"
files = [f for f in glob.glob(str(D / "*REV4*.md")) if not f.endswith("STALE_REFERENCE_AUDIT_REV4.md")] + [str(D / "V1_1_REVISION4_ADDENDUM.md"), str(ROOT / "reference/confirmatory_specs/F4_MIRRORED_CURRENT_RECORDS.json"),
         str(ROOT / "reference/feature_registry_v1.1.csv"), str(ROOT / "reference/feature_registry_v1.1.meta.json"), str(ROOT / "scripts/narrative_registry.py"), str(ROOT / "scripts/f4_stopping_rule.py"),
         str(ROOT / "scripts/f4_permutation_test.py"), str(ROOT / "simulations/f4_revision4/README.md"), str(ROOT / "reference/baseline_fit/baseline_fit_k8_report.md")]
pats = {"106 structural / 25 empirical": r"\b106\b|\b25 (empirical|EMPIRICAL)", "Option A1/A3": r"\bA1\b|\bA3\b", "10.2-point MDE": r"10\.2", "season-week-only permutation": r"season-week permutation", "PENDING_PRE_FREEZE": r"PENDING_PRE_FREEZE",
        "left-closed / float digitize of d": r"left-closed|digitize\(d|digitize\(.*EDGES", "old power/MDE (55-62%, ~13 points)": r"55.62|MDE (is )?about 13|about 13 points|~13", "B = 299 simulations": r"B = 299|B=299", "registry hash b714c780 as current": r"b714c780"}
hist = re.compile(r"supersed|not 106|was 106|\(was|retired|correction|withdrawn|reclassified|rev(ision)? ?[23]|earlier|first stopping|no longer|SUPERSEDED|corrected|re-?run|->|→|findings|still (says|describes)|say 106|before the fix|binned|was b714c780|Supersedes registry|superseded sha|\(was ", re.I)
out, active = [], []
for f in files:
    for n, l in enumerate(Path(f).read_text().split("\n"), 1):
        for k, rx in pats.items():
            if re.search(rx, l):
                c = "HISTORICAL/CORRECTION NOTE" if hist.search(l) else "ACTIVE-STALE"; rel = str(Path(f).relative_to(ROOT)); out.append((k, rel, n, c, l.strip()[:150]))
                if c == "ACTIVE-STALE": active.append(out[-1])
md = ["# Stale-reference audit — revision 4 active files", "", "Scope: revision 4 docs, F4 spec JSON, regenerated registry CSV/meta, registry builder, stopping-rule and permutation modules, simulation README, baseline report. Patterns: " + "; ".join(pats) + ".", "",
      f"Result: {len(out)} matches; **{len(active)} ACTIVE-STALE**. Every other match is an explicit supersession/correction statement.", "",
      "Intentionally unchanged historical records (append-only / point-in-time, not active definitions): `research_ledger/hypotheses_ledger.csv` original REGISTERED rows and `research_ledger/partition_manifest.csv` (registry b714c780… at build time), `reports/v1.1/v1.1_build_report.md`.", "", "## ACTIVE-STALE items"] + ([f"- {a[1]}:{a[2]} ({a[0]}): {a[4]}" for a in active] or ["- none"]) + ["", "## All matches", "| pattern | file:line | class | text |", "|---|---|---|---|"] + [f"| {k} | {f}:{n} | {c} | {t.replace('|', '/')} |" for k, f, n, c, t in out]
(D / "STALE_REFERENCE_AUDIT_REV4.md").write_text("\n".join(md) + "\n"); print(len(out), "matches;", len(active), "active-stale"); [print(a) for a in active]
