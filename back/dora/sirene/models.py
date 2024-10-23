from django.contrib.postgres.indexes import GinIndex
from django.db import models


class Establishment(models.Model):
    siret = models.CharField(verbose_name="Siret", max_length=14, primary_key=True)
    siren = models.CharField(verbose_name="Siren", max_length=9, db_index=True)
    name = models.CharField(verbose_name="Nom", max_length=255, db_index=True)
    parent_name = models.CharField(
        verbose_name="Nom de l’unité légale", max_length=255, db_index=True
    )

    ape = models.CharField(
        max_length=6,
    )
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    city_code = models.CharField(max_length=5, db_index=True)
    postal_code = models.CharField(max_length=5)
    is_siege = models.BooleanField(db_index=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    full_search_text = models.TextField(help_text="Renseigner NOM + NOM UNITÉ LÉGALE")

    class Meta:
        indexes = [
            # https://www.postgresql.org/docs/current/pgtrgm.html#id-1.11.7.40.8
            GinIndex(
                name="full_text_trgm_idx",
                fields=("full_search_text",),
                opclasses=("gin_trgm_ops",),
            )
        ]
        verbose_name = "Établissement"

    def __str__(self):
        return f"{self.name} ({self.siret})"
