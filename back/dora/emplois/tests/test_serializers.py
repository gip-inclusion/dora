import pytest
from data_inclusion.schema.v1.publics import Public as DiPublic
from model_bakery import baker

from dora.core.test_utils import make_published_service
from dora.emplois.serializers import ServiceSerializer
from dora.emplois.views import PREFETCH_RELATED_SERVICE_LIST
from dora.services.models import (
    AccessCondition,
    BeneficiaryAccessMode,
    CoachOrientationMode,
    Credential,
    FundingLabel,
    Public,
    Requirement,
    Service,
    ServiceKind,
)


def test_service_serializer_publics_defaults_to_all_publics():
    service = make_published_service()
    service.publics.clear()

    data = ServiceSerializer(service).data

    assert data["publics"] == ["Tous publics"]


def test_service_serializer_publics_with_publics():
    service = make_published_service()
    service.publics.clear()

    public_jeunes = baker.make(
        Public,
        name="Jeunes 18-25",
        corresponding_di_publics=[DiPublic.JEUNES],
        structure=service.structure,
    )
    public_seniors = baker.make(
        Public,
        name="Seniors 60+",
        corresponding_di_publics=[DiPublic.SENIORS],
        structure=service.structure,
    )
    service.publics.set([public_jeunes, public_seniors])

    data = ServiceSerializer(service).data

    assert data["publics"] == ["Jeunes 18-25", "Seniors 60+"]


@pytest.mark.parametrize(
    "add_access_conditions,add_requirements,qpv_or_zrr,expected",
    [
        (
            True,
            True,
            False,
            [
                "Inscrit à Pôle emploi",
                "Inscrit à la Mission Locale",
                "Niveau bac",
                "Permis B",
            ],
        ),
        (
            True,
            True,
            True,
            [
                "Inscrit à Pôle emploi",
                "Inscrit à la Mission Locale",
                "Niveau bac",
                "Permis B",
                "Uniquement QPV ou ZFRR",
            ],
        ),
        (False, True, False, ["Niveau bac", "Permis B"]),
        (
            True,
            False,
            False,
            ["Inscrit à Pôle emploi", "Inscrit à la Mission Locale"],
        ),
        (False, False, True, ["Uniquement QPV ou ZFRR"]),
    ],
    ids=[
        "ac_and_req_no_qpv",
        "ac_and_req_with_qpv",
        "only_requirements",
        "only_access_conditions",
        "only_qpv_flag",
    ],
)
def test_service_serializer_eligibility_requirements(
    add_access_conditions, add_requirements, qpv_or_zrr, expected
):
    service = make_published_service()
    service.access_conditions.clear()
    service.requirements.clear()

    if add_access_conditions:
        ac_1 = baker.make(
            AccessCondition,
            name="Inscrit à Pôle emploi",
            structure=service.structure,
        )
        ac_2 = baker.make(
            AccessCondition,
            name="Inscrit à la Mission Locale",
            structure=service.structure,
        )
        service.access_conditions.add(ac_1, ac_2)
    if add_requirements:
        req_1 = baker.make(Requirement, name="Niveau bac", structure=service.structure)
        req_2 = baker.make(Requirement, name="Permis B", structure=service.structure)
        service.requirements.add(req_1, req_2)

    service.qpv_or_zrr = qpv_or_zrr
    service.save()

    data = ServiceSerializer(service).data
    assert data["eligibility_requirements"] == expected


def test_service_serializer_basic_fields():
    service = make_published_service(
        short_desc="Une courte description",
        is_cumulative=True,
        online_form="https://example.org/formulaire",
        is_contact_info_public=True,
    )

    service.get_diffusion_zone_details_display = lambda: "Zone de diffusion"

    data = ServiceSerializer(service).data

    assert data["id"] == str(service.id)
    assert data["diffusion_zone"] == "Zone de diffusion"
    assert data["short_desc"] == "Une courte description"
    assert data["is_cumulative"] is True
    assert data["online_form"] == "https://example.org/formulaire"
    assert data["is_contact_info_public"] is True


