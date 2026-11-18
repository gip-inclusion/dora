import importlib

from django.apps import apps as django_apps

from dora.core.test_utils import make_model, make_service
from dora.services.enums import ServiceStatus
from dora.services.models import CoachOrientationMode, Service
from dora.services.utils import update_sync_checksum

recompute_migration = importlib.import_module(
    "dora.services.migrations.0027_recompute_mobilisation_link"
)

MOBILISATION_LINK_MODE = "utiliser-lien-mobilisation"
OTHER_MODE = "envoyer-un-courriel"

LINK = "https://example.com/mobilisation"
OTHER_LINK = "https://example.com/autre"

EMPTY_LINKS = {
    "appointment_link": "",
    "online_form": "",
    "coach_orientation_modes_external_form_link": "",
    "beneficiaries_access_modes_external_form_link": "",
}


def make_dora_form_service(with_dora_form=True, **kwargs):
    service = make_service(status=ServiceStatus.PUBLISHED, **{**EMPTY_LINKS, **kwargs})
    if with_dora_form:
        service.coach_orientation_modes.add(
            CoachOrientationMode.objects.get(value="formulaire-dora")
        )
    return service


def run_migration():
    # Les deux opérations de la migration, dans l'ordre déclaré.
    recompute_migration.clear_mobilisation_links(django_apps, None)
    recompute_migration.recompute_sync_checksums(django_apps, None)


def test_link_is_removed_when_the_first_filled_field_matches():
    service = make_dora_form_service(appointment_link=LINK, mobilisation_link=LINK)

    run_migration()

    service.refresh_from_db()
    assert service.mobilisation_link is None


def test_link_is_kept_when_the_first_filled_field_differs():
    service = make_dora_form_service(
        appointment_link=OTHER_LINK, mobilisation_link=LINK
    )

    run_migration()

    service.refresh_from_db()
    assert service.mobilisation_link == LINK


def test_link_is_kept_when_a_higher_priority_field_differs_even_if_a_lower_priority_field_matches():
    service = make_dora_form_service(
        appointment_link=OTHER_LINK,
        online_form=LINK,
        mobilisation_link=LINK,
    )

    run_migration()

    service.refresh_from_db()
    assert service.mobilisation_link == LINK


def test_empty_fields_are_skipped_in_favour_of_the_next_one():
    service = make_dora_form_service(online_form=LINK, mobilisation_link=LINK)

    run_migration()

    service.refresh_from_db()
    assert service.mobilisation_link is None


def test_link_is_kept_when_no_field_is_filled():
    service = make_dora_form_service(mobilisation_link=LINK)

    run_migration()

    service.refresh_from_db()
    assert service.mobilisation_link == LINK


def test_link_is_kept_without_the_dora_form_mode():
    service = make_dora_form_service(
        with_dora_form=False,
        appointment_link=LINK,
        mobilisation_link=LINK,
    )

    run_migration()

    service.refresh_from_db()
    assert service.mobilisation_link == LINK


def test_services_without_a_link_are_left_untouched():
    service = make_dora_form_service(
        appointment_link=LINK,
        mobilisation_link=None,
        mobilisation_modes=[OTHER_MODE, MOBILISATION_LINK_MODE],
    )

    run_migration()

    service.refresh_from_db()
    assert service.mobilisation_link is None
    assert service.mobilisation_modes == [OTHER_MODE, MOBILISATION_LINK_MODE]


def test_mobilisation_link_mode_is_removed_with_the_link():
    service = make_dora_form_service(
        appointment_link=LINK,
        mobilisation_link=LINK,
        mobilisation_modes=[OTHER_MODE, MOBILISATION_LINK_MODE],
    )

    run_migration()

    service.refresh_from_db()
    assert service.mobilisation_link is None
    assert service.mobilisation_modes == [OTHER_MODE]


def test_mobilisation_link_mode_is_kept_when_the_link_is_kept():
    service = make_dora_form_service(
        appointment_link=OTHER_LINK,
        mobilisation_link=LINK,
        mobilisation_modes=[MOBILISATION_LINK_MODE],
    )

    run_migration()

    service.refresh_from_db()
    assert service.mobilisation_link == LINK
    assert service.mobilisation_modes == [MOBILISATION_LINK_MODE]


def test_null_mobilisation_modes_are_normalised_to_an_empty_list():
    service = make_dora_form_service(
        appointment_link=LINK,
        mobilisation_link=LINK,
        mobilisation_modes=None,
    )

    run_migration()

    service.refresh_from_db()
    assert service.mobilisation_modes == []


def add_dora_form(service):
    service.coach_orientation_modes.add(
        CoachOrientationMode.objects.get(value="formulaire-dora")
    )
    return service


def make_dora_form_model(**kwargs):
    model = add_dora_form(make_model(**{**EMPTY_LINKS, **kwargs}))
    Service.including_models.filter(pk=model.pk).update(
        sync_checksum=update_sync_checksum(model)
    )
    model.refresh_from_db()
    return model


def test_models_are_cleared_too():
    model = make_dora_form_model(appointment_link=LINK, mobilisation_link=LINK)

    run_migration()

    model.refresh_from_db()
    assert model.mobilisation_link is None


def test_model_checksum_is_recomputed_after_the_link_is_cleared():
    model = make_dora_form_model(appointment_link=LINK, mobilisation_link=LINK)
    stale_checksum = model.sync_checksum

    run_migration()

    model.refresh_from_db()
    # L'empreinte stockée est celle que l'application calculera au prochain
    # enregistrement : aucune copie ne basculera en « modèle modifié ».
    assert model.sync_checksum != stale_checksum
    assert model.sync_checksum == update_sync_checksum(model)


def test_up_to_date_copies_follow_the_new_model_checksum():
    model = make_dora_form_model(appointment_link=LINK, mobilisation_link=LINK)
    previous = model.sync_checksum
    copy = make_dora_form_service(
        model=model,
        appointment_link=LINK,
        mobilisation_link=LINK,
        last_sync_checksum=previous,
    )

    run_migration()

    model.refresh_from_db()
    copy.refresh_from_db()
    assert copy.last_sync_checksum != previous
    assert copy.last_sync_checksum == model.sync_checksum
    assert copy.last_sync_checksum == update_sync_checksum(model)


def test_outdated_copies_keep_their_own_checksum():
    model = make_dora_form_model(appointment_link=LINK, mobilisation_link=LINK)
    copy = make_dora_form_service(
        model=model,
        appointment_link=LINK,
        mobilisation_link=LINK,
        last_sync_checksum="obsolete",
    )

    run_migration()

    model.refresh_from_db()
    # Cette copie a de vraies modifications en attente : ne pas les masquer.
    copy.refresh_from_db()
    assert copy.last_sync_checksum == "obsolete"


def test_untouched_model_checksum_is_left_alone():
    model = make_dora_form_model(appointment_link=OTHER_LINK, mobilisation_link=LINK)
    unchanged = model.sync_checksum

    run_migration()

    model.refresh_from_db()
    assert model.mobilisation_link == LINK
    assert model.sync_checksum == unchanged
