from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..extensions.database import db
from ..mixins import FormatMixin  # or the correct mixin you're standardizing on


class ClinikoAccount(db.Model, FormatMixin):
    """Medical or mental Cliniko accounts."""
    
    __tablename__ = "cliniko_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String, nullable=False, index=True, unique=True)
    api_key: Mapped[str] = mapped_column(db.String, nullable=True)
    cliniko_id_name: Mapped[str] = mapped_column(db.String, nullable=True)
    business_id: Mapped[str] = mapped_column(db.String, nullable=True)

    # Relationships
    appointment_types: Mapped[List["ClinikoAppointmentType"]] = relationship(
        "ClinikoAppointmentType",
        backref="cliniko_account",
        order_by="ClinikoAppointmentType.id"
    )

    practitioners: Mapped[List["ClinikoPractitioner"]] = relationship(
        "ClinikoPractitioner",
        backref="cliniko_account",
        order_by="ClinikoPractitioner.created_at"
    )

    appointments: Mapped[List["Appointment"]] = relationship(
        "Appointment",
        backref="cliniko_account",
        order_by="Appointment.datetime"
    )

    practitioners_availability: Mapped[List["PractitionerAvailability"]] = relationship(
        "PractitionerAvailability",
        backref="cliniko_account",
        order_by="PractitionerAvailability.datetime"
    )

    def __init__(self, name: str, api_key: str, cliniko_id_name: str, business_id: str):
        self.name = name
        self.api_key = api_key
        self.cliniko_id_name = cliniko_id_name
        self.business_id = business_id
