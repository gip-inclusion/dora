from django.apps import AppConfig


class ServicesConfig(AppConfig):
    name = "dora.services"
    verbose_name = "Services"

    def ready(self):
        super().ready()

        from . import signals_publics  # noqa: F401
