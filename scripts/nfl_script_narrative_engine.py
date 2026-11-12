#!/usr/bin/env python3
"""NFL Script & Narrative Engine v1.0.1.

Pregame-only descriptive discovery of gematria, calendar, schedule-record,
head-to-head, scoreline and optional roster-name relationships. Not a betting
model. All output is non-directional and preserves competing narratives.

v1.0.1 is a correctness / data-integrity patch of v1.0 (no new research
features). See docs/nfl_script_narrative_engine/README.md for the change list.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, platform, re, subprocess, sys, uuid
from datetime import date, datetime, timezone
from pathlib import Path
import pandas as pd

ENGINE_VERSION = "1.0.1"
REPO_ROOT = Path(__file__).resolve().parents[1]
IDENTITY_PATH = REPO_ROOT / "reference" / "team_identity_eras.csv"
TNF_PATH_DEFAULT = REPO_ROOT / "reference" / "tnf_broadcast_games.csv"
DEFAULT_LEDGER = Path("research_ledger") / "findings_ledger.csv"
GAMES_DEFAULT_SOURCE = "https://github.com/nflverse/nflverse-data/releases/download/schedules/games.csv"
ROSTER_DEFAULT_SOURCE = "https://github.com/nflverse/nflverse-data/releases/download/weekly_rosters/"

# Only these schedule columns are ever loaded. Market columns (moneyline, spread,
# totals, odds) present in nflverse games.csv are deliberately never read.
SCHEDULE_REQUIRED = {"game_id", "season", "game_type", "week", "gameday", "gametime",
                     "away_team", "away_score", "home_team", "home_score"}
TNF_COLUMNS = ["game_id", "season", "week", "gameday", "away_team", "home_team", "network",
               "tnf_brand_status", "source_url", "verification_status"]

# Chronological validation periods (preregistered; do not tune against holdout).
SPLITS = (("discovery", 1999, 2018), ("validation", 2019, 2022),
          ("holdout", 2023, 2025), ("prospective", 2026, 9999))

# Non-canonical codes seen in nflverse files (older weekly rosters use e.g. ARZ/BLT/CLV/HST/SL).
CODE_ALIASES = {"ARZ": "ARI", "BLT": "BAL", "CLV": "CLE", "HST": "HOU", "SL": "STL", "JAC": "JAX",
                "LAR": "LA", "WSH": "WAS", "SDG": "SD", "LVR": "LV", "KAN": "KC", "NWE": "NE",
                "NOR": "NO", "SFO": "SF", "TAM": "TB", "GNB": "GB"}

OUTCOMES = ("HOME_WIN", "AWAY_WIN", "TIE")

LEDGER_FIELDS = ["ledger_row", "run_id", "observed_at_utc", "engine_version", "code_commit",
                 "game_id", "game_id_source", "season", "week", "target_date", "split", "team",
                 "feature_id", "family_id", "category", "finding", "value", "match_type",
                 "name_basis", "data_quality", "caveat", "prev_hash", "row_hash"]


# ---------------------------------------------------------------- identities
_IDENT_CACHE = {}

def identities(path=IDENTITY_PATH):
    key = str(path)
    if key not in _IDENT_CACHE:
        frame = pd.read_csv(path, dtype={"franchise_id": str, "code": str})
        for col in ("season_start", "season_end"):
            frame[col] = frame[col].astype(int)
        _IDENT_CACHE[key] = frame
    return _IDENT_CACHE[key]

def code_to_franchise(path=IDENTITY_PATH):
    table = identities(path)
    return dict(zip(table.code, table.franchise_id))

def normalize_code(code):
    up = str(code).strip().upper()
    return CODE_ALIASES.get(up, up)

def to_franchise(code, path=IDENTITY_PATH):
    """Map any era/alias code (OAK, LV, SD, STL, LAR, ARZ ...) to its franchise id."""
    mapping = code_to_franchise(path)
    norm = normalize_code(code)
    if norm in mapping:
        return mapping[norm]
    raise ValueError(f"Unknown team code: {code!r}")

def identity_for(franchise, season, path=IDENTITY_PATH):
    """Historical identity (city/nickname actually in use) for a franchise in an NFL season."""
    table = identities(path)
    rows = table[(table.franchise_id == franchise) & (table.season_start <= season) &
                 (table.season_end >= season)]
    if rows.empty:
        raise ValueError(f"No identity era for {franchise} in season {season}")
    return rows.iloc[0].to_dict()

def current_identity(franchise, path=IDENTITY_PATH):
    table = identities(path)
    rows = table[table.franchise_id == franchise].sort_values("season_end")
    return rows.iloc[-1].to_dict()

def identity_strings(ident):
    """Cipher input strings. Full identity is always city + nickname (spelled out)."""
    return {"city": ident["city"], "nickname": ident["nickname"],
            "full_identity": f'{ident["city"]} {ident["nickname"]}'}

def nfl_season_for_date(day):
    """Fallback only: January/February games belong to the previous NFL season."""
    return day.year - 1 if day.month <= 2 else day.year

def split_for_season(season):
    for name, lo, hi in SPLITS:
        if lo <= season <= hi:
            return name
    return "pre_discovery"


# ------------------------------------------------------------------- ciphers
def letters(value):
    return re.sub(r"[^A-Z]", "", str(value).upper())

def digital_root(value):
    value = abs(int(value))
    return 0 if value == 0 else 1 + (value - 1) % 9

def ciphers(value):
    nums = [ord(ch) - 64 for ch in letters(value)]
    ordinal = sum(nums)
    reverse = sum(27 - n for n in nums)
    pyth = sum(((n - 1) % 9) + 1 for n in nums)
    return {"ordinal": ordinal, "ordinal_root": digital_root(ordinal),
            "reverse_ordinal": reverse, "reverse_root": digital_root(reverse),
            "pythagorean": pyth, "pythagorean_root": digital_root(pyth),
            "letters": len(nums)}


# ------------------------------------------------------------ record helpers
def team_record(frame, team):
    w = l = t = 0
    for row in frame.itertuples(index=False):
        if team == row.away_team: own, opp = row.away_score, row.home_score
        elif team == row.home_team: own, opp = row.home_score, row.away_score
        else: continue
        if pd.isna(own) or pd.isna(opp): continue
        if own > opp: w += 1
        elif own < opp: l += 1
        else: t += 1
    games = w + l + t
    return {"wins": w, "losses": l, "ties": t, "games": games, "record": f"{w}-{l}-{t}",
            "win_pct": ((w + 0.5 * t) / games) if games else None}

def win_pct(record):
    """Standings win percentage: (wins + 0.5 * ties) / games."""
    games = record["wins"] + record["losses"] + record["ties"]
    return (record["wins"] + 0.5 * record["ties"]) / games if games else None

def game_outcome(home_score, away_score):
    """Three-outcome label for predictive evaluation; ties are never folded into W/L."""
    if home_score > away_score: return "HOME_WIN"
    if home_score < away_score: return "AWAY_WIN"
    return "TIE"

def team_games(frame, team):
    return frame[(frame.away_team == team) | (frame.home_team == team)]

def last_result_date(frame, team, result):
    rows = team_games(frame, team).sort_values("gameday")
    for row in rows.iloc[::-1].itertuples(index=False):
        own, opp = ((row.away_score, row.home_score) if row.away_team == team
                    else (row.home_score, row.away_score))
        if ((result == "win" and own > opp) or (result == "loss" and own < opp)
                or (result == "tie" and own == opp)):
            return row.gameday
    return None

def elapsed_months(start, end):
    """Exact days, calendar month boundaries crossed, and completed calendar months.

    Completed months subtracts one when the end day-of-month is earlier than the
    start day-of-month (no month-end clipping rule is applied).
    """
    boundaries = (end.year - start.year) * 12 + end.month - start.month
    completed = boundaries - (1 if end.day < start.day else 0)
    return {"days": (end - start).days, "month_boundaries": boundaries,
            "completed_months": completed}

def mirrored(rec_a, rec_b):
    """Mirrored records require at least one decided game each (suppresses 0-0-0)."""
    if rec_a["games"] < 1 or rec_b["games"] < 1:
        return False
    return (rec_a["wins"] == rec_b["losses"] and rec_a["losses"] == rec_b["wins"]
            and rec_a["ties"] == rec_b["ties"])

def hour(value):
    try: return int(str(value).split(":")[0])
    except (TypeError, ValueError): return None

def is_thanksgiving(day):
    return day.month == 11 and day.weekday() == 3 and 22 <= day.day <= 28

def classify_slot(day, gametime):
    """Schedule-derived slot label. NEVER a branded-TNF determination."""
    wd = day.strftime("%A")
    hr = hour(gametime)
    late = hr is not None and hr >= 19
    if wd == "Thursday":
        if is_thanksgiving(day): return "thanksgiving"
        return "thursday_evening_proxy" if late else "thursday_other"
    if wd == "Sunday" and late: return "sunday_night_proxy"
    if wd == "Monday" and late: return "monday_night_proxy"
    return "other"


# ------------------------------------------------------------------ data I/O
def read_schedule(path):
    header = list(pd.read_csv(path, nrows=0).columns)
    missing = SCHEDULE_REQUIRED - set(header)
    if missing: raise ValueError(f"games.csv missing required columns: {sorted(missing)}")
    frame = pd.read_csv(path, usecols=sorted(SCHEDULE_REQUIRED), low_memory=False)
    frame["gameday"] = pd.to_datetime(frame.gameday, errors="coerce").dt.date
    frame = frame[frame.gameday.notna()].copy()
    frame["season"] = pd.to_numeric(frame.season, errors="coerce")
    frame["week"] = pd.to_numeric(frame.week, errors="coerce")
    frame["gametime"] = frame.gametime.fillna("").astype(str)
    frame["weekday"] = frame.gameday.map(lambda d: d.strftime("%A"))
    frame["slot"] = [classify_slot(d, t) for d, t in zip(frame.gameday, frame.gametime)]
    mapping = code_to_franchise()
    frame["away_code"] = frame.away_team
    frame["home_code"] = frame.home_team
    frame["away_team"] = frame.away_code.map(lambda c: mapping.get(normalize_code(c)))
    frame["home_team"] = frame.home_code.map(lambda c: mapping.get(normalize_code(c)))
    bad = frame[frame.away_team.isna() | frame.home_team.isna()]
    if len(bad):
        codes = sorted(set(bad.away_code[bad.away_team.isna()]) | set(bad.home_code[bad.home_team.isna()]))
        raise ValueError(f"Unmapped team codes in schedule: {codes}")
    return frame

def prepare_history(raw, target):
    frame = raw[raw.gameday.map(lambda d: d < target)]
    return frame[frame.away_score.notna() & frame.home_score.notna()].copy()

def load_games(path, target):
    return prepare_history(read_schedule(path), target)

def identity_coverage_gaps(frame):
    """Games whose (code, season) has no identity era row. Should be zero."""
    table = identities()
    gaps = 0
    for side in ("away_code", "home_code"):
        for code, season in set(zip(frame[side], frame.season)):
            norm = normalize_code(code)
            ok = ((table.code == norm) & (table.season_start <= season) &
                  (table.season_end >= season)).any()
            gaps += 0 if ok else 1
    return gaps

def load_tnf_table(path):
    """Branded-TNF table. Only rows marked branded_tnf + verified (+ source_url) count."""
    info = {"path": str(path) if path else None, "rows": 0, "verified_rows": 0, "verified_game_ids": set()}
    if not path or not Path(path).exists():
        info["status"] = "absent"
        return info
    frame = pd.read_csv(path, dtype=str).fillna("")
    missing = set(TNF_COLUMNS) - set(frame.columns)
    if missing: raise ValueError(f"TNF table missing columns: {sorted(missing)}")
    ok = frame[(frame.tnf_brand_status == "branded_tnf") & (frame.verification_status == "verified") &
               (frame.source_url != "")]
    info.update({"rows": len(frame), "verified_rows": len(ok),
                 "verified_game_ids": set(ok.game_id), "status": "loaded"})
    return info


# ---------------------------------------------------------------- provenance
def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()

def input_provenance(path, role, source_url=None, source_default=None, retrieved=None, frame=None):
    path = Path(path)
    stat = path.stat()
    header = list(pd.read_csv(path, nrows=0).columns) if path.suffix == ".csv" else []
    entry = {"role": role, "path": str(path), "basename": path.name, "sha256": sha256_file(path),
             "bytes": stat.st_size, "file_mtime_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(timespec="seconds"),
             "source_url": source_url or source_default,
             "source_url_basis": "supplied" if source_url else ("default_declared_unverified" if source_default else "none"),
             "retrieved_date": retrieved or "unknown (not supplied; see file_mtime_utc)",
             "schema_columns": len(header),
             "schema_sha256": hashlib.sha256(",".join(header).encode()).hexdigest() if header else None}
    if frame is not None and len(frame):
        entry["coverage"] = {"rows_loaded": int(len(frame)),
                             "season_min": int(frame.season.min()), "season_max": int(frame.season.max()),
                             "first_gameday": str(frame.gameday.min()), "last_gameday": str(frame.gameday.max())}
    return entry

def code_provenance():
    def git(*args):
        try:
            return subprocess.run(["git", "-C", str(REPO_ROOT), *args], capture_output=True,
                                  text=True, timeout=15).stdout.strip()
        except Exception:
            return ""
    commit = git("rev-parse", "HEAD") or "unknown"
    return {"engine_version": ENGINE_VERSION, "git_commit": commit,
            "working_tree_dirty": bool(git("status", "--porcelain", "--", "scripts", "reference")),
            "script_sha256": sha256_file(Path(__file__).resolve()),
            "python": platform.python_version(), "pandas": pd.__version__}


# -------------------------------------------------------------------- ledger
class LedgerError(Exception):
    pass

def _row_hash(row):
    content = {k: str(row.get(k, "")) for k in LEDGER_FIELDS if k != "row_hash"}
    return hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()

def verify_ledger(path):
    """Verify an append-only ledger's hash chain. Returns (ok, n_rows, head_hash, errors)."""
    path = Path(path)
    if not path.exists(): return True, 0, "GENESIS", []
    errors, prev, count = [], "GENESIS", 0
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != LEDGER_FIELDS:
            return False, 0, prev, ["header does not match LEDGER_FIELDS"]
        for i, row in enumerate(reader, start=1):
            count = i
            if row["ledger_row"] != str(i): errors.append(f"row {i}: ledger_row out of sequence")
            if row["prev_hash"] != prev: errors.append(f"row {i}: prev_hash chain broken")
            if row["row_hash"] != _row_hash(row): errors.append(f"row {i}: row_hash mismatch (content altered)")
            prev = row["row_hash"]
    return (not errors), count, prev, errors

