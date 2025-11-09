# db.py - SQLite helpers, users, invoices and audit_log
import sqlite3, os, json, datetime
from contextlib import closing
from decimal import Decimal, getcontext
import secrets, hashlib

getcontext().prec = 28

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DB_PATH = os.path.join(DB_DIR, "invoices.db")

def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    with closing(conn.cursor()) as c:
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT,
            salt TEXT,
            role TEXT
        )""")
        c.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            invoice_id TEXT PRIMARY KEY,
            company TEXT,
            branch TEXT,
            date TEXT,
            recipient TEXT,
            quantity TEXT,
            price TEXT,
            total TEXT,
            notes TEXT
        )""")
        c.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            invoice_id TEXT,
            user TEXT,
            timestamp TEXT,
            details TEXT
        )""")
        conn.commit()
    conn.close()

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def log_action(action, invoice_id=None, user=None, details=None):
    conn = get_conn()
    with closing(conn.cursor()) as c:
        c.execute("INSERT INTO audit_log (action, invoice_id, user, timestamp, details) VALUES (?,?,?,?,?)",
                  (action, invoice_id, user or "anonymous", datetime.datetime.utcnow().isoformat(), json.dumps(details, default=str)))
        conn.commit()
    conn.close()

# User management
def hash_password(password: str, salt: bytes = None):
    if salt is None:
        salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 200000)
    return dk.hex(), salt.hex()

def verify_password(password: str, hash_hex: str, salt_hex: str):
    salt = bytes.fromhex(salt_hex)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 200000)
    return dk.hex() == hash_hex

def create_user(username, password, role="clerk"):
    if not username or not password:
        return False, "username & password required"
    # password complexity
    if len(password) < 8:
        return False, "password min length 8"
    with closing(get_conn().cursor()) as c:
        try:
            h, s = hash_password(password)
            c.execute("INSERT INTO users (username, password_hash, salt, role) VALUES (?,?,?,?)", (username, h, s, role))
            c.connection.commit()
            log_action("create_user", user=username, details={"role": role})
            return True, ""
        except Exception as e:
            return False, str(e)

def get_user(username):
    with closing(get_conn().cursor()) as c:
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        r = c.fetchone()
        if not r:
            return None
        # convert to dict
        cols = [d[0] for d in c.description]
        return dict(zip(cols, r))

# Basic invoices CRUD
def insert_invoice(row, user="system"):
    with closing(get_conn().cursor()) as c:
        c.execute("INSERT OR REPLACE INTO invoices VALUES (?,?,?,?,?,?,?,?,?)", (
            row['invoice_id'], row['company'], row['branch'], row['date'], row['recipient'],
            str(row['quantity']), str(row['price']), str(row['total']), row.get('notes', '')
        ))
        c.connection.commit()
        log_action("insert", invoice_id=row['invoice_id'], user=user, details=row)

def fetch_all():
    import pandas as pd
    df = pd.read_sql_query("SELECT * FROM invoices ORDER BY date DESC", get_conn())
    return df
