FROM python:3.9-slim

WORKDIR /app

# Install system dependencies (including PostgreSQL development libraries)
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PORT=8050
ENV DATABASE_URL=postgresql://baseball_user:baseball_password@postgres:5432/baseball_db
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8050

# Start application with Gunicorn
CMD gunicorn --workers 4 --bind 0.0.0.0:$PORT app:server