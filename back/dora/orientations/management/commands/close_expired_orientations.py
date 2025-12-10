from datetime import timedelta

from django.conf import settings
from django.core.management import BaseCommand
from django.db.models import BooleanField, Case, Q, Value, When
from django.utils import timezone

from dora.orientations.emails import send_orientation_expiration_emails
from dora.orientations.models import Orientation, OrientationStatus


class Command(BaseCommand):
    help = "Clôturer les orientations en attente après un délai"

    def handle(self, *args, **options):
        self.stdout.write(
            f"Clôture automatique des orientations en attente après {settings.ORIENTATION_EXPIRATION_PERIOD_DAYS} jours."
        )

        expiration_date = timezone.now() - timedelta(
            days=settings.ORIENTATION_EXPIRATION_PERIOD_DAYS
        )
        email_cutoff_date = timezone.now() - timedelta(days=60)

        expired_orientations = (
            Orientation.objects.filter(
                Q(
                    processing_date__isnull=True,
                    creation_date__lte=expiration_date,
                )
                | Q(
                    processing_date__lte=expiration_date,
                ),
                status=OrientationStatus.PENDING,
            )
            .annotate(
                should_send_email=Case(
                    When(creation_date__gte=email_cutoff_date, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                )
            )
            .select_related("service")
        )

        orientations_closed = 0
        emails_sent = 0
        emails_attempted = 0

        for orientation in expired_orientations:
            start_date = (
                orientation.processing_date
                if orientation.processing_date
                else orientation.creation_date
            )

            orientation.status = OrientationStatus.EXPIRED
            orientation.processing_date = timezone.now()

            try:
                orientation.delete_attachments()
            except Exception as e:
                self.stderr.write(
                    f"Erreur lors de la suppression des pièces jointes pour l'orientation {orientation.id}: {e}"
                )

            if orientation.should_send_email:
                emails_attempted += 1
                try:
                    send_orientation_expiration_emails(orientation, start_date)
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
