import asyncio
import csv
import datetime
import logging
from pathlib import Path
from typing import Iterable, List, Optional

import ccxt.async_support as ccxt

from .config import Settings, ensure_data_dir


class DataCollector:
    """Handles async communication with the exchange via ccxt."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = ccxt.binance({
            "apiKey": settings.api_key,
            "secret": settings.api_secret,
            "enableRateLimit": True,
        })
        ensure_data_dir(settings)
        logging.info("Data Collector initialized for Binance.")

    async def __aenter__(self) -> "DataCollector":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def get_current_price(self, symbol: str) -> Optional[float]:
        """Fetch the latest ticker price for a symbol."""
        try:
            ticker = await self.client.fetch_ticker(symbol)
            return float(ticker.get("last", ticker.get("close")))
        except Exception as exc:  # pragma: no cover - depends on network
            logging.error("Error getting current price for %s: %s", symbol, exc)
            return None

    async def fetch_historical_data(
        self, symbol: str, timeframe: str, since_months: int
    ) -> Optional[Path]:
        """Fetch OHLCV data and persist it to a CSV file."""
        if not self.client.has.get("fetchOHLCV", False):
            logging.error("%s does not support fetching OHLCV data.", self.client.id)
            return None

        try:
            since = self.client.parse8601(
                (
                    datetime.datetime.now()
                    - datetime.timedelta(days=since_months * 30)
                ).isoformat()
            )
            klines = await self.client.fetch_ohlcv(symbol, timeframe, since)
            if not klines:
                logging.warning("No OHLCV data returned for %s", symbol)
                return None

            filename = ensure_data_dir(self.settings) / f"{symbol.replace('/', '_')}_{timeframe}_data.csv"
            self._write_csv(filename, klines)
            logging.info("Saved %s candles to %s", len(klines), filename)
            return filename
        except Exception as exc:  # pragma: no cover - depends on network
            logging.error("Error fetching/writing historical data for %s: %s", symbol, exc)
            return None

    def _write_csv(self, path: Path, klines: Iterable[List[float]]) -> None:
        with path.open("w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Timestamp", "Open", "High", "Low", "Close", "Volume"])
            writer.writerows(klines)

    async def close(self) -> None:
        await self.client.close()


async def fetch_prices(settings: Settings) -> List[Optional[float]]:
    async with DataCollector(settings) as collector:
        tasks = [collector.get_current_price(symbol) for symbol in settings.symbols]
        return await asyncio.gather(*tasks)
