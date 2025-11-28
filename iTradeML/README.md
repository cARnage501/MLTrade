# iTradeML

A modular, container-ready crypto trading research stack inspired by the provided
"Modularized Architecture" vision. The project layers data acquisition,
feature engineering, strategy logic, and orchestration into a single toolkit.

## Architecture
- **Data**: `DataCollector` (optional ccxt integration) for live market data and
  `synthetic` for offline time-series generators.
- **Indicators**: Fibonacci retracement helpers to enrich OHLCV-like price bars.
- **Strategy**: `BasicStrategy` pairs SMA crossovers with Fibonacci support/resistance
  to emit BUY/SELL signals.
- **Pipeline**: `pipeline.run_offline_demo` stitches the pieces together to produce
  signals and JSON outputs for inspection.
- **CLI**: `python -m itrademl.cli describe|demo` for quick exploration.

## Getting Started
1. **(Optional) Install extras for live data**
   - `ccxt` is required only if you plan to call `DataCollector`.
   - Offline demo and tests run with the Python standard library.
2. **Run the offline demo**
   ```bash
   python -m itrademl.cli demo
   ```
   This generates synthetic OHLCV data, evaluates the strategy, and writes
   `data/outputs/synthetic_signals.json`.
3. **Describe the architecture**
   ```bash
   python -m itrademl.cli describe
   ```
4. **Fetch live data (optional)**
   - Set `ITRADEML_API_KEY` / `ITRADEML_API_SECRET` and other env vars in
     `.env` or your shell.
   - Install `ccxt` and call `itrademl.data.collector.collect_and_close()` inside a
     script to pull OHLCV data.

## Configuration
Environment variables control defaults:
- `ITRADEML_EXCHANGE` (default: `binance`)
- `ITRADEML_SYMBOL` (default: `BTC/USDT`)
- `ITRADEML_TIMEFRAME` (default: `1h`)
- `ITRADEML_LOOKBACK_DAYS` (default: `60`)
- `ITRADEML_FAST_WINDOW` / `ITRADEML_SLOW_WINDOW`
- `ITRADEML_LOG_LEVEL`

## Tests
```bash
pytest
```

## Containerization
The included Dockerfile builds a minimal image that exposes the CLI entrypoint.
```bash
docker build -t itrademl .
docker run --rm itrademl describe
docker run --rm -v "$PWD/data:/app/data" itrademl demo
```
Mounting `./data` keeps generated signals on the host.
