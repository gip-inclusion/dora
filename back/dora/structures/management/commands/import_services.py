from django.core.management.base import BaseCommand

from scripts.import_services import import_services


class Command(BaseCommand):
    help = "Créer des nouveaux services basés sur des modèles pour des structures en utilisant des infos fournies par un CSV"

    def handle(self, *args, **kwargs):
        import_services()
