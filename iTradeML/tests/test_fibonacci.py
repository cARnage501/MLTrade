from itrademl.indicators.fibonacci import compute_levels, append_levels
from itrademl.data.synthetic import PriceBar
from datetime import datetime


def test_compute_levels_basic():
    levels = compute_levels(100, 50)
    assert levels.high == 100
    assert levels.low == 50
    assert round(levels.levels[0.5], 2) == 75.0


def test_append_levels_adds_columns():
    bars = [
        PriceBar(timestamp=datetime.utcnow(), open=10, high=12, low=8, close=11, volume=50),
        PriceBar(timestamp=datetime.utcnow(), open=11, high=13, low=9, close=12, volume=55),
    ]
    result = append_levels(bars)
    assert any(key.startswith("fib_") for key in result[-1].keys())