def test_service_serializer_funding_labels():
    service = make_published_service()
    service.funding_labels.clear()

    label_1 = baker.make(FundingLabel, label="Label 1")
    label_2 = baker.make(FundingLabel, label="Label 2")
    service.funding_labels.add(label_1, label_2)

    data = ServiceSerializer(service).data

    assert sorted(data["funding_labels"]) == ["Label 1", "Label 2"]


def test_service_serializer_mobilization_modes_professionals():
    service = make_published_service()
    service.coach_orientation_modes.clear()

    mode_formulaire_dora = CoachOrientationMode.objects.get(value="formulaire-dora")
    mode_mail_avec_fiche = CoachOrientationMode.objects.get(
        value="envoyer-un-mail-avec-une-fiche-de-prescription"
    )
    mode_envoyer_mail = CoachOrientationMode.objects.get(value="envoyer-un-mail")
    mode_telephoner = CoachOrientationMode.objects.get(value="telephoner")
    mode_autre = CoachOrientationMode.objects.get(value="autre")
    mode_completer_formulaire = CoachOrientationMode.objects.get(
        value="completer-le-formulaire-dadhesion"
    )

    service.coach_orientation_modes.set(
        [
            mode_envoyer_mail,
            mode_autre,
            mode_formulaire_dora,
            mode_telephoner,
            mode_mail_avec_fiche,
            mode_completer_formulaire,
        ]
    )
    service.coach_orientation_modes_other = "Autre modalité personnalisée"
    service.coach_orientation_modes_external_form_link = (
        "https://example.org/external-form"
    )
    service.contact_email = "contact@example.org"
    service.save()

    data = ServiceSerializer(service).data["mobilization_modes_professionals"]

    # Tous les coach_orientation_modes possibles sont présents et ordonnés comme dans
    # COACH_ORIENTATION_MODES_ORDER
    assert data == [
        {
            "name": "Orienter votre bénéficiaire via le formulaire DORA",
            "link": None,
            "custom": False,
        },
        {
            "name": "Envoyer un email avec une fiche de prescription",
            "link": None,
            "custom": False,
        },
        {
            "name": mode_completer_formulaire.label,
            "link": "https://example.org/external-form",
            "custom": False,
        },
        {
            "name": mode_envoyer_mail.label,
            "link": None,
            "custom": False,
        },
        {
            "name": mode_telephoner.label,
            "link": None,
            "custom": False,
        },
        {
            "name": "Autre modalité personnalisée",
            "link": None,
            "custom": True,
        },
    ]


def test_service_serializer_mobilization_modes_individuals():
    service = make_published_service()
    service.beneficiaries_access_modes.clear()

    mode_completer_formulaire = BeneficiaryAccessMode.objects.get(
        value="completer-le-formulaire-dadhesion"
    )
    mode_professionnel = BeneficiaryAccessMode.objects.get(value="professionnel")
    mode_autre = BeneficiaryAccessMode.objects.get(value="autre")
    mode_envoyer_mail = BeneficiaryAccessMode.objects.get(value="envoyer-un-mail")
    mode_telephoner = BeneficiaryAccessMode.objects.get(value="telephoner")
    mode_se_presenter = BeneficiaryAccessMode.objects.get(value="se-presenter")

    service.beneficiaries_access_modes.set(
        [
            mode_autre,
            mode_envoyer_mail,
            mode_professionnel,
            mode_completer_formulaire,
            mode_telephoner,
            mode_se_presenter,
        ]
    )
    service.beneficiaries_access_modes_other = "Autre accès personnalisée"
    service.beneficiaries_access_modes_external_form_link = (
        "https://example.org/beneficiary-form"
    )
    service.beneficiaries_access_modes_external_form_link_text = "Remplir le formulaire"
    service.save()

    data = ServiceSerializer(service).data["mobilization_modes_individuals"]

    # Tous les beneficiaries_access_modes possibles sont présents et ordonnés comme dans
    # BENEFICIARIES_ACCESS_MODES_ORDER
    assert data == [
        {
            "name": mode_se_presenter.label,
            "link": None,
            "custom": False,
        },
        {
            "name": "Remplir le formulaire",
            "link": "https://example.org/beneficiary-form",
            "custom": False,
        },
        {
            "name": mode_envoyer_mail.label,
            "link": None,
            "custom": False,
        },
        {
            "name": mode_telephoner.label,
            "link": None,
            "custom": False,
        },
        {
            "name": "Orientation par un professionnel",
            "link": None,
            "custom": False,
        },
        {
            "name": "Autre accès personnalisée",
            "link": None,
            "custom": True,
        },
    ]


