"""Fibonacci retracement calculations."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from itrademl.data.synthetic import PriceBar


@dataclass
class FibonacciLevels:
    high: float
    low: float
    levels: dict[float, float]


DEFAULT_LEVELS = (0.236, 0.382, 0.5, 0.618, 0.786)


def compute_levels(high: float, low: float, levels: Iterable[float] = DEFAULT_LEVELS) -> FibonacciLevels:
    diff = high - low
    computed = {round(level, 3): high - diff * level for level in levels}
    return FibonacciLevels(high=high, low=low, levels=computed)


def append_levels(bars: List[PriceBar], levels: Iterable[float] = DEFAULT_LEVELS) -> List[dict]:
    """Return list of dicts with fibonacci levels attached."""
    enriched = []
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    for idx, bar in enumerate(bars):
        window_high = max(highs[max(0, idx - 49) : idx + 1])
        window_low = min(lows[max(0, idx - 49) : idx + 1])
        fibs = compute_levels(window_high, window_low, levels)
        row = {
            "timestamp": bar.timestamp,
            "open": bar.open,
            "high": bar.high,
            "low": bar.low,
            "close": bar.close,
            "volume": bar.volume,
        }
        for level, price in fibs.levels.items():
            row[f"fib_{level:.3f}"] = price
        enriched.append(row)
    return enriched
