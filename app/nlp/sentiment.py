"""
TrendWise AI — Financial Sentiment Analyzer
Uses VADER (lexicon-based) + TextBlob (pattern-based) for multi-method
sentiment analysis on financial news headlines.

Viva Talking Points:
  - VADER is specifically tuned for social media / news text
  - TextBlob provides subjectivity scoring (fact vs. opinion)
  - Compound score combines positive, negative, neutral intensities
  - Thresholds: >= 0.05 Positive, <= -0.05 Negative, else Neutral
"""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# TextBlob is optional — graceful fallback if corpora not downloaded
try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False


class FinancialSentimentAnalyzer:
    """
    Multi-method sentiment analyzer for financial news text.

    Methods used:
        1. VADER  — Valence Aware Dictionary and sEntiment Reasoner
        2. TextBlob — Pattern-based polarity & subjectivity
    """

    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()

    def analyze_text(self, text):
        """
        Analyze sentiment of a single text string.

        Args:
            text: News headline or article text

        Returns:
            Dictionary with compound, positive, negative, neutral scores,
            label, confidence, and subjectivity
        """
        if not text or not text.strip():
            return self._empty_result()

        # ── VADER Analysis ───────────────────────────
        vader_scores = self.vader.polarity_scores(text)

        # ── TextBlob Analysis (with fallback) ────────
        subjectivity = 0.0
        tb_polarity = 0.0
        if TEXTBLOB_AVAILABLE:
            try:
                blob = TextBlob(text)
                subjectivity = round(blob.sentiment.subjectivity, 3)
                tb_polarity = round(blob.sentiment.polarity, 3)
            except Exception:
                pass

        compound = vader_scores['compound']

        return {
            'compound': round(compound, 3),
            'positive': round(vader_scores['pos'], 3),
            'negative': round(vader_scores['neg'], 3),
            'neutral': round(vader_scores['neu'], 3),
            'textblob_polarity': tb_polarity,
            'subjectivity': subjectivity,
            'label': self._get_label(compound),
            'confidence': self._get_confidence(compound),
        }

    def analyze_articles(self, articles):
        """
        Analyze sentiment for a list of news articles.

        Args:
            articles: List of dicts with 'title', 'publisher', 'link', 'published' keys

        Returns:
            Dictionary with 'articles' (analyzed list) and 'overall' (aggregate stats)
        """
        if not articles:
            return {'articles': [], 'overall': self._empty_overall()}

        results = []
        for article in articles:
            sentiment = self.analyze_text(article.get('title', ''))
            sentiment.update({
                'title': article.get('title', ''),
                'publisher': article.get('publisher', 'Unknown'),
                'link': article.get('link', '#'),
                'published': article.get('published', ''),
            })
            results.append(sentiment)

        # ── Aggregate Scores ─────────────────────────
        compounds = [r['compound'] for r in results]
        avg_compound = sum(compounds) / len(compounds) if compounds else 0

        pos_count = sum(1 for r in results if r['label'] == 'Positive')
        neg_count = sum(1 for r in results if r['label'] == 'Negative')
        neu_count = sum(1 for r in results if r['label'] == 'Neutral')

        overall = {
            'score': round(avg_compound, 3),
            'label': self._get_label(avg_compound),
            'confidence': self._get_confidence(avg_compound),
            'total_articles': len(results),
            'positive_count': pos_count,
            'negative_count': neg_count,
            'neutral_count': neu_count,
            'positive_pct': round(pos_count / len(results) * 100, 1) if results else 0,
            'negative_pct': round(neg_count / len(results) * 100, 1) if results else 0,
            'neutral_pct': round(neu_count / len(results) * 100, 1) if results else 0,
        }

        return {'articles': results, 'overall': overall}

    # ── Helper Methods ────────────────────────────────

    @staticmethod
    def _get_label(compound):
        """Classify compound score into sentiment label."""
        if compound >= 0.05:
            return 'Positive'
        elif compound <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'

    @staticmethod
    def _get_confidence(compound):
        """
        Convert compound score to confidence percentage.
        Maps |compound| from [0, 1] to [0%, 100%].
        """
        return round(min(abs(compound) * 100, 100), 1)

    @staticmethod
    def _empty_result():
        return {
            'compound': 0, 'positive': 0, 'negative': 0, 'neutral': 1,
            'textblob_polarity': 0, 'subjectivity': 0,
            'label': 'Neutral', 'confidence': 0,
        }

    @staticmethod
    def _empty_overall():
        return {
            'score': 0, 'label': 'Neutral', 'confidence': 0,
            'total_articles': 0, 'positive_count': 0,
            'negative_count': 0, 'neutral_count': 0,
            'positive_pct': 0, 'negative_pct': 0, 'neutral_pct': 0,
        }
