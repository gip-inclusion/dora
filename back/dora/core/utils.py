from dataclasses import dataclass
from furl import furl
import logging
import json
import re
import requests
from typing import Tuple

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.text import Truncator
from django.contrib.gis.geos import Point
from dora.core.constants import WGS84
from django.contrib.gis.geos import Point

logger = logging.getLogger(__name__)

TRUTHY_VALUES = ("1", 1, "True", "true", "t", "T", True)
FALSY_VALUES = ("0", 0, "False", "false", "f", "F", False)


def normalize_description(desc: str, limit: int) -> Tuple[str, str]:
    if len(desc) < limit:
        return desc, ""
    else:
        return Truncator(desc).chars(limit), desc


def normalize_phone_number(phone: str) -> str:
    if not phone:
        return phone
    has_intl_prefix = phone.strip().startswith("+")
    phone = "".join([c for c in phone if c.isdigit()])
    if has_intl_prefix:
        phone = re.sub("^330", "0", phone)
        phone = re.sub("^33", "0", phone)

    return phone[:10]


def code_insee_to_code_dept(code_insee):
    return code_insee[:3] if code_insee.startswith("97") else code_insee[:2]


def get_object_or_none(klass, *args, **kwargs):
    """
    Use get() to return an object, or return None if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
    one object is found.
    """
    try:
        return get_object_or_404(klass, *args, **kwargs)
    except Http404:
        return None


@dataclass
class GeoData:
    address: str
    city: str
    postal_code: str
    city_code: str
    geom: Point

    def __str__(self):
        return f"GeoData({self.address}, {self.postal_code} {self.city} (INSEE : {self.city_code}))"


def get_geo_data(address, city=None, postal_code=None, city_code=None):
    url = furl("https://api-adresse.data.gouv.fr").add(
        path="/search/",
        args={
            "q": " ".join(filter(None, [address, city])),
            "postcode": postal_code,
            "citycode": city_code,
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
        logger.error(f"Erreur dans la récupération des données: {response.content}")
        return None

    result = json.loads(response.content)
    if result["features"]:
        feat = result["features"][0]
        if feat["properties"]["score"] > 0.5:
            coords = feat["geometry"]["coordinates"]
            return GeoData(
                address=feat["properties"]["name"],
                city=feat["properties"]["city"],
                postal_code=feat["properties"]["postcode"],
                city_code=feat["properties"]["citycode"],
                geom=Point(coords[0], coords[1], srid=WGS84),
            )
        else:
            logger.error("Résultat incertain")
            return None
    else:
        logger.error("Aucun résultat trouvé")
        return None
