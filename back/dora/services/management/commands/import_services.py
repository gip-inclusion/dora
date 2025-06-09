import csv
import sys
from types import SimpleNamespace

from django.core.management.base import BaseCommand
from django.db import transaction

from dora.admin_express.models import AdminDivisionType
from dora.core.utils import get_geo_data
from dora.services.enums import ServiceStatus
from dora.services.models import FundingLabel, LocationKind, ServiceModel, ServiceSource
from dora.services.utils import instantiate_model
from dora.structures.models import Structure
from dora.users.models import User


class Command(BaseCommand):
    help = "Créer des nouveaux services basés sur des modèles pour des structures en utilisant les infos fournies par un CSV"

    def add_arguments(self, parser):
        parser.add_argument("file_path", help="Le path du fichier csv à importer ")
        parser.add_argument(
            "--wet-run",
            help="Exécuter l'import en vrai (modifie la base de données)",
            default=False,
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        wet_run = bool(kwargs["wet_run"])
        bot_user = User.objects.get_dora_bot()

        with open(file_path, "r") as f:
            reader = csv.reader(f)
            import_services(reader, bot_user, wet_run)


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
                f"Un ou plusieurs {category_label} sont introuvables : {invalid_values}. Ligne ignorée.",
            )
        raise ValueError(
            f"Un ou plusieurs {category_label} sont dupliqués. Ligne ignorée.",
        )

    return queryset


def _extract_diffusion_zone_type_from_line(line):
    diffusion_zone_type_raw = line.get("diffusion_zone_type", "").strip()
    if not diffusion_zone_type_raw:
        return None

    for choice in AdminDivisionType:
        if diffusion_zone_type_raw == choice.label:
            return choice

    raise ValueError(
        f"Type de zone de diffusion avec la valeur '{diffusion_zone_type_raw}' introuvable. Valeur ignorée.",
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
        diffusion_zone_type=_extract_diffusion_zone_type_from_line(line),
    )
    return data


def _edit_and_save_service(
    service, data, idx, importing_user, geo_data_missing_lines, wet_run
):
    source, _ = ServiceSource.objects.get_or_create(
        value="fichier-xxx",
        defaults={
            "label": "Fichier CSV des services de XXX",
        },
    )

    service.creator = importing_user
    service.last_editor = importing_user
    service.source = source
    service.contact_name = data.contact_name
    service.contact_email = data.contact_email
    service.contact_phone = data.contact_phone
    service.address1 = data.location_address
    service.address2 = data.location_complement
    service.city = data.location_city
    service.postal_code = data.location_postal_code
    service.location_kinds.set(data.location_kinds)
    service.diffusion_zone_type = data.diffusion_zone_type

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

    if wet_run:
        service.funding_labels.add(*data.funding_labels)

        service.save()


def import_services(
    reader,
    importing_user,
    wet_run=False,
):
    created_count = 0
    errors = []
    geo_data_missing_lines = []

    if wet_run:
        print("⚠️ PRODUCTION RUN ⚠️")
    else:
        print("🧘 DRY RUN 🧘")

    [headers, *lines] = reader
    lines = [dict(zip(headers, line)) for line in lines]

    try:
        with transaction.atomic():
            for idx, line in enumerate(lines, 1):
                try:
                    print(f"\nTraitement de la ligne {idx} :")

                    ####################
                    # EXTRACT
                    ####################

                    data = _extract_data_from_line(line)

                    ####################
                    # TRANSFORM
                    ####################

                    # Vérification que le SIRET de la structure est bien renseigné
                    if not data.structure_siret:
                        error_msg = f"Erreur : SIRET manquant. Ligne {idx} ignorée."
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
                        error_msg = f"Erreur : Structure avec le SIRET {data.structure_siret} introuvable. Ligne {idx} ignorée."
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
                        error_msg = f"Erreur : Modèle de service avec le slug {data.modele_slug} introuvable. Ligne {idx} ignorée."
                        print(
                            f"❌ {error_msg}",
                            file=sys.stderr,
                        )
                        errors.append(error_msg)
                        continue

                    # Vérification du type de zone de diffusion (contrainte d'intégrité sur la table Services)
                    if not data.diffusion_zone_type:
                        error_msg = f"Erreur : Type de zone de diffusion manquant. Ligne {idx} ignorée."
                        print(
                            f"❌ {error_msg}",
                            file=sys.stderr,
                        )
                        errors.append(error_msg)
                        continue

                    # Vérification du type de zone de diffusion (contrainte d'intégrité sur la table Services)
                    if not data.diffusion_zone_type:
                        error_msg = f"Erreur : Type de zone de diffusion manquant. Ligne {idx} ignorée."
                        print(
                            f"❌ {error_msg}",
                            file=sys.stderr,
                        )
                        errors.append(error_msg)
                        continue

                    ####################
                    # LOAD
                    ####################

                    print(
                        f"Création d'un nouveau service pour la structure avec le SIRET '{data.structure_siret}'."
                    )
                    new_service = instantiate_model(model, structure, importing_user)
                    _edit_and_save_service(
                        new_service,
                        data,
                        idx,
                        importing_user,
                        geo_data_missing_lines,
                        wet_run,
                    )
                    created_count += 1
                    print("✅ Service créé.")

                except Exception as e:
                    error_msg = f"Erreur lors du traitement de la ligne {idx} - {e}"
                    print(f"❌ {error_msg}", file=sys.stderr)
                    errors.append(error_msg)
                    continue

            if not wet_run:
                raise Exception(
                    "Mode dry-run activé. Toutes les modifications sont annulées."
                )

    except Exception as e:
        if str(e) != "Mode dry-run activé. Toutes les modifications sont annulées.":
            print(f"Erreur critique : {e}", file=sys.stderr)

    print("\n--------------------------------------------------")
    print("Traitement du fichier CSV terminé.")
    print(f"Résumé : {created_count} services créés, {len(errors)} erreurs.")
    print(f"Lignes sans données géographiques ({len(geo_data_missing_lines)}) :")
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
    }
