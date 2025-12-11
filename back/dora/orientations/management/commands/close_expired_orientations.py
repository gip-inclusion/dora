from datetime import timedelta

from django.conf import settings
from django.core.management import BaseCommand
from django.db import transaction
from django.db.models.functions import Coalesce
from django.utils import timezone

from dora.orientations.emails import send_orientation_expiration_emails
from dora.orientations.models import Orientation, OrientationStatus


class Command(BaseCommand):
    help = "Clôturer les orientations qui sont en cours sans réponse après un délai"

    def handle(self, *args, **options):
        self.stdout.write(
            f"Clôture des orientations qui sont en cours sans réponse après {settings.ORIENTATION_EXPIRATION_PERIOD_DAYS} jours."
        )

        expiration_date = timezone.localdate() - timedelta(
            days=settings.ORIENTATION_EXPIRATION_PERIOD_DAYS
        )

        expired_orientations = (
            Orientation.objects.alias(
                effective_start_date=Coalesce("processing_date", "creation_date")
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

                    self.stdout.write(f"L'orientation {orientation.id} a été clôturée.")

                    transaction.on_commit(
                        lambda: self.send_mail(orientation, effective_start_date)
                    )

            except Exception as e:
                self.stderr.write(
                    f"Erreur lors de la clôture de l'orientation {orientation.id}: {e}"
                )

        self.stdout.write(
            f"{len(expired_orientations)} orientations ont été clôturées."
        )

    def send_mail(self, orientation: Orientation, start_date: str) -> None:
        email_cutoff_date = timezone.localdate() - timedelta(days=60)

        if orientation.creation_date.date() >= email_cutoff_date:
            send_orientation_expiration_emails(orientation, start_date)
            self.stdout.write(
                f"Des mails ont été envoyés pour l'orientation {orientation.id}."
            )
