import importlib

import pytest
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from model_bakery import baker

from dora.core.test_utils import make_model, make_service, make_structure
from dora.services.enums import ServiceStatus
from dora.services.models import (
    Service,
    ServiceCategory,
    ServiceModel,
    ServiceSubCategory,
    UpdateFrequency,
    validate_unique_form_names,
)
from dora.services.utils import update_sync_checksum

DUMMY_SERVICE = {"name": "Mon service"}


def test_superuser_can_create_model_from_others_service(api_client):
    user = baker.make("users.User", is_valid=True, is_staff=True)
    struct = make_structure()
    service = make_service(status=ServiceStatus.PUBLISHED)
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/models/",
        {"structure": struct.slug, "service": service.slug, **DUMMY_SERVICE},
    )
    assert 201 == response.status_code


def test_everybody_can_see_models(api_client):
    service = make_model()
    response = api_client.get("/models/")

    assert 200 == response.status_code
    assert service.slug in [s["slug"] for s in response.data]


def test_models_not_visible_in_service_lists(api_client):
    service = make_model()
    response = api_client.get("/services/")

    assert 200 == response.status_code
    assert service.slug not in [s["slug"] for s in response.data]


def test_is_model_param_is_true_in_models(api_client):
    service = make_model()
    response = api_client.get(f"/models/{service.slug}/")

    assert 200 == response.status_code
    assert response.data["is_model"] is True


def test_is_model_param_is_false_in_services(api_client):
    service = make_service(status=ServiceStatus.PUBLISHED)
    response = api_client.get(f"/services/{service.slug}/")

    assert 200 == response.status_code
    assert response.data["is_model"] is False


def test_cant_set_is_model_param_on_service(api_client):
    user = baker.make("users.User", is_valid=True)
    struct = make_structure(user)
    service = make_service(structure=struct)
    api_client.force_authenticate(user=user)
    response = api_client.patch(f"/services/{service.slug}/", {"is_model": True})

    assert 200 == response.status_code

    service.refresh_from_db()

    assert service.is_model is False


def test_cant_unset_is_model_param_on_model(api_client):
    user = baker.make("users.User", is_valid=True)
    struct = make_structure(user)
    model = make_model(structure=struct)
    api_client.force_authenticate(user=user)
    response = api_client.patch(f"/models/{model.slug}/", {"is_model": False})

    assert 200 == response.status_code

    model.refresh_from_db()

    assert model.is_model is True


def test_can_create_model_from_scratch(api_client):
    user = baker.make("users.User", is_valid=True)
    struct = make_structure(user)
    api_client.force_authenticate(user=user)
    response = api_client.post("/models/", {"structure": struct.slug, **DUMMY_SERVICE})

    assert 201 == response.status_code

    ServiceModel.objects.get(slug=response.data["slug"])


def test_can_create_model_from_my_service(api_client):
    user = baker.make("users.User", is_valid=True)
    struct = make_structure(user)
    service = make_service(status=ServiceStatus.PUBLISHED, structure=struct)
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/models/",
        {"structure": struct.slug, "service": service.slug, **DUMMY_SERVICE},
    )

    assert 201 == response.status_code

    service = ServiceModel.objects.get(slug=response.data["slug"])

    assert service.structure.pk == struct.pk


def test_create_model_from_service_becomes_ancestor(api_client):
    user = baker.make("users.User", is_valid=True)
    struct = make_structure(user)
    service = make_service(status=ServiceStatus.PUBLISHED, structure=struct)
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/models/",
        {"structure": struct.slug, "service": service.slug, **DUMMY_SERVICE},
    )

    assert 201 == response.status_code

    model = ServiceModel.objects.get(slug=response.data["slug"])

    assert service.structure.pk == struct.pk

    service.refresh_from_db()

    assert service.model == model
    assert service.last_sync_checksum == model.sync_checksum


def test_cant_create_model_from_others_service(api_client):
    user = baker.make("users.User", is_valid=True)
    struct = make_structure(user)
    service = make_service(status=ServiceStatus.PUBLISHED)

    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/models/",
        {"structure": struct.slug, "service": service.slug, **DUMMY_SERVICE},
    )

    assert 403 == response.status_code


