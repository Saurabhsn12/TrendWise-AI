"""
TrendWise AI — Authentication Routes
Handles user signup, login, and logout.
Fixes: Signup now properly saves users to DB. Login redirects correctly.
"""
from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models.database import create_user, verify_user
from app.utils.validators import validate_signup

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    """Landing page with signup form."""
    if session.get('authenticated'):
        return redirect(url_for('main.home'))
    return render_template('index.html')


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    Handle user registration.
    FIX: Original code had form posting to /home with no save logic.
    Now properly validates input, saves to DB, and auto-logs in.
    """
    username = request.form.get('Username', '').strip()
    email = request.form.get('Email', '').strip()
    password = request.form.get('Password', '')

    # Validate input
    is_valid, error = validate_signup(username, email, password)
    if not is_valid:
        return render_template('index.html', error=error)

    # Create user in database
    success, message = create_user(username, email, password)
    if not success:
        return render_template('index.html', error=message)

    # Auto-login after successful signup
    session['username'] = username
    session['authenticated'] = True

    # Fetch user_id for session
    from app.models.database import get_db
    db = get_db()
    user = db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
    if user:
        session['user_id'] = user['id']

    return redirect(url_for('main.home'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.
    FIX: Original redirected to /home-page (non-existent). Now redirects to /home.
    """
    if request.method == 'POST':
        username = request.form.get('Username', '').strip()
        password = request.form.get('Password', '')

        user = verify_user(username, password)
        if user:
            session['username'] = username
            session['user_id'] = user['id']
            session['authenticated'] = True
            return redirect(url_for('main.home'))
        else:
            return render_template('login.html', error='Invalid username or password')

    # Already logged in? Go to home
    if session.get('authenticated'):
        return redirect(url_for('main.home'))

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """Handle user logout and clear session."""
    session.clear()
    return redirect(url_for('auth.login'))
