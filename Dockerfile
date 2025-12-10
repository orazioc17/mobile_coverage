# Python slim is lightweight but we need some libraries for pandas
FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable stdout flush
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy dependencies first to improve Docker cache efficiency
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app

# Expose Django’s port
EXPOSE 8000

# Default command (development mode)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]