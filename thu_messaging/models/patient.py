from zoneinfo import ZoneInfo
from ..extensions.database import db
import sys
import logging
import pytz
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DatabaseError
import hashlib
import uuid
from babel.dates import format_datetime
from .language import languages_patients
from .gender import genders_patients
from sqlalchemy.orm import Mapped
from typing import List
from ..mixins import CRUDMixin, FormatMixin


class Patient(db.Model, CRUDMixin, FormatMixin):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    year_of_birth = db.Column(db.Integer, nullable=True, default=None)
    first_name = db.Column(db.String(), nullable=True)
    last_name = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    phone = db.Column(db.String(), nullable=True)
    tz = db.Column(db.String(), nullable=False)
    notes = db.Column(db.String(), nullable=True)
    cliniko_medical_id = db.Column(db.BigInteger, nullable=True, unique=True)
    cliniko_mental_id = db.Column(db.BigInteger, nullable=True, unique=True)
    first_language = db.Column(db.String(), nullable=False)
    second_language = db.Column(db.String(), nullable=True)
    auth0_id = db.Column(db.String())
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=datetime.now()
    )

    appointments = db.relationship(
        "Appointment",
        backref="patient"
    )
    attachments = db.relationship(
        "PatientAttachment",
        lazy="dynamic",
        backref="patient"
    )

    treatment_notes = db.relationship(
        "TreatmentNote",
        lazy="dynamic",
        backref="patient"
    )

    first_lang_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'languages.id'
        )
    )

    second_lang_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'languages.id'
        )
    )

    languages: Mapped[List["Language"]] = db.relationship(
        secondary=languages_patients,
        back_populates="patients" # Parent = Language
    )

    gender_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'genders.id'
        )
    )

    genders: Mapped[List["Gender"]] = db.relationship(
        secondary=genders_patients,
        back_populates="patients" # Parent = Language
    )


    def format(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "tz": self.tz,
            "notes": self.notes,
            "cliniko_medical_id": self.cliniko_medical_id,
            "cliniko_mental_id": self.cliniko_mental_id,
            "year_of_birth": self.year_of_birth,
            "first_language": self.first_language,
            "second_language": self.second_language,
            "auth0_id": self.auth0_id,
            "created_at": format_datetime(self.created_at.astimezone(ZoneInfo("US/Pacific")), format="long", locale='en_US'),
            "appointments_ids": [a.id for a in self.appointments],
            "attachments_ids":  [a.id for a in self.attachments],
            "gender_id": self.gender_id
        }

    def uuid(self) -> str:
        m = hashlib.md5()
        m.update(str(self.id).encode('utf-8'))
        id = uuid.UUID(m.hexdigest())
        return str(id)


# A dict of tables to be used in recovering personal info route with variables:
# interpreters and patients
tables_dict = {
    table.__tablename__: table for table in db.Model.__subclasses__()}


def table_object(table_name):
    return tables_dict.get(table_name)