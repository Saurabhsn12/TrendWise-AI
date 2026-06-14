import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import yfinance as yf
import os

def show_combine_plot(df, stock, start_date, end_date):
    plt.style.use("ggplot")
    plt.figure(figsize=(18, 8), dpi=300)
    plt.grid(True)
    plt.xlabel("Dates", fontsize=20)
    plt.xticks(fontsize=15)
    plt.ylabel("Close Price", fontsize=20)
    plt.yticks(fontsize=15)
    plt.plot(df["Close"], linewidth=2, color="blue", label="Final_closing")
    plt.plot(df["High"], linewidth=2, color="green", label="High")
    plt.plot(df["Low"], linewidth=2, color="red", label="Low")
    plt.title("Stock Closing Price", fontsize=30)
    plt.legend()
    plt.tight_layout()

    filename = f"images/{stock}_{start_date}_{end_date}_combined.png"
    image_path = os.path.join("static", "images")
    if not os.path.exists(image_path):
        os.makedirs(image_path)

    plt.savefig(os.path.join("static", filename), dpi=300, bbox_inches="tight")
    plt.close()
    return filename


def show_high_plot(df, stock, start_date, end_date):
    plt.style.use("ggplot")
    plt.figure(figsize=(18, 8), dpi=300)
    plt.grid(True)
    plt.xlabel("Dates", fontsize=20)
    plt.xticks(fontsize=15)
    plt.ylabel("High Price", fontsize=20)
    plt.yticks(fontsize=15)
    plt.plot(df["High"], linewidth=2, color="green", label="High")
    plt.title("Stock High Price", fontsize=30)
    plt.legend()
    plt.tight_layout()

    filename = f"images/{stock}_{start_date}_{end_date}_high.png"
    image_path = os.path.join("static", "images")
    if not os.path.exists(image_path):
        os.makedirs(image_path)

    plt.savefig(os.path.join("static", filename), dpi=300, bbox_inches="tight")
    plt.close()
    return filename


def show_low_plot(df, stock, start_date, end_date):
    plt.style.use("ggplot")
    plt.figure(figsize=(18, 8), dpi=300)
    plt.grid(True)
    plt.xlabel("Dates", fontsize=20)
    plt.xticks(fontsize=15)
    plt.ylabel("Low Price", fontsize=20)
    plt.yticks(fontsize=15)
    plt.plot(df["Low"], linewidth=2, color="red", label="Low")
    plt.title("Stock Low Price", fontsize=30)
    plt.legend()
    plt.tight_layout()

    filename = f"images/{stock}_{start_date}_{end_date}_low.png"
    image_path = os.path.join("static", "images")
    if not os.path.exists(image_path):
        os.makedirs(image_path)

    plt.savefig(os.path.join("static", filename), dpi=300, bbox_inches="tight")
    plt.close()
    return filename


def show_close_plot(df, stock, start_date, end_date):
    plt.style.use("ggplot")
    plt.figure(figsize=(18, 8), dpi=300)
    plt.grid(True)
    plt.xlabel("Dates", fontsize=20)
    plt.xticks(fontsize=15)
    plt.ylabel("Close Price", fontsize=20)
    plt.yticks(fontsize=15)
    plt.plot(df["Close"], linewidth=2, color="blue", label="Close")
    plt.title("Stock Close Price", fontsize=30)
    plt.legend()
    plt.tight_layout()

    filename = f"images/{stock}_{start_date}_{end_date}_close.png"
    image_path = os.path.join("static", "images")
    if not os.path.exists(image_path):
        os.makedirs(image_path)

    plt.savefig(os.path.join("static", filename), dpi=300, bbox_inches="tight")
    plt.close()
    return filename


