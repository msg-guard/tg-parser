#!/usr/bin/env python3
"""File operations and output formatting utilities."""

import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, TypeAlias, Union

import aiofiles
from telethon.tl.types import Channel, Chat, User

# Type aliases
EntityType: TypeAlias = User | Chat | Channel
MessageDict: TypeAlias = Dict[str, Union[str, int]]

log = logging.getLogger("telegram_exporter")


async def save_to_json(data: List[MessageDict], filename: str) -> None:
    """Save message data to a JSON file.

    Args:
        data: List of message dictionaries to save
        filename: Output filename

    """
    message_count = len(data)
    log_message = f"💾 Saving {message_count} messages to {filename}"
    log.info(log_message)

    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    async with aiofiles.open(filename, "w", encoding="utf-8") as file:
        await file.write(json_data)

    complete_message = f"✅ Save completed: {filename}"
    log.info(complete_message)


def get_output_filename(entity: EntityType) -> str:
    """Generate an output filename based on entity information and current timestamp.

    Args:
        entity: Telegram entity (User, Chat, or Channel)

    Returns:
        Formatted filename string

    """
    entity_title = getattr(entity, "title", None)
    entity_username = getattr(entity, "username", None)
    entity_id = str(entity.id)

    chat_name = entity_title or entity_username or entity_id
    safe_chat_name = chat_name.replace(" ", "_")

    current_time = datetime.now(timezone.utc)
    timestamp = current_time.strftime("%Y%m%d_%H%M%S")

    return f"{safe_chat_name}_{timestamp}.json"
