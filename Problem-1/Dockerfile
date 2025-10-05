# Use official Python base
FROM python:3.11-slim

# Create work dir
WORKDIR /app

# Install deps first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py .

# Expose app port
EXPOSE 8000

# Run the app
CMD ["python", "app.py"]
