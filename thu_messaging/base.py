"""
base.py

Defines the BaseMessenger abstract class, which provides a consistent
interface for integrating with different messaging platforms such as
WhatsApp, Viber, or others.

Each concrete messenger should subclass BaseMessenger and implement all
required abstract methods to ensure uniform interaction with message APIs.
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any


class BaseMessenger(ABC):
    """
    Abstract base class for messenger integrations.

    This defines the core interface for sending messages, templates,
    fetching messages, and handling webhook data.
    """

    def __init__(self, token: str, sender_id: str):
        """
        Initialize the messenger with required credentials.

        Args:
            token (str): Authorization token or API key.
            sender_id (str): Sender's ID or phone number ID (platform-specific).
        """
        self.token = token
        self.sender_id = sender_id

    @abstractmethod
    def send_message(self, to: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> Dict:
        """
        Send a plain text message.

        Args:
            to (str): Recipient's phone number or contact ID.
            content (str): Message text.
            metadata (Optional[Dict[str, Any]]): Optional extra context for logging or storage.

        Returns:
            Dict: API response payload.
        """
        pass

    @abstractmethod
    def send_template(self, to: str, template_name: str, variables: Dict[str, str]) -> Dict:
        """
        Send a platform-specific message template.

        Args:
            to (str): Recipient's contact info.
            template_name (str): Template identifier.
            variables (Dict[str, str]): Mapping of placeholders to values.

        Returns:
            Dict: API response payload.
        """
        pass

    @abstractmethod
    def get_messages(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """
        Retrieve past messages based on filters.

        Args:
            filters (Optional[Dict[str, Any]]): Optional filter criteria like date, sender, etc.

        Returns:
            List[Dict]: List of message records.
        """
        pass

    @abstractmethod
    def parse_webhook(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Parse incoming webhook data into a standardized message format.

        Args:
            data (Dict[str, Any]): Raw webhook payload.

        Returns:
            List[Dict[str, Any]]: Normalized list of message objects.
        """
        pass
