from django.contrib.postgres.fields import ArrayField
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=5, unique=True)
    department = models.CharField(max_length=3)
    epci = models.CharField(max_length=9)
    region = models.CharField(max_length=3)
    postal_codes = ArrayField(
        models.CharField(max_length=5),
        blank=True,
        default=list,
    )

    class Meta:
        verbose_name = "commune"
        verbose_name_plural = "communes"

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"


class Department(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=3, unique=True)
    region = models.CharField(max_length=3)

    class Meta:
        verbose_name = "département"
        verbose_name_plural = "départements"

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

    class Meta:
        verbose_name = "EPCI"
        verbose_name_plural = "EPCI"

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"


class Region(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=3, unique=True)

    class Meta:
        verbose_name = "région"
        verbose_name_plural = "régions"

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"
