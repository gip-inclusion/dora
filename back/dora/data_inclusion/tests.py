from data_inclusion.schema.v1 import ModeMobilisation, PersonneMobilisatrice
from model_bakery import baker

from .mappings import is_orientable, map_service
from .test_utils import make_di_service_data

ALL_DI_ORIENTATION_MODES = [
    ModeMobilisation.ENVOYER_UN_COURRIEL,
    ModeMobilisation.SE_PRESENTER,
    ModeMobilisation.TELEPHONER,
    ModeMobilisation.UTILISER_LIEN_MOBILISATION,
]

DI_MODES_WITHOUT_LINK = [
    ModeMobilisation.ENVOYER_UN_COURRIEL,
    ModeMobilisation.SE_PRESENTER,
    ModeMobilisation.TELEPHONER,
]


def test_map_service_modes_mobilisation_with_link_mode_and_link():
    di_service_data = make_di_service_data(
        mobilisable_par=[PersonneMobilisatrice.PROFESSIONNELS],
        modes_mobilisation=ALL_DI_ORIENTATION_MODES,
        lien_mobilisation="https://example.com",
    )
    service = map_service(di_service_data, False)

    # Le lien de mobilisation du service prime sur le formulaire DORA
    assert service["modes_mobilisation"] == [
        "envoyer-un-courriel",
        "se-presenter",
        "telephoner",
        "utiliser-lien-mobilisation",
    ]
    assert service["lien_mobilisation"] == "https://example.com"


def test_map_service_modes_mobilisation_with_link_mode_but_no_link_with_email():
    di_service_data = make_di_service_data(
        mobilisable_par=[PersonneMobilisatrice.PROFESSIONNELS],
        modes_mobilisation=ALL_DI_ORIENTATION_MODES,
        lien_mobilisation=None,
        courriel="contact@example.com",
    )
    service = map_service(di_service_data, False)

    # Le mode utiliser-lien-mobilisation est retiré faute de lien, et le
    # formulaire DORA prend le relais
    assert service["modes_mobilisation"] == [
        "envoyer-un-courriel",
        "se-presenter",
        "telephoner",
        "formulaire-dora",
    ]


def test_map_service_modes_mobilisation_with_link_mode_but_no_link_without_email():
    di_service_data = make_di_service_data(
        mobilisable_par=[PersonneMobilisatrice.PROFESSIONNELS],
        modes_mobilisation=ALL_DI_ORIENTATION_MODES,
        lien_mobilisation=None,
        courriel=None,
    )
    service = map_service(di_service_data, False)

    assert service["modes_mobilisation"] == [
        "envoyer-un-courriel",
        "se-presenter",
        "telephoner",
    ]


def test_map_service_modes_mobilisation_without_link_mode_with_email():
    di_service_data = make_di_service_data(
        mobilisable_par=[PersonneMobilisatrice.PROFESSIONNELS],
        modes_mobilisation=DI_MODES_WITHOUT_LINK,
        courriel="contact@example.com",
    )
    service = map_service(di_service_data, False)

    assert service["modes_mobilisation"] == [
        "envoyer-un-courriel",
        "se-presenter",
        "telephoner",
        "formulaire-dora",
    ]


def test_map_service_modes_mobilisation_without_link_mode_without_email():
    di_service_data = make_di_service_data(
        mobilisable_par=[PersonneMobilisatrice.PROFESSIONNELS],
        modes_mobilisation=DI_MODES_WITHOUT_LINK,
        courriel=None,
    )
    service = map_service(di_service_data, False)

    assert service["modes_mobilisation"] == [
        "envoyer-un-courriel",
        "se-presenter",
        "telephoner",
    ]


def test_map_service_modes_mobilisation_adds_professionnels_with_dora_form():
    # Un service déclaré mobilisable par les seuls usagers reste orientable par
    # les professionnels via le formulaire DORA
    di_service_data = make_di_service_data(
        mobilisable_par=[PersonneMobilisatrice.USAGERS],
        modes_mobilisation=[ModeMobilisation.TELEPHONER],
        courriel="contact@example.com",
    )
    service = map_service(di_service_data, False)

    assert service["modes_mobilisation"] == ["telephoner", "formulaire-dora"]
    assert service["mobilisable_par"] == ["usagers", "professionnels"]


def test_map_service_modes_mobilisation_when_not_provided():
    di_service_data = make_di_service_data(
        mobilisable_par=None,
        modes_mobilisation=None,
        courriel="contact@example.com",
    )
    service = map_service(di_service_data, False)

    assert service["modes_mobilisation"] == ["formulaire-dora"]
    assert service["mobilisable_par"] == ["professionnels"]


def test_map_service_modes_mobilisation_when_not_provided_without_email():
    di_service_data = make_di_service_data(
        mobilisable_par=None,
        modes_mobilisation=None,
        courriel=None,
    )
    service = map_service(di_service_data, False)

    assert service["modes_mobilisation"] is None
    assert service["mobilisable_par"] is None


def test_map_service_mobilisation_precisions():
    di_service_data = make_di_service_data(
        mobilisation_precisions="Uniquement le mardi matin",
    )
    service = map_service(di_service_data, False)

    assert service["mobilisation_precisions"] == "Uniquement le mardi matin"


def test_is_orientable_by_default():
    assert is_orientable(make_di_service_data()) is True


def test_is_orientable_when_source_is_blacklisted(settings):
    settings.NON_ORIENTABLE_DI_SOURCES = frozenset({"blacklisted-source"})

    assert is_orientable(make_di_service_data(source="blacklisted-source")) is False
    assert is_orientable(make_di_service_data(source="another-source")) is True


def test_is_not_orientable_when_siren_is_blacklisted(settings):
    di_service_data = make_di_service_data()
    di_service_data["structure"]["siret"] = (
        f"{settings.ORIENTATION_SIRENE_BLACKLIST[0]}12345"
    )

    assert is_orientable(di_service_data) is False


def test_is_orientable_without_siret():
    di_service_data = make_di_service_data()
    di_service_data["structure"]["siret"] = None

    assert is_orientable(di_service_data) is True


def test_is_not_orientable_without_email():
    assert is_orientable(make_di_service_data(courriel=None)) is False


def test_is_not_orientable_when_dora_form_is_disabled_for_the_structure():
    di_service_data = make_di_service_data()
    baker.make(
        "structures.DisabledDoraFormDIStructure",
        source=di_service_data["source"],
        structure_id=di_service_data["structure_id"],
    )

    assert is_orientable(di_service_data) is False


def test_map_service_address_line():
    di_service_data = make_di_service_data(
        adresse="6 Boulevard St Denis",
        complement_adresse="Plateforme de l'inclusion",
        code_postal="75010",
        commune="Paris",
    )
    service = map_service(di_service_data, False)

    assert (
        service["address_line"]
        == "6 Boulevard St Denis Plateforme de l'inclusion - 75010 Paris"
    )
