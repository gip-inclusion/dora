import pytest
from data_inclusion.schema.v1 import ModeMobilisation, PersonneMobilisatrice
from django.core.management import call_command

from dora.core.di_v1 import sync_v1_service_fields, sync_v1_structure_fields
from dora.core.test_utils import make_model, make_service, make_structure, make_user
from dora.data_inclusion.enums import TypologieStructure
from dora.services.enums import ServiceStatus
from dora.services.models import (
    AccessCondition,
    BeneficiaryAccessMode,
    CoachOrientationMode,
    Credential,
    Requirement,
    Service,
)
from dora.services.utils import (
    instantiate_service_from_model,
    synchronize_service_from_model,
)
from dora.structures.models import Structure, StructureNationalLabel


def test_backfill_di_v1_mobilisation_link():
    service = make_service(appointment_link="https://example.com/appt")
    Service.objects.filter(pk=service.pk).update(mobilisation_link=None)

    call_command("backfill_di_v1", "--services", "--wet-run")
    service.refresh_from_db()
    assert service.mobilisation_link == "https://example.com/appt"


@pytest.mark.parametrize(
    ("diffusion_zone_type", "diffusion_zone_details", "expected"),
    [
        ("country", "", ["france"]),
        ("department", "29", ["29"]),
    ],
)
def test_backfill_di_v1_zone_eligibilite(
    diffusion_zone_type, diffusion_zone_details, expected
):
    service = make_service(
        diffusion_zone_type=diffusion_zone_type,
        diffusion_zone_details=diffusion_zone_details,
    )
    Service.objects.filter(pk=service.pk).update(zone_eligibilite=None)

    call_command("backfill_di_v1", "--services", "--wet-run")
    service.refresh_from_db()
    assert service.zone_eligibilite == expected


def test_sync_mobilisation_fields_from_orientation_modes():
    service = make_service(
        coach_orientation_modes_external_form_link="https://example.com/coach",
    )
    service.coach_orientation_modes.set(
        CoachOrientationMode.objects.filter(value="envoyer-un-mail")
    )
    service.beneficiaries_access_modes.set(
        BeneficiaryAccessMode.objects.filter(value__in=["telephoner", "se-presenter"])
    )

    sync_v1_service_fields(service)
    service.refresh_from_db()

    assert service.mobilisation_modes == [
        ModeMobilisation.ENVOYER_UN_COURRIEL.value,
        ModeMobilisation.SE_PRESENTER.value,
        ModeMobilisation.TELEPHONER.value,
        ModeMobilisation.UTILISER_LIEN_MOBILISATION.value,
    ]
    assert service.mobilisable_by == [
        PersonneMobilisatrice.USAGERS.value,
        PersonneMobilisatrice.PROFESSIONNELS.value,
    ]
    assert service.mobilisation_link == "https://example.com/coach"
    assert service.mobilisation_details is None


def test_sync_mobilisation_fields_maps_adhesion_form_with_coach_link():
    service = make_service(
        coach_orientation_modes_external_form_link="https://example.com/coach-form",
    )
    service.coach_orientation_modes.set(
        CoachOrientationMode.objects.filter(value="completer-le-formulaire-dadhesion")
    )

    sync_v1_service_fields(service)
    service.refresh_from_db()

    assert service.mobilisation_modes == [
        ModeMobilisation.UTILISER_LIEN_MOBILISATION.value,
    ]
    assert service.mobilisation_link == "https://example.com/coach-form"


