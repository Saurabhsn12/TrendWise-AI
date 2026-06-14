"""
TrendWise AI — News Service
Fetches stock-related news articles using yFinance.
No paid API keys required — uses yFinance's built-in news feed.
"""
import yfinance as yf
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def fetch_stock_news(ticker, max_articles=15):
    """
    Fetch latest news articles for a stock ticker via yFinance.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL')
        max_articles: Maximum number of articles to return

    Returns:
        List of dicts with title, publisher, link, published keys
    """
    try:
        ticker_obj = yf.Ticker(ticker)
        raw_news = ticker_obj.news

        if not raw_news:
            logger.warning(f'No news found for ticker: {ticker}')
            return []

        articles = []
        for item in raw_news[:max_articles]:
            # Handle different yfinance news formats
            title = ''
            publisher = 'Unknown'
            link = '#'
            published = ''

            # yfinance >= 0.2.x format
            if isinstance(item, dict):
                title = item.get('title', '')

                # Some versions nest under 'content'
                if not title and 'content' in item:
                    content = item['content']
                    title = content.get('title', '')
                    publisher = content.get('provider', {}).get('displayName', 'Unknown')
                    link = content.get('canonicalUrl', {}).get('url', '#')
                    pub_date = content.get('pubDate', '')
                    if pub_date:
                        published = pub_date[:19]  # Trim to datetime
                else:
                    publisher = item.get('publisher', 'Unknown')
                    link = item.get('link', '#')

                    # Handle timestamp
                    pub_time = item.get('providerPublishTime', 0)
                    if pub_time:
                        try:
                            published = datetime.fromtimestamp(pub_time).strftime('%Y-%m-%d %H:%M')
                        except (OSError, ValueError):
                            published = ''

            if title:
                articles.append({
                    'title': title,
                    'publisher': publisher,
                    'link': link,
                    'published': published,
                })

        logger.info(f'Fetched {len(articles)} news articles for {ticker}')
        return articles

    except Exception as e:
        logger.error(f'Error fetching news for {ticker}: {e}')
        return []
