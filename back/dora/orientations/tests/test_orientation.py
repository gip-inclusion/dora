from dora.core.test_utils import make_orientation, make_published_service


def test_dora_service_orientation_get_service_address_line():
    service = make_published_service(
        address1="6 Boulevard St Denis",
        address2="Plateforme de l'inclusion",
        postal_code="75010",
        # on ne peut pas spécifier de ville dans le contexte d'un test
    )
    orientation = make_orientation(service=service)
    assert (
        orientation.get_service_address_line()
        == "6 Boulevard St Denis Plateforme de l'inclusion - 75010"
    )


def test_di_service_orientation_get_service_address_line():
    orientation = make_orientation(
        service=None,
        di_service_id="di_service_id",
        di_service_address_line="6 Boulevard St Denis Plateforme de l'inclusion - 75010 Paris",
    )
    assert (
        orientation.get_service_address_line()
        == "6 Boulevard St Denis Plateforme de l'inclusion - 75010 Paris"
    )