@pytest.mark.parametrize(
    ("service_kwargs", "coach_modes", "expected_link", "expected_details"),
    [
        (
            {
                "appointment_link": "https://example.com/rdv",
                "online_form": "https://example.com/online",
                "coach_orientation_modes_external_form_link": "https://example.com/coach",
            },
            ["telephoner"],
            "https://example.com/rdv",
            "Liens supplémentaires: https://example.com/online, https://example.com/coach",
        ),
        (
            {
                "appointment_link": "https://example.com/link",
                "online_form": "https://example.com/link",
                "coach_orientation_modes_external_form_link": "https://example.com/other",
            },
            [],
            "https://example.com/link",
            "Liens supplémentaires: https://example.com/other",
        ),
        (
            {
                "coach_orientation_modes_external_form_link": "https://example.com/stale",
                "beneficiaries_access_modes_external_form_link": (
                    "https://example.com/beneficiary"
                ),
            },
            ["envoyer-un-mail"],
            "https://example.com/stale",
            "Liens supplémentaires: https://example.com/beneficiary",
        ),
        (
            {"online_form": "https://example.com/online"},
            [],
            "https://example.com/online",
            None,
        ),
    ],
)
def test_sync_mobilisation_fields_aggregates_links(
    service_kwargs, coach_modes, expected_link, expected_details
):
    service = make_service(**service_kwargs)
    if coach_modes:
        service.coach_orientation_modes.set(
            CoachOrientationMode.objects.filter(value__in=coach_modes)
        )
    sync_v1_service_fields(service)
    service.refresh_from_db()
    assert service.mobilisation_link == expected_link
    assert service.mobilisation_details == expected_details
    assert ModeMobilisation.UTILISER_LIEN_MOBILISATION.value in (
        service.mobilisation_modes or []
    )


def test_sync_mobilisation_fields_maps_adhesion_form_with_beneficiary_link():
    service = make_service(
        beneficiaries_access_modes_external_form_link=(
            "https://example.com/beneficiary-form"
        ),
    )
    service.beneficiaries_access_modes.set(
        BeneficiaryAccessMode.objects.filter(value="completer-le-formulaire-dadhesion")
    )

    sync_v1_service_fields(service)
    service.refresh_from_db()

    assert service.mobilisation_modes == [
        ModeMobilisation.UTILISER_LIEN_MOBILISATION.value,
    ]
    assert service.mobilisation_link == "https://example.com/beneficiary-form"


def test_sync_mobilisation_fields_maps_formulaire_dora_without_storing_url():
    service = make_service()
    service.coach_orientation_modes.set(
        CoachOrientationMode.objects.filter(value="formulaire-dora")
    )

    sync_v1_service_fields(service)
    service.refresh_from_db()

    assert service.mobilisation_modes == [
        ModeMobilisation.UTILISER_LIEN_MOBILISATION.value,
    ]
    assert service.mobilisation_link is None


def test_sync_mobilisation_fields_skips_form_mode_without_link():
    service = make_service()
    service.coach_orientation_modes.set(
        CoachOrientationMode.objects.filter(value="completer-le-formulaire-dadhesion")
    )

    sync_v1_service_fields(service)
    service.refresh_from_db()

    assert service.mobilisation_modes is None
    assert service.mobilisation_link is None


def test_sync_mobilisation_fields_concatenates_autre_details():
    service = make_service(
        coach_orientation_modes_other="Précision accompagnateur",
        beneficiaries_access_modes_other="Précision bénéficiaire",
    )
    service.coach_orientation_modes.set(
        CoachOrientationMode.objects.filter(value="autre")
    )
    service.beneficiaries_access_modes.set(
        BeneficiaryAccessMode.objects.filter(value="autre")
    )

    sync_v1_service_fields(service)
    service.refresh_from_db()

    assert service.mobilisation_details == (
        "Professionnels : Précision accompagnateur ; Usagers : Précision bénéficiaire"
    )
    assert service.mobilisation_modes is None
    assert service.mobilisable_by == [
        PersonneMobilisatrice.USAGERS.value,
        PersonneMobilisatrice.PROFESSIONNELS.value,
    ]


def test_sync_mobilisation_fields_autre_beneficiary_is_usagers():
    service = make_service(
        beneficiaries_access_modes_other="Précision bénéficiaire",
    )
    service.coach_orientation_modes.clear()
    service.beneficiaries_access_modes.set(
        BeneficiaryAccessMode.objects.filter(value="autre")
    )

    sync_v1_service_fields(service)
    service.refresh_from_db()

    assert service.mobilisable_by == [PersonneMobilisatrice.USAGERS.value]
    assert service.mobilisation_modes is None
    assert service.mobilisation_details == "Précision bénéficiaire"


def test_sync_mobilisation_fields_professionnel_only_is_not_usagers():
    service = make_service()
    service.coach_orientation_modes.clear()
    service.beneficiaries_access_modes.set(
        BeneficiaryAccessMode.objects.filter(value="professionnel")
    )

    sync_v1_service_fields(service)
    service.refresh_from_db()

    assert service.mobilisable_by == [PersonneMobilisatrice.PROFESSIONNELS.value]
    assert service.mobilisation_modes is None


