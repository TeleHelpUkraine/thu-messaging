"""
whatsapp.client

This module provides a WhatsAppMessenger class that integrates with the
Meta WhatsApp Cloud API for sending text and template messages.

It extends the BaseMessenger abstract class and implements platform-specific
behavior for sending messages via HTTP requests. Webhook-based message
receiving is stubbed for future implementation.
"""

import requests
from typing import Dict, List, Optional, Any

from thu_messaging.base import BaseMessenger


class WhatsAppMessenger(BaseMessenger):
    """
    WhatsApp Messenger integration using Meta WhatsApp Cloud API.
    """

    BASE_URL = "https://graph.facebook.com/v18.0"

    def send_message(self, to: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> Dict:
        """
        Send a plain text message via WhatsApp.

        Args:
            to (str): Recipient's WhatsApp number in international format (e.g. +1234567890).
            content (str): Text message content.
            metadata (Optional[Dict[str, Any]]): Extra metadata to attach or store (not sent to API).

        Returns:
            Dict: Response data from Meta API if successful.
        """
        url = f"{self.BASE_URL}/{self.sender_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {
                "body": content
            }
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def send_template(self, to: str, template_name: str, variables: Dict[str, str]) -> Dict:
        """
        Placeholder for sending a WhatsApp template message.

        Args:
            to (str): Recipient's phone number.
            template_name (str): Name of the pre-approved template.
            variables (Dict[str, str]): Mapping of variable placeholders to values.

        Returns:
            Dict: API response once implemented.

        Raises:
            NotImplementedError: Method is not yet implemented.
        """
        raise NotImplementedError("Template sending is not implemented yet.")

    def get_messages(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """
        Placeholder for retrieving messages.

        Note: Meta's WhatsApp Cloud API does not support message history retrieval.
        Messages must be collected via webhook and stored locally.

        Returns:
            List[Dict]: Message data from your storage backend.

        Raises:
            NotImplementedError: Method is not applicable via API.
        """
        raise NotImplementedError("Use webhook-based message collection.")

    def parse_webhook(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Stub for normalizing incoming webhook events from Meta.

        Args:
            data (Dict[str, Any]): Raw webhook payload.

        Returns:
            List[Dict[str, Any]]: Normalized list of message dicts (to be implemented).
        """
        return []
