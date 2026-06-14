"""
TrendWise AI — Database Module
Handles SQLite database connections and schema initialization.
Designed for easy migration to PostgreSQL in the future.
"""
import sqlite3
from flask import g, current_app
from werkzeug.security import generate_password_hash, check_password_hash


# ─── Connection Management ────────────────────────────────────────

def get_db():
    """Get database connection for the current request context."""
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE_PATH'])
        g.db.row_factory = sqlite3.Row  # Return rows as dictionaries
    return g.db


def close_db(e=None):
    """Close database connection at end of request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db(app):
    """Initialize the database schema with all required tables."""
    with app.app_context():
        db = sqlite3.connect(app.config['DATABASE_PATH'])
        cursor = db.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Search history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                ticker TEXT NOT NULL,
                start_date TEXT,
                end_date TEXT,
                searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # Favorite stocks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS favorite_stocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                ticker TEXT NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, ticker)
            )
        ''')

        db.commit()
        db.close()


# ─── User Operations ──────────────────────────────────────────────

def create_user(username, email, password):
    """
    Create a new user with hashed password.

    Returns:
        Tuple of (success: bool, message: str)
    """
    db = get_db()
    hashed = generate_password_hash(password)
    try:
        db.execute(
            'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
            (username, email, hashed)
        )
        db.commit()
        return True, 'User created successfully'
    except sqlite3.IntegrityError as e:
        if 'username' in str(e):
            return False, 'Username already exists'
        elif 'email' in str(e):
            return False, 'Email already registered'
        return False, 'Registration failed'


def verify_user(username, password):
    """
    Verify user credentials.

    Returns:
        User dict if valid, None otherwise
    """
    db = get_db()
    user = db.execute(
        'SELECT * FROM users WHERE username = ?', (username,)
    ).fetchone()

    if user and check_password_hash(user['password'], password):
        return dict(user)
    return None


def get_user_by_id(user_id):
    """Get user by ID."""
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    return dict(user) if user else None


# ─── Search History Operations ─────────────────────────────────────

def save_search(user_id, ticker, start_date=None, end_date=None):
    """Save a stock search to history."""
    db = get_db()
    db.execute(
        'INSERT INTO search_history (user_id, ticker, start_date, end_date) VALUES (?, ?, ?, ?)',
        (user_id, ticker, start_date, end_date)
    )
    db.commit()


def get_search_history(user_id, limit=20):
    """Get recent search history for a user."""
    db = get_db()
    rows = db.execute(
        'SELECT * FROM search_history WHERE user_id = ? ORDER BY searched_at DESC LIMIT ?',
        (user_id, limit)
    ).fetchall()
    return [dict(row) for row in rows]


# ─── Favorite Stocks Operations ───────────────────────────────────

def add_favorite(user_id, ticker):
    """Add a stock to user's favorites. Returns True if added, False if already exists."""
    db = get_db()
    try:
        db.execute(
            'INSERT INTO favorite_stocks (user_id, ticker) VALUES (?, ?)',
            (user_id, ticker)
        )
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def remove_favorite(user_id, ticker):
    """Remove a stock from user's favorites."""
    db = get_db()
    db.execute(
        'DELETE FROM favorite_stocks WHERE user_id = ? AND ticker = ?',
        (user_id, ticker)
    )
    db.commit()


def get_favorites(user_id):
    """Get all favorite stocks for a user."""
    db = get_db()
    rows = db.execute(
        'SELECT * FROM favorite_stocks WHERE user_id = ? ORDER BY added_at DESC',
        (user_id,)
    ).fetchall()
    return [dict(row) for row in rows]
