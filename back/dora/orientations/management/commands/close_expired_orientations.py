from datetime import timedelta

from django.conf import settings
from django.core.management import BaseCommand
from django.db.models import Q
from django.utils import timezone

from dora.orientations.emails import send_orientation_expiration_emails
from dora.orientations.models import Orientation, OrientationStatus


class Command(BaseCommand):
    help = "Clôturer les orientations qui sont en cours  qui sont plus valables"

    def handle(self, *args, **options):
        self.stdout.write(
            f"Clôture automatique des orientations en cours qui ne sont plus valables après {settings.ORIENTATION_EXPIRATION_PERIOD_DAYS} jours."
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
                should_send_email=Q(
                    processing_date__isnull=True, creation_date__gte=email_cutoff_date
                )
                | Q(processing_date__gte=email_cutoff_date)
            )
            .select_related("service")
        )

        orientations_to_update = []

        for orientation in expired_orientations:
            orientation.status = OrientationStatus.EXPIRED

            # bulk_update n'invoque pas save() donc il faut mettre à jour le processing_date
            orientation.processing_date = timezone.now()

            orientation.delete_attachments()

            if orientation.should_send_email:
                send_orientation_expiration_emails(orientation)
                orientation.last_reminder_email_sent = timezone.now()

            orientations_to_update.append(orientation)

        Orientation.objects.bulk_update(
            orientations_to_update,
            ["status", "last_reminder_email_sent", "processing_date"],
        )

        self.stdout.write(f"{len(orientations_to_update)} orientations ont clôturées")
