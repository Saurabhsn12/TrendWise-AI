"""
TrendWise AI — WSGI Entry Point
Used by Gunicorn / production WSGI servers.
"""
from app import create_app

app = create_app()
