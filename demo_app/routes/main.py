# demo_app/routes/main.py

from flask import Blueprint, render_template, request, redirect, flash
from thu_messaging.whatsapp.client import WhatsAppMessenger
import os

main_bp = Blueprint("main", __name__)

# Load env values (can move to a config module later)
whatsapp_token = os.getenv("WHATSAPP_TOKEN", "your_token_here")
whatsapp_phone_id = os.getenv("WHATSAPP_PHONE_ID", "your_phone_number_id")
messenger = WhatsAppMessenger(token=whatsapp_token, sender_id=whatsapp_phone_id)

@main_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        phone = request.form["phone"]
        message = request.form["message"]

        try:
            result = messenger.send_message(to=phone, content=message)
            flash(f"Message sent to {phone} ✅", "success")
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")

        return redirect("/")

    return render_template("index.html")