def test_sync_mobilisation_fields_professionnel_adds_professionnels():
    service = make_service()
    service.coach_orientation_modes.set(
        CoachOrientationMode.objects.filter(value="envoyer-un-mail")
    )
    service.beneficiaries_access_modes.set(
        BeneficiaryAccessMode.objects.filter(value__in=["telephoner", "professionnel"])
    )

    sync_v1_service_fields(service)
    service.refresh_from_db()

    assert service.mobilisable_by == [
        PersonneMobilisatrice.USAGERS.value,
        PersonneMobilisatrice.PROFESSIONNELS.value,
    ]
    assert service.mobilisation_modes == [
        ModeMobilisation.ENVOYER_UN_COURRIEL.value,
        ModeMobilisation.TELEPHONER.value,
    ]


def test_service_patch_syncs_mobilisation_fields(api_client):
    user = make_user(is_valid=True)
    structure = make_structure(user)
    service = make_service(structure=structure, status=ServiceStatus.DRAFT)
    api_client.force_authenticate(user=user)

    response = api_client.patch(
        f"/services/{service.slug}/",
        {
            "coachOrientationModes": ["envoyer-un-mail"],
            "beneficiariesAccessModes": ["se-presenter"],
            "mobilisationDetails": "ne doit pas être pris en compte",
            "mobilisationLink": "https://ignored.example.com",
        },
        format="json",
    )

    assert response.status_code == 200
    assert response.data["mobilisation_modes"] == [
        ModeMobilisation.ENVOYER_UN_COURRIEL.value,
        ModeMobilisation.SE_PRESENTER.value,
    ]
    assert response.data["mobilisation_modes_display"] == [
        ModeMobilisation.ENVOYER_UN_COURRIEL.label,
        ModeMobilisation.SE_PRESENTER.label,
    ]
    assert response.data["mobilisable_by"] == [
        PersonneMobilisatrice.USAGERS.value,
        PersonneMobilisatrice.PROFESSIONNELS.value,
    ]
    service.refresh_from_db()
    assert service.mobilisation_modes == [
        ModeMobilisation.ENVOYER_UN_COURRIEL.value,
        ModeMobilisation.SE_PRESENTER.value,
    ]
    assert service.mobilisable_by == [
        PersonneMobilisatrice.USAGERS.value,
        PersonneMobilisatrice.PROFESSIONNELS.value,
    ]
    assert service.mobilisation_details is None
    assert service.mobilisation_link is None


def test_sync_mobilisation_fields_keeps_formulaire_dora_on_model_without_url():
    model = make_model()
    model.coach_orientation_modes.set(
        CoachOrientationMode.objects.filter(value="formulaire-dora")
    )

    sync_v1_service_fields(model)
    model.refresh_from_db()

    assert model.mobilisation_modes == [
        ModeMobilisation.UTILISER_LIEN_MOBILISATION.value,
    ]
    assert model.mobilisable_by == [PersonneMobilisatrice.PROFESSIONNELS.value]
    assert model.mobilisation_link is None


def test_sync_mobilisation_fields_keeps_external_link_on_model():
    model = make_model(
        coach_orientation_modes_external_form_link="https://example.com/form",
    )
    model.coach_orientation_modes.set(
        CoachOrientationMode.objects.filter(value="completer-le-formulaire-dadhesion")
    )

    sync_v1_service_fields(model)
    model.refresh_from_db()

    assert model.mobilisation_modes == [
        ModeMobilisation.UTILISER_LIEN_MOBILISATION.value,
    ]
    assert model.mobilisation_link == "https://example.com/form"


def test_synchronize_service_from_model_recomputes_mobilisation():
    structure = make_structure()
    model = make_model(structure=structure)
    model.coach_orientation_modes.set(
        CoachOrientationMode.objects.filter(value="telephoner")
    )
    service = make_service(structure=structure, model=model)

    synchronize_service_from_model(service, model)
    service.refresh_from_db()

    assert service.mobilisation_modes == [ModeMobilisation.TELEPHONER.value]
    assert service.mobilisable_by == [PersonneMobilisatrice.PROFESSIONNELS.value]


