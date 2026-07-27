import json

from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone

from dora.core.commands import BaseCommand
from dora.orientations.models import Orientation


def _di_service_id(orientation: Orientation) -> str:
    if orientation.service_id:
        return f"dora--{orientation.service_id}"
    return orientation.di_service_id


class Command(BaseCommand):
    help = (
        "Exporte au format JSON toutes les orientations émises par Les Emplois "
        "afin qu'elles puissent être réimportées dans Les Emplois."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            type=str,
            help="Chemin du fichier JSON de sortie (par défaut : généré automatiquement)",
        )

    def _serialize_orientation(self, orientation: Orientation) -> dict:
        emplois_data = orientation.emplois_orientation_data
        return {
            # Identifiants Les Emplois transmis à la création de l'orientation et
            # stockés tels quels : ils permettent à Les Emplois de rattacher
            # l'orientation à ses propres objets lors du réimport.
            "emplois_sync_uid": emplois_data.emplois_sync_uid,
            "beneficiary_id": emplois_data.beneficiary_id,
            "prescriber_id": emplois_data.prescriber_id,
            "structure_id": emplois_data.structure_id,
            "service_id": _di_service_id(orientation),
            # Cycle de vie
            "status": orientation.status,
            "creation_date": orientation.creation_date,
            "processing_date": orientation.processing_date,
            # Bénéficiaire
            "beneficiary_contact_preferences": orientation.beneficiary_contact_preferences,
            "beneficiary_other_contact_method": orientation.beneficiary_other_contact_method,
            "beneficiary_availability": orientation.beneficiary_availability,
            "beneficiary_attachments": orientation.beneficiary_attachments,
            # Référent
            "referent_last_name": orientation.referent_last_name,
            "referent_first_name": orientation.referent_first_name,
            "referent_email": orientation.referent_email,
            "referent_phone": orientation.referent_phone,
            # Demande
            "requirements": orientation.requirements,
            "situation": orientation.situation,
            "situation_other": orientation.situation_other,
            "orientation_reasons": orientation.orientation_reasons,
            "duration_weekly_hours": orientation.duration_weekly_hours,
            "duration_weeks": orientation.duration_weeks,
            "data_protection_commitment": orientation.data_protection_commitment,
        }

    def handle(self, *args, **options):
        orientations = (
            Orientation.objects.emplois()
            .select_related("emplois_orientation_data", "service")
            .order_by("pk")
        )

        data = [
            self._serialize_orientation(orientation) for orientation in orientations
        ]

        output_file = (
            options["output"]
            or f"emplois_orientations_export_{timezone.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(
                data, json_file, cls=DjangoJSONEncoder, ensure_ascii=False, indent=2
            )

        self.logger.info(
            "%s orientation(s) Les Emplois exportée(s) dans %s.",
            len(data),
            output_file,
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"{len(data)} orientation(s) Les Emplois exportée(s) dans : {output_file}"
            )
        )
