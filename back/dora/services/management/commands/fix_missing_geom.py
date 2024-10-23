import json

import requests
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from furl import furl

from dora.core.constants import WGS84
from dora.services.models import Service


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
        url = furl("https://api-adresse.data.gouv.fr").add(
            path="/search/",
            args={
                "q": s.address1,
                "citycode": s.city_code,
                "autocomplete": 0,
                "limit": 1,
            },
        )
        response = requests.get(
            url,
            params={},
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        if response.status_code != 200:
            self.stderr.write(
                self.style.ERROR(
                    f"Erreur dans la récupération des données: {response.content}"
                )
            )
            return

        result = json.loads(response.content)
        if result["features"]:
            feat = result["features"][0]
            if feat["properties"]["score"] > 0.5:
                coords = feat["geometry"]["coordinates"]
                s.geom = Point(coords[0], coords[1], srid=WGS84)
                s.save(update_fields=["geom"])
            else:
                self.stderr.write(self.style.ERROR(("Résultat incertain")))
