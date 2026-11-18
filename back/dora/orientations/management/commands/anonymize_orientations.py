from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.db.models import Func, UUIDField
from django.utils import timezone

from dora.core.commands import BaseCommand
from dora.orientations.models import EmploisOrientationData, Orientation


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
            is_anonymized=False, creation_date__date__lte=anonymization_date
        )

        with transaction.atomic():
            emplois_count = EmploisOrientationData.objects.filter(
                orientation__in=orientations_to_anonymize
            ).update(
                beneficiary_id=Func(
                    function="gen_random_uuid", output_field=UUIDField()
                ),
                prescriber_email="",
                prescriber_first_name="",
                prescriber_last_name="",
                prescriber_phone="",
            )

            count = orientations_to_anonymize.update(
                beneficiary_first_name="",
                beneficiary_last_name="",
                beneficiary_phone="",
                beneficiary_email="",
                beneficiary_france_travail_number="",
                beneficiary_other_contact_method="",
                # Les fichiers, désormais non référencés, sont supprimés du
                # stockage par la commande `delete_orphaned_uploads`.
                beneficiary_attachments=[],
                situation=[],
                situation_other="",
                requirements=[],
                orientation_reasons="",
                referent_first_name="",
                referent_last_name="",
                referent_phone="",
                referent_email="",
                di_contact_name="",
                di_contact_email="",
                di_contact_phone="",
                is_anonymized=True,
            )

        self.logger.info(
            "%s orientations ont été anonymisées (dont %s avec des données Les Emplois).",
            count,
            emplois_count,
        )
