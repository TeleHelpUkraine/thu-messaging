from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), nullable=False)
    sender = db.Column(db.String(20), nullable=False)  # 'admin' or 'patient'
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    messenger = db.Column(db.String(20), default='WhatsApp')
    message_metadata = db.Column(db.JSON, nullable=True)
