import random
from _operator import itemgetter
from datetime import date
from functools import reduce
from typing import Optional

import requests
from django.conf import settings
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db.models import IntegerField, Q, QuerySet, Value
from django.utils import timezone

import dora.services.models as models
from dora import data_inclusion
from dora.core.constants import WGS84
from dora.decoupage_administratif.models import City
from dora.services.models import ServiceSubCategory

from .models import FundingLabel
from .serializers import FundingLabelSerializer, SearchResultSerializer
from .utils import filter_services_by_city_code

MAX_DISTANCE = 50
DEPARTMENT_CODE_SOMME = "80"
DEPARTMENT_CODE_VOSGES = "88"
MEDIATION_NUMERIQUE_SOURCE = "mediation-numerique"
FRANCE_SERVICES_STRUCTURE_ID_PREFIX = "mediation-numerique--France-Services"


def _filter_and_annotate_dora_services(
    services: QuerySet[models.Service],
    location: Point,
    with_remote: bool,
    with_onsite: bool,
) -> QuerySet[models.Service]:
    no_services = models.Service.objects.none()
    # 1) services ayant un lieu de déroulement, à moins de MAX_DISTANCE km
    services_on_site = (
        services.filter(location_kinds__value="en-presentiel")
        .annotate(distance=Distance("geom", location))
        .filter(distance__lte=D(km=MAX_DISTANCE))
        if with_onsite
        else no_services
    )
    # 2) services sans lieu de déroulement
    services_remote = (
        (
            services.filter(
                Q(location_kinds__value="a-distance")
                | ~Q(location_kinds__value="en-presentiel")
            )
            .exclude(id__in=services_on_site)
            .distinct()
            .annotate(distance=Value(None, output_field=IntegerField()))
        )
        if with_remote
        else no_services
    )
    return services_on_site | services_remote


def _sort_services(services):
    on_site_services = []
    remote_services = []

    for s in services:
        if (
            "en-presentiel" in s["location_kinds"]
            and s["distance"] is not None
            and s["distance"] <= MAX_DISTANCE
        ):
            on_site_services.append(s)
        elif "a-distance" in s["location_kinds"] or s["location_kinds"] == []:
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


DI_SERVICE_KINDS = {
    "accompagnement",
    "aide-financiere",
    "aide-materielle",
    "atelier",
    "formation",
    "information",
}


