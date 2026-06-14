"""
TrendWise AI — Sentiment Analysis Routes
Provides sentiment analysis dashboard for stock-related news.
"""
from flask import Blueprint, render_template, request, session
from app.routes.main import login_required
from app.nlp.sentiment import FinancialSentimentAnalyzer
from app.services.news_service import fetch_stock_news
from app.utils.validators import validate_ticker

sentiment_bp = Blueprint('sentiment', __name__)

# Initialize analyzer once (singleton pattern)
analyzer = FinancialSentimentAnalyzer()


@sentiment_bp.route('/sentiment', methods=['GET', 'POST'])
@login_required
def sentiment_dashboard():
    """
    Sentiment analysis dashboard.
    GET: Shows form to enter ticker.
    POST: Fetches news, analyzes sentiment, displays results.
    """
    if request.method == 'POST':
        ticker = request.form.get('ticker', '')

        # Validate
        is_valid, result = validate_ticker(ticker)
        if not is_valid:
            return render_template('sentiment.html', error=result)

        ticker = result

        # Fetch news
        articles = fetch_stock_news(ticker)
        if not articles:
            return render_template(
                'sentiment.html',
                ticker=ticker,
                error=f'No news articles found for {ticker}. Try a major stock like AAPL, TSLA, or GOOGL.',
            )

        # Analyze sentiment
        sentiment_data = analyzer.analyze_articles(articles)

        return render_template(
            'sentiment.html',
            ticker=ticker,
            sentiment=sentiment_data,
        )

    return render_template('sentiment.html')


@sentiment_bp.route('/sentiment/<ticker>')
@login_required
def sentiment_for_ticker(ticker):
    """Direct sentiment analysis via URL (linked from analysis page)."""
    is_valid, result = validate_ticker(ticker)
    if not is_valid:
        return render_template('sentiment.html', error=result)

    ticker = result
    articles = fetch_stock_news(ticker)

    if not articles:
        return render_template(
            'sentiment.html',
            ticker=ticker,
            error=f'No news articles found for {ticker}.',
        )

    sentiment_data = analyzer.analyze_articles(articles)

    return render_template(
        'sentiment.html',
        ticker=ticker,
        sentiment=sentiment_data,
    )
