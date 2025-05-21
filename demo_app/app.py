"""
demo_app Flask app

Simple example interface to send WhatsApp messages using the thu_messaging library.
"""

import os
from flask import Flask, render_template, request, redirect, flash

from dotenv import load_dotenv
load_dotenv()


from thu_messaging.whatsapp.client import WhatsAppMessenger

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "dev-secret")  # for flash messages

# Read token and sender ID from env (or fallback to dummy values for dev)
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "your_token_here")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID", "your_phone_number_id")

# Instantiate the WhatsApp client
messenger = WhatsAppMessenger(token=WHATSAPP_TOKEN, sender_id=WHATSAPP_PHONE_ID)


@app.route("/", methods=["GET", "POST"])
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
