#!/usr/bin/env python3
"""Command-line interface for the Telegram chat exporter."""

import argparse
import asyncio

from rich.console import Console

from parser.api.client import run_export
from parser.utils.logging import setup_logging

log = setup_logging()
console = Console()


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments namespace

    """
    parser = argparse.ArgumentParser(description="Telegram chat history exporter (JSON only)")
    parser.add_argument("--api_id", type=str, required=True, help="Telegram API ID")
    parser.add_argument("--api_hash", type=str, required=True, help="Telegram API Hash")
    parser.add_argument("--chat_id", type=str, required=True, help="Target chat ID to export")
    parser.add_argument("--limit", type=int, help="Maximum number of messages to export")

    return parser.parse_args()


def main() -> None:
    """Run the Telegram chat exporter."""
    title = "[bold blue]Telegram Chat History Exporter[/bold blue]"
    console.print(title)
    args = parse_arguments()
    asyncio.run(run_export(args.api_id, args.api_hash, args.chat_id, args.limit))


if __name__ == "__main__":
    main()
