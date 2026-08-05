"""Migration des modes d'orientation DORA vers les modes de mobilisation data·inclusion.

Les deux référentiels `BeneficiaryAccessMode` / `CoachOrientationMode` et les huit
champs associés du service sont fusionnés dans les quatre champs du schéma d·i v1.
"""

from collections import defaultdict

from django.db import migrations

# Correspondances entre les anciennes valeurs DORA et les modes de mobilisation.
# La valeur `autre` n'a pas d'équivalent : son texte libre part dans
# `mobilisation_precisions`. La valeur `professionnel` (côté bénéficiaire) est
# redondante avec `mobilisable_par` et disparaît elle aussi.
COACH_MODE_MAP = {
    "envoyer-un-mail": "envoyer-un-courriel",
    "envoyer-un-mail-avec-une-fiche-de-prescription": "envoyer-un-courriel",
    "telephoner": "telephoner",
    "se-presenter": "se-presenter",
    "completer-le-formulaire-dadhesion": "utiliser-lien-mobilisation",
    "formulaire-dora": "formulaire-dora",
}

BENEFICIARY_MODE_MAP = {
    "envoyer-un-mail": "envoyer-un-courriel",
    "telephoner": "telephoner",
    "se-presenter": "se-presenter",
    "completer-le-formulaire-dadhesion": "utiliser-lien-mobilisation",
}

# Ordre canonique : les valeurs sont toujours écrites dans cet ordre, faute de
# quoi une permutation modifierait le checksum de synchronisation des modèles.
MODES_MOBILISATION_ORDER = [
    "envoyer-un-courriel",
    "se-presenter",
    "telephoner",
    "utiliser-lien-mobilisation",
    "formulaire-dora",
]
MOBILISABLE_PAR_ORDER = ["usagers", "professionnels"]

PRECISIONS_SEPARATOR = "\n\n"
# Préfixe du lien bénéficiaire écrasé, conservé en clair dans les précisions.
LIEN_USAGERS_PREFIX = "Lien de mobilisation pour les usagers : "
BATCH_SIZE = 1000


def compute_mobilisation_fields(
    beneficiary_modes,
    coach_modes,
    coach_link,
    beneficiary_link,
    coach_other,
    beneficiary_other,
):
    """Calcule les quatre champs de mobilisation à partir des anciennes valeurs.

    Isolée de la migration pour être testable directement.
    """
    beneficiary_modes = set(beneficiary_modes or ())
    coach_modes = set(coach_modes or ())

    # `mobilisable_par` : la valeur `professionnel` signifie que le bénéficiaire
    # doit passer par un professionnel, donc que le service n'est pas mobilisable
    # directement par les usagers.
    mobilisable_par = set()
    if coach_modes:
        mobilisable_par.add("professionnels")
    if beneficiary_modes:
        if "professionnel" in beneficiary_modes:
            mobilisable_par = {"professionnels"}
        else:
            mobilisable_par.add("usagers")

    modes = {COACH_MODE_MAP[mode] for mode in coach_modes if mode in COACH_MODE_MAP} | {
        BENEFICIARY_MODE_MAP[mode]
        for mode in beneficiary_modes
        if mode in BENEFICIARY_MODE_MAP
    }

    # Un seul lien subsiste, celui de l'accompagnateur est prioritaire.
    coach_link = (coach_link or "").strip()
    beneficiary_link = (beneficiary_link or "").strip()
    lien_mobilisation = coach_link or beneficiary_link
    if not lien_mobilisation:
        modes.discard("utiliser-lien-mobilisation")

    coach_other = (coach_other or "").strip()
    beneficiary_other = (beneficiary_other or "").strip()
    precisions_parts = [coach_other]
    if beneficiary_other != coach_other:
        precisions_parts.append(beneficiary_other)
    # Le lien bénéficiaire écrasé par celui de l'accompagnateur est conservé en
    # clair : c'est la seule information que la fusion perdrait sinon.
    if beneficiary_link and beneficiary_link != lien_mobilisation:
        precisions_parts.append(LIEN_USAGERS_PREFIX + beneficiary_link)
    precisions = PRECISIONS_SEPARATOR.join(part for part in precisions_parts if part)

    return {
        "modes_mobilisation": [
            mode for mode in MODES_MOBILISATION_ORDER if mode in modes
        ],
        "mobilisable_par": [
            person for person in MOBILISABLE_PAR_ORDER if person in mobilisable_par
        ],
        "mobilisation_precisions": precisions,
        "lien_mobilisation": lien_mobilisation,
    }


def _flush(Service, batch):
    if batch:
        Service._base_manager.bulk_update(
            batch,
            [
                "modes_mobilisation",
                "mobilisable_par",
                "mobilisation_precisions",
                "lien_mobilisation",
            ],
        )


def forward(apps, schema_editor):
    Service = apps.get_model("services", "Service")

    # Les deux tables de liaison sont chargées en une requête chacune.
    beneficiary_modes_by_service = defaultdict(set)
    for (
        service_id,
        value,
    ) in Service.beneficiaries_access_modes.through.objects.values_list(
        "service_id", "beneficiaryaccessmode__value"
    ):
        beneficiary_modes_by_service[service_id].add(value)

    coach_modes_by_service = defaultdict(set)
    for (
        service_id,
        value,
    ) in Service.coach_orientation_modes.through.objects.values_list(
        "service_id", "coachorientationmode__value"
    ):
        coach_modes_by_service[service_id].add(value)

    # `_base_manager` : les modèles de service (`is_model=True`) sont dans la même
    # table et doivent être migrés eux aussi.
    services = Service._base_manager.only(
        "id",
        "beneficiaries_access_modes_external_form_link",
        "beneficiaries_access_modes_other",
        "coach_orientation_modes_external_form_link",
        "coach_orientation_modes_other",
    ).order_by("id")

    batch = []
    for service in services.iterator(chunk_size=BATCH_SIZE):
        fields = compute_mobilisation_fields(
            beneficiary_modes=beneficiary_modes_by_service.get(service.id, set()),
            coach_modes=coach_modes_by_service.get(service.id, set()),
            coach_link=service.coach_orientation_modes_external_form_link,
            beneficiary_link=service.beneficiaries_access_modes_external_form_link,
            coach_other=service.coach_orientation_modes_other,
            beneficiary_other=service.beneficiaries_access_modes_other,
        )
        for name, value in fields.items():
            setattr(service, name, value)

        batch.append(service)
        if len(batch) >= BATCH_SIZE:
            _flush(Service, batch)
            batch = []

    _flush(Service, batch)


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0005_add_mobilisation_fields"),
    ]

    operations = [
        # Non réversible : la reconstruction des anciennes valeurs serait
        # ambiguë (`envoyer-un-mail` et `envoyer-un-mail-avec-une-fiche-de
        # -prescription` sont indiscernables une fois fusionnés).
        migrations.RunPython(forward, migrations.RunPython.noop),
    ]
