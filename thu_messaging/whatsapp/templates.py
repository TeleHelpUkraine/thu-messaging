"""
templates.py

This module provides helper functions for building WhatsApp template messages
in the format required by Meta's WhatsApp Cloud API.

Templates must be pre-approved in your WhatsApp Business Manager dashboard.
This module supports text-based templates with variable substitution.
"""

from typing import Dict, List


def build_template_payload(
    to: str,
    sender_id: str,
    template_name: str,
    language: str = "en_US",
    variables: List[str] = None
) -> Dict:
    """
    Build the JSON payload for sending a WhatsApp template message.

    Args:
        to (str): Recipient's phone number (e.g. '+1234567890').
        sender_id (str): WhatsApp Business phone number ID.
        template_name (str): Name of the approved template in Meta.
        language (str): Language code for the template (default: 'en_US').
        variables (List[str]): List of variables to inject into the template.

    Returns:
        Dict: Payload formatted for Meta WhatsApp API.
    """
    components = []

    if variables:
        components.append({
            "type": "body",
            "parameters": [{"type": "text", "text": v} for v in variables]
        })

    return {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language},
            "components": components
        }
    }