def append_ledger(path, rows):
    """Append rows (never rewrite). Refuses to append to a ledger that fails verification."""
    path = Path(path)
    ok, count, head, errors = verify_ledger(path)
    if not ok: raise LedgerError("ledger failed verification: " + "; ".join(errors[:3]))
    path.parent.mkdir(parents=True, exist_ok=True)
    new_file = not path.exists()
    with open(path, "a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=LEDGER_FIELDS)
        if new_file: writer.writeheader()
        for row in rows:
            count += 1
            record = {k: ("" if row.get(k) is None else str(row.get(k, ""))) for k in LEDGER_FIELDS}
            record["ledger_row"] = str(count)
            record["prev_hash"] = head
            record["row_hash"] = _row_hash(record)
            head = record["row_hash"]
            writer.writerow(record)
    return count, head


# ----------------------------------------------------------------------- run
def run(args):
    target = date.fromisoformat(args.date)
    away, home = to_franchise(args.away), to_franchise(args.home)
    if away == home: raise ValueError("Supply two different valid team codes.")
    raw = read_schedule(args.games)
    history = prepare_history(raw, target)
    regular = history[history.game_type.eq("REG")].copy()

    tnf = load_tnf_table(getattr(args, "tnf_table", TNF_PATH_DEFAULT))
    regular["branded_tnf_verified"] = regular.game_id.isin(tnf["verified_game_ids"])
    tnf["verified_ids_not_in_schedule"] = len(tnf["verified_game_ids"] - set(raw.game_id))
    tnf["verified_game_ids"] = len(tnf["verified_game_ids"])

    match = raw[(raw.gameday == target) & (raw.away_team == away) & (raw.home_team == home)]
    if len(match):
        row = match.iloc[0]
        season, game_type = int(row.season), row.game_type
        week = args.week if args.week is not None else int(row.week)
        game_id, game_id_source = row.game_id, "nflverse_schedule"
    else:
        season, game_type, week = nfl_season_for_date(target), None, args.week
        game_id = f"unmatched_{target.isoformat()}_{away}_{home}"
        game_id_source = "synthetic_game_not_in_schedule"
    ident = {t: identity_for(t, season) for t in (away, home)}
    cur = {t: current_identity(t) for t in (away, home)}
    season_games = regular[regular.season.eq(season)]
    records = {t: team_record(season_games, t) for t in (away, home)}

    findings = []
    def add(feature_id, category, label, value, caveat, team="", family="", quality="computed",
            match_type="descriptive", basis="n/a"):
        findings.append({"category": category, "finding": label, "value": str(value), "caveat": caveat,
                         "feature_id": feature_id, "family_id": family or feature_id, "team": team,
                         "name_basis": basis, "match_type": match_type, "data_quality": quality})

    inputs = [input_provenance(args.games, "schedule", getattr(args, "games_source_url", None),
                               GAMES_DEFAULT_SOURCE, getattr(args, "games_retrieved", None), raw)]
    if Path(TNF_PATH_DEFAULT if not getattr(args, "tnf_table", None) else args.tnf_table).exists():
        inputs.append(input_provenance(getattr(args, "tnf_table", None) or TNF_PATH_DEFAULT, "tnf_broadcast_table"))
    inputs.append(input_provenance(IDENTITY_PATH, "team_identity_eras"))

    context = {"engine": "NFL Script & Narrative Engine", "version": ENGINE_VERSION,
      "frozen_at": datetime.now().astimezone().isoformat(timespec="seconds"),
      "target_date": target.isoformat(), "away": away, "home": home, "week": week,
      "season": season, "season_source": "nflverse_schedule" if len(match) else "date_fallback",
      "game_id": game_id, "game_id_source": game_id_source, "game_type": game_type,
      "validation_split": split_for_season(season),
      "outcome_vocabulary": list(OUTCOMES),
      "historical_cutoff_exclusive": target.isoformat(),
      "data_cutoff": {"rule": "gameday < target_date (date-level; same-day earlier kickoffs excluded)",
                      "target_date_exclusive": target.isoformat(),
                      "last_game_included": str(regular.gameday.max()) if len(regular) else None},
      "data_scope": {"completed_regular_season_games": len(regular),
        "first_game": str(regular.gameday.min()), "last_game": str(regular.gameday.max()),
        "identity_coverage_gaps": identity_coverage_gaps(history)},
      "tnf_table": tnf,
      "governance": ["Target-date and later results are excluded.",
        "No odds, market prices, or market-implied probabilities are used (market columns are never loaded).",
        "All narrative clusters are descriptive and non-directional.",
        "Cipher variants are dependent, not independent evidence (shared family_id).",
        "Historical team identity is primary; current identity is a separate comparison field.",
        "Branded TNF is counted only from the verified TNF table; Thursday/kickoff proxies are not TNF.",
        "Ties are a separate outcome (HOME_WIN/AWAY_WIN/TIE); win_pct = (W + 0.5*T)/G.",
        "Historical frequencies are descriptive and in-sample."],
      "season_records_before_game": records}

    # -- records
    if mirrored(records[away], records[home]):
        add("records.mirrored_current_season", "records", "Mirrored current-season records",
            f"{away} {records[away]['record']} / {home} {records[home]['record']}",
            "Descriptive symmetry; not a winner prediction.", family="records.mirrored",
            quality="official_schedule_result")
    for team in (away, home):
        add("records.current_season_record", "records", f"{team} current-season record",
            records[team]["record"], "Regular season games before target date.", team=team,
            family="records.current_season", quality="official_schedule_result")
        pct = records[team]["win_pct"]
        add("records.current_season_win_pct", "records", f"{team} current-season win pct",
            "n/a" if pct is None else f"{pct:.3f}", "(W + 0.5*T)/G.", team=team,
            family="records.current_season", quality="official_schedule_result")

    # -- thursday / prime-time slots (never labelled TNF unless verified)
    for team in (away, home):
        tg = team_games(regular, team)
        thu = tg[tg.weekday.eq("Thursday")]
        slots = [
            ("schedule.all_thursday_record", f"{team} all-Thursday record", thu,
             "Every Thursday regular-season game; not branded TNF.", "schedule_derived"),
            ("schedule.thursday_excl_thanksgiving_record", f"{team} Thursday (excl. Thanksgiving) record",
             thu[~thu.slot.eq("thanksgiving")], "Not branded TNF.", "schedule_derived"),
            ("schedule.thursday_evening_proxy_record", f"{team} Thursday >=7 PM ET proxy record (excl. Thanksgiving)",
             thu[thu.slot.eq("thursday_evening_proxy")],
             "Schedule-time proxy only; NOT a TNF record (includes pre-2006 and kickoff-night games).", "schedule_proxy_not_tnf"),
            ("schedule.thanksgiving_record", f"{team} Thanksgiving Thursday record", thu[thu.slot.eq("thanksgiving")],
             "Thanksgiving games are not branded TNF.", "schedule_derived"),
            ("schedule.sunday_night_proxy_record", f"{team} Sunday >=7 PM ET proxy record",
             tg[tg.slot.eq("sunday_night_proxy")], "Schedule-time proxy; not a verified package label.", "schedule_proxy_not_tnf"),
            ("schedule.monday_night_proxy_record", f"{team} Monday >=7 PM ET proxy record",
             tg[tg.slot.eq("monday_night_proxy")], "Schedule-time proxy; not a verified package label.", "schedule_proxy_not_tnf")]
        for fid, label, frame, caveat, quality in slots:
            add(fid, "schedule_records", label, team_record(frame, team)["record"], caveat, team=team,
                family="schedule.slot_records", quality=quality)
        if tnf["verified_rows"]:
            tnf_games = tg[tg.branded_tnf_verified]
            add("schedule.branded_tnf_verified_record", "schedule_records", f"{team} branded TNF record (verified table)",
                team_record(tnf_games, team)["record"], "Only games in the verified branded-TNF table.", team=team,
                family="schedule.slot_records", quality="verified_external_table")
        else:
            add("schedule.branded_tnf_verified_record", "schedule_records", f"{team} branded TNF record (verified table)",
                "unavailable: no verified branded-TNF table", "Branded TNF is never inferred from Thursday or kickoff times.",
                team=team, family="schedule.slot_records", quality="unavailable")
        last_win = last_result_date(thu, team, "win")
        if last_win:
            em = elapsed_months(last_win, target)
            note = f"Last qualifying Thursday win: {last_win}."
            add("calendar.days_since_last_thursday_win", "calendar", f"{team} days since last Thursday win",
                em["days"], note, team=team, family="calendar.since_last_thursday_win", quality="schedule_derived")
            add("calendar.month_boundaries_since_last_thursday_win", "calendar",
                f"{team} calendar-month boundaries since last Thursday win", em["month_boundaries"],
                note + " Counts month boundaries crossed, not completed months.", team=team,
                family="calendar.since_last_thursday_win", quality="schedule_derived")
            add("calendar.completed_months_since_last_thursday_win", "calendar",
                f"{team} completed calendar months since last Thursday win", em["completed_months"],
                note, team=team, family="calendar.since_last_thursday_win", quality="schedule_derived")
        if tnf["verified_rows"]:
            tnf_win = last_result_date(tg[tg.branded_tnf_verified], team, "win")
            if tnf_win:
                em = elapsed_months(tnf_win, target)
                add("calendar.completed_months_since_last_tnf_win", "calendar",
                    f"{team} completed months since last branded TNF win", em["completed_months"],
                    f"Last verified TNF win: {tnf_win}; {em['days']} days; {em['month_boundaries']} month boundaries.",
                    team=team, family="calendar.since_last_tnf_win", quality="verified_external_table")

    # -- head to head (franchise continuity across relocations)
    h2h = regular[((regular.away_team == away) & (regular.home_team == home)) |
                  ((regular.away_team == home) & (regular.home_team == away))].sort_values("gameday")
    context["head_to_head"] = {away: team_record(h2h, away), home: team_record(h2h, home), "games": len(h2h)}
    if len(h2h):
        prev = h2h.iloc[-1]
        context["previous_meeting"] = {"date": str(prev.gameday), "away": prev.away_team,
          "away_score": int(prev.away_score), "home": prev.home_team, "home_score": int(prev.home_score),
          "outcome": game_outcome(prev.home_score, prev.away_score)}
        if prev.away_score == prev.home_score:
            add("head_to_head.previous_meeting_tied", "head_to_head", "Previous meeting was tied",
                f"{int(prev.away_score)}-{int(prev.home_score)} on {prev.gameday}",
                "Historical context only; not a rematch prediction.", quality="official_schedule_result")

    # -- calendar
    remaining = (date(target.year, 12, 31) - target).days
    digit_sum = sum(int(ch) for ch in target.strftime("%Y%m%d"))
    add("calendar.days_remaining_in_year", "calendar", "Days remaining in calendar year, excluding game date",
        remaining, "December 31 of the target's calendar year minus target date.", family="calendar.date")
    add("calendar.date_digit_sum", "calendar", "Date digit sum", digit_sum, "Date format YYYYMMDD.", family="calendar.date")
    add("calendar.date_digit_root", "calendar", "Date digital root", digital_root(digit_sum), "Date format YYYYMMDD.", family="calendar.date")
    add("calendar.weekday_number", "calendar", "Weekday number", target.isoweekday(),
        "ISO weekday: Monday=1 through Sunday=7.", family="calendar.weekday")
    add("calendar.weekday_root", "calendar", "Weekday digital root", digital_root(target.isoweekday()),
        "ISO weekday: Monday=1 through Sunday=7.", family="calendar.weekday")

    # -- gematria: historical identity primary, current identity separate
    team_values = {}
    parts = ("ordinal", "ordinal_root", "reverse_ordinal", "reverse_root", "pythagorean", "pythagorean_root")
    for team in (away, home):
        hist, now = ident[team], cur[team]
        entry = {"franchise_id": team, "season": season,
                 "historical": {"city": hist["city"], "nickname": hist["nickname"], "display_name": hist["display_name"],
                                "code": hist["code"], "ciphers": {k: ciphers(v) for k, v in identity_strings(hist).items()}},
                 "current": {"city": now["city"], "nickname": now["nickname"], "display_name": now["display_name"],
                             "code": now["code"], "ciphers": {k: ciphers(v) for k, v in identity_strings(now).items()}}}
        entry["current_equals_historical"] = (hist["city"], hist["nickname"]) == (now["city"], now["nickname"])
        team_values[team] = entry
        bases = [("historical", hist)] + ([] if entry["current_equals_historical"] else [("current", now)])
        for basis, idt in bases:
            for kind, text in identity_strings(idt).items():
                values = ciphers(text)
                for part in parts:
                    add(f"gematria.{kind}.{part}", "gematria", f"{team} {basis} {kind} {part}", values[part],
                        f"String: {text.upper()}", team=team, family=f"gematria.{team}.{basis}.{kind}",
                        quality="computed", match_type="value", basis=basis)
    context["team_ciphers"] = team_values
    context["combined_nickname_ciphers"] = ciphers(ident[away]["nickname"] + " " + ident[home]["nickname"])

    # -- scoreline base rates
    n = len(regular)
    score27 = int((regular.away_score.eq(27) | regular.home_score.eq(27)).sum())
    ties = int(regular.away_score.eq(regular.home_score).sum())
    tie2727 = int((regular.away_score.eq(27) & regular.home_score.eq(27)).sum())
    total54 = int((regular.away_score + regular.home_score).eq(54).sum())
    context["scoreline_base_rates"] = {"games": n, "either_team_27": score27,
      "either_team_27_rate": score27 / n if n else None, "ties": ties, "tie_rate": ties / n if n else None,
      "exact_27_27": tie2727, "exact_27_27_rate": tie2727 / n if n else None,
      "total_54": total54, "total_54_rate": total54 / n if n else None}
    add("base_rates.exact_27_27", "base_rates", "Historical exact 27-27 frequency",
        f"{tie2727}/{n} ({tie2727/n:.3%})" if n else "n/a", "Completed regular-season games in supplied schedule file; in-sample.")
    add("base_rates.total_54", "base_rates", "Historical total-54 frequency",
        f"{total54}/{n} ({total54/n:.3%})" if n else "n/a", "Completed regular-season games; descriptive only.")

    # -- streaks (regular season only)
    for team in (away, home):
        for result in ("win", "loss"):
            d = last_result_date(regular, team, result)
            if d:
                add(f"streaks.days_since_last_{result}", "streaks", f"Days since {team} last {result}", (target - d).days,
                    f"Last regular-season {result}: {d}; target date excluded; playoffs excluded.", team=team,
                    family="streaks.days_since", quality="official_schedule_result")

    # -- optional roster name matching
    player_matches = []
    if args.rosters and week is not None:
        roster_path = args.rosters / f"roster_weekly_{season}.csv"
        if roster_path.exists():
            roster = pd.read_csv(roster_path, low_memory=False)
            roster["season"] = pd.to_numeric(roster.season, errors="coerce")
            roster["week"] = pd.to_numeric(roster.week, errors="coerce")
            mapping = code_to_franchise()
            roster["team_fid"] = roster.team.map(lambda c: mapping.get(normalize_code(c)) if pd.notna(c) else None)
            context["roster_unmapped_team_codes"] = sorted(set(roster.team[roster.team_fid.isna()].dropna().astype(str)))
            weeks = sorted(roster.loc[(roster.season == season) & (roster.week <= week), "week"].dropna().unique())
            snapshot = int(weeks[-1]) if weeks else None
            context["roster_snapshot_week"] = snapshot
            context["roster_snapshot_caveat"] = "Latest weekly roster at or before target week; not official game-day inactives; snapshot freeze time unverified."
            inputs.append(input_provenance(roster_path, "weekly_roster", getattr(args, "rosters_source_url", None),
                                           ROSTER_DEFAULT_SOURCE, getattr(args, "rosters_retrieved", None)))
            if snapshot is not None:
                roster = roster[(roster.season == season) & (roster.week == snapshot)]
                if "status" in roster: roster = roster[roster.status.astype(str).str.upper().eq("ACT")]
                for opponent, player_team in ((away, home), (home, away)):
                    bases = [("historical", ident[opponent]["nickname"])]
                    if cur[opponent]["nickname"] != ident[opponent]["nickname"]:
                        bases.append(("current", cur[opponent]["nickname"]))
                    for basis, nickname in bases:
                        target_cipher = ciphers(nickname)
                        for row in roster[roster.team_fid.eq(player_team)].itertuples():
                            name = getattr(row, "full_name", None)
                            if not name or pd.isna(name): continue
                            cv = ciphers(name)
                            exact = [k for k in ("ordinal", "reverse_ordinal", "pythagorean") if cv[k] == target_cipher[k]]
                            roots = [k for k in ("ordinal_root", "reverse_root", "pythagorean_root") if cv[k] == target_cipher[k]]
                            if exact or roots:
                                player_matches.append({"player": name, "team": player_team, "name_basis": basis,
                                  "opponent_nickname": nickname.upper(), "exact_systems": exact, "root_systems": roots})
    context["player_name_matches"] = player_matches
    for item in player_matches:
        if item["exact_systems"]:
            add("player_names.exact_match_vs_opponent_nickname", "player_names",
                f'{item["player"]} matches {item["opponent_nickname"]}', ",".join(item["exact_systems"]),
                "Name-value match only; no player-performance inference. Systems listed are dependent (one family).",
                team=item["team"], family=f'player_names.{item["team"]}.{item["player"]}.{item["name_basis"]}',
                quality="roster_snapshot_timing_unverified", match_type="exact", basis=item["name_basis"])

    # -- external claim audit (never validated against proxies)
    claim_args = {away: getattr(args, "claimed_away_tnf_record", None), home: getattr(args, "claimed_home_tnf_record", None)}
    if any(claim_args.values()):
        context["external_tnf_claims"] = {k: v for k, v in claim_args.items() if v}
        for team, claim in claim_args.items():
            if not claim: continue
            if tnf["verified_rows"]:
                verified = team_record(team_games(regular[regular.branded_tnf_verified], team), team)["record"]
            else:
                verified = "unavailable (no verified branded-TNF table)"
            evening = team_record(team_games(regular[regular.slot.eq("thursday_evening_proxy")], team), team)["record"]
            add("claim_audit.external_tnf_record", "claim_audit", f"{team} external TNF claim vs verified TNF table",
                f"claimed {claim}; verified {verified}",
                f"Unverified until a verified table exists. Thursday >=7 PM proxy for context only: {evening} (not TNF).",
                team=team, family="claim_audit.tnf", quality="external_claim_unverified", match_type="claim")

    # -- provenance + ledger
    context["provenance"] = {"inputs": inputs, "code": code_provenance(),
                             "identity_table_sha256": sha256_file(IDENTITY_PATH)}
    run_id = getattr(args, "run_id", None) or uuid.uuid4().hex
    observed = datetime.now(timezone.utc).isoformat(timespec="seconds")
    context["run_id"], context["observed_at_utc"] = run_id, observed
    ledger_path = None if getattr(args, "no_ledger", False) else Path(getattr(args, "ledger", None) or DEFAULT_LEDGER)
    if ledger_path is not None:
        base = {"run_id": run_id, "observed_at_utc": observed, "engine_version": ENGINE_VERSION,
                "code_commit": context["provenance"]["code"]["git_commit"], "game_id": game_id,
                "game_id_source": game_id_source, "season": season, "week": "" if week is None else week,
                "target_date": target.isoformat(), "split": split_for_season(season)}
        rows = [{**base, **{k: f[k] for k in ("team", "feature_id", "family_id", "category", "finding", "value",
                                              "match_type", "name_basis", "data_quality", "caveat")}} for f in findings]
        count, head = append_ledger(ledger_path, rows)
        context["ledger"] = {"path": str(ledger_path), "rows_appended": len(rows), "total_rows": count, "chain_head_sha256": head}

    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    cols = ["category", "finding", "value", "caveat", "feature_id", "family_id", "team", "name_basis", "match_type", "data_quality"]
    pd.DataFrame(findings, columns=cols).to_csv(out / "findings.csv", index=False)
    (out / "frozen_context.json").write_text(json.dumps(context, indent=2, default=str))

    report = [f"# NFL Script & Narrative Engine v{ENGINE_VERSION} — {away} @ {home}", "",
      f"**Target:** {target.isoformat()} | **Season:** {season} | **Week:** {week} | **Split:** {split_for_season(season)} | **Frozen:** {context['frozen_at']}",
      f"**Game ID:** {game_id} ({game_id_source}) | **Code:** {context['provenance']['code']['git_commit'][:12]}"
      f"{' (dirty)' if context['provenance']['code']['working_tree_dirty'] else ''}", "",
      "## Governance", "- Pregame cutoff excludes target-date and later results.",
      "- Descriptive research only; no betting recommendation.",
      "- Branded TNF is counted only from the verified TNF table; Thursday/kickoff proxies are labelled proxies.",
      "- Historical team identity is primary; current identity is a separate comparison.",
      "- Cipher variants share a family_id and are not independent confirmations.", "",
      "## Team identities (historical primary)"]
    for team in (away, home):
        h = team_values[team]["historical"]
        c = team_values[team]["current"]
        report.append(f"- {team}: {h['display_name']} ({h['code']}); current: {c['display_name']}"
                      f"{'' if not team_values[team]['current_equals_historical'] else ' (same)'}")
    report += ["", "## Current records", f"- {away}: {records[away]['record']}", f"- {home}: {records[home]['record']}", "",
               "## Findings (gematria values are in findings.csv / ledger)",
               "| Category | Finding | Value | Caveat |", "|---|---|---|---|"]
    for item in findings:
        if item["category"] == "gematria": continue
        report.append("| " + " | ".join(str(item[k]).replace("|", "/") for k in ("category", "finding", "value", "caveat")) + " |")
    report += ["", "## Gematria (exact values; roots are secondary)", "| Team | Basis | String | Ordinal | Ord root | Reverse | Rev root | Pyth | Pyth root |",
               "|---|---|---|---|---|---|---|---|---|"]
    for team in (away, home):
        for basis in ("historical", "current"):
            if basis == "current" and team_values[team]["current_equals_historical"]: continue
            block = team_values[team][basis]
            for kind, text in (("city", block["city"]), ("nickname", block["nickname"]),
                               ("full_identity", f'{block["city"]} {block["nickname"]}')):
                v = block["ciphers"][kind]
                report.append(f"| {team} | {basis} | {text.upper()} | {v['ordinal']} | {v['ordinal_root']} | {v['reverse_ordinal']} | "
                              f"{v['reverse_root']} | {v['pythagorean']} | {v['pythagorean_root']} |")
    report += ["", "## Interpretation",
      "Do not select the narrative with the most matches. Report both sides.",
      "Historical frequencies are descriptive and in-sample, not predictive.",
      "Predictive evaluation requires preregistration and chronological holdout testing."]
    (out / "report.md").write_text("\n".join(report) + "\n")
    return context, findings


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--games", type=Path)
    parser.add_argument("--date", help="Target game date YYYY-MM-DD")
    parser.add_argument("--away")
    parser.add_argument("--home")
    parser.add_argument("--week", type=int)
    parser.add_argument("--rosters", type=Path)
    parser.add_argument("--tnf-table", type=Path, default=TNF_PATH_DEFAULT, dest="tnf_table")
    parser.add_argument("--claimed-away-tnf-record")
    parser.add_argument("--claimed-home-tnf-record")
    parser.add_argument("--games-source-url")
    parser.add_argument("--games-retrieved", help="Retrieval date of the schedule file (YYYY-MM-DD)")
    parser.add_argument("--rosters-source-url")
    parser.add_argument("--rosters-retrieved")
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER,
                        help="Append-only hash-chained findings ledger")
    parser.add_argument("--no-ledger", action="store_true", dest="no_ledger",
                        help="Dry run: do not append to the ledger")
    parser.add_argument("--run-id")
    parser.add_argument("--verify-ledger", type=Path, dest="verify_ledger",
                        help="Verify a ledger's hash chain and exit")
    parser.add_argument("--output", type=Path, default=Path("narrative_output"))
    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    if args.verify_ledger:
        ok, count, head, errors = verify_ledger(args.verify_ledger)
        print(json.dumps({"ok": ok, "rows": count, "chain_head_sha256": head, "errors": errors}, indent=2))
        sys.exit(0 if ok else 1)
    for name in ("games", "date", "away", "home"):
        if getattr(args, name) is None:
            parser.error(f"--{name} is required")
    run(args)

if __name__ == "__main__":
    main()
