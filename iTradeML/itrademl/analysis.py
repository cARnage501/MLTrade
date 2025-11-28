from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple
import logging


def calculate_fibonacci_retracement(high: float, low: float) -> Dict[float, float]:
    levels = {
        0.0: high,
        0.236: high - 0.236 * (high - low),
        0.382: high - 0.382 * (high - low),
        0.5: high - 0.5 * (high - low),
        0.618: high - 0.618 * (high - low),
        1.0: low,
    }
    return levels


def _safe_extremes(prices: Iterable[float]) -> Tuple[float, float]:
    values = list(prices)
    if not values:
        raise ValueError("No prices provided for Fibonacci analysis.")
    return max(values), min(values)


@dataclass
class FibonacciSignal:
    symbol: str
    last_close: float
    high: float
    low: float
    levels: Dict[float, float]
    recommendation: str


def build_fibonacci_signals(symbol: str, closes: List[float]) -> FibonacciSignal:
    high, low = _safe_extremes(closes)
    levels = calculate_fibonacci_retracement(high, low)
    last_close = closes[-1]

    recommendation = "hold"
    tolerance = (high - low) * 0.01

    if last_close >= levels[0.382] - tolerance and last_close <= levels[0.382] + tolerance:
        recommendation = "watch for resistance"
    elif last_close >= levels[0.5] - tolerance and last_close <= levels[0.5] + tolerance:
        recommendation = "pivot zone"
    elif last_close <= levels[0.618] + tolerance:
        recommendation = "potential buy"
    elif last_close >= levels[0.236] - tolerance:
        recommendation = "potential take profit"

    logging.info(
        "%s close=%.2f high=%.2f low=%.2f fib_levels=%s recommendation=%s",
        symbol,
        last_close,
        high,
        low,
        levels,
        recommendation,
    )

    return FibonacciSignal(
        symbol=symbol,
        last_close=last_close,
        high=high,
        low=low,
        levels=levels,
        recommendation=recommendation,
    )
