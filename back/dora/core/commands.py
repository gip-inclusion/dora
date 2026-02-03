from django.core import management
from itoutils.django.commands import LoggedCommandMixin


class BaseCommand(LoggedCommandMixin, management.BaseCommand):
    def handle(self, *args, **options):
        raise NotImplementedError()
