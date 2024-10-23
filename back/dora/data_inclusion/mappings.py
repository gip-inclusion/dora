from data_inclusion.schema import Profil
from django.conf import settings
from django.utils import dateparse, timezone

from dora.admin_express.models import AdminDivisionType
from dora.core.utils import code_insee_to_code_dept
from dora.services.enums import ServiceStatus
from dora.services.models import (
    BeneficiaryAccessMode,
    CoachOrientationMode,
    LocationKind,
    ServiceCategory,
    ServiceKind,
    ServiceSubCategory,
    get_diffusion_zone_details_display,
    get_update_status,
)

from .constants import THEMATIQUES_MAPPING_DI_TO_DORA

DI_TO_DORA_DIFFUSION_ZONE_TYPE_MAPPING = {
    "commune": "city",
    "epci": "epci",
    "departement": "department",
    "region": "region",
    "pays": "country",
}


# Différence entre les types "" ou [] et None :
# Une valeur nulle (None) signifie que l'information n'est pas renseignée tandis
# qu'une valeur vide ("" ou []) signifie que l'information est renseignée mais vide.
# Ces valeurs ayant un sens différent, leur traitement peut lui aussi différer.


# TODO:
# On pourrait avoir envie d'instancier un objet service et de réutiliser la sérialisation implémentée.
# Les relations m2m nécessitent malheureusement la sauvegarde en db.
# On pourrait tout de même implémenter les mappings avec des serializers basés sur ceux existants.


def map_search_result(result: dict, supported_service_kinds: list[str]) -> dict:
    # On transforme les champs nécessaires à l'affichage des resultats de recherche au format DORA
    # (c.a.d qu'on veut un objet similaire à ce que renvoie le SearchResultSerializer)

    # Voir différence entre les types "" ou [] et None dans le commentaire en haut du fichier

    service_data = result["service"]
    location_kinds = service_data["modes_accueil"] or []
    if location_kinds == [] and result["distance"] is not None:
        location_kinds = ["en-presentiel"]

    kinds = (
        filter(lambda kind: kind in supported_service_kinds, service_data["types"])
        if service_data["types"] is not None
        else None
    )

    return {
        #
        # SearchResultSerializer
        #
        "distance": result["distance"]
        if result["distance"] is not None
        else None,  # en km
        "address1": service_data["adresse"],
        "address2": service_data["complement_adresse"],
        "city": service_data["commune"],
        "postal_code": service_data["code_postal"],
        #
        # ServiceListSerializer
        #
        "structure_info": {"name": service_data["structure"]["nom"]},
        #
        # ServiceSerializer
        #
        # TODO: spécifier 'en-presentiel' si on a une geoloc/adresse?
        "location_kinds": location_kinds,
        "kinds": kinds,
        "fee_condition": service_data["frais"][0] if service_data["frais"] else None,
        "modification_date": service_data["date_maj"],
        "name": service_data["nom"],
        "short_desc": service_data["presentation_resume"] or "",
        "slug": f"{service_data['source']}--{service_data['id']}",
        "status": ServiceStatus.PUBLISHED.value,
        "structure": service_data["structure_id"],
        # Champs spécifiques aux résultats d·i
        "type": "di",
        "di_source": service_data["source"],
        "di_source_display": service_data["source"].title(),  # TODO
        "id": service_data["id"],
        "diffusion_zone_type": DI_TO_DORA_DIFFUSION_ZONE_TYPE_MAPPING.get(
            result["service"]["zone_diffusion_type"], None
        ),
        "coordinates": (result["service"]["longitude"], result["service"]["latitude"])
        if result["service"]["longitude"] and result["service"]["latitude"]
        else None,
        "is_orientable": is_orientable(service_data),
    }


def is_orientable(service_data: dict) -> bool:
    siren = (
        service_data["structure"]["siret"][:9]
        if service_data["structure"].get("siret")
        else None
    )
    blacklisted = siren in settings.ORIENTATION_SIRENE_BLACKLIST
    blacklisted |= not service_data["courriel"]
    return not blacklisted


