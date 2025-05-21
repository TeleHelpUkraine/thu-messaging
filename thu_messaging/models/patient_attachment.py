from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from ..extensions.database import db
from ..mixins.format import FormatMixin


class PatientAttachment(db.Model, FormatMixin):
    """Attachments related to a patient appointment and interpreter."""

    __tablename__ = "patient_attachments"

    id: Mapped[int] = mapped_column(primary_key=True)

    cliniko_medical_id: Mapped[Optional[int]] = mapped_column(db.BigInteger, nullable=True)
    cliniko_mental_id: Mapped[Optional[int]] = mapped_column(db.BigInteger, nullable=True)

    patient_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=False
    )

    interpreter_id: Mapped[Optional[int]] = mapped_column(
        db.Integer,
        db.ForeignKey("interpreters.id"),
        nullable=True
    )

    appointment_id: Mapped[Optional[int]] = mapped_column(
        db.Integer,
        db.ForeignKey("appointments.id"),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        default=datetime.utcnow
    )

    assigned_date: Mapped[Optional[datetime]] = mapped_column(
        db.DateTime(timezone=True),
        nullable=True,
        default=None
    )

    translated_date: Mapped[Optional[datetime]] = mapped_column(
        db.DateTime(timezone=True),
        nullable=True,
        default=None
    )

    filename: Mapped[Optional[str]] = mapped_column(db.String, nullable=True)

    download_info: Mapped[str] = mapped_column(
        db.String,
        default=" "
    )

    def __init__(
        self,
        cliniko_medical_id: Optional[int] = None,
        cliniko_mental_id: Optional[int] = None,
        assigned_date: Optional[datetime] = None,
        appointment_id: Optional[int] = None,
        translated_date: Optional[datetime] = None,
        interpreter_id: Optional[int] = None,
        patient_id: int = None,
        created_at: Optional[datetime] = None,
        filename: Optional[str] = None
    ):
        self.cliniko_medical_id = cliniko_medical_id
        self.cliniko_mental_id = cliniko_mental_id
        self.patient_id = patient_id
        self.created_at = created_at or datetime.utcnow()
        self.filename = filename
        self.assigned_date = assigned_date
        self.translated_date = translated_date
        self.interpreter_id = interpreter_id
        self.appointment_id = appointment_id
        self.download_info = ''
