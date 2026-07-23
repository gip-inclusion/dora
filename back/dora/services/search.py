import logging
import random
from _operator import itemgetter
from datetime import date
from functools import reduce
from typing import Optional

import requests
from data_inclusion.schema.v1 import ModeAccueil
from django.conf import settings
from django.db.models import Q

import dora.services.models as models
from dora import data_inclusion
from dora.api.exceptions import ServiceUnavailable
from dora.data_inclusion.mappings import map_search_result
from dora.decoupage_administratif.models import City
from dora.services.models import ServiceSubCategory

from .models import FundingLabel
from .serializers import FundingLabelSerializer, SearchResultSerializer

MAX_DISTANCE = 50
DEPARTMENT_CODE_SOMME = "80"
DEPARTMENT_CODE_VOSGES = "88"
MEDIATION_NUMERIQUE_SOURCE = "mediation-numerique"
FRANCE_SERVICES_STRUCTURE_ID_PREFIX = "mediation-numerique--France-Services"

logger = logging.getLogger(__name__)


def _sort_services(services):
    on_site_services = []
    remote_services = []

    for s in services:
        if (
            ModeAccueil.EN_PRESENTIEL in s["location_kinds"]
            and s["distance"] is not None
            and s["distance"] <= MAX_DISTANCE
        ):
            on_site_services.append(s)
        elif ModeAccueil.A_DISTANCE in s["location_kinds"] or s["location_kinds"] == []:
            remote_services.append(s)
    random.seed(date.today().isoformat())
    random.shuffle(on_site_services)
    on_site_services = sorted(on_site_services, key=itemgetter("distance"))
    on_site_services = iter(on_site_services)

    random.shuffle(remote_services)
    remote_services = iter(remote_services)

    results = []
    no_more_on_site = False
    no_more_remote = False
    while not no_more_on_site or not no_more_remote:
        try:
            results.append(next(on_site_services))
            results.append(next(on_site_services))
        except StopIteration:
            no_more_on_site = True
        try:
            results.append(next(remote_services))
        except StopIteration:
            no_more_remote = True
    return results


def _filter_di_results(raw_di_results: list, city_code: str) -> list:
    city = City.objects.filter(code=city_code).first()

    if not city:
        return raw_di_results

    if city.department == DEPARTMENT_CODE_VOSGES:
        # Exclusion des services mediation-numerique
        return [
            result
            for result in raw_di_results
            if result["service"]["source"] != MEDIATION_NUMERIQUE_SOURCE
        ]

    if city.department == DEPARTMENT_CODE_SOMME:
        # Exclusion des services mediation-numerique, sauf les services de France Services
        return [
            result
            for result in raw_di_results
            if result["service"]["source"] != MEDIATION_NUMERIQUE_SOURCE
            or result["service"]["structure"]["id"].startswith(
                FRANCE_SERVICES_STRUCTURE_ID_PREFIX
            )
        ]

    return raw_di_results


def _get_raw_di_results(
    di_client: data_inclusion.DataInclusionClient,
    city_code: str,
    categories: Optional[list[str]] = None,
    subcategories: Optional[list[str]] = None,
    kinds: Optional[list[str]] = None,
    fees: Optional[list[str]] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
) -> list:
    """Search data.inclusion services.

    The ``di_client`` acts as an entrypoint to the data.inclusion service repository.

    The other arguments match the input parameters from the classical search.

    This function essentially:

    * maps the input parameters,
    * offloads the search to the data.inclusion client,

    This function should catch any client and upstream errors to prevent any impact on
    the classical flow of dora.

    Returns:
        A list of search results by SearchResultSerializer.
    """
    thematiques = []
    if categories is not None:
        # Sélection des sous-catégories correspondant aux catégories
        subcategories_filters = reduce(
            lambda x, y: x | y,
            [Q(value__startswith=category) for category in categories],
        )
        thematiques += ServiceSubCategory.objects.filter(
            subcategories_filters
        ).values_list("value", flat=True)
    if subcategories is not None:
        # Exclusion des sous-catégories --autre
        thematiques += [subcat for subcat in subcategories if "--autre" not in subcat]

    # Si on recherche uniquement des sous-catégories `autre`, la liste des thématiques
    # va être vide et d·i renverrait *tous* les services.
    # On renvoie donc plutôt une liste vide.
    if not thematiques and subcategories:
        return []

    try:
        raw_di_results = di_client.search_services(
            code_commune=city_code,
            thematiques=thematiques if len(thematiques) > 0 else None,
            types=kinds,
            frais=fees,
            lat=lat,
            lon=lon,
        )
    except requests.ConnectionError:
        raise ServiceUnavailable(
            "L’API data.inclusion.gouv.fr nécessaire pour la recherche "
            "n’est pas disponible. Merci de réessayer ultérieurement."
        )

    if raw_di_results is None:
        return []

    return _filter_di_results(raw_di_results, city_code)


