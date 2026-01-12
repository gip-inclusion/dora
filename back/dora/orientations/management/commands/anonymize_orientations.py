from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from dora.core.commands import BaseCommand
from dora.orientations.models import Orientation


class Command(BaseCommand):
    help = "Anonymise les orientations en supprimant les données personnelles après un délai"

    def handle(self, *args, **options):
        self.logger.info(
            "Anonymisation des orientations qui ont été créées il y a plus de %d jours.",
            settings.ORIENTATION_ANONYMIZATION_PERIOD_DAYS,
        )

        anonymization_date = timezone.localdate() - timedelta(
            days=settings.ORIENTATION_ANONYMIZATION_PERIOD_DAYS
        )

        orientations_to_anonymize = Orientation.objects.filter(
            creation_date__date__lte=anonymization_date
        )

        orientations_to_update = []

        for orientation in orientations_to_anonymize:
            orientation.beneficiary_first_name = ""
            orientation.beneficiary_last_name = ""
            orientation.beneficiary_phone = ""
            orientation.beneficiary_email = ""
            orientation.beneficiary_france_travail_number = ""
            orientation.referent_first_name = ""
            orientation.referent_last_name = ""
            orientation.referent_phone = ""
            orientation.referent_email = ""
            orientation.di_contact_name = ""
            orientation.di_contact_email = ""

            orientation.is_anonymized = True
            orientation.processing_date = timezone.now()

            orientations_to_update.append(orientation)

        count = orientations_to_anonymize.update(
            beneficiary_first_name="",
            beneficiary_last_name="",
            beneficiary_phone="",
            beneficiary_email="",
            beneficiary_france_travail_number="",
            referent_first_name="",
            referent_last_name="",
            referent_phone="",
            referent_email="",
            di_contact_name="",
            di_contact_email="",
            is_anonymized=True,
            processing_date=timezone.now(),
        )

        self.logger.info(
            "%s orientations ont été anonymisées.",
            count,
        )
