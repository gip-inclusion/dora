import textwrap

from data_inclusion.schema.v1 import ModeMobilisation, PersonneMobilisatrice, Public
from django.conf import settings
from django.utils import dateparse, timezone

from dora.core.utils import (
    address_to_one_line,
    code_insee_to_code_dept,
    get_category_from_subcategory,
)
from dora.services.enums import ServiceStatus
from dora.services.models import (
    BeneficiaryAccessMode,
    CoachOrientationMode,
    LocationKind,
    ServiceCategory,
    ServiceKind,
    ServiceSubCategory,
    UpdateFrequency,
    get_update_needed,
)
from dora.structures.models import DisabledDoraFormDIStructure

from .constants import (
    MODE_MOBILISATION_DI_TO_DORA,
)
from .diffusion_zone_info import get_diffusion_zone_info

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
        [service_data["type"]]
        if service_data["type"] in supported_service_kinds
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
        "location_kinds": location_kinds,
        "kinds": kinds,
        "fee_condition": service_data["frais"],
        "funding_labels": [],
        "modification_date": service_data["date_maj"],
        "name": service_data["nom"],
        "short_desc": textwrap.shorten(
            service_data["description"], width=200, placeholder="…"
        )
        if service_data["description"]
        else "",
        "slug": service_data["id"],
        "status": ServiceStatus.PUBLISHED.value,
        "structure": service_data["structure_id"],
        # Champs spécifiques aux résultats d·i
        "type": "di",
        "di_source": service_data["source"],
        "di_source_display": service_data["source"].title(),  # TODO
        "id": service_data["id"],
        "coordinates": (result["service"]["longitude"], result["service"]["latitude"])
        if result["service"]["longitude"] and result["service"]["latitude"]
        else None,
        "publication_date": None,
    }


def is_orientable(service_data: dict) -> bool:
    siren = (
        service_data["structure"]["siret"][:9]
        if service_data["structure"].get("siret")
        else None
    )
    blacklisted = siren in settings.ORIENTATION_SIRENE_BLACKLIST
    blacklisted |= not service_data["courriel"]

    if blacklisted:
        return False

    return not DisabledDoraFormDIStructure.objects.filter(
        source=service_data["source"], structure_id=service_data["structure_id"]
    ).exists()


