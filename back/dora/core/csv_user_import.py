import csv
import re
from typing import Dict, List

from dora.structures.emails import (
    send_france_travail_invitation_email,
    send_invitation_email,
)
from dora.structures.models import (
    Structure,
    StructureMember,
    StructurePutativeMember,
)
from dora.users.models import User


class ImportUserHelper:
    FRANCE_TRAVAIL_CSV_HEADERS = ["safir", "email", "prenom", "nom"]

    NON_FRANCE_TRAVAIL_CSV_HEADERS = ["structure_siret", "email", "prenom", "nom"]

    def import_france_travail_users(
        self,
        reader: csv.reader,
        wet_run: bool = False,
        make_users_admin: bool = False,
    ) -> None:
        errors = []
        users_to_import = []
        self._display_run_type(wet_run)

        [headers, *lines] = reader

        if self._check_headers(headers, self.FRANCE_TRAVAIL_CSV_HEADERS):
            return

        lines = [dict(zip(headers, line)) for line in lines]
        for index, row in enumerate(lines, 2):
            try:
                safir = row["safir"]
                structure = self._structure_by_safir(safir)
                email = row.get("email") or self._name_to_france_travail_email(
                    row["prenom"], row["nom"]
                )
                first_name = row.get("prenom")
                last_name = row.get("nom")

                users_to_import.append(
                    {
                        "structure": structure,
                        "email": email,
                        "first_name": first_name,
                        "last_name": last_name,
                    }
                )
            except Exception as ex:
                errors.append(f"[{index}]: {ex}")

        if errors:
            print("Il y a des erreurs qui empêchent l'import :")
            print(("\n".join(errors)))
            return

        for index, user in enumerate(users_to_import):
            print(
                f"{index}. Import {user['first_name']} {user['last_name']} pour l'agence avec le code SAFIR : {safir}"
            )
            if wet_run:
                self._import_user(
                    user,
                    is_france_travail=True,
                    admin=make_users_admin,
                )

    def import_users(
        self, reader: csv.reader, wet_run: bool = False, make_users_admin: bool = False
    ) -> None:
        errors = []
        users_to_import = []
        self._display_run_type(wet_run)

        [headers, *lines] = reader

        if self._check_headers(headers, self.NON_FRANCE_TRAVAIL_CSV_HEADERS):
            return

        lines = [dict(zip(headers, line)) for line in lines]

        for index, row in enumerate(lines, 2):
            try:
                structure_siret = row.get("structure_siret")
                structure = self._structure_by_siret(structure_siret)
                email = row.get("email").strip()
                first_name = row.get("prenom")
                last_name = row.get("nom")

                if not email:
                    raise Exception("An email is required")

                users_to_import.append(
                    {
                        "structure": structure,
                        "email": email,
                        "first_name": first_name,
                        "last_name": last_name,
                    }
                )

            except Exception as ex:
                errors.append(f"[{index}]: {ex}")

        if errors:
            print("Il y a des erreurs qui empêchent l'import :")
            print(("\n".join(errors)))
            return

        for index, user in enumerate(users_to_import):
            print(
                f"{index}. Import {user['first_name']} {user['last_name']} pour la structure avec le SIRET : {structure_siret}"
            )
            if wet_run:
                self._import_user(
                    user,
                    is_france_travail=False,
                    admin=make_users_admin,
                )

    @staticmethod
    def _structure_by_siret(siret: str) -> Structure:
        try:
            return Structure.objects.get(siret=siret)
        except Structure.DoesNotExist:
            raise Exception(f"La structure avec le SIRET {siret} n'existe pas en base")

    @staticmethod
    def _structure_by_safir(safir: str) -> Structure | None:
        try:
            return Structure.objects.get(code_safir_ft=safir)
        except Structure.DoesNotExist:
            raise Exception(f"L'agence FT avec le code {safir} n'existe pas en base")

    @staticmethod
    def _maybe_upgrade_as_admin(member, admin: bool) -> str:
        if admin and not member.is_admin:
            member.is_admin = True
            member.save()
            structure = member.structure
            structure.admin_already_invited = True
            structure.save(update_fields=["admin_already_invited"])
            return " (mais désormais en tant qu'admin)"
        return ""

    def _import_user(
        self, user: Dict[str, str], is_france_travail: bool, admin: bool = True
    ) -> None:
        email = user["email"]
        structure = user["structure"]

        try:
            user = User.objects.get_by_email(email)
        except User.DoesNotExist:
            user = self._create_new_user(user)
        try:
            member = StructurePutativeMember.objects.get(user=user, structure=structure)
            result = f"{email} a déjà été invité·e"
            result += self._maybe_upgrade_as_admin(member, admin)
        except StructurePutativeMember.DoesNotExist:
            try:
                member = StructureMember.objects.get(user=user, structure=structure)
                result = f"{email} est déjà membre de la structure"
                result += self._maybe_upgrade_as_admin(member, admin)
            except StructureMember.DoesNotExist:
                member = StructurePutativeMember.objects.create(
                    user=user,
                    structure=structure,
                    invited_by_admin=True,
                    is_admin=admin,
                )
                if admin:
                    structure.admin_already_invited = True
                    structure.save(update_fields=["admin_already_invited"])

                result = f"{email} invité·e"
                if admin:
                    result += " comme administrateur·rice"

                self._send_email_to_new_member(member, is_france_travail)

        print(result)

    @staticmethod
    def _create_new_user(user: Dict[str, str]) -> User:
        email = user["email"]
        first_name = user["first_name"]
        last_name = user["last_name"]

        user = User.objects.create_user(
            email,
        )
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return user

    @staticmethod
    def _send_email_to_new_member(
        member: StructurePutativeMember, is_france_travail: bool
    ) -> None:
        inviter_name = "L’équipe DORA"

        if is_france_travail:
            send_france_travail_invitation_email(
                member,
                inviter_name,
            )
        else:
            send_invitation_email(member, inviter_name)

    @staticmethod
    def _display_run_type(wet_run: bool) -> None:
        if wet_run:
            print("PRODUCTION RUN")
        else:
            print("DRY RUN")

    @staticmethod
    def _check_headers(
        actual_headers: List[str], expected_headers: List[str]
    ) -> set[str]:
        missing_headers = set(expected_headers) - set(actual_headers)
        if missing_headers:
            print(
                f"Les headers suivants sont manquants : ({', '.join(missing_headers)})"
            )

        return missing_headers

    @staticmethod
    def _strip_accents(term: str) -> str:
        result = re.sub(r"[àáâãäå]", "a", term)
        result = re.sub(r"[èéêë]", "e", result)
        result = re.sub(r"[ìíîï]", "i", result)
        result = re.sub(r"[òóôõö]", "o", result)
        result = re.sub(r"[ùúûü]", "u", result)
        result = re.sub(r"[ç]", "c", result)

        return result

    def _name_to_france_travail_email(self, first_name: str, last_name: str) -> str:
        if not all([first_name, last_name]):
            raise Exception(f"Erreur nom ou prénom : {first_name} - {last_name}")

        return f"{self._strip_accents(first_name.lower())}.{self._strip_accents(last_name.lower())}@francetravail.fr".replace(
            " ", "-"
        )
