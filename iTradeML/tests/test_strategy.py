from itrademl.strategy.basic import BasicStrategy
from itrademl.data.synthetic import generate_trend


def test_strategy_generates_signals():
    bars = generate_trend(steps=80)
    signals = BasicStrategy(fast=5, slow=15).evaluate(bars)
    assert isinstance(signals, list)
    assert all(hasattr(sig, "action") for sig in signals)
