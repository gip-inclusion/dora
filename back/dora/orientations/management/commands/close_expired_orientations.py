from datetime import timedelta

from django.conf import settings
from django.core.management import BaseCommand
from django.db.models.functions import Coalesce
from django.utils import timezone

from dora.orientations.emails import send_orientation_expiration_emails
from dora.orientations.models import Orientation, OrientationStatus


class Command(BaseCommand):
    help = "Clôturer les orientations en attente après un délai"

    def handle(self, *args, **options):
        self.stdout.write(
            f"Clôture automatique des orientations en attente après {settings.ORIENTATION_EXPIRATION_PERIOD_DAYS} jours."
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

        orientations_closed = 0
        emails_sent = 0
        emails_attempted = 0

        for orientation in expired_orientations:
            effective_start_date = (
                orientation.processing_date or orientation.creation_date
            )

            orientation.set_status(OrientationStatus.EXPIRED)

            try:
                orientation.delete_attachments()
            except Exception as e:
                self.stderr.write(
                    f"Erreur lors de la suppression des pièces jointes pour l'orientation {orientation.id}: {e}"
                )

            email_cutoff_date = timezone.localdate() - timedelta(days=60)
            if orientation.creation_date.date() >= email_cutoff_date:
                emails_attempted += 1

                try:
                    send_orientation_expiration_emails(
                        orientation, effective_start_date
                    )
                    orientation.last_reminder_email_sent = timezone.now()
                    emails_sent += 1
                except Exception as e:
                    self.stderr.write(
                        f"Erreur lors de l'envoi de l'email pour l'orientation {orientation.id}: {e}"
                    )

            orientation.save()
            orientations_closed += 1

        self.stdout.write(f"{orientations_closed} orientations ont été clôturées.")
        self.stdout.write(
            f"{emails_sent} mails envoyés avec succès sur un total de {emails_attempted}."
        )
