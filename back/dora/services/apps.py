from django.apps import AppConfig


class ServicesConfig(AppConfig):
    name = "dora.services"
    verbose_name = "services"

    def ready(self):
        super().ready()
        # connecte la double écriture `kinds` → `kind` (import pour effet de bord)
        import dora.services.signals  # noqa
