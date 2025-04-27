#!/usr/bin/env python3
"""Entity resolution utilities for Telegram API entities."""

import logging
from typing import Optional, Type

from telethon import TelegramClient
from telethon.tl.types import (
    Channel,
    Chat,
    PeerChannel,
    PeerChat,
    PeerUser,
    User,
)

# Type aliases
EntityType = User | Chat | Channel

log = logging.getLogger("telegram_exporter")


async def resolve_by_username(client: TelegramClient, username: str) -> EntityType:
    """Resolve entity by username.

    Args:
        client: Telegram client
        username: Username to resolve

    Returns:
        Resolved entity

    """
    log_message = f"🔍 Resolving entity by username: {username}"
    log.info(log_message)
    return await client.get_entity(username)


async def resolve_by_peer_type(
    client: TelegramClient,
    chat_id: int,
    peer_class: Type[PeerUser] | Type[PeerChat] | Type[PeerChannel],
) -> Optional[EntityType]:
    """Resolve entity using a specific peer class.

    Args:
        client: Telegram client
        chat_id: Chat ID to resolve
        peer_class: PeerUser, PeerChat, or PeerChannel class

    Returns:
        Resolved entity or None if not found

    """
    peer_instance = peer_class(chat_id)
    try:
        return await client.get_entity(peer_instance)
    except Exception:
        return None


async def resolve_as_channel(client: TelegramClient, chat_id: int) -> Optional[EntityType]:
    """Resolve entity as a channel using the -100 prefix convention.

    Args:
        client: Telegram client
        chat_id: Chat ID to resolve

    Returns:
        Resolved entity or None if not found

    """
    try:
        channel_id_str = f"-100{chat_id}"
        channel_id = int(channel_id_str)
        peer = PeerChannel(channel_id)
        return await client.get_entity(peer)
    except Exception:
        return None


async def resolve_from_negative_id(client: TelegramClient, chat_id: int) -> Optional[EntityType]:
    """Resolve entity from a negative ID, attempting to extract a channel ID.

    Args:
        client: Telegram client
        chat_id: Negative chat ID to resolve

    Returns:
        Resolved entity or None if not found

    """
    abs_id = abs(chat_id)
    abs_id_str = str(abs_id)

    if not abs_id_str.startswith("100"):
        return None

    try:
        orig_id_str = abs_id_str[3:]
        orig_id = int(orig_id_str)
        peer = PeerChannel(orig_id)
        return await client.get_entity(peer)
    except Exception:
        return None


async def get_entity_by_id(client: TelegramClient, chat_id: str | int) -> EntityType:
    """Get a Telegram entity by ID or username.

    Args:
        client: Telegram client
        chat_id: Chat ID (numeric or username) to resolve

    Returns:
        Resolved entity

    Raises:
        ValueError: If entity cannot be found

    """
    if isinstance(chat_id, str):
        is_numeric = chat_id.strip("-").isdigit()
        if is_numeric:
            numeric_id = int(chat_id)
            return await resolve_numeric_id(client, numeric_id)
        return await resolve_by_username(client, chat_id)
    return await resolve_numeric_id(client, chat_id)


async def resolve_numeric_id(client: TelegramClient, chat_id: int) -> EntityType:
    """Resolve entity by numeric ID using multiple resolution strategies.

    Args:
        client: Telegram client
        chat_id: Numeric chat ID to resolve

    Returns:
        Resolved entity

    Raises:
        ValueError: If entity cannot be found

    """
    log_message = f"🔍 Resolving entity by ID: {chat_id}"
    log.info(log_message)

    peer_types = [PeerUser, PeerChat, PeerChannel]
    for peer_type in peer_types:
        entity = await resolve_by_peer_type(client, chat_id, peer_type)
        if entity:
            return entity

    if chat_id > 0:
        entity = await resolve_as_channel(client, chat_id)
        if entity:
            return entity

    if chat_id < 0:
        entity = await resolve_from_negative_id(client, chat_id)
        if entity:
            return entity

    try:
        return await client.get_entity(chat_id)
    except Exception as e:
        error_message = f"❌ Failed to find chat with ID {chat_id}: {e}"
        log.error(error_message)
        error_text = f"Could not find chat with ID {chat_id}"
        raise ValueError(error_text) from e
