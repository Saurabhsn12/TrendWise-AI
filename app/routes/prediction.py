"""
TrendWise AI — Stock Prediction Routes
Handles ARIMA-based stock price prediction.
Fixed: yFinance multi-level column handling for newer versions.
"""
import io
import base64

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import yfinance as yf
from flask import Blueprint, render_template, current_app
from pmdarima import auto_arima
from statsmodels.tsa.stattools import adfuller

prediction_bp = Blueprint('prediction', __name__)


@prediction_bp.route('/predict/<ticker>')
def predict_stock(ticker):
    """
    Predict next day stock price using ARIMA model.

    Args:
        ticker: Stock ticker symbol from URL
    """
    try:
        # Step 1: Download 1 year of stock data
        df = yf.download(ticker, period='1y', progress=False)

        # FIX: Handle multi-level columns from newer yfinance
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        if 'Close' not in df.columns:
            raise ValueError(f'No Close price data found for {ticker}')

        df = df[['Close']].dropna()
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
        df = df.dropna()
        df = df.round(2)

        if len(df) < 30:
            raise ValueError(f'Insufficient data for {ticker}. Need at least 30 days, got {len(df)}.')

        # Step 2: Test stationarity to determine differencing parameter
        close_values = df['Close'].values.flatten()
        stationarity = _test_stationarity(close_values)
        d = 0 if stationarity == 'Stationary' else 1

        # Step 3: Fit ARIMA model
        model = auto_arima(
            close_values,
            start_p=0, start_q=0,
            max_p=5, max_q=5,
            d=d,
            seasonal=False,
            stepwise=True,
            trace=False,
            suppress_warnings=True,
        )

        # Step 4: Forecast next day
        forecast_value = float(model.predict(n_periods=1)[0])

        # Step 5: Get last known price
        last_price = float(close_values[-1])
        change_pct = ((forecast_value - last_price) / last_price) * 100

        # Step 6: Generate forecast visualization
        img_base64 = _generate_forecast_plot(df, ticker, forecast_value)

        return render_template(
            'predict.html',
            ticker=ticker,
            forecast=round(forecast_value, 2),
            last_price=round(last_price, 2),
            change_pct=round(change_pct, 2),
            direction='up' if change_pct > 0 else 'down',
            plot_url=img_base64,
            arima_order=str(model.order),
        )

    except Exception as e:
        current_app.logger.error(f'Prediction error for {ticker}: {e}')
        return render_template(
            'predict.html',
            ticker=ticker,
            forecast='N/A',
            last_price=None,
            change_pct=None,
            direction=None,
            plot_url=None,
            error=str(e),
            arima_order=None,
        )


def _test_stationarity(values):
    """
    Test stationarity using Augmented Dickey-Fuller test.

    Returns:
        'Stationary' or 'Non-Stationary'
    """
    try:
        adft = adfuller(values, autolag='AIC')
        p_value = adft[1]
        return 'Stationary' if p_value < 0.05 else 'Non-Stationary'
    except Exception:
        return 'Non-Stationary'


def _generate_forecast_plot(df, ticker, forecast):
    """
    Generate a forecast plot showing recent prices + predicted next day.

    Returns:
        Base64-encoded PNG image string
    """
    recent = df['Close'][-60:]
    dates = recent.index
    values = recent.values.flatten()

    forecast_date = dates[-1] + pd.Timedelta(days=1)
    last_price = float(values[-1])

    fig, ax = plt.subplots(figsize=(12, 5))

    # Plot recent prices
    ax.plot(dates, values, label='Recent Close', color='#1565c0', linewidth=2, alpha=0.9)

    # Fill under the curve
    ax.fill_between(dates, values, alpha=0.1, color='#1565c0')

    # Plot forecast
    color = '#2e7d32' if forecast > last_price else '#c62828'
    ax.plot(
        [dates[-1], forecast_date],
        [last_price, forecast],
        label=f'Forecast: ${forecast:.2f}', color=color,
        marker='o', linewidth=2.5, markersize=10, zorder=5,
    )

    # Styling
    ax.set_title(f'{ticker} — Next Day Price Prediction', fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Close Price', fontsize=12)
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#fafafa')
    fig.patch.set_facecolor('#fafafa')
    plt.tight_layout()

    # Convert to base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120, bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('ascii')