def test_can_create_service_from_any_model(api_client):
    user = baker.make("users.User", is_valid=True)
    struct = make_structure(user)
    model = make_model(structure=struct)
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/services/",
        {"structure": struct.slug, "model": model.slug, **DUMMY_SERVICE},
    )
    assert 201 == response.status_code

    slug = response.data["slug"]
    service = Service.objects.get(slug=slug)

    assert service.structure.pk == struct.pk
    assert service.model == model


def test_manager_can_create_model_from_service_in_its_dept(api_client):
    user = baker.make("users.User", is_valid=True, is_manager=True, departments=["31"])
    struct_src = make_structure(department="31")
    struct_dest = make_structure(department="31")
    service = make_service(status=ServiceStatus.PUBLISHED, structure=struct_src)
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/models/",
        {"structure": struct_dest.slug, "service": service.slug, **DUMMY_SERVICE},
    )

    assert 201 == response.status_code


def test_manager_cant_create_model_from_service_outside_its_dept(api_client):
    user = baker.make("users.User", is_valid=True, is_manager=True, departments=["31"])
    struct_src = make_structure(department="44")
    struct_dest = make_structure(department="31")
    service = make_service(status=ServiceStatus.PUBLISHED, structure=struct_src)
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/models/",
        {"structure": struct_dest.slug, "service": service.slug, **DUMMY_SERVICE},
    )

    assert 403 == response.status_code


def test_manager_cant_create_model_in_struct_outside_its_dept(api_client):
    user = baker.make("users.User", is_valid=True, is_manager=True, departments=["31"])
    struct_src = make_structure(department="31")
    struct_dest = make_structure(department="44")
    service = make_service(status=ServiceStatus.PUBLISHED, structure=struct_src)
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/models/",
        {"structure": struct_dest.slug, "service": service.slug, **DUMMY_SERVICE},
    )

    assert 403 == response.status_code


def test_update_model_and_update_all_linked_services(api_client):
    service_name = "Nom du service"
    new_model_name = "Nouveau nom du modèle"

    # ÉTANT DONNÉ un modèle lié à un service
    user = baker.make("users.User", is_valid=True)
    struct = make_structure(user)
    model = make_model(structure=struct, name="Nom du modèle")
    service = make_service(
        model=model,
        structure=struct,
        name=service_name,
        status=ServiceStatus.PUBLISHED,
    )

    # QUAND je mets à jour le modèle en demandant la mise à jour des services associés
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        f"/models/{model.slug}/",
        {"name": new_model_name, "update_all_services": "true"},
    )

    assert 200 == response.status_code

    service.refresh_from_db()

    # ALORS le service est mise à jour avec le nouveau nom du modèle
    # nit: ou ajouter le commentaire dans la clause assert (1 pierre, 2 coups)
    assert service.name == new_model_name, (
        "le service doit être mis à jour avec le nouveau nom du modèle"
    )


def test_update_model_and_update_only_linked_services(api_client):
    service_name_1 = "Nom du service 1"
    service_name_2 = "Nom du service 2"
    new_model_name = "Nouveau nom du modèle"

    user = baker.make("users.User", is_valid=True)
    struct = make_structure(user)

    # ÉTANT DONNÉ un service lié à un modèle
    model = make_model(structure=struct, name="Nom du modèle")
    service_1 = make_service(
        model=model,
        structure=struct,
        name=service_name_1,
        status=ServiceStatus.PUBLISHED,
    )
    # ET un service non-lié à un modèle
    service_2 = make_service(
        model=None,
        structure=struct,
        name=service_name_2,
        status=ServiceStatus.PUBLISHED,
    )

    # QUAND je mets à jour le modèle en demandant la mise à jour des services associés
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        f"/models/{model.slug}/",
        {"name": new_model_name, "update_all_services": "true"},
    )

    assert 200 == response.status_code

    service_1.refresh_from_db()
    service_2.refresh_from_db()

    # ALORS seul le service associé au modèle est associé
    assert service_1.name == new_model_name
    assert service_2.name == service_name_2


