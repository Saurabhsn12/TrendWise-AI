"""
TrendWise AI — Report Routes
Handles PDF report generation and download.
"""
from flask import Blueprint, request, send_file, render_template, session, current_app
import os
from app.routes.main import login_required
from app.services.stock_service import get_company_info
from app.services.news_service import fetch_stock_news
from app.nlp.sentiment import FinancialSentimentAnalyzer
from app.ai.insight_generator import generate_insight
from app.ai.recommendation_engine import generate_recommendation
from app.services.report_service import generate_pdf_report
from app.utils.validators import validate_ticker

reports_bp = Blueprint('reports', __name__)
analyzer = FinancialSentimentAnalyzer()


@reports_bp.route('/report/generate', methods=['POST'])
@login_required
def generate_report():
    """
    Generate a comprehensive PDF report for a stock.
    Combines all analysis modules into a single downloadable report.
    """
    ticker = request.form.get('ticker', '')

    is_valid, result = validate_ticker(ticker)
    if not is_valid:
        return render_template('insights.html', error=result)

    ticker = result

    try:
        # Gather all data
        company = get_company_info(ticker)
        articles = fetch_stock_news(ticker)
        sentiment_data = analyzer.analyze_articles(articles) if articles else None
        overall_sentiment = sentiment_data['overall'] if sentiment_data else {}

        stock_data = {
            'ticker': ticker,
            'company_name': company['long_name'],
            'sector': company['sector'],
            'industry': company['industry'],
            'current_price': company['current_price'],
            'high': company.get('fifty_two_week_high'),
            'low': company.get('fifty_two_week_low'),
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

        insight = generate_insight(stock_data)
        recommendation = generate_recommendation(stock_data)

        # Generate PDF
        report_path = generate_pdf_report(
            ticker, company, insight, recommendation, sentiment_data
        )

        # Return as download
        full_path = os.path.join(current_app.root_path, 'static', report_path)
        return send_file(
            full_path,
            as_attachment=True,
            download_name=os.path.basename(report_path),
            mimetype='application/pdf',
        )

    except Exception as e:
        current_app.logger.error(f'Report generation error for {ticker}: {e}')
        return render_template('insights.html', ticker=ticker, error=f'Report generation failed: {str(e)}')
