from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from thu_messaging.extensions.database import db
from ..mixins import FormatMixin

# Association tables
languages_practitioners = db.Table(
    'languages_practitioners',
    db.Column('language_id', db.Integer, db.ForeignKey('languages.id'), primary_key=True),
    db.Column('doctor_id', db.Integer, db.ForeignKey('practitioners.id'), primary_key=True)
)

languages_patients = db.Table(
    'languages_patients',
    db.Column('language_id', db.Integer, db.ForeignKey('languages.id'), primary_key=True),
    db.Column('patient_id', db.Integer, db.ForeignKey('patients.id'), primary_key=True)
)

languages_interpreters = db.Table(
    'languages_interpreters',
    db.Column('language_id', db.Integer, db.ForeignKey('languages.id'), primary_key=True),
    db.Column('interpreter_id', db.Integer, db.ForeignKey('interpreters.id'), primary_key=True)
)


class Language(db.Model, FormatMixin):
    """Languages spoken by patients, practitioners, and interpreters."""
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    short_name: Mapped[str] = mapped_column(db.String, nullable=False, unique=True)
    full_name: Mapped[str] = mapped_column(db.String, nullable=False, unique=True)

    practitioners: Mapped[List["ClinikoPractitioner"]] = relationship(
        secondary=languages_practitioners,
        back_populates="languages"
    )

    patients: Mapped[List["Patient"]] = relationship(
        secondary=languages_patients,
        back_populates="languages"
    )

    interpreters: Mapped[List["Interpreter"]] = relationship(
        secondary=languages_interpreters,
        back_populates="languages"
    )

    appointments: Mapped[List["Appointment"]] = relationship("Appointment", backref="language")

    def __repr__(self) -> str:
        return f"<Language {self.short_name} ({self.full_name})>"
