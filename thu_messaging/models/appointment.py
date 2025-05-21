from ..extensions.database import db
from ..mixins import CRUDMixin, FormatMixin
from zoneinfo import ZoneInfo


class Appointment(db.Model, CRUDMixin, FormatMixin):
    """Appointments table from Cliniko appointments"""
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    datetime = db.Column(db.DateTime(timezone=True))

    interpreter_id = db.Column(
        db.Integer,
        db.ForeignKey("interpreters.id", ondelete='CASCADE', onupdate="CASCADE"),
        nullable=True
    )

    information = db.Column(db.String(), nullable=True)

    cliniko_appointment_id = db.Column(db.BigInteger, nullable=False, primary_key=True, unique=True)

    cliniko_practitioner_id = db.Column(
        db.BigInteger,
        db.ForeignKey('practitioners.cliniko_practitioner_id', ondelete='CASCADE', onupdate="CASCADE")
    )

    patient_id = db.Column(
        db.BigInteger,
        db.ForeignKey('patients.id', ondelete='CASCADE', onupdate="CASCADE")
    )

    cliniko_account_id = db.Column(
        db.Integer,
        db.ForeignKey("cliniko_accounts.id", ondelete='CASCADE', onupdate="CASCADE"),
        nullable=False,
        primary_key=True
    )

    cliniko_appointment_type_id = db.Column(
        db.BigInteger,
        db.ForeignKey("cliniko_appointment_types.cliniko_appointment_type_id", ondelete='CASCADE', onupdate="CASCADE")
    )

    language_id = db.Column(
        db.Integer,
        db.ForeignKey('languages.id')
    )

    interpreter_availability_id = db.Column(
        db.BigInteger,
        db.ForeignKey("availability.id", ondelete='CASCADE', onupdate="CASCADE"),
        nullable=True
    )

    practitioner_availability_id = db.Column(
        db.BigInteger,
        db.ForeignKey("practitioners_availability.id", ondelete='CASCADE', onupdate="CASCADE"),
        nullable=True
    )

    appointment_status = db.relationship("AppointmentStatus")

    cancellation_reason_id = db.Column(
        db.Integer,
        db.ForeignKey('cancellation_reasons.id', ondelete='CASCADE', onupdate="CASCADE"),
        nullable=True
    )

    created_at = db.Column(db.DateTime(timezone=True))
    booked = db.Column(db.Boolean, nullable=True)
    canceled = db.Column(db.Boolean)
    missed = db.Column(db.Boolean)
    completed = db.Column(db.Boolean)

    patient_attachments = db.relationship("PatientAttachment", backref='attachments')

    add_interpreter = db.Column(db.Boolean)

    def __init__(
        self,
        datetime,
        interpreter_id,
        cliniko_appointment_id,
        cliniko_practitioner_id,
        cliniko_account_id,
        interpreter_availability_id,
        practitioner_availability_id,
        cliniko_appointment_type_id,
        patient_id,
        information,
        cancellation_reason_id,
        booked,
        canceled,
        missed,
        completed,
        language_id,
        created_at=None,
        add_interpreter=False
    ):
        self.datetime = datetime
        self.interpreter_id = interpreter_id
        self.cliniko_appointment_id = cliniko_appointment_id
        self.cliniko_practitioner_id = cliniko_practitioner_id
        self.cliniko_account_id = cliniko_account_id
        self.interpreter_availability_id = interpreter_availability_id
        self.practitioner_availability_id = practitioner_availability_id
        self.cliniko_appointment_type_id = cliniko_appointment_type_id
        self.patient_id = patient_id
        self.information = information
        self.cancellation_reason_id = cancellation_reason_id
        self.booked = booked
        self.canceled = canceled
        self.missed = missed
        self.completed = completed
        self.language_id = language_id
        self.created_at = created_at or datetime.now(tz=ZoneInfo("UTC"))
        self.add_interpreter = add_interpreter
