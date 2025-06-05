FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY backend /app

# Create necessary directories
RUN mkdir -p /app/data/reports /app/data/cache /app/logs

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=src.app
ENV FLASK_ENV=development

# Expose the port
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"] 