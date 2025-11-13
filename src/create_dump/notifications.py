# src/create_dump/notifications.py

"""Handles sending notifications."""

from __future__ import annotations

import httpx
from .logging import logger

class NotificationManager:
    """Handles sending notifications."""

    def __init__(self, topic: str | None):
        self.topic = topic

    async def send(self, message: str) -> None:
        """Sends a notification to the configured topic."""
        if not self.topic:
            return

        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"https://ntfy.sh/{self.topic}",
                    content=message,
                    headers={"Title": "Create Dump Notification"},
                )
        except httpx.HTTPError as e:
            logger.error("Failed to send notification", error=str(e))