def _map_di_results(
    raw_di_results: list,
    location_kinds: Optional[list[str]] = None,
) -> list:
    """Convert DI service to Dora format.

    Returns:
        A list of search results by SearchResultSerializer.
    """
    mapped_di_results = [map_search_result(result) for result in raw_di_results]

    # FIXME: exclu les services uniquement en présentiel à plus de MAX_DISTANCE
    # du lieu de recherche (ainsi que ceux qui ne retournent pas d'information de distance).
    # À terme il faudra passer par un rayon configurable
    mapped_di_results = [
        result
        for result in mapped_di_results
        if (
            ModeAccueil.A_DISTANCE in result["location_kinds"]
            or (
                result.get("distance") is not None
                and result["distance"] <= MAX_DISTANCE
            )
        )
    ]

    # FIXME: gestion du paramètre `location_kinds`
    # Idéalement, il faudrait le transmettre à l’API d·i, mais tant qu’elle ne le prend pas
    # en charge, on filtre les services à posteriori
    with_remote = not location_kinds or ModeAccueil.A_DISTANCE in location_kinds
    with_onsite = not location_kinds or ModeAccueil.EN_PRESENTIEL in location_kinds
    mapped_di_results = [
        result
        for result in mapped_di_results
        if (
            (with_onsite and ModeAccueil.EN_PRESENTIEL in result["location_kinds"])
            or (with_remote and ModeAccueil.A_DISTANCE in result["location_kinds"])
        )
    ]
    return mapped_di_results


def _dora_services_by_id(service_ids):
    return {
        str(service.id): service
        for service in models.Service.objects.filter_for_DI()
        .select_related(
            "structure",
        )
        .prefetch_related(
            "kinds",
            "fee_condition",
            "location_kinds",
            "publics",
            "categories",
            "subcategories",
            "funding_labels",
            "coach_orientation_modes",
            "beneficiaries_access_modes",
        )
        .filter(id__in=service_ids)
        .distinct()
    }


