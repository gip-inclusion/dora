from datetime import timedelta

from django.utils import timezone
from model_bakery import baker

from dora.core.test_utils import make_orientation, make_published_service
from dora.emplois.serializers import (
    DisabledDoraFormDIStructureSerializer,
    ReferenceDataSerializer,
    ServiceSerializer,
)
from dora.emplois.views import PREFETCH_RELATED_SERVICE_LIST
from dora.orientations.models import OrientationStatus
from dora.services.models import (
    BeneficiaryAccessMode,
    CoachOrientationMode,
    Credential,
    FundingLabel,
    Service,
)


def test_reference_data_serializer_fields():
    data = ReferenceDataSerializer(
        {
            "kind": "funding_label",
            "value": "cd-drome",
            "label": "CD Drome",
        }
    ).data

    assert data == {
        "kind": "funding_label",
        "value": "cd-drome",
        "label": "CD Drome",
    }


def test_service_serializer_basic_fields():
    service = make_published_service(
        short_desc="Une courte description",
        recurrence="Tous les jours de 8h30 à 12h30",
        online_form="https://example.org/formulaire",
        contact_name="John Doe",
        contact_phone="0123456789",
        contact_email="john.doe@example.org",
        is_contact_info_public=True,
        coach_orientation_modes_other="Autre modalité personnalisée",
        coach_orientation_modes_external_form_link="https://example.org/external-form",
        coach_orientation_modes_external_form_link_text="Remplir le formulaire",
        beneficiaries_access_modes_other="Autre accès personnalisée",
        beneficiaries_access_modes_external_form_link="https://example.org/beneficiary-form",
        beneficiaries_access_modes_external_form_link_text="Remplir le formulaire",
    )

    data = ServiceSerializer(service).data

    assert data["id"] == str(service.id)
    assert data["short_desc"] == "Une courte description"
    assert data["recurrence"] == "Tous les jours de 8h30 à 12h30"
    assert data["online_form"] == "https://example.org/formulaire"
    assert data["contact_name"] == "John Doe"
    assert data["contact_phone"] == "0123456789"
    assert data["contact_email"] == "john.doe@example.org"
    assert data["is_contact_info_public"] is True
    assert data["coach_orientation_modes_other"] == "Autre modalité personnalisée"
    assert (
        data["coach_orientation_modes_external_form_link"]
        == "https://example.org/external-form"
    )
    assert (
        data["coach_orientation_modes_external_form_link_text"]
        == "Remplir le formulaire"
    )
    assert data["beneficiaries_access_modes_other"] == "Autre accès personnalisée"
    assert (
        data["beneficiaries_access_modes_external_form_link"]
        == "https://example.org/beneficiary-form"
    )
    assert (
        data["beneficiaries_access_modes_external_form_link_text"]
        == "Remplir le formulaire"
    )


def test_service_serializer_funding_labels():
    service = make_published_service()
    service.funding_labels.clear()

    label_1 = baker.make(FundingLabel, label="Label 1", value="label-1")
    label_2 = baker.make(FundingLabel, label="Label 2", value="label-2")
    service.funding_labels.add(label_1, label_2)

    data = ServiceSerializer(service).data

    assert sorted(data["funding_labels"]) == ["label-1", "label-2"]


def test_service_serializer_custom_mobilization_form():
    service = make_published_service()
    service.coach_orientation_modes.clear()
    service.coach_orientation_modes.add(
        CoachOrientationMode.objects.get(value="completer-le-formulaire-dadhesion")
    )
    service.coach_orientation_modes_external_form_link = (
        "https://example.org/external-form"
    )
    service.coach_orientation_modes_external_form_link_text = "Remplir le formulaire"
    service.save()

    data = ServiceSerializer(service).data

    assert data["custom_mobilization_form"] == {
        "label": "Remplir le formulaire",
        "link": "https://example.org/external-form",
    }


def test_service_serializer_coach_orientation_modes():
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

    data = ServiceSerializer(service).data["coach_orientation_modes"]

    assert sorted(data) == sorted(
        [
            mode_formulaire_dora.value,
            mode_mail_avec_fiche.value,
            mode_envoyer_mail.value,
            mode_telephoner.value,
            mode_autre.value,
            mode_completer_formulaire.value,
        ]
    )


def test_service_serializer_beneficiaries_access_modes():
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

    data = ServiceSerializer(service).data["beneficiaries_access_modes"]

    assert sorted(data) == sorted(
        [
            mode_se_presenter.value,
            mode_completer_formulaire.value,
            mode_envoyer_mail.value,
            mode_telephoner.value,
            mode_professionnel.value,
            mode_autre.value,
        ]
    )


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


