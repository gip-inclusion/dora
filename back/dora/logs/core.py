import logging

from django_datadog_logger.formatters import datadog

from .models import ActionLog


class RedactUserInformationDataDogJSONFormatter(datadog.DataDogJSONFormatter):
    def json_record(self, message, extra, record):
        log_entry_dict = super().json_record(message, extra, record)
        for log_key in {"usr.name", "usr.email", "usr.session_key"}:
            if log_key in log_entry_dict:
                del log_entry_dict[log_key]
        return log_entry_dict


class ActionLogHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        # voir : https://docs.python.org/3/library/logging.html#logrecord-attributes
        payload = {}
        if record.args and isinstance(record.args, dict):
            payload |= record.args
        ActionLog(level=record.levelno, msg=record.msg, payload=payload).save()


# ne pas s'amuser à instancier un logger pour les actions, plutôt utiliser :
# logging.getLogger("dora.logs.core")
# (ce logger est initialisé à la création de l'app Django)
logging.getLogger(__name__).addHandler(ActionLogHandler())
