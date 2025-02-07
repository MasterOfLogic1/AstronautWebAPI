# Stage 1: Build Stage
FROM python:3.9-slim as builder

RUN apt-get update -qq && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# (Install dependencies here)
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt

# Stage 2: Final Image
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY . /app/
# (Optional: you can re-install only what is needed, or copy the entire virtual environment)
EXPOSE $PORT
CMD ["gunicorn", "AstronautWebAPI.wsgi:application", "--bind", "0.0.0.0:$PORT"]
