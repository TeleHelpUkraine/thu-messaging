from datetime import datetime
from zoneinfo import ZoneInfo
import logging

class FormatMixin:
    def format_service_name(self, language):
        if len(self.__dict__.get("name", "").split("|")) > 1:
            self.__dict__["name"] = (
                self.__dict__["name"].split("|")[0]
                if language == 'en'
                else self.__dict__["name"].split("|")[1]
            )
        return self

    def format_attachment(self) -> dict:
        dict_self = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, str) and len(value) > 30:
                    value = value[0:30] + "\t" + value[30:50]
                dict_self[key] = value
        return dict_self

    def format(self) -> dict:
        dict_self = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                try:
                    if isinstance(value, datetime):
                        value = value.isoformat()
                    dict_self[key] = value
                except Exception as error:
                    logging.error(f"ERROR IN FORMAT {error}")
        return dict_self

    def admin_format(self) -> dict:
        dict_self = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, datetime):
                    dict_self[key] = value.astimezone(ZoneInfo("US/Pacific")).strftime("%m/%d/%Y, %H:%M:%S %Z")
                else:
                    dict_self[key] = value
        return dict_self

    def __str__(self) -> str:
        return " ".join(f"{key}:{value}" for key, value in self.__dict__.items() if not key.startswith('_'))

    def __repr__(self) -> str:
        return "REPR: " + self.__class__.__name__ + ": " + ". ".join(
            str(value) for key, value in self.__dict__.items() if not key.startswith('_')
        )
