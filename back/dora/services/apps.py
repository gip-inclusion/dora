from django.apps import AppConfig


class ServicesConfig(AppConfig):
    name = "dora.services"
    verbose_name = "Services"

    def ready(self):
        # Connecte les gestionnaires de signaux de double écriture des publics (import pour effet de bord).
        from . import signals  # noqa: F401