def test_instantiate_service_from_model_keeps_empty_dora_form_link():
    structure = make_structure()
    user = make_user()
    model = make_model(structure=structure)
    model.coach_orientation_modes.set(
        CoachOrientationMode.objects.filter(value="formulaire-dora")
    )
    sync_v1_service_fields(model)

    service = instantiate_service_from_model(model, structure, user)
    service.refresh_from_db()

    assert model.mobilisation_link is None
    assert service.mobilisation_modes == [
        ModeMobilisation.UTILISER_LIEN_MOBILISATION.value,
    ]
    assert service.mobilisation_link is None


@pytest.mark.parametrize(
    ("typology", "national_labels", "expected"),
    [
        pytest.param(
            TypologieStructure.FT.value,
            [],
            ["france-travail"],
            id="typology",
        ),
        pytest.param(
            TypologieStructure.ASSO.value,
            ["mission-locale"],
            ["mission-locale"],
            id="national_label",
        ),
        pytest.param(
            TypologieStructure.FT.value,
            ["france-travail"],
            ["france-travail"],
            id="deduplicates_typology_and_label",
        ),
        pytest.param(
            TypologieStructure.ASSO.value,
            ["cci"],
            ["chambres-consulaires"],
            id="label_alias",
        ),
        pytest.param(
            TypologieStructure.ASSO.value,
            [],
            None,
            id="no_mapping",
        ),
    ],
)
def test_reseaux_porteurs(typology, national_labels, expected):
    structure = make_structure(typology=typology)
    for label in national_labels:
        structure.national_labels.add(StructureNationalLabel.objects.get(value=label))

    sync_v1_structure_fields(structure)
    structure.refresh_from_db()

    assert structure.reseaux_porteurs == expected


def test_backfill_di_v1_reseaux_porteurs():
    structure = make_structure(typology=TypologieStructure.FT.value)
    structure.national_labels.add(
        StructureNationalLabel.objects.get(value="france-travail")
    )
    Structure.objects.filter(pk=structure.pk).update(reseaux_porteurs=None)

    call_command("backfill_di_v1", "--structures", "--wet-run")
    structure.refresh_from_db()
    assert structure.reseaux_porteurs == ["france-travail"]


@pytest.mark.parametrize(
    ("names", "expected_publics"),
    [
        pytest.param(["Résident en qpv"], ["residents-qpv-frr"], id="single_keyword"),
        pytest.param(
            ["Résident en QPV"],
            ["residents-qpv-frr"],
            id="case_insensitive",
        ),
        pytest.param(
            ["Habite en qpv", "Habite en zfrr"],
            ["residents-qpv-frr"],
            id="two_keywords_same_public",
        ),
        pytest.param(
            ["Bénéficiaire du rsa", "Inscrit à france travail"],
            ["beneficiaires-des-minimas-sociaux", "demandeurs-emploi"],
            id="two_publics_sorted",
        ),
        pytest.param(["Être majeur"], [], id="no_keyword"),
        pytest.param(
            ["Après un entretien de conversation"],
            [],
            id="keyword_inside_another_word",
        ),
        pytest.param(
            ["Critère d'universalité"],
            [],
            id="keyword_inside_another_accented_word",
        ),
        pytest.param(
            ["Personnes mal logées"],
            ["personnes-en-situation-durgence"],
            id="keyword_with_accord",
        ),
        pytest.param(
            ["Carte d’invalidité"],
            ["personnes-en-situation-de-handicap"],
            id="typographic_apostrophe",
        ),
        pytest.param(
            ["Bénéficiaire de l'aah"],
            ["personnes-en-situation-de-handicap"],
            id="keyword_after_elision",
        ),
    ],
)
def test_extract_conditions_acces_and_publics_maps_publics(names, expected_publics):
    service = make_service()
    for name in names:
        service.access_conditions.add(AccessCondition.objects.create(name=name))

    sync_v1_service_fields(service)
    service.refresh_from_db()

    assert service.publics_derived_from_conditions == expected_publics


