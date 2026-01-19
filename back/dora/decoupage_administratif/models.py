from django.contrib.postgres.fields import ArrayField
from django.db import models


class Commune(models.Model):
    nom = models.CharField(max_length=255)
    code = models.CharField(max_length=5, unique=True)
    code_departement = models.CharField(max_length=3)
    code_epci = models.CharField(max_length=9)
    code_region = models.CharField(max_length=3)
    codes_postaux = ArrayField(
        models.CharField(max_length=5),
        blank=True,
        default=list,
    )

    class Meta:
        verbose_name = "commune"
        verbose_name_plural = "communes"

    def __str__(self) -> str:
        return f"{self.nom} ({self.code})"


class Departement(models.Model):
    nom = models.CharField(max_length=255)
    code = models.CharField(max_length=3, unique=True)
    code_region = models.CharField(max_length=3)

    class Meta:
        verbose_name = "département"
        verbose_name_plural = "départements"

    def __str__(self) -> str:
        return f"{self.nom} ({self.code})"


class Epci(models.Model):
    nom = models.CharField(max_length=255)
    code = models.CharField(max_length=9, unique=True)
    codes_departements = ArrayField(
        models.CharField(max_length=3),
        blank=True,
        default=list,
    )
    codes_regions = ArrayField(
        models.CharField(max_length=3),
        blank=True,
        default=list,
    )

    class Meta:
        verbose_name = "EPCI"
        verbose_name_plural = "EPCI"

    def __str__(self) -> str:
        return f"{self.nom} ({self.code})"


class Region(models.Model):
    nom = models.CharField(max_length=255)
    code = models.CharField(max_length=3, unique=True)

    class Meta:
        verbose_name = "région"
        verbose_name_plural = "régions"

    def __str__(self) -> str:
        return f"{self.nom} ({self.code})"
