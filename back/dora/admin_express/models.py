from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex

from dora.core.constants import WGS84

sentinel = object()


class GeoManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cache = {}


# Cache progressif pour les tables comportant de nombreuses géometries
class ManyGeoManager(GeoManager):
    def get_from_code(self, insee_code):
        value = self._cache.get(insee_code, sentinel)
        if value is not sentinel:
            return value

        try:
            value = self.defer("geom").get(code=insee_code)
        except self.model.DoesNotExist:
            value = None
        self._cache[insee_code] = value
        return value


# Cache instantané pour les tables comportant peu de géometries
# on fait la requête une fois pour toute
class FewGeoManager(GeoManager):
    def get_from_code(self, insee_code):
        if len(self._cache):
            return self._cache.get(insee_code)

        values = self.defer("geom").all()
        self._cache = {value.code: value for value in values}
        return self._cache.get(insee_code)


class AdminDivision(models.Model):
    code = models.CharField(max_length=9, primary_key=True)
    name = models.CharField(max_length=230)
    normalized_name = models.CharField(max_length=230)
    geom = models.MultiPolygonField(srid=WGS84, geography=True, spatial_index=True)

    class Meta:
        abstract = True


class CityManager(ManyGeoManager):
    pass


class City(AdminDivision):
    department = models.CharField(max_length=3, db_index=True)
    region = models.CharField(max_length=2, db_index=True)
    epci = models.CharField(max_length=20, db_index=True)
    epcis = ArrayField(
        models.CharField(max_length=9, primary_key=True),
        blank=True,
        default=list,
    )
    population = models.IntegerField()
    objects = CityManager()

    class Meta:
        indexes = [
            GinIndex(
                name="city_name_trgm_idx",
                fields=("normalized_name",),
                opclasses=("gin_trgm_ops",),
            )
        ]


class EPCIManager(ManyGeoManager):
    pass


class EPCI(AdminDivision):
    nature = models.CharField(max_length=150, db_index=True)
    departments = ArrayField(
        models.CharField(max_length=9, primary_key=True),
        blank=True,
        default=list,
    )
    regions = ArrayField(
        models.CharField(max_length=9, primary_key=True),
        blank=True,
        default=list,
    )
    objects = EPCIManager()

    class Meta:
        indexes = [
            GinIndex(
                name="epci_name_trgm_idx",
                fields=("normalized_name",),
                opclasses=("gin_trgm_ops",),
            )
        ]


class DepartmentManager(FewGeoManager):
    pass


class Department(AdminDivision):
    region = models.CharField(max_length=2, db_index=True)
    objects = DepartmentManager()

    class Meta:
        indexes = [
            GinIndex(
                name="department_name_trgm_idx",
                fields=("normalized_name",),
                opclasses=("gin_trgm_ops",),
            )
        ]


class RegionManager(FewGeoManager):
    pass


class Region(AdminDivision):
    objects = RegionManager()

    class Meta:
        indexes = [
            GinIndex(
                name="region_name_trgm_idx",
                fields=("normalized_name",),
                opclasses=("gin_trgm_ops",),
            )
        ]
