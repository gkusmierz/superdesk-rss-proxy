# Use the official lightweight Python image.
FROM python:3.9-slim

# Install necessary packages for SSL/TLS support.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    openssl \
    ca-certificates \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Optionally, you can verify the OpenSSL version.
RUN openssl version -a

# Set the working directory.
WORKDIR /app

# Copy the application code.
COPY app.py /app

# Install Python dependencies.
RUN pip install --no-cache-dir \
    flask \
    cloudscraper \
    requests \
    flask-limiter \
    cryptography

# Expose the port.
EXPOSE 8000

# Run the application.
CMD ["python", "app.py"]
