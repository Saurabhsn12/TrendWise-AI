"""
TrendWise AI — Main Routes
Handles home page, intro, dashboard, and miscellaneous pages.
"""
from flask import Blueprint, render_template, session, redirect, url_for
from functools import wraps

main_bp = Blueprint('main', __name__)


def login_required(f):
    """Decorator to require authentication for protected routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@main_bp.route('/home')
@login_required
def home():
    """
    Main home page with stock search form.
    FIX: Original crashed with KeyError when session['username'] was missing.
    Now uses session.get() with a default value.
    """
    username = session.get('username', 'User')
    return render_template('home.html', username=username)


@main_bp.route('/intro')
def intro():
    """Introduction / About page — publicly accessible."""
    return render_template('intro.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """
    User dashboard with real data:
    - Recent search history
    - Feature quick-access cards
    """
    from app.models.database import get_search_history, get_favorites

    username = session.get('username', 'User')
    user_id = session.get('user_id')

    # Get real data from database
    search_history = []
    favorites = []
    if user_id:
        search_history = get_search_history(user_id, limit=10)
        favorites = get_favorites(user_id)

    return render_template(
        'dashboard.html',
        username=username,
        search_history=search_history,
        favorites=favorites,
    )


@main_bp.route('/mistake')
def mistake():
    """Redirect page for unauthenticated access attempts."""
    return (
        '<div style="text-align:center;padding:80px;font-family:Segoe UI,sans-serif">'
        '<h1 style="color:#3e2723">Please Sign Up or Login First</h1>'
        '<p><a href="/" style="color:#6c4f3d">Go to Signup</a> | '
        '<a href="/login" style="color:#6c4f3d">Go to Login</a></p></div>'
    )
