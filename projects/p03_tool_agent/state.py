"""SQLite approval and effect ledger for a local, simulated action."""
import sqlite3
from contextlib import closing
import time
from pathlib import Path


class SQLiteActionStore:
    def __init__(self, path, clock=time.time):
        self.path = str(Path(path))
        self.clock = clock
        with closing(sqlite3.connect(self.path)) as conn, conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS approvals (
                key TEXT PRIMARY KEY, tenant TEXT NOT NULL, action TEXT NOT NULL,
                target TEXT NOT NULL, expires_at REAL NOT NULL)''')
            conn.execute('''CREATE TABLE IF NOT EXISTS effects (
                key TEXT PRIMARY KEY, tenant TEXT NOT NULL, action TEXT NOT NULL,
                target TEXT NOT NULL, applied_at REAL NOT NULL)''')

    def grant(self, approval, ttl_seconds=60):
        if not 0 < ttl_seconds <= 3600:
            raise ValueError('invalid approval lifetime')
        fields = (approval.key, approval.tenant, approval.action, approval.target)
        with closing(sqlite3.connect(self.path)) as conn, conn:
            conn.execute('BEGIN IMMEDIATE')
            prior = conn.execute('SELECT tenant,action,target FROM approvals WHERE key=?',
                                 (approval.key,)).fetchone()
            if prior and prior != fields[1:]:
                raise PermissionError('approval key reused')
            conn.execute('''INSERT OR REPLACE INTO approvals
                (key,tenant,action,target,expires_at) VALUES (?,?,?,?,?)''',
                (*fields, self.clock() + ttl_seconds))

    def apply(self, approval):
        fields = (approval.tenant, approval.action, approval.target)
        with closing(sqlite3.connect(self.path)) as conn, conn:
            conn.execute('BEGIN IMMEDIATE')
            prior = conn.execute('SELECT tenant,action,target FROM effects WHERE key=?',
                                 (approval.key,)).fetchone()
            if prior:
                if prior != fields:
                    raise PermissionError('idempotency key reused')
                return 'already_applied'
            granted = conn.execute('SELECT tenant,action,target,expires_at FROM approvals WHERE key=?',
                                   (approval.key,)).fetchone()
            if not granted or granted[:3] != fields or granted[3] <= self.clock():
                raise PermissionError('approval missing, mismatched or expired')
            conn.execute('''INSERT INTO effects (key,tenant,action,target,applied_at)
                VALUES (?,?,?,?,?)''', (approval.key, *fields, self.clock()))
            return 'applied'
