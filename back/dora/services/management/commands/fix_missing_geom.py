
from django.core.management.base import BaseCommand

from dora.services.models import Service
from dora.services.utils import update_geom


class Command(BaseCommand):
    def handle(self, *args, **options):
        services_w_missing_geo = Service.objects.filter(
            location_kinds__value="en-presentiel", geom=None
        ).exclude(city_code="", address1="")
        self.stdout.write(
            self.style.NOTICE(
                f"{services_w_missing_geo.count()} services sans géométrie"
            )
        )
        total = services_w_missing_geo.count()
        for i, s in enumerate(services_w_missing_geo):
            self.stdout.write(f"{i}/{total}")
            self.fix_geo(s)

    def fix_geo(self, s):
        assert s.geom is None
        update_geom(s)
