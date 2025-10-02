import logging

from .models import ActionLog


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