@pytest.mark.parametrize(
    "update_all_services, expected_name",
    [("true", "Nom du modèle"), ("false", "Nom du service")],
)
def test_update_model_without_changes_resyncs_linked_services_only_if_requested(
    api_client, update_all_services, expected_name
):
    # ÉTANT DONNÉ un service lié à un modèle, en retard sur celui-ci
    user = baker.make("users.User", is_valid=True)
    struct = make_structure(user)
    model = make_model(structure=struct, name="Nom du modèle")
    service = make_service(
        model=model,
        structure=struct,
        name="Nom du service",
        status=ServiceStatus.PUBLISHED,
    )

    # QUAND j'enregistre le modèle sans le modifier
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        f"/models/{model.slug}/",
        {"name": model.name, "update_all_services": update_all_services},
    )

    assert 200 == response.status_code

    # ALORS le service n'est resynchronisé que si la mise à jour a été demandée
    service.refresh_from_db()
    model.refresh_from_db()
    assert service.name == expected_name
    if update_all_services == "true":
        assert service.last_sync_checksum == model.sync_checksum


def test_update_service_from_model(api_client):
    service_name = "Nom du service"
    service_slug = "nom-du-service"
    model_name = "Nouveau nom du modèle"

    # ÉTANT DONNÉ un modèle lié à un service
    user = baker.make("users.User", is_valid=True)
    struct = make_structure(user)
    model = make_model(structure=struct, name=model_name)
    service = make_service(
        model=model,
        structure=struct,
        slug=service_slug,
        name=service_name,
        status=ServiceStatus.PUBLISHED,
    )
    assert service.name == service_name

    # QUAND je demande la mise à jour du service via son modèle
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/services/update-from-model/",
        {
            "services": [service_slug],
        },
    )
    assert 204 == response.status_code

    service.refresh_from_db()

    # ALORS le service a été mis à jour
    assert service.name == model_name, "le nom du service doit être mis à jour"


def test_update_service_from_model_m2m(api_client):
    service_name = "Nom du service"
    service_slug = "nom-du-service"
    model_name = "Nouveau nom du modèle"
    model_slug = "nouveau-nom-du-modele"
    user = baker.make("users.User", is_valid=True)

    # ÉTANT DONNÉ un service lié à un modèle avec des champs custom et M2M
    struct = make_structure(user)
    global_condition1 = baker.make("AccessCondition", structure=None)
    struct_condition1 = baker.make("AccessCondition", structure=struct)

    model = make_model(
        structure=struct,
        name=model_name,
        slug=model_slug,
    )
    # SYNC_CUSTOM_M2M_FIELDS
    model.access_conditions.add(global_condition1)
    model.access_conditions.add(struct_condition1)

    # SYNC_M2M_FIELDS
    model.categories.add(ServiceCategory.objects.get(value="numerique"))
    model.subcategories.add(
        ServiceSubCategory.objects.get(
            value="choisir-un-metier--confirmer-son-choix-de-metier"
        )
    )

    service = make_service(
        model=model,
        structure=struct,
        slug=service_slug,
        name=service_name,
        status=ServiceStatus.PUBLISHED,
    )

    assert sorted(service.access_conditions.values_list("id", flat=True)) != sorted(
        model.access_conditions.values_list("id", flat=True)
    )
    assert sorted(service.categories.values_list("value", flat=True)) != sorted(
        model.categories.values_list("value", flat=True)
    )
    assert sorted(service.subcategories.values_list("value", flat=True)) != sorted(
        model.subcategories.values_list("value", flat=True)
    )

    # QUAND je demande la mise à jour du service via son modèle
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/services/update-from-model/",
        {
            "services": [service_slug],
        },
    )
    service.refresh_from_db()

    # ALORS les champs custom et M2M ont été mis à jour
    assert 204 == response.status_code
    assert sorted(service.access_conditions.values_list("id", flat=True)) == sorted(
        model.access_conditions.values_list("id", flat=True)
    )
    assert sorted(service.categories.values_list("value", flat=True)) == sorted(
        model.categories.values_list("value", flat=True)
    )
    assert sorted(service.subcategories.values_list("value", flat=True)) == sorted(
        model.subcategories.values_list("value", flat=True)
    )


