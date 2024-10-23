# Use the official lightweight Python image.
FROM python:3.9-slim

# Set the working directory in the container.
WORKDIR /app

# Copy the application code to the working directory.
COPY app.py /app

# Install the necessary Python packages.
RUN pip install --no-cache-dir flask cloudscraper

# Expose the port on which the app runs.
EXPOSE 8000

# Run the application.
CMD ["python", "app.py"]
