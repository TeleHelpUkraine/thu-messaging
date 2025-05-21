from datetime import datetime
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..extensions.database import db
from ..mixins import CRUDMixin, FormatMixin
from .cliniko_appointment_type import services_practitioners
from .language import languages_practitioners


class ClinikoPractitioner(db.Model, CRUDMixin, FormatMixin):
    """Practitioners from Cliniko"""

    __tablename__ = "practitioners"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliniko_practitioner_id = db.Column(
            db.BigInteger, nullable=False, unique=True
        )
    name: Mapped[str] = mapped_column(db.String, nullable=False)
    email: Mapped[str] = mapped_column(db.String, nullable=False)
    tz: Mapped[str] = mapped_column(db.String, nullable=False)

    cliniko_account_id: Mapped[int] = mapped_column(
        db.ForeignKey("cliniko_accounts.id", ondelete="SET NULL"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), nullable=False)
    last_updated: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True), default=datetime.now, nullable=False
    )

    specialization: Mapped[str] = mapped_column(db.String, nullable=True)
    information: Mapped[str] = mapped_column(db.String, nullable=True)

    # Language preferences
    first_lang_id: Mapped[int] = mapped_column(db.ForeignKey("languages.id"))
    second_lang_id: Mapped[int] = mapped_column(db.ForeignKey("languages.id"))
    third_lang_id: Mapped[int] = mapped_column(db.ForeignKey("languages.id"))

    # Relationships
    languages: Mapped[List["Language"]] = relationship(
        secondary=languages_practitioners,
        back_populates="practitioners"
    )

    cliniko_appointment_types: Mapped[List["ClinikoAppointmentType"]] = relationship(
        secondary=services_practitioners,
        back_populates="practitioners"
    )

    availability: Mapped[List["PractitionerAvailability"]] = relationship(
        "PractitionerAvailability",
        backref="practitioner",
        order_by="PractitionerAvailability.datetime"
    )

    appointments: Mapped[List["Appointment"]] = relationship(
        "Appointment",
        backref="practitioner",
        order_by="Appointment.datetime"
    )

    def __repr__(self):
        return f"<ClinikoPractitioner {self.name} ({self.cliniko_practitioner_id})>"
