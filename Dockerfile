# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies (e.g., for psycopg2)
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory to /app (repository root)
WORKDIR /app

# Copy the requirements file first for caching
COPY requirements.txt /app/

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire repository into the container
COPY . /app/

# Copy the entrypoint script and ensure it is executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the port (Railway sets the $PORT environment variable)
EXPOSE $PORT

# Set the entrypoint and command.
ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "AstronautWebAPI.wsgi:application", "--bind", "0.0.0.0:$PORT"]
