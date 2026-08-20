from data_inclusion.schema.v1 import ModeMobilisation, PersonneMobilisatrice


def sync_mobilisation_fields(service):
    coach_values = set(service.coach_orientation_modes.values_list("value", flat=True))
    beneficiary_values = set(
        service.beneficiaries_access_modes.values_list("value", flat=True)
    )

    link = service.coach_orientation_modes_external_form_link or None
    if not link:
        link = service.beneficiaries_access_modes_external_form_link or None
    if not link and "formulaire-dora" in coach_values:
        link = service.get_dora_form_url()

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
        elif value == "formulaire-dora" and link:
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

    if "professionnel" in beneficiary_values:
        professionnels = True
        usagers = False
    else:
        professionnels = any(value != "autre" for value in coach_values)
        usagers = any(value != "autre" for value in beneficiary_values)

    mobilisable_by = []
    if usagers:
        mobilisable_by.append(PersonneMobilisatrice.USAGERS.value)
    if professionnels:
        mobilisable_by.append(PersonneMobilisatrice.PROFESSIONNELS.value)

    details_parts = []
    if "autre" in coach_values and service.coach_orientation_modes_other:
        details_parts.append(service.coach_orientation_modes_other)
    if "autre" in beneficiary_values and service.beneficiaries_access_modes_other:
        details_parts.append(service.beneficiaries_access_modes_other)

    service.mobilisation_modes = sorted(modes) or None
    service.mobilisable_by = mobilisable_by or None
    service.mobilisation_details = ", ".join(details_parts).strip() or None
    service.mobilisation_link = link
    service.save(
        update_fields=[
            "mobilisation_modes",
            "mobilisable_by",
            "mobilisation_details",
            "mobilisation_link",
        ]
    )
