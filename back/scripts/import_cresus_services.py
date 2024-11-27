import csv
import sys
from types import SimpleNamespace

from django.db import transaction

from dora.admin_express.models import AdminDivisionType
from dora.core.utils import get_geo_data
from dora.services.models import (
    LocationKind,
    ServiceModel,
    ServiceSource,
    ServiceStatus,
)
from dora.services.utils import instantiate_model
from dora.structures.models import Structure
from dora.users.models import User

csv_file_path = "./cresus_services_light.csv"

# 💡 Mettre à True pour activer les écritures en base de données
wet_run = False

created_count = 0
error_count = 0

bot_user = User.objects.get_dora_bot()
source, _ = ServiceSource.objects.get_or_create(
    value="fichier-cresus",
    defaults={"label": "Fichier CSV des services de la fondation Cresus"},
)


def _extract_location_kinds_from_line(line):
    location_kinds_raw = line.get("location_kinds", "").strip()
    if not location_kinds_raw:
        return []

    location_kinds_entities = {
        kind.label.lower(): kind for kind in LocationKind.objects.all()
    }

    location_kinds = []
    for entry in location_kinds_raw.split(","):
        cleaned_entry = entry.strip().lower()
        if cleaned_entry in location_kinds_entities:
            location_kinds.append(location_kinds_entities[cleaned_entry])
        else:
            print(
                f"\tType d'accueil avec la valeur '{entry.strip()}' introuvable. Valeur ignorée.",
                file=sys.stderr,
            )

    return location_kinds


def _extract_diffusion_zone_type_from_line(line):
    diffusion_zone_type_raw = line.get("diffusion_zone_type", "").strip()
    if not diffusion_zone_type_raw:
        return None

    for choice in AdminDivisionType:
        if diffusion_zone_type_raw == choice.label:
            return choice

    raise ValueError(
        f"\tType de zone de diffusion avec la valeur '{diffusion_zone_type_raw}' introuvable. Valeur ignorée.",
    )


def _extract_data_from_line(line):
    data = SimpleNamespace(
        modele_slug=line.get("modele_slug").strip(),
        structure_name=line.get("structure_name").strip(),
        structure_siret=line.get("structure_siret").replace(" ", "").strip(),
        contact_name=line.get("contact_name").strip(),
        contact_email=line.get("contact_email").strip(),
        contact_phone=line.get("contact_phone").replace(" ", "").strip(),
        location_kinds=_extract_location_kinds_from_line(line),
        location_city=line.get("location_city").strip(),
        location_address=line.get("location_address").strip(),
        location_complement=line.get("location_complement").strip(),
        location_postal_code=line.get("location_postal_code").replace(" ", "").strip(),
        diffusion_zone_type=_extract_diffusion_zone_type_from_line(line),
        diffusion_zone_city=line.get("diffusion_zone_city").strip(),
    )
    return data


def _edit_and_save_service(service, data):
    service.creator = bot_user
    service.last_editor = bot_user
    service.source = source
    service.contact_name = data.contact_name
    service.contact_email = data.contact_email
    service.contact_phone = data.contact_phone
    service.address1 = data.location_address
    service.address2 = data.location_complement
    service.city = data.location_city
    service.postal_code = data.location_postal_code
    service.status = ServiceStatus.PUBLISHED
    service.location_kinds.set(data.location_kinds)
    service.diffusion_zone_type = data.diffusion_zone_type

    if wet_run:
        geo_data = get_geo_data(
            service.address1, city=service.city, postal_code=service.postal_code
        )
        if geo_data:
            service.city_code = geo_data.city_code
            service.geom = geo_data.geom

        service.save()


if wet_run:
    print("⚠️ PRODUCTION RUN ⚠️")
else:
    print("🧘 DRY RUN 🧘")

with open(csv_file_path, "r") as f:
    rdr = csv.reader(f)
    [headers, *lines] = rdr
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
                    print(
                        "\t❌ Erreur : SIRET manquant. Ligne ignorée.", file=sys.stderr
                    )
                    error_count += 1
                    continue

                # Vérification que la structure existe bien en BDD
                try:
                    structure = Structure.objects.get(siret=data.structure_siret)
                except Structure.DoesNotExist:
                    print(
                        f"\t❌ Erreur : Structure avec le SIRET {data.structure_siret} introuvable. Ligne ignorée.",
                        file=sys.stderr,
                    )
                    error_count += 1
                    continue

                # Vérification que le modèle de service existe lui aussi
                try:
                    model = ServiceModel.objects.get(slug=data.modele_slug)
                except ServiceModel.DoesNotExist:
                    print(
                        f"\t❌ Erreur : Modèle de service avec le slug {data.modele_slug} introuvable. Ligne ignorée.",
                        file=sys.stderr,
                    )
                    error_count += 1
                    continue

                # Vérification du type de zone de diffusion (contrainte d'intégrité sur la table Services)
                if not data.diffusion_zone_type:
                    print(
                        "\t❌ Erreur : Type de zone de diffusion manquant. Ligne ignorée.",
                        file=sys.stderr,
                    )
                    error_count += 1
                    continue

                ####################
                # LOAD
                ####################

                print(
                    f"\tCréation d'un nouveau service pour la structure avec le SIRET '{data.structure_siret}'."
                )
                new_service = instantiate_model(model, structure, bot_user)
                _edit_and_save_service(new_service, data)
                created_count += 1
                print("\t✅ Service créé.")

            except Exception as e:
                print(f"\t❌ Erreur lors du traitement - {e}", file=sys.stderr)
                error_count += 1
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
print(f"Résumé : {created_count} services créés, {error_count} erreurs.")
print("--------------------------------------------------\n")
