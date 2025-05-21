from thu_messaging.extensions.database import db
from ..mixins import CRUDMixin, FormatMixin 

class Message(db.Model, CRUDMixin, FormatMixin):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=True)
    sender = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    messenger = db.Column(db.String(20), default="internal", nullable=False)
    message_metadata = db.Column(db.JSON, nullable=True)
    attachment_url = db.Column(db.Text, nullable=True)
    read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Message from {self.sender} to {self.phone} at {self.timestamp}>"
