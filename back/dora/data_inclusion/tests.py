import pytest

from .constants import THEMATIQUES_MAPPING_DI_TO_DORA
from .mappings import map_service
from .test_utils import FakeDataInclusionClient, make_di_service_data


def test_map_service_thematiques_mapping():
    input_thematiques = [
        "logement-hebergement",
        "logement-hebergement--connaissance-de-ses-droits-et-interlocuteurs",
        "logement-hebergement--besoin-dadapter-mon-logement",
    ] + list(THEMATIQUES_MAPPING_DI_TO_DORA.keys())

    expected_categories = ["logement-hebergement"]
    expected_subcategories = [
        "logement-hebergement--connaissance-de-ses-droits-et-interlocuteurs",
        "logement-hebergement--besoin-dadapter-mon-logement",
    ] + list(THEMATIQUES_MAPPING_DI_TO_DORA.values())

    di_service_data = make_di_service_data(thematiques=input_thematiques)
    service = map_service(di_service_data, False)

    assert sorted(service["categories"]) == sorted(expected_categories)
    assert sorted(service["subcategories"]) == sorted(expected_subcategories)


@pytest.mark.parametrize(
    "thematiques_dora, thematiques_di",
    [
        (
            ["logement-hebergement--etre-accompagne-pour-se-loger"],
            ["logement-hebergement--etre-accompagne-dans-son-projet-accession"],
        ),
        (
            ["logement-hebergement--gerer-son-budget"],
            ["logement-hebergement--etre-accompagne-en cas-de-difficultes-financieres"],
        ),
        (
            ["logement-hebergement--autre"],
            ["logement-hebergement--financer-son-projet-travaux"],
        ),
    ],
)
def test_di_client_search_thematiques_mapping(thematiques_dora, thematiques_di):
    di_client = FakeDataInclusionClient()
    di_service_data = make_di_service_data(thematiques=thematiques_di)
    di_client.services.append(di_service_data)

    results = di_client.search_services(thematiques=thematiques_dora)

    assert len(results) == 1
