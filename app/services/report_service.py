"""
TrendWise AI — PDF Report Generator
Generates professional PDF analysis reports for stocks.
Uses fpdf2 (free, no external dependencies).

Report Sections:
  1. Cover page with branding
  2. Company overview
  3. Price analysis
  4. AI insight summary
  5. Recommendation with factors
  6. Disclaimer
"""
import os
from datetime import datetime
from fpdf import FPDF
from flask import current_app
import logging

logger = logging.getLogger(__name__)


def _sanitize(text):
    """Replace Unicode characters with Latin-1 safe equivalents for PDF fonts."""
    replacements = {
        '\u2014': '-',   # em dash
        '\u2013': '-',   # en dash
        '\u2018': "'",   # left single quote
        '\u2019': "'",   # right single quote
        '\u201c': '"',   # left double quote
        '\u201d': '"',   # right double quote
        '\u2026': '...',  # ellipsis
        '\u2248': '~',   # approximately equal
        '\u2265': '>=',  # greater than or equal
        '\u2264': '<=',  # less than or equal
        '\u00b7': '-',   # middle dot
    }
    s = str(text)
    for k, v in replacements.items():
        s = s.replace(k, v)
    # Strip any remaining non-latin1 characters
    return s.encode('latin-1', errors='replace').decode('latin-1')


class TrendWiseReport(FPDF):
    """Custom PDF class with TrendWise branding."""

    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(62, 39, 35)  # --tw-primary
        self.cell(0, 8, 'TrendWise AI - Stock Analysis Report', border=0, align='L')
        self.set_font('Helvetica', '', 8)
        self.set_text_color(109, 76, 65)
        self.cell(0, 8, datetime.now().strftime('%Y-%m-%d %H:%M'), border=0, align='R', new_x='LMARGIN', new_y='NEXT')
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-20)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(62, 39, 35)
        self.cell(0, 10, _sanitize(title), new_x='LMARGIN', new_y='NEXT')
        self.set_draw_color(108, 79, 61)
        self.line(10, self.get_y(), 80, self.get_y())
        self.ln(4)

    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 6, _sanitize(text))
        self.ln(3)

    def key_value(self, key, value):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(62, 39, 35)
        self.cell(60, 7, f'{_sanitize(key)}:', align='L')
        self.set_font('Helvetica', '', 10)
        self.set_text_color(60, 60, 60)
        self.cell(0, 7, _sanitize(value), new_x='LMARGIN', new_y='NEXT')


