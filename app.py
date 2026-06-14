"""
TrendWise AI — Application Entry Point
Run this file to start the development server.

Usage:
    python app.py
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