def test_service_serializer_forms_info_uses_storage_url(monkeypatch):
    service = make_published_service()
    service.forms = ["form1.pdf", "form2.pdf"]
    service.save()

    def fake_url(path):
        return f"https://files.example/{path}"

    monkeypatch.setattr(
        "dora.emplois.serializers.default_storage.url",
        fake_url,
    )

    data = ServiceSerializer(service).data

    assert data["forms_info"] == [
        {"name": "form1.pdf", "url": "https://files.example/form1.pdf"},
        {"name": "form2.pdf", "url": "https://files.example/form2.pdf"},
    ]


def test_service_serializer_credentials():
    service = make_published_service()
    service.credentials.clear()

    cred_1 = baker.make(Credential, name="Carte d'identité")
    cred_2 = baker.make(Credential, name="Justificatif de domicile")
    service.credentials.add(cred_1, cred_2)

    data = ServiceSerializer(service).data

    assert sorted(data["credentials"]) == [
        "Carte d'identité",
        "Justificatif de domicile",
    ]


def test_service_serializer_kinds():
    service = make_published_service()
    service.kinds.clear()

    kind_1, kind_2, kind_3 = ServiceKind.objects.all()[:3]
    service.kinds.add(kind_1, kind_2, kind_3)

    data = ServiceSerializer(service).data

    assert sorted(data["kinds"]) == [
        kind_1.label,
        kind_2.label,
        kind_3.label,
    ]


def test_service_serializer_is_orientable_with_dora_form_when_orientable_and_mode(
    orientable_service_via_dora_form,
):
    service = orientable_service_via_dora_form

    mode = CoachOrientationMode.objects.get(value="formulaire-dora")
    service.coach_orientation_modes.add(mode)

    # Vérification de cohérence sur la logique métier sous-jacente
    assert service.is_orientable() is True

    data = ServiceSerializer(service).data
    assert data["is_orientable_with_dora_form"] is True


def test_service_serializer_is_not_orientable_with_dora_form_when_not_orientable():
    service = make_published_service()
    service.contact_email = ""
    service.structure.disable_orientation_form = True
    service.structure.save()
    service.save()

    mode = CoachOrientationMode.objects.get(value="formulaire-dora")
    service.coach_orientation_modes.add(mode)

    assert service.is_orientable() is False

    data = ServiceSerializer(service).data
    assert data["is_orientable_with_dora_form"] is False


def test_service_serializer_is_not_orientable_with_dora_form_without_dora_mode(
    orientable_service_via_dora_form,
):
    service = orientable_service_via_dora_form

    assert service.is_orientable() is True
    assert (
        service.coach_orientation_modes.filter(value="formulaire-dora").exists()
        is False
    )

    data = ServiceSerializer(service).data
    assert data["is_orientable_with_dora_form"] is False


def test_service_serializer_is_orientable_with_dora_form_when_ft_whitelisted(
    ft_orientable_service,
):
    service = ft_orientable_service

    # On s'assure que l'orientation se fait via la liste blanche FT, et non via le formulaire Dora classique
    service.contact_email = ""
    service.structure.disable_orientation_form = True
    service.structure.save()
    service.save()

    mode = CoachOrientationMode.objects.get(value="formulaire-dora")
    service.coach_orientation_modes.add(mode)

    assert service.is_orientable_ft_service() is True
    assert service.is_orientable() is True

    data = ServiceSerializer(service).data
    assert data["is_orientable_with_dora_form"] is True


def test_service_serializer_does_not_add_queries_when_relations_prefetched(
    django_assert_max_num_queries,
):
    base_service = make_published_service()

    service = (
        Service.objects.filter(pk=base_service.pk)
        .select_related("structure")
        .prefetch_related(*PREFETCH_RELATED_SERVICE_LIST)
        .get()
    )

    with django_assert_max_num_queries(0):
        ServiceSerializer(service).data