def _map_kinds_dora_to_di(kinds: list[str]) -> list[str]:
    return [kind for kind in kinds if kind in DI_SERVICE_KINDS]


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
    with_dora: bool = False,
) -> list:
    """Search data.inclusion services.

    The ``di_client`` acts as an entrypoint to the data.inclusion service repository.

    The search will target the sources configured by the ``DATA_INCLUSION_STREAM_SOURCES``
    environment variable.

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

    # Si on veut toutes les sources incluant Dora, on ne spécifie pas de sources
    # (on récupère tous les services de toutes les sources).
    # Sinon, on spécifie les sources à récupérer (liste des sources sauf Dora).
    sources = None if with_dora else settings.DATA_INCLUSION_STREAM_SOURCES

    types = _map_kinds_dora_to_di(kinds) if kinds else None

    try:
        raw_di_results = di_client.search_services(
            sources=sources,
            score_qualite_minimum=(
                # Pas de filtrage sur le score de qualité si on veut aussi les services DORA
                None if with_dora else settings.DATA_INCLUSION_SCORE_QUALITE_MINIMUM
            ),
            code_commune=city_code,
            thematiques=thematiques if len(thematiques) > 0 else None,
            types=types,
            frais=fees,
            lat=lat,
            lon=lon,
        )
    except requests.ConnectionError:
        return []

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
    supported_service_kinds = models.ServiceKind.objects.values_list("value", flat=True)

    mapped_di_results = [
        data_inclusion.map_search_result(result, supported_service_kinds)
        for result in raw_di_results
    ]

    # FIXME: exclu les services uniquement en présentiel à plus de MAX_DISTANCE
    # du lieu de recherche (ainsi que ceux qui ne retournent pas d'information de distance).
    # À terme il faudra passer par un rayon configurable
    mapped_di_results = [
        result
        for result in mapped_di_results
        if (
            "a-distance" in result["location_kinds"]
            or (
                result.get("distance") is not None
                and result["distance"] <= MAX_DISTANCE
            )
        )
    ]

    # FIXME: gestion du paramètre `location_kinds`
    # Idéalement, il faudrait le transmettre à l’API d·i, mais tant qu’elle ne le prend pas
    # en charge, on filtre les services à posteriori
    with_remote = not location_kinds or "a-distance" in location_kinds
    with_onsite = not location_kinds or "en-presentiel" in location_kinds
    mapped_di_results = [
        result
        for result in mapped_di_results
        if (
            (with_onsite and "en-presentiel" in result["location_kinds"])
            or (with_remote and "a-distance" in result["location_kinds"])
        )
    ]
    return mapped_di_results


def _get_di_results(
    di_client: data_inclusion.DataInclusionClient,
    city_code: str,
    categories: Optional[list[str]] = None,
    subcategories: Optional[list[str]] = None,
    kinds: Optional[list[str]] = None,
    fees: Optional[list[str]] = None,
    location_kinds: Optional[list[str]] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
) -> list:
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

    mapped_di_results = _map_di_results(raw_di_results, location_kinds)

    return mapped_di_results


def _get_dora_results(
    request,
    city_code: str,
    city: City,
    categories: Optional[list[str]] = None,
    subcategories: Optional[list[str]] = None,
    kinds: Optional[list[str]] = None,
    fees: Optional[list[str]] = None,
    location_kinds: Optional[list[str]] = None,
    funding_labels: Optional[list[str]] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
):
    services = (
        models.Service.objects.filter_for_DI()
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
    )

    if kinds:
        services = services.filter(kinds__value__in=kinds)

    if fees:
        services = services.filter(fee_condition__value__in=fees)

    if location_kinds:
        services = services.filter(location_kinds__value__in=location_kinds)

    if funding_labels:
        services = services.filter(funding_labels__value__in=funding_labels)

    with_remote = not location_kinds or "a-distance" in location_kinds
    with_onsite = not location_kinds or "en-presentiel" in location_kinds

    categories_filter = Q()
    if categories:
        categories_filter = Q(categories__value__in=categories)

    subcategories_filter = Q()
    if subcategories:
        for subcategory in subcategories:
            cat, subcat = subcategory.split("--")
            if subcat == "autre":
                # Quand on cherche une sous-catégorie de type 'Autre', on veut
                # aussi remonter les services sans sous-catégorie
                all_sister_subcats = models.ServiceSubCategory.objects.filter(
                    value__startswith=f"{cat}--"
                )
                subcategories_filter |= Q(subcategories__value=subcategory) | (
                    Q(categories__value=cat) & ~Q(subcategories__in=all_sister_subcats)
                )
            else:
                subcategories_filter |= Q(subcategories__value=subcategory)

    services = services.filter(categories_filter | subcategories_filter).distinct()

    geofiltered_services = filter_services_by_city_code(services, city_code)

    # Exclude suspended services
    services_to_display = geofiltered_services.filter(
        Q(suspension_date=None) | Q(suspension_date__gte=timezone.now())
    ).distinct()

    results = _filter_and_annotate_dora_services(
        services_to_display,
        city.center if not lat or not lon else Point(lon, lat, srid=WGS84),
        with_remote,
        with_onsite,
    )

    funding_labels_found = FundingLabel.objects.filter(service__in=results).distinct()

    return SearchResultSerializer(
        results, many=True, context={"request": request}
    ).data, {
        "funding_labels": FundingLabelSerializer(funding_labels_found, many=True).data
    }


def _get_unified_results(
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
) -> list:
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
        with_dora=True,
    )

    # Les ID de services DI sont de la forme "source--id".
    # On récupère l'ID Dora du service et la distance calculée par DI,
    # en conservant l'ordre des résultats DI (triés par distance).
    dora_results_from_di = [
        (result["service"]["id"].split("--")[1], result["distance"])
        for result in raw_di_results
        if result["service"]["source"] == "dora"
    ]
    dora_distances = {dora_id: distance for dora_id, distance in dora_results_from_di}
    dora_ids = list(dora_distances.keys())

    dora_services_by_id = {
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
        .filter(id__in=dora_ids)
        .distinct()
    }

    # Annotation des services avec la distance calculée par DI,
    # en conservant l'ordre des résultats DI.
    annotated_dora_results = []
    for dora_id in dora_ids:
        service = dora_services_by_id.get(dora_id)
        if service:
            service.distance = dora_distances.get(dora_id)
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
    city: City,
    categories: Optional[list[str]] = None,
    subcategories: Optional[list[str]] = None,
    kinds: Optional[list[str]] = None,
    fees: Optional[list[str]] = None,
    location_kinds: Optional[list[str]] = None,
    funding_labels: Optional[list[str]] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    unified_search_enabled: bool = True,
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

    # Par défaut, le mode de recherche est unifié (recherche DI puis filtrage Dora)
    if settings.DI_DORA_UNIFIED_SEARCH_ENABLED and unified_search_enabled:
        results, metadata = _get_unified_results(
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
        if len(results) == 0:
            # Pas de résultat peut signifier que DI n'est pas accessible.
            # On relance la recherche sur les services DORA locaux.
            results, metadata = _get_dora_results(
                request=request,
                categories=categories,
                subcategories=subcategories,
                city_code=city_code,
                city=city,
                kinds=kinds,
                fees=fees,
                location_kinds=location_kinds,
                funding_labels=funding_labels,
                lat=lat,
                lon=lon,
            )
        return _sort_services(results), metadata

    # Sinon, le mode de recherche est distribué (recherche DI + recherche Dora)
    di_results = (
        _get_di_results(
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
        if di_client is not None
        else []
    )

    dora_results, metadata = _get_dora_results(
        request=request,
        categories=categories,
        subcategories=subcategories,
        city_code=city_code,
        city=city,
        kinds=kinds,
        fees=fees,
        location_kinds=location_kinds,
        funding_labels=funding_labels,
        lat=lat,
        lon=lon,
    )

    all_results = [*dora_results, *di_results]
    return _sort_services(all_results), metadata
