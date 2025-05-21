from datetime import datetime
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..extensions.database import db
from ..mixins import CRUDMixin, FormatMixin
from .language import languages_interpreters


class Interpreter(db.Model, CRUDMixin, FormatMixin):
    __tablename__ = "interpreters"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(db.String, nullable=False)
    last_name: Mapped[str] = mapped_column(db.String, nullable=False)
    email: Mapped[str] = mapped_column(db.String, nullable=False, unique=True)
    tz: Mapped[str] = mapped_column(db.String, nullable=False)

    U: Mapped[bool] = mapped_column(db.Boolean, nullable=True)
    R: Mapped[bool] = mapped_column(db.Boolean, nullable=True)

    first_lang_id: Mapped[int] = mapped_column(db.ForeignKey('languages.id'))
    second_lang_id: Mapped[int] = mapped_column(db.ForeignKey('languages.id'))

    mental_apts: Mapped[bool] = mapped_column(db.Boolean, nullable=True)
    cliniko_medical_id: Mapped[int] = mapped_column(db.BigInteger, nullable=True)
    cliniko_mental_id: Mapped[int] = mapped_column(db.BigInteger, nullable=True)
    auth0_id: Mapped[str] = mapped_column(db.String, nullable=True)

    last_updated: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), default=datetime.now)

    languages: Mapped[List["Language"]] = relationship(
        secondary=languages_interpreters,
        back_populates="interpreters"
    )

    availability: Mapped[List["InterpreterTimes"]] = relationship(
        "InterpreterTimes",
        backref="interpreter",
        lazy="dynamic",
        passive_deletes=True,
        order_by="InterpreterTimes.datetime"
    )

    appointments: Mapped[List["Appointment"]] = relationship(
        "Appointment",
        backref="interpreter"
    )

    attachments: Mapped[List["PatientAttachment"]] = relationship(
        "PatientAttachment",
        backref="interpreter"
    )

    def format(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "U": self.U,
            "R": self.R,
            "tz": self.tz,
            "cliniko_medical_id": self.cliniko_medical_id,
            "cliniko_mental_id": self.cliniko_mental_id,
            "auth0_id": self.auth0_id,
            "mental_apts": self.mental_apts,
            "appointments_ids": [a.id for a in self.appointments],
            "availability_count": self.availability.count() if self.availability else 0
        }

    def __repr__(self):
        return (
            f"<Interpreter {self.first_name} {self.last_name}, ID: {self.id}, "
            f"Email: {self.email}, U: {self.U}, R: {self.R}, TZ: {self.tz}, "
            f"Mental ID: {self.cliniko_mental_id}, Medical ID: {self.cliniko_medical_id}, "
            f"auth0_id: {self.auth0_id}, Mental_apts: {self.mental_apts}>"
        )
