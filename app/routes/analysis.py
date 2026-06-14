"""
TrendWise AI — Stock Analysis Routes
Handles stock analysis, chart generation, and image cleanup.
"""
from flask import Blueprint, render_template, request, jsonify, current_app, session
from app.routes.main import login_required
from app.services.stock_service import fetch_stock_data, get_company_info, get_price_extremes
from app.services.chart_service import (
    show_close_plot, show_high_plot, show_low_plot,
    show_combine_plot, cleanup_images,
)
from app.utils.validators import validate_ticker, validate_date_range

analysis_bp = Blueprint('analysis', __name__)


@analysis_bp.route('/analysis', methods=['POST'])
@login_required
def analyze():
    """
    Perform stock analysis and display results.
    Validates inputs, fetches data, generates charts, and renders analysis page.
    """
    stockname = request.form.get('stockname', '')
    start_date = request.form.get('startDate', '')
    end_date = request.form.get('endDate', '')

    # Validate ticker
    is_valid, ticker_result = validate_ticker(stockname)
    if not is_valid:
        return render_template(
            'home.html',
            username=session.get('username', 'User'),
            error=ticker_result,
        )
    stockname = ticker_result

    # Validate date range
    is_valid, date_error = validate_date_range(start_date, end_date)
    if not is_valid:
        return render_template(
            'home.html',
            username=session.get('username', 'User'),
            error=date_error,
        )

    try:
        # Fetch stock data
        df = fetch_stock_data(stockname, start_date, end_date)
        high, low = get_price_extremes(df)

        # Generate charts
        close_img = show_close_plot(df, stockname, start_date, end_date)
        high_img = show_high_plot(df, stockname, start_date, end_date)
        low_img = show_low_plot(df, stockname, start_date, end_date)
        combined_img = show_combine_plot(df, stockname, start_date, end_date)

        # Get company info
        company = get_company_info(stockname)

        # Save to search history
        user_id = session.get('user_id')
        if user_id:
            try:
                from app.models.database import save_search
                save_search(user_id, stockname, start_date, end_date)
            except Exception:
                pass  # Don't break analysis if history save fails

        return render_template(
            'analysis.html',
            stockname=stockname,
            startDate=start_date,
            endDate=end_date,
            high=high,
            low=low,
            og_name=company['long_name'],
            sector=company['sector'],
            industry=company['industry'],
            ceo=company['ceo'],
            headquarters=company['headquarters'],
            market_cap=company['market_cap'],
            pe_ratio_forward=company['pe_ratio_forward'],
            pe_ratio_trailing=company['pe_ratio_trailing'],
            eps=company['eps'],
            dividend_yield=company['dividend_yield'],
            fifty_two_week_high=company['fifty_two_week_high'],
            fifty_two_week_low=company['fifty_two_week_low'],
            close_img=close_img,
            high_img=high_img,
            low_img=low_img,
            combined_img=combined_img,
        )

    except ValueError as e:
        return render_template(
            'home.html',
            username=session.get('username', 'User'),
            error=str(e),
        )
    except Exception as e:
        current_app.logger.error(f'Analysis error for {stockname}: {e}')
        return render_template(
            'home.html',
            username=session.get('username', 'User'),
            error=f'Error analyzing stock: {str(e)}',
        )


@analysis_bp.route('/delete-images', methods=['POST'])
def delete_images():
    """Delete generated chart images from server (called via JS on page unload)."""
    data = request.get_json()
    images = data.get('images', [])
    deleted = cleanup_images(images, current_app.static_folder)
    return jsonify({'deleted': deleted})
