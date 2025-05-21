from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..extensions.database import db
from ..mixins import FormatMixin  # Use your actual shared mixin


class CancellationReason(db.Model, FormatMixin):
    """Reason provided for appointment cancellation."""

    __tablename__ = "cancellation_reasons"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String, nullable=False)

    appointments: Mapped[list["Appointment"]] = relationship(
        "Appointment",
        back_populates="cancellation_reason",  # Optional: define on Appointment side
        lazy="dynamic"
    )

    def __init__(self, name: str):
        self.name = name
