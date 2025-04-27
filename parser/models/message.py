#!/usr/bin/env python3
"""Message data models and formatting utilities."""

from typing import Any, Optional

# Type aliases
MessageDict = dict[str, str | int]


def extract_sender_info(message: Any) -> tuple[str, str]:
    """Extract sender information from a message.

    Args:
        message: Telegram message object

    Returns:
        Tuple of (sender_name, sender_id)

    """
    sender = message.sender
    first_name = getattr(sender, "first_name", "")
    last_name = getattr(sender, "last_name", "")
    full_name = first_name + " " + last_name
    sender_name = full_name.strip() or "Unknown"

    sender_id_raw = message.sender_id
    sender_id = str(sender_id_raw) if sender_id_raw else "Unknown"

    return sender_name, sender_id


def format_message(message: Any) -> Optional[MessageDict]:
    """Format a Telegram message into a dictionary.

    Args:
        message: Telegram message object

    Returns:
        Formatted message dictionary or None if message is empty

    """
    message_text = message.message
    if not message_text:
        return None

    sender_name, sender_id = extract_sender_info(message)
    message_date = message.date
    formatted_date = message_date.strftime("%Y-%m-%d %H:%M:%S")
    message_id = message.id

    return {
        "id": message_id,
        "date": formatted_date,
        "sender_id": sender_id,
        "sender_name": sender_name,
        "text": message_text,
    }
