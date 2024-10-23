import csv
import re

from django.core.management.base import BaseCommand

from dora.structures.emails import send_invitation_for_pe_members_email
from dora.structures.models import (
    Structure,
    StructureMember,
    StructurePutativeMember,
)
from dora.users.models import User

"""
Import des conseillers et admins de agences FT :
    - fichiers aux format CSV en entrée : un pour les admins, l'autre pour les conseillers
    - format : SAFIR,NOM,PRENOM,fonction (avec entête)

Les adresses e-mail sont déduites à partir du nom / prénom (si absentes).
"""


class ImportError(Exception):
    pass


def strip_accents(term: str) -> str:
    # "quelques lignes de code en plus valent mieux qu'une dépendance en plus"
    # (sinon on aurait pu utiliser `unicodedata`)

    result = re.sub(r"[àáâãäå]", "a", term)
    result = re.sub(r"[èéêë]", "e", result)
    result = re.sub(r"[ìíîï]", "i", result)
    result = re.sub(r"[òóôõö]", "o", result)
    result = re.sub(r"[ùúûü]", "u", result)

    return result


def to_pe_email(first_name: str, last_name: str) -> str:
    if not all([first_name, last_name]):
        raise ImportError(f"Erreur nom ou prénom : {first_name} - {last_name}")

    return f"{strip_accents(first_name.lower())}.{strip_accents(last_name.lower())}@francetravail.fr".replace(
        " ", "-"
    )


def structure_by_safir(safir: str) -> Structure | None:
    try:
        return Structure.objects.get(code_safir_pe=safir)
    except Structure.DoesNotExist as ex:
        raise ImportError(
            f"L'agence FT avec le code {safir} n'existe pas en base"
        ) from ex


def invite_user(structure, email, admin=True) -> str:
    def _maybe_upgrade_as_admin(member, admin: bool) -> str:
        if admin and not member.is_admin:
            member.is_admin = True
            member.save()
            return " (mais désormais en tant qu'admin)"
        return ""

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(
            email,
        )
    try:
        member = StructurePutativeMember.objects.get(user=user, structure=structure)
        result = f"{email} a déjà été invité·e"
        result += _maybe_upgrade_as_admin(member, admin)
    except StructurePutativeMember.DoesNotExist:
        try:
            member = StructureMember.objects.get(user=user, structure=structure)
            result = f"{email} est déjà membre de la structure"
            result += _maybe_upgrade_as_admin(member, admin)
        except StructureMember.DoesNotExist:
            member = StructurePutativeMember.objects.create(
                user=user,
                structure=structure,
                invited_by_admin=True,
                is_admin=admin,
            )

            result = f"{email} invité·e"
            if admin:
                result += " comme administrateur·rice"

            send_invitation_for_pe_members_email(
                member,
                "L’équipe DORA",
            )

    return result


class Command(BaseCommand):
    help = "Importe des administrateurs ou conseillers d'agence France Travail"

    def add_arguments(self, parser):
        parser.add_argument("filename")

        parser.add_argument(
            "--wet-run",
            action="store_true",
            help="Traitement *réel* du fichier d'entrée : ajout d'utilisateurs et envois d'e-mails",
        )
        parser.add_argument(
            "--admin",
            action="store_true",
            help="Crée des utilisateurs avec le statut d'aministrateur de structure",
        )

    def handle(self, *args, **options):
        filename = options["filename"]
        wet_run = options["wet_run"]
        admin = options["admin"]

        if wet_run:
            self.stdout.write(self.style.WARNING("PRODUCTION RUN"))
        else:
            self.stdout.write(self.style.NOTICE("DRY RUN"))

        with open(filename) as structures_file:
            reader = csv.DictReader(structures_file, delimiter=",")
            for i, row in enumerate(reader):
                try:
                    safir = row["SAFIR"]
                    structure = structure_by_safir(safir)
                    email = row.get("EMAIL") or to_pe_email(row["PRENOM"], row["NOM"])
                except Exception as ex:
                    self.stdout.write(
                        self.style.ERROR(f"Erreur de traitement L{i + 1}: {ex}")
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"{i}. Import pour l'agence avec le code SAFIR : {safir}"
                        )
                    )

                    if wet_run:
                        self.stdout.write(
                            self.style.NOTICE(
                                invite_user(structure, email, admin=admin)
                            )
                        )
