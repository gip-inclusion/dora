from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from dora.core.commands import BaseCommand
from dora.orientations.models import Orientation, OrientationStatus


class Command(BaseCommand):
    help = (
        "Supprime les pièces jointes des orientations terminées (acceptées, rejetées, expirées) "
        "après un certain délai"
    )

    def handle(self, *args, **options):
        self.logger.info(
            "Suppression des pièces jointes des orientations terminées il y a plus de %d mois.",
            settings.ORIENTATION_ATTACHMENTS_EXPIRATION_PERIOD_MONTHS,
        )

        expiration_date = timezone.localdate() - relativedelta(
            months=settings.ORIENTATION_ATTACHMENTS_EXPIRATION_PERIOD_MONTHS
        )

        orientations = Orientation.objects.filter(
            processing_date__lte=expiration_date,
            status__in=[
                OrientationStatus.ACCEPTED,
                OrientationStatus.MODERATION_REJECTED,
                OrientationStatus.REJECTED,
                OrientationStatus.EXPIRED,
            ],
        )

        for orientation in orientations:
            try:
                with transaction.atomic():
                    orientation.delete_attachments()

                    self.logger.info(
                        "Les pièces jointes de l'orientation %s ont été supprimées.",
                        orientation.pk,
                    )

            except Exception as e:
                self.logger.warning(
                    "Erreur lors de la suppression des pièces jointes de l'orientation %s: %s",
                    orientation.pk,
                    e,
                )

        self.logger.info(
            "%d orientations terminées il y a plus de %d mois ont vu leurs pièces jointes supprimées.",
            len(orientations),
            settings.ORIENTATION_ATTACHMENTS_EXPIRATION_PERIOD_MONTHS,
        )
