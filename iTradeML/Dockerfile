FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY itrademl itrademl
COPY config.example.json config.example.json

ENV ITRADEML_TIMEFRAME=1d \
    ITRADEML_MONTHS=6 \
    ITRADEML_DATA_DIR=/app/data

CMD ["python", "-m", "itrademl"]
