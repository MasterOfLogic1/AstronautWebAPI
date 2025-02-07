# Stage 1: Build Stage
FROM python:3.9-slim as builder

RUN apt-get update -qq && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt

# Stage 2: Final Image
FROM python:3.9-slim
WORKDIR /app

# Copy installed Python packages
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/

# Copy gunicorn executable explicitly
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn

COPY . /app/

EXPOSE 8000
CMD ["sh", "-c", "PORT=${PORT:-8000} && gunicorn AstronautWebAPI.wsgi:application --bind 0.0.0.0:$PORT"]
#CMD ["sh", "-c", "gunicorn AstronautWebAPI.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
