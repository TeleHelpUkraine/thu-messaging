"""
demo_app Flask app

Simple example interface to send WhatsApp messages using the thu_messaging library.
Now includes SQLAlchemy integration for messaging database.
"""

import os
from flask import Flask, render_template, request, redirect, flash
from dotenv import load_dotenv
from flask_migrate import Migrate

import thu_messaging.models

from thu_messaging.extensions.database import db
from thu_messaging.whatsapp.client import WhatsAppMessenger
# Optional: import Message model for future use
# from thu_messaging.models.message import Message
from demo_app.routes.main import main_bp
from demo_app.routes.chats import chats_bp
from demo_app.routes.webhook import webhook_bp


load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET", "dev-secret")

    # === 🔌 Database Setup ===
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {"options": "-c timezone=utc"}
    }

    db.init_app(app)
    migrate = Migrate(app, db)

    
    app.register_blueprint(main_bp)
    app.register_blueprint(chats_bp, url_prefix="/chats")
    app.register_blueprint(webhook_bp)

    return app