def test_extract_conditions_acces_and_publics_dedupes_names_across_relations():
    service = make_service()
    service.access_conditions.add(AccessCondition.objects.create(name="Être majeur"))
    service.credentials.add(Credential.objects.create(name="Être majeur"))
    service.requirements.add(Requirement.objects.create(name="Avoir un CV"))

    sync_v1_service_fields(service)
    service.refresh_from_db()

    assert service.conditions_acces == "Avoir un CV\nÊtre majeur"


def test_extract_conditions_acces_and_publics_keeps_false_positives_in_conditions_acces():
    service = make_service()
    service.access_conditions.add(
        AccessCondition.objects.create(name="Après un entretien de conversation")
    )

    sync_v1_service_fields(service)
    service.refresh_from_db()

    assert service.conditions_acces == "Après un entretien de conversation"
    assert service.publics_derived_from_conditions == []


def test_extract_conditions_acces_and_publics_leaves_user_publics_untouched():
    service = make_service(publics=["jeunes"])
    service.access_conditions.add(
        AccessCondition.objects.create(name="Bénéficiaire du rsa")
    )

    sync_v1_service_fields(service)
    service.refresh_from_db()

    assert service.publics == ["jeunes"]
    assert service.publics_derived_from_conditions == [
        "beneficiaires-des-minimas-sociaux"
    ]


def test_extract_conditions_acces_and_publics_drops_publics_whose_condition_disappeared():
    service = make_service()
    condition = AccessCondition.objects.create(name="Bénéficiaire du rsa")
    service.access_conditions.add(condition)
    sync_v1_service_fields(service)

    service.access_conditions.remove(condition)
    sync_v1_service_fields(service)
    service.refresh_from_db()

    assert service.publics_derived_from_conditions == []


def test_extract_conditions_acces_and_publics_reads_all_three_relations():
    service = make_service()
    service.access_conditions.add(AccessCondition.objects.create(name="Résident qpv"))
    service.credentials.add(Credential.objects.create(name="Notification rqth"))
    service.requirements.add(Requirement.objects.create(name="Suivi mission locale"))

    sync_v1_service_fields(service)
    service.refresh_from_db()

    assert service.publics_derived_from_conditions == [
        "jeunes",
        "personnes-en-situation-de-handicap",
        "residents-qpv-frr",
    ]
    assert (
        service.conditions_acces
        == "Notification rqth\nRésident qpv\nSuivi mission locale"
    )


def test_extract_conditions_acces_and_publics_keeps_unmatched_names_sorted():
    service = make_service()
    service.access_conditions.add(AccessCondition.objects.create(name="Être majeur"))
    service.credentials.add(Credential.objects.create(name="Pièce d'identité"))
    service.requirements.add(Requirement.objects.create(name="Avoir un CV"))

    sync_v1_service_fields(service)
    service.refresh_from_db()

    assert service.conditions_acces == "Avoir un CV\nÊtre majeur\nPièce d'identité"
    assert service.publics_derived_from_conditions == []


def test_extract_conditions_acces_and_publics_excludes_matched_names_from_conditions_acces():
    service = make_service()
    service.access_conditions.add(
        AccessCondition.objects.create(name="Résident QPV"),
        AccessCondition.objects.create(name="Être majeur"),
    )

    sync_v1_service_fields(service)
    service.refresh_from_db()

    assert service.conditions_acces == "Être majeur\nRésident QPV"
    assert service.publics_derived_from_conditions == ["residents-qpv-frr"]


def test_extract_conditions_acces_and_publics_without_relations():
    service = make_service()

    sync_v1_service_fields(service)
    service.refresh_from_db()

    assert service.conditions_acces is None
    assert service.publics_derived_from_conditions == []


def test_backfill_di_v1_access_conditions():
    service = make_service()
    service.access_conditions.add(
        AccessCondition.objects.create(name="Résident en qpv"),
        AccessCondition.objects.create(name="Être majeur"),
    )
    Service.objects.filter(pk=service.pk).update(
        conditions_acces=None, publics_derived_from_conditions=[]
    )

    call_command("backfill_di_v1", "--services", "--wet-run")
    service.refresh_from_db()

    assert service.conditions_acces == "Être majeur\nRésident en qpv"
    assert service.publics_derived_from_conditions == ["residents-qpv-frr"]
