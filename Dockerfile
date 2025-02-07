# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies needed for building some Python packages (e.g., psycopg2)
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory to /app (this will be our repository root inside the container)
WORKDIR /app

# Copy the requirements file first to leverage Docker caching if dependencies haven’t changed
COPY requirements.txt /app/

# Upgrade pip and install the dependencies from requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire repository into the container
COPY . /app/

# Run Django's collectstatic command.
# Since manage.py is in the AstronautWebAPI directory, call it accordingly.
RUN python AstronautWebAPI/manage.py collectstatic --noinput

# Expose the port (Railway sets the $PORT environment variable)
EXPOSE $PORT

# Run the application using Gunicorn.
# Gunicorn will use the WSGI application found in AstronautWebAPI/wsgi.py.
CMD ["gunicorn", "AstronautWebAPI.wsgi:application", "--bind", "0.0.0.0:$PORT"]
