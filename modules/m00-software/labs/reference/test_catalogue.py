import csv
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import urlopen
from http.server import HTTPServer

from catalogue import (check_outputs, normalise_extension, scan_directory,
                       save_snapshot, search_documents, write_csv)
from api_server import make_handler
from api_client import fetch_documents


class CatalogueTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "inputs"
        self.root.mkdir()
        (self.root / "notes, draft.TXT").write_text("hello", encoding="utf-8")
        (self.root / "empty.txt").touch()
        (self.root / "README").write_text("plain", encoding="utf-8")
        (self.root / "nested").mkdir()
        (self.root / "nested" / "hidden.txt").write_text("nested")
        self.database = self.base / "catalogue.db"

    def test_direct_files_sizes_and_suffixes(self):
        records, warnings = scan_directory(self.root)
        self.assertEqual(len(records), 3)
        self.assertEqual(warnings, [])
        by_name = {row["name"]: row for row in records}
        self.assertEqual(by_name["empty.txt"]["size_bytes"], 0)
        self.assertEqual(by_name["notes, draft.TXT"]["extension"], ".txt")
        self.assertEqual(by_name["README"]["extension"], "")
        self.assertEqual(by_name["notes, draft.TXT"]["size_bytes"], 5)

    def test_symlink_is_not_an_extra_document(self):
        (self.root / "link.txt").symlink_to(self.root / "empty.txt")
        self.assertEqual(len(scan_directory(self.root)[0]), 3)

    def test_bad_root_is_not_empty_success(self):
        with self.assertRaises(ValueError):
            scan_directory(self.base / "missing")

    def test_csv_roundtrip_quotes_and_headers(self):
        rows, _ = scan_directory(self.root)
        output = self.base / "catalogue.csv"
        write_csv(rows, output)
        with output.open(newline="", encoding="utf-8") as handle:
            loaded = list(csv.DictReader(handle))
        self.assertIn("notes, draft.TXT", [row["name"] for row in loaded])
        self.assertEqual(sum(int(row["size_bytes"]) for row in loaded), 10)

    def test_refresh_deduplicates_and_removes_stale_rows(self):
        rows, _ = scan_directory(self.root)
        save_snapshot(rows, self.root, self.database)
        save_snapshot(rows, self.root, self.database)
        self.assertEqual(len(search_documents(self.database)), 3)
        (self.root / "README").unlink()
        save_snapshot(scan_directory(self.root)[0], self.root, self.database)
        self.assertEqual(len(search_documents(self.database)), 2)

    def test_refresh_preserves_other_roots(self):
        rows, _ = scan_directory(self.root)
        save_snapshot(rows, self.root, self.database)
        other = self.base / "other"
        other.mkdir()
        (other / "second.md").write_text("other")
        save_snapshot(scan_directory(other)[0], other, self.database)
        save_snapshot([], self.root, self.database)
        self.assertEqual([r["name"] for r in search_documents(self.database)],
                         ["second.md"])

    def test_failed_refresh_rolls_back_previous_snapshot(self):
        rows, _ = scan_directory(self.root)
        save_snapshot(rows, self.root, self.database)
        bad = [dict(rows[0], size_bytes=-1)]
        with self.assertRaises(sqlite3.IntegrityError):
            save_snapshot(bad, self.root, self.database)
        self.assertEqual(len(search_documents(self.database)), 3)

    def test_search_normalises_and_binds_untrusted_values(self):
        save_snapshot(scan_directory(self.root)[0], self.root, self.database)
        self.assertEqual(len(search_documents(self.database, " TXT ")), 2)
        self.assertEqual(search_documents(self.database, "txt' OR 1=1 --"), [])

    def test_missing_database_not_created_by_search(self):
        with self.assertRaises(ValueError):
            search_documents(self.database)
        self.assertFalse(self.database.exists())

    def test_empty_filter_rejected(self):
        with self.assertRaises(ValueError):
            normalise_extension("...")

    def test_output_guard(self):
        with self.assertRaises(ValueError):
            check_outputs(self.root, [self.root / "output.csv"])
        with self.assertRaises(ValueError):
            check_outputs(self.root, [self.database, self.database])

    def test_individual_stat_failure_is_visible_warning(self):
        original = Path.stat
        def stat(path, *args, **kwargs):
            if path.name == "notes, draft.TXT":
                raise PermissionError("simulated inspection failure")
            return original(path, *args, **kwargs)
        with patch.object(Path, "stat", stat):
            rows, warnings = scan_directory(self.root)
        self.assertEqual(len(rows), 2)
        self.assertEqual(len(warnings), 1)

    def test_cli_end_to_end(self):
        script = Path(__file__).with_name("catalogue.py")
        run = subprocess.run(
            [sys.executable, str(script), "scan", str(self.root),
             "--db", str(self.database)], capture_output=True, text=True,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)["count"], 3)
        bad = subprocess.run(
            [sys.executable, str(script), "scan", str(self.base / "missing")],
            capture_output=True, text=True,
        )
        self.assertNotEqual(bad.returncode, 0)

    def test_api_contract_filter_and_unknown_route(self):
        server = HTTPServer(("127.0.0.1", 0), make_handler(self.root))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            port = server.server_port
            payload = fetch_documents(port, "TXT")
            self.assertEqual(payload["count"], 2)
            with urlopen(f"http://127.0.0.1:{port}/health", timeout=2) as response:
                self.assertEqual(json.load(response), {"status": "ok"})
            for route, expected in [("missing", 404),
                                    ("documents?extension=", 400)]:
                with self.assertRaises(HTTPError) as caught:
                    urlopen(f"http://127.0.0.1:{port}/{route}", timeout=2)
                self.assertEqual(caught.exception.code, expected)
                caught.exception.close()
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
