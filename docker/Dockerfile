FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/

# Local media storage volume mount point (matches MEDIA_STORAGE_ROOT default)
RUN mkdir -p /app/media_storage

# Expose port
EXPOSE 8045

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8045"]
