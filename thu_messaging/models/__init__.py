from .patient import Patient
from .appointment import Appointment
from .message import Message
from .practitioner import ClinikoPractitioner
from .interpreter import Interpreter
from .language import Language
from .treatment_note import TreatmentNote
from .patient_attachment import PatientAttachment
from .gender import Gender
from .cliniko_account import ClinikoAccount
from .cliniko_appointment_type import ClinikoAppointmentType
from .cancellation_reason import CancellationReason
from .availability_interpreter import InterpreterTimes
from .availability_practitioner import PractitionerAvailability
from ..extensions.database import db

tables_dict = {
    table.__tablename__: table for table in db.Model.__subclasses__()
}

def table_object(table_name):
    return tables_dict.get(table_name)