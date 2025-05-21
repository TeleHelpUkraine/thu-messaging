from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Mapped, mapped_column
from ..extensions.database import db
from ..mixins import FormatMixin


class TreatmentNote(db.Model, FormatMixin):
    """Translation-related treatment notes attached to an appointment."""

    __tablename__ = "treatment_notes"

    id: Mapped[int] = mapped_column(primary_key=True)

    practitioner_id: Mapped[Optional[int]] = mapped_column(db.BigInteger, nullable=True)
    account_id: Mapped[Optional[int]] = mapped_column(db.Integer, nullable=True)
    patient_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("patients.id"))
    interpreter_id: Mapped[Optional[int]] = mapped_column(db.Integer, db.ForeignKey("interpreters.id"), nullable=True)
    appointment_id: Mapped[Optional[int]] = mapped_column(db.Integer, db.ForeignKey("appointments.id"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo("UTC"))
    )
    finalized_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo("UTC"))
    )

    assigned_date: Mapped[Optional[datetime]] = mapped_column(db.DateTime(timezone=True), nullable=True, default=None)
    translated_date: Mapped[Optional[datetime]] = mapped_column(db.DateTime(timezone=True), nullable=True, default=None)

    download_info: Mapped[str] = mapped_column(db.String, nullable=True, default=' ')
    cliniko_id: Mapped[int] = mapped_column(db.BigInteger, unique=True, nullable=False)

    def __init__(
        self,
        practitioner_id: Optional[int],
        account_id: Optional[int],
        cliniko_id: int,
        patient_id: int,
        assigned_date: Optional[datetime] = None,
        appointment_id: Optional[int] = None,
        translated_date: Optional[datetime] = None,
        interpreter_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        download_info: Optional[str] = None,
        finalized_at: Optional[datetime] = None
    ):
        self.practitioner_id = practitioner_id
        self.account_id = account_id
        self.patient_id = patient_id
        self.created_at = created_at or datetime.now(ZoneInfo("UTC"))
        self.assigned_date = assigned_date
        self.translated_date = translated_date
        self.cliniko_id = cliniko_id
        self.interpreter_id = interpreter_id
        self.appointment_id = appointment_id
        self.download_info = download_info or ''
        self.finalized_at = finalized_at or datetime.now(ZoneInfo("UTC"))
