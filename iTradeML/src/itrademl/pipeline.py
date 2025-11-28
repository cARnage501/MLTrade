"""High-level orchestration for the iTradeML stack."""
from __future__ import annotations

import json
import logging
from pathlib import Path

from itrademl import logging_config
from itrademl.data.synthetic import generate_trend
from itrademl.strategy.basic import BasicStrategy, Signal

logger = logging.getLogger(__name__)


def run_offline_demo(output_dir: str | Path = "./data/outputs") -> list[Signal]:
    """Generate synthetic data and return strategy signals."""
    logging_config.configure_logging()

    bars = generate_trend()
    strategy = BasicStrategy()
    signals = strategy.evaluate(bars)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    json_path = output_path / "synthetic_signals.json"
    with json_path.open("w", encoding="utf-8") as fp:
        json.dump(
            [{"timestamp": s.timestamp.isoformat(), "action": s.action, "price": s.price} for s in signals],
            fp,
            indent=2,
        )
    logger.info("Saved %s signals to %s", len(signals), json_path)
    return signals


def describe_architecture() -> str:
    """Return a human-readable description of the modular architecture."""
    return (
        "iTradeML is organized into modular layers: data acquisition (ccxt-powered with "
        "optional synthetic generators), feature engineering (technical indicators like "
        "Fibonacci retracements), strategy logic (signal generation), and experiment "
        "pipelines for backtesting or live trading."
    )
