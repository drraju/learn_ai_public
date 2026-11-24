"""Direct-child metadata catalogue. Python 3.11+, standard library only."""
import argparse
import csv
from datetime import datetime, timezone
import json
import logging
from pathlib import Path
import sqlite3
from contextlib import closing

FIELDS = ["path", "name", "extension", "size_bytes", "modified_utc"]
SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
    path TEXT PRIMARY KEY,
    root TEXT NOT NULL,
    name TEXT NOT NULL,
    extension TEXT NOT NULL,
    size_bytes INTEGER NOT NULL CHECK (size_bytes >= 0),
    modified_utc TEXT NOT NULL
)
"""


def normalise_extension(value: str) -> str:
    cleaned = value.strip().lower().lstrip(".")
    if not cleaned:
        raise ValueError("extension must not be empty")
    return "." + cleaned


def scan_directory(root: Path) -> tuple[list[dict], list[str]]:
    """Scan direct regular files. Fail on an invalid root; warn per file."""
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"input is not an existing directory: {root}")
    # Listing errors propagate: a failed listing is not an empty inventory.
    entries = sorted(root.iterdir(), key=lambda path: path.name)
    records = []
    warnings = []
    for path in entries:
        try:
            if path.is_symlink() or not path.is_file():
                continue
            info = path.stat()
            records.append({
                "path": str(path.resolve()),
                "name": path.name,
                "extension": path.suffix.lower(),
                "size_bytes": info.st_size,
                "modified_utc": datetime.fromtimestamp(
                    info.st_mtime, timezone.utc
                ).isoformat(),
            })
        except OSError as error:
            warnings.append(f"could not inspect {path.name}: {error}")
    return records, warnings


def write_csv(records: list[dict], output: Path) -> None:
    """Write metadata CSV. Parent directory must already exist."""
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)


def save_snapshot(records: list[dict], root: Path, database: Path) -> None:
    """Refresh one root atomically; preserve other roots and close resources."""
    root_text = str(root.expanduser().resolve())
    with closing(sqlite3.connect(database)) as connection:
        connection.execute(SCHEMA)
        with connection:
            connection.execute(
                "DELETE FROM documents WHERE root = ?", (root_text,)
            )
            connection.executemany(
                """INSERT INTO documents
                   (path, root, name, extension, size_bytes, modified_utc)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                [
                    (row["path"], root_text, row["name"], row["extension"],
                     row["size_bytes"], row["modified_utc"])
                    for row in records
                ],
            )


def search_documents(database: Path, extension: str | None = None) -> list[dict]:
    """Query an existing database; avoid creating one by a mistyped search."""
    if not database.is_file():
        raise ValueError("database not found; run scan with --db first")
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = sqlite3.Row
        sql = "SELECT " + ", ".join(FIELDS) + " FROM documents"
        parameters = ()
        if extension is not None:
            sql += " WHERE extension = ?"
            parameters = (normalise_extension(extension),)
        sql += " ORDER BY name, path"
        return [dict(row) for row in connection.execute(sql, parameters)]


def check_outputs(root: Path, outputs: list[Path]) -> None:
    resolved_root = root.expanduser().resolve()
    seen = set()
    for output in outputs:
        resolved = output.expanduser().resolve()
        if resolved == resolved_root or resolved_root in resolved.parents:
            raise ValueError("outputs must be outside the scanned directory")
        if resolved in seen:
            raise ValueError("CSV and database outputs must be different files")
        if not resolved.parent.is_dir():
            raise ValueError("output parent directory must already exist")
        seen.add(resolved)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    scan = commands.add_parser("scan", help="inventory direct files")
    scan.add_argument("root", type=Path)
    scan.add_argument("--csv", type=Path)
    scan.add_argument("--db", type=Path)
    search = commands.add_parser("search", help="query stored metadata")
    search.add_argument("database", type=Path)
    search.add_argument("--extension")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        if args.command == "scan":
            outputs = [p for p in (args.csv, args.db) if p is not None]
            check_outputs(args.root, outputs)
            records, warnings = scan_directory(args.root)
            if args.csv:
                write_csv(records, args.csv.expanduser())
            if args.db:
                save_snapshot(records, args.root, args.db.expanduser())
            for warning in warnings:
                logging.warning("%s", warning)
            payload = {"count": len(records), "documents": records,
                       "warnings": warnings}
        else:
            records = search_documents(args.database.expanduser(), args.extension)
            payload = {"count": len(records), "documents": records}
        print(json.dumps(payload, indent=2))
        return 0
    except (OSError, ValueError, sqlite3.Error) as error:
        logging.error("%s", error)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
