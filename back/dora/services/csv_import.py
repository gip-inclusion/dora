import sys
from types import SimpleNamespace

from django.db import transaction

from dora.admin_express.models import AdminDivisionType
from dora.core.utils import get_geo_data
from dora.services.enums import ServiceStatus
from dora.services.models import (
    FundingLabel,
    LocationKind,
    Service,
    ServiceModel,
    ServiceSource,
)
from dora.services.utils import instantiate_service_from_model
from dora.structures.models import Structure

CSV_HEADERS = [
    "modele_slug",
    "structure_siret",
    "contact_email",
    "diffusion_zone_type",
    "labels_financement",
    "contact_name",
    "contact_phone",
    "location_kinds",
    "location_city",
    "location_address",
    "location_complement",
    "location_postal_code",
    "is_contact_info_public",
]


def import_services(
    reader,
    importing_user,
    service_source,
    wet_run=False,
):
    created_count = 0
    errors = []
    geo_data_missing_lines = []
    duplicated_services = []
    draft_services_created = []

    if wet_run:
        print("⚠️ PRODUCTION RUN ⚠️")
    else:
        print("🧘 DRY RUN 🧘")

    [headers, *lines] = reader
    lines = [dict(zip(headers, line)) for line in lines]

    try:
        invalid_headers = set(headers) - set(CSV_HEADERS)
        if invalid_headers:
            return {
                "created_count": 0,
                "errors": [
                    f"En-têtes de colonnes invalides dans le fichier CSV : {', '.join(invalid_headers)}"
                ],
            }
        with transaction.atomic():
            for idx, line in enumerate(lines, 2):
                try:
                    print(f"\nTraitement de la ligne {idx} :")

                    data = _extract_data_from_line(line)

                    # Vérification que le SIRET de la structure est bien renseigné
                    if not data.structure_siret:
                        error_msg = f"[{idx}] SIRET manquant pour la structure."
                        print(
                            f"❌ {error_msg}",
                            file=sys.stderr,
                        )
                        errors.append(error_msg)
                        continue

                    # Vérification que la structure existe bien en BDD
                    try:
                        structure = Structure.objects.get(siret=data.structure_siret)
                    except Structure.DoesNotExist:
                        error_msg = f"[{idx}] Structure avec le SIRET {data.structure_siret} introuvable."
                        print(
                            f"❌ {error_msg}",
                            file=sys.stderr,
                        )
                        errors.append(error_msg)
                        continue

                    # Vérification que le modèle de service existe lui aussi
                    try:
                        model = ServiceModel.objects.get(slug=data.modele_slug)
                    except ServiceModel.DoesNotExist:
                        error_msg = f"[{idx}] Modèle de service avec le slug {data.modele_slug} introuvable."
                        print(
                            f"❌ {error_msg}",
                            file=sys.stderr,
                        )
                        errors.append(error_msg)
                        continue

                    print(
                        f"Création d'un nouveau service pour la structure avec le SIRET '{data.structure_siret}'."
                    )
                    new_service = instantiate_service_from_model(
                        model, structure, importing_user
                    )
                    _edit_and_save_service(
                        new_service,
                        data,
                        idx,
                        importing_user,
                        geo_data_missing_lines,
                        service_source,
                        draft_services_created,
                    )
                    if _is_service_duplicated(data):
                        duplicated_services.append(
                            {
                                "idx": idx,
                                "siret": data.structure_siret,
                                "model_slug": data.modele_slug,
                                "contact_email": data.contact_email,
                            }
                        )
                        print(
                            f"SIRET {data.structure_siret} - il existe déjà un service avec le modèle {data.modele_slug} et le courriel {data.contact_email}",
                            file=sys.stderr,
                        )
                    created_count += 1
                    print("✅ Service créé.")

                except Exception as e:
                    error_msg = f"[{idx}] {e}"
                    print(f"❌ {error_msg}", file=sys.stderr)
                    errors.append(error_msg)
                    continue

            if len(errors) > 0 and wet_run:
                created_count = 0
                raise Exception(
                    f"⚠️ {len(errors)} erreurs rencontrées lors du traitement du fichier CSV.\n"
                    "Toutes les modifications sont annulées."
                )

            if not wet_run:
                raise Exception(
                    "Mode dry-run activé. Toutes les modifications sont annulées."
                )

    except Exception as e:
        if str(e) != "Mode dry-run activé. Toutes les modifications sont annulées.":
            print(f"\nErreur critique : {e}", file=sys.stderr)

    print("\n--------------------------------------------------")
    print("Traitement du fichier CSV terminé.")
    print(f"Résumé : {created_count} services créés, {len(errors)} erreurs.")
    print(f"Lignes sans données géographiques : ({len(geo_data_missing_lines)})")
    print(f"Services dupliqués : ({len(duplicated_services)}):")
    print(f"Services en brouillon créés : ({len(draft_services_created)})")
    for entry in geo_data_missing_lines:
        print(
            f"Ligne {entry['idx']}: Adresse={entry['address']}, Ville={entry['city']}, "
            f"Code postal={entry['postal_code']}"
        )
    print("--------------------------------------------------\n")

    return {
        "created_count": created_count,
        "errors": errors,
        "geo_data_missing_lines": geo_data_missing_lines,
        "duplicated_services": duplicated_services,
        "draft_services_created": draft_services_created,
    }


