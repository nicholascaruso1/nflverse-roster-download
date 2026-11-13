"""Single place for filesystem configuration (no hard-coded absolute paths). Environment variables:
  NFL_REPO_ROOT      repository root (default: two levels above this file)
  NFLVERSE_GAMES_CSV nflverse games.csv (REQUIRED for scripts that need the schedule structure or, for the authorized baseline fit, outcomes)
  NFL_DERIVED_DIR    derived/v1.1 partition directory (default: <repo>/derived/v1.1)
  F4_OUT_DIR         where results are written (default: ./results next to this file)
Importing this module puts <repo>/scripts and this directory on sys.path."""
import os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = Path(os.environ.get("NFL_REPO_ROOT", HERE.parents[1])).resolve()
for p in (REPO / "scripts", HERE):
    if str(p) not in sys.path: sys.path.insert(0, str(p))
DERIVED = Path(os.environ.get("NFL_DERIVED_DIR", REPO / "derived" / "v1.1"))   # gitignored Parquet partitions
OUT = Path(os.environ.get("F4_OUT_DIR", HERE / "results")); OUT.mkdir(parents=True, exist_ok=True)
def games_csv():
    p = os.environ.get("NFLVERSE_GAMES_CSV")
    if not p or not Path(p).exists(): raise SystemExit("Set NFLVERSE_GAMES_CSV to the nflverse games.csv path")
    return p
