import csv
import sys
from types import SimpleNamespace

from django.db import transaction

from dora.services.models import ServiceModel, ServiceSource
from dora.services.utils import instantiate_model
from dora.structures.models import Structure
from dora.users.models import User
from dora.services.utils import update_geom

csv_file_path = "./cresus_services.csv"

# 💡 Mettre à True pour activer les écritures en base de données
dry_run = True

created_count = 0
error_count = 0

bot_user = User.objects.get_dora_bot()
source, _ = ServiceSource.objects.get_or_create(
    value="fichier-cresus",
    defaults={"label": "Fichier CSV des services de la fondation Cresus"},
)


def _extract_data_from_line(line):
    data = SimpleNamespace(
        modele_slug=line.get("modele_slug").strip(),
        structure_name=line.get("structure_name").strip(),
        structure_siret=line.get("structure_siret").replace(" ", "").strip(),
        contact_name=line.get("contact_name").strip(),
        contact_email=line.get("contact_email").strip(),
        contact_phone=line.get("contact_phone").replace(" ", "").strip(),
        location_kind=line.get("location_kind").strip(),
        location_city=line.get("location_city").strip(),
        location_address=line.get("location_address").strip(),
        location_complement=line.get("location_complement").strip(),
        location_postal_code=line.get("location_postal_code").replace(" ", "").strip(),
        diffusion_zone_type=line.get("diffusion_zone_type").strip(),
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

    if not dry_run:
        update_geom(service)

    service.save()


if dry_run:
    print("🧘 DRY RUN 🧘")
else:
    print("⚠️ PRODUCTION RUN ⚠️")

with open(csv_file_path, "r") as f:
    rdr = csv.reader(f)
    [headers, *lines] = rdr
    lines = [dict(zip(headers, line)) for line in lines]

try:
    with transaction.atomic():
        for idx, line in enumerate(lines, 1):
            try:
                print(f"\nTraitement de la ligne {idx} :")

                # Récupération des données
                data = _extract_data_from_line(line)

                # Vérification que le SIRET de la structure est bien renseigné
                if not data.structure_siret:
                    print("\tSIRET manquant. Ligne ignorée.", file=sys.stderr)
                    error_count += 1
                    continue

                # Vérification que la structure existe bien en BDD
                try:
                    structure = Structure.objects.get(siret=data.structure_siret)
                except Structure.DoesNotExist:
                    print(
                        f"\tStructure avec le SIRET {data.structure_siret} introuvable. Ligne ignorée.",
                        file=sys.stderr,
                    )
                    error_count += 1
                    continue

                # Vérification que le modèle de service existe lui aussi
                try:
                    model = ServiceModel.objects.get(slug=data.modele_slug)
                except ServiceModel.DoesNotExist:
                    print(
                        f"\tModèle de service avec le slug {data.modele_slug} introuvable. Ligne ignorée.",
                        file=sys.stderr,
                    )
                    error_count += 1
                    continue

                # Création du service
                print(
                    f"\tCréation d'un nouveau service pour la structure avec le SIRET '{data.structure_siret}'."
                )
                new_service = instantiate_model(model, structure, bot_user)
                _edit_and_save_service(new_service, data)
                created_count += 1
                print("\tService créé.")

            except Exception as e:
                print(f"\tErreur lors du traitement - {e}", file=sys.stderr)
                error_count += 1
                continue

        # Forcer un rollback si dry_run est activé
        if dry_run:
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
