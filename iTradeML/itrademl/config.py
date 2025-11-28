from dataclasses import dataclass, field
from pathlib import Path
import json
import os
from typing import List

DEFAULT_SYMBOLS = [
    "BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "ADA/USDT", "DOGE/USDT",
    "MATIC/USDT", "SOL/USDT", "DOT/USDT", "LTC/USDT", "SHIB/USDT", "AVAX/USDT",
    "TRX/USDT", "LINK/USDT", "ATOM/USDT", "ETC/USDT", "XLM/USDT", "ALGO/USDT",
    "VET/USDT", "FIL/USDT", "MANA/USDT", "SAND/USDT", "AXS/USDT", "THETA/USDT",
    "XTZ/USDT",
]


@dataclass
class Settings:
    api_key: str = ""
    api_secret: str = ""
    timeframe: str = "1d"
    months: int = 6
    symbols: List[str] = field(default_factory=lambda: DEFAULT_SYMBOLS.copy())
    data_dir: Path = Path("data")

    @classmethod
    def from_env(cls) -> "Settings":
        api_key = os.getenv("ITRADEML_API_KEY", "")
        api_secret = os.getenv("ITRADEML_API_SECRET", "")
        timeframe = os.getenv("ITRADEML_TIMEFRAME", "1d")
        months = int(os.getenv("ITRADEML_MONTHS", "6"))
        symbols_env = os.getenv("ITRADEML_SYMBOLS")
        if symbols_env:
            symbols = [symbol.strip() for symbol in symbols_env.split(",") if symbol.strip()]
        else:
            symbols = DEFAULT_SYMBOLS.copy()
        data_dir = Path(os.getenv("ITRADEML_DATA_DIR", "data"))
        return cls(api_key=api_key, api_secret=api_secret, timeframe=timeframe, months=months, symbols=symbols, data_dir=data_dir)

    def to_json(self, path: Path) -> None:
        payload = {
            "api_key": self.api_key,
            "api_secret": self.api_secret,
            "timeframe": self.timeframe,
            "months": self.months,
            "symbols": self.symbols,
            "data_dir": str(self.data_dir),
        }
        path.write_text(json.dumps(payload, indent=2))

    @classmethod
    def from_json(cls, path: Path) -> "Settings":
        payload = json.loads(path.read_text())
        return cls(
            api_key=payload.get("api_key", ""),
            api_secret=payload.get("api_secret", ""),
            timeframe=payload.get("timeframe", "1d"),
            months=int(payload.get("months", 6)),
            symbols=payload.get("symbols", DEFAULT_SYMBOLS.copy()),
            data_dir=Path(payload.get("data_dir", "data")),
        )


def ensure_data_dir(settings: Settings) -> Path:
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    return settings.data_dir
