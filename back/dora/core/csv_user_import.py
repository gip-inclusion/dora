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

"""
Import des conseillers et admins de agences FT :
    - fichiers aux format CSV en entrée : un pour les admins, l'autre pour les conseillers
    - format : SAFIR,NOM,PRENOM,fonction (avec entête)

Les adresses e-mail sont déduites à partir du nom / prénom (si absentes).
"""

# TODO: make idempotent
# TODO: check headers
# TODO: check email?


class ImportError(Exception):
    pass


class ImportUserHelper:
    def __init__(self):
        self.is_france_travail = False

    def import_france_travail_users(
        self,
        reader,
        wet_run=False,
        make_users_admin=False,
    ):
        for i, row in enumerate(reader):
            try:
                safir = row["SAFIR"]
                structure = self._structure_by_safir(safir)
                email = row.get("EMAIL") or self.name_to_france_travail_email(
                    row["PRENOM"], row["NOM"]
                )
                first_name = row.get("PRENOM")
                last_name = row.get("NOM")
            except Exception as ex:
                print(f"Erreur de traitement L{i + 1}: {ex}")
            else:
                print(f"{i}. Import pour l'agence avec le code SAFIR : {safir}")

                if wet_run:
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

    def import_users(self, reader, structure_id, wet_run=False, make_users_admin=False):
        structure = self._structure_by_id(structure_id)
        for i, row in enumerate(reader):
            try:
                email = row.get("EMAIL")
                first_name = row.get("PRENOM")
                last_name = row.get("NOM")
            except Exception as ex:
                print(f"Erreur de traitement L{i + 1}: {ex}")
            else:
                print(f"{i}. Import pour l'agence avec l'ID : {structure_id}")

                if wet_run:
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
            raise ImportError(f"Erreur nom ou prénom : {first_name} - {last_name}")

        return f"{self._strip_accents(first_name.lower())}.{self._strip_accents(last_name.lower())}@francetravail.fr".replace(
            " ", "-"
        )

    @staticmethod
    def _structure_by_id(id: str) -> Structure:
        try:
            return Structure.objects.get(id=id)
        except Structure.DoesNotExist as ex:
            raise ImportError(
                f"La structure avec l'ID {id} n'existe pas en base"
            ) from ex

    @staticmethod
    def _structure_by_safir(safir: str) -> Structure | None:
        try:
            return Structure.objects.get(code_safir_pe=safir)
        except Structure.DoesNotExist as ex:
            raise ImportError(
                f"L'agence FT avec le code {safir} n'existe pas en base"
            ) from ex

    def _get_structure(self, structure_id: str) -> Structure | None:
        filter_key = "code_safir_pe" if self.is_france_travail else "id"
        filter = {[filter_key]: structure_id}
        try:
            return Structure.objects.get(**filter)
        except Structure.DoesNotExist:
            raise ImportError(
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
