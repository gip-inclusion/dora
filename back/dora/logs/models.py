import logging
import pprint
import uuid

import django.db.models as models
from django.contrib.postgres.indexes import BrinIndex
from django.core.exceptions import ValidationError


class ActionLog(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name="identifiant"
    )

    created_at = models.DateTimeField(
        auto_now=True, editable=False, verbose_name="date de création"
    )

    level = models.SmallIntegerField(
        null=False,
        blank=True,
        verbose_name="niveau de log",
        editable=False,
        choices=logging._levelToName.items(),
    )

    msg = models.TextField(null=False, blank=True, verbose_name="message")

    # un des futurs besoins de ce log sera de tracker les points avec une thématique légale,
    # style AIPD, RGPD ou action sensibles sur les données.
    # on pourra adjoindre plus de détails dans le payload.
    legal = models.BooleanField(
        null=False,
        default=False,
        blank=True,
        verbose_name="implications légales (RGPD, AIPD..)",
    )

    payload = models.JSONField(
        default=dict,
        null=False,
        blank=True,
        verbose_name="contenu supplémentaire (JSON)",
    )

    # note :
    # pour l'instant, pas d'implémentation de recherche sur le contenu du message du log.
    # le système actuel se veut simple et ne nécessitera pas forcément une recherche "fulltext".
    # si le cas se présente :
    # - ajouter un champ de type `SearchVectorField` par ex.
    # - indexer le champ `msg` (GIN)

    class Meta:
        verbose_name = "historique des actions"
        verbose_name_plural = "historique des actions"
        indexes = (
            BrinIndex(
                fields=("created_at",),
                name="idx_%(app_label)s_%(class)s_created_at",
                autosummarize=True,
            ),
            models.Index(fields=("level",)),
            models.Index(fields=("legal",)),
        )

    def __repr__(self):
        return pprint.pformat(
            {
                "_id": str(self.pk),
                "_createdAt": str(self.created_at),
                "_level": self.level_name,
                "_msg": self.msg,
                "_legal": self.legal,
            }
            | self.payload
        )

    def __str__(self):
        return f"{str(self.pk)} - {self.level_name}"

    def clean(self):
        # le champ `legal` peut être inclus dans le payload
        # pour être directement créé par le logger,
        # mais il doit être un booléen
        if isinstance(self.payload, dict):
            if legal := self.payload.get("legal"):
                if not isinstance(legal, bool):
                    raise ValidationError(
                        "Le champ JSON 'legal' doit être un booléen", code="legal"
                    )
                self.legal = legal
                del self.payload["legal"]

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def level_name(self):
        return logging._levelToName[self.level]
