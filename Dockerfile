# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies required for psycopg2 (pg_config, gcc, etc.)
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables to prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside the container
WORKDIR /AstronautWebAPI

# Copy requirements.txt into the container’s working directory
COPY requirements.txt ./

# Upgrade pip and install the dependencies from requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project into the container
COPY . .

# Collect static files (if applicable)
RUN python manage.py collectstatic --noinput

# Expose the port (Railway sets $PORT dynamically)
EXPOSE $PORT

# Run the application using Gunicorn
CMD gunicorn AstronautWebAPI.wsgi:application --bind 0.0.0.0:$PORT