def test_update_service_from_model_wrong_permission(api_client):
    service_name = "Nom du service"
    service_slug = "nom-du-service"
    model_name = "Nouveau nom du modèle"

    # ÉTANT DONNÉ un modèle lié à un service
    user = baker.make("users.User", is_valid=True)

    struct = make_structure(user)
    model = make_model(structure=struct, name=model_name)
    service = make_service(
        model=model,
        structure=struct,
        slug=service_slug,
        name=service_name,
        status=ServiceStatus.PUBLISHED,
    )

    assert service.name == service_name

    # ET un utilisateur n'appartenant pas à la structure
    user2 = baker.make("users.User", is_valid=True)

    # QUAND je demande la mise à jour du service via son modèle avec un utilisateur n'appartenant pas à la structure
    api_client.force_authenticate(user=user2)
    response = api_client.post(
        "/services/update-from-model/",
        {
            "services": [service_slug],
        },
    )

    # ALORS je ne suis pas autorisé à faire la mise à jour
    assert 403 == response.status_code

    # ET le service n'a pas été mis à jour
    service.refresh_from_db()

    assert service.name != model_name, "le service ne doit pas avoir été mis à jour"


def test_reject_update_service_from_model(api_client):
    service_name = "Nom du service"
    service_slug = "nom-du-service"
    model_name = "Nouveau nom du modèle"
    model_slug = "nouveau-nom-du-modele"

    # ÉTANT DONNÉ un modèle lié à un service
    user = baker.make("users.User", is_valid=True)
    struct = make_structure(user)
    model = make_model(structure=struct, name=model_name, slug=model_slug)
    service = make_service(
        model=model,
        structure=struct,
        slug=service_slug,
        name=service_name,
        status=ServiceStatus.PUBLISHED,
    )
    assert service_name == service_name

    # QUAND je refuse la mise à jour du service via son modèle
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/services/reject-update-from-model/",
        {
            "data": [{"model_slug": model_slug, "service_slug": service_slug}],
        },
    )
    assert 204 == response.status_code

    service.refresh_from_db()

    # ALORS le service n'a été mis à jour
    assert service.name != model_name
    # mais son checksum a été mis à jour
    assert service.last_sync_checksum == model.sync_checksum


def test_reject_update_service_from_model_non_existing_model(api_client):
    service_name = "Nom du service"
    service_slug = "nom-du-service"
    model_name = "Nouveau nom du modèle"
    model_slug = "nouveau-nom-du-modele"

    # ÉTANT DONNÉ un modèle lié à un service
    user = baker.make("users.User", is_valid=True)
    struct = make_structure(user)
    model = make_model(structure=struct, name=model_name, slug=model_slug)
    service = make_service(
        model=model,
        structure=struct,
        slug=service_slug,
        name=service_name,
        status=ServiceStatus.PUBLISHED,
    )
    assert service.name == service_name

    # QUAND je refuse la mise à jour du service via son modèle
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/services/reject-update-from-model/",
        {
            "data": [{"model_slug": "non-existing-slug", "service_slug": service_slug}],
        },
    )
    assert 204 == response.status_code

    service.refresh_from_db()

    # ALORS le service n'a été mis à jour
    assert service.name != model_name
    assert service.last_sync_checksum != model.sync_checksum


def test_reject_update_service_from_model_non_existing_service(api_client):
    service_name = "Nom du service"
    service_slug = "nom-du-service"
    model_name = "Nouveau nom du modèle"
    model_slug = "nouveau-nom-du-modele"

    # ÉTANT DONNÉ un modèle lié à un service
    user = baker.make("users.User", is_valid=True)
    struct = make_structure(user)
    model = make_model(structure=struct, name=model_name, slug=model_slug)
    service = make_service(
        model=model,
        structure=struct,
        slug=service_slug,
        name=service_name,
        status=ServiceStatus.PUBLISHED,
    )
    assert service.name == service_name

    # QUAND je refuse la mise à jour du service via son modèle
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/services/reject-update-from-model/",
        {
            "data": [{"model_slug": model_slug, "service_slug": "non-existing-slug"}],
        },
    )
    assert 204 == response.status_code

    service.refresh_from_db()

    # ALORS le service n'a été mis à jour
    assert service.name != model_name
    assert service.last_sync_checksum != model.sync_checksum


