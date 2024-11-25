import csv
import sys
from types import SimpleNamespace

from django.db import transaction

from dora.core.validators import ValidationError, validate_siret
from dora.sirene.models import Establishment
from dora.structures.emails import send_invitation_email
from dora.structures.models import (
    Structure,
    StructureMember,
    StructurePutativeMember,
    StructureSource,
)
from dora.users.models import User

# 💡 Mettre à True pour activer les écritures en base de données
wet_run = False

csv_file_path = "./cresus_structures.csv"

created_count = 0
ignored_count = 0
error_count = 0

bot_user = User.objects.get_dora_bot()
source, _ = StructureSource.objects.get_or_create(
    value="fichier-cresus",
    defaults={"label": "Fichier CSV des structures de la fondation Cresus"},
)


def _extract_data_from_line(line):
    data = SimpleNamespace(
        name=line.get("name").strip(),
        siret=line.get("siret").replace(" ", "").strip(),
        admin_email=line.get("admin_email").strip(),
        structure_email=line.get("structure_email").strip(),
        phone_number=line.get("phone_number").replace(" ", "").strip(),
        label=line.get("label").strip(),
        website=line.get("website").strip(),
        location_city=line.get("location_city").strip(),
        location_address=line.get("location_address").strip(),
        location_complement=line.get("location_complement").strip(),
        location_postal_code=line.get("location_postal_code").replace(" ", "").strip(),
    )
    return data


def _edit_and_save_structure(structure, data):
    structure.creator = bot_user
    structure.last_editor = bot_user
    structure.source = source
    structure.name = data.name
    structure.email = data.structure_email
    structure.phone = data.phone_number
    structure.url = data.website
    structure.save()


def _invite_structure_admin(structure, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(email)

    try:
        member = StructurePutativeMember.objects.get(user=user, structure=structure)
        print(f"\t{email} a déjà été invité·e")
        if not member.is_admin:
            member.is_admin = True
            member.save()
    except StructurePutativeMember.DoesNotExist:
        try:
            member = StructureMember.objects.get(user=user, structure=structure)
            print(f"\t{email} est déjà membre de la structure")

            if not member.is_admin:
                member.is_admin = True
                member.save()
        except StructureMember.DoesNotExist:
            member = StructurePutativeMember.objects.create(
                user=user,
                structure=structure,
                invited_by_admin=True,
                is_admin=True,
            )

            print(f"\t{email} invité·e comme administrateur·rice")
            send_invitation_email(member, "L’équipe DORA")


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
                print(f"\nTraitement de la ligne {idx + 1} :")

                # Récupération des données
                data = _extract_data_from_line(line)

                # Vérification que le SIRET est renseigné
                if not data.siret:
                    print(
                        "\tErreur : SIRET manquant ou vide. Ligne ignorée.",
                        file=sys.stderr,
                    )
                    error_count += 1
                    continue

                # Vérification que le SIRET est valide
                try:
                    validate_siret(data.siret)
                except ValidationError as e:
                    print(
                        f"\tErreur : SIRET invalide ({data.siret}) - {e}. Ligne ignorée.",
                        file=sys.stderr,
                    )
                    error_count += 1
                    continue

                # Vérification de l'email de l'admin
                if not data.admin_email:
                    print(
                        "\tErreur : Email de l'administrateur·ice manquant ou vide. Ligne ignorée.",
                        file=sys.stderr,
                    )
                    error_count += 1
                    continue

                # Vérification que la structure n'existe pas déjà
                structure = Structure.objects.filter(siret=data.siret).first()
                if structure:
                    print(f"\tStructure existante : '{structure.name}'. Ligne ignorée.")
                    ignored_count += 1
                    continue

                # Création de la structure
                print(f"\tCréation d'une nouvelle structure pour le SIRET {data.siret}")
                try:
                    establishment = Establishment.objects.get(siret=data.siret)
                    print(
                        f"\tÉtablissement trouvé pour le SIRET {data.siret}. Création à partir de celui-ci."
                    )
                    structure = Structure.objects.create_from_establishment(
                        establishment, data.name
                    )
                except Establishment.DoesNotExist:
                    print(
                        f"\tAucun établissement trouvé pour le SIRET {data.siret}. Création à partir des données CSV."
                    )
                    structure = Structure(name=data.name, siret=data.siret)

                _edit_and_save_structure(structure, data)

                if wet_run:
                    _invite_structure_admin(structure, data.admin_email)

                created_count += 1
                print("\tStructure créée.")

            except Exception as e:
                print(f"\tErreur inattendue - {e}", file=sys.stderr)
                error_count += 1
                continue

        # Forcer un rollback si dry_run est activé
        if not wet_run:
            raise Exception(
                "Mode dry-run activé. Toutes les modifications sont annulées."
            )

except Exception as e:
    if str(e) != "Mode dry-run activé. Toutes les modifications sont annulées.":
        print(f"Erreur critique : {e}", file=sys.stderr)

print("\n--------------------------------------------------")
print("Traitement du fichier CSV terminé.")
print(
    f"Résumé : {created_count} structures créées, {ignored_count} structures ignorées, {error_count} erreurs."
)
print("--------------------------------------------------\n")
