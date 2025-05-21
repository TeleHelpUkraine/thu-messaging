from typing import List
from sqlalchemy import event
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..extensions.database import db
from ..mixins import CRUDMixin, FormatMixin  # <- assuming you have these

# Association table for many-to-many with patients
genders_patients = db.Table(
    'genders_patients',
    db.Column('gender_id', db.Integer, db.ForeignKey('genders.id'), primary_key=True),
    db.Column('patient_id', db.Integer, db.ForeignKey('patients.id'), primary_key=True)
)

class Gender(db.Model, CRUDMixin, FormatMixin):
    """Gender options for patients (e.g., Female, Male, Other)"""
    __tablename__ = "genders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    gender: Mapped[str] = mapped_column(db.String, nullable=True, default=None)

    patients: Mapped[List["Patient"]] = relationship(
        secondary=genders_patients,
        back_populates="genders"
    )

    def __repr__(self):
        return f"<Gender id={self.id}, gender={self.gender}>"

# Automatically insert default values on table creation
@event.listens_for(Gender.__table__, "after_create")
def insert_default_genders(target, connection, **kw):
    default_genders = ['Female', 'Male', 'Other']
    connection.execute(
        target.insert(),
        [{"gender": g} for g in default_genders]
    )
