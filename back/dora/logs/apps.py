from django.apps import AppConfig


class LogsConfig(AppConfig):
    name = "dora.logs"
    verbose_name = "logs"

    def ready(self):
        super().ready()
        # force la définition du logger 'dora.logs.core'
        import dora.logs.core  # noqa
