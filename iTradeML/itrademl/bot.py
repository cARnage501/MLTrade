import asyncio
import logging
from pathlib import Path
from typing import Dict, List

from .analysis import FibonacciSignal, build_fibonacci_signals
from .config import Settings, ensure_data_dir
from .data_collector import DataCollector
from .storage import latest_data_paths, load_closes


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def bootstrap_settings(config_path: Path | None = None) -> Settings:
    if config_path and config_path.exists():
        settings = Settings.from_json(config_path)
    else:
        settings = Settings.from_env()
    ensure_data_dir(settings)
    return settings


async def sync_symbol(collector: DataCollector, symbol: str, settings: Settings) -> Path | None:
    logging.info("Syncing OHLCV data for %s", symbol)
    return await collector.fetch_historical_data(symbol, settings.timeframe, settings.months)


async def sync_all(settings: Settings) -> List[Path | None]:
    async with DataCollector(settings) as collector:
        tasks = [sync_symbol(collector, symbol, settings) for symbol in settings.symbols]
        return await asyncio.gather(*tasks)


def analyze_latest(settings: Settings) -> Dict[str, FibonacciSignal]:
    signals: Dict[str, FibonacciSignal] = {}
    paths = latest_data_paths(settings)
    for symbol, path in paths.items():
        closes = load_closes(path)
        signals[symbol] = build_fibonacci_signals(symbol, closes)
    return signals


def render_report(signals: Dict[str, FibonacciSignal]) -> str:
    lines: List[str] = []
    for signal in signals.values():
        lines.append(
            (
                f"{signal.symbol}: close={signal.last_close:.2f}, high={signal.high:.2f}, "
                f"low={signal.low:.2f}, rec={signal.recommendation}"
            )
        )
    if not lines:
        return "No data available. Run sync to download candles first."
    return "\n".join(lines)


async def main() -> None:
    settings = bootstrap_settings()
    logging.info("Starting iTradeML with %s symbols", len(settings.symbols))
    await sync_all(settings)
    signals = analyze_latest(settings)
    report = render_report(signals)
    print("iTradeML Fibonacci scan")
    print(report)


if __name__ == "__main__":  # pragma: no cover
    asyncio.run(main())