def map_service(service_data: dict, is_authenticated: bool) -> dict:
    # Voir différence entre les types "" ou [] et None dans le commentaire en haut du fichier

    categories = []
    subcategories = []
    if service_data["thematiques"] is not None:
        categories = ServiceCategory.objects.filter(
            value__in=[
                get_category_from_subcategory(thematique)
                for thematique in service_data["thematiques"]
            ]
        )
        subcategories = ServiceSubCategory.objects.filter(
            value__in=service_data["thematiques"]
        )

    location_kinds = None
    if service_data["modes_accueil"] is not None:
        location_kinds = LocationKind.objects.filter(
            value__in=service_data["modes_accueil"]
        )

    kind = ServiceKind.objects.filter(value=service_data["type"]).first()

    department = None
    if service_data["code_insee"] is not None:
        department = code_insee_to_code_dept(service_data["code_insee"])

    update_needed = None
    if service_data["date_maj"] is not None:
        update_needed = get_update_needed(
            status=ServiceStatus.PUBLISHED,
            update_frequency=UpdateFrequency.NEVER,  # Un service DI de ne peut pas être mise à jour sur DORA
            modification_date=timezone.make_aware(
                dateparse.parse_datetime(service_data["date_maj"])
            ),
        )

    structure_insee_code = (
        service_data["structure"]["code_insee"]
        if service_data["structure"].get("code_insee")
        else service_data["structure"].get("_di_geocodage_code_insee")
    )

    structure_department = (
        code_insee_to_code_dept(structure_insee_code) if structure_insee_code else ""
    )

    beneficiaries_access_modes = None
    beneficiaries_access_modes_external_form_link = None
    beneficiaries_access_modes_other = None
    if (
        service_data["modes_mobilisation"] is not None
        and service_data["mobilisable_par"] is not None
        and PersonneMobilisatrice.USAGERS in service_data["mobilisable_par"]
    ):
        beneficiaries_access_modes = BeneficiaryAccessMode.objects.filter(
            value__in=[
                MODE_MOBILISATION_DI_TO_DORA[mode]
                for mode in service_data["modes_mobilisation"]
            ]
        )
        # Autres champs
        beneficiaries_access_modes_external_form_link = service_data[
            "lien_mobilisation"
        ]
        beneficiaries_access_modes_other = service_data["mobilisation_precisions"]

    coach_orientation_modes = None
    coach_orientation_modes_external_form_link = None
    coach_orientation_modes_other = None
    if (
        service_data["modes_mobilisation"] is not None
        and service_data["mobilisable_par"] is not None
        and PersonneMobilisatrice.PROFESSIONNELS in service_data["mobilisable_par"]
    ):
        modes_mobilisation = service_data["modes_mobilisation"].copy()
        # Suppression du mode utiliser-lien-mobilisation si lien_mobilisation n'est pas spécifié
        if (
            ModeMobilisation.UTILISER_LIEN_MOBILISATION in modes_mobilisation
            and not service_data["lien_mobilisation"]
        ):
            modes_mobilisation.remove(ModeMobilisation.UTILISER_LIEN_MOBILISATION)
        # Conversion des modes de mobilisation en modes d'orientation accompagnateur
        coach_orientation_mode_values = [
            MODE_MOBILISATION_DI_TO_DORA[mode] for mode in modes_mobilisation
        ]
        # Ajout du mode formulaire-dora si pas de mode utiliser-lien-mobilisation et si courriel existe
        if (
            ModeMobilisation.UTILISER_LIEN_MOBILISATION not in modes_mobilisation
            and service_data["courriel"]
        ):
            coach_orientation_mode_values.append("formulaire-dora")
        coach_orientation_modes = CoachOrientationMode.objects.filter(
            value__in=coach_orientation_mode_values
        )
        # Autres champs
        coach_orientation_modes_external_form_link = service_data["lien_mobilisation"]
        coach_orientation_modes_other = service_data["mobilisation_precisions"]
    elif service_data["courriel"]:
        coach_orientation_modes = CoachOrientationMode.objects.filter(
            value="formulaire-dora"
        )

    publics = None
    if service_data["publics"] is not None:
        publics = [
            Public(p)
            for p in (set(service_data["publics"]) & {p.value for p in Public})
        ]

    diffusion_zone_info = get_diffusion_zone_info(service_data["zone_eligibilite"])

    requirements = requirements_display = (
        [service_data["conditions_acces"]] if service_data["conditions_acces"] else None
    )

    return {
        "access_conditions": None,
        "access_conditions_display": None,
        "address1": service_data["adresse"],
        "address2": service_data["complement_adresse"],
        "address_line": address_to_one_line(
            service_data["adresse"],
            service_data["complement_adresse"],
            service_data["code_postal"],
            service_data["commune"],
        ),
        "beneficiaries_access_modes": [m.value for m in beneficiaries_access_modes]
        if beneficiaries_access_modes is not None
        else None,
        "beneficiaries_access_modes_display": [
            m.label for m in beneficiaries_access_modes
        ]
        if beneficiaries_access_modes is not None
        else None,
        "beneficiaries_access_modes_external_form_link": beneficiaries_access_modes_external_form_link,
        "beneficiaries_access_modes_external_form_link_text": "",
        "beneficiaries_access_modes_other": beneficiaries_access_modes_other,
        "can_write": False,
        "categories": [c.value for c in categories],
        "categories_display": [c.label for c in categories],
        "city": service_data["commune"],
        "city_code": service_data["code_insee"],
        "coach_orientation_modes": [m.value for m in coach_orientation_modes]
        if coach_orientation_modes is not None
        else None,
        "coach_orientation_modes_display": [m.label for m in coach_orientation_modes]
        if coach_orientation_modes is not None
        else None,
        "coach_orientation_modes_external_form_link": coach_orientation_modes_external_form_link,
        "coach_orientation_modes_external_form_link_text": "",
        "coach_orientation_modes_other": coach_orientation_modes_other,
        "publics": [p.value for p in publics] if publics is not None else None,
        "publics_display": [p.label for p in publics] if publics is not None else None,
        "contact_email": service_data["courriel"],
        "contact_name": service_data["contact_nom_prenom"],
        "contact_phone": service_data["telephone"],
        # double implémentation de cette valeur métier (voir modèle du service DORA) 😩
        "contact_info_filled": bool(
            service_data["courriel"] or service_data["telephone"]
        ),
        "creation_date": None,
        "credentials": [],
        "credentials_display": [],
        "department": department,
        "diffusion_zone_details": diffusion_zone_info["diffusion_zone_details"],
        "diffusion_zone_details_display": diffusion_zone_info[
            "diffusion_zone_details_display"
        ],
        "diffusion_zone_type": diffusion_zone_info["diffusion_zone_type"],
        "diffusion_zone_type_display": diffusion_zone_info[
            "diffusion_zone_type_display"
        ],
        "duration_weekly_hours": service_data["volume_horaire_hebdomadaire"],
        "duration_weeks": service_data["nombre_semaines"],
        "fee_condition": service_data["frais"],
        "fee_details": service_data["frais_precisions"],
        "forms": None,
        "forms_info": None,
        "full_desc": service_data["description"] or "",
        "funding_labels": [],
        "funding_labels_display": [],
        "geom": None,
        "has_already_been_unpublished": None,
        "is_available": True,
        "is_contact_info_public": True,
        "is_cumulative": None,
        "is_orientable": is_orientable(service_data),
        "is_model": False,
        "kinds": [kind.value] if kind is not None else None,
        "kinds_display": [kind.label] if kind is not None else None,
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
        "recurrence": service_data["horaires_accueil"],
        "remote_url": None,
        "requirements": requirements,
        "requirements_display": requirements_display,
        "short_desc": textwrap.shorten(
            service_data["description"], width=200, placeholder="…"
        )
        if service_data["description"]
        else "",
        "slug": service_data["id"],
        "source": service_data["source"],
        "status": ServiceStatus.PUBLISHED.value,
        "structure": service_data["structure_id"],
        "structure_info": {
            "name": service_data["structure"]["nom"],
            "city": service_data["structure"]["commune"],
            "department": structure_department,
            "phone": service_data["structure"]["telephone"],
            "email": service_data["structure"]["courriel"],
        },
        "subcategories": [c.value for c in subcategories],
        "subcategories_display": [c.label for c in subcategories],
        "suspension_date": None,
        "update_frequency": None,
        "update_frequency_display": None,
        "update_needed": update_needed,
        "use_inclusion_numerique_scheme": False,
        "is_orientable_ft_service": False,
    }
