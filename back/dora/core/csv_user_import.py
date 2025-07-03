import re

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

# TODO: check headers
# TODO: check email?


class ImportUserHelper:
    def __init__(self):
        self.is_france_travail = False

    def import_france_travail_users(
        self,
        reader,
        wet_run=False,
        make_users_admin=False,
    ):
        if wet_run:
            print("PRODUCTION RUN")
        else:
            print("DRY RUN")

        errors = []
        for i, row in enumerate(reader):
            try:
                safir = row["safir"]
                structure = self._structure_by_safir(safir)
                email = row.get("email") or self.name_to_france_travail_email(
                    row["prenom"], row["nom"]
                )
                first_name = row.get("prenom")
                last_name = row.get("nom")
            except Exception as ex:
                line_number = i + 1
                print(f"Erreur de traitement Ligne {line_number}: {ex}")
                errors.append(line_number)
            else:
                print(f"{i}. Import pour l'agence avec le code SAFIR : {safir}")

                if not errors and wet_run:
                    print(
                        self.invite_user(
                            structure,
                            email,
                            first_name,
                            last_name,
                            is_france_travail=True,
                            admin=make_users_admin,
                        )
                    )

    def import_users(self, reader, wet_run=False, make_users_admin=False):
        errors = []

        if wet_run:
            print("PRODUCTION RUN")
        else:
            print("DRY RUN")

        for i, row in enumerate(reader):
            try:
                structure_siret = row.get("structure_siret")
                structure = self._structure_by_siret(structure_siret)
                email = row.get("email")
                first_name = row.get("prenom")
                last_name = row.get("nom")
            except Exception as ex:
                line_number = i + 1
                print(f"Erreur de traitement Ligne {line_number}: {ex}")
                errors.append(line_number)

            else:
                print(
                    f"{i}. Import pour la structure avec le SIRET : {structure_siret}"
                )

                if not errors and wet_run:
                    print(
                        self.invite_user(
                            structure,
                            email,
                            first_name,
                            last_name,
                            is_france_travail=False,
                            admin=make_users_admin,
                        )
                    )

    @staticmethod
    def _strip_accents(term: str) -> str:
        result = re.sub(r"[àáâãäå]", "a", term)
        result = re.sub(r"[èéêë]", "e", result)
        result = re.sub(r"[ìíîï]", "i", result)
        result = re.sub(r"[òóôõö]", "o", result)
        result = re.sub(r"[ùúûü]", "u", result)

        return result

    def name_to_france_travail_email(self, first_name: str, last_name: str) -> str:
        if not all([first_name, last_name]):
            raise Exception(f"Erreur nom ou prénom : {first_name} - {last_name}")

        return f"{self._strip_accents(first_name.lower())}.{self._strip_accents(last_name.lower())}@francetravail.fr".replace(
            " ", "-"
        )

    @staticmethod
    def _structure_by_siret(siret: str) -> Structure:
        try:
            return Structure.objects.get(siret=siret)
        except Structure.DoesNotExist as ex:
            raise Exception(
                f"La structure avec le SIRET {siret} n'existe pas en base"
            ) from ex

    @staticmethod
    def _structure_by_safir(safir: str) -> Structure | None:
        try:
            return Structure.objects.get(code_safir_pe=safir)
        except Structure.DoesNotExist as ex:
            raise Exception(
                f"L'agence FT avec le code {safir} n'existe pas en base"
            ) from ex

    def _get_structure(self, structure_id: str) -> Structure | None:
        filter_key = "code_safir_pe" if self.is_france_travail else "id"
        filter = {[filter_key]: structure_id}
        try:
            return Structure.objects.get(**filter)
        except Structure.DoesNotExist:
            raise Exception(
                f"La structure avec {'le code safir' if self.is_france_travail else "l'id"} : {structure_id} n'existe pas en base"
            )

    @staticmethod
    def _maybe_upgrade_as_admin(member, admin: bool) -> str:
        if admin and not member.is_admin:
            member.is_admin = True
            member.save()
            return " (mais désormais en tant qu'admin)"
        return ""

    def invite_user(
        self, structure, email, first_name, last_name, is_france_travail, admin=True
    ) -> str:
        try:
            user = User.objects.get_by_email(email)
        except User.DoesNotExist:
            user = User.objects.create_user(
                email,
            )
            user.first_name = first_name
            user.last_name = last_name
            user.save()
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

                result = f"{email} invité·e"
                if admin:
                    result += " comme administrateur·rice"

                inviter_name = "L’équipe DORA"

                if is_france_travail:
                    send_france_travail_invitation_email(
                        member,
                        inviter_name,
                    )
                else:
                    send_invitation_email(member, inviter_name)

        return result
