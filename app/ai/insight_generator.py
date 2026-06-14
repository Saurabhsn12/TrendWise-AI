"""
TrendWise AI — Insight Generator
Generates intelligent stock market insights using:
  1. Gemini Free API (primary - when API key is configured)
  2. Local rule-based engine (fallback - always available, no API needed)

Architecture:
  Provider pattern — can switch between AI providers via config.
  All providers implement the same interface: generate_insight(stock_data) -> str

Viva Talking Points:
  - Provider pattern enables swapping AI backends without changing business logic
  - Local fallback ensures the app works offline and at zero cost
  - Gemini integration demonstrates real Generative AI capability
  - Prompts are designed with financial context for accurate responses
"""
import logging
from flask import current_app

logger = logging.getLogger(__name__)


def generate_insight(stock_data):
    """
    Generate AI-powered stock market insight.

    Args:
        stock_data: Dictionary with keys:
            - ticker, company_name, sector, industry
            - current_price, high, low
            - pe_ratio_forward, pe_ratio_trailing, eps
            - market_cap, dividend_yield
            - fifty_two_week_high, fifty_two_week_low
            - sentiment_label, sentiment_score (optional)

    Returns:
        Dictionary with:
            - summary: Market overview paragraph
            - trend: Trend analysis paragraph
            - technical: Technical analysis summary
            - risk: Risk assessment
            - opportunity: Opportunity analysis
            - provider: Which AI provider was used
    """
    provider = current_app.config.get('AI_PROVIDER', 'local')
    api_key = current_app.config.get('GEMINI_API_KEY', '')

    if provider == 'gemini' and api_key:
        try:
            return _generate_gemini_insight(stock_data, api_key)
        except Exception as e:
            logger.warning(f'Gemini API failed, falling back to local: {e}')
            return _generate_local_insight(stock_data)
    else:
        return _generate_local_insight(stock_data)


def _generate_gemini_insight(stock_data, api_key):
    """Generate insight using Google Gemini Free API."""
    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = f"""You are a professional financial analyst. Analyze the following stock data and provide a concise investment insight report.

Stock: {stock_data.get('ticker', 'N/A')} ({stock_data.get('company_name', 'N/A')})
Sector: {stock_data.get('sector', 'N/A')}
Industry: {stock_data.get('industry', 'N/A')}
Price Range (analyzed period): High ${stock_data.get('high', 'N/A')}, Low ${stock_data.get('low', 'N/A')}
Current Price: ${stock_data.get('current_price', 'N/A')}
Market Cap: ${stock_data.get('market_cap', 'N/A')}
Forward P/E: {stock_data.get('pe_ratio_forward', 'N/A')}
Trailing P/E: {stock_data.get('pe_ratio_trailing', 'N/A')}
EPS: {stock_data.get('eps', 'N/A')}
Dividend Yield: {stock_data.get('dividend_yield', 'N/A')}
52-Week High: ${stock_data.get('fifty_two_week_high', 'N/A')}
52-Week Low: ${stock_data.get('fifty_two_week_low', 'N/A')}
News Sentiment: {stock_data.get('sentiment_label', 'N/A')} (Score: {stock_data.get('sentiment_score', 'N/A')})

Provide your analysis in exactly this format (keep each section to 2-3 sentences):

MARKET SUMMARY: [Overview of current market position]
TREND ANALYSIS: [Price trend and momentum analysis]
TECHNICAL ANALYSIS: [Key technical indicators and what they suggest]
RISK ASSESSMENT: [Key risks to consider]
OPPORTUNITY ANALYSIS: [Potential opportunities and catalysts]

Important: Be factual, not promotional. This is for educational purposes only."""

        response = model.generate_content(prompt)
        text = response.text

        # Parse the structured response
        sections = _parse_gemini_response(text)
        sections['provider'] = 'Gemini AI'
        return sections

    except ImportError:
        logger.warning('google-generativeai not installed, falling back to local')
        return _generate_local_insight(stock_data)


