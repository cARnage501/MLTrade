"""Configuration utilities for iTradeML.

This module centralizes environment-driven settings so that services such as
API clients and database connectors can pull values from a single place.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import os


@dataclass
class ExchangeSettings:
    """Exchange-level configuration."""

    exchange_id: str = os.getenv("ITRADEML_EXCHANGE", "binance")
    symbol: str = os.getenv("ITRADEML_SYMBOL", "BTC/USDT")
    api_key: str | None = os.getenv("ITRADEML_API_KEY")
    api_secret: str | None = os.getenv("ITRADEML_API_SECRET")
    rate_limit: bool = os.getenv("ITRADEML_ENABLE_RATE_LIMIT", "true").lower() == "true"


@dataclass
class DataSettings:
    timeframe: str = os.getenv("ITRADEML_TIMEFRAME", "1h")
    lookback_days: int = int(os.getenv("ITRADEML_LOOKBACK_DAYS", "60"))
    cache_dir: Path = Path(os.getenv("ITRADEML_CACHE_DIR", "./data/cache")).resolve()


@dataclass
class StrategySettings:
    fast_window: int = int(os.getenv("ITRADEML_FAST_WINDOW", "10"))
    slow_window: int = int(os.getenv("ITRADEML_SLOW_WINDOW", "25"))
    fibonacci_levels: tuple[float, ...] = field(
        default_factory=lambda: (0.236, 0.382, 0.5, 0.618, 0.786)
    )


@dataclass
class AppSettings:
    """Aggregate configuration."""

    exchange: ExchangeSettings = field(default_factory=ExchangeSettings)
    data: DataSettings = field(default_factory=DataSettings)
    strategy: StrategySettings = field(default_factory=StrategySettings)


settings = AppSettings()
