# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /AstronautWebAPI

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /AstronautWebAPI/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port (Railway sets $PORT dynamically)
EXPOSE $PORT

# Run the application
CMD gunicorn AstronautWebAPI.wsgi:application --bind 0.0.0.0:$PORT
