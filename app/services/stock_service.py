"""
TrendWise AI — Stock Service
Handles all stock data fetching and processing via yFinance.
"""
import yfinance as yf
import pandas as pd
import requests

# Create a custom session to bypass Yahoo Finance rate limits
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})


def fetch_stock_data(ticker, start_date, end_date):
    """
    Fetch historical stock data from yFinance.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL')
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)

    Returns:
        pandas DataFrame with stock data

    Raises:
        ValueError: If no data is found for the given ticker/dates
    """
    df = yf.download(ticker, start=start_date, end=end_date, session=session)

    if df.empty:
        raise ValueError(
            f"No data found for ticker '{ticker}' between {start_date} and {end_date}. "
            f"Please check the ticker symbol and date range."
        )

    return df


def get_company_info(ticker):
    """
    Get detailed company information from yFinance.

    Args:
        ticker: Stock ticker symbol

    Returns:
        Dictionary with company details
    """
    ticker_obj = yf.Ticker(ticker, session=session)
    info = ticker_obj.get_info()

    # Safely get CEO name
    officers = info.get('companyOfficers', [])
    ceo = officers[0].get('name') if officers else None

    # Build headquarters string
    city = info.get('city')
    country = info.get('country')
    headquarters = f"{city}, {country}" if city and country else None

    return {
        'long_name': info.get('longName', ticker),
        'sector': info.get('sector', 'N/A'),
        'industry': info.get('industry', 'N/A'),
        'ceo': ceo or 'N/A',
        'headquarters': headquarters or 'N/A',
        'market_cap': info.get('marketCap'),
        'pe_ratio_forward': info.get('forwardPE'),
        'pe_ratio_trailing': info.get('trailingPE'),
        'eps': info.get('trailingEps'),
        'dividend_yield': info.get('dividendYield'),
        'fifty_two_week_high': info.get('fiftyTwoWeekHigh'),
        'fifty_two_week_low': info.get('fiftyTwoWeekLow'),
        'current_price': info.get('currentPrice') or info.get('regularMarketPrice'),
        'previous_close': info.get('previousClose'),
        'volume': info.get('volume'),
    }


def get_price_extremes(df):
    """
    Get highest high and lowest low from stock data.

    Args:
        df: pandas DataFrame with 'High' and 'Low' columns

    Returns:
        Tuple of (high, low) rounded to 2 decimal places
    """
    high_val = df['High'].max()
    low_val = df['Low'].min()

    # Handle both single-level and multi-level column indices (yfinance versions)
    if hasattr(high_val, 'iloc'):
        high_val = high_val.iloc[0]
    if hasattr(low_val, 'iloc'):
        low_val = low_val.iloc[0]

    return round(float(high_val), 2), round(float(low_val), 2)
