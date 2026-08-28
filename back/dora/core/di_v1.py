"""Migration logic for DI v1 fields.

For every new field or set of fields:
1. Add the necessary schema migration (AddField only, no data migration)
2. Extend sync_v1_service_fields() or sync_v1_structure_fields() below
3. Expose the field in dora/api/serializers.py (DI v1 name, mapped from the model)
4. Add tests (core/tests/test_di_v1.py and dora/api/test_api.py)
5. Backfill existing rows after deploy with backfill_di_v1 --wet-run
"""

from data_inclusion.schema.v1 import ModeMobilisation, PersonneMobilisatrice

SERVICE_DI_V1_FIELDS = [
    "mobilisation_modes",
    "mobilisable_by",
    "mobilisation_details",
    "mobilisation_link",
]

STRUCTURE_DI_V1_FIELDS = []


def sync_v1_service_fields(service, *, save=True):
    coach_values = {mode.value for mode in service.coach_orientation_modes.all()}
    beneficiary_values = {
        mode.value for mode in service.beneficiaries_access_modes.all()
    }

    links = list(
        dict.fromkeys(
            link
            for link in (
                service.appointment_link or None,
                service.online_form or None,
                service.coach_orientation_modes_external_form_link or None,
                service.beneficiaries_access_modes_external_form_link or None,
            )
            if link
        )
    )
    primary_link, *extra_links = links or [None]

    modes = set()
    for value in coach_values:
        if value == "envoyer-un-mail":
            modes.add(ModeMobilisation.ENVOYER_UN_COURRIEL.value)
        elif value == "envoyer-un-mail-avec-une-fiche-de-prescription":
            modes.add(ModeMobilisation.ENVOYER_UN_COURRIEL.value)
        elif value == "se-presenter":
            modes.add(ModeMobilisation.SE_PRESENTER.value)
        elif value == "telephoner":
            modes.add(ModeMobilisation.TELEPHONER.value)
        elif (
            value == "completer-le-formulaire-dadhesion"
            and service.coach_orientation_modes_external_form_link
        ):
            modes.add(ModeMobilisation.UTILISER_LIEN_MOBILISATION.value)
        elif value == "formulaire-dora":
            modes.add(ModeMobilisation.UTILISER_LIEN_MOBILISATION.value)

    for value in beneficiary_values:
        if value == "envoyer-un-mail":
            modes.add(ModeMobilisation.ENVOYER_UN_COURRIEL.value)
        elif value == "se-presenter":
            modes.add(ModeMobilisation.SE_PRESENTER.value)
        elif value == "telephoner":
            modes.add(ModeMobilisation.TELEPHONER.value)
        elif (
            value == "completer-le-formulaire-dadhesion"
            and service.beneficiaries_access_modes_external_form_link
        ):
            modes.add(ModeMobilisation.UTILISER_LIEN_MOBILISATION.value)

    if primary_link:
        modes.add(ModeMobilisation.UTILISER_LIEN_MOBILISATION.value)

    mobilisable_by = []
    if any(value != "professionnel" for value in beneficiary_values):
        mobilisable_by.append(PersonneMobilisatrice.USAGERS.value)
    if coach_values or "professionnel" in beneficiary_values:
        mobilisable_by.append(PersonneMobilisatrice.PROFESSIONNELS.value)

    coach_details = (
        service.coach_orientation_modes_other if "autre" in coach_values else None
    )
    beneficiary_details = (
        service.beneficiaries_access_modes_other
        if "autre" in beneficiary_values
        else None
    )
    if coach_details and beneficiary_details:
        mobilisation_details = (
            f"Professionnels : {coach_details} ; Usagers : {beneficiary_details}"
        )
    else:
        mobilisation_details = coach_details or beneficiary_details or None

    if extra_links:
        extra_line = f"Liens supplémentaires: {', '.join(extra_links)}"
        mobilisation_details = (
            f"{mobilisation_details}\n{extra_line}"
            if mobilisation_details
            else extra_line
        )

    service.mobilisation_modes = sorted(modes) or None
    service.mobilisable_by = mobilisable_by or None
    service.mobilisation_details = mobilisation_details
    service.mobilisation_link = primary_link
    if save:
        service.save(update_fields=SERVICE_DI_V1_FIELDS)


def sync_v1_structure_fields(structure, *, save=True):
    if save and STRUCTURE_DI_V1_FIELDS:
        structure.save(update_fields=STRUCTURE_DI_V1_FIELDS)
