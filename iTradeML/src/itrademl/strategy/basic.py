"""Baseline strategy using moving averages and fibonacci levels."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from statistics import mean
from typing import List

from itrademl.config import settings
from itrademl.data.synthetic import PriceBar
from itrademl.indicators.fibonacci import append_levels

logger = logging.getLogger(__name__)


@dataclass
class Signal:
    timestamp: object
    action: str
    price: float


class BasicStrategy:
    """Generate trade signals using SMA crossovers and fibonacci confluence."""

    def __init__(self, fast: int | None = None, slow: int | None = None):
        self.fast = fast or settings.strategy.fast_window
        self.slow = slow or settings.strategy.slow_window

    def evaluate(self, bars: List[PriceBar]) -> List[Signal]:
        enriched = append_levels(bars)
        closes = [row["close"] for row in enriched]

        signals: List[Signal] = []
        for idx, row in enumerate(enriched):
            if idx + 1 < self.slow:
                continue
            fast_window = closes[idx - self.fast + 1 : idx + 1]
            slow_window = closes[idx - self.slow + 1 : idx + 1]
            sma_fast = mean(fast_window)
            sma_slow = mean(slow_window)

            fib_prices = [v for k, v in row.items() if k.startswith("fib_")]
            near_support = row["close"] <= min(fib_prices) * 1.01
            near_resistance = row["close"] >= max(fib_prices) * 0.99

            if sma_fast > sma_slow and near_support:
                signals.append(Signal(timestamp=row["timestamp"], action="BUY", price=row["close"]))
            elif sma_fast < sma_slow and near_resistance:
                signals.append(Signal(timestamp=row["timestamp"], action="SELL", price=row["close"]))

        logger.info("Generated %s signals", len(signals))
        return signals
