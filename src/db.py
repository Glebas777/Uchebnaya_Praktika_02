import sqlite3
import os
import sys
import hashlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DB_PATH, DB_DIR, DB_TABLES, DEFAULT_USERS


def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def get_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()

    for name, sql in DB_TABLES.items():
        cursor.execute(sql)
        print(f'[db] Таблица "{name}" создана или уже существует')

    for login, password, role in DEFAULT_USERS:
        try:
            cursor.execute(
                'INSERT INTO users (login, password_hash, role) VALUES (?, ?, ?)',
                (login, hash_password(password), role)
            )
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()
    print(f'[db] База данных готова: {DB_PATH}')


def log_syscall(call_name, args, user, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO syscalls_log (call_name, args, user, status) VALUES (?, ?, ?, ?)',
        (call_name, str(args), user, status)
    )
    conn.commit()
    conn.close()


def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, login, role, created_at FROM users ORDER BY id')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def find_user(login):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE login = ?', (login,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


if __name__ == '__main__':
    init_db()