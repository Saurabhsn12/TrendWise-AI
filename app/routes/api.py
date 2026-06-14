"""
TrendWise AI — REST API Routes
Provides JSON API endpoints with Swagger documentation at /api/docs.
"""
from flask import Blueprint
from flask_restx import Api, Resource, fields
from app.services.stock_service import fetch_stock_data, get_company_info, get_price_extremes

api_bp = Blueprint('api', __name__, url_prefix='/api')

api = Api(
    api_bp,
    version='1.0',
    title='TrendWise AI API',
    description='Intelligent Stock Market Analysis REST API',
    doc='/docs',
)

# ── Namespaces ────────────────────────────────────────────────────
stock_ns = api.namespace('stocks', description='Stock analysis operations')

# ── Request / Response Models ─────────────────────────────────────
analysis_input = api.model('AnalysisInput', {
    'ticker': fields.String(required=True, description='Stock ticker symbol', example='AAPL'),
    'start_date': fields.String(required=True, description='Start date (YYYY-MM-DD)', example='2024-01-01'),
    'end_date': fields.String(required=True, description='End date (YYYY-MM-DD)', example='2024-12-31'),
})


@stock_ns.route('/analyze')
class StockAnalysis(Resource):
    """Analyze a stock by ticker and date range."""

    @stock_ns.expect(analysis_input)
    @stock_ns.doc(description='Perform stock analysis and return JSON results')
    def post(self):
        """Analyze stock performance over a date range."""
        ticker = api.payload.get('ticker')
        start_date = api.payload.get('start_date')
        end_date = api.payload.get('end_date')

        try:
            df = fetch_stock_data(ticker, start_date, end_date)
            high, low = get_price_extremes(df)
            company = get_company_info(ticker)

            return {
                'ticker': ticker,
                'company_name': company['long_name'],
                'period': {'start': start_date, 'end': end_date},
                'price_range': {'high': high, 'low': low},
                'company_info': company,
                'status': 'success',
            }
        except Exception as e:
            return {'error': str(e), 'status': 'error'}, 400


@stock_ns.route('/info/<string:ticker>')
class StockInfo(Resource):
    """Get company information for a stock ticker."""

    @stock_ns.doc(description='Get detailed company information')
    def get(self, ticker):
        """Retrieve company fundamentals."""
        try:
            company = get_company_info(ticker)
            return {'ticker': ticker, 'info': company, 'status': 'success'}
        except Exception as e:
            return {'error': str(e), 'status': 'error'}, 400
