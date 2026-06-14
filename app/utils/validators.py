"""
TrendWise AI — Input Validators
Validates user inputs for security and data integrity.
"""
import re
from datetime import datetime


def validate_ticker(ticker):
    """
    Validate stock ticker symbol.
    Supports US tickers (AAPL), Indian NSE (RELIANCE.NS), and BSE (RELIANCE.BO).

    Returns:
        Tuple of (is_valid: bool, cleaned_ticker_or_error: str)
    """
    if not ticker or not isinstance(ticker, str):
        return False, 'Stock ticker is required'

    ticker = ticker.strip().upper()

    # Ticker: 1-20 alphanumeric chars, dots, dashes
    # Supports: AAPL, BRK.B, RELIANCE.NS, BAJAJ-AUTO.NS, TCS.BO
    if not re.match(r'^[A-Z0-9.\-]{1,20}$', ticker):
        return False, 'Invalid ticker format. Examples: AAPL, RELIANCE.NS, TCS.BO'

    return True, ticker


def validate_date_range(start_date, end_date):
    """
    Validate date range for stock analysis.

    Returns:
        Tuple of (is_valid: bool, error_message_or_None)
    """
    if not start_date or not end_date:
        return False, 'Both start date and end date are required'

    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return False, 'Invalid date format. Use YYYY-MM-DD'

    if start >= end:
        return False, 'Start date must be before end date'

    if end > datetime.now():
        return False, 'End date cannot be in the future'

    return True, None


def validate_signup(username, email, password):
    """
    Validate signup form data.

    Returns:
        Tuple of (is_valid: bool, error_message_or_None)
    """
    if not username or len(username.strip()) < 3:
        return False, 'Username must be at least 3 characters'

    if not re.match(r'^[a-zA-Z0-9_]+$', username.strip()):
        return False, 'Username can only contain letters, numbers, and underscores'

    if not email or not re.match(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$', email):
        return False, 'Please enter a valid email address'

    if not password or len(password) < 4:
        return False, 'Password must be at least 4 characters'

    return True, None
