"""
TrendWise AI — Stock Recommendation Engine
Generates intelligent Buy/Hold/Sell recommendations based on:
  - Technical indicators (P/E, EPS, price position)
  - Market data (52-week range, market cap)
  - Sentiment analysis scores
  - Volume and trend signals

Scoring System:
  Each factor contributes a weighted score from -2 to +2.
  Final score mapped to: Strong Buy, Buy, Hold, Watch, Sell.

Viva Talking Points:
  - Multi-factor scoring model combines quantitative and qualitative signals
  - Each factor has explicit weight reflecting its predictive importance
  - Confidence score reflects how many factors agree on direction
  - Reasoning is generated for transparency (explainable AI)
"""
import logging

logger = logging.getLogger(__name__)

# ── Recommendation Thresholds ────────────────────
STRONG_BUY_THRESHOLD = 1.5
BUY_THRESHOLD = 0.5
HOLD_UPPER = 0.5
HOLD_LOWER = -0.5
WATCH_THRESHOLD = -1.0
# Below WATCH_THRESHOLD = Sell


def generate_recommendation(stock_data):
    """
    Generate stock recommendation with confidence and reasoning.

    Args:
        stock_data: Dictionary with financial metrics and optional sentiment data

    Returns:
        Dictionary with:
            - recommendation: 'Strong Buy', 'Buy', 'Hold', 'Watch', or 'Sell'
            - confidence: 0-100 percentage
            - score: Raw numeric score
            - reasoning: List of factor explanations
            - factors: Detailed factor breakdown
    """
    factors = []
    total_score = 0
    total_weight = 0

    # ── Factor 1: Valuation (P/E Ratio) ────────── Weight: 2.0
    pe_score, pe_reason = _evaluate_pe_ratio(stock_data)
    factors.append({'name': 'Valuation (P/E)', 'score': pe_score, 'weight': 2.0, 'reason': pe_reason})
    total_score += pe_score * 2.0
    total_weight += 2.0

    # ── Factor 2: Earnings (EPS) ─────────────── Weight: 1.5
    eps_score, eps_reason = _evaluate_eps(stock_data)
    factors.append({'name': 'Earnings (EPS)', 'score': eps_score, 'weight': 1.5, 'reason': eps_reason})
    total_score += eps_score * 1.5
    total_weight += 1.5

    # ── Factor 3: Price Position (52-week) ───── Weight: 1.5
    pos_score, pos_reason = _evaluate_price_position(stock_data)
    factors.append({'name': 'Price Position', 'score': pos_score, 'weight': 1.5, 'reason': pos_reason})
    total_score += pos_score * 1.5
    total_weight += 1.5

    # ── Factor 4: Dividend Yield ─────────────── Weight: 1.0
    div_score, div_reason = _evaluate_dividend(stock_data)
    factors.append({'name': 'Dividend Yield', 'score': div_score, 'weight': 1.0, 'reason': div_reason})
    total_score += div_score * 1.0
    total_weight += 1.0

    # ── Factor 5: Earnings Growth ────────────── Weight: 2.0
    growth_score, growth_reason = _evaluate_earnings_growth(stock_data)
    factors.append({'name': 'Earnings Growth', 'score': growth_score, 'weight': 2.0, 'reason': growth_reason})
    total_score += growth_score * 2.0
    total_weight += 2.0

    # ── Factor 6: Market Sentiment ───────────── Weight: 1.5
    sent_score, sent_reason = _evaluate_sentiment(stock_data)
    factors.append({'name': 'Market Sentiment', 'score': sent_score, 'weight': 1.5, 'reason': sent_reason})
    total_score += sent_score * 1.5
    total_weight += 1.5

    # ── Calculate Final Score ────────────────────
    weighted_score = total_score / total_weight if total_weight > 0 else 0
    recommendation = _score_to_recommendation(weighted_score)
    confidence = _calculate_confidence(factors, weighted_score)

    # ── Generate Reasoning ───────────────────────
    reasoning = _generate_reasoning(factors, recommendation, stock_data)

    return {
        'recommendation': recommendation,
        'confidence': confidence,
        'score': round(weighted_score, 3),
        'reasoning': reasoning,
        'factors': factors,
    }


# ─── Factor Evaluation Functions ──────────────────

def _evaluate_pe_ratio(data):
    pe = data.get('pe_ratio_trailing')
    if pe is None:
        return 0, 'P/E ratio data unavailable'
    if pe < 0:
        return -1, f'Negative P/E ({pe:.1f}) indicates current losses'
    elif pe < 12:
        return 2, f'Very attractive valuation (P/E: {pe:.1f})'
    elif pe < 18:
        return 1, f'Reasonably valued (P/E: {pe:.1f})'
    elif pe < 30:
        return 0, f'Moderately valued (P/E: {pe:.1f})'
    elif pe < 50:
        return -1, f'Premium valuation (P/E: {pe:.1f})'
    else:
        return -2, f'Very expensive (P/E: {pe:.1f})'


def _evaluate_eps(data):
    eps = data.get('eps')
    if eps is None:
        return 0, 'EPS data unavailable'
    if eps > 10:
        return 2, f'Strong earnings (EPS: ${eps:.2f})'
    elif eps > 3:
        return 1, f'Healthy earnings (EPS: ${eps:.2f})'
    elif eps > 0:
        return 0, f'Modest earnings (EPS: ${eps:.2f})'
    else:
        return -1, f'Negative earnings (EPS: ${eps:.2f})'


