from django.contrib.gis.db import models as gis_models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.db import models

from dora.core.constants import WGS84

sentinel = object()


class GeoManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cache = {}


# Cache progressif pour les tables comportant de nombreuses entités
class ManyGeoManager(GeoManager):
    def get_from_code(self, code):
        value = self._cache.get(code, sentinel)
        if value is not sentinel:
            return value

        try:
            value = self.get(code=code)
        except self.model.DoesNotExist:
            value = None
        self._cache[code] = value
        return value


# Cache instantané pour les tables comportant peu d'entités
# on fait la requête une fois pour toute
class FewGeoManager(GeoManager):
    def get_from_code(self, code):
        if len(self._cache):
            return self._cache.get(code)

        values = self.all()
        self._cache = {value.code: value for value in values}
        return self._cache.get(code)


class AdminDivision(models.Model):
    """Classe abstraite pour les divisions administratives sans géométrie."""

    name = models.CharField(max_length=255)
    normalized_name = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"


class CityManager(ManyGeoManager):
    pass


class City(AdminDivision):
    code = models.CharField(max_length=5, primary_key=True)
    department = models.CharField(max_length=3, db_index=True)
    epci = models.CharField(max_length=9, db_index=True)
    region = models.CharField(max_length=3, db_index=True)
    postal_codes = ArrayField(
        models.CharField(max_length=5),
        blank=True,
        default=list,
    )
    population = models.IntegerField(default=0)
    center = gis_models.PointField(srid=WGS84, geography=True)
    objects = CityManager()

    class Meta:
        verbose_name = "commune"
        verbose_name_plural = "communes"
        indexes = [
            GinIndex(
                name="da_city_name_trgm_idx",
                fields=("normalized_name",),
                opclasses=("gin_trgm_ops",),
            )
        ]


class DepartmentManager(FewGeoManager):
    pass


class Department(AdminDivision):
    code = models.CharField(max_length=3, primary_key=True)
    region = models.CharField(max_length=3, db_index=True)
    objects = DepartmentManager()

    class Meta:
        verbose_name = "département"
        verbose_name_plural = "départements"
        indexes = [
            GinIndex(
                name="da_dept_name_trgm_idx",
                fields=("normalized_name",),
                opclasses=("gin_trgm_ops",),
            )
        ]


class EPCIManager(ManyGeoManager):
    pass


class EPCI(AdminDivision):
    code = models.CharField(max_length=9, primary_key=True)
    departments = ArrayField(
        models.CharField(max_length=3),
        blank=True,
        default=list,
    )
    regions = ArrayField(
        models.CharField(max_length=3),
        blank=True,
        default=list,
    )
    objects = EPCIManager()

    class Meta:
        verbose_name = "EPCI"
        verbose_name_plural = "EPCI"
        indexes = [
            GinIndex(
                name="da_epci_name_trgm_idx",
                fields=("normalized_name",),
                opclasses=("gin_trgm_ops",),
            )
        ]


class RegionManager(FewGeoManager):
    pass


class Region(AdminDivision):
    code = models.CharField(max_length=3, primary_key=True)
    objects = RegionManager()

    class Meta:
        verbose_name = "région"
        verbose_name_plural = "régions"
        indexes = [
            GinIndex(
                name="da_region_name_trgm_idx",
                fields=("normalized_name",),
                opclasses=("gin_trgm_ops",),
            )
        ]
