from data_inclusion.schema.v1 import ModeMobilisation, PersonneMobilisatrice

from dora.core.test_utils import make_model, make_service, make_structure, make_user
from dora.services.enums import ServiceStatus
from dora.services.mobilisation import sync_mobilisation_fields
from dora.services.models import BeneficiaryAccessMode, CoachOrientationMode
from dora.services.utils import synchronize_service_from_model


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

    sync_mobilisation_fields(service)
    service.refresh_from_db()

    assert service.mobilisation_modes == [
        ModeMobilisation.ENVOYER_UN_COURRIEL.value,
        ModeMobilisation.SE_PRESENTER.value,
        ModeMobilisation.TELEPHONER.value,
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

    sync_mobilisation_fields(service)
    service.refresh_from_db()

    assert service.mobilisation_modes == [
        ModeMobilisation.UTILISER_LIEN_MOBILISATION.value,
    ]
    assert service.mobilisation_link == "https://example.com/coach-form"


def test_sync_mobilisation_fields_maps_adhesion_form_with_beneficiary_link():
    service = make_service(
        beneficiaries_access_modes_external_form_link=(
            "https://example.com/beneficiary-form"
        ),
    )
    service.beneficiaries_access_modes.set(
        BeneficiaryAccessMode.objects.filter(value="completer-le-formulaire-dadhesion")
    )

    sync_mobilisation_fields(service)
    service.refresh_from_db()

    assert service.mobilisation_modes == [
        ModeMobilisation.UTILISER_LIEN_MOBILISATION.value,
    ]
    assert service.mobilisation_link == "https://example.com/beneficiary-form"


def test_sync_mobilisation_fields_maps_formulaire_dora_with_dora_link():
    service = make_service()
    service.coach_orientation_modes.set(
        CoachOrientationMode.objects.filter(value="formulaire-dora")
    )

    sync_mobilisation_fields(service)
    service.refresh_from_db()

    assert service.mobilisation_modes == [
        ModeMobilisation.UTILISER_LIEN_MOBILISATION.value,
    ]
    assert service.mobilisation_link == service.get_dora_form_url()


def test_sync_mobilisation_fields_skips_form_mode_without_link():
    service = make_service()
    service.coach_orientation_modes.set(
        CoachOrientationMode.objects.filter(value="completer-le-formulaire-dadhesion")
    )

    sync_mobilisation_fields(service)
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

    sync_mobilisation_fields(service)
    service.refresh_from_db()

    assert service.mobilisation_details == (
        "Précision accompagnateur, Précision bénéficiaire"
    )
    assert service.mobilisation_modes is None


def test_sync_mobilisation_fields_professionnel_overrides_usagers():
    service = make_service()
    service.coach_orientation_modes.set(
        CoachOrientationMode.objects.filter(value="envoyer-un-mail")
    )
    service.beneficiaries_access_modes.set(
        BeneficiaryAccessMode.objects.filter(value__in=["telephoner", "professionnel"])
    )

    sync_mobilisation_fields(service)
    service.refresh_from_db()

    assert service.mobilisable_by == [PersonneMobilisatrice.PROFESSIONNELS.value]
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
