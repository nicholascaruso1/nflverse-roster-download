#!/usr/bin/env python3
"""Post-closure D1 sensitivity check: do QB spikes (pass_attempt==1, pass==0, play_type=='qb_spike') change D1?
Usage: python3 -I spike_check.py <pregame play_by_play_2026.parquet or .csv>   (pregame file SHA-256 422f7893...0795)"""
import sys
import pandas as pd
f = sys.argv[1]
p = pd.read_csv(f, low_memory=False) if f.endswith(".csv") else pd.read_parquet(f)
print("rows", len(p), "all qb_spike rows", int((p.qb_spike == 1).sum()), "| spikes inside the audit EPA filter (play_type in pass/run):",
      int(((p.qb_spike == 1) & p.play_type.isin(["pass", "run"])).sum()))
for n in ["C.Wentz", "K.Murray"]:
    r = p[(p.passer_player_name == n) & (p.posteam == "MIN")]
    a = r[r["pass"] == 1]
    base = int(((a.pass_attempt == 1) & (a.sack != 1)).sum())
    withsp = int(((r.pass_attempt == 1) & (r.sack != 1)).sum())
    print(f"{n}: dropbacks {len(a)}, attempts excl sacks (pass==1 filter, as in audit) {base}, with spikes {withsp}, "
          f"spike rows {int((r.qb_spike == 1).sum())}, spike yards {r[r.qb_spike == 1].passing_yards.sum():.0f}")