def _parse_gemini_response(text):
    """Parse Gemini's structured response into sections."""
    sections = {
        'summary': '', 'trend': '', 'technical': '',
        'risk': '', 'opportunity': '', 'provider': 'Gemini AI'
    }

    current_key = None
    key_map = {
        'MARKET SUMMARY': 'summary',
        'TREND ANALYSIS': 'trend',
        'TECHNICAL ANALYSIS': 'technical',
        'RISK ASSESSMENT': 'risk',
        'OPPORTUNITY ANALYSIS': 'opportunity',
    }

    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue

        matched = False
        for prefix, key in key_map.items():
            if line.upper().startswith(prefix):
                current_key = key
                # Extract content after the prefix and colon
                content = line[len(prefix):].lstrip(':').lstrip()
                # Remove markdown bold markers
                content = content.replace('**', '')
                if content:
                    sections[current_key] = content
                matched = True
                break

        if not matched and current_key:
            line = line.replace('**', '')
            if sections[current_key]:
                sections[current_key] += ' ' + line
            else:
                sections[current_key] = line

    # Fallback if parsing failed
    if not any(sections[k] for k in ['summary', 'trend', 'technical']):
        cleaned = text.replace('**', '').strip()
        sections['summary'] = cleaned[:500] if len(cleaned) > 500 else cleaned

    return sections