def test_cant_instantiate_a_service(api_client):
    user = baker.make("users.User", is_valid=True)
    struct = make_structure(user)
    service = make_service(structure=struct, status=ServiceStatus.PUBLISHED)
    dest_struct = make_structure(user)
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/services/",
        {"structure": dest_struct.slug, "model": service.slug, **DUMMY_SERVICE},
    )
    assert 400 == response.status_code
    assert response.data["model"][0]["code"] == "does_not_exist"


def test_can_instantiate_models_in_my_structures(api_client):
    user = baker.make("users.User", is_valid=True)
    model = make_model()
    dest_struct = make_structure(user)
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/services/",
        {"structure": dest_struct.slug, "model": model.slug, **DUMMY_SERVICE},
    )

    assert 201 == response.status_code


def test_cant_instantiate_models_in_other_structures(api_client):
    model = make_model()
    dest_struct = make_structure()
    user = baker.make("users.User", is_valid=True)
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/services/",
        {"structure": dest_struct.slug, "model": model.slug, **DUMMY_SERVICE},
    )
    assert 403 == response.status_code


def test_is_orientable_with_orientation_form():
    # fix : les services étaient orientables même si le formulaire
    # d'orientation était désactivé sur la structure source.
    structure = make_structure(
        baker.make("users.User", is_valid=True),
        disable_orientation_form=False,
    )
    service = make_service(
        structure=structure,
        status=ServiceStatus.PUBLISHED,
        contact_email="test@test.com",
    )

    assert service.is_orientable()

    structure.disable_orientation_form = True

    assert not service.is_orientable()


def test_validate_unique_form_names_rejects_duplicate_file_names():
    # Deux clés S3 distinctes peuvent pointer vers le même nom de fichier :
    # c'est ce nom, seul affiché, qui doit rester unique.
    with pytest.raises(ValidationError):
        validate_unique_form_names(["prod/42/dossier.pdf", "prod/51/dossier.pdf"])


def test_validate_unique_form_names_accepts_distinct_file_names():
    validate_unique_form_names(["prod/42/dossier.pdf", "prod/42/attestation.pdf"])


def test_service_forms_reject_duplicate_file_names():
    service = make_service(forms=["prod/42/dossier.pdf", "prod/42/dossier.pdf"])

    with pytest.raises(ValidationError) as excinfo:
        service.full_clean()

    assert "forms" in excinfo.value.error_dict


def test_service_api_rejects_duplicate_form_names(api_client):
    user = baker.make("users.User", is_valid=True)
    structure = make_structure(user)
    service = make_service(structure=structure, status=ServiceStatus.DRAFT)
    api_client.force_authenticate(user=user)

    response = api_client.patch(
        f"/services/{service.slug}/",
        {"forms": ["prod/42/dossier.pdf", "prod/51/dossier.pdf"]},
    )

    assert 400 == response.status_code
    assert "forms" in response.data


recompute_migration = importlib.import_module(
    "dora.services.migrations.0021_recompute_sync_checksums_update_frequency"
)


def test_recompute_sync_checksums_matches_application_checksum():
    # ÉTANT DONNÉ un modèle dont l'empreinte a été calculée avec une ancienne formule
    struct = make_structure()
    model = make_model(structure=struct, update_frequency=UpdateFrequency.EVERY_MONTH)
    # ET deux copies, l'une à jour et l'autre avec des modifications en attente
    up_to_date = make_service(model=model, structure=struct)
    outdated = make_service(model=model, structure=struct)
    ServiceModel.objects.filter(pk=model.pk).update(sync_checksum="ancienne")
    Service.objects.filter(pk=up_to_date.pk).update(last_sync_checksum="ancienne")
    Service.objects.filter(pk=outdated.pk).update(last_sync_checksum="obsolete")

    # QUAND la migration recalcule les empreintes
    recompute_migration.recompute_sync_checksums(django_apps, None)

    # ALORS l'empreinte du modèle est celle que l'application calcule
    model.refresh_from_db()
    assert model.sync_checksum == update_sync_checksum(model)
    # ET seule la copie qui était à jour la suit
    up_to_date.refresh_from_db()
    outdated.refresh_from_db()
    assert up_to_date.last_sync_checksum == model.sync_checksum
    assert outdated.last_sync_checksum == "obsolete"
