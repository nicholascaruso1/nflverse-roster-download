"""Generic append-only, hash-chained CSV (used by the v1.1 partition manifest and hypotheses ledger).

Each row stores the previous row's hash and its own hash over every other field, so editing,
deleting or reordering any row breaks verification. Files are only ever opened for append.
"""
from __future__ import annotations
import csv, hashlib, json
from pathlib import Path


class ChainError(Exception):
    pass


def row_hash(row, fields):
    content = {k: str(row.get(k, "")) for k in fields if k != "row_hash"}
    return hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()


def verify(path, fields, seq_field):
    """Return (ok, n_rows, head_hash, errors)."""
    path = Path(path)
    if not path.exists():
        return True, 0, "GENESIS", []
    errors, prev, count = [], "GENESIS", 0
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != list(fields):
            return False, 0, prev, ["header does not match expected fields"]
        for i, row in enumerate(reader, start=1):
            count = i
            if row[seq_field] != str(i): errors.append(f"row {i}: {seq_field} out of sequence")
            if row["prev_hash"] != prev: errors.append(f"row {i}: prev_hash chain broken")
            if row["row_hash"] != row_hash(row, fields): errors.append(f"row {i}: row_hash mismatch (content altered)")
            prev = row["row_hash"]
    return (not errors), count, prev, errors


def read_rows(path):
    path = Path(path)
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def append(path, fields, seq_field, rows):
    """Append rows; refuses to touch a chain that fails verification. Returns (total_rows, head_hash)."""
    path = Path(path)
    ok, count, head, errors = verify(path, fields, seq_field)
    if not ok:
        raise ChainError("chain failed verification: " + "; ".join(errors[:3]))
    path.parent.mkdir(parents=True, exist_ok=True)
    new_file = not path.exists()
    with open(path, "a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields))
        if new_file: writer.writeheader()
        for row in rows:
            count += 1
            record = {k: ("" if row.get(k) is None else str(row.get(k, ""))) for k in fields}
            record[seq_field] = str(count)
            record["prev_hash"] = head
            record["row_hash"] = row_hash(record, fields)
            head = record["row_hash"]
            writer.writerow(record)
    return count, head
