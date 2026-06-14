import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, session, jsonify, redirect, url_for
import yfinance as yf
import os
from functools import wraps
import requests
import time
import datetime

app = Flask(__name__)
from extra_stuff import show_close_plot, show_combine_plot, show_high_plot, show_low_plot
app.secret_key = 'your_secret_key'
from flask_restx import Api, Resource, fields

def get_symbol_from_name(company_name):
    api_key = "YOUR_ALPHA_VANTAGE_API_KEY"
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={company_name}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if "bestMatches" in data and data["bestMatches"]:
        return data["bestMatches"][0]["1. symbol"]  # most relevant match
    else:
        return None

global_data = {}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return render_template('login.html', error=None)
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def home():
    """
    This function renders the home page of the application.

    Returns:
        render_template: The rendered HTML template for the home page.
    """
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("Username")
        password = request.form.get("Password")

        conn = sqlite3.connect("trendwise.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result and check_password_hash(result[0], password):
            session["username"] = username
            session["authenticated"] = True
            return redirect("/home-page")
        else:
            return render_template("login.html", error="Invalid username or password")
    
    # For GET (i.e., just visiting /login)
    return render_template("login.html")







@app.route('/dashboard')
def dashboard():
    if not session.get('authenticated'):
        return redirect('/login')
    
    username = session.get('username', 'User')

    dates = ["2025-07-01", "2025-07-02", "2025-07-03"]
    prices = [100, 110, 120]

    return render_template("dashboard.html", username=username, dates=dates, prices=prices)


@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    image_folder = os.path.join(app.root_path, 'static')
    for file in os.listdir(image_folder):
        if file.endswith('.png'):
            os.remove(os.path.join(image_folder, file))
    return redirect(url_for('login'))



api = Api(app, version="1.0", title="Stock Analysis API", description="A simple Stock Analysis API", doc="/docs")

index_np = api.namespace("Index", description="Index operations", path="/index")
analysis_np = api.namespace("Analysis", description="Analysis operations", path="/analysis")
login_np = api.namespace("Login", description="Login operations", path="/login")

input_model = api.model("InputModel", {
    "stockname": fields.String(required=True, description="Stock name"),
    "startDate": fields.String(required=True, description="Start date in YYYY-MM-DD format"),
    "endDate": fields.String(required=True, description="End date in YYYY-MM-DD format")
})

# home_np = api.namespace("Home", description="Home operations", path="/home-api")

# @home_np.route("/", methods=["POST"])
# class HomeResource(Resource):
#     def post(self):
#         return {"message": "Welcome to the Stock Analysis API!"}


@index_np.route("/")
class IndexResource(Resource):
  def get(self):
    """
    API Home Endpoint

    Returns a message informing users that the home page is a sign-up page and they must fill in the required entries.
    """
    return {
      "message": "Welcome to TrendWise! Please visit the home page (/) and fill in all required fields to sign up."
    }



@analysis_np.route("/")
class AnalysisResource(Resource):
  @analysis_np.expect(input_model)
  def post(self):
    """
     Perform stock analysis based on user input.
     This endpoint allows users to input a stock name and a date range,
     and it returns an analysis of the stock's performance during that period.
    **Request Body:**
      - `stockname`: (str) The stock name to analyze.
      - `startDate`: (str) The start date for the analysis in YYYY-MM-DD format.
      - `endDate`: (str) The end date for the analysis in YYYY-MM-DD format.
    **Returns**:
        `str`: Rendered HTML template with stock analysis results.
    """
    stockname = api.payload.get("stockname")
    startDate = api.payload.get("startDate")
    endDate = api.payload.get("endDate")
    df = yf.download(stockname, start= f"{startDate}", end= f"{endDate}")
    high = round(df["High"].max(), 2)
    low = round(df["Low"].min(), 2)

    show_close_plot(df)
    show_combine_plot(df)
    show_high_plot(df)
    show_low_plot(df)
    ticker = yf.Ticker(stockname)
    info = ticker.get_info()
    og_name = info.get("longName")
    
    
    sector = info.get("sector")
    industry = info.get("industry")
    ceo = info.get("companyOfficers", [{}])[0].get("name")
    headquarters = f"{info.get('city')}, {info.get('country')}" if info.get("city") and info.get("country") else None

    market_cap = info.get("marketCap")
    pe_ratio_forward = info.get("forwardPE")
    pe_ratio_trailing = info.get("trailingPE")
    eps = info.get("trailingEps")
    dividend_yield = info.get("dividendYield")
    fifty_two_week_high = info.get("fiftyTwoWeekHigh")
    fifty_two_week_low = info.get("fiftyTwoWeekLow")

    return render_template("analysis.html", stockname=stockname, startDate=startDate, endDate=endDate, high=high, low=low, og_name=og_name, sector=sector, industry=industry, ceo=ceo, headquarters=headquarters, market_cap=market_cap, pe_ratio_forward=pe_ratio_forward, pe_ratio_trailing=pe_ratio_trailing, eps=eps, dividend_yield=dividend_yield, fifty_two_week_high=fifty_two_week_high, fifty_two_week_low=fifty_two_week_low)



@app.route("/home", methods=["GET", "POST"])
def home_page():
    return render_template("home.html", username=session["username"])




@app.route("/mistake")
def mistake():
  return "<h1>Kindly Sign-up First</h1>"

@app.route("/analysis", methods=["POST"])
def mainpage():
    stockname = request.form.get("stockname")
    startDate = request.form.get("startDate")
    endDate = request.form.get("endDate")

    df = yf.download(stockname, start=startDate, end=endDate)

    high = round(df["High"].max().iloc[0], 2)
    low = round(df["Low"].min().iloc[0], 2)

    # Generate plots and get filenames
    close_img = show_close_plot(df, stockname, startDate, endDate)
    high_img = show_high_plot(df, stockname, startDate, endDate)
    low_img = show_low_plot(df, stockname, startDate, endDate)
    combined_img = show_combine_plot(df, stockname, startDate, endDate)

    ticker = yf.Ticker(stockname)
    info = ticker.get_info()
    og_name = info.get("longName")

    sector = info.get("sector")
    industry = info.get("industry")
    ceo = info.get("companyOfficers", [{}])[0].get("name")
    headquarters = f"{info.get('city')}, {info.get('country')}" if info.get("city") and info.get("country") else None

    market_cap = info.get("marketCap")
    pe_ratio_forward = info.get("forwardPE")
    pe_ratio_trailing = info.get("trailingPE")
    eps = info.get("trailingEps")
    dividend_yield = info.get("dividendYield")
    fifty_two_week_high = info.get("fiftyTwoWeekHigh")
    fifty_two_week_low = info.get("fiftyTwoWeekLow")

    return render_template("analysis.html",
        stockname=stockname,
        startDate=startDate,
        endDate=endDate,
        high=high,
        low=low,
        og_name=og_name,
        sector=sector,
        industry=industry,
        ceo=ceo,
        headquarters=headquarters,
        market_cap=market_cap,
        pe_ratio_forward=pe_ratio_forward,
        pe_ratio_trailing=pe_ratio_trailing,
        eps=eps,
        dividend_yield=dividend_yield,
        fifty_two_week_high=fifty_two_week_high,
        fifty_two_week_low=fifty_two_week_low,
        close_img=close_img,
        high_img=high_img,
        low_img=low_img,
        combined_img=combined_img
    )

@app.route('/delete-images', methods=['POST'])
def delete_images():
    data = request.get_json()
    images = data.get('images', [])
    deleted = []
    for img in images:
        if img:
            img_path = os.path.join(app.root_path, 'static', img)
            if os.path.exists(img_path):
                try:
                    os.remove(img_path)
                    deleted.append(img)
                except Exception as e:
                    pass 
    return jsonify({'deleted': deleted})

@app.route('/predict/<ticker>')
def predict_stock(ticker):
    import io
    import base64
    from pmdarima import auto_arima
    from statsmodels.tsa.stattools import adfuller
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')

    def test_stationality(timeseries):
        rolling_mean = timeseries.rolling(48).mean()
        rolling_std = timeseries.rolling(48).std()

        # Plot rolling stats (optional if you want to save/display it separately)
        plt.style.use("ggplot")
        plt.figure(figsize=(18, 8))
        plt.grid(True)
        plt.xlabel("Dates", fontsize=20)
        plt.xticks(fontsize=15)
        plt.ylabel("Close Price", fontsize=20)
        plt.yticks(fontsize=15)
        plt.plot(timeseries, linewidth=2, color="blue", label="Original")
        plt.plot(rolling_mean, linewidth=2, color="red", label="Rolling Mean")
        plt.plot(rolling_std, linewidth=2, color="green", label="Rolling Std")
        plt.title(f"{ticker} Stock Rolling Statistics", fontsize=30)
        plt.legend()
        plt.tight_layout()
        plt.close()  # Just for calculation; don't display here

        # ADF Test
        adft = adfuller(timeseries["Close"])
        p_value = adft[1]
        return "Stationary" if p_value < 0.05 else "Non-Stationary"

    # Step 1: Download stock data
    df = yf.download(ticker, period="1y")
    df = df[['Close']].dropna()
    df = df.round(2)
    df.reset_index(inplace=True)
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    # Step 2: Test stationarity and define `d`
    stationarity = test_stationality(df)
    d = 0 if stationarity == "Stationary" else 1

    # Step 3: Fit ARIMA
    model = auto_arima(df['Close'], start_p=0, start_q=0, max_p=5, max_q=5, d=d,
                       seasonal=False, stepwise=True, trace=False)
    
    # Step 4: Forecast next day
    forecast = model.predict(n_periods=1)[0]

    # Step 5: Plot last 60 days + forecast
    recent = df['Close'][-60:]
    forecast_date = recent.index[-1] + pd.Timedelta(days=1)
    forecast_series = recent.append(pd.Series([forecast], index=[forecast_date]))

    plt.figure(figsize=(10, 5))
    plt.plot(recent.index, recent.values, label='Recent Close', color='blue')
    plt.plot(forecast_series.index[-2:], forecast_series.values[-2:], label='Forecast', color='red', marker='o')
    plt.title(f'{ticker} Stock Price Prediction (Next Day)', fontsize=16)
    plt.xlabel('Date')
    plt.ylabel('Close Price (USD)')
    plt.legend()
    plt.grid(True)

    # Convert plot to base64 image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('ascii')

    return render_template('predict.html', ticker=ticker, forecast=round(forecast, 2), plot_url=img_base64)








if __name__ == "__main__":
  app.run(debug= True)
