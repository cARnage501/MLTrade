"""Standard logging configuration for iTradeML."""
from __future__ import annotations

import logging
import os

_LOG_LEVEL = os.getenv("ITRADEML_LOG_LEVEL", "INFO").upper()


def configure_logging() -> None:
    """Configure root logger for console output."""
    logging.basicConfig(
        level=getattr(logging, _LOG_LEVEL, logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
