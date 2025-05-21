from datetime import datetime
from typing import List
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..extensions.database import db
from ..mixins import FormatMixin  # replace with the actual mixin you're standardizing on

# Association table
services_practitioners = db.Table(
    "services_practitioners",
    db.Column("service_id", db.ForeignKey("cliniko_appointment_types.id"), primary_key=True),
    db.Column("practitioner_id", db.ForeignKey("practitioners.id"), primary_key=True),
)


class ClinikoAppointmentType(db.Model, FormatMixin):
    """Service types from Cliniko Accounts."""

    __tablename__ = "cliniko_appointment_types"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    name: Mapped[str] = mapped_column(db.String, nullable=False)
    cliniko_appointment_type_id: Mapped[int] = mapped_column(db.BigInteger, primary_key=True, nullable=False, unique=True)

    cliniko_account_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey("cliniko_accounts.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), default=datetime.utcnow)

    practitioners: Mapped[List["ClinikoPractitioner"]] = relationship(
        secondary=services_practitioners,
        back_populates="cliniko_appointment_types"
    )

    appointments: Mapped[List["Appointment"]] = relationship(
        "Appointment",
        backref="cliniko_appointment_type",
        order_by="Appointment.datetime"
    )

    def __init__(self, name: str, cliniko_account_id: int, cliniko_appointment_type_id: int):
        self.name = name
        self.cliniko_account_id = cliniko_account_id
        self.cliniko_appointment_type_id = cliniko_appointment_type_id
        self.created_at = datetime.utcnow()

    def mobile_service_format(self, language: str) -> dict:
        """Return a dict representation with localized datetime and language-specific name."""
        dict_self = {}

        # Handle localized datetime formatting
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                continue

            if isinstance(value, datetime):
                dict_self[key] = value.astimezone(ZoneInfo("UTC")).strftime("%m/%d/%Y, %H:%M:%S %Z")
            else:
                dict_self[key] = value

        # Handle multilingual name
        if 'name' in dict_self and '|' in dict_self['name']:
            dict_self['name'] = dict_self['name'].split('|')[0 if language == 'en' else 1]

        return dict_self
