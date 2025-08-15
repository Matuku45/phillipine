# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose the port your app runs on (should match the port in app.py)
EXPOSE 10000

# Run the Flask app
CMD ["python", "app.py"]
