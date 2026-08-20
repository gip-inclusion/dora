from data_inclusion.schema.v1 import ModeMobilisation, PersonneMobilisatrice


def sync_mobilisation_fields(service, *, save=True):
    coach_values = {mode.value for mode in service.coach_orientation_modes.all()}
    beneficiary_values = {
        mode.value for mode in service.beneficiaries_access_modes.all()
    }

    link = None
    if "completer-le-formulaire-dadhesion" in coach_values:
        link = service.coach_orientation_modes_external_form_link or None
    if not link and "completer-le-formulaire-dadhesion" in beneficiary_values:
        link = service.beneficiaries_access_modes_external_form_link or None

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
        elif value == "completer-le-formulaire-dadhesion" and link:
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
        elif value == "completer-le-formulaire-dadhesion" and link:
            modes.add(ModeMobilisation.UTILISER_LIEN_MOBILISATION.value)

    has_professionnels = bool(coach_values) or "professionnel" in beneficiary_values
    has_usagers = any(value != "professionnel" for value in beneficiary_values)

    mobilisable_by = []
    if has_usagers:
        mobilisable_by.append(PersonneMobilisatrice.USAGERS.value)
    if has_professionnels:
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

    service.mobilisation_modes = sorted(modes) or None
    service.mobilisable_by = mobilisable_by or None
    service.mobilisation_details = mobilisation_details
    service.mobilisation_link = link
    if save:
        service.save(
            update_fields=[
                "mobilisation_modes",
                "mobilisable_by",
                "mobilisation_details",
                "mobilisation_link",
            ]
        )
