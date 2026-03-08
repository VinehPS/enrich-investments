# Use the official Python concise image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for compiling some python packages like cryptography)
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies first (to leverage Docker caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Cloud Run defaults to 8080)
EXPOSE 8080

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
