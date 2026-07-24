import json

from django.utils import timezone

from dora.core.commands import BaseCommand
from dora.orientations.models import Orientation


def _isoformat(value):
    return value.isoformat() if value else None


def _service_id(orientation: Orientation) -> str:
    # On reconstruit l'identifiant de service tel que Les Emplois l'avait fourni :
    # un service DORA (converti en FK à la création) redevient « dora--<uuid> »,
    # sinon on conserve le `di_service_id` d'origine.
    # Même logique que `OrientationViewSet.perform_create` et
    # `EmploisOrientationCreateSerializer.to_representation`.
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
            "emplois_sync_uid": str(emplois_data.emplois_sync_uid),
            "beneficiary_id": str(emplois_data.beneficiary_id),
            "prescriber_id": str(emplois_data.prescriber_id)
            if emplois_data.prescriber_id
            else None,
            "structure_id": str(emplois_data.structure_id),
            "service_id": _service_id(orientation),
            # Cycle de vie
            "status": orientation.status,
            "creation_date": _isoformat(orientation.creation_date),
            "processing_date": _isoformat(orientation.processing_date),
            # Bénéficiaire
            "beneficiary_contact_preferences": orientation.beneficiary_contact_preferences,
            "beneficiary_other_contact_method": orientation.beneficiary_other_contact_method,
            "beneficiary_availability": _isoformat(
                orientation.beneficiary_availability
            ),
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
            json.dump(data, json_file, ensure_ascii=False, indent=2)

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
