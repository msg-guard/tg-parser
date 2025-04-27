#!/usr/bin/env python3
"""Telegram client API and message fetching functionality."""

import logging
from typing import Any, Optional, Sequence

from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

from parser.api.entities import EntityType, get_entity_by_id
from parser.models.message import MessageDict, format_message
from parser.utils.file import get_output_filename, save_to_json

log = logging.getLogger("telegram_exporter")


async def init_client(api_id: str, api_hash: str) -> TelegramClient:
    """Initialize and connect a Telegram client.

    Args:
        api_id: Telegram API ID
        api_hash: Telegram API hash

    Returns:
        Connected TelegramClient instance

    """
    session_name = f"exporter_{api_id}"
    client = TelegramClient(session_name, api_id, api_hash)

    log.info("🔌 Connecting to Telegram...")
    await client.start()
    log.info("✅ Connected successfully")

    return client


async def fetch_batch(client: TelegramClient, entity: EntityType, offset_id: int, batch_size: int) -> Any:
    """Fetch a batch of messages from a Telegram entity.

    Args:
        client: Telegram client
        entity: Target entity to fetch messages from
        offset_id: Message ID to start fetching from
        batch_size: Number of messages to fetch

    Returns:
        Batch of messages

    """
    request = GetHistoryRequest(
        peer=entity,
        offset_id=offset_id,
        offset_date=None,
        add_offset=0,
        limit=batch_size,
        max_id=0,
        min_id=0,
        hash=0,
    )
    return await client(request)


async def process_messages(messages: Sequence[Any], result_list: list[MessageDict]) -> tuple[int, int]:
    """Process a batch of messages and add formatted messages to the result list.

    Args:
        messages: List of Telegram message objects
        result_list: List to append formatted messages to

    Returns:
        Tuple of (total_message_count, last_message_id)

    """
    if not messages:
        total_count = len(result_list)
        return total_count, 0

    new_messages = []
    for msg in messages:
        formatted = format_message(msg)
        if formatted:
            new_messages.append(formatted)

    result_list.extend(new_messages)
    total_count = len(result_list)
    last_message = messages[-1]
    last_id = last_message.id

    return total_count, last_id


async def fetch_messages(
    client: TelegramClient,
    entity: EntityType,
    limit: Optional[int] = None,
    batch_size: int = 100,
) -> list[MessageDict]:
    """Fetch messages from a Telegram entity with progress reporting.

    Args:
        client: Telegram client
        entity: Target entity to fetch messages from
        limit: Maximum number of messages to fetch (None for all)
        batch_size: Size of each batch to fetch

    Returns:
        List of formatted message dictionaries

    """
    offset_id = 0
    all_messages: list[MessageDict] = []

    entity_title = getattr(entity, "title", None)
    entity_name = entity_title if entity_title else entity.id
    log_message = f"📥 Starting to fetch messages from chat: {entity_name}"
    log.info(log_message)

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Downloading messages"),
        BarColumn(),
        TextColumn("[bold green]{task.completed}"),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task("", total=None)

        while True:
            history = await fetch_batch(client, entity, offset_id, batch_size)
            message_list = history.messages

            if not message_list:
                break

            total, new_offset = await process_messages(message_list, all_messages)
            progress.update(task, completed=total)
            offset_id = new_offset

            if limit and total >= limit:
                all_messages = all_messages[:limit]
                break

    message_count = len(all_messages)
    log_message = f"✅ Successfully fetched {message_count} messages"
    log.info(log_message)

    return all_messages


async def export_chat(client: TelegramClient, entity: EntityType, limit: Optional[int]) -> None:
    """Export chat messages to a JSON file.

    Args:
        client: Telegram client
        entity: Target entity to export messages from
        limit: Maximum number of messages to export (None for all)

    """
    output_file = get_output_filename(entity)
    log_message = f"📤 Starting export to {output_file}"
    log.info(log_message)

    try:
        messages = await fetch_messages(client, entity, limit)
        await save_to_json(messages, output_file)
        log.info("🎉 Export completed successfully")
    except Exception as e:
        log.error("❌ Export failed: %s", e)
        raise


async def run_export(api_id: str, api_hash: str, chat_id: str, limit: Optional[int] = None) -> None:
    """Run the export process from start to finish.

    Args:
        api_id: Telegram API ID
        api_hash: Telegram API hash
        chat_id: Target chat ID to export
        limit: Maximum number of messages to export (None for all)

    """
    client = None

    try:
        client = await init_client(api_id, api_hash)
        entity = await get_entity_by_id(client, chat_id)
        await export_chat(client, entity, limit)
    finally:
        if client:
            log.info("👋 Disconnecting...")
            await client.disconnect()
            log.info("✅ Disconnected")
