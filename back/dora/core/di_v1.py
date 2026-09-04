"""Migration logic for DI v1 fields.

For every new field or set of fields:
1. Add the necessary schema migration (AddField only, no data migration)
2. Extend sync_v1_service_fields() or sync_v1_structure_fields() below
3. Expose the field in dora/api/serializers.py (DI v1 name, mapped from the model)
4. Add tests (core/tests/test_di_v1.py and dora/api/test_api.py)
5. Backfill existing rows after deploy with backfill_di_v1 --wet-run
"""

import re

from data_inclusion.schema.v1 import ModeMobilisation, PersonneMobilisatrice
from django.core.exceptions import ValidationError
from django.db.models import prefetch_related_objects
from unidecode import unidecode

from dora.core.validators import validate_opening_hours_str
from dora.data_inclusion.diffusion_zone_info import (
    get_zone_eligibilite_from_diffusion_zone,
)
from dora.structures.reseaux_porteurs_mappings import (
    LABEL_NATIONAL_TO_RESEAU,
    TYPOLOGY_TO_RESEAU,
)

SERVICE_DI_V1_FIELDS = [
    "mobilisation_modes",
    "mobilisable_by",
    "mobilisation_details",
    "mobilisation_link",
    "zone_eligibilite",
    "conditions_acces",
    "publics_derived_from_conditions",
    "horaires_accueil",
]

STRUCTURE_DI_V1_FIELDS = ["reseaux_porteurs"]

# M2M lues par `sync_v1_service_fields`. Le `prefetch_related_objects` en tête de la
# fonction ne coûte rien quand l'appelant a déjà préchargé (cas du backfill, qui itère
# sur des milliers de lignes) et évite les requêtes une-par-relation sur les appels
# unitaires (sérialiseurs, admin, synchronisation depuis un modèle).
SERVICE_SYNC_PREFETCHES = [
    "coach_orientation_modes",
    "beneficiaries_access_modes",
    "access_conditions",
    "requirements",
    "credentials",
]

STRUCTURE_SYNC_PREFETCHES = ["national_labels"]


def sync_v1_service_fields(service, *, save=True):
    prefetch_related_objects([service], *SERVICE_SYNC_PREFETCHES)

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
    service.zone_eligibilite = get_zone_eligibilite_from_diffusion_zone(
        service.diffusion_zone_type,
        service.diffusion_zone_details,
    )

    conditions_acces, publics = extract_conditions_acces_and_publics(service)
    service.conditions_acces = conditions_acces
    service.publics_derived_from_conditions = publics

    if service.recurrence:
        try:
            validate_opening_hours_str(service.recurrence)
        except ValidationError:
            pass
        else:
            service.horaires_accueil = service.recurrence

    if save:
        service.save(update_fields=SERVICE_DI_V1_FIELDS)


def sync_v1_structure_fields(structure, *, save=True):
    prefetch_related_objects([structure], *STRUCTURE_SYNC_PREFETCHES)

    reseaux = set()
    if structure.typology:
        if reseau := TYPOLOGY_TO_RESEAU.get(structure.typology):
            reseaux.add(reseau)
    for label in structure.national_labels.all():
        if reseau := LABEL_NATIONAL_TO_RESEAU.get(label.value):
            reseaux.add(reseau)
    structure.reseaux_porteurs = sorted(reseaux) or None
    if save:
        structure.save(update_fields=STRUCTURE_DI_V1_FIELDS)


KEYWORDS_TO_PUBLICS_MAP = {
    "aah": "personnes-en-situation-de-handicap",
    "allocation spécifique de solidarité": "beneficiaires-des-minimas-sociaux",
    "carte d'invalidité": "personnes-en-situation-de-handicap",
    "cdaph": "personnes-en-situation-de-handicap",
    "contrat d'intégration républicaine": "personnes-exilees",
    "france travail": "demandeurs-emploi",
    "mal logé": "personnes-en-situation-durgence",
    "mission locale": "jeunes",
    "qpv": "residents-qpv-frr",
    "rqth": "personnes-en-situation-de-handicap",
    "rsa": "beneficiaires-des-minimas-sociaux",
    "sans logement": "personnes-en-situation-durgence",
    "zfrr": "residents-qpv-frr",
    "zrr": "residents-qpv-frr",
}

KEYWORDS_TO_PUBLICS_PATTERNS = [
    (re.compile(rf"\b{re.escape(keyword)}\w*"), public)
    for keyword, public in KEYWORDS_TO_PUBLICS_MAP.items()
]

APOSTROPHES = str.maketrans({"’": "'", "‘": "'"})


def extract_conditions_acces_and_publics(service):
    # Fonction pure des M2M de conditions : on ne réinjecte pas `service.publics`, saisi
    # par l'utilisateur. Sinon un public déduit une fois ne pourrait plus jamais être
    # retiré, la suppression de la condition qui l'a produit laissant la valeur en base.
    publics = set()

    # Un même libellé peut apparaître dans plusieurs des trois relations, et les choix
    # personnalisés sont dupliqués par structure : on dédoublonne pour ne pas répéter la
    # ligne dans `conditions_acces`.
    names = {
        obj.name
        for relation in (
            service.access_conditions,
            service.credentials,
            service.requirements,
        )
        for obj in relation.all()
    }

    matched_names = set()
    for pattern, public in KEYWORDS_TO_PUBLICS_PATTERNS:
        matching = {
            name
            for name in names
            if pattern.search(name.lower().translate(APOSTROPHES))
        }
        if matching:
            publics.add(public)
            matched_names |= matching

    conditions_acces = (
        "\n".join(sorted(names, key=lambda name: (unidecode(name).casefold(), name)))
        or None
    )

    return conditions_acces, sorted(publics)
