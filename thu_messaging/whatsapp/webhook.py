# thu_messaging/whatsapp/webhook.py

def parse_whatsapp_webhook(data):
    """
    Parse WhatsApp webhook payload from Meta and extract standardized fields.

    Expected output format:
    {
        "phone": "+1234567890",
        "sender": "patient",
        "content": "Message text",
        "timestamp": datetime_obj,
        "messenger": "whatsapp",
        "message_metadata": {...}
    }
    """
    # TODO: handle real webhook structure here
    return None  # or parsed dictionary if valid
