FROM python:3.12-slim

WORKDIR /app

# Cache buster - force rebuild
RUN echo "Cache buster: $(date)" > /tmp/cache_buster

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Set environment variables
ENV PYTHONPATH=/app
ENV DATABASE_URL=sqlite:///./costco_ocr.db

# Expose port (Railway will override this)
EXPOSE 8000

# Run with Railway PORT handling
CMD python -c "import os; import uvicorn; from app.main import app; uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))" 