from data_inclusion.schema.v1.publics import Public as DiPublic
from model_bakery import baker

from dora.core.test_utils import make_service, make_structure
from dora.services.models import Public, Service
from dora.services.utils import TOUS_PUBLICS, compute_publics_di

FAMILLES = DiPublic.FAMILLES.value
ETUDIANTS = DiPublic.ETUDIANTS.value


def test_signal_add_writes_columns():
    service = make_service()
    service.publics.add(
        baker.make(Public, name="familles", corresponding_di_publics=[FAMILLES])
    )
    service.refresh_from_db()
    assert (service.publics_di, service.publics_precisions) == compute_publics_di(
        service
    )
    assert service.publics_di == [FAMILLES]


def test_signal_set_rewrites_columns():
    service = make_service()
    service.publics.add(
        baker.make(Public, name="familles", corresponding_di_publics=[FAMILLES])
    )
    service.publics.set(
        [baker.make(Public, name="etudiants", corresponding_di_publics=[ETUDIANTS])]
    )
    service.refresh_from_db()
    assert (service.publics_di, service.publics_precisions) == compute_publics_di(
        service
    )
    assert service.publics_di == [ETUDIANTS]


def test_signal_clear_returns_tous_publics():
    service = make_service()
    service.publics.add(
        baker.make(Public, name="familles", corresponding_di_publics=[FAMILLES])
    )
    service.publics.clear()
    service.refresh_from_db()
    assert (service.publics_di, service.publics_precisions) == ([TOUS_PUBLICS], "")


def test_signal_public_save_applies_to_all_associated_services():
    service = make_service()
    public = baker.make(Public, name="familles", corresponding_di_publics=[FAMILLES])
    service.publics.add(public)

    public.corresponding_di_publics = [ETUDIANTS]
    public.save()
    service.refresh_from_db()
    assert (service.publics_di, service.publics_precisions) == ([ETUDIANTS], "")


def test_signal_survives_later_full_save():
    # Quand on modifie les publics d'un service, il y a des fonctions invoquées après le patch qui invoque
    # service.save(). Ce test assure que la double écriture fonctionne dans ce cas
    service = make_service()
    service.publics.add(
        baker.make(Public, name="familles", corresponding_di_publics=[FAMILLES])
    )
    service.save()
    service.refresh_from_db()
    assert (service.publics_di, service.publics_precisions) == ([FAMILLES], "")


def test_update_service_model():
    service_model = baker.make(Service, is_model=True, structure=make_structure())
    service_model.publics.add(
        baker.make(Public, name="familles", corresponding_di_publics=[FAMILLES])
    )
    service_model.refresh_from_db()

    assert (
        service_model.publics_di,
        service_model.publics_precisions,
    ) == compute_publics_di(service_model)
    assert service_model.publics_di == [FAMILLES]
