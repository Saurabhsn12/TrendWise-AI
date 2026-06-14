"""
TrendWise AI — Chart Service
Generates matplotlib charts for stock data visualization.
Preserved from original extra_stuff.py with structural improvements.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from flask import current_app


def _ensure_image_dir():
    """Ensure the static/images directory exists."""
    image_path = os.path.join(current_app.static_folder, 'images')
    os.makedirs(image_path, exist_ok=True)
    return image_path


def _save_plot(filename):
    """Save current matplotlib plot to static folder and close it."""
    filepath = os.path.join(current_app.static_folder, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    return filename


def show_close_plot(df, stock, start_date, end_date):
    """Generate closing price chart."""
    _ensure_image_dir()
    plt.style.use('ggplot')
    plt.figure(figsize=(18, 8), dpi=300)
    plt.grid(True)
    plt.xlabel('Dates', fontsize=20)
    plt.xticks(fontsize=15)
    plt.ylabel('Close Price', fontsize=20)
    plt.yticks(fontsize=15)
    plt.plot(df['Close'], linewidth=2, color='blue', label='Close')
    plt.title('Stock Close Price', fontsize=30)
    plt.legend()
    plt.tight_layout()

    filename = f'images/{stock}_{start_date}_{end_date}_close.png'
    return _save_plot(filename)


def show_high_plot(df, stock, start_date, end_date):
    """Generate high price chart."""
    _ensure_image_dir()
    plt.style.use('ggplot')
    plt.figure(figsize=(18, 8), dpi=300)
    plt.grid(True)
    plt.xlabel('Dates', fontsize=20)
    plt.xticks(fontsize=15)
    plt.ylabel('High Price', fontsize=20)
    plt.yticks(fontsize=15)
    plt.plot(df['High'], linewidth=2, color='green', label='High')
    plt.title('Stock High Price', fontsize=30)
    plt.legend()
    plt.tight_layout()

    filename = f'images/{stock}_{start_date}_{end_date}_high.png'
    return _save_plot(filename)


def show_low_plot(df, stock, start_date, end_date):
    """Generate low price chart."""
    _ensure_image_dir()
    plt.style.use('ggplot')
    plt.figure(figsize=(18, 8), dpi=300)
    plt.grid(True)
    plt.xlabel('Dates', fontsize=20)
    plt.xticks(fontsize=15)
    plt.ylabel('Low Price', fontsize=20)
    plt.yticks(fontsize=15)
    plt.plot(df['Low'], linewidth=2, color='red', label='Low')
    plt.title('Stock Low Price', fontsize=30)
    plt.legend()
    plt.tight_layout()

    filename = f'images/{stock}_{start_date}_{end_date}_low.png'
    return _save_plot(filename)


def show_combine_plot(df, stock, start_date, end_date):
    """Generate combined (Close, High, Low) chart."""
    _ensure_image_dir()
    plt.style.use('ggplot')
    plt.figure(figsize=(18, 8), dpi=300)
    plt.grid(True)
    plt.xlabel('Dates', fontsize=20)
    plt.xticks(fontsize=15)
    plt.ylabel('Close Price', fontsize=20)
    plt.yticks(fontsize=15)
    plt.plot(df['Close'], linewidth=2, color='blue', label='Final_closing')
    plt.plot(df['High'], linewidth=2, color='green', label='High')
    plt.plot(df['Low'], linewidth=2, color='red', label='Low')
    plt.title('Stock Closing Price', fontsize=30)
    plt.legend()
    plt.tight_layout()

    filename = f'images/{stock}_{start_date}_{end_date}_combined.png'
    return _save_plot(filename)


def cleanup_images(image_list, static_folder):
    """
    Delete specified image files from static folder.

    Args:
        image_list: List of image filenames (relative to static folder)
        static_folder: Absolute path to static folder

    Returns:
        List of successfully deleted filenames
    """
    deleted = []
    for img in image_list:
        if img:
            img_path = os.path.join(static_folder, img)
            if os.path.exists(img_path):
                try:
                    os.remove(img_path)
                    deleted.append(img)
                except OSError:
                    pass
    return deleted
