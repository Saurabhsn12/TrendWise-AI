# Use Python 3.11 slim image for a smaller, secure base
FROM python:3.11.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for building python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data during the build process to save time/memory during runtime
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('vader_lexicon')"

# Copy the rest of the application code
COPY . .

# Expose port 7860 (Hugging Face Spaces default port)
EXPOSE 7860

# Command to run the application using Gunicorn
CMD ["gunicorn", "--workers=2", "--threads=4", "--worker-class=gthread", "-b", "0.0.0.0:7860", "wsgi:app"]
