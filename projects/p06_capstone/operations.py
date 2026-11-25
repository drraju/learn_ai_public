"""Local request ledger and aggregate metrics; stores no question text or bearer tokens."""
import argparse
import hashlib
import json
import sqlite3
from contextlib import closing
import statistics
import time
from pathlib import Path


class OperationsStore:
    def __init__(self, path, clock=time.time):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.clock = clock
        with closing(sqlite3.connect(self.path)) as conn, conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS requests (
                request_id TEXT PRIMARY KEY, tenant TEXT NOT NULL,
                question_sha256 TEXT NOT NULL, result_json TEXT NOT NULL,
                status TEXT NOT NULL, elapsed_ms REAL NOT NULL, created_at REAL NOT NULL)''')

    @staticmethod
    def fingerprint(question):
        return hashlib.sha256(question.encode('utf-8')).hexdigest()

    def existing(self, request_id, tenant, question):
        with closing(sqlite3.connect(self.path)) as conn, conn:
            row = conn.execute('SELECT tenant,question_sha256,result_json FROM requests WHERE request_id=?',
                               (request_id,)).fetchone()
        if row is None:
            return None
        if row[0] != tenant or row[1] != self.fingerprint(question):
            raise ValueError('request ID reused for different input')
        return json.loads(row[2])

    def record(self, request_id, tenant, question, result, elapsed_ms):
        with closing(sqlite3.connect(self.path)) as conn, conn:
            conn.execute('BEGIN IMMEDIATE')
            row = conn.execute('SELECT tenant,question_sha256,result_json FROM requests WHERE request_id=?',
                               (request_id,)).fetchone()
            if row:
                if row[0] != tenant or row[1] != self.fingerprint(question):
                    raise ValueError('request ID reused for different input')
                return json.loads(row[2])
            conn.execute('''INSERT INTO requests VALUES (?,?,?,?,?,?,?)''',
                         (request_id, tenant, self.fingerprint(question),
                          json.dumps(result), result['status'], elapsed_ms, self.clock()))
        return result

    def metrics(self):
        with closing(sqlite3.connect(self.path)) as conn, conn:
            rows = conn.execute('SELECT status,elapsed_ms FROM requests').fetchall()
        values = [elapsed for _, elapsed in rows]
        return {'requests': len(rows),
                'answered': sum(status == 'answered' for status, _ in rows),
                'no_evidence': sum(status == 'no_evidence' for status, _ in rows),
                'median_ms': round(statistics.median(values), 3) if values else None}

    def purge_older_than(self, seconds):
        if seconds < 0:
            raise ValueError('retention must be nonnegative')
        with closing(sqlite3.connect(self.path)) as conn, conn:
            cursor = conn.execute('DELETE FROM requests WHERE created_at < ?',
                                  (self.clock() - seconds,))
            return cursor.rowcount


def main():
    parser = argparse.ArgumentParser(description='Inspect or purge the local P6 request ledger')
    parser.add_argument('action', choices=('metrics', 'purge'))
    parser.add_argument('--db', default='generated/p6_state.db')
    parser.add_argument('--days', type=int, default=7)
    args = parser.parse_args()
    store = OperationsStore(args.db)
    if args.action == 'metrics':
        print(json.dumps(store.metrics(), indent=2))
    else:
        print(json.dumps({'purged': store.purge_older_than(args.days * 86400)}))


if __name__ == '__main__':
    main()
