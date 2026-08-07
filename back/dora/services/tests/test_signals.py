"""Double écriture `Service.kinds` → `Service.kind` (`dora.services.signals`)."""

from django.db import connection
from django.test.utils import CaptureQueriesContext

from dora.core.test_utils import make_model, make_service, make_structure, make_user
from dora.services.enums import ServiceStatus
from dora.services.models import Service, ServiceKind
from dora.services.utils import (
    instantiate_service_from_model,
    synchronize_service_from_model,
)


def kinds(*values):
    return ServiceKind.objects.filter(value__in=values)


def reloaded_kind(service):
    return Service._base_manager.get(pk=service.pk).kind


def test_set_derives_the_kind():
    service = make_service()

    service.kinds.set(kinds("information", "aide-financiere"))

    assert reloaded_kind(service) == "aide-financiere"


def test_in_memory_instance_is_up_to_date():
    # sans quoi un `save()` ultérieur du même objet réécrirait une valeur périmée
    service = make_service()

    service.kinds.set(kinds("formation"))
    service.save()

    assert service.kind == "formation"
    assert reloaded_kind(service) == "formation"


def test_add_and_remove_recompute_the_kind():
    service = make_service()
    service.kinds.set(kinds("information"))

    service.kinds.add(*kinds("aide-materielle"))
    assert reloaded_kind(service) == "aide-materielle"

    service.kinds.remove(*kinds("aide-materielle"))
    assert reloaded_kind(service) == "information"


def test_clear_empties_the_kind():
    service = make_service()
    service.kinds.set(kinds("atelier"))

    service.kinds.clear()

    assert reloaded_kind(service) == ""


def test_service_models_are_synchronized_too():
    # `Service.objects` exclut les modèles : la synchronisation passe par `_base_manager`
    model = make_model()

    model.kinds.set(kinds("atelier", "formation"))

    assert reloaded_kind(model) == "formation"


def test_service_instantiated_from_a_model_inherits_the_kind():
    model = make_model()
    model.kinds.set(kinds("accompagnement", "aide-financiere"))

    service = instantiate_service_from_model(model, make_structure(), make_user())

    assert reloaded_kind(service) == "aide-financiere"


def test_service_synchronized_from_its_model_follows_the_kind():
    # `views.py` enchaîne `synchronize_service_from_model()` puis `service.save()` :
    # l'instance en mémoire doit déjà porter le nouveau type
    model = make_model()
    model.kinds.set(kinds("information"))
    service = instantiate_service_from_model(model, make_structure(), make_user())
    model.kinds.set(kinds("aide-financiere"))

    synchronize_service_from_model(service, model)
    service.save()

    assert reloaded_kind(service) == "aide-financiere"


def test_reverse_add_derives_the_kind():
    service = make_service()

    ServiceKind.objects.get(value="formation").service_set.add(service)

    assert reloaded_kind(service) == "formation"


def test_reverse_remove_recomputes_the_kind():
    service = make_service()
    service.kinds.set(kinds("information", "formation"))

    ServiceKind.objects.get(value="formation").service_set.remove(service)

    assert reloaded_kind(service) == "information"


def test_reverse_clear_empties_the_kind():
    # les liens sont supprimés avant `post_clear` : les services concernés sont relevés
    # en amont, sur `pre_clear`
    service = make_service()
    other = make_service()
    kind = ServiceKind.objects.get(value="formation")
    service.kinds.set([kind])
    other.kinds.set([kind, *kinds("information")])

    kind.service_set.clear()

    assert reloaded_kind(service) == ""
    assert reloaded_kind(other) == "information"


def test_deleting_a_service_kind_recomputes_the_kind():
    # la table de liaison part en cascade sans émettre `m2m_changed`
    service = make_service()
    other = make_service()
    kind = ServiceKind.objects.get(value="formation")
    service.kinds.set([kind])
    other.kinds.set([kind, *kinds("information")])

    kind.delete()

    assert reloaded_kind(service) == ""
    assert reloaded_kind(other) == "information"


def test_deleting_service_kinds_in_bulk_recomputes_the_kind():
    service = make_service()
    service.kinds.set(kinds("formation", "information"))

    kinds("formation").delete()

    assert reloaded_kind(service) == "information"


def test_editing_only_the_label_does_not_resync(django_assert_num_queries):
    # `accompagnement` compte des dizaines de milliers de services liés en production :
    # corriger un libellé depuis l'admin ne doit pas tous les recalculer
    kind = ServiceKind.objects.get(value="formation")
    for _ in range(3):
        make_service().kinds.set([kind])

    kind.label = "Formation professionnelle"
    with django_assert_num_queries(2):  # relecture de `value` + UPDATE du référentiel
        kind.save()


def test_resync_does_not_scale_with_the_number_of_services(django_assert_num_queries):
    def rename_kind(value, service_count):
        kind = ServiceKind.objects.create(value=value, label=value)
        for _ in range(service_count):
            make_service().kinds.set([kind])
        kind.value = f"{value}-bis"

        with CaptureQueriesContext(connection) as queries:
            kind.save()
        return len(queries)

    assert rename_kind("un", 1) == rename_kind("plusieurs", 6)


def test_renaming_a_service_kind_recomputes_the_kind():
    service = make_service()
    kind = ServiceKind.objects.get(value="formation")
    service.kinds.set([kind])
    assert reloaded_kind(service) == "formation"

    # sortie du référentiel DI : le service n'a plus de type dérivable
    kind.value = "plus-utilise"
    kind.save()

    assert reloaded_kind(service) == ""


def test_write_through_the_api(api_client):
    user = make_user(is_valid=True)
    structure = make_structure(user=user)
    api_client.force_authenticate(user=user)

    response = api_client.post(
        "/services/",
        {
            "name": "Un service",
            "structure": structure.slug,
            "kinds": ["information", "formation"],
        },
    )

    assert response.status_code == 201
    assert Service.objects.get(slug=response.data["slug"]).kind == "formation"


def test_update_through_the_api(api_client):
    user = make_user(is_valid=True)
    structure = make_structure(user=user)
    service = make_service(structure=structure, status=ServiceStatus.PUBLISHED)
    service.kinds.set(kinds("information"))
    api_client.force_authenticate(user=user)

    response = api_client.patch(
        f"/services/{service.slug}/", {"kinds": ["aide-financiere"]}
    )

    assert response.status_code == 200
    assert reloaded_kind(service) == "aide-financiere"