def map_service(service_data: dict, is_authenticated: bool) -> dict:
    # Voir différence entre les types "" ou [] et None dans le commentaire en haut du fichier

    categories = None
    subcategories = None
    if service_data["thematiques"] is not None:
        thematiques = [
            THEMATIQUES_MAPPING_DI_TO_DORA.get(thematique, thematique)
            for thematique in service_data["thematiques"]
        ]
        categories = ServiceCategory.objects.filter(value__in=thematiques)
        subcategories = ServiceSubCategory.objects.filter(value__in=thematiques)

    location_kinds = None
    if service_data["modes_accueil"] is not None:
        location_kinds = LocationKind.objects.filter(
            value__in=service_data["modes_accueil"]
        )

    kinds = None
    if service_data["types"] is not None:
        kinds = ServiceKind.objects.filter(value__in=service_data["types"])

    zone_diffusion_type = DI_TO_DORA_DIFFUSION_ZONE_TYPE_MAPPING.get(
        service_data["zone_diffusion_type"], None
    )

    department = None
    if service_data["code_insee"] is not None:
        department = code_insee_to_code_dept(service_data["code_insee"])

    update_status = None
    if service_data["date_maj"] is not None:
        update_status = get_update_status(
            status=ServiceStatus.PUBLISHED,
            modification_date=timezone.make_aware(
                dateparse.parse_datetime(service_data["date_maj"])
            ),
        ).value

    fee_condition = None
    if service_data["frais"] is not None:
        fee_condition = ", ".join(service_data["frais"])

    structure_insee_code = (
        service_data["structure"]["code_insee"]
        if service_data["structure"].get("code_insee")
        else service_data["structure"].get("_di_geocodage_code_insee")
    )

    structure_department = (
        code_insee_to_code_dept(structure_insee_code) if structure_insee_code else ""
    )

    beneficiaries_access_modes = None
    if service_data["modes_orientation_beneficiaire"] is not None:
        beneficiaries_access_modes = BeneficiaryAccessMode.objects.filter(
            value__in=service_data["modes_orientation_beneficiaire"]
        )

    coach_orientation_modes = None
    if service_data["modes_orientation_accompagnateur"] is not None:
        coach_orientation_modes = CoachOrientationMode.objects.filter(
            value__in=service_data["modes_orientation_accompagnateur"]
        )

    profils = None
    if service_data["profils"] is not None:
        profils = [
            Profil(p)
            for p in (set(service_data["profils"]) & {p.value for p in Profil})
        ]
    return {
        "access_conditions": None,
        "access_conditions_display": None,
        "address1": service_data["adresse"],
        "address2": service_data["complement_adresse"],
        "beneficiaries_access_modes": [m.value for m in beneficiaries_access_modes]
        if beneficiaries_access_modes is not None
        else None,
        "beneficiaries_access_modes_display": [
            m.label for m in beneficiaries_access_modes
        ]
        if beneficiaries_access_modes is not None
        else None,
        "beneficiaries_access_modes_external_form_link": service_data[
            "formulaire_en_ligne"
        ],
        "beneficiaries_access_modes_external_form_link_text": "",
        "beneficiaries_access_modes_other": service_data[
            "modes_orientation_beneficiaire_autres"
        ],
        "can_write": False,
        "categories": [c.value for c in categories] if categories is not None else None,
        "categories_display": [c.label for c in categories]
        if categories is not None
        else None,
        "city": service_data["commune"],
        "city_code": service_data["code_insee"],
        "coach_orientation_modes": [m.value for m in coach_orientation_modes]
        if coach_orientation_modes is not None
        else None,
        "coach_orientation_modes_display": [m.label for m in coach_orientation_modes]
        if coach_orientation_modes is not None
        else None,
        "coach_orientation_modes_external_form_link": service_data[
            "formulaire_en_ligne"
        ],
        "coach_orientation_modes_external_form_link_text": "",
        "coach_orientation_modes_other": service_data[
            "modes_orientation_accompagnateur_autres"
        ],
        "concerned_public": [p.value for p in profils] if profils is not None else None,
        "concerned_public_display": [p.label for p in profils]
        if profils is not None
        else None,
        "contact_email": service_data["courriel"]
        if service_data["contact_public"] or is_authenticated
        else None,
        "contact_name": service_data["contact_nom_prenom"]
        if service_data["contact_public"] or is_authenticated
        else None,
        "contact_phone": service_data["telephone"]
        if service_data["contact_public"] or is_authenticated
        else None,
        # double implémentation de cette valeur métier (voir modèle du service DORA) 😩
        "contact_info_filled": bool(
            service_data["courriel"] or service_data["telephone"]
        ),
        "creation_date": service_data["date_creation"],
        "credentials": service_data["justificatifs"],
        "credentials_display": service_data["justificatifs"],
        "department": department,
        "diffusion_zone_details": service_data["zone_diffusion_code"],
        "diffusion_zone_details_display": get_diffusion_zone_details_display(
            diffusion_zone_details=service_data["zone_diffusion_code"],
            diffusion_zone_type=zone_diffusion_type,
        ),
        "diffusion_zone_type": zone_diffusion_type,
        "diffusion_zone_type_display": AdminDivisionType(zone_diffusion_type).label
        if zone_diffusion_type is not None
        else "",
        "fee_condition": fee_condition,
        "fee_details": service_data["frais_autres"],
        "forms": None,
        "forms_info": None,
        "full_desc": service_data["presentation_detail"] or "",
        "geom": None,
        "has_already_been_unpublished": None,
        "is_available": True,
        "is_contact_info_public": service_data["contact_public"],
        "is_cumulative": service_data["cumulable"],
        "is_orientable": is_orientable(service_data),
        "kinds": [k.value for k in kinds] if kinds is not None else None,
        "kinds_display": [k.label for k in kinds] if kinds is not None else None,
        "lien_source": service_data["lien_source"],
        "location_kinds": [lk.value for lk in location_kinds]
        if location_kinds is not None
        else None,
        "location_kinds_display": [lk.label for lk in location_kinds]
        if location_kinds is not None
        else None,
        "model": None,
        "model_changed": None,
        "model_name": None,
        "modification_date": service_data["date_maj"],
        "name": service_data["nom"],
        "online_form": None,
        "postal_code": service_data["code_postal"],
        "publication_date": None,
        "qpv_or_zrr": None,
        "recurrence": service_data["recurrence"],
        "remote_url": None,
        "requirements": service_data["pre_requis"],
        "requirements_display": service_data["pre_requis"],
        "short_desc": service_data["presentation_resume"] or "",
        "slug": f"{service_data['source']}--{service_data['id']}",
        "source": service_data["source"],
        "status": ServiceStatus.PUBLISHED.value,
        "structure": service_data["structure_id"],
        "structure_info": {
            "name": service_data["structure"]["nom"],
            "department": structure_department,
            "phone": service_data["structure"]["telephone"],
            "email": service_data["structure"]["courriel"],
        },
        "subcategories": [c.value for c in subcategories]
        if subcategories is not None
        else None,
        "subcategories_display": [c.label for c in subcategories]
        if subcategories is not None
        else None,
        "suspension_date": service_data["date_suspension"],
        "update_status": update_status,
        "use_inclusion_numerique_scheme": False,
    }
