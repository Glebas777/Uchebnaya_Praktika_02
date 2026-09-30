import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, 'db')
DB_PATH = os.path.join(DB_DIR, 'os.sqlite')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

PYTHON_MIN_VERSION = (3, 10)

DB_TABLES = {
    'users': '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''',
    'processes': '''
        CREATE TABLE IF NOT EXISTS processes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            state TEXT NOT NULL,
            owner TEXT NOT NULL,
            memory INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''',
    'files': '''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE NOT NULL,
            content TEXT DEFAULT '',
            owner TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''',
    'syscalls_log': '''
        CREATE TABLE IF NOT EXISTS syscalls_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            call_name TEXT NOT NULL,
            args TEXT,
            user TEXT,
            status TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    '''
}

DEFAULT_USERS = [
    ('admin', 'admin', 'administrator'),
    ('user', 'user', 'user'),
]