def _get_results(
    request,
    di_client: data_inclusion.DataInclusionClient,
    city_code: str,
    categories: Optional[list[str]] = None,
    subcategories: Optional[list[str]] = None,
    kinds: Optional[list[str]] = None,
    fees: Optional[list[str]] = None,
    location_kinds: Optional[list[str]] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
):
    """Search data.inclusion services and convert them to the Dora format.

    Returns:
        A list of search results by SearchResultSerializer.
    """
    raw_di_results = _get_raw_di_results(
        di_client=di_client,
        city_code=city_code,
        categories=categories,
        subcategories=subcategories,
        kinds=kinds,
        fees=fees,
        lat=lat,
        lon=lon,
    )

    # Les ID de services DI sont de la forme "source--id".
    # On récupère l'ID Dora du service et la distance calculée par DI,
    # en conservant l'ordre des résultats DI (triés par distance).
    dora_distances = {
        result["service"]["id"].split("--")[1]: result["distance"]
        for result in raw_di_results
        if result["service"]["source"] == "dora"
    }
    dora_ids = list(dora_distances.keys())

    dora_services_by_id = _dora_services_by_id(dora_ids)

    # Annotation des services avec la distance calculée par DI,
    # en conservant l'ordre des résultats DI.
    annotated_dora_results = []
    for dora_id in dora_ids:
        service = dora_services_by_id.get(dora_id)
        if service:
            service.distance = dora_distances[dora_id]
            annotated_dora_results.append(service)

    serialized_dora_results = SearchResultSerializer(
        annotated_dora_results, many=True, context={"request": request}
    ).data
    funding_labels_found = FundingLabel.objects.filter(
        service__in=annotated_dora_results
    ).distinct()

    other_raw_results = [
        result for result in raw_di_results if result["service"]["source"] != "dora"
    ]

    if settings.DATA_INCLUSION_SCORE_QUALITE_MINIMUM:
        other_raw_results = [
            result
            for result in other_raw_results
            if result["service"]["score_qualite"]
            >= settings.DATA_INCLUSION_SCORE_QUALITE_MINIMUM
        ]

    serialized_other_results = _map_di_results(other_raw_results, location_kinds)

    serialized_results = [*serialized_dora_results, *serialized_other_results]

    return serialized_results, {
        "funding_labels": FundingLabelSerializer(funding_labels_found, many=True).data
    }


def search_services(
    request,
    di_client: data_inclusion.DataInclusionClient,
    city_code: str,
    categories: Optional[list[str]] = None,
    subcategories: Optional[list[str]] = None,
    kinds: Optional[list[str]] = None,
    fees: Optional[list[str]] = None,
    location_kinds: Optional[list[str]] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
) -> (list[dict], dict):
    """Search services from all available repositories.

    It always includes results from dora own databases.

    If the ``di_client`` parameter is defined, results from data.inclusion will be
    added using the client dependency.

    Note : this is the only point where di_client is "injected"

    Returns:
        - A list of search results by SearchResultSerializer.
        - A metadata dictionary
    """
    # Recherche DI puis filtrage Dora.
    results, metadata = _get_results(
        request=request,
        di_client=di_client,
        categories=categories,
        subcategories=subcategories,
        city_code=city_code,
        kinds=kinds,
        fees=fees,
        location_kinds=location_kinds,
        lat=lat,
        lon=lon,
    )
    return _sort_services(results), metadata


def _get_keyword_search_results(request, raw_di_results):
    def dora_id(service):
        return service["id"].removeprefix("dora--")

    dora_ids = {
        dora_id(result["service"])
        for result in raw_di_results
        if result["service"]["source"] == "dora"
    }
    dora_services_by_id = _dora_services_by_id(dora_ids)
    results = []
    for raw_di_result in raw_di_results:
        if raw_di_result["service"]["source"] == "dora":
            service = dora_services_by_id.get(dora_id(raw_di_result["service"]))
            if service:
                service.distance = raw_di_result["distance"]
                service.search_score = raw_di_result["score_recherche"]
                data = SearchResultSerializer(
                    service, context={"request": request}
                ).data
                results.append(data)
            else:
                logger.warning(
                    "d·i a retourné un service inconnu, id: %s",
                    dora_id(raw_di_result["service"]),
                )
        else:
            results.append(map_search_result(raw_di_result))
    return results


def search_keyword(request, api_params):
    di_client = data_inclusion.di_client_factory()
    try:
        raw_di_results = di_client.search(**api_params, size=50)
    except requests.RequestException:
        raise ServiceUnavailable(
            "L’API data.inclusion.gouv.fr nécessaire pour la recherche "
            "n’est pas disponible. Merci de réessayer ultérieurement."
        )
    results = _get_keyword_search_results(request, raw_di_results["items"])
    metadata = {
        "services_pages": raw_di_results["pages"],
        "services_total": raw_di_results["total"],
    }
    return results, metadata
