#!/usr/bin/env python3
"""Logging configuration and utilities."""

import logging

from rich.console import Console
from rich.logging import RichHandler

console = Console()


def setup_logging() -> logging.Logger:
    """Configure and return a logger with rich formatting."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    return logging.getLogger("telegram_exporter")