def _evaluate_price_position(data):
    current = data.get('current_price')
    w52_high = data.get('fifty_two_week_high')
    w52_low = data.get('fifty_two_week_low')

    if not all([current, w52_high, w52_low]) or w52_high == w52_low:
        return 0, 'Insufficient price range data'

    position = (current - w52_low) / (w52_high - w52_low) * 100

    if position < 20:
        return 1, f'Near 52-week low ({position:.0f}% range) — potential value entry'
    elif position < 40:
        return 0.5, f'In lower range ({position:.0f}%) — moderate entry point'
    elif position < 60:
        return 0, f'Mid-range ({position:.0f}%) — neutral positioning'
    elif position < 80:
        return -0.5, f'In upper range ({position:.0f}%) — momentum play'
    else:
        return -1, f'Near 52-week high ({position:.0f}%) — watch for pullback'


def _evaluate_dividend(data):
    div = data.get('dividend_yield')
    if div is None or div == 0:
        return 0, 'No dividend yield'
    if div > 0.05:
        return 1.5, f'High dividend yield ({div*100:.1f}%) — strong income'
    elif div > 0.03:
        return 1, f'Good dividend yield ({div*100:.1f}%)'
    elif div > 0.01:
        return 0.5, f'Moderate dividend ({div*100:.1f}%)'
    else:
        return 0, f'Low dividend ({div*100:.1f}%)'


def _evaluate_earnings_growth(data):
    pe_forward = data.get('pe_ratio_forward')
    pe_trailing = data.get('pe_ratio_trailing')

    if pe_forward is None or pe_trailing is None or pe_trailing <= 0:
        return 0, 'Growth data unavailable'

    growth_ratio = pe_forward / pe_trailing

    if growth_ratio < 0.7:
        return 2, f'Strong expected growth (fwd P/E {pe_forward:.1f} vs trailing {pe_trailing:.1f})'
    elif growth_ratio < 0.9:
        return 1, f'Moderate growth expected (fwd P/E {pe_forward:.1f})'
    elif growth_ratio < 1.1:
        return 0, f'Stable earnings expected (fwd P/E ~= trailing)'
    else:
        return -1, f'Earnings may decline (fwd P/E {pe_forward:.1f} > trailing {pe_trailing:.1f})'


def _evaluate_sentiment(data):
    label = data.get('sentiment_label')
    score = data.get('sentiment_score', 0)

    if not label or label == 'N/A':
        return 0, 'Sentiment data unavailable'

    if label == 'Positive':
        if score > 0.3:
            return 1.5, f'Strongly positive sentiment (score: {score})'
        return 1, f'Positive market sentiment (score: {score})'
    elif label == 'Negative':
        if score < -0.3:
            return -1.5, f'Strongly negative sentiment (score: {score})'
        return -1, f'Negative market sentiment (score: {score})'
    else:
        return 0, f'Neutral market sentiment (score: {score})'


# ─── Helper Functions ─────────────────────────────

def _score_to_recommendation(score):
    if score >= STRONG_BUY_THRESHOLD:
        return 'Strong Buy'
    elif score >= BUY_THRESHOLD:
        return 'Buy'
    elif score >= HOLD_LOWER:
        return 'Hold'
    elif score >= WATCH_THRESHOLD:
        return 'Watch'
    else:
        return 'Sell'


def _calculate_confidence(factors, weighted_score):
    """Calculate confidence based on factor agreement."""
    if not factors:
        return 0

    # Count factors that agree with the overall direction
    direction = 1 if weighted_score > 0 else (-1 if weighted_score < 0 else 0)
    agreeing = sum(1 for f in factors if (
        (f['score'] > 0 and direction > 0) or
        (f['score'] < 0 and direction < 0) or
        (f['score'] == 0 and direction == 0)
    ))

    agreement_pct = (agreeing / len(factors)) * 100

    # Boost confidence by score magnitude
    magnitude_bonus = min(abs(weighted_score) * 15, 20)

    confidence = min(agreement_pct + magnitude_bonus, 99)
    return round(confidence, 1)


def _generate_reasoning(factors, recommendation, stock_data):
    """Generate human-readable reasoning for the recommendation."""
    reasoning = []

    # Top positive factors
    bullish = sorted([f for f in factors if f['score'] > 0], key=lambda x: x['score'] * x['weight'], reverse=True)
    bearish = sorted([f for f in factors if f['score'] < 0], key=lambda x: x['score'] * x['weight'])

    if bullish:
        top = bullish[0]
        reasoning.append(f"Bullish: {top['reason']}")
    if len(bullish) > 1:
        reasoning.append(f"Supporting: {bullish[1]['reason']}")

    if bearish:
        top = bearish[0]
        reasoning.append(f"Caution: {top['reason']}")

    # Summary
    ticker = stock_data.get('ticker', 'This stock')
    reasoning.append(
        f"Overall, {ticker} receives a '{recommendation}' rating based on a multi-factor analysis "
        f"combining valuation, earnings, price momentum, dividends, growth outlook, and market sentiment."
    )

    return reasoning
