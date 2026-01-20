from django.contrib.gis.db import models as gis_models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.db import models

from dora.core.constants import WGS84


class City(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=5, unique=True)
    department = models.CharField(max_length=3, db_index=True)
    epci = models.CharField(max_length=9, db_index=True)
    region = models.CharField(max_length=3, db_index=True)
    postal_codes = ArrayField(
        models.CharField(max_length=5),
        blank=True,
        default=list,
    )
    population = models.IntegerField(default=0)
    center = gis_models.PointField(srid=WGS84, geography=True, null=True, blank=True)
    normalized_name = models.CharField(max_length=255, blank=True, default="")

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

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"


class Department(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=3, unique=True)
    region = models.CharField(max_length=3, db_index=True)
    normalized_name = models.CharField(max_length=255, blank=True, default="")

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

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"


class EPCI(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=9, unique=True)
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
    normalized_name = models.CharField(max_length=255, blank=True, default="")

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

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"


class Region(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=3, unique=True)
    normalized_name = models.CharField(max_length=255, blank=True, default="")

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

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"