def test_service_serializer_is_orientable_with_form_when_orientable_and_mode(
    orientable_service_via_dora_form,
):
    service = orientable_service_via_dora_form

    mode = CoachOrientationMode.objects.get(value="formulaire-dora")
    service.coach_orientation_modes.add(mode)

    # Vérification de cohérence sur la logique métier sous-jacente
    assert service.is_orientable() is True

    data = ServiceSerializer(service).data
    assert data["is_orientable_with_form"] is True


def test_service_serializer_is_not_orientable_with_form_when_not_orientable():
    service = make_published_service()
    service.contact_email = ""
    service.structure.disable_orientation_form = True
    service.structure.save()
    service.save()

    mode = CoachOrientationMode.objects.get(value="formulaire-dora")
    service.coach_orientation_modes.add(mode)

    assert service.is_orientable() is False

    data = ServiceSerializer(service).data
    assert data["is_orientable_with_form"] is False


def test_service_serializer_is_not_orientable_with_form_without_dora_mode(
    orientable_service_via_dora_form,
):
    service = orientable_service_via_dora_form

    assert service.is_orientable() is True
    assert (
        service.coach_orientation_modes.filter(value="formulaire-dora").exists()
        is False
    )

    data = ServiceSerializer(service).data
    assert data["is_orientable_with_form"] is False


def test_service_serializer_is_orientable_with_form_when_ft_whitelisted(
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
    assert data["is_orientable_with_form"] is True


def test_average_orientation_response_delay_days_none_when_no_orientations():
    service = make_published_service()
    data = ServiceSerializer(service).data
    assert data["average_orientation_response_delay_days"] is None


def test_average_orientation_response_delay_days_none_when_only_pending_orientations():
    service = make_published_service()
    now = timezone.now()
    make_orientation(
        service=service,
        status=OrientationStatus.PENDING,
        creation_date=now - timedelta(days=5),
        processing_date=None,
    )
    data = ServiceSerializer(service).data
    assert data["average_orientation_response_delay_days"] is None


def test_average_orientation_response_delay_days_single_orientation():
    service = make_published_service()
    creation = timezone.now() - timedelta(days=10)
    processing = creation + timedelta(days=3)
    make_orientation(
        service=service,
        status=OrientationStatus.ACCEPTED,
        creation_date=creation,
        processing_date=processing,
    )
    data = ServiceSerializer(service).data
    assert data["average_orientation_response_delay_days"] == 3


def test_average_orientation_response_delay_days_average_of_multiple_orientations():
    service = make_published_service()
    base = timezone.now() - timedelta(days=30)
    make_orientation(
        service=service,
        status=OrientationStatus.ACCEPTED,
        creation_date=base,
        processing_date=base + timedelta(days=2),
    )
    make_orientation(
        service=service,
        status=OrientationStatus.REJECTED,
        creation_date=base - timedelta(days=10),
        processing_date=base - timedelta(days=10) + timedelta(days=4),
    )
    data = ServiceSerializer(service).data
    # (2 + 4) / 2 = 3
    assert data["average_orientation_response_delay_days"] == 3


def test_average_orientation_response_delay_days_rounds_to_nearest_integer():
    service = make_published_service()
    base = timezone.now() - timedelta(days=20)
    make_orientation(
        service=service,
        status=OrientationStatus.ACCEPTED,
        creation_date=base,
        processing_date=base + timedelta(days=1),
    )
    make_orientation(
        service=service,
        status=OrientationStatus.ACCEPTED,
        creation_date=base - timedelta(days=5),
        processing_date=base - timedelta(days=5) + timedelta(days=2),
    )
    data = ServiceSerializer(service).data
    # (1 + 2) / 2 = 1.5 -> round to 2
    assert data["average_orientation_response_delay_days"] == 2


def test_average_orientation_response_delay_days_only_counts_this_service():
    service = make_published_service()
    other_service = make_published_service()
    creation = timezone.now() - timedelta(days=10)
    make_orientation(
        service=service,
        status=OrientationStatus.ACCEPTED,
        creation_date=creation,
        processing_date=creation + timedelta(days=2),
    )
    make_orientation(
        service=other_service,
        status=OrientationStatus.ACCEPTED,
        creation_date=creation,
        processing_date=creation + timedelta(days=10),
    )
    data = ServiceSerializer(service).data
    assert data["average_orientation_response_delay_days"] == 2


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


def test_disabled_dora_form_di_structure_serializer_fields():
    item = baker.make(
        "structures.DisabledDoraFormDIStructure",
        source="foobar",
        structure_id="structure-1",
        comment="Commentaire",
    )

    data = DisabledDoraFormDIStructureSerializer(item).data

    assert data == {
        "source": "foobar",
        "structure_id": "structure-1",
    }
