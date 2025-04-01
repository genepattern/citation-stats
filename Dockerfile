# Use official Python 3.9.21 image
FROM python:3.9.21-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir pandas numpy openpyxl

# Copy main.py into the container
COPY main.py .

# Default command (can be overridden in docker run)
