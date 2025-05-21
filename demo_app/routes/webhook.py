# demo_app/routes/webhook.py

from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from thu_messaging.whatsapp.webhook import parse_whatsapp_webhook
from thu_messaging.extensions.database import db
from thu_messaging.models.message import Message

webhook_bp = Blueprint("webhook", __name__)

@webhook_bp.route("/webhook", methods=["GET"])
def verify():
    """
    WhatsApp webhook verification (Meta)
    """
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == "your_verify_token":
        return challenge, 200
    return "Verification failed", 403


@webhook_bp.route("/webhook", methods=["POST"])
def receive_message():
    """
    Receive messages from Meta WhatsApp webhook and save to DB.
    """
    try:
        data = request.get_json(force=True)
        parsed = parse_whatsapp_webhook(data)

        if parsed:
            msg = Message.create(**parsed)
            return jsonify({"status": "saved"}), 200
        return jsonify({"status": "ignored"}), 200

    except BadRequest:
        return jsonify({"error": "Invalid JSON"}), 400
