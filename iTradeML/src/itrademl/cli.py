"""Command-line interface for iTradeML."""
from __future__ import annotations

import argparse
import logging

from itrademl import logging_config
from itrademl.pipeline import describe_architecture, run_offline_demo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="iTradeML modular trading toolkit")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("demo", help="Run the offline synthetic data demo")
    subparsers.add_parser("describe", help="Print the modular architecture summary")
    return parser


def main(argv: list[str] | None = None) -> int:
    logging_config.configure_logging()
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "demo":
        signals = run_offline_demo()
        logging.info("Demo complete with %s signals", len(signals))
    elif args.command == "describe":
        print(describe_architecture())
    else:
        parser.print_help()
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