def _generate_local_insight(stock_data):
    """
    Generate insight using local rule-based engine.
    No API keys needed — works completely offline.
    """
    ticker = stock_data.get('ticker', 'N/A')
    name = stock_data.get('company_name', ticker)
    sector = stock_data.get('sector', 'N/A')
    high = stock_data.get('high', 0)
    low = stock_data.get('low', 0)
    pe_forward = stock_data.get('pe_ratio_forward')
    pe_trailing = stock_data.get('pe_ratio_trailing')
    eps = stock_data.get('eps')
    market_cap = stock_data.get('market_cap')
    dividend = stock_data.get('dividend_yield')
    w52_high = stock_data.get('fifty_two_week_high')
    w52_low = stock_data.get('fifty_two_week_low')
    current = stock_data.get('current_price')
    sentiment = stock_data.get('sentiment_label', 'Neutral')
    sentiment_score = stock_data.get('sentiment_score', 0)

    # ── Market Summary ──────────────────────────────
    cap_label = _format_market_cap(market_cap)
    summary = (
        f"{name} ({ticker}) is a {cap_label} company operating in the {sector} sector. "
        f"During the analyzed period, the stock traded between ${low} and ${high}, "
        f"showing a price range of ${round(high - low, 2) if high and low else 'N/A'}. "
    )
    if current and w52_high:
        pct_from_high = round((1 - current / w52_high) * 100, 1) if w52_high else 0
        summary += f"The stock is currently trading {pct_from_high}% below its 52-week high of ${w52_high}."

    # ── Trend Analysis ──────────────────────────────
    trend = ""
    if current and w52_high and w52_low:
        range_pct = (current - w52_low) / (w52_high - w52_low) * 100 if (w52_high - w52_low) else 50
        if range_pct > 70:
            trend = f"The stock is showing bullish momentum, trading near its 52-week high. Price action suggests strong upward pressure with buyers maintaining control. "
        elif range_pct > 40:
            trend = f"The stock is trading in a consolidation range, suggesting a neutral trend. The price is balanced between support and resistance levels. "
        else:
            trend = f"The stock is showing bearish pressure, trading closer to its 52-week low. This could indicate either weakness or a potential value opportunity. "

        if sentiment and sentiment != 'N/A':
            trend += f"Market sentiment from recent news is {sentiment.lower()}"
            if sentiment_score:
                trend += f" (score: {sentiment_score})"
            trend += ", which "
            if sentiment == 'Positive':
                trend += "supports the current upward momentum."
            elif sentiment == 'Negative':
                trend += "may add downward pressure."
            else:
                trend += "suggests a wait-and-watch approach."
    else:
        trend = f"Trend data for {name} suggests monitoring the stock for directional confirmation. Watch for breakout above recent highs or breakdown below support levels."

    # ── Technical Analysis ──────────────────────────
    technical = ""
    if pe_forward and pe_trailing:
        if pe_forward < pe_trailing:
            technical = f"The forward P/E ratio ({pe_forward:.1f}) is lower than the trailing P/E ({pe_trailing:.1f}), indicating analysts expect earnings growth. "
        else:
            technical = f"The forward P/E ratio ({pe_forward:.1f}) is higher than the trailing P/E ({pe_trailing:.1f}), suggesting potential earnings deceleration. "
    elif pe_trailing:
        if pe_trailing < 15:
            technical = f"With a P/E ratio of {pe_trailing:.1f}, the stock appears to be value-priced. "
        elif pe_trailing < 25:
            technical = f"With a P/E ratio of {pe_trailing:.1f}, the stock is moderately valued. "
        else:
            technical = f"With a P/E ratio of {pe_trailing:.1f}, the stock has a premium valuation, reflecting high growth expectations. "

    if eps:
        technical += f"EPS of ${eps:.2f} " + ("shows strong profitability. " if eps > 0 else "indicates the company is currently unprofitable. ")

    if not technical:
        technical = f"Technical indicators for {name} should be evaluated alongside SMA and EMA crossovers for entry/exit signals."

    # ── Risk Assessment ─────────────────────────────
    risks = []
    if pe_trailing and pe_trailing > 40:
        risks.append("high valuation (P/E > 40) leaves the stock vulnerable to corrections")
    if not dividend or dividend == 0:
        risks.append("no dividend income, making it purely growth-dependent")
    if current and w52_high and current > w52_high * 0.95:
        risks.append("trading near 52-week high increases correction risk")
    if sentiment == 'Negative':
        risks.append("negative news sentiment may weigh on short-term price action")

    if risks:
        risk = f"Key risks include: {', '.join(risks)}. Investors should maintain appropriate position sizing and set stop-loss levels."
    else:
        risk = f"The risk profile for {name} appears moderate. Standard diversification principles should be applied."

    # ── Opportunity Analysis ────────────────────────
    opportunities = []
    if pe_trailing and pe_trailing < 20:
        opportunities.append("relatively attractive valuation")
    if dividend and dividend > 0.02:
        opportunities.append(f"dividend yield of {dividend*100:.1f}% provides income")
    if current and w52_low and current < w52_low * 1.15:
        opportunities.append("trading near 52-week low could present a value entry point")
    if sentiment == 'Positive':
        opportunities.append("positive news sentiment supports near-term momentum")
    if eps and eps > 0 and pe_forward and pe_forward < pe_trailing:
        opportunities.append("expected earnings growth could drive price appreciation")

    if opportunities:
        opportunity = f"Potential opportunities include: {', '.join(opportunities)}. These factors may support positive price action if broader market conditions remain favorable."
    else:
        opportunity = f"{name} presents a standard risk-reward profile. Monitor for catalysts such as earnings beats, sector rotations, or macro tailwinds that could unlock value."

    return {
        'summary': summary,
        'trend': trend,
        'technical': technical,
        'risk': risk,
        'opportunity': opportunity,
        'provider': 'Local Analysis Engine',
    }


def _format_market_cap(market_cap):
    """Format market cap into human-readable label."""
    if not market_cap:
        return 'N/A-cap'
    if market_cap >= 200e9:
        return 'mega-cap'
    elif market_cap >= 10e9:
        return 'large-cap'
    elif market_cap >= 2e9:
        return 'mid-cap'
    elif market_cap >= 300e6:
        return 'small-cap'
    else:
        return 'micro-cap'
