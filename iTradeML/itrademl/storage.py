import csv
from pathlib import Path
from typing import Dict, List

from .config import Settings, ensure_data_dir


def load_closes(path: Path) -> List[float]:
    closes: List[float] = []
    with path.open() as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            closes.append(float(row["Close"]))
    return closes


def latest_data_paths(settings: Settings) -> Dict[str, Path]:
    data_dir = ensure_data_dir(settings)
    paths: Dict[str, Path] = {}
    for symbol in settings.symbols:
        filename = data_dir / f"{symbol.replace('/', '_')}_{settings.timeframe}_data.csv"
        if filename.exists():
            paths[symbol] = filename
    return paths
