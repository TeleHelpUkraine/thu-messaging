import sys
import logging
from sqlalchemy.exc import SQLAlchemyError
from ..extensions.database import db

class CRUDMixin:
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            db.session.refresh(self)
            return self
        except (BaseException, SQLAlchemyError) as error:
            db.session.rollback()
            logging.error(f"ERROR ON INSERT {error}, SELF: {self.__dict__}, sys.exc_info(): {sys.exc_info()}")
            return None

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            logging.info(f"Instance deleted: {self}")
        except BaseException:
            db.session.rollback()
            logging.error(sys.exc_info())

    def update(self):
        try:
            db.session.commit()
            db.session.refresh(self)
            logging.info(f"Updated {self.__class__.__name__}")
            return self
        except (Exception, SQLAlchemyError, TypeError, ValueError, KeyError) as error:
            db.session.rollback()
            logging.error(f"ERROR IN UPDATE: {error}, {sys.exc_info()}, SELF {self}")

    def dict_update(self, kwargs, commit=True):
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                else:
                    logging.error(f"No attr {key} in self.")
            if commit:
                db.session.commit()
            db.session.refresh(self)
            return self
        except (BaseException, SQLAlchemyError, AttributeError, ValueError) as error:
            logging.error(f"ERROR IN DICT UPDATE {error}")
            db.session.rollback()
            return error

    def appt_update(self, kwargs):
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    if key not in ['information', 'canceled', 'cancellation_reason_id']:
                        setattr(self, key, value)
                    if key == 'information' and value not in self.__dict__["information"]:
                        new_value = self.__dict__["information"] + " " + value
                        setattr(self, key, new_value)
                    if 'cancel' in key and not self.__dict__[key]:
                        setattr(self, key, value)
                else:
                    logging.info(f"NO ATTRIBUTE {key} IN {self.__class__.__name__}")
                db.session.commit()
                db.session.refresh(self)
            logging.info(f"APPT UPDATE {self.format()}")
            return self
        except (BaseException, SQLAlchemyError, AttributeError, ValueError) as error:
            logging.error(f"ERROR IN APPT UPDATE {error}")
            db.session.rollback()
