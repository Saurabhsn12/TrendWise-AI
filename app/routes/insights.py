"""
TrendWise AI — AI Insights Routes
Provides AI-powered stock insights and recommendations.
Combines: Generative AI (Phase 3) + Recommendation Engine (Phase 4)
"""
from flask import Blueprint, render_template, request, session, current_app
from app.routes.main import login_required
from app.services.stock_service import get_company_info
from app.services.news_service import fetch_stock_news
from app.nlp.sentiment import FinancialSentimentAnalyzer
from app.ai.insight_generator import generate_insight
from app.ai.recommendation_engine import generate_recommendation
from app.utils.validators import validate_ticker

insights_bp = Blueprint('insights', __name__)
analyzer = FinancialSentimentAnalyzer()


@insights_bp.route('/insights', methods=['GET', 'POST'])
@login_required
def ai_insights():
    """
    AI Insights Dashboard.
    Combines company data + sentiment + AI insight + recommendation in one page.
    """
    if request.method == 'POST':
        ticker = request.form.get('ticker', '')

        is_valid, result = validate_ticker(ticker)
        if not is_valid:
            return render_template('insights.html', error=result)

        ticker = result

        try:
            # Step 1: Get company fundamentals
            company = get_company_info(ticker)

            # Step 2: Get sentiment
            articles = fetch_stock_news(ticker)
            sentiment_data = analyzer.analyze_articles(articles) if articles else None
            overall_sentiment = sentiment_data['overall'] if sentiment_data else {}

            # Step 3: Build stock data package
            stock_data = {
                'ticker': ticker,
                'company_name': company['long_name'],
                'sector': company['sector'],
                'industry': company['industry'],
                'current_price': company['current_price'],
                'high': company['fifty_two_week_high'],
                'low': company['fifty_two_week_low'],
                'pe_ratio_forward': company['pe_ratio_forward'],
                'pe_ratio_trailing': company['pe_ratio_trailing'],
                'eps': company['eps'],
                'market_cap': company['market_cap'],
                'dividend_yield': company['dividend_yield'],
                'fifty_two_week_high': company['fifty_two_week_high'],
                'fifty_two_week_low': company['fifty_two_week_low'],
                'sentiment_label': overall_sentiment.get('label', 'N/A'),
                'sentiment_score': overall_sentiment.get('score', 0),
            }

            # Step 4: Generate AI insight
            insight = generate_insight(stock_data)

            # Step 5: Generate recommendation
            recommendation = generate_recommendation(stock_data)

            return render_template(
                'insights.html',
                ticker=ticker,
                company=company,
                insight=insight,
                recommendation=recommendation,
                sentiment=sentiment_data,
                stock_data=stock_data,
            )

        except Exception as e:
            current_app.logger.error(f'Insights error for {ticker}: {e}')
            return render_template('insights.html', ticker=ticker, error=str(e))

    return render_template('insights.html')
