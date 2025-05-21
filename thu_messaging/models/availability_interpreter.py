from datetime import datetime as dt
from zoneinfo import ZoneInfo
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from babel.dates import format_datetime

from ..extensions.database import db
from ..mixins import FormatMixin
from .interpreter import Interpreter


class InterpreterTimes(db.Model, FormatMixin):
    __tablename__ = "availability"

    id: Mapped[int] = mapped_column(db.BigInteger, primary_key=True)

    datetime: Mapped[dt] = mapped_column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: dt.now(tz=ZoneInfo("UTC"))
    )

    interpreter_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey(Interpreter.id, ondelete="CASCADE"),
        nullable=False
    )

    mental_apts: Mapped[Optional[bool]] = mapped_column(db.Boolean, nullable=True)
    U: Mapped[Optional[bool]] = mapped_column(db.Boolean, nullable=True)  # Ukrainian
    R: Mapped[Optional[bool]] = mapped_column(db.Boolean, nullable=True)  # Russian
    booked: Mapped[Optional[bool]] = mapped_column(db.Boolean, nullable=True)
    canceled: Mapped[Optional[bool]] = mapped_column(db.Boolean, nullable=True)

    cliniko_appointment_id: Mapped[Optional[int]] = mapped_column(
        db.BigInteger, nullable=True, default=None, index=True
    )

    appointment: Mapped[Optional["Appointment"]] = relationship(
        "Appointment",
        backref="interpreter_availability"
    )

    def __init__(
        self,
        booked: bool,
        interpreter_id: int,
        datetime: dt,
        canceled: bool,
        U: bool,
        R: bool,
        mental_apts: bool,
        cliniko_appointment_id: Optional[int] = None
    ):
        self.datetime = datetime
        self.interpreter_id = interpreter_id
        self.booked = booked
        self.canceled = canceled
        self.U = U
        self.R = R
        self.mental_apts = mental_apts
        self.cliniko_appointment_id = cliniko_appointment_id

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Insertion failed: {e}")

    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Update failed: {e}")

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Deletion failed: {e}")

    def format(self) -> dict:
        return {
            "id": self.id,
            "datetime": self.datetime,
            "formatted_datetime": format_datetime(
                self.datetime.astimezone(ZoneInfo("US/Pacific"))
            ),
            "interpreter_id": self.interpreter_id,
            "booked": self.booked,
            "canceled": self.canceled,
            "U": self.U,
            "R": self.R,
            "mental_apts": self.mental_apts,
            "cliniko_appointment_id": self.cliniko_appointment_id,
        }

    def __repr__(self) -> str:
        return (
            f"<InterpreterTimes id={self.id}, datetime={self.datetime}, interpreter_id={self.interpreter_id}, "
            f"booked={self.booked}, canceled={self.canceled}, U={self.U}, R={self.R}, "
            f"mental_apts={self.mental_apts}, cliniko_appointment_id={self.cliniko_appointment_id}>"
        )
