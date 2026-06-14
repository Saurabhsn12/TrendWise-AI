# 🚀 TrendWise AI

**Intelligent Stock Market Analysis and Financial Insight Platform**

> A full-stack AI-powered stock analysis platform built with Flask, featuring NLP sentiment analysis, machine learning predictions, AI-driven recommendations, and professional PDF report generation.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Screenshots](#-screenshots)
- [Indian Stock Market Support](#-indian-stock-market-support)
- [Author](#-author)

---

## ✨ Features

### 📊 Stock Analysis
- Real-time stock data fetching via **yFinance**
- Interactive charts with **Close**, **High**, **Low**, and **Combined** views
- **SMA** (Simple Moving Average) and **EMA** (Exponential Moving Average) indicators
- Company fundamental data: P/E ratio, EPS, market cap, dividend yield

### 🤖 AI-Powered Insights (Phase 3)
- **Dual-provider architecture**: Google Gemini API (primary) + Local Analysis Engine (fallback)
- 5-section analysis: Market Summary, Trend, Technical, Risk, Opportunity
- Works completely offline with the local engine — no API key required

### 💡 Stock Recommendation Engine (Phase 4)
- **6-factor weighted scoring model**:
  - Valuation (P/E Ratio) — Weight: 2.0
  - Earnings (EPS) — Weight: 1.5
  - Price Position (52-Week Range) — Weight: 1.5
  - Dividend Yield — Weight: 1.0
  - Earnings Growth (Forward vs Trailing P/E) — Weight: 2.0
  - Market Sentiment (NLP-derived) — Weight: 1.5
- Output: **Strong Buy / Buy / Hold / Watch / Sell** with confidence percentage
- Explainable reasoning for transparency

### 📰 NLP Sentiment Analysis (Phase 2)
- **VADER** (Valence Aware Dictionary and sEntiment Reasoner) for sentiment scoring
- **TextBlob** for polarity and subjectivity analysis
- Real-time news fetching from yFinance
- Sentiment dashboard with Plotly visualizations

### 📈 Price Prediction
- **ARIMA** (Auto-Regressive Integrated Moving Average) model
- Next-day price prediction with statistical confidence

### 📄 PDF Report Generation (Phase 6)
- Professional multi-page branded PDF reports
- Sections: Cover page, Company overview, Financial metrics, AI analysis, Factor breakdown, Sentiment, Disclaimer
- One-click download from the Insights page

### 🔐 Security
- Werkzeug password hashing (PBKDF2-SHA256)
- Session-based authentication with security headers
- Input validation and sanitization
- SQL injection protection via parameterized queries

### 🌐 REST API
- Swagger-documented API at `/api/docs`
- Endpoints for stock analysis and company info
- JSON responses for external integration

### 🔍 Smart Search
- Auto-complete stock suggestions as you type
- 50+ Indian NSE stocks + 25+ US stocks in the database
- Keyboard navigation support (Arrow keys + Enter)

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.11, Flask 3.1 |
| **Frontend** | HTML5, CSS3, Bootstrap 5, Jinja2 |
| **Database** | SQLite3 |
| **Data** | yFinance, Pandas, NumPy |
| **Visualization** | Matplotlib, Plotly, Seaborn |
| **NLP** | VADER Sentiment, TextBlob, NLTK |
| **ML/Stats** | scikit-learn, statsmodels, pmdarima (ARIMA) |
| **AI** | Google Gemini API (optional), Local Rule Engine |
| **PDF** | fpdf2 |
| **API** | Flask-RESTX (Swagger) |
| **Deployment** | Gunicorn, Heroku/Railway ready |

---

## 🏗 Architecture

```
TrendWise-main/
├── app/                          # Application Package
│   ├── __init__.py               # App Factory (create_app)
│   ├── ai/                       # AI Module
│   │   ├── insight_generator.py  # Gemini + Local AI Engine
│   │   └── recommendation_engine.py  # 6-Factor Scoring
│   ├── nlp/                      # NLP Module
│   │   └── sentiment.py          # VADER + TextBlob Analyzer
│   ├── models/                   # Data Layer
│   │   └── database.py           # SQLite ORM, User CRUD
│   ├── services/                 # Business Logic
│   │   ├── stock_service.py      # yFinance Data Fetching
│   │   ├── chart_service.py      # Matplotlib Charts
│   │   ├── news_service.py       # News Feed Scraping
│   │   └── report_service.py     # PDF Report Generator
│   ├── routes/                   # Flask Blueprints (8)
│   │   ├── auth.py               # Signup, Login, Logout
│   │   ├── main.py               # Home, Dashboard, Intro
│   │   ├── analysis.py           # Stock Analysis + Charts
│   │   ├── prediction.py         # ARIMA Prediction
│   │   ├── sentiment.py          # NLP Sentiment Dashboard
│   │   ├── insights.py           # AI Insights + Recommendation
│   │   ├── reports.py            # PDF Report Download
│   │   └── api.py                # REST API (Swagger)
│   ├── utils/                    # Utilities
│   │   └── validators.py         # Input Validation
│   ├── templates/                # Jinja2 Templates (9)
│   └── static/                   # CSS, JS, Images
├── config.py                     # Configuration Module
├── app.py                        # Development Entry Point
├── wsgi.py                       # Production Entry (Gunicorn)
├── requirements.txt              # Python Dependencies
├── Procfile                      # Heroku/Railway Deployment
└── .env.example                  # Environment Template
```

### Design Patterns Used
- **App Factory Pattern** — Modular Flask initialization
- **Blueprint Pattern** — Route organization (8 blueprints)
- **Service Layer Pattern** — Business logic separation
- **Provider Pattern** — AI backend switching (Gemini/Local)
- **Decorator Pattern** — `@login_required` authentication

---

## 🚀 Installation

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-username/TrendWise-AI.git
cd TrendWise-AI

# 2. Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate     # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment (optional)
copy .env.example .env
# Edit .env with your settings

# 5. Run the application
python app.py
```

Open **http://localhost:5000** in your browser.

---

## 📱 Usage

1. **Sign Up** → Create an account at the homepage
2. **Login** → Enter credentials
3. **Analyze** → Enter a stock ticker (e.g., `AAPL`, `RELIANCE.NS`) with date range
4. **View Charts** → See Close, High, Low, and Combined price charts
5. **Predict** → Click "Predict Next Day Price" for ARIMA prediction
6. **Sentiment** → Navigate to Sentiment tab for NLP news analysis
7. **AI Insights** → Get Buy/Hold/Sell recommendation with confidence score
8. **Download PDF** → Generate and download a professional analysis report

---

## 📡 API Documentation

Visit **http://localhost:5000/api/docs** for interactive Swagger documentation.

### Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/stocks/analyze` | POST | Analyze a stock with date range |
| `/api/stocks/info/<ticker>` | GET | Get company information |

---

## 🇮🇳 Indian Stock Market Support

TrendWise AI fully supports Indian stocks:

| Exchange | Suffix | Example |
|----------|--------|---------|
| **NSE** (National Stock Exchange) | `.NS` | `RELIANCE.NS`, `TCS.NS`, `INFY.NS` |
| **BSE** (Bombay Stock Exchange) | `.BO` | `RELIANCE.BO`, `TCS.BO`, `INFY.BO` |

The auto-suggest feature includes 50+ popular Indian stocks. Just start typing!

---

## 🧠 Key Technical Concepts (Viva Ready)

| Topic | What to Explain |
|-------|----------------|
| **App Factory** | `create_app()` creates Flask app, registers blueprints, initializes DB |
| **Blueprints** | Modular route organization — 8 separate modules |
| **VADER Sentiment** | Lexicon-based, rule-augmented for social media/news text |
| **Recommendation Engine** | Weighted multi-factor scoring: Valuation, Earnings, Position, Dividends, Growth, Sentiment |
| **Provider Pattern** | Switch AI backends (Gemini/Local) without changing business logic |
| **Password Hashing** | Werkzeug PBKDF2-SHA256, never stores plaintext |
| **ARIMA Model** | Auto-regressive model for time-series forecasting |
| **REST API** | Flask-RESTX with Swagger auto-documentation |

---

## 👤 Author

**Saurabh Nehra**

- 📧 Email: [saurabhnehra44@gmail.com](mailto:saurabhnehra44@gmail.com)
- 📍 Location: Rajasthan, India
- 🎓 B.Tech Computer Science (Final Year)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

*(Originally developed for educational and academic purposes as a Final Year B.Tech project)*

---

## 🙏 Acknowledgements

- [yFinance](https://github.com/ranaroussi/yfinance) — Stock data
- [VADER Sentiment](https://github.com/cjhutto/vaderSentiment) — Sentiment analysis
- [Flask](https://flask.palletsprojects.com/) — Web framework
- [Plotly](https://plotly.com/) — Interactive charts
- [Bootstrap](https://getbootstrap.com/) — UI framework

---

> **Disclaimer**: TrendWise AI is an educational project. It does not constitute financial advice. Always consult a qualified financial advisor before making investment decisions.
