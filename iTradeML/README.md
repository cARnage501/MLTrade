# iTradeML

A modular crypto market toolkit that follows the architecture described in `ModularizedArchitecure.docx`. The project focuses on data collection, Fibonacci-based analysis, and simple reporting across a curated list of top trading pairs.

## Features
- **Top 25 symbols** drawn from the notebooks (`BTC/USDT`, `ETH/USDT`, and more) are loaded by default.
- **Async data collection** via `ccxt` with rate limiting enabled to stay exchange-friendly.
- **Historical OHLCV export** to CSV for every tracked symbol.
- **Fibonacci retracement scan** that builds a light-weight recommendation (buy/hold/take profit zones).
- **Configurable runtime** through environment variables or a JSON config file.
- **Containerized** with a single Dockerfile for running the bot end-to-end.

## Project layout
```
itrademl/
  __init__.py
  __main__.py          # Entry point: python -m itrademl
  analysis.py          # Fibonacci calculations and recommendations
  bot.py               # Orchestration, reporting, CLI entry
  config.py            # Settings loader (env or JSON), default symbols
  data_collector.py    # Async ccxt client for ticker + OHLCV
  storage.py           # CSV helpers for persisted candle data
config.example.json    # Example configuration payload
Dockerfile             # Container definition
requirements.txt       # Python dependencies
```

## Configuration
The bot loads settings from environment variables first and falls back to `config.example.json` format when a path is provided.

| Env var | Purpose | Default |
| --- | --- | --- |
| `ITRADEML_API_KEY` | Binance API key | empty |
| `ITRADEML_API_SECRET` | Binance secret | empty |
| `ITRADEML_TIMEFRAME` | Candle timeframe (ccxt syntax) | `1d` |
| `ITRADEML_MONTHS` | How many months of history to fetch | `6` |
| `ITRADEML_SYMBOLS` | Comma-separated symbols list | top 25 defaults |
| `ITRADEML_DATA_DIR` | Directory to store CSV exports | `data` |

To persist a JSON config:
```
python - <<'PY'
from pathlib import Path
from itrademl.config import Settings
Settings.from_env().to_json(Path("config.json"))
PY
```

## Running locally
Install dependencies and invoke the package entry point:
```
pip install -r requirements.txt
python -m itrademl
```

## Docker usage
Build and run the container with your API keys:
```
docker build -t itrademl:latest .
docker run -e ITRADEML_API_KEY=your_key -e ITRADEML_API_SECRET=your_secret itrademl:latest
```
The container writes CSVs to `/app/data` inside the image.

## Notes
- Exchange calls rely on Binance via `ccxt`. If you want to test offline, set `ITRADEML_SYMBOLS` to a small list and mock the CSVs in the `data/` directory.
- Logging defaults to `INFO` level and prints to stdout for container compatibility.
