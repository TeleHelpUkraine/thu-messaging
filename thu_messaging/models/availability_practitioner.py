from datetime import datetime
from zoneinfo import ZoneInfo
import logging

from typing import Optional
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Mapped, mapped_column
from ..extensions.database import db
from ..mixins import FormatMixin


class PractitionerAvailability(db.Model, FormatMixin):
    """Availability slots for Cliniko practitioners."""

    __tablename__ = "practitioners_availability"

    id: Mapped[int] = mapped_column(db.BigInteger, primary_key=True)

    timestamp: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        nullable=False
    )

    cliniko_practitioner_id: Mapped[int] = mapped_column(
        db.BigInteger,
        db.ForeignKey('practitioners.cliniko_practitioner_id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False
    )

    cliniko_appointment_id: Mapped[Optional[int]] = mapped_column(
        db.BigInteger,
        db.ForeignKey("appointments.cliniko_appointment_id", ondelete='CASCADE'),
        nullable=True
    )

    cliniko_account_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey("cliniko_accounts.id", ondelete='CASCADE'),
        nullable=False
    )

    booked: Mapped[Optional[bool]] = mapped_column(db.Boolean, nullable=True, default=False)
    canceled: Mapped[Optional[bool]] = mapped_column(db.Boolean, nullable=True, default=False)

    created_at: Mapped[Optional[datetime]] = mapped_column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(tz=ZoneInfo("UTC")),
        nullable=True
    )

    __table_args__ = (
        db.UniqueConstraint("cliniko_practitioner_id", "timestamp", name="uq_practitioner_datetime_appointment"),
    )

    @classmethod
    def create_availability(
        cls,
        session,
        cliniko_practitioner_id: int,
        datetime_value: datetime,
        cliniko_account_id: int
    ) -> Optional["PractitionerAvailability"]:
        """Creates a new availability if one doesn't already exist for that time and practitioner."""

        # Ensure datetime is timezone-aware
        if datetime_value.tzinfo is None:
            datetime_value = datetime_value.replace(tzinfo=ZoneInfo("UTC"))

        try:
            existing_entry = session.query(cls).filter_by(
                cliniko_practitioner_id=cliniko_practitioner_id,
                datetime=datetime_value
            ).first()

            if existing_entry:
                logging.info(
                    f"⚠️ Availability already exists for Practitioner {cliniko_practitioner_id} at {datetime_value}. Skipping insert."
                )
                return existing_entry

            new_availability = cls(
                cliniko_practitioner_id=cliniko_practitioner_id,
                datetime=datetime_value,
                cliniko_account_id=cliniko_account_id
            )

            session.add(new_availability)
            session.commit()
            logging.info(
                f"✅ New availability created for Practitioner {cliniko_practitioner_id} at {datetime_value}."
            )
            return new_availability

        except IntegrityError:
            session.rollback()
            logging.error(
                f"❌ Duplicate availability for Practitioner {cliniko_practitioner_id} at {datetime_value}."
            )
            return None

        except SQLAlchemyError as e:
            session.rollback()
            logging.error(
                f"❌ Database error while creating availability for Practitioner {cliniko_practitioner_id}: {e}"
            )
            return None
