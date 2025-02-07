FROM python:3.9-slim as builder

RUN apt-get update -qq && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt

# Debug: Print gunicorn location
RUN find / -name "gunicorn"  # <-- This helps locate where gunicorn is installed

# Stage 2: Final Image
FROM python:3.9-slim
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY . /app/

EXPOSE $PORT
CMD ["gunicorn", "AstronautWebAPI.wsgi:application", "--bind", "0.0.0.0:$PORT"]