def _extract_multiple_values_from_line(line, header_name, model, category_label):
    values = [
        label.strip() for label in line.get(header_name, "").split(",") if label.strip()
    ]

    if len(values) == 0:
        return []

    queryset = model.objects.filter(value__in=values)

    if queryset.count() != len(values):
        invalid_values = set(values) - set(queryset.values_list("value", flat=True))
        if len(invalid_values) > 0:
            raise ValueError(
                f"Un ou plusieurs {category_label} sont introuvables : {invalid_values}.",
            )
        raise ValueError(
            f"Un ou plusieurs {category_label} sont dupliqués.",
        )

    return queryset


def _extract_diffusion_zone_type_from_line(line):
    diffusion_zone_type_raw = line.get("diffusion_zone_type", "").strip()
    if not diffusion_zone_type_raw:
        return ""

    for choice in AdminDivisionType:
        if diffusion_zone_type_raw == choice.value:
            return choice

    raise ValueError(
        f"Type de zone de diffusion avec la valeur '{diffusion_zone_type_raw}' introuvable.",
    )


def _extract_data_from_line(line):
    data = SimpleNamespace(
        modele_slug=line.get("modele_slug").strip(),
        structure_siret=line.get("structure_siret").replace(" ", "").strip(),
        contact_name=line.get("contact_name").strip(),
        contact_email=line.get("contact_email").strip(),
        contact_phone=line.get("contact_phone").replace(" ", "").strip(),
        location_city=line.get("location_city").strip(),
        location_address=line.get("location_address").strip(),
        location_complement=line.get("location_complement").strip(),
        location_postal_code=line.get("location_postal_code").replace(" ", "").strip(),
        location_kinds=_extract_multiple_values_from_line(
            line, "location_kinds", LocationKind, "types d'accueil"
        ),
        funding_labels=_extract_multiple_values_from_line(
            line, "labels_financement", FundingLabel, "labels de financement"
        ),
        is_contact_info_public=line.get("is_contact_info_public", "").strip(),
        diffusion_zone_type=_extract_diffusion_zone_type_from_line(line),
    )
    return data


def _edit_and_save_service(
    service,
    data,
    idx,
    importing_user,
    geo_data_missing_lines,
    source_info,
    draft_services_created,
):
    service.creator = importing_user
    service.last_editor = importing_user
    service.contact_name = data.contact_name
    service.contact_email = data.contact_email
    service.contact_phone = data.contact_phone
    service.address1 = data.location_address
    service.address2 = data.location_complement
    service.city = data.location_city
    service.postal_code = data.location_postal_code
    service.location_kinds.set(data.location_kinds)
    service.diffusion_zone_type = data.diffusion_zone_type
    service.is_contact_info_public = data.is_contact_info_public.lower() == "oui"

    _set_service_source(service, source_info)

    if service.address1 and service.city and service.postal_code:
        geo_data = get_geo_data(
            service.address1, city=service.city, postal_code=service.postal_code
        )
        if geo_data:
            service.city_code = geo_data.city_code
            service.geom = geo_data.geom
            service.diffusion_zone_details = geo_data.city_code
        else:
            geo_data_missing_lines.append(
                {
                    "idx": idx,
                    "address": service.address1,
                    "city": service.city,
                    "postal_code": service.postal_code,
                }
            )

    if service.is_eligible_for_publishing():
        service.status = ServiceStatus.PUBLISHED
    else:
        missing_fields = service.get_missing_properties_for_publishing()
        draft_services_created.append(
            {
                "idx": idx,
                "name": service.name,
                "missing_fields": missing_fields,
            }
        )

    service.funding_labels.add(*data.funding_labels)

    service.save()


def _set_service_source(service, source_info):
    source, _ = ServiceSource.objects.get_or_create(
        value=source_info["value"],
        label=source_info["label"],
    )
    service.source = source


def _is_service_duplicated(data):
    return Service.objects.filter(
        structure__siret=data.structure_siret,
        model__slug=data.modele_slug,
        contact_email=data.contact_email,
    ).exists()