def generate_pdf_report(ticker, company, insight, recommendation, sentiment=None):
    """
    Generate a comprehensive PDF report.

    Args:
        ticker: Stock symbol
        company: Company info dict
        insight: AI insight dict
        recommendation: Recommendation dict
        sentiment: Optional sentiment dict

    Returns:
        Absolute path to the generated PDF file
    """
    pdf = TrendWiseReport()
    pdf.alias_nb_pages()

    # ── Cover Page ─────────────────────────────────────
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font('Helvetica', 'B', 32)
    pdf.set_text_color(62, 39, 35)
    pdf.cell(0, 15, 'TrendWise AI', align='C', new_x='LMARGIN', new_y='NEXT')

    pdf.set_font('Helvetica', '', 14)
    pdf.set_text_color(109, 76, 65)
    pdf.cell(0, 10, 'Intelligent Stock Market Analysis Report', align='C', new_x='LMARGIN', new_y='NEXT')

    pdf.ln(15)
    pdf.set_font('Helvetica', 'B', 24)
    pdf.set_text_color(62, 39, 35)
    name = _sanitize(company.get('long_name', ticker))
    pdf.cell(0, 12, f'{name} ({ticker})', align='C', new_x='LMARGIN', new_y='NEXT')

    pdf.ln(5)
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(109, 76, 65)
    pdf.cell(0, 8, _sanitize(f'Sector: {company.get("sector", "N/A")} | Industry: {company.get("industry", "N/A")}'), align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.cell(0, 8, f'Generated: {datetime.now().strftime("%B %d, %Y at %H:%M")}', align='C', new_x='LMARGIN', new_y='NEXT')

    # Recommendation on cover
    rec_text = recommendation.get('recommendation', 'N/A')
    confidence = recommendation.get('confidence', 0)
    pdf.ln(15)
    pdf.set_font('Helvetica', 'B', 20)
    if rec_text in ('Strong Buy', 'Buy'):
        pdf.set_text_color(46, 125, 50)
    elif rec_text == 'Hold':
        pdf.set_text_color(245, 127, 23)
    else:
        pdf.set_text_color(198, 40, 40)
    pdf.cell(0, 12, f'Recommendation: {rec_text}', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(109, 76, 65)
    pdf.cell(0, 8, f'Confidence: {confidence}% | Score: {recommendation.get("score", 0)}', align='C', new_x='LMARGIN', new_y='NEXT')

    # ── Company Overview ───────────────────────────────
    pdf.add_page()
    pdf.section_title('1. Company Overview')

    pdf.key_value('Company', name)
    pdf.key_value('Ticker', ticker)
    pdf.key_value('Sector', company.get('sector', 'N/A'))
    pdf.key_value('Industry', company.get('industry', 'N/A'))
    pdf.key_value('CEO', company.get('ceo', 'N/A'))
    pdf.key_value('Headquarters', company.get('headquarters', 'N/A'))
    pdf.ln(3)

    # Financial metrics
    pdf.section_title('2. Key Financial Metrics')

    _safe_kv(pdf, 'Current Price', company.get('current_price'), prefix='$')
    _safe_kv(pdf, 'Market Cap', _fmt_cap(company.get('market_cap')))
    _safe_kv(pdf, 'Trailing P/E', company.get('pe_ratio_trailing'))
    _safe_kv(pdf, 'Forward P/E', company.get('pe_ratio_forward'))
    _safe_kv(pdf, 'EPS', company.get('eps'), prefix='$')
    _safe_kv(pdf, 'Dividend Yield', _fmt_pct(company.get('dividend_yield')))
    _safe_kv(pdf, '52-Week High', company.get('fifty_two_week_high'), prefix='$')
    _safe_kv(pdf, '52-Week Low', company.get('fifty_two_week_low'), prefix='$')
    pdf.ln(3)

    # ── AI Analysis ────────────────────────────────────
    pdf.add_page()
    pdf.section_title('3. AI-Powered Analysis')

    provider = insight.get('provider', 'Local')
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f'Analysis Provider: {provider}', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(3)

    for title, key in [
        ('Market Summary', 'summary'),
        ('Trend Analysis', 'trend'),
        ('Technical Analysis', 'technical'),
        ('Risk Assessment', 'risk'),
        ('Opportunity Analysis', 'opportunity'),
    ]:
        content = insight.get(key, '')
        if content:
            pdf.set_font('Helvetica', 'B', 11)
            pdf.set_text_color(62, 39, 35)
            pdf.cell(0, 8, title, new_x='LMARGIN', new_y='NEXT')
            pdf.body_text(content)

    # ── Recommendation Detail ──────────────────────────
    pdf.add_page()
    pdf.section_title('4. Recommendation Breakdown')

    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(62, 39, 35)
    pdf.cell(0, 10, f'Final Rating: {rec_text} (Confidence: {confidence}%)', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(3)

    # Factor table
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_fill_color(245, 240, 235)
    pdf.cell(55, 8, 'Factor', border=1, fill=True)
    pdf.cell(20, 8, 'Score', border=1, align='C', fill=True)
    pdf.cell(20, 8, 'Weight', border=1, align='C', fill=True)
    pdf.cell(95, 8, 'Reason', border=1, fill=True, new_x='LMARGIN', new_y='NEXT')

    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(60, 60, 60)
    for factor in recommendation.get('factors', []):
        pdf.cell(55, 7, factor['name'], border=1)
        pdf.cell(20, 7, str(factor['score']), border=1, align='C')
        pdf.cell(20, 7, str(factor['weight']), border=1, align='C')
        reason = factor['reason'][:55] + '...' if len(factor['reason']) > 55 else factor['reason']
        pdf.cell(95, 7, _sanitize(reason), border=1, new_x='LMARGIN', new_y='NEXT')

    pdf.ln(5)

    # Reasoning
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(62, 39, 35)
    pdf.cell(0, 8, 'Reasoning:', new_x='LMARGIN', new_y='NEXT')
    for reason in recommendation.get('reasoning', []):
        pdf.body_text(f'  - {reason}')

    # ── Sentiment (if available) ───────────────────────
    if sentiment and sentiment.get('overall'):
        pdf.ln(5)
        pdf.section_title('5. Market Sentiment')
        overall = sentiment['overall']
        pdf.key_value('Overall Sentiment', overall.get('label', 'N/A'))
        pdf.key_value('Sentiment Score', str(overall.get('score', 0)))
        pdf.key_value('Articles Analyzed', str(overall.get('total_articles', 0)))
        pdf.key_value('Positive', str(overall.get('positive_count', 0)))
        pdf.key_value('Neutral', str(overall.get('neutral_count', 0)))
        pdf.key_value('Negative', str(overall.get('negative_count', 0)))

    # ── Disclaimer ─────────────────────────────────────
    pdf.ln(10)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(150, 150, 150)
    pdf.multi_cell(0, 5,
        'DISCLAIMER: This report is generated by TrendWise AI for educational and informational purposes only. '
        'It does not constitute financial advice, investment recommendation, or an offer to buy or sell securities. '
        'Always consult a qualified financial advisor before making investment decisions. '
        'Past performance is not indicative of future results.'
    )

    # ── Save PDF ───────────────────────────────────────
    reports_dir = os.path.join(current_app.root_path, 'static', 'reports')
    os.makedirs(reports_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'TrendWise_Report_{ticker}_{timestamp}.pdf'
    filepath = os.path.join(reports_dir, filename)

    pdf.output(filepath)
    logger.info(f'PDF report generated: {filepath}')

    return f'reports/{filename}'


# ── Helper Utilities ──────────────────────────────────

def _safe_kv(pdf, key, value, prefix=''):
    if value is not None:
        pdf.key_value(key, f'{prefix}{value}')
    else:
        pdf.key_value(key, 'N/A')


def _fmt_cap(cap):
    if not cap:
        return 'N/A'
    if cap >= 1e12:
        return f'${cap/1e12:.2f}T'
    elif cap >= 1e9:
        return f'${cap/1e9:.2f}B'
    elif cap >= 1e6:
        return f'${cap/1e6:.2f}M'
    return f'${cap:,.0f}'


def _fmt_pct(val):
    if val is None:
        return 'N/A'
    return f'{val*100:.2f}%'
