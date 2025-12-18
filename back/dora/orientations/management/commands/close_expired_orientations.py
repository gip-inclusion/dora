import functools
from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.db.models.functions import Coalesce
from django.utils import timezone

from dora.core.commands import BaseCommand
from dora.orientations.emails import send_orientation_expiration_emails
from dora.orientations.models import Orientation, OrientationStatus


class Command(BaseCommand):
    help = "Clôturer les orientations qui sont en cours sans réponse après un délai"

    def handle(self, *args, **options):
        self.logger.info(
            "Clôture des orientations qui sont en cours sans réponse après %d jours.",
            settings.ORIENTATION_EXPIRATION_PERIOD_DAYS,
        )

        expiration_date = timezone.localdate() - timedelta(
            days=settings.ORIENTATION_EXPIRATION_PERIOD_DAYS
        )

        expired_orientations = (
            Orientation.objects.alias(
                effective_start_date=Coalesce(
                    "processing_date__date", "creation_date__date"
                )
            )
            .filter(
                effective_start_date__lte=expiration_date,
                status=OrientationStatus.PENDING,
            )
            .select_related("service")
        )

        for orientation in expired_orientations:
            try:
                with transaction.atomic():
                    effective_start_date = (
                        orientation.processing_date or orientation.creation_date
                    )

                    orientation.set_status(OrientationStatus.EXPIRED)

                    self.logger.info("L'orientation %s a été clôturée.", orientation.pk)

                    transaction.on_commit(
                        functools.partial(
                            self.send_email_notifications,
                            orientation,
                            effective_start_date,
                        )
                    )

            except Exception as e:
                self.logger.warning(
                    "Erreur lors de la clôture de l'orientation %s: %s",
                    orientation.id,
                    e,
                )

        self.logger.info(
            "%d orientations ont été clôturées.", len(expired_orientations)
        )

    def send_email_notifications(
        self, orientation: Orientation, start_date: str
    ) -> None:
        if settings.ORIENTATION_EXPIRATION_EMAILS_ENABLED:
            send_orientation_expiration_emails(orientation, start_date)
            self.logger.info(
                "Des mails ont été envoyés pour l'orientation %s.", orientation.id
            )
