"""
TrendWise AI — Application Factory
Creates and configures the Flask application instance.
"""
import os
import logging
from flask import Flask
from config import Config


def create_app(config_class=Config):
    """
    Create and configure the Flask application.

    Args:
        config_class: Configuration class to use (default: Config)

    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ── Configure logging ─────────────────────────────────────
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    )
    app.logger.info('TrendWise AI starting up...')

    # ── Download NLTK data (needed for TextBlob/VADER) ─────────
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
    except Exception:
        pass  # Don't crash if NLTK download fails

    # ── Ensure required directories exist ─────────────────────
    os.makedirs(os.path.join(app.static_folder, 'images'), exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'reports'), exist_ok=True)

    # ── Initialize database ───────────────────────────────────
    from app.models.database import init_db, close_db
    init_db(app)
    app.teardown_appcontext(close_db)

    # ── Register Blueprints ───────────────────────────────────
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.analysis import analysis_bp
    from app.routes.prediction import prediction_bp
    from app.routes.api import api_bp
    from app.routes.sentiment import sentiment_bp
    from app.routes.insights import insights_bp
    from app.routes.reports import reports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(sentiment_bp)
    app.register_blueprint(insights_bp)
    app.register_blueprint(reports_bp)

    # ── Error handlers ────────────────────────────────────────
    _register_error_handlers(app)

    app.logger.info('TrendWise AI ready.')
    return app


def _register_error_handlers(app):
    """Register custom error handlers."""

    @app.errorhandler(404)
    def not_found(e):
        return (
            '<div style="text-align:center;padding:80px;font-family:-apple-system,sans-serif;'
            'background:#131722;color:#d1d4dc;min-height:100vh">'
            '<h1 style="color:#ef5350;font-size:2rem;font-weight:700">404</h1>'
            '<p style="color:#787b86">Page not found</p>'
            '<a href="/" style="color:#2962ff">&larr; Go Home</a></div>'
        ), 404

    @app.errorhandler(500)
    def server_error(e):
        app.logger.error(f'Server error: {e}')
        return (
            '<div style="text-align:center;padding:80px;font-family:-apple-system,sans-serif;'
            'background:#131722;color:#d1d4dc;min-height:100vh">'
            '<h1 style="color:#ef5350;font-size:2rem;font-weight:700">500</h1>'
            '<p style="color:#787b86">Something went wrong</p>'
            '<a href="/" style="color:#2962ff">&larr; Go Home</a></div>'
        ), 500